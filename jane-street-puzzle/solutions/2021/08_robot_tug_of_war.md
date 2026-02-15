# Robot Tug-of-War - August 2021 (Solution)

**Puzzle:** [08_robot_tug_of_war.md](../../puzzles/2021/08_robot_tug_of_war.md)

## Official Solution

### Setting Up the Function

Define f on [-0.5, 0.5] as:
**f(x) = Prob(Player 1 wins at a starting position of x)**

By symmetry of the game:
f(x) = Prob(Player 1 wins in the first move) + ∫ₓ^½ Prob(Player 2 wins starting at (-y)) dy
     = (½ + x) + ∫ₓ^½ (1 - f(-y)) dy

### Finding the Differential Equation

Differentiating and applying the fundamental theorem of calculus:
**f'(x) = f(-x)**

Differentiating again:
**f''(x) = -f(x)**

### General Solution

The general solution to this differential equation is:
**f(x) = A·sin(x) + B·cos(x)**

### Boundary Conditions

1. f(½) = 1
2. f'(0) = f(0), which implies A = B

From the first equation: A·sin(½) + B·cos(½) = 1

With A = B:
**A = B = 1/(sin(½) + cos(½))**

So: **f(x) = (sin(x) + cos(x))/(sin(½) + cos(½))**

### Finding the Answer

Solve: (sin(x) + cos(x))/(sin(½) + cos(½)) = ½ on [-½, 0]

### Answer

**-0.2850001**

Or exactly: **arcsin(sin(½ + π/4)/2) - π/4**
