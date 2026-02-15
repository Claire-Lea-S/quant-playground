# Somewhat Square Sudoku - January 2025 (Solution)

**Puzzle:** [01_somewhat_square_sudoku.md](../../puzzles/2025/01_somewhat_square_sudoku.md)

## Official Solution

### Number Theory Approach

Let *S* be the sum of the digits in the first row, and let *d* be the GCD of the 9-digit numbers formed by the nine rows. The sum of these 9-digit numbers will be 111,111,111 × *S* = 3 × 3 × 37 × 333,667 × *S*, so *d* must be a divisor of this value.

Furthermore, if a 9-digit integer *N* is a divisor of 999,999,999, then any cyclic permutation of *N* will be as well.

### Finding the Solution

We know our rows all contain 0, 2, and 5. One of them begins with a 0, so we look at large divisors of 111,111,111 to see if multiples of any of them are 8-digit numbers with distinct positive digits containing a 2 and a 5.

It turns out 37 × 333,667 = 12,345,679 is one such number. The only other 8-digit multiples of 12,345,679 with distinct positive digits are 24,691,358, 49,382,716, and 61,728,395.

This last value (61,728,395), when cyclically shifted 8 times, is the one that can validly populate the sudoku grid.

### Answer

**283,950,617**

**Solution image:** https://www.janestreet.com/puzzles/somewhat-square-sudoku-solution.jpg
