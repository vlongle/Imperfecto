from imperfect_info_games.games.rock_paper_scissor import RockPaperScissorGame
from imperfect_info_games.evaluate import evaluate_strategies
import numpy as np

np.random.seed(0)

if __name__ == "__main__":
    print("In standard rock paper scissor game, the nash strategy [1/3, 1/3, 1/3] is unexploitable by "
          "any other strategy.")
    print("That means that it will always have 0 payoff against all strategy[p, q, 1-p-q]. Do the math with the "
          "normal form game matrix to convince yourself that this is true.")
    print("In this example, we will fix P0 strategy to be uniform, and vary P1 strategy")
    print("\n")
    P0_uniform_strategy = {"P0": [1/3, 1/3, 1/3]}

    strategies = [np.array([1/3, 1/3, 1/3]), np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0]),
                  np.array([0.5, 0.5, 0.0]), np.array([0.5, 0.0, 0.5]), np.array([0.0, 0.5, 0.5]), np.array([0.4, 0.4, 0.2])]
    print("P1 strategy \t \t payoff")
    print("-" * 40)
    with np.printoptions(suppress=True, precision=2):
        for strat in strategies:
            P1_strategy = {"P1": strat}
            avg_payoffs = evaluate_strategies(RockPaperScissorGame, [
                P0_uniform_strategy, P1_strategy], n_iters=1000)
            print(f"{np.array2string(strat):20} \t {avg_payoffs}")
