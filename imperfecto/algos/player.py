"""A collection of player classes.

Includes:
    * Player
    * FixedPolicyPlayer
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Sequence

from imperfecto.misc.utils import get_action


class Player(ABC):
    """
    An abstract player class.

   Attributes:
        name (str): The name of the player.
    """

    def __init__(self, name=""):
        self.name = name

    def __str__(self) -> str:
        if self.name == "":
            return self.__class__.__name__
        else:
            return "Player(" + self.name + ")"

    def __repr__(self) -> str:
        if self.name is None:
            return self.__class__.__name__
        else:
            return "Player(" + self.name + ")"

    @abstractmethod
    def act(self, infostate: str) -> int:
        """
        Returns the action to take given an infostate.

        Args:
            infostate: The infostate to take the action in.

        Returns:
            The action to take.
        """
        pass

    def update_strategy(self, history: Sequence[Enum], player_id: int) -> None:
        """Update the strategy of the player at the end of the game.

        Args:
            history: The history of the game, which *must* be a terminal node.
            player_id: The id of the player to update (i.e., my id).
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
    """A player with a given fixed strategy.

    Args:
        name (str): The name of the player.
        strategy (dict): The fixed strategy of the player.

    Attributes:
        name (str): The name of the player.
        strategy (dict): The fixed strategy of the player.
    """

    def __init__(self, name: str, strategy: dict):
        super().__init__(name)
        self.strategy = strategy

    def act(self, infostate: str) -> int:
        return get_action(self.strategy[infostate])
