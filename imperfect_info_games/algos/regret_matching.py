"""A class of regret matching player for N-player normal form games.
See the paper "a simple adaptive procedure leading to correlated equilibrium" (2000)
by SERGIU HART AND ANDREU MAS-COLELL.
"""
from copy import copy
from enum import IntEnum
from typing import List

import numpy as np

from imperfect_info_games.player import Player
from imperfect_info_games.utils import get_action


class RegretMatchingPlayer(Player):
    """
    Regret Matching (Hart and Mas-Colell 2000) Player works by maintaining a cumulative
    regret vector for each action.

    The current regret is the difference between the counterfactual reward and the reward of
    the actual action taken.

    The policy is action distribution proportional to the positive entries of the cumulative regret vector.
    """

    def __init__(self, name: str, n_actions: int):
        super().__init__(name=name)
        self.n_actions = n_actions
        self.cum_regrets = np.zeros(self.n_actions)

    def __str__(self):
        return "Regret Matching Agent(" + self.name + ")"

    def __repr__(self):
        return "Regret Matching Agent(" + self.name + ")"

    @staticmethod
    def regret_matching_strategy(regrets: np.ndarray) -> np.ndarray:
        """Return the regret matching policy.

        Args:
            regrets(np.ndarray): cumulative regrets vector.

        Returns:
            action_probs(np.ndarray): action distribution according to regret-matching policy.
        """
        action_probs = np.where(regrets > 0, regrets, 0)
        if np.sum(action_probs) > 0:
            action_probs /= np.sum(action_probs)
        else:
            action_probs = np.ones(len(action_probs)) / len(action_probs)
        return action_probs

    @property
    def strategy(self):
        return self.regret_matching_strategy(self.cum_regrets)

    def act(self, infostate: str) -> int:
        del infostate
        return get_action(self.strategy)

    def update_strategy(self, history: List[IntEnum], player_id: int) -> None:
        """Update the cumulative regret vector. This will update the strategy of the player as
        the strategy is computed from the cumulative regret vector.

        Args:
            history(Sequence[]): history of the game.
            player_id(int): player id.
        """
        my_action = history[player_id]
        # compute counterfactual rewards
        counterfactual_rewards = np.zeros(self.n_actions)
        for action in range(self.n_actions):
            action = self.game.actions(action)  # int to action enum
            counterfactual_history = copy(history)
            # suppose player `player_id` has played `action`
            counterfactual_history[player_id] = action
            counterfactual_rewards[int(action)] = self.game.get_payoffs(
                counterfactual_history)[player_id]

        self.cum_regrets += counterfactual_rewards - \
            counterfactual_rewards[int(my_action)]
