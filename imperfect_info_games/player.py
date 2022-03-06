"""A collection of player classes.

Includes:
    - Player
    - FixedPolicyPlayer
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Sequence

from imperfect_info_games.utils import get_action


class Player(ABC):
    """
    An abstract player class.

   Properties
   ----------
        - name (str): The name of the player.

    Abstract methods
    ----------------
        - get_action(self, infostate) -> action:
            Returns the action to take in this infostate.

    Optional methods
    ----------------
        - update_strategy(self, history) -> None:
            Updates the strategy of the player given the revealed history.
    """

    def __init__(self, name=""):
        self.name = name

    def __str__(self) -> str:
        if self.name == "":
            return self.__class__.__name__
        else:
            return "Agent(" + self.name + ")"

    def __repr__(self) -> str:
        if self.name is None:
            return self.__class__.__name__
        else:
            return "Agent(" + self.name + ")"

    @abstractmethod
    def act(self, infostate: str) -> int:
        """
        Returns the action to take in this infostate.

        Args:
            - infostate (str): The infostate to take the action in.

        Returns:
            - action (int): The action to take.
        """
        pass

    def update_strategy(self, history: Sequence[Enum], player_id: int) -> None:
        """Update the strategy of the player at the end of the game.

        Args:
            - history (Sequence[Enum]): The history of the game, which *must*
                be a terminal node.
            - player_id (int): The id of the player to update (i.e., my id).
        """
        del history, player_id
        pass

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, game):
        self._game = game


class FixedPolicyPlayer(Player):
    def __init__(self, name: str, strategy: dict):
        """
        Args:
            - name (str): The name of the player.
            - strategy (dict): A dictionary mapping infostates to action probability distributions i.e., key (str) and value (np.ndarray)
        """
        super().__init__(name)
        self.strategy = strategy

    def act(self, infostate: str) -> int:
        return get_action(self.strategy[infostate])
