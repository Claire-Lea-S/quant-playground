# Hooks 10 - March 2024

**Category:** Grid Puzzle
**URL:** https://www.janestreet.com/puzzles/hooks-10-index/

## Problem Statement

The grid can be partitioned into 9 L-shaped "hooks". The largest is 9-by-9 (contains 17 squares), the next largest is 8-by-8 (contains 15 squares), and so on. The smallest hook is just a single square.

Find where the hooks are located, and place nine 9's in one of the hooks, eight 8's in another, seven 7's in another, and so on.

### Rules

- The filled squares must form a connected region (squares are "connected" if they are orthogonally adjacent)
- Every 2-by-2 region must contain at least one unfilled square
- The clues in the grid are placed in cells that are **not** filled in the completed grid
- A number in the grid represents the **sum** of all values in orthogonally adjacent cells in the completed grid

**Answer:** The product of the areas of the connected groups of empty squares in the completed grid.

**Image:**

![Hooks 10 Grid](03_hooks_10_1.png)