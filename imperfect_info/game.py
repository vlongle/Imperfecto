from abc import ABC, abstractmethod
import numpy as np
import enlighten


class TwoPlayerNormalFormGame(ABC):
    """
    A class that represents a two player game. (normal-form game)
    - agents: a list of agent objects
    - n_steps: number of steps to run the game for
    - compute_rewards(actions): a function that takes in the actions of the agents and returns a list of rewards
    - step(): play one game
    - run(): play the game for n_steps
    """

    def __init__(self, agents, n_steps=100):
        assert(len(agents) == 2)
        self.agents = agents
        self.n_steps = n_steps
        self.eps_rewards = []
        self.strats = {agent: [] for agent in agents}
        self.manager = enlighten.get_manager()

    @abstractmethod
    def compute_rewards(self, actions):
        """
        Compute the rewards for the agents given the actions.
        Args:
            actions: a list of actions
        Return:
            a list of rewards
        """
        pass

    def step(self, freeze_ls=[]):
        """
        Play one game.
         - get actions
         - get rewards
         - update policies
        Args:
            freeze_ls (optional): a list of agent not `freeze`. These agents' policies will not be updated.
        """
        actions = [agent.act() for agent in self.agents]
        rewards = self.compute_rewards(actions)
        self.eps_rewards.append(rewards)
        # associate names with actions and rewards
        actions = dict(zip(self.agents, actions))
        rewards = dict(zip(self.agents, rewards))  # type: ignore
        for agent in self.agents:
            if agent not in freeze_ls:
                agent.update_policy(actions, rewards)

    def run(self, freeze_ls=[]):
        """
        Play the game for n_steps.
        Args:
            freeze_ls (optional): a list of agent not `freeze`. These agents' policies will not be updated.
        """
        pbar = self.manager.counter(
            total=self.n_steps, desc=type(self).__name__, unit='ticks')
        for _ in range(self.n_steps):
            self.step(freeze_ls)
            for agent in self.agents:
                self.strats[agent].append(agent.policy.copy())
            pbar.update()

    def get_avg_strats(self):
        return {agent: np.mean(strats, axis=0) for agent, strats in self.strats.items()}

    def get_avg_rewards(self):
        return np.mean(self.eps_rewards, axis=0)


class extensiveFormGame(ABC):
    @property
    def players(self):
        return self._players

    @property
    def actions(self):
        return self._actions

    @property
    def has_chance_player(self):
        return self._has_chance_player

    @players.setter
    def players(self, val):
        self._players = val

    @actions.setter
    def actions(self, val):
        self._actions = val

    @has_chance_player.setter
    def has_chance_player(self, val):
        self._has_chance_player = val

    @abstractmethod
    def get_active_player(self, history):
        pass

    @abstractmethod
    def is_terminal(self, history):
        pass

    @abstractmethod
    def get_payoffs(self, history):
        pass

    @abstractmethod
    def get_opponent(self, active_player):
        pass

    @abstractmethod
    def get_infostate(self, active_player, history):
        pass
