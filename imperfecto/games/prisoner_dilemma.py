"""A 2-player vintage Prisoner's Dilemma game (https://en.wikipedia.org/wiki/Prisoner%27s_dilemma).

This is a classic paradox in game theory where a stable outcome (i.e., a Nash equilibrium) is worse
off for both players.
"""
from enum import IntEnum
from typing import Sequence

from imperfecto.games.game import NormalFormGame
from imperfecto.misc.utils import lessVerboseEnum


class PRISONER_DILEMMA_ACTIONS(lessVerboseEnum, IntEnum):
    """Available actions in the Prisoner's Dilemma game."""
    SNITCH = 0
    SILENCE = 1


class PrisonerDilemmaGame(NormalFormGame):
    """A 2-player vintage classical Prisoner's Dilemma game.
    (https://en.wikipedia.org/wiki/Prisoner%27s_dilemma)

    Two players are crime partners in a robbery. They were arrested by the police but the police
    has no evidence to convict them. So the police commisioner sits each player on a separate room
    and offers them a deal. If one player confesses and snitches against the other, the confessor
    will go free and their partner will receive 3 years. If both players stay silent, they will serve
    1 year for another mirror crime that the police was able to catch. However, if both of them betray
    each other, they will both serve 2 years.

    Payoff:
        * If both silence, get 1 year each.
        * If both betray, get 2 years each.
        * If one silence and one snitches, the snitch goes free and the silent partner gets 3 years.

    Nash Equilibria:
        The only Nash Equilibrium is when both players snitch. (payoff = -2 for both)
    """

    actions = PRISONER_DILEMMA_ACTIONS
    n_players = 2

    def get_payoffs(self, history: Sequence[PRISONER_DILEMMA_ACTIONS]) -> Sequence[float]:
        assert self.is_terminal(history)
        history_str = self.history_to_str(history)
        match history_str:
            case 'SNITCH-SNITCH':
                return [-2, -2]
            case 'SILENCE-SILENCE':
                return [-1, -1]
            case 'SILENCE-SNITCH':
                return [-3, 0]
            case 'SNITCH-SILENCE':
                return [0, -3]
            case _:
                # default case
                raise ValueError("Invalid history " + str(history))
