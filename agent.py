class Agent:
    def __init__(self, name="Mike Hunt"):
        self.name = name

    def act(self):
        pass

    def __str__(self):
        return "Agent(" + self.name + ")"

    def __repr__(self):
        return "Agent(" + self.name + ")"

    def set_game(self, game):
        self.game = game

    def update_policy(self, actions, rewards):
        pass
