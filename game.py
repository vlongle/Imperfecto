class TwoPlayerGame:
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
        for _ in range(self.n_steps):
            self.step(freeze_ls)
