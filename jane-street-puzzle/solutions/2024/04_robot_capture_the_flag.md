# Robot Capture-the-Flag - April 2024 (Solution)

**Puzzle:** [04_robot_capture_the_flag.md](../../puzzles/2024/04_robot_capture_the_flag.md)

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