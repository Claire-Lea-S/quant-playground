# Robot Weightlifting - June 2021 (Solution)

**Puzzle:** [06_robot_weightlifting.md](../../puzzles/2021/06_robot_weightlifting.md)

## Official Solution

Working backwards from the 1st seed's decision, we work with each seed's probability of successfully lifting their selected weights.

Given the 1st seed knows *x* (3rd seed's success probability) and *y* (2nd seed's success probability), there are three possible strategies:

1. Lift slightly more than the 3rd seed, with (*x*-ε) chance of success
2. Lift slightly more than the 2nd seed, with (*y*-ε) chance of success
3. Lift zero weight with success probability 1

The function for the 2nd seed's optimal probability of lifting (*y*), dependent on *x*, is piecewise smooth with six different pieces and two jump discontinuities.

The optimal choice for the 3rd seed is at a point of triple intersection where the 1st seed is indifferent between the three strategies.

**Answer: p(w) = 0.286833**

Final selections:
- x = 0.286833…
- y = 0.436041…
- z = 1

Winning probabilities:
- 3rd seed: 0.286833…
- 2nd seed: 0.310970…
- 1st seed: 0.402197…
