# Robot Updated Swimming Trials - May 2022 (Solution)

**Puzzle:** [05_robot_updated_swimming_trials.md](../../puzzles/2022/05_robot_updated_swimming_trials.md)

## Official Solution

The equilibrium probability *p* has the property that if all opponents are choosing the discrete strategy with this probability, then the remaining competitor is indifferent to choosing the discrete strategy or not.

Interestingly, in order to solve for *p* we do NOT need to compute what the alternate continuous strategy is, we must only assume it would put nonzero weight on every race with probability 1.

By symmetry, the remaining competitor's probability of winning must be exactly 1/3 whether they choose discrete or continuous. So we compute the probability of winning with discrete or continuous with all other competitors using probability *p*, set it equal to 1/3, and then backsolve for *p*.

**Answer: p ≈ 0.999560**

The probability of choosing the discrete strategy in the Nash equilibrium is very high.
