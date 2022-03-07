# Demos

## Getting Started
Run
```
$ python3 regret_matching_demo.py --help
```
to print out the available options.


## Writing Your Own Games!

### Normal-form Games
Add a new game by writing an `ACTION_ENUM` class that defines the possible action that is 
available to each player. Then, write a Game class that inherits from our `NormalFormGame`. You will
need to implement the `get_payoffs` function.
```
from enum import intenum
from typing import sequence

from imperfect_info_games.games.game import normalformgame
from imperfect_info_games.utils import lessverboseenum


class MY_CUSTOM_ACTION(lessVerboseEnum, IntEnum):
    ...

class MyCustomNormalFormGame(NormalFormGame):
    actions = MY_CUSTOM_ACTION 
    n_players = ...
    def get_payoffs(self, history: Sequence[MY_CUSTOM_ACTION]) -> Sequence[float]:
        ...
```
See `imperfect_info_games/games/prisoner_dilemma.py` for an example. You can then use your custom
game with the functions available in `imperfect_info_games/demos/regret_matching_demo.py`. For example,
```
...
from imperfect_info_games.demos import to_train_regret_matching

Game = MyCustomNormalFormGame
to_train_regret_matching(Game)
```
