# Sum One, Somewhere - April 2025 (Solution)

**Puzzle:** [04_sum_one_somewhere.md](../../puzzles/2025/04_sum_one_somewhere.md)

## Official Solution

### Setting Up the Equations

For a fixed *p*, let:
- f(*p*) = probability that the tree has an infinite path of sum zero
- g(*p*) = probability that the tree has an infinite path of sum at most 1

The problem asks to find *p* such that g(*p*) = 1/2.

### Finding f(p)

Using the decomposition of a binary tree into its root and its two subtrees:

f(*p*) = *p* · (2f(*p*) - f(*p*)²)

This simplifies to:

**f(*p*) = 2 - 1/*p***

### Finding g(p)

Similarly:

g(*p*) = *p* · (2g(*p*) - g(*p*)²) + (1-*p*) · (2f(*p*) - f(*p*)²)

### Solving for p

Plugging in g(*p*) = 1/2, we end up with a cubic equation in *p*:

**3*p*³ - 10*p*² + 12*p* - 4 = 0**

### Answer

**p ≈ 0.5306035754**
