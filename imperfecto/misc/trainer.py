"""A class to train players in an extensive form game.

The players are trained over a number of games by calling each player's ``update_strategy`` method
after each game. The average payoffs and the average strategies during training are recorded.
"""
import logging
from typing import Sequence, Type

import numpy as np

import enlighten
from imperfecto.algos.player import Player
from imperfecto.games.game import ExtensiveFormGame
import pandas as pd


class NormalFormTrainer:
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
        num_spaces = 8 * self.game.n_players
        logging.debug(
            f"iter | history {' '* num_spaces} | payoffs")
        for i in range(self.n_iters):
            history, payoffs = self.game.play()
            ep_payoffs.append(payoffs)
            for player_id, player in enumerate(self.game.players):
                self.ep_strategies[player].append(
                    player.strategy)
                if player not in freeze_ls:
                    player.update_strategy(history, player_id)
            if self.display_status_bar:
                self.pbar.update()
            logging.debug(
                f"{i:4}  {self.game.history_to_str(history):{int(1.5 * num_spaces)}} {np.array2string(np.array(payoffs)):2}")
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

    def moving_avg(self, arr):
        """Compute the moving average of an array.

        Args:
            arr (np.ndarray): The array to compute the moving average of.

        Returns:
            np.ndarray: The moving average of the array.
        """
        avg = np.cumsum(arr, axis=0, dtype=float)
        discount = np.repeat(
            np.arange(1, arr.shape[0] + 1), arr.shape[1], axis=0).reshape(arr.shape)
        return avg / discount

    def store_strategies(self, filenames) -> None:
        """Store the average strategies of each player in a csv file.

        Args:
            filename (str): The name of the csv file to store the strategies in.
        """
        actions = list(map(str, self.game.actions))  # type: ignore
        dfs = []
        avg_dfs = []
        for player, strategies in self.ep_strategies.items():
            strategies = np.array(strategies)
            avg_strategies = self.moving_avg(strategies)
            df = pd.DataFrame(strategies, columns=actions)
            avg_df = pd.DataFrame(avg_strategies, columns=actions)
            df["player"] = player.name
            df["iter"] = df.index
            avg_df["player"] = player.name
            avg_df["iter"] = avg_df.index
            dfs.append(df)
            avg_dfs.append(avg_df)

        df = pd.concat(dfs, ignore_index=True)
        avg_df = pd.concat(avg_dfs, ignore_index=True)
        # write json to file
        df.to_json(filenames[0], orient='records', indent=2)
        avg_df.to_json(filenames[1], orient='records', indent=2)
