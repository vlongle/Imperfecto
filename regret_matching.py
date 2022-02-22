from agent import Agent
import numpy as np
from utils import get_action


def get_action(action_probs):
    return np.random.choice(range(len(action_probs)), p=action_probs)


class RegretMatchingAgent(Agent):
    def __init__(self, name, n_actions):
        super().__init__(name)
        self.n_actions = n_actions
        self.cum_regrets = np.zeros(self.n_actions)

    def __str__(self):
        return "Regret Matching Agent(" + self.name + ")"

    def __repr__(self):
        return "Regret Matching Agent(" + self.name + ")"

    @staticmethod
    def regret_matching_policy(regrets):
        action_probs = np.where(regrets > 0, regrets, 0)
        if np.sum(action_probs) > 0:
            action_probs /= np.sum(action_probs)
        else:
            action_probs = np.ones(len(action_probs)) / len(action_probs)
        return action_probs

    @property
    def policy(self):
        return self.regret_matching_policy(self.cum_regrets)

    def act(self):
        return get_action(self.policy)

    def update_policy(self, actions, player_rewards):
        my_action = actions[self]
        opponent_name = actions.keys() - {self}
        opponent_action = actions[opponent_name.pop()]
        # compute counterfactual rewards
        counterfactual_rewards = self.game.compute_counterfactual_rewards(
            opponent_action)
        # print(
        #     f"my_action = {my_action}; opponent_action = {opponent_action}; regret = {counterfactual_rewards - counterfactual_rewards[my_action]} ")
        self.cum_regrets += counterfactual_rewards - \
            counterfactual_rewards[my_action]
