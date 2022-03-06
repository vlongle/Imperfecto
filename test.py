from imperfect_info_games.games.rock_paper_scissor import RockPaperScissorGame, ROCK_PAPER_SCISSOR_ACTIONS
from imperfect_info_games.games.game import ExtensiveFormGame
from typing import Type


class Test:
    pass


def do(game: Type[ExtensiveFormGame]):
    print(game)


# print(do(RockPaperScissorGame))
# print(do(RockPaperScissorGame()))
# print(do(Test))


# game = RockPaperScissorGame([1, 2])
#
# print(game.get_payoffs([ROCK_PAPER_SCISSOR_ACTIONS.ROCK,
#                         ROCK_PAPER_SCISSOR_ACTIONS.PAPER]))
