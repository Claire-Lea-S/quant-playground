# Robot Swimming Trials - October 2021 (Solution)

**Puzzle:** [10_robot_swimming_trials.md](../../puzzles/2021/10_robot_swimming_trials.md)

## Official Solution

### The Uniform Strategy

Since we're searching for the smallest *N* where the discrete strategy is not optimal, the alternative strategy will bid a nonzero amount on every race. The best non-discrete strategy is the **uniform strategy**: bidding 1/N on every race.

### Key Insight

The uniform strategy wins a race exactly when none of the 3N-1 other discrete-strategy-playing robots select that race for their fuel.

### Common Mistakes

1. **Wrong assumption:** Events across races are independent → gives incorrect *N*=9, *p*≈0.350245
2. **Wrong assumption:** Events are disjoint → gives incorrect *N*=8, *p*≈0.370916

### Correct Recursion

Let P(R, m, n) = probability that, if we need to assign R robots to (m+n) total races (m already have a robot, n don't), we eventually assign at least one robot to all races.

**P(R, m, n) = (m × P(R-1, m, n) + n × P(R-1, m+1, n-1)) / (m+n)**

With boundaries:
- P(R, m, 0) = 1
- P(0, m, n) = 0 for n > 0

### Finding the Answer

We want the smallest *N* such that:

**1 - P(3N-1, 0, N) > 1/3**

### Answer

**N = 8, p = 0.334578**
