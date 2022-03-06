import numpy as np
from regret_matching import RegretMatchingPlayer
import logging
import enlighten

np.random.seed(0)


class counterfactualRegretMinimizer:
    """
    Counterfactual regret minimizer (cfr) is a self-play
    algorithm that approximates a Nash equilibrium in two-player
    zero-sum games.

    It assumes that the players' policies are common knowledge (very common
    assumption in this literature). Each player maintains a regret for each action
    in each information set (cf. Q(a, s) value in RL). The policy is proportional to regrets.

    Counterfactual regrets are calculated by searching down the trees, taking into account the
    reach probabilities. Compare the regret formula to the advantage function in RL Q-learning.

    Reach probabilities are needed since the nodes in one's player infostate might belong to different infostates of
    their opponent. Therefore, not every node (history) in the infostate is equally likely to be reached, so the reach
    probs should be taken into account to skew the action distribution at that infostate appropriately.
    """

    # NOTE: implementing two-player zero-sum game for now
    def __init__(self, game, n_iters):
        self.game = game
        self.n_iters = n_iters
        self.cum_regrets = {player: {} for player in self.game.players}
        # to calculate the average policy over many training iterations
        self.strategy_sum = {player: {} for player in self.game.players}

    def get_policy(self, player, infostate):
        """
        Returns the policy for a given player and infostate.
        """
        cum_regrets = self.cum_regrets[player][infostate]
        return RegretMatchingPlayer.regret_matching_strategy(cum_regrets)

    def format_hist(self, hist):
        s = ''.join(str(a) for a in hist)
        replacements = {'-': '', 'PASS': 'P', 'BET': ''}
        for k, v in replacements.items():
            s = s.replace(k, v)
        return s + ' ' * (5-len(s))

    def cfr(self, history, reach_probs):
        """
        Args:
            - history: sequence of actions (including chance's action). This sequence uniquely identifies a node in the
                game tree. In code, it must be a list of integers
            - reach_probs: np.array of shape (num_players) indicating the probability of a player reaching this node assuming
            that the other player always play to reach the infostate that the node belongs to (w/ prob=1).
a list of integers
        Return:
            - node utility V(S) for the active player at this history s
        """
        active_player = self.game.get_active_player(history)
        if self.game.is_terminal(history):
            return self.game.get_payoffs(history)[active_player]
        opponent = self.game.get_opponent(active_player)
        infostate = self.game.get_infostate(active_player, history)
        if infostate not in self.cum_regrets[active_player]:
            self.cum_regrets[active_player][infostate] = np.zeros(
                len(self.game.actions))

        cur_policy = self.get_policy(active_player, infostate)
        # advantage function: Q(s, a) - V(s)
        counterfactual_values = np.zeros(len(self.game.actions))
        for action in self.game.actions:
            new_reach_probs = reach_probs.copy()
            new_reach_probs[active_player] *= cur_policy[action.value]
            # zero-sum game so my utility is equal to negative opponent utility
            counterfactual_values[action.value] = - \
                self.cfr(history + [action], new_reach_probs)

        node_util = cur_policy @ counterfactual_values  # dot product
        regrets = (counterfactual_values - node_util) * \
            reach_probs[opponent]  # note that regrets for this node
        # are weighted by reach_probability assuming that the current player always plays to reach this infostate

        # update cumulative regrets, which affect the policy
        self.cum_regrets[active_player][infostate] += regrets
        if infostate not in self.strategy_sum[active_player]:
            self.strategy_sum[active_player][infostate] = np.zeros(
                len(self.game.actions))

        self.strategy_sum[active_player][infostate] += reach_probs[active_player] * cur_policy
        logging.debug(
            f"{' ' * 6} {self.format_hist(history):5}  {np.array2string(reach_probs, precision=2, suppress_small=True):15} {active_player} \t  {infostate:10}   {np.array2string(counterfactual_values - node_util, precision=2, suppress_small=True):10} \t  {np.array2string(cur_policy, precision=2, suppress_small=True)}")
        return node_util

    def get_avg_strats(self):
        avg_strats = {player: {} for player in self.game.players}
        for player in self.game.players:
            for infostate in self.strategy_sum[player]:
                avg_strats[player][infostate] = RegretMatchingPlayer.regret_matching_strategy(
                    self.strategy_sum[player][infostate])
        return avg_strats

    def train(self):
        utils = 0
        logging.debug(
            'iter | hist | reach_prob | active_player | infostate |    regrets \t|   policy')
        logging.debug('-' * 82)
        manager = enlighten.get_manager()
        pbar = manager.counter(total=self.n_iters, desc='CFR', unit='ticks')
        for i in range(self.n_iters):
            logging.debug(i)
            # TODO: figure a more elegant way to do this
            history = [] if not self.game.has_chance_player else [self.game.chance_action()]
            utils += self.cfr(history, np.ones(len(self.game.players)))
            pbar.update()
        logging.debug('-' * 82)

        avg_strats = self.get_avg_strats()
        logging.info("info_set |  avg_policy |  avg_regrets")
        logging.info('-' * 82)
        for player in self.game.players:
            for info_set in self.cum_regrets[player]:
                logging.info(
                    f"{self.format_hist(info_set):10} {np.array2string(avg_strats[player][info_set], precision=2, suppress_small=True):12}   {np.array2string(self.cum_regrets[player][info_set]/self.n_iters, precision=2, suppress_small=True):10}")

        logging.info('-' * 82)
        logging.info(
            f"Average utility for the 1st player over {self.n_iters} iters: {utils/self.n_iters: .3f}")
