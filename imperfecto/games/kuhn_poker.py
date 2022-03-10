'''An implement of Kuhn Poker game.

We have two players. We have three cards: Jack, Queen, King, where King beats Queen and Queen beats
Jack. In this game, each player gets a random card. On a turn, a player can either
    * pass: do nothing. The opponent wins all chip in the pot.
    * bet: place a chip in the pot.
After two passes or two bets (not necessarily consecutive), the game ends. Player with the highest card wins.

The Maximum depth of the game tree is 3. The game tree is as follows.
Game tree::

                [chance]
                   |
              assign cards
                   |
                [player1]
                /      \\

            [pass]      [bet]
             |             |
          [player2]       [player2]
            /   \\         /   \\
          pass    bet   pass     bet
           |      |       |         |
           (h)  [player1]   (1)       (h)
                /   \\

              pass   bet
                |     |
                (2)   (h)

Leaf nodes notation:
    * (h): player has highest card wins!
    * (1): player 1 wins! (player 2 chickens out)
    * (2): player 2 wins! (player 1 chickens out)

In this game, we have 12 info-sets. Each info-set has 2 states since the opponent can have any of the two cards that I'm not already holding. We have 6 ways to deal 2 out of 3 cards to 2 players, and 2 states / info-set so we have 6/2 = 3 info sets at every decision node. We have 4 decision nodes so 3 * 4 = 12 info sets.

Note:
    There's a subtle difference between the number of info sets and the number of nodes per info set (the size of the info set). The size of the info set tells us how many worlds are consistent with the player's observations so far.
    The number of info sets is more "meta". A player, without entering into a game / trajectory, can reason ahead about the different info sets that they can be in once some partial observations are available to them when
    the game starts.
'''

from enum import Enum
from enum import IntEnum
from typing import Sequence

import numpy as np

from imperfecto.algos.player import Player
from imperfecto.games.game import ExtensiveFormGame
from imperfecto.misc.utils import lessVerboseEnum


class KUHN_POKER_ACTIONS(lessVerboseEnum, IntEnum):
    """Available actions in Kuhn Poker."""
    PASS = 0
    BET = 1


class KUHN_POKER_CHANCE_ACTIONS(lessVerboseEnum, IntEnum):
    """Availble chance actions in Kuhn Poker.

    We have 3 cards J, Q, K dealt randomly to 2 players.
    """
    JQ = 0  # player 2 wins
    JK = 1  # player 2 wins
    QK = 2  # player 2 wins
    QJ = 3  # player 1 wins
    KJ = 4  # player 1 wins
    KQ = 5  # player 1 wins


class KuhnPokerGame(ExtensiveFormGame):
    """A Kuhn Poker (https://en.wikipedia.org/wiki/Kuhn_poker) game class.

    Payoff:
        The winner wins whatever is in the pot. A player can win either in showdown by having the
        highest card or win by having their opponent chickens out.

    Nash equilibrium:
        There are infinitely many Nash equilibria. Player one can choose any probability ``alpha``
        in [0, 1/3] to bet when having Jack, and pass when the other play bets. They should bet with
        probability ``3 * alpha`` when having a King, and if the other player bets, they should bet.
        They should always pass when having a Queen, and if the other player bets, they should pass.
        The second player should always bet when having a King; when having a Queen, check if possible
        otherwise call with probability 1/3. When they have a Jack, they should never call and bet with
        probability 1/3. The first player's expected payoff under Nash equilibria is -1/18.
    """
    actions = KUHN_POKER_ACTIONS
    chance_actions = KUHN_POKER_CHANCE_ACTIONS
    n_players = 2
    has_chance_player = True

    def is_terminal(self, history: Sequence[IntEnum]):
        history_str = self.history_to_str(history[1:])  # ignore chance node
        terminal_nodes = ["PASS-PASS", "BET-BET", "BET-PASS",
                          "PASS-BET-PASS", "PASS-BET-BET"]
        return history_str in terminal_nodes

    def get_active_player(self, history: Sequence[IntEnum]) -> Player:
        return self.players[(len(history)-1) % 2]

    def get_winner(self, chance_action: KUHN_POKER_CHANCE_ACTIONS) -> int:
        """Return the winner of the game given a chance action.

        Args:
            chance_action: the chance action

        Returns:
            the winner (player_id) of the game
        """
        if chance_action.value < 3:
            return 1
        return 0

    def showdown(self, history) -> np.ndarray:
        """
        Return the payoff value of the game in the showdown case given a history.

        Winner is the player with the highest card. We don't take into account the amount of chips
        in the pot. Winner gets +1 point while loser gets -1 point.

        Args:
            history: the history of the game

        Returns:
            the payoff value of the game in the showdown case
        """
        winner = self.get_winner(history[0])
        return np.array([1, -1]) if winner == 0 else np.array([-1, 1])

    def get_payoffs(self, history):
        assert self.is_terminal(history)
        match '-'.join(map(str, history[1:])):
            case "PASS-PASS":
                return 1 * self.showdown(history)  # wins 2 chips
            case "BET-BET":
                return 2 * self.showdown(history)  # wins 4 chips
            case "BET-PASS":
                return np.array([1, -1])  # player 2 forfeits, player 1 wins
            case "PASS-BET-PASS":
                return np.array([-1, 1])  # player 1 forfeits, player 2 wins
            case "PASS-BET-BET":
                return 2 * self.showdown(history)  # wins 4 chips
        raise Exception("Invalid history")

    def get_card(self, chance_action: KUHN_POKER_CHANCE_ACTIONS, player_id: int) -> str:
        """Return the card that a chance action has dealt to a player.

        Args:
            chance_action: a chance action
            player_id: the player who receives the card

        Returns:
            the card that the chance action has dealt to the player
        """
        return chance_action.name[player_id]

    def get_infostate(self, history: Sequence[Enum]) -> str:
        player_id = self.get_active_player(history).player_id  # type: ignore
        my_card = self.get_card(history[0], player_id)  # type: ignore
        return my_card + "-" + "-".join(map(str, history[1:]))

    def chance_action(self) -> KUHN_POKER_CHANCE_ACTIONS:
        """Return a chance action.

        We have 3 cards J, Q, K dealt randomly to 2 players. This function handles the card dealing.

        Returns:
            a chance action
        """
        return KUHN_POKER_CHANCE_ACTIONS(np.random.choice(range(len(KUHN_POKER_CHANCE_ACTIONS))))

    @staticmethod
    def shorten_history(history_str: str) -> str:
        """Shorten history string. For example, "KJ-PASS-BET" -> "KJPB".
        Args:
            history_str: history string

        Returns:
            A shortened history string
        """
        s = ''.join(str(a) for a in history_str)
        replacements = {'-': '', 'PASS': 'P', 'BET': 'B'}
        for k, v in replacements.items():
            s = s.replace(k, v)
        return s + ' ' * (5-len(s))
