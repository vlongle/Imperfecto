"""A collection of functions for evaluating strategies given a game.
"""
from typing import Sequence, Type

import numpy as np

from imperfect_info_games.games.game import ExtensiveFormGame
from imperfect_info_games.player import FixedPolicyPlayer


def evaluate_strategies(Game: Type[ExtensiveFormGame], strategies: Sequence[dict],
                        n_iters: int) -> Sequence[float]:
    """Evaluates a set of strategies on a game.

    Args:
        - game_cls (Type[ExtensiveFormGame]): The game class to evaluate the strategies on
                                            (e.g., `RockPaperScissorGame`).
        - strategies (Sequence[dict]): A list of strategies, each is a strategy for each player
                                        in the game.
                        (e.g.,
                            `player0_strat = {"P0": [1/3, 1/3, 1/3]} # equally likely rock-paper-scissor`
                            `player1_strat = {"P1": [0.4, 0.4, 0.2]}`
                            `strategies = [player0_strat, player1_strat]`
                        )
        - n_iters (int) : The number of iterations to run the game for.

    Returns:
        - payoffs (Sequence[float]): A list of the average payoffs of each strategy.
    """
    players = [FixedPolicyPlayer(str(i), strategy)
               for i, strategy in enumerate(strategies)]
    game = Game(players)
    avg_payoffs = []
    for _ in range(n_iters):
        _, payoffs = game.play()
        avg_payoffs.append(payoffs)

    return np.mean(avg_payoffs, axis=0)
