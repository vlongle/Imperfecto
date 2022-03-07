"""The implementation of Counterfactual regret minimization (CFR) algorithm.
(Zinkevich et al. "Regret minimization in games with incomplete information" 2008)

CFR is a self-play algorithm that assumes that the joint strategy of all players in the game is
public knowledge. The algorithm iteratively updates the regret of each player's action at each
information set. The average strategy of each player in CFR provably converges to a Nash equilibrium.

Counterfactual regrets are calculated by searching down the game tree, taking into account the
reach probabilities.

Reach probabilities are factored in since the nodes in one's player infostate might belong to
different infostates of their opponent. Therefore, not every node (history) in the infostate is
equally likely to be reached, so the reach probs should be taken into account to skew the action
distribution at that infostate appropriately.
"""

from enum import IntEnum
import logging
from typing import List

import enlighten
import numpy as np

from imperfect_info_games.algos.regret_matching import RegretMatchingPlayer
from imperfect_info_games.player import Player
from imperfect_info_games.utils import get_action


class CounterFactualRegretMinimizerPlayer(Player):
    """CounterFactualRegretMinimizerPlayer.

    Attributes
    ----------
        - player_id: int
            the player id of the player in the game.
        - cum_regrets: dict
            map from infostate to a regret vector of size n_actions
        - strategy_sum: dict
            map from infostate to the cumulative strategy at that infostate until now. Useful for
            calculating the average strategy over many iters

    Methods
    -------
        - act(self, infostate: str)
            returns the action to take at a given infostate.
        - get_avg_strategies(self)
            returns the average strategy of the player at each infostate.
        - strategy(self, infostate: str)
            returns the strategy for a given player at an infostate.
    """

    def __init__(self, name, player_id):
        super().__init__(name)
        self.player_id = player_id
        self.cum_regrets = {}  # map from infostate to a regret vector of size n_actions
        # map from infostate to the cumulative strategy at that info state until now. Useful for
        # calculating the average strategy over many iters
        self.strategy_sum = {}

    def strategy(self, infostate: str) -> np.ndarray:
        """the strategy for a given player at a infostate.

        Args:
            player (Player): player to get the strategy for.
            infostate (str): string representing the infostate

        Returns:
            action_probs (np.ndarray): array of shape (len(self.game.actions)) representing
            the action probability distribution.
        """
        cum_regrets = self.cum_regrets[infostate]
        return RegretMatchingPlayer.regret_matching_strategy(cum_regrets)

    def act(self, infostate: str) -> int:
        return get_action(self.strategy(infostate))

    def get_avg_strategies(self) -> dict:
        """Returns the average strategy of the player at each infostate.

        Returns:
            avg_strategies (dict): map from infostate to the average strategy at that infostate.
        """
        avg_strats = {}
        for infostate, strat_sum in self.strategy_sum.items():
            avg_strats[infostate] = RegretMatchingPlayer.regret_matching_strategy(
                strat_sum)
        return avg_strats


