class Agent:
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

    def act(self):
        """
        Return the action the agent wants to take (given its current policy)
        """
        pass

    def update_policy(self, actions, rewards):
        """
        actions: dict with keys: agent class, values: action taken by that agent
        rewards: dict with keys: agent class, values: reward received by that agent
        Update the agent's internal policy
        """
        pass
