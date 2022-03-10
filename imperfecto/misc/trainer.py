"""A class to train players in an extensive form game.

The players are trained over a number of games by calling each player's ``update_strategy`` method
after each game. The average payoffs and the average strategies during training are recorded.
"""
from typing import Sequence, Type

import numpy as np

import enlighten
from imperfecto.algos.player import Player
from imperfecto.games.game import ExtensiveFormGame


class Trainer:
    """A class to train players in an extensive form game.

    Args:
        Game: The game class to train players in.
        players: The players to train.
        n_iters: The number of games to train for.
        display_status_bar: Whether to display a status bar during training.

    Attributes:
        game (ExtensiveFormGame): The game to train players in.
        n_iter (int): The number of games to train for.
        ep_strategies (dict): The strategies of each player in each game.
        ep_payoffs (np.ndarray): The payoffs of each player in each game over the course of this trainer instance.
        display_status_bar (bool): Whether to display a status bar during training.
        manager (enlighten.Manager): The enlighten manager to display the status bar.
        pbar (enlighten.Counter): The enlighten counter to display the status bar.
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

        Note:
            Players in the ``freeze_ls`` list will not be trained.

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

    @property
    def avg_strategies(self) -> dict:
        """Get the average strategies of each player.

        Returns:
            dict: The average strategies of each player.
        """
        return {player: np.mean(strategies, axis=0) for player, strategies in self.ep_strategies.items()}
