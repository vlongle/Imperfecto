"""A 3-player bar-crowding game's version of El Farol Bar problem
(https://en.wikipedia.org/wiki/El_Farol_Bar_problem).

Reference:
----------
[Matthew Rouso's lecture](https://www.youtube.com/watch?v=P7Dg5FRH0cc)
"""

from enum import IntEnum
from typing import Sequence

from imperfect_info_games.games.game import NormalFormGame
from imperfect_info_games.utils import lessVerboseEnum


class BAR_CROWDING_ACTIONS(lessVerboseEnum, IntEnum):
    GO_TO_BAR = 0
    STAY_HOME = 1


class BarCrowdingGame(NormalFormGame):
    """A 3-player bar-crowding game's version of El Farol Bar problem
   (https://en.wikipedia.org/wiki/El_Farol_Bar_problem).

    Each player has two actions: go to the bar and stay at home. Each player wants to go to the bar
    but if all three of them go to the bar, the bar will be crowded. If only one player go to the bar,
    then they will feel lonely and silly. Ideally, exactly two players should go to the bar and have
    fun.

    Payoff
    -------
    If the bar is overcrowded, every player get a payoff of -1.
    If a player shows up and feel silly, they get a payoff of 0.
    If a player stays at home, they get a payoff of +1.
    If exactly two players go to the bar, they get a payoff of +2.

    Nash Equilibrium
    -----------------
    The pure Nash equilibria are
    1. All three stay at home.
    2. Three outcomes where exactly two players go to the bar, and one player stays at home.
    """
    actions = BAR_CROWDING_ACTIONS
    n_players = 3

    def get_payoffs(self, history: Sequence[BAR_CROWDING_ACTIONS]) -> Sequence[float]:
        assert self.is_terminal(history)
        history_str = self.history_to_str(history)
        match history_str:
            case "STAY_HOME-STAY_HOME-STAY_HOME":
                return [1, 1, 1]
            case "GO_TO_BAR-STAY_HOME-STAY_HOME":
                return [0, 1, 1]
            case "STAY_HOME-GO_TO_BAR-STAY_HOME":
                return [1, 0, 1]
            case "STAY_HOME-STAY_HOME-GO_TO_BAR":
                return [1, 1, 0]
            case "STAY_HOME-GO_TO_BAR-GO_TO_BAR":
                return [1, 2, 2]
            case "GO_TO_BAR-STAY_HOME-GO_TO_BAR":
                return [2, 1, 2]
            case "GO_TO_BAR-GO_TO_BAR-STAY_HOME":
                return [2, 2, 1]
            case "GO_TO_BAR-GO_TO_BAR-GO_TO_BAR":
                return [-1, -1, -1]
            case _:
                # default case
                raise ValueError("Invalid history " + str(history))
