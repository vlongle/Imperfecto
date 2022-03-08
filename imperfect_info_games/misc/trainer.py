"""A class to train players in an extensive form game."""
from typing import Sequence, Type

import enlighten
import numpy as np

from imperfect_info_games.algos.player import Player
from imperfect_info_games.games.game import ExtensiveFormGame


class Trainer:
    """A class to train players in an extensive form game.

    Attributes:
        game (ExtensiveFormGame): The game to train players in.
        n_iter (int): The number of games to train for.
        ep_strategies (dict): The strategies of each player in each game.
        ep_payoffs (np.ndarray): The payoffs of each player in each game over the course of this trainer instance.
        display_status_bar (bool): Whether to display a status bar during training.
        manager (enlighten.Manager): The enlighten manager to display the status bar.
        pbar (enlighten.Counter): The enlighten counter to display the status bar.

        Args:
            Game (Type[ExtensiveFormGame]): The game to train players in. Must take `players` as the args to __init__ function.
            players (Sequence[Player]): The players to train.
            n_iters (int): The number of games to train for.
            display_status_bar (bool): Whether to display a status bar during training.
    Methods:
        train (Sequence[Player]): Train the players for `n_iter` games using each player's `update_strategy` function.
        get_avg_strategies (): Get the average strategies of each player.
    """

    def __init__(self, Game: Type[ExtensiveFormGame], players: Sequence[Player], n_iters: int = 100,
                 display_status_bar: bool = True):

        self.game = Game(players)
        self.n_iters = n_iters
        self.ep_strategies = {player: [] for player in self.game.players}
        self.ep_payoffs = []
        self.display_status_bar = display_status_bar
        if self.display_status_bar:
            self.manager = enlighten.get_manager()
            self.pbar = self.manager.counter(
                total=self.n_iters, desc=f'RM/{self.game.__class__.__name__}:', unit='ticks')

    def train(self, freeze_ls: Sequence[Player] = []) -> np.ndarray:
        """Train the players for `n_iter` games using each player's `update_strategy` function.

        Args:
            freeze_ls (Sequence[Player]): The players to freeze during training.

        Returns:
            np.ndarray: The average payoffs of each player during this `train` call.
        """
        ep_payoffs = []
        for _ in range(self.n_iters):
            history, payoffs = self.game.play()
            ep_payoffs.append(payoffs)
            for player_id, player in enumerate(self.game.players):
                # check if strategy is a property of the player object
                if hasattr(player, 'strategy'):
                    self.ep_strategies[player].append(
                        player.strategy)  # type: ignore
                if player not in freeze_ls:
                    player.update_strategy(history, player_id)
            if self.display_status_bar:
                self.pbar.update()
        self.ep_payoffs += ep_payoffs
        return np.mean(ep_payoffs, axis=0)

    @property
    def avg_payoffs(self) -> np.ndarray:
        """Get the average payoffs of each player over the course of this trainer instance.

        Returns:
            np.ndarray: The average payoffs of each player.
        """
        return np.mean(self.ep_payoffs, axis=0)

    def get_avg_strategies(self) -> dict:
        """Get the average strategies of each player.

        Returns:
            dict: The average strategies of each player.
        """
        return {player: np.mean(strategies, axis=0) for player, strategies in self.ep_strategies.items()}
