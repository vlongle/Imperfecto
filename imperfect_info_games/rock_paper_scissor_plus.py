from rock_paper_scissor import ROCK_PAPER_SCISSOR_ACTIONS
from game import extensiveFormGame, TwoPlayerNormalFormGame
from cfr import counterfactualRegretMinimizer
from agent import FixedPolicyAgent

import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


class rockPaperScissorPlus():
    pass


class rockPaperScissorPlusExtensiveGame(extensiveFormGame):
    """
    Asymmetric rock-paper-scissor game so that the Nash equilibrium is not the uniform policy.
    In this game, if a player chooses a scissors and wins, the winner gets paid twice as much.

    The Nash equilibrium in this game is [prob_rock, prob_paper, prob_scissor] = [0.4, 0.4, 0.2],
    and this is a fair game.
    """

    def __init__(self):
        self.players = [0, 1]
        self.actions = ROCK_PAPER_SCISSOR_ACTIONS
        self.has_chance_player = False

    def get_active_player(self, history):
        return len(history) % 2

    def is_terminal(self, history):
        return len(history) == 2

    def get_payoffs(self, history):
        # WARNING: this is all WRONG btw lol!!
        assert self.is_terminal(history)
        match '-'.join(map(str, history)):
            case "ROCK-PAPER":
                return [-1, 1]
            case "ROCK-SCISSOR":
                return [2, -2]
            case "PAPER-ROCK":
                return [-1, 1]
            case "PAPER-SCISSOR":
                return [-2, 2]
            case "SCISSOR-ROCK":
                return [2, -2]
            case "SCISSOR-PAPER":
                return [-2, 2]
        return [0, 0]

    def get_opponent(self, player):
        return 1 - player

    def get_infostate(self, player, history):
        del history
        return "P" + str(player)


class RockPaperScissorPlusNormalGame(TwoPlayerNormalFormGame):
    def compute_rewards(self, actions):
        print("actions:", '-'.join(map(str, actions)))
        match '-'.join(map(str, actions)):
            case "ROCK-PAPER":
                return [1, -1]
            case "ROCK-SCISSOR":
                return [2, -2]
            case "PAPER-ROCK":
                return [-1, 1]
            case "PAPER-SCISSOR":
                return [-2, 2]
            case "SCISSOR-ROCK":
                return [2, -2]
            case "SCISSOR-PAPER":
                return [-2, 2]
        return [0, 0]


if __name__ == "__main__":
    # WARNING: somehow this is NOT working. Doesn't
    # converge to the Nash equilibrium. Need to figure out why.
    # game = rockPaperScissorPlusExtensiveGame()
    # cfr_solver = counterfactualRegretMinimizer(game, n_iters=10000)
    # cfr_solver.train()

    policy = [0.4, 0.4, 0.2]
    agents = [FixedPolicyAgent("a", policy), FixedPolicyAgent("b", policy)]
    game = RockPaperScissorPlusNormalGame(agents, n_steps=1)
    game.run()
    print(f'eps_rewards {game.get_avg_rewards()}')
