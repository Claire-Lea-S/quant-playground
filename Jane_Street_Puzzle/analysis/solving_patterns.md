# Jane Street Puzzle Solving Patterns

This document captures patterns and strategies learned from analyzing 120+ Jane Street puzzles.

## Puzzle Type Distribution

Based on the catalog analysis:

| Category | Count | Key Techniques |
|----------|-------|----------------|
| Grid Puzzles | ~35 | Constraint propagation, backtracking |
| Game Theory | ~15 | Nash equilibrium, backward induction |
| Probability | ~10 | Integration, expected value |
| Geometry | ~8 | Area calculations, symmetry |
| Visual/Word | ~10 | Pattern recognition, decoding |
| Unknown/Other | ~50 | Various |

## Pattern 1: Robot Series (Game Theory)

### Common Structure
- Two players making simultaneous or sequential decisions
- Uniform random distributions [0,1]
- Looking for Nash equilibrium or optimal strategy

### Key Techniques
1. **Backward Induction**: Start from terminal states, work backwards
2. **Indifference Principle**: At equilibrium, player must be indifferent between choices
3. **Threshold Strategies**: Often involves finding critical cutoff values
4. **Golden Ratio**: φ = (√5-1)/2 ≈ 0.618 appears frequently in symmetric games

### Example Problems
- Robot Javelin: Rethrow threshold at golden ratio
- Robot Baseball: Full count probability maximization
- Robot Capture-the-Flag: Incomplete information optimization

### Template Approach
```
1. Define game states and transitions
2. Identify terminal states and values
3. Work backwards computing expected values
4. Find equilibrium by setting derivatives to zero
5. Verify using indifference conditions
```

## Pattern 2: Hooks Series (Grid Puzzles)

### Common Structure
- Grid divided into L-shaped "hooks" of decreasing sizes
- Numbers must be placed according to region constraints
- Connectivity and spacing requirements

### Key Techniques
1. **Start with extremes**: Place 9s in 9-hook first (most constrained)
2. **Use given clues**: Border clues restrict possibilities
3. **Check connectivity**: Ensure filled cells form connected region
4. **No 2×2 filled**: Common constraint in many grid puzzles

### Template Approach
```
1. Identify most constrained regions
2. Use clues to eliminate possibilities
3. Apply global constraints (connectivity)
4. Verify all local constraints
5. Calculate answer metric (usually product of areas)
```

## Pattern 3: Number Cross Series

### Common Structure
- Grid with regions of same digits
- Numbers formed by concatenation must satisfy clues
- Tiles can displace values with increment rules

### Key Techniques
1. **Work from row clues**: Each clue constrains possible number formations
2. **Track increments**: Displaced values affect neighbors
3. **No repeated numbers**: Each number appears once

## Pattern 4: Geometric Probability

### Common Structure
- Random points in geometric region
- Calculate probability of some condition
- Answer often involves π, ln, or algebraic numbers

### Key Techniques
1. **Symmetry reduction**: Use 8-fold or 4-fold symmetry
2. **Integration setup**: Define valid regions carefully
3. **Change of variables**: Polar coordinates often help
4. **Perpendicular bisector**: Common in equidistance problems

### Common Answer Forms
- `(a + bπ + c·ln(d)) / e` for some integers
- Algebraic numbers like golden ratio
- Roots of low-degree polynomials

## Pattern 5: Visual/Decoding Puzzles

### Common Structure
- Image with hidden information
- Multi-step decoding process
- Final answer is a word or phrase

### Key Techniques
1. **Identify the encoding**: Emoji names, first letters, positions
2. **Extract message**: Usually spells out instructions
3. **Apply transformation**: Caesar cipher, indexing, etc.
4. **Wordplay**: Puns and references common (K-9 = canine)

## General Problem-Solving Framework

### Step 1: Classify the Problem
- Game theory? → Look for equilibrium
- Grid puzzle? → Look for constraints
- Probability? → Set up integrals
- Visual? → Look for hidden patterns

### Step 2: Identify Key Constraints
- What must be true?
- What are the boundary conditions?
- What symmetries exist?

### Step 3: Find Entry Points
- Most constrained elements
- Given clues or values
- Boundary cases

### Step 4: Develop Strategy
- Backward induction for sequential problems
- Constraint propagation for logic puzzles
- Integration for probability
- Pattern matching for visual puzzles

### Step 5: Verify Solution
- Check all constraints satisfied
- Verify answer format matches expected
- Cross-check with partial solutions

## Common Mathematical Tools

### Probability & Statistics
- Expected value calculations
- Conditional probability
- Integration over regions

### Calculus
- Optimization (derivatives = 0)
- Area calculations
- Limits and infinite series

### Game Theory
- Nash equilibrium
- Minimax strategies
- Information asymmetry

### Combinatorics
- Counting arrangements
- Permutations and combinations
- Inclusion-exclusion

### Geometry
- Area formulas
- Perpendicular bisectors
- Polar coordinates

## Tips for Improvement

1. **Practice by category**: Focus on one type until comfortable
2. **Time yourself**: Many puzzles have implicit difficulty levels
3. **Read solutions carefully**: Understand the key insight
4. **Look for patterns**: Many puzzles are variations of others
5. **Build a toolkit**: Keep track of useful techniques
6. **Don't give up**: Most puzzles have elegant solutions
