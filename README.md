# Dynamic-Programming-Instances
Some implementations of Dynamic Programming solutions to problems.

**hog_solver.py:** A Dynamic Programming approach to finding the optimal move in the hog game (http://inst.eecs.berkeley.edu/~cs61a/fa17/proj/hog/). This involved calculating the probability of dice roll permutations depending on the number rolled, and using a DP table to recursively calculate the move resulting in the maximal probability of success. The subproblem here was `H(y, t)` = your probability of winning given your score `y`, opponent's score `t`.
