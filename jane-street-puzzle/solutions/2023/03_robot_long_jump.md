# Robot Long Jump - March 2023 (Solution)

**Puzzle:** [03_robot_long_jump.md](../../puzzles/2023/03_robot_long_jump.md)

## Official Solution

### Nash Equilibrium Strategy

The optimal play involves waiting until a robot's position is at least some threshold *x* and then jumping, where *x* satisfies the equation:

**(x³ - 3x + 2)eˣ = 3x**

### The Threshold

This threshold comes to approximately **0.416195355**.

### Calculating the Answer

Given that threshold, the chance of any given round scoring a positive number is:

**(1 - x)eˣ**

### Answer

The probability that an attempt scores 0 is:

**1 - (1 - x)eˣ ≈ 0.114845886**
