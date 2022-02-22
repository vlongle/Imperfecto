from enum import Enum
from regret_matching import RegretMatchingAgent
from game import TwoPlayerGame
from agent import Agent
import numpy as np
from utils import get_action
from tqdm import tqdm
np.random.seed(0)


class RockPaperScissor(Enum):
    ROCK = 0
    PAPER = 1
    SCISSOR = 2


class RockPaperScissorGame(TwoPlayerGame):
    def __init__(self, agents, n_steps=1000):
        super().__init__(agents, n_steps)
        for agent in agents:
            agent.set_game(self)

    def compute_rewards(self, actions):
        actions = [RockPaperScissor(action) for action in actions]
        action, opponent_action = actions
        rewards = []
        if action == opponent_action:
            rewards = [0, 0]
        elif action == RockPaperScissor.ROCK and opponent_action == RockPaperScissor.SCISSOR:
            rewards = [1, -1]
        elif action == RockPaperScissor.PAPER and opponent_action == RockPaperScissor.ROCK:
            rewards = [1, -1]
        elif action == RockPaperScissor.SCISSOR and opponent_action == RockPaperScissor.PAPER:
            rewards = [1, -1]
        else:
            rewards = [-1, 1]
        #print(f"compute_rewards({actions}) -> {rewards}")
        return rewards

    def compute_counterfactual_rewards(self, opponent_action):
        return np.array([self.compute_rewards([action, opponent_action])[0]
                         for action in RockPaperScissor])


class FixedPolicyAgent(Agent):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy

    def act(self):
        return get_action(self.policy)


if __name__ == '__main__':
    policies = []
    for i in tqdm(range(500)):
        regret_matching = RegretMatchingAgent(
            name='regret matching', n_actions=len(RockPaperScissor))
        opponent_policy = np.array([1/3, 1/3, 1/3])
        fixed_opponent = FixedPolicyAgent("fixed_opponent", opponent_policy)
        agents = [regret_matching, fixed_opponent]
        game = RockPaperScissorGame(agents, n_steps=1000)
        game.run()
        policies.append(regret_matching.policy)

    print('average policy', np.mean(policies, axis=0))
