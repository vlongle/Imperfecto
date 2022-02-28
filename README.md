# Coalition Formation under uncertainty

**Author**: Long Le

C++ Code to simulate agents engaging in coalition formation under uncertainty.


## Poker algorithms

- Game-Tree Search w/ Adaptation in Stochastic Imperfect-Info Game


CFR: deep counterfactual regret minimization. (https://arxiv.org/pdf/1811.00164.pdf)

Our bargaining game
Sorta like an extensive-form game but with simultaneous moves

https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-254-game-theory-with-engineering-applications-spring-2010/lecture-notes/MIT6_254S10_lec12.pdf


Multi-stage games with simultaneous moves at some stages.
Simultaneous moves can be captured by information set to represent not being able to obseve your opponent's move when it's your turn to make a decision (at your decision node).


Two issues:
- Have to come up w/ some heuristic for non-leaf node evaluation because the game tree depth is too deep to be evaluated all the way to completion (think Chess)
- Have to evaluate leaf nodes in imperfect-info game (think Poker). Leaf nodes = showdown but you still don't have info. about your opponent's cards, how to evaluate?

* If both players play to minimize average overall regret, their average strategies will meet at approximation of Nash Equilibrium at some point. This is good to know BECAUSE our theoretical part of the paper is concerned with the core, which is some sort of Nash equil

### Counterfactual regret minimization for Poker
https://int8.io/counterfactual-regret-minimization-for-poker-ai/

__No-Regret learning__:

It seems that Exp3 is for normal-form game (or repeated bandit), and CRM (counterfactual regret mimization) is for extensive form gamenormal-form game, and CRM (counterfactual regret mimization) is for extensive form game, which is repeated AND sequential.

http://researchers.lille.inria.fr/~lazaric/Webpage/MVA-RL_Course17_files/regret_games.pdf


Regret of a trust distribution (policy) is the cumulative (up until this time) difference between the policy's loss and the best __single__ expert. The reward vector might be assigned by an adversary.  Self-play no-regret learning converges to Nash equil or something like that.

Reach prob. following a joint strategies (in our case, joint strategies dependent on weight belief)





https://www.ma.imperial.ac.uk/~dturaev/neller-lanctot.pdf

Asking the correct question:
Our profit by and large depends on
- the opponent's private info
- how the opponent play


CFR seems to have to do the accounting for both me and my opponent??
How does this even work??

I think this is a centralized algorithm that assumes that your opponent is also cfr agent? 

CFR is for computing Nash equil (https://proceedings.neurips.cc/paper/2007/file/08d98638c6fcd194a4b1e6992063e944-Paper.pdf)


Nash equilibrium has this nice property in two-player zero-sum game.
In expectation, it does no worse than a tie (expected payoff >= 0) against ANY opponent's strategy. We say, a strategy in the Nash equil is "unexploitable".
Properties
http://www.math.tau.ac.il/~mansour/course_games/2006/lecture5.pdf



http://www.cs.cmu.edu/afs/cs/academic/class/15780-s13/www/lec/ganzfried_gt.pdf
https://ai.plainenglish.io/building-a-poker-ai-part-7-exploitability-multiplayer-cfr-and-3-player-kuhn-poker-25f313bf83cf
