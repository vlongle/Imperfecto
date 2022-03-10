# -*- coding: utf-8 -*-
"""A collection of base game classes.

Classes:
    * ExtensiveFormGame
    * NormalFormGame
"""
from abc import ABC, abstractmethod
from enum import EnumMeta, IntEnum
from typing import Sequence, Tuple

from imperfecto.algos.player import Player


class ExtensiveFormGame(ABC):
    """Abstract class for extensive form games.

    In an extensive form game, players have some private information, and are unsure
    about the true state of the world.

    Note:
        ``ExtensiveFormGame`` subclass must have class-level attribute ``actions``, and
        ``n_players``.

    Args:
        players: The players of the game.

    Attributes:
        actions: The actions of the game (class-level attribute).
        n_players: The number of players in the game (class-level attribute).
        players (Sequence[Player]): The players of the game.
    """

    n_players: int
    actions: EnumMeta

    def __init__(self, players: Sequence[Player]):
        self.players = players

    @property
    def players(self) -> Sequence[Player]:
        """The players of the game."""
        return self._players

    @players.setter
    def players(self, val: Sequence[Player]) -> None:
        self._players = val
        # setting game for each player
        for player in self._players:
            player.game = self

    @abstractmethod
    def get_active_player(self, history: Sequence[IntEnum]) -> Player:
        """Get the active player of the game at the current decision point.

        Args:
            history: The history of the game.

        Returns:
            The active player of the game at the current decision point.
        """
        pass

    @abstractmethod
    def is_terminal(self, history: Sequence[IntEnum]) -> bool:
        """Check if the game is in a terminal state.

        Args:
            history: The history of the game.

        Returns:
            True if the game is in a terminal state, False otherwise.
        """
        pass

    @abstractmethod
    def get_payoffs(self, history: Sequence[IntEnum]) -> Sequence[float]:
        """Return the payoff for each player at the current node.

        Note:
            history must be a terminal node.

        Args:
            history: The history of the game.

        Returns:
            The payoffs of the players at the end of the game.
        """
        pass

    @abstractmethod
    def get_infostate(self, history: Sequence[IntEnum]) -> str:
        """Return the infostate (i.e. the information set) of the game.

        Args:
            history: The history of the game.

        Returns:
            A string representation of the infostate of the game.
        """
        pass

    def history_to_str(self, history: Sequence[IntEnum]) -> str:
        """Return a string representation of the history of the game.

        Args:
            history: The history of the game.

        Returns:
            A string representation of the history of the game.
        """
        return '-'.join(str(action) for action in history)

    def play(self) -> Tuple[Sequence[IntEnum], Sequence[float]]:
        """
        Play the game with the current players and their strategies and return the payoffs.

        Returns:
            A tuple of the play-out history of the game and the payoffs of the players.
        """
        history = []
        while not self.is_terminal(history):
            active_player = self.get_active_player(history)
            infostate = self.get_infostate(history)
            action = getattr(self, "actions")(active_player.act(
                infostate))  # convert int to action enum
            history.append(action)
        return history, self.get_payoffs(history)

    @staticmethod
    def shorten_history(history_str: str) -> str:
        """Shorten history string. Games with long action names should
        override this method.

        Args:
            history_str: history string to shorten.

        Returns:
            a shortened history string.
        """
        return history_str


class NormalFormGame(ExtensiveFormGame, ABC):
    """N-player normal form game.

    This class of game is a special form of extensive-form games. A normal form game involves every
    player making simultaneous moves. Thus, they are unsure about each other's move.

    Args:
        players: The players of the game.
    """

    def __init__(self, players: Sequence[Player]):
        assert len(players) == self.n_players
        super().__init__(players)

    def is_terminal(self, history: Sequence[IntEnum]) -> bool:
        return len(history) == self.n_players

    def get_infostate(self, history: Sequence[IntEnum]) -> str:
        info_str_dict = {i: f"P{i}" for i in range(self.n_players)}
        if len(history) not in range(self.n_players):
            raise ValueError("Invalid history " + str(history))
        return info_str_dict[len(history)]

    def get_active_player(self, history: Sequence[IntEnum]) -> Player:
        if len(history) not in range(self.n_players):
            raise ValueError("Invalid history " + str(history))
        return self.players[len(history)]
