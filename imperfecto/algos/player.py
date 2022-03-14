"""A collection of player classes.

Includes:
    * Player
    * FixedPolicyPlayer
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Sequence

import numpy as np

from imperfecto.misc.utils import get_action


class Player(ABC):
    """
    An abstract player class.

   Attributes:
        name (str): The name of the player.
        strategy (dict): map from instostate to np.array of shape (n_actions,).
    """

    def __init__(self, name=""):
        self.name = name
        self.strategy = {}

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

    def act(self, infostate: str) -> int:
        """
        Returns the action to take given an infostate.

        Args:
            infostate: The infostate to take the action in.

        Returns:
            The action to take.
        """
        if infostate not in self.strategy:
            # uniform
            self.strategy[infostate] = np.ones(
                len(self.game.actions)) / len(self.game.actions)
        return get_action(self.strategy[infostate])

    @abstractmethod
    def update_strategy(self, history: Sequence[Enum], player_id: int) -> None:
        """Update the strategy of the player at the end of the game.

        Args:
            history: The history of the game, which *must* be a terminal node.
            player_id: The id of the player to update (i.e., my id).
        """
        pass

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, game):
        self._game = game

    @property
    def strategy(self):
        """A dict with key = infostate and value = np.array of shape (n_actions,)."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: dict):
        self._strategy = strategy


class NormalFormPlayer(Player, ABC):
    def __init__(self, name=""):
        super().__init__(name)
        self.name = name
        self.strategy = np.empty(0)

    @property
    def strategy(self):
        """A np.array of shape (n_actions,)."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: np.ndarray):
        self._strategy = strategy

    def act(self, infostate: str) -> int:
        del infostate
        if self.strategy.size == 0:
            # uniform strategy
            self.strategy = np.ones(
                len(self.game.actions)) / len(self.game.actions)
        return get_action(self.strategy)  # type: ignore


class FixedPolicyPlayer(Player):
    """A player with a given fixed strategy.

    Args:
        name: The name of the player.
        strategy: The fixed strategy of the player.

    Attributes:
        name (str): The name of the player.
        strategy (dict): The fixed strategy of the player.
    """

    def __init__(self, name: str, strategy: dict):
        super().__init__(name)
        self.strategy = strategy

    def update_strategy(self, history: Sequence[Enum], player_id: int) -> None:
        del history, player_id  # do nothing
        pass
