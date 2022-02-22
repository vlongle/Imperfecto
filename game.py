class TwoPlayerGame:
    def __init__(self, agents, n_steps=100):
        assert(len(agents) == 2)
        self.agents = agents
        self.n_steps = n_steps

    def compute_rewards(self, actions):
        pass

    def step(self):
        actions = [agent.act() for agent in self.agents]
        rewards = self.compute_rewards(actions)
        # associate names with actions and rewards
        actions = dict(zip(self.agents, actions))
        rewards = dict(zip(self.agents, rewards))  # type: ignore
        for agent in self.agents:
            agent.update_policy(actions, rewards)

    def run(self):
        for _ in range(self.n_steps):
            self.step()
