"""A demo for rock paper scissor games.

Usage
-----
`python3 rock_paper_scissor.py --help`
to print the options available.

`python3 rock_paper_scissor.py --game=<game>`
where <game> is one of ['RockPaperScissorGame', 'AsymmetricRockPaperScissorGame'].

"""
from pprint import pprint
from typing import Type

import click
import numpy as np

from imperfect_info_games.algos.regret_matching import RegretMatchingPlayer
from imperfect_info_games.evaluate import evaluate_strategies
from imperfect_info_games.games.game import ExtensiveFormGame
from imperfect_info_games.games.rock_paper_scissor import (
    AsymmetricRockPaperScissorGame,
    RockPaperScissorGame,
)
from imperfect_info_games.trainer import Trainer
np.random.seed(0)


def verify_nash_strategy(Game: Type[ExtensiveFormGame], nash_strategy: np.ndarray,
                         n_iters: int = 10000) -> None:
    """
    Verifies that the given strategy is a Nash equilibrium.

    Args:
        Game: The game to verify the strategy for.
        nash_strategy: The strategy to verify.
        n_iters: The number of iterations to run the game for.
    """
    print(f"In {Game.__name__}, the nash strategy {nash_strategy} is unexploitable by "
          "any other strategy.")
    print("That means that it will always have 0 payoff against all strategy[p, q, 1-p-q]. Do the math with the "
          "normal form game matrix to convince yourself that this is true.")
    print("In this example, we will fix P0 strategy to be nash strategy, and vary P1 strategy")
    print("\n")
    P0_uniform_strategy = {"P0": nash_strategy}

    strategies = [np.array([1/3, 1/3, 1/3]), np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0]),
                  np.array([0.5, 0.5, 0.0]), np.array([0.5, 0.0, 0.5]), np.array([0.0, 0.5, 0.5]), np.array([0.4, 0.4, 0.2])]
    print("P1 strategy \t \t payoff")
    print("-" * 40)
    with np.printoptions(suppress=True, precision=2):
        for strat in strategies:
            P1_strategy = {"P1": strat}
            avg_payoffs = evaluate_strategies(Game, [
                P0_uniform_strategy, P1_strategy], n_iters=n_iters)
            print(f"{np.array2string(strat):20} \t {avg_payoffs}")
    print()


def to_train_regret_matching(Game: Type[ExtensiveFormGame], n_iters: int = 10000) -> None:
    """Train both players by the regret-matching algorithm and print the average strategies and payoffs.

    Args:
        Game: The game to train the players for.
        n_iters: The number of iterations to run the game for.
    """
    regret_matching_0 = RegretMatchingPlayer(
        name='RM0', n_actions=len(Game.actions))
    regret_matching_1 = RegretMatchingPlayer(
        name='RM1', n_actions=len(Game.actions))
    players = [regret_matching_0, regret_matching_1]
    trainer = Trainer(Game, players, n_iters=n_iters)
    avg_payoffs = trainer.train()
    print(
        f'Training regret-matching players for game {Game.__name__} after {n_iters} iters:')
    print('average strategies')
    pprint(trainer.get_avg_strategies())
    print(f'eps_rewards {avg_payoffs}')
    print()


def to_train_delay_regret_matching(Game: Type[ExtensiveFormGame], n_iters: int = 10000, freeze_duration: int = 10):
    """Train both players by the regret-matching algorithm and print the average strategies and payoffs.
    We alternatively freeze one player's strategy and train the other player. This is a process of
    co-evolution.

    Args:
        Game: The game to train the players for.
        n_iters: The number of iterations to run the game for.
        freeze_duration: The number of iterations to freeze the strategy of the player that is not being trained.
    """
    assert 0 < freeze_duration < n_iters
    # no. of intervals where someone is frozen
    freeze_interval = n_iters // freeze_duration
    regret_matching_1 = RegretMatchingPlayer(
        name='RM0', n_actions=len(Game.actions))
    regret_matching_2 = RegretMatchingPlayer(
        name='RM1', n_actions=len(Game.actions))
    agents = [regret_matching_1, regret_matching_2]
    trainer = Trainer(Game, agents, n_iters=freeze_duration)
    for _ in range(freeze_interval):
        # evolve RM0, freeze RM1
        trainer.train(freeze_ls=[regret_matching_2])
        # evolve second agent, freeze 1st
        trainer.train(freeze_ls=[regret_matching_1])

    print(
        f'Training delay regret-matching players for game {Game.__name__} after {n_iters} iters:')
    print('average strategies')
    pprint(trainer.get_avg_strategies())
    print(f'eps_rewards {trainer.avg_payoffs}')
    print()


@click.command()
@click.option("--game", type=click.Choice(["RockPaperScissorGame", "AsymmetricRockPaperScissorGame"]),
              default="RockPaperScissorGame", help="The game to demo.")
@click.option("--n_iters", type=int, default=10000, help="The number of iterations to run the game for.")
@click.option("--train_regret_matching", is_flag=True, default=False, help="Train regret matching players.")
@click.option("--train_delay_regret_matching", is_flag=True, default=False, help="Train delay regret matching players.")
def main(game: str, n_iters: int = 10000, train_regret_matching: bool = False, train_delay_regret_matching: bool = False):
    """Demo for rock-paper-scissor games.

    Available games:
    ----------------

    RockPaperScissorGame, AsymmetricRockPaperScissorGame

    Available options:
    ------------------

        --game: The game to demo.
        --n_iters: The number of iterations to run the game for.
        --train_regret_matching: Whether to train regret matching players.
        --train_delay_regret_matching: Whether to train delay regret matching players.

    We will also show the Nash equilibrium for the game so the user can verify that the regret matching
    players' strategies indeed converge to Nash.
    """
    Game = RockPaperScissorGame if game == "RockPaperScissorGame" else AsymmetricRockPaperScissorGame
    nash_strategy = np.array(
        [1/3, 1/3, 1/3]) if game == "RockPaperScissorGame" else np.array([0.4, 0.4, 0.2])
    verify_nash_strategy(Game, nash_strategy, n_iters=n_iters)

    if train_regret_matching:
        to_train_regret_matching(Game, n_iters=n_iters)

    if train_delay_regret_matching:
        to_train_delay_regret_matching(Game, n_iters=n_iters)


if __name__ == "__main__":
    main()
