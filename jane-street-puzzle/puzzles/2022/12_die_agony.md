# Die Agony - December 2022

**Category:** Grid Puzzle / Logic
**URL:** https://www.janestreet.com/puzzles/die-agony-index/

## Problem Statement

A six-sided die, with numbers written on each of its faces, is placed on the 6-by-6 grid, in the lower-left (yellow) corner. It then makes a sequence of "moves". Each move consists of tipping the die into an orthogonally adjacent square within the grid.

**Scoring:**
- The die starts with a "score" of 0
- On the Nth move, its score increases by N times the value of the die facing up after the move
- The die is only allowed to move into a square if its score after the move matches the value in the square
- The die cannot be translated or rotated in place in addition to these moves

After some number of moves the die arrives in the upper-right (blue) corner.

**Answer:** The sum of values in the unvisited squares from the die's journey.

**Image:**

![Die Agony Grid](12_die_agony_1.png)
