import numpy as np


def get_action(action_probs):
    action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
    return action
