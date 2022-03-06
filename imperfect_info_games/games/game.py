"""A collection of game classes.
"""
from abc import ABC, abstractmethod
from enum import EnumMeta, IntEnum
from typing import Sequence, Tuple

from imperfect_info_games.player import Player


class ExtensiveFormGame(ABC):
    """Abstract class for extensive form games.

    Required class properties
    -------------------
        - actions (EnumMeta): The actions of the game.
        - n_players (int): The number of players in the game.

    Required instance properties
    -------------------
        - players (Sequence[Player]): The players of the game.

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
        - play(self) -> Tuple[Sequence[IntEnum], Sequence[float]]:
            Play the game with the current players and their strategies and return the payoffs.
    """

    actions: EnumMeta
    n_players: int

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
            - history (Sequence[IntEnum]): The history of the game.

        Returns:
            - player (Player): The active player of the game at the current decision point.
        """
        pass

    @abstractmethod
    def is_terminal(self, history: Sequence[IntEnum]) -> bool:
        """Check if the game is in a terminal state.

        Args:
            - history (Sequence[IntEnum]): The history of the game.

        Returns:
            - is_terminal (bool): True if the game is in a terminal state, False otherwise.
        """
        pass

    @abstractmethod
    def get_payoffs(self, history: Sequence[IntEnum]) -> Sequence[float]:
        """Return the payoff for each player at the current node. This node *must* be a terminal node.
        Args:
            - history (Sequence[IntEnum]): The history of the game.

        Returns:
            - payoffs (Sequence[float]): The payoffs of the players at the end of the game.
        """
        pass

    @abstractmethod
    def get_infostate(self, history: Sequence[IntEnum]) -> str:
        """Return the infostate (i.e. the information set) of the game.

        Args:
            - history (Sequence[IntEnum]): The history of the game.

        Returns:
            - infostate (str): A string representation of the infostate of the game.
        """
        pass

    def history_to_str(self, history: Sequence[IntEnum]) -> str:
        """Return a string representation of the history of the game.

        Args:
            - history (Sequence[IntEnum]): The history of the game.

        Returns:
            - history_str (str): A string representation of the history of the game.
        """
        return '-'.join(str(action) for action in history)

    def play(self) -> Tuple[Sequence[IntEnum], Sequence[float]]:
        """
        Play the game with the current players and their strategies and return the payoffs.

        Returns:
            - history (Sequence[IntEnum]): The history of the game.
            - payoffs (Sequence[float]): The payoffs of the players at the end of the game.
        """
        history = []
        while not self.is_terminal(history):
            active_player = self.get_active_player(history)
            infostate = self.get_infostate(history)
            action = getattr(self, "actions")(active_player.act(
                infostate))  # convert int to action enum
            history.append(action)
        return history, self.get_payoffs(history)


class NormalFormGame(ExtensiveFormGame, ABC):
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
