# Knight Moves 6 - October 2024 (Solution)

**Puzzle:** [10_knight_moves_6.md](../../puzzles/2024/10_knight_moves_6.md)

## Official Solution

### Optimal Sum

Nearly 40% of entries achieved a minimal sum of A + B + C = **6**. Since C needed to be a divisor of 2024, there were only 4 plausible permutations:
- (1, 3, 2) — most popular, 214 entries
- (3, 2, 1) — 86 entries
- (3, 1, 2) — 54 entries
- (2, 3, 1) — 31 entries

### Notable Entries

**Longest journeys:** Fred Vu chose (3, 1, 2) with:
- 32-move a1-to-f6: a1,c2,a3,b1,d2,f3,e1,d3,b2,a4,c5,a6,b4,a2,c1,b3,a5,c4,e5,c6,d4,b5,d6,f5,e3,d5,f4,e2,c3,d1,f2,e4,f6
- Theoretically-maximal 34-move a6-to-f1

**Most "multiply" moves (16):** Justin Snopek with (3, 1, 2)

**Lowest sum with 12 total moves:** A + B + C = 19 from Shyam Padmanabhan with (4, 7, 8):
- a1,b3,d4,c6,b4,d5,f6
- a6,b4,c6,d4,c2,e3,f1

**Unique triple with lowest sum:** (2, 1, 4) from Richard Turner

### Statistics

Most popular C values (divisors of 2024):
- 2: 335 entries
- 4: 167 entries
- 8: 153 entries
- 1: 126 entries
- 22: 99 entries

The largest integer in any entry was 46. The least positive integer to appear in exactly zero entries was 19.
