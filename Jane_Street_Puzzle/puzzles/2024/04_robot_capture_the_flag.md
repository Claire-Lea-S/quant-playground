# Robot Capture-the-Flag - April 2024

**Category:** Game Theory / Geometry
**Difficulty:** Hard
**URL:** https://www.janestreet.com/puzzles/robot-capture-the-flag-index/

## Problem Statement

### Setup
Two robots, Aaron and Erin, begin at the center of a unit circle. A flag is randomly placed inside the circle.

**Information asymmetry:**
- Aaron learns the flag's distance (r) from center
- Erin learns only its direction (θ) in polar coordinates

### Rules
- Each robot may make a single move after the flag is placed
- Robots act without knowledge of each other's actions
- Movement must stay within the circle boundaries
- Erin is programmed to play a fixed distance *e* along the detected angle θ

### Winning Condition
Whichever robot is closer to the flag after these moves captures the flag and is declared the winner.

### Challenge
Determine the probability Aaron wins, assuming optimal play by both robots, given Erin's fixed-distance movement strategy.

**Answer format:** 10 decimal places.

## Key Concepts to Apply

- Polar coordinate geometry
- Optimization under incomplete information
- Minimax strategies
- Integration over probability distributions

## Hints for Solving

1. Consider Erin first chooses optimal distance *e*
2. Aaron then optimizes his response given knowledge of *r* but not *θ*
3. For small *r*, Aaron may be better staying at center
4. Use geometric analysis of when Aaron's circle intersects Erin's

## My Attempt

[Write your solution approach here]

---

## Official Solution

### Problem Setup
Aaron and Erin play a flag-capture game. Erin picks a distance *e* along a random angle, while Aaron chooses distance *a* and angle to maximize his winning probability. Erin strategically selects *e* to minimize Aaron's advantage.

### Critical Distance
The optimal distance Erin should choose is approximately:
**e ≈ 0.501306994212753**

### Aaron's Strategy
- If the flag's radius *r* is less than *e*/2, Aaron guarantees victory by staying at the center
- Otherwise, Aaron should select distance *a* that maximizes the fraction of his circular search area within striking distance |*r*−*e*| of the flag

### Solution Method
The solution involves calculating "the subtended angle determined by the circles' intersection points" using an arcsin integral that accounts for polar coordinates and flag position probability distributions.

### Final Answer
**Aaron wins with probability ≈ 0.166186486474** (about 16.6%)

## Lessons Learned

1. Information asymmetry drastically affects winning probabilities
2. Knowing distance vs direction leads to very different optimal strategies
3. Geometric probability requires careful integration over all possible configurations
4. Even with less information, a well-chosen fixed strategy (Erin's) can be quite effective
