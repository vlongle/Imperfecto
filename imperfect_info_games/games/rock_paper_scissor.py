"""A collection of 2-player rock paper scissor games.

This includes:
    - Standard Rock Paper Scissor
    - Asymmetric Rock Paper Scissor
"""
from enum import IntEnum
from typing import Sequence

from imperfect_info_games.games.game import ExtensiveFormGame
from imperfect_info_games.player import Player
from imperfect_info_games.utils import lessVerboseEnum


class ROCK_PAPER_SCISSOR_ACTIONS(lessVerboseEnum, IntEnum):
    """Available actions for the rock-paper-scissors game."""
    ROCK = 0
    PAPER = 1
    SCISSOR = 2


class RockPaperScissorGame(ExtensiveFormGame):
    """A (standard) 2-player rock-paper-scissor (extensive-form) game.

    Payoff
    ------
    Rock beats scissors, scissors beats paper, and paper beats rock.
    Winner gets +1 payoff, loser gets -1 payoff.

    Nash Equilibrium
    ----------------
    The nash strategy (unexploitable) is (1/3, 1/3, 1/3)
    """

    actions = ROCK_PAPER_SCISSOR_ACTIONS
    n_players = 2

    def __init__(self, players: Sequence[Player]):
        assert len(players) == self.n_players
        super().__init__(players)

    def get_active_player(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> Player:
        if len(history) not in range(self.n_players):
            raise ValueError("Invalid history " + str(history))
        return self.players[len(history)]

    def is_terminal(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> bool:
        return len(history) == 2

    def get_payoffs(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> Sequence[float]:
        assert self.is_terminal(history)
        history_str = self.history_to_str(history)
        match history_str:
            case "ROCK-PAPER":
                return [-1, 1]
            case "ROCK-SCISSOR":
                return [1, -1]
            case "PAPER-ROCK":
                return [1, -1]
            case "PAPER-SCISSOR":
                return [-1, 1]
            case "SCISSOR-ROCK":
                return [-1, 1]
            case "SCISSOR-PAPER":
                return [1, -1]
        return [0, 0]

    def get_infostate(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> str:
        info_str_dict = {0: "P0", 1: "P1"}
        if len(history) not in range(self.n_players):
            raise ValueError("Invalid history " + str(history))
        return info_str_dict[len(history)]


class AsymmetricRockPaperScissorGame(RockPaperScissorGame):
    """A asymmetric 2-player rock-paper-scissors (extensive-form) game.

    Payoff
    ------
    Rock beats scissors, scissors beats paper, and paper beats rock.
    **But** winner gets +2 payoff, loser gets -2 payoff when someone plays
    scissor. Otherwise, winner gets +1 payoff, loser gets -1 payoff.

    Nash Equilibrium
    ----------------
    The nash strategy (unexploitable) is (0.4, 0.4, 0.2)
    """

    def get_payoffs(self, history: Sequence[ROCK_PAPER_SCISSOR_ACTIONS]) -> Sequence[float]:
        """Override the get_payoffs function of standard rock-paper-scissors such that
        the winner gets +2 payoff, loser gets -2 payoff when someone plays scissor. Otherwise,
        winner gets +1 payoff, loser gets -1 payoff.

        Args:
            history: The history of the game.

        Returns:
            The payoffs of the players.
        """
        assert self.is_terminal(history)
        if len(history) > 2:
            raise ValueError("Invalid history " + str(history))

        history_str = self.history_to_str(history)
        match history_str:
            case "ROCK-PAPER":
                return [-1, 1]
            case "ROCK-SCISSOR":
                return [2, -2]
            case "PAPER-ROCK":
                return [1, -1]
            case "PAPER-SCISSOR":
                return [-2, 2]
            case "SCISSOR-ROCK":
                return [-2, 2]
            case "SCISSOR-PAPER":
                return [2, -2]
        return [0, 0]


# def play_against_fixed_policy():
#     """
#     regret-matching agent plays against a fixed policy agent in
#     rock-paper-scissor.
#     """
#     n_steps = 10000
#     regret_matching = RegretMatchingAgent(
#         name='regret matching', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
#     opponent_policy = np.array([1/3, 1/3, 1/3])
#     #opponent_policy = np.array([0.34, 0.33, 0.33])
#     fixed_opponent = FixedPolicyAgent("fixed_opponent", opponent_policy)
#     agents = [regret_matching, fixed_opponent]
#     game = RockPaperScissorGame(agents, n_steps=n_steps)
#     game.run()
#     print(f'avg strats after {n_steps} steps')
#     pprint(game.get_avg_strats())
#     print(f'eps_rewards {game.get_avg_rewards()}')
#
#
# def play_against_regret_matching():
#     """
#     both agents are regret-matching agents.
#     Their avg policies should both converge to a Nash equilibrium,
#     which is [1/3, 1/3, 1/3] for rock-paper-scissor.
#     """
#     n_steps = 10000
#     regret_matching_1 = RegretMatchingAgent(
#         name='regret matching 1', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
#     regret_matching_2 = RegretMatchingAgent(
#         name='regret matching 2', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
#     agents = [regret_matching_1, regret_matching_2]
#     game = RockPaperScissorGame(agents, n_steps=n_steps)
#     game.run()
#     print(f'avg strats after {n_steps} steps')
#     pprint(game.get_avg_strats())
#     print(f'eps_rewards {game.get_avg_rewards()}')
#
#
# def play_against_delay_regret_matching():
#     """
#     both agents are regret-matching agents. We delay the policy update of one agent
#     while updating the other for several games.
#     Their avg policies should both converge to a Nash equilibrium,
#     which is [1/3, 1/3, 1/3] for rock-paper-scissor.
#     """
#     n_steps = 10000
#     freeze_interval = 50
#     freeze_duration = n_steps // freeze_interval  # no. of games per freeze interval
#     regret_matching_1 = RegretMatchingAgent(
#         name='regret matching 1', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
#     regret_matching_2 = RegretMatchingAgent(
#         name='regret matching 2', n_actions=len(ROCK_PAPER_SCISSOR_ACTIONS))
#     agents = [regret_matching_1, regret_matching_2]
#     game = RockPaperScissorGame(agents, n_steps=freeze_duration)
#     for _ in range(freeze_interval):
#         # evolve first agent, freeze 2nd
#         game.run(freeze_ls=[regret_matching_2])
#         # evolve second agent, freeze 1st
#         game.run(freeze_ls=[regret_matching_1])
#
#     print(f'avg strats after {n_steps} steps')
#     pprint(game.get_avg_strats())
#     print(f'eps_rewards {game.get_avg_rewards()}')
#
#
# if __name__ == '__main__':
#     play_against_delay_regret_matching()
#     # play_against_fixed_policy()
#     # play_against_regret_matching()