class counterfactualRegretMinimizerTrainer:
    """
    CFR (Zinkevich et al. "Regret minimization in games with incomplete information" 2008)
    is a self-play algorithm that assumes that the joint strategy of all players in the game is
    public knowledge. The algorithm iteratively updates the regret of each player's action at each
    information set. The average strategy of each player in CFR provably converges to a Nash equilibrium.

    Properties
    ----------
        - game: Game
            the game to train on.
        - n_iters: int
            the number of iterations to run CFR for.

    Methods
    -------
        - train(self)
            trains the game using CFR for `n_iters` iterations.
        - cfr(self, infostate: str, reach_probs: np.ndarray, player: Player,
            opponent: Player, reach_probs_opponent: np.ndarray)
            runs the CFR update step on a given infostate.
    """

    def __init__(self, game, n_iters: int):
        self.game = game
        self.n_iters = n_iters

    def cfr(self, history: List[IntEnum], reach_probs: np.ndarray) -> np.ndarray:
        """ Counterfactual regret minimization update step at the current node.

        CFR is quite similar to advantage function in classic Q-learning. For example,
            - node_utils ~ V(s)
            - counterfactual_values ~ Q(s, a)
            - regret ~ advantage function: Q(s, a) - V(s)

        Args:
            history (List[IntEnum]): list of actions taken so far (current node)
            reach_probs (np.ndarray): array of shape game.n_players. The reach probabilities for the
            current infostate (current node) played by the players' joint strategy.

        Returns:
            node_util (np.ndarray): the utility (expected payoff) of the current node for
            each player.
        """
        if self.game.is_terminal(history):
            return np.array(self.game.get_payoffs(history))
        active_player = self.game.get_active_player(history)
        active_player_id = active_player.player_id
        infostate = self.game.get_infostate(history)
        # create cum_regrets for the current infostate if it doesn't exist
        if infostate not in active_player.cum_regrets:
            active_player.cum_regrets[infostate] = np.zeros(
                len(self.game.actions))

        cur_policy = active_player.strategy(infostate)

        counterfactual_values = np.zeros(
            shape=(self.game.n_players, len(self.game.actions)))

        node_utils = np.zeros(self.game.n_players)
        for action in self.game.actions:
            new_reach_probs = reach_probs.copy()
            new_reach_probs[active_player_id] *= cur_policy[int(action)]
            counterfactual_values[:, action.value] = self.cfr(
                history + [action], new_reach_probs)

        for player_id in range(self.game.n_players):
            # dot product
            node_utils[player_id] = cur_policy @ counterfactual_values[player_id, :]

        # note that regrets for this node are weighted by reach_probability
        # assuming that the current player always plays to reach this infostate
        # discount = prod of reach_probs except the active_player_id entry
        discount = np.prod(reach_probs[:active_player_id]) * \
            np.prod(reach_probs[active_player_id + 1:])
        regrets = (counterfactual_values[active_player_id,
                   :] - node_utils[active_player_id]) * discount

        # update cumulative regrets, which affect the policy
        active_player.cum_regrets[infostate] += regrets

        # update strategy_sum
        if infostate not in active_player.strategy_sum:
            active_player.strategy_sum[infostate] = np.zeros(
                len(self.game.actions))
        active_player.strategy_sum[infostate] += reach_probs[active_player_id] * cur_policy

        logging.debug(
            f"{' ' * 6} {self.game.shorten_history(self.game.history_to_str(history)):5}\t"
            f"{np.array2string(reach_probs, precision=2, suppress_small=True):15} {active_player.name} \t\t"
            f"{self.game.shorten_history(infostate):5}\t"
            f"{np.array2string(counterfactual_values[active_player_id] - node_utils[active_player_id], precision=2, suppress_small=True):15}"
            f"\t  {np.array2string(cur_policy, precision=2, suppress_small=True)}")
        return node_utils

    def train(self) -> None:
        """Train the game using CFR for `n_iters` iterations."""
        utils = np.zeros(self.game.n_players)
        manager = enlighten.get_manager()
        pbar = manager.counter(
            total=self.n_iters, desc=f'CFR/{self.game.__class__.__name__}:', unit='ticks')
        logging.debug(
            'iter | hist | reach_prob | active_player | infostate |    regrets \t|   policy')
        logging.debug('-' * 82)
        for i in range(self.n_iters):
            logging.debug(i)
            history = []
            if hasattr(self.game, "has_chance_player") and self.game.has_chance_player:
                history = [self.game.chance_action()]
            utils += self.cfr(history, np.ones(len(self.game.players)))
            pbar.update()
        logging.debug('-' * 82)

        avg_strats = {player: player.get_avg_strategies()
                      for player in self.game.players}
        num_spaces = 2 * len(self.game.actions)
        logging.info(
            f"info_set |  avg_policy {' ' * num_spaces}|  avg_regrets")
        logging.info('-' * 82)
        for player in self.game.players:
            for info_set in player.cum_regrets:
                logging.info(
                    f"{self.game.shorten_history(info_set):10} {np.array2string(avg_strats[player][info_set], precision=2, suppress_small=True):{4  * num_spaces}}"
                    f"{np.array2string(player.cum_regrets[info_set]/self.n_iters, precision=2, suppress_small=True):{4 * num_spaces}}")

        logging.info('-' * 82)
        logging.info(
            f"Average utilities for Game {self.game.__class__.__name__} over {self.n_iters} iters: {np.array2string(utils/self.n_iters, precision=3, suppress_small=True)}")
