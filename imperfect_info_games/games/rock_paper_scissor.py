"""A collection of 2-player rock paper scissor games.

This includes:
    - Standard Rock Paper Scissor
    - Asymmetric Rock Paper Scissor
"""
from enum import IntEnum
from typing import Sequence

from imperfect_info_games.games.game import NormalFormGame
from imperfect_info_games.utils import lessVerboseEnum


class ROCK_PAPER_SCISSOR_ACTIONS(lessVerboseEnum, IntEnum):
    """Available actions for the rock-paper-scissors game."""
    ROCK = 0
    PAPER = 1
    SCISSOR = 2


class RockPaperScissorGame(NormalFormGame):
    """A (standard) 2-player rock-paper-scissor (extensive-form) game.

    Payoff
    ------
    Rock beats scissors, scissors beats paper, and paper beats rock.
    Winner gets +1 payoff, loser gets -1 payoff.

    Nash Equilibrium
    ----------------
    The nash strategy (unexploitable) is (1/3, 1/3, 1/3) (payoff = 0 for all)
    """

    actions = ROCK_PAPER_SCISSOR_ACTIONS
    n_players = 2

    def get_payoffs(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> Sequence[float]:
        assert self.is_terminal(history)
        history_str = self.history_to_str(history)
        match history_str:
            case "ROCK-PAPER":
                return [-1, 1]
            case "ROCK-SCISSOR":
                return [1, -1]
            case "PAPER-ROCK":
                return [1, -1]
            case "PAPER-SCISSOR":
                return [-1, 1]
            case "SCISSOR-ROCK":
                return [-1, 1]
            case "SCISSOR-PAPER":
                return [1, -1]
        return [0, 0]


class AsymmetricRockPaperScissorGame(RockPaperScissorGame):
    """An asymmetric 2-player rock-paper-scissors (extensive-form) game.

    Payoff
    ------
    Rock beats scissors, scissors beats paper, and paper beats rock.
    **But** winner gets +2 payoff, loser gets -2 payoff when someone plays
    scissor. Otherwise, winner gets +1 payoff, loser gets -1 payoff.

    Nash Equilibrium
    ----------------
    The Nash strategy (unexploitable) is (0.4, 0.4, 0.2) (payoff = 0 for all)
    """

    def get_payoffs(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> Sequence[float]:
        """Override the get_payoffs function of standard rock-paper-scissors such that
        the winner gets +2 payoff, loser gets -2 payoff when someone plays scissor. Otherwise,
        winner gets +1 payoff, loser gets -1 payoff.

        Args:
            history: The history of the game.

        Returns:
            The payoffs of the players.
        """
        assert self.is_terminal(history)
        if len(history) > 2:
            raise ValueError("Invalid history " + str(history))

        history_str = self.history_to_str(history)
        match history_str:
            case "ROCK-PAPER":
                return [-1, 1]
            case "ROCK-SCISSOR":
                return [2, -2]
            case "PAPER-ROCK":
                return [1, -1]
            case "PAPER-SCISSOR":
                return [-2, 2]
            case "SCISSOR-ROCK":
                return [-2, 2]
            case "SCISSOR-PAPER":
                return [2, -2]
        return [0, 0]
