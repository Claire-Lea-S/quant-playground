# Robot Baseball - October 2025

**Category:** Game Theory / Probability
**Difficulty:** Hard
**URL:** https://www.janestreet.com/puzzles/robot-baseball-index/

## Problem Statement

The Artificial Automaton Athletics Association is developing a competitive robot baseball format. Each game consists of independent at-bats where a batter maximizes expected score and a pitcher minimizes it through simultaneous decision-making.

### At-Bat Structure

Players track balls (starting at 0) and strikes (starting at 0). Each pitch involves:
- Pitcher chooses: throw ball or strike
- Batter chooses: wait or swing
- Decisions made simultaneously and secretly

### Outcome Rules

| Pitch | Batter Action | Result |
|-------|---------------|--------|
| Ball | Wait | +1 ball |
| Strike | Wait | +1 strike |
| Ball | Swing | +1 strike |
| Strike | Swing | Home run (prob *p*) or +1 strike (prob 1-*p*) |

### Ending Conditions

An at-bat concludes when:
- Balls reach 4: batter scores 1 point (walk)
- Strikes reach 3: batter scores 0 points (strikeout)
- Home run occurs: batter scores 4 points

### The Challenge

The league adjusts parameter *p* to optimize viewer engagement. Find *q*, the maximal probability that at-bats reach a full count (3 balls and 2 strikes).

Assume both players employ optimal mixed strategies. Quad-A has selected the *p* value that maximizes *q*.

**Answer Required:** Calculate *q* to ten decimal places.

## Key Concepts to Apply

- Backward induction from terminal states
- Nash equilibrium in zero-sum games
- Mixed strategy calculation
- Optimization over parameter *p*

## Hints for Solving

1. Work backwards from the full count state
2. At each game state, find the Nash equilibrium probabilities for both players
3. The outcome is symmetric with respect to player choices
4. Both players' equilibrium probabilities must make opponent indifferent

## My Attempt

[Write your solution approach here]

---

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

## Lessons Learned

1. Backward induction is essential for sequential games with multiple states
2. Symmetry in game structure often simplifies equilibrium calculations
3. In zero-sum games, optimal play makes the opponent indifferent
