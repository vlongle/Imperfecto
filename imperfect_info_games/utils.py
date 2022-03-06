"""
A collection of helper functions and classes.
"""
import numpy as np
from enum import Enum


class lessVerboseEnum(Enum):
    """
    A less verbose version of the Enum class.

    Usage
    -----
    ```
        class Test(lessVerboseEnum):
            TEST=0

        print(Test.TEST) # prints "TEST" instead of "Test.TEST"
    ```
    """

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


def get_action(action_probs: np.ndarray) -> int:
    """
    Sample an action from an action probability distribution.

    Args:
        action_probs (np.array): a numpy array of probabilities of length n_actions

    Returns:
        int: the index of the action sampled with the given probabilities
    """
    action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
    return action
