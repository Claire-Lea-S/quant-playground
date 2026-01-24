# Game Theory Deep Dive: Jane Street Robot Puzzles

This document provides detailed analysis of the "Robot" series puzzles, which form a significant subset of Jane Street puzzles focused on game theory and probability.

## Overview of Robot Puzzles

| Puzzle | Date | Core Concept |
|--------|------|--------------|
| Robot Javelin | Dec 2025 | Information asymmetry, counter-exploitation |
| Robot Baseball | Oct 2025 | Sequential game states, mixed strategies |
| Robot Road Trip | Jul 2025 | Continuous optimization |
| Robot Capture-the-Flag | Apr 2024 | Incomplete information, geometric strategy |
| Robot Long Jump | Mar 2023 | Similar to Javelin variant |
| Robot Swimming Trials | Oct 2021 | Racing/timing strategy |
| Robot Tug-of-War | Aug 2021 | Force allocation |
| Robot Weightlifting | Jun 2021 | Sequential choices |
| Robot Archery | Dec 2021 | Targeting optimization |

## Core Technique: Nash Equilibrium

### Definition
A Nash equilibrium is a strategy profile where no player can improve by unilaterally changing their strategy.

### For Two-Player Zero-Sum Games
In these games, what one player wins, the other loses. The equilibrium satisfies:
- Player 1's strategy makes Player 2 indifferent among their choices
- Player 2's strategy makes Player 1 indifferent among their choices

### Mathematical Setup
For a game with continuous strategy spaces [0,1]:
1. Let p(x) = probability Player 1 chooses strategy x
2. Let q(y) = probability Player 2 chooses strategy y
3. Find p, q such that expected payoff is constant for all choices in support

## Detailed Example: Robot Javelin

### The Fair Game (No Information Asymmetry)

**Setup**: Each player draws from U[0,1], decides to keep or rethrow.

**Finding Equilibrium Threshold t**:
- If opponent uses threshold t:
  - Keep value x if: E[win | keep x] ≥ E[win | rethrow]
  - E[win | keep x] = P(opponent keeps < x) + P(opponent rethrows) × x
  - E[win | rethrow] = same calculation with x replaced by E[U[0,1]] = 0.5

**Setting up indifference at x = t**:
```
P(Y < t | keep) × 1 + P(Y ≥ t | keep) × t/t + P(rethrow) × t =
P(Y < t | keep) × 0.5 + P(Y ≥ t | keep) × 0.5 + P(rethrow) × 0.5
```

**Solution**: t = (√5 - 1)/2 ≈ 0.618 (golden ratio!)

### Why the Golden Ratio?

The golden ratio appears because of the recursive nature of the problem:
- The value of keeping t must equal the value of rethrowing
- The value of rethrowing is 0.5 (expected value of uniform)
- This creates an equation t² + t - 1 = 0
- Positive root is φ = (√5 - 1)/2

## Detailed Example: Robot Baseball

### State Space
Each at-bat state is (balls, strikes) where:
- balls ∈ {0, 1, 2, 3}
- strikes ∈ {0, 1, 2}

### Terminal States
- (4, _): Walk → Batter scores 1
- (_, 3): Strikeout → Batter scores 0
- Home run during play → Batter scores 4

### Backward Induction Process

**Step 1**: Start at (3, 2) - full count
- If Ball+Wait: Walk (value 1)
- If Strike+Wait: Strikeout (value 0)
- If Ball+Swing: Strikeout (value 0)
- If Strike+Swing: HR with prob p (value 4p), else out (value 0)

**Step 2**: Find Nash equilibrium at (3, 2)
Let π = P(pitcher throws strike), σ = P(batter swings)

Batter's payoff:
```
U(σ, π) = (1-π)(1-σ)×1 + π(1-σ)×0 + (1-π)σ×0 + πσ×4p
        = (1-π)(1-σ) + 4pπσ
```

Setting ∂U/∂σ = 0 for batter's indifference:
```
-(1-π) + 4pπ = 0  →  π = 1/(1+4p)
```

**Step 3**: Continue backwards to all states

### Key Insight
Due to symmetry, at each state the equilibrium probabilities satisfy:
- P(pitcher throws strike) = P(batter swings)
- This simplifies calculations significantly

## Techniques for Solving Game Theory Puzzles

### 1. Identify the Type of Game
- **Simultaneous**: Both players move at once → Look for Nash equilibrium
- **Sequential**: Players alternate → Use backward induction
- **With Information Asymmetry**: One player knows more → Analyze both cases

### 2. Set Up the Payoff Structure
- Define what each player gains/loses for each outcome
- Identify whether it's zero-sum (simpler) or general sum

### 3. Find Equilibrium Strategies
For mixed strategies:
```
1. Assume player i mixes between actions with probabilities p_i
2. Calculate expected payoff for player j as function of p_i
3. Set j indifferent: ∂E[payoff_j]/∂(action) = 0
4. Solve system of equations
```

### 4. Handle Continuous Strategy Spaces
When strategies are continuous (e.g., choose a point in [0,1]):
```
1. Conjecture threshold strategy: act if x > t
2. Set up indifference equation at threshold
3. Solve for t
4. Verify no profitable deviation exists
```

### 5. Exploit Symmetry
If the game is symmetric:
- Equilibrium strategies will often be identical
- Reduces the number of unknowns
- Look for fixed points: σ(t) = t type equations

## Common Mathematical Patterns

### Golden Ratio φ = (√5-1)/2 ≈ 0.618
Appears when:
- Threshold satisfies t² + t = 1
- Recursive structure with self-similarity
- Uniform distribution problems

### Probability Expressions
Common forms in answers:
- `(a + b√c) / d` - algebraic numbers
- Roots of cubics or quartics
- Involving π for circular/angular problems

### Integration Techniques Needed
- Double integrals over unit square
- Polar coordinate transformations
- Indicator function integration

## Practice Problems by Difficulty

### Easier (Start Here)
1. Robot Archery - Single decision, optimize target
2. Robot Weightlifting - Sequential lifting

### Medium
3. Robot Swimming Trials - Racing strategy
4. Robot Tug-of-War - Force allocation

### Harder
5. Robot Baseball - Multi-state equilibrium
6. Robot Javelin - Counter-exploitation
7. Robot Capture-the-Flag - Geometric + game theory

## Verification Checklist

After solving, verify:
- [ ] All players are indifferent at equilibrium
- [ ] No profitable unilateral deviation exists
- [ ] Answer is in correct format (10 decimal places often required)
- [ ] Boundary cases handled (what if p=0 or p=1?)
- [ ] Units/scaling correct

## Resources for Further Learning

- "Game Theory" by Fudenberg & Tirole
- "A Course in Game Theory" by Osborne & Rubinstein
- Online: gambit-project.org for computational game theory
