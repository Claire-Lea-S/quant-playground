# Robot Archery - December 2021 (Solution)

**Puzzle:** [12_robot_archery.md](../../puzzles/2021/12_robot_archery.md)

## Official Solution

### Setup

Without loss of generality, assume an arrow's distance to the center of the target is U[0,1] distributed.

Let *P_{j,k}(x)* denote the probability that Player *j* out of *k* in the current line will eventually win the game, given that the current best dart is at distance *x*.

### 2-Player Tournament

*P_{1,2}(x) + P_{2,2}(x) = 1*
*P_{1,2}(0) = 0*
*P_{1,2}(x) = ∫₀ˣ P_{2,2}(u) du*

Taking derivatives and substituting: *P'_{1,2}(x) = -P_{1,2}(x)*

Solving: **P_{1,2}(x) = 1 - e^{-x}**

### 4-Player System

Similar systems of integral equations lead to:

**P_{4,4}(1) = (-5/4)(cos(1) + sin(1)) + (1/2)e^{-1} + (e^{-1/2})(cos(√3/2) + (5/√3)sin(√3/2))**

### Answer

**≈ 0.18343765086**

**Solution image:** https://www.janestreet.com/puzzles/2021-12-01-robot-archery-solution.png
