"""A class to train players in an extensive form game.

The players are trained over a number of games by calling each player's ``update_strategy`` method
after each game. The average payoffs and the average strategies during training are recorded.
"""
import logging
from typing import Sequence, Type

import enlighten
import numpy as np
import pandas as pd

from imperfecto.algos.player import Player
from imperfecto.games.game import ExtensiveFormGame


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
        self.ep_histories = []
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
            freeze_ls: The players to freeze during training.

        Returns:
            The average payoffs of each player during this `train` call.
        """
        num_spaces = 8 * self.game.n_players
        logging.debug(
            f"iter | history {' '* num_spaces} | payoffs")
        for i in range(self.n_iters):
            history, payoffs = self.game.play()
            self.ep_payoffs.append(payoffs)
            self.ep_histories.append(history)
            for player_id, player in enumerate(self.game.players):
                self.ep_strategies[player].append(
                    player.strategy)
                if player not in freeze_ls:
                    player.update_strategy(history, player_id)
            if self.display_status_bar:
                self.pbar.update()
            logging.debug(
                f"{i:4}  {self.game.history_to_str(history):{int(1.5 * num_spaces)}} {np.array2string(np.array(payoffs)):2}")
        return np.mean(self.ep_payoffs[-self.n_iters:], axis=0)

    @property
    def avg_payoffs(self) -> np.ndarray:
        """Get the average payoffs of each player over the course of this trainer instance.

        Returns:
            The average payoffs of each player.
        """
        return np.mean(self.ep_payoffs, axis=0)

    @property
    def avg_strategies(self) -> dict:
        """Get the average strategies of each player.

        Returns:
            The average strategies of each player.
        """

        return {player: np.mean(strategies, axis=0) for player, strategies in self.ep_strategies.items()}

    def moving_avg(self, arr: np.ndarray) -> np.ndarray:
        """Compute the moving average of an array.

        Args:
            arr: The 2D array to compute the moving average of. The first axis
            is iter / time.

        Returns:
            The moving average of the array.
        """
        avg = np.cumsum(arr, axis=0, dtype=float)
        discount = np.repeat(
            np.arange(1, arr.shape[0] + 1), arr.shape[1], axis=0).reshape(arr.shape)
        return avg / discount

    def make_df(self, strategies: np.ndarray, player_name: str) -> pd.DataFrame:
        """Make a dataframe from a strategy array.

        Args:
            strategies: The strategies to make a dataframe from.
            player_name: The name of the player.
        """
        actions = list(map(str, self.game.actions))  # type: ignore
        df = pd.DataFrame(strategies, columns=actions)
        df["player"] = player_name
        df["iter"] = df.index
        return df

    def store_strategies(self, filenames: dict) -> None:
        """Store the episodic strategies and average strategies of each player in json files.

        Args:
            filenames: The names of the json files to store the strategies and average strategies in.
                        Must have key 'strategy_file' and 'avg_strategy_file' and string values
                        corresponding to the file locations.
        """
        dfs = [self.make_df(np.array(strategies), player.name)
               for player, strategies in self.ep_strategies.items()]
        avg_dfs = [self.make_df(self.moving_avg(np.array(strategies)), player.name)
                   for player, strategies in self.ep_strategies.items()]
        df = pd.concat(dfs, ignore_index=True)
        avg_df = pd.concat(avg_dfs, ignore_index=True)
        # write json to file
        df.to_json(filenames['strategy_file'], orient='records', indent=2)
        avg_df.to_json(filenames['avg_strategy_file'],
                       orient='records', indent=2)

    def store_histories_payoffs(self, filenames: dict) -> None:
        """Store the episodic histories and payoffs of each player in json files.

        Args:
            filenames: The names of the json files to store the histories and payoffs in.
                        Must have key 'histories_payoffs_file'.
        """
        df = pd.DataFrame()
        df["history"] = list(
            map(lambda e: list(map(str, e)), self.ep_histories))
        df["payoffs"] = list(self.moving_avg(np.array(self.ep_payoffs)))
        df["iter"] = df.index
        df.to_json(filenames['histories_payoffs_file'],
                   orient='records', indent=2)

    def store_data(self, filenames: dict) -> None:
        """Record data about the training process.
        Args:
            filenames: The names of the json files to store data in.
        """
        self.store_strategies(filenames)
        self.store_histories_payoffs(filenames)
