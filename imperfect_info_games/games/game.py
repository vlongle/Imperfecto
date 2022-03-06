"""A collection of game classes.
"""
from abc import ABC, abstractmethod
from enum import Enum, EnumMeta
from typing import Sequence

from imperfect_info_games.player import Player


class ExtensiveFormGame(ABC):
    """Abstract class for extensive form games.

    Required properties
    -------------------
        - players (Sequence[Player]): The players of the game.
        - actions (EnumMeta): The actions of the game.

    Abstract methods
    -----------------
        - is_terminal(self, history) -> bool:
             Return whether the game is terminal.
        - get_payoffs(self, history) -> Sequence[float]:
             Return the payoffs of the players at the end of the game.
        - get_active_player(self, history) -> Player:
             Return the active player.
        - get_infostate(self, history) -> str
             Return the string representation of the infostate (information set) of the game.

    Implementation methods
    ----------------------
        - history_to_str(self, history) -> str:
            Return a string representation of the history of the game.
        - play(self) -> Sequence[float]:
            Play the game with the current players and their strategies and return the payoffs.
    """

    def __init__(self, players: Sequence[Player]):
        self._players = players

    @property
    def players(self) -> Sequence[Player]:
        """The players of the game."""
        return self._players

    @property
    def actions(self) -> EnumMeta:
        """The actions of the game.

        Example
        -------
        from utils import lessVerboseEnum

        class ROCK_PAPER_SCISSOR_ACTIONS(lessVerboseEnum):
            ROCK = 0
            PAPER = 1
            SCISSOR = 2
        ... # define some child class of ExtensiveFormGame
        game.actions = ROCK_PAPER_SCISSOR_ACTIONS
        """
        return self._actions

    @players.setter
    def players(self, val: Sequence[Player]) -> None:
        self._players = val

    @actions.setter
    def actions(self, val: EnumMeta) -> None:
        self._actions = val

    @abstractmethod
    def get_active_player(self, history: Sequence[Enum]) -> Player:
        """Get the active player of the game at the current decision point.

        Args:
            - history (Sequence[Enum]): The history of the game.

        Returns:
            - player (Player): The active player of the game at the current decision point.
        """
        pass

    @abstractmethod
    def is_terminal(self, history: Sequence[Enum]) -> bool:
        """Check if the game is in a terminal state.

        Args:
            - history (Sequence[Enum]): The history of the game.

        Returns:
            - is_terminal (bool): True if the game is in a terminal state, False otherwise.
        """
        pass

    @abstractmethod
    def get_payoffs(self, history: Sequence[Enum]) -> Sequence[float]:
        """Return the payoff for each player at the current node. This node *must* be a terminal node.
        Args:
            - history (Sequence[Enum]): The history of the game.

        Returns:
            - payoffs (Sequence[float]): The payoffs of the players at the end of the game.
        """
        pass

    @abstractmethod
    def get_infostate(self, history: Sequence[Enum]) -> str:
        """Return the infostate (i.e. the information set) of the game.

        Args:
            - history (Sequence[Enum]): The history of the game.

        Returns:
            - infostate (str): A string representation of the infostate of the game.
        """
        pass

    def history_to_str(self, history: Sequence[Enum]) -> str:
        """Return a string representation of the history of the game.

        Args:
            - history (Sequence[Enum]): The history of the game.

        Returns:
            - history_str (str): A string representation of the history of the game.
        """
        return '-'.join(str(action) for action in history)

    def play(self) -> Sequence[float]:
        """
        Play the game with the current players and their strategies and return the payoffs.

        Returns:
            - payoffs (Sequence[float]): The payoffs of the players at the end of the game.
        """
        history = []
        while not self.is_terminal(history):
            active_player = self.get_active_player(history)
            infostate = self.get_infostate(history)
            action = getattr(self, "actions")(active_player.act(
                infostate))  # convert int to action enum
            history.append(action)
        return self.get_payoffs(history)
