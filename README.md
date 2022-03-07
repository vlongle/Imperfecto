<h1 align="center">
  <br>
  <a><img src="imgs/poker_meme.jpeg" alt="Imperfect Information Games"></a>
</h1>

<h4 align="center">A Reinforcement Learning AI to play the (simplified) Crab Game Bomb Tag game.</h4>

<p align="center">
    <a href="https://github.com/vlongle/crabgame_ai/commits/main">
    <img src="https://img.shields.io/github/last-commit/vlongle/imperfect_information_games.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub last commit">
    <a href="https://github.com/vlongle/crabgame_ai/issues">
    <img src="https://img.shields.io/github/issues-raw/vlongle/imperfect_information_games.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub issues">
    <a href="https://github.com/vlongle/crabgame_ai/pulls">
    <img src="https://img.shields.io/github/issues-pr-raw/vlongle/imperfect_information_games.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub pull requests">
    <a href="https://twitter.com/intent/tweet?text=Try this dope Python module for AI in imperfect information games!:&url=https%3A%2F%2Fgithub.com%2Fvlongle%2Fimperfect_information_games">
    <img src="https://img.shields.io/twitter/url/https/github.com/vlongle/imperfect_information_games.svg?style=flat-square&logo=twitter"
         alt="GitHub tweet">
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#installation">Installation</a> •
  <a href="#background">Background</a> •
  <a href="#features">Features</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#references">References</a> •
  <a href="#license">License</a>
</p>

## About

A Python module of heavily commented implementations of algorithms and games for games 
with imperfect information such as Rock-Paper-Scissor and Poker. See [Features](#features) for a
list of games and algorithms we provide. See [Installation](#installation) for instruction on how
to install this module, and [Getting Started](#getting-started) on usage and how to customize our
module for your own game.

## Installation
Clone this repo and install it as a module.
```
$ git clone https://github.com/vlongle/imperfect_information_games.git
$ cd imperfect_information_games
$ pip3 install -e .
```
Try to import the module to check if the installation has been successful.
```
$ python3
>> import imperfect_information_games
```

## Background
### Imperfect Information Games

Games such as Chess are known as "perfect information" games as there is no private information to 
each player. Every player can observe each other's moves, and the game state (i.e., the chess board).

However, games such as Poker are "imperfect-information" as each player has their own private card.
Games with simultaneously moves such as rock-paper-scissor can also be modeled as imperfect information
as each player doesn't know the opponent's move ahead of time.

Games with imperfect information are typically modeled as [extensive-form game (EFG)](https://en.wikipedia.org/wiki/Extensive-form_game). 
EFG models sequential game with a game. Players take turn to make a move until a termination node is
reached, where the payoff is revealed. Players make decision at each decision node. However, the
players do not know exactly which node they are in. Instead, they only know that they're in a set
of nodes known as an information set. An information set represents all the possible worlds that
are consistent with what the player knows. 

## Features

 | Games                         | Progress    |
 | -----------                   | ----------- |
 | Rock-paper-scissor            | ✔️           |
 | Asymmetric Rock-paper-scissor | ✔️           |
 | Bar-crowding Game             | ✔️           |
 | Prisoner's Dilemma            | ✔️           |
 | Kuhn Poker                    | ✔️           |

 | Algorithm                                | Progress    |
 | -----------                              | ----------- |
 | Regret Matching                          | ✔️           |
 | Counterfactual Regret Minimization (CFR) | ✔️           |

## Getting Started
Look at all the demos that we have in `imperfect_info_games/demos` folder, and try any of them. For example, run (from the repo's root folder)
```
$ python3 imperfect_info_games/demos/regret_matching_demo.py --help
```
to print out the available options for that demo file. Pick your desired options and run a demo file. For example,
```
$ python3 imperfect_info_games/demos/regret_matching_demo.py --game PrisonerDilemmaGame
--train_regret_matching
```


### Writing Your Own Games!

#### Normal-form Games
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
## TODOs
- Implement other variations of counterfactual regret stuff like Monte Carlo, deep counterfactual
- Implement some cool visualization of training like this (https://medium.com/hackernoon/artificial-intelligence-poker-and-regret-part-2-ee2e329d6571).
- Implement bandit stuff (Exp3 for example, UCB, beta Thompson sampling stuff https://www.youtube.com/watch?v=XxTgX8FlDlI, https://www.cs.ubc.ca/labs/lci/mlrg/slides/Introduction_to_Bandits.pdf). A whole book on bandit lol (https://tor-lattimore.com/downloads/book/book.pdf)
- Consider opponent modeling as well (https://abhinavrobinson.medium.com/ai-wins-rock-paper-scissors-mostly-65e0542f945b this is a nice summary, and the CMU slides somewhere as well... (
http://www.cs.cmu.edu/afs/cs/academic/class/15780-s13/www/lec/ganzfried_gt.pdf))
- Maybe also implement some deep RL methods like Q-learning, actor-critic for these games.

## References
- [An Introduction to Counterfactual Regret Minimization (Neller \& Lanctot)](http://modelai.gettysburg.edu/2013/cfr/cfr.pdf) 
- [Steps to building a Poker AI  (Thomas Trenner)](https://medium.com/ai-in-plain-english/steps-to-building-a-poker-ai-part-1-outline-and-history-58fbedaf6ded)
- [](https://www.kaggle.com/ihelon/rock-paper-scissors-agents-comparison)

## License
MIT License @ Long Le 2021.
