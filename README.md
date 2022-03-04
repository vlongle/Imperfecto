# Algorithms for Imperfect Information Games

A collection of implementations of algorithms and games for games with imperfect information.
## Getting Started
```

```
## Imperfect Information Games

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

| Games              | Progress    |
| -----------        | ----------- |
| Kuhn Poker         | :heavy_check_mark: |
| Rock-paper-scissor | &#9745; |

## References
