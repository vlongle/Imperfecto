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
        """
        Compute the rewards for each of the agent's possible action given the opponent's (fixed) action.
        """
        return np.array([self.compute_rewards([action, opponent_action])[0]
                         for action in RockPaperScissor])


class FixedPolicyAgent(Agent):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy

    def act(self):
        return get_action(self.policy)


def play_against_fixed_policy():
    """
    regret-matching agent plays against a fixed policy agent in
    rock-paper-scissor.
    """
    policies = []
    for _ in tqdm(range(500)):
        regret_matching = RegretMatchingAgent(
            name='regret matching', n_actions=len(RockPaperScissor))
        #opponent_policy = np.array([1/3, 1/3, 1/3])
        opponent_policy = np.array([0.34, 0.33, 0.33])
        fixed_opponent = FixedPolicyAgent("fixed_opponent", opponent_policy)
        agents = [regret_matching, fixed_opponent]
        game = RockPaperScissorGame(agents, n_steps=5000)
        game.run()
        policies.append(regret_matching.policy)

    print('average policy', np.mean(policies, axis=0))


def play_against_regret_matching():
    """
    both agents are regret-matching agents.
    Their avg policies should both converge to a Nash equilibrium,
    which is [1/3, 1/3, 1/3] for rock-paper-scissor.
    """
    policies = [[], []]
    for _ in tqdm(range(500)):
        regret_matching_1 = RegretMatchingAgent(
            name='regret matching 1', n_actions=len(RockPaperScissor))
        regret_matching_2 = RegretMatchingAgent(
            name='regret matching 2', n_actions=len(RockPaperScissor))
        agents = [regret_matching_1, regret_matching_2]
        game = RockPaperScissorGame(agents, n_steps=1000)
        game.run()
        policies[0].append(regret_matching_1.policy)
        policies[1].append(regret_matching_2.policy)

    print('average policy 1', np.mean(policies[0], axis=0))
    print('average policy 2', np.mean(policies[1], axis=0))


def play_against_delay_regret_matching():
    """
    both agents are regret-matching agents. We delay the policy update of one agent
    while updating the other for several games.
    Their avg policies should both converge to a Nash equilibrium,
    which is [1/3, 1/3, 1/3] for rock-paper-scissor.
    """
    regret_matching_1 = RegretMatchingAgent(
        name='regret matching 1', n_actions=len(RockPaperScissor))
    regret_matching_2 = RegretMatchingAgent(
        name='regret matching 2', n_actions=len(RockPaperScissor))
    agents = [regret_matching_1, regret_matching_2]
    game = RockPaperScissorGame(agents, n_steps=1000)
    policies = [[], []]
    for i in range(40):
        for _ in range(100):
            # freeze second agent, to train first agent
            game.run(freeze_ls=[regret_matching_2])
            policies[0].append(regret_matching_1.policy)
            policies[1].append(regret_matching_2.policy)
        for _ in range(100):
            # freeze first agent, to train second agent
            game.run(freeze_ls=[regret_matching_1])
            policies[0].append(regret_matching_1.policy)
            policies[1].append(regret_matching_2.policy)

        winner = np.argmax(game.eps_rewards[i])
        print('iter', i, np.mean(
            policies[0], axis=0), np.mean(policies[1], axis=0), winner)


if __name__ == '__main__':
    play_against_delay_regret_matching()
