from regret_matching import RegretMatchingAgent
from game import TwoPlayerNormalFormGame
from agent import FixedPolicyAgent
import numpy as np
from utils import lessVerboseEnum
from pprint import pprint
np.random.seed(0)


class ROCK_PAPER_SCISSOR_ACTIONS(lessVerboseEnum):
    ROCK = 0
    PAPER = 1
    SCISSOR = 2


class RockPaperScissorGame(TwoPlayerNormalFormGame):
    def __init__(self, agents, n_steps=1000):
        super().__init__(agents, n_steps)
        for agent in agents:
            agent.set_game(self)

    def compute_rewards(self, actions):
        actions = [ROCK_PAPER_SCISSOR_ACTIONS(action) for action in actions]
        action, opponent_action = actions
        rewards = []
        if action == opponent_action:
            rewards = [0, 0]
        elif action == ROCK_PAPER_SCISSOR_ACTIONS.ROCK and opponent_action == ROCK_PAPER_SCISSOR_ACTIONS.SCISSOR:
            rewards = [1, -1]
        elif action == ROCK_PAPER_SCISSOR_ACTIONS.PAPER and opponent_action == ROCK_PAPER_SCISSOR_ACTIONS.ROCK:
            rewards = [1, -1]
        elif action == ROCK_PAPER_SCISSOR_ACTIONS.SCISSOR and opponent_action == ROCK_PAPER_SCISSOR_ACTIONS.PAPER:
            rewards = [1, -1]
        else:
            rewards = [-1, 1]
        return rewards

    def compute_counterfactual_rewards(self, opponent_action):
        """
        Compute the rewards for each of the agent's possible action given the opponent's (fixed) action.
        """
        return np.array([self.compute_rewards([action, opponent_action])[0]
                         for action in ROCK_PAPER_SCISSOR_ACTIONS])


def play_against_fixed_policy():
    """
    regret-matching agent plays against a fixed policy agent in
    rock-paper-scissor.
    """
    n_steps = 10000
    regret_matching = RegretMatchingAgent(
        name='regret matching', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
    opponent_policy = np.array([1/3, 1/3, 1/3])
    #opponent_policy = np.array([0.34, 0.33, 0.33])
    fixed_opponent = FixedPolicyAgent("fixed_opponent", opponent_policy)
    agents = [regret_matching, fixed_opponent]
    game = RockPaperScissorGame(agents, n_steps=n_steps)
    game.run()
    print(f'avg strats after {n_steps} steps')
    pprint(game.get_avg_strats())
    print(f'eps_rewards {game.get_avg_rewards()}')


def play_against_regret_matching():
    """
    both agents are regret-matching agents.
    Their avg policies should both converge to a Nash equilibrium,
    which is [1/3, 1/3, 1/3] for rock-paper-scissor.
    """
    n_steps = 10000
    regret_matching_1 = RegretMatchingAgent(
        name='regret matching 1', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
    regret_matching_2 = RegretMatchingAgent(
        name='regret matching 2', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
    agents = [regret_matching_1, regret_matching_2]
    game = RockPaperScissorGame(agents, n_steps=n_steps)
    game.run()
    print(f'avg strats after {n_steps} steps')
    pprint(game.get_avg_strats())
    print(f'eps_rewards {game.get_avg_rewards()}')


def play_against_delay_regret_matching():
    """
    both agents are regret-matching agents. We delay the policy update of one agent
    while updating the other for several games.
    Their avg policies should both converge to a Nash equilibrium,
    which is [1/3, 1/3, 1/3] for rock-paper-scissor.
    """
    n_steps = 10000
    freeze_interval = 50
    freeze_duration = n_steps // freeze_interval  # no. of games per freeze interval
    regret_matching_1 = RegretMatchingAgent(
        name='regret matching 1', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
    regret_matching_2 = RegretMatchingAgent(
        name='regret matching 2', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
    agents = [regret_matching_1, regret_matching_2]
    game = RockPaperScissorGame(agents, n_steps=freeze_duration)
    for _ in range(freeze_interval):
        # evolve first agent, freeze 2nd
        game.run(freeze_ls=[regret_matching_2])
        # evolve second agent, freeze 1st
        game.run(freeze_ls=[regret_matching_1])

    print(f'avg strats after {n_steps} steps')
    pprint(game.get_avg_strats())
    print(f'eps_rewards {game.get_avg_rewards()}')


if __name__ == '__main__':
    play_against_delay_regret_matching()
    # play_against_fixed_policy()
    # play_against_regret_matching()
