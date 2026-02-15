# Robot Baseball - October 2025 (Solution)

**Puzzle:** [10_robot_baseball.md](../../puzzles/2025/10_robot_baseball.md)

## Official Solution

### Methodology
The solution employed backward induction from full count to the start of an at-bat. For each strike zone probability *p*, determine the Nash equilibrium strategies for both pitcher and batter.

### Key Insight
"The outcome of a pitch is symmetric with respect to the pitcher's choice and the batter's choice."

This symmetry means both players' equilibrium probabilities—throwing strikes and swinging—are identical, as each player must make their opponent indifferent between their options.

### Answer
**q = 0.2959679934**

Achieved at approximately *p* = 0.2269732.

### Optimal Player Statistics
- Strikeout rate: 68%
- Walk rate: 21%
- Home run rate: 11% of plate appearances
- Batting line: .139/.318/.556