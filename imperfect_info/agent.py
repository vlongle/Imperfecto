"""A collection of agent classes.

Includes:
    - Agent
    - FixedPolicyAgent
"""
from typing import Sequence
from enum import Enum
from abc import ABC, abstractmethod
from utils import get_action


class Agent(ABC):
    """
    Agent:
    - name (str)
    - game (Game) - the game the agent is playing
    - set_game(game) - sets the game the agent is playing
    - act() - returns the action the agent wants to take, using its policy
    - update_policy(actions, rewards) - updates the policy of the agent
    """

    def __init__(self, name="Mike Hunt"):
        self.name = name

    def __str__(self):
        return "Agent(" + self.name + ")"

    def __repr__(self):
        return "Agent(" + self.name + ")"

    def set_game(self, game):
        self.game = game

    @abstractmethod
    def act(self, history: Sequence[Enum]) -> int:
        """
        Return the action the agent wants to take (given its current policy)
        """
        pass

    @abstractmethod
    def update_policy(self, actions, rewards):
        """
        actions: dict with keys: agent class, values: action taken by that agent
        rewards: dict with keys: agent class, values: reward received by that agent
        Update the agent's internal policy
        """
        pass


class FixedPolicyAgent(Agent):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy

    def act(self):
        return get_action(self.policy)

    def update_policy(self, actions, rewards):
        del actions, rewards
        pass
