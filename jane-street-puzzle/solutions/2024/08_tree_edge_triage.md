# Tree-edge Triage - August 2024 (Solution)

**Puzzle:** [08_tree_edge_triage.md](../../puzzles/2024/08_tree_edge_triage.md)

## Official Solution

### Setting Up the Equation

Suppose for a given *p*, Aaron's probability of winning on the infinite tree is *x*. Looking at the first two turns in the game, Aaron can win if at least one of the two sides of the tree has 3 edges marked *A* and BOTH subtrees Beren can choose between are winnable by Aaron (which has probability *x*, independently per subtree).

The equation *x* and *p* must satisfy is:

**x = 2p³x² - p⁶x⁴**

(The subtracted term is from double counting when Aaron can win on both sides of the tree.)

### Finding the Critical Point

We want to find the smallest positive *p* where this has a positive root *x* < 1.

As *p* increases, the graph of the quartic approaches the graph of f(x) = x from below, and the moment where it touches will be tangent. Adding the constraint that the derivative equals 1 at the point of equality:

**1 = 2p³(2x) - p⁶(4x³)**

### Solution

These two equations are solved by:
- x = 8/9
- **p = (27/32)^(1/3)**

So the lowest nonzero probability Aaron can have of winning the game is the surprisingly high 8/9 chance!
