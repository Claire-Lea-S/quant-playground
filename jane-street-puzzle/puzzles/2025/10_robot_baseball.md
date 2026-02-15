# Robot Baseball - October 2025

**Category:** Game Theory / Probability
**URL:** https://www.janestreet.com/puzzles/robot-baseball-index/

## Problem Statement

The Artificial Automaton Athletics Association is developing a competitive robot baseball format. Each game consists of independent at-bats where a batter maximizes expected score and a pitcher minimizes it through simultaneous decision-making.

**At-Bat Structure:**
Players track balls (starting at 0) and strikes (starting at 0). Each pitch involves:
- Pitcher chooses: throw ball or strike
- Batter chooses: wait or swing
- Decisions made simultaneously and secretly

**Outcome Rules:**

| Pitch | Batter Action | Result |
|-------|---------------|--------|
| Ball | Wait | +1 ball |
| Strike | Wait | +1 strike |
| Ball | Swing | +1 strike |
| Strike | Swing | Home run (prob *p*) or +1 strike (prob 1-*p*) |

**Ending Conditions:**
- Balls reach 4: batter scores 1 point (walk)
- Strikes reach 3: batter scores 0 points (strikeout)
- Home run occurs: batter scores 4 points

**The Challenge:** The league adjusts parameter *p* to optimize viewer engagement. Find *q*, the maximal probability that at-bats reach a full count (3 balls and 2 strikes).

Assume both players employ optimal mixed strategies. Quad-A has selected the *p* value that maximizes *q*.

**Answer:** Calculate *q* to ten decimal places.
