# Knight Moves 4 - September 2021 (Solution)

**Puzzle:** [09_knight_moves_4.md](../../puzzles/2021/09_knight_moves_4.md)

## Official Solution

The move count of 50 (and region sum of 75) can be deduced using three observations:
- The sum of all numbers must be a triangular number
- The sum of all numbers must be divisible by the number of regions (17)
- The regions of size 2 must have an odd sum by parity arguments of knight moves

Once this is known the path of the knight can be deduced by hand or with the aid of a program.

**Answer: 14820**

The sum of the squares of the maxima of each row comes to 14820.

**Solution grid:** https://www.janestreet.com/puzzles/2021-09-01-knight-moves-4-solution.png
