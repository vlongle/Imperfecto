"""A demo for the regret-matching algorithm (Hart and Mas-Colell 2000) for various
N-player normal form games.

For 2-player zero-sum game, regret matching algorithm's average strategy provably converges to Nash.
However, it seems to work for more than 2-player games as well.

Usage:
    Run::

        $ python3 imperfecto/demos/regret_matching_demo.py --help

to print the available options.
"""

import logging
from pprint import pprint
from typing import Type

import click
import numpy as np

from imperfecto.algos.regret_matching import RegretMatchingPlayer
from imperfecto.games.bar_crowding import BarCrowdingGame
from imperfecto.games.game import ExtensiveFormGame
from imperfecto.games.prisoner_dilemma import PrisonerDilemmaGame
from imperfecto.games.rock_paper_scissor import (
    AsymmetricRockPaperScissorGame,
    RockPaperScissorGame,
)
from imperfecto.misc.evaluate import evaluate_strategies
from imperfecto.misc.trainer import NormalFormTrainer


def generate_random_prob_dist(n_actions: int) -> np.ndarray:
    """Generate a random probability distribution for a game.

    Args:
        n_actions: The number of actions in the game.

    Returns:
        A numpy array of shape (n_actions,).
    """
    return np.random.dirichlet(np.ones(n_actions), size=1)[0]


def verify_nash_strategy(Game: Type[ExtensiveFormGame], nash_strategy: np.ndarray,
                         n_iters: int = 10000, n_random_strategies: int = 5) -> None:
    """
    Verifies (roughly) that the given strategy is a Nash equilibrium. The idea of
    Nash strategy is only pplicable for 2-player (normal form).
    zero-sum games. We verify Nash strategy by pitting the strategy against random opponent's strategy.
    The Nash strategy should be unexploitable (i.e., having the payoff >= 0).

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

    strategies = [generate_random_prob_dist(
        len(Game.actions))for _ in range(n_random_strategies)]
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
    """Train all players simultaneously by the regret-matching algorithm and print the average
    strategies and payoffs.

    Args:
        Game: The game to train the players for.
        n_iters: The number of iterations to run the game for.
    """
    players = [RegretMatchingPlayer(name=f"RM{i}", n_actions=len(Game.actions))
               for i in range(Game.n_players)]
    trainer = NormalFormTrainer(Game, players, n_iters=n_iters)
    avg_payoffs = trainer.train()
    with np.printoptions(suppress=True, precision=2):
        print(
            f'Training regret-matching players for game {Game.__name__} after {n_iters} iters:')
        print('average strategies:')
        pprint(trainer.avg_strategies)
        print(f'eps_rewards: {avg_payoffs}')
        print()
    trainer.store_strategies(["strategy.json", "avg_strategy.json"])


def to_train_delay_regret_matching(Game: Type[ExtensiveFormGame], n_iters: int = 10000, freeze_duration: int = 10):
    """Train all players by the regret-matching algorithm and print the average strategies and payoffs.
    We alternatively freeze one player's strategy and train the other player(s). This is a process of
    co-evolution.

    Args:
        Game: The game to train the players for.
        n_iters: The number of iterations to run the game for.
        freeze_duration: The number of iterations to freeze the strategy of the player that is not being trained.
    """
    assert 0 < freeze_duration < n_iters
    # no. of intervals where someone is frozen
    freeze_interval = n_iters // freeze_duration
    players = [RegretMatchingPlayer(name=f"RM{i}", n_actions=len(Game.actions))
               for i in range(Game.n_players)]
    trainer = NormalFormTrainer(Game, players, n_iters=freeze_duration)
    for _ in range(freeze_interval):
        for i in range(Game.n_players):
            # train player i freezing the rest
            freeze_list = [player for player_id,
                           player in enumerate(players) if player_id != i]
            trainer.train(freeze_ls=freeze_list)

    with np.printoptions(suppress=True, precision=2):
        print(
            f'Training delay regret-matching players for game {Game.__name__} after {n_iters} iters:')
        print('average strategies:')
        pprint(trainer.avg_strategies)
        print(f'eps_rewards: {trainer.avg_payoffs}')
        print()
    trainer.store_strategies(["strategy.json", "avg_strategy.json"])


@click.command()
@click.option("--game", type=click.Choice(["RockPaperScissorGame", "AsymmetricRockPaperScissorGame", "BarCrowdingGame", "PrisonerDilemmaGame"]),
              default="RockPaperScissorGame", help="The game to demo.")
@click.option("--n_iters", type=int, default=10000, help="The number of iterations to run the game for.")
@click.option("--train_regret_matching", is_flag=True, default=False, help="Train regret matching players.")
@click.option("--train_delay_regret_matching", is_flag=True, default=False, help="Train delay regret matching players.")
@click.option("--verbose_level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]), default="INFO", help="The verbosity level of the game.")
@click.option("--seed", type=int, default=0, help="The random seed to use for the game.")
def main(game: str, n_iters: int = 10000, train_regret_matching: bool = False, train_delay_regret_matching: bool = False, verbose_level: str = "INFO", seed: int = 0) -> None:
    """Demo for N-player normal-form games using the regret-matching algorithm.

    Available games:
    ----------------

    RockPaperScissorGame, AsymmetricRockPaperScissorGame, BarCrowdingGame, PrisonerDilemmaGame

    Available options:
    ------------------

        --game: The game to demo.
        --n_iters: The number of iterations to run the game for.
        --train_regret_matching: Whether to train regret matching players.
        --train_delay_regret_matching: Whether to train delay regret matching players.

    We will also show the Nash equilibrium for 2-player zero-sum games so the user can verify that the regret matching players' strategies indeed converge to Nash.
    """
    logging.basicConfig(level=getattr(
        logging, verbose_level), format="%(message)s")
    np.random.seed(seed)
    Game_dict = {
        "RockPaperScissorGame": RockPaperScissorGame,
        "AsymmetricRockPaperScissorGame": AsymmetricRockPaperScissorGame,
        "BarCrowdingGame": BarCrowdingGame,
        "PrisonerDilemmaGame": PrisonerDilemmaGame,
    }
    nash_strategy_dict = {
        "RockPaperScissorGame": np.array([0.5, 0.5, 0.0]),
        "AsymmetricRockPaperScissorGame": np.array([0.5, 0.5, 0.0]),
    }
    Game = Game_dict[game]
    if game in nash_strategy_dict:
        nash_strategy = nash_strategy_dict[game]
        verify_nash_strategy(Game, nash_strategy, n_iters=n_iters)

    if train_regret_matching:
        to_train_regret_matching(Game, n_iters=n_iters)

    if train_delay_regret_matching:
        to_train_delay_regret_matching(Game, n_iters=n_iters)


if __name__ == "__main__":
    main()
