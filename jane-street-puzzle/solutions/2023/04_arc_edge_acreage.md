# Arc-edge Acreage - April 2023 (Solution)

**Puzzle:** [04_arc_edge_acreage.md](../../puzzles/2023/04_arc_edge_acreage.md)

## Official Solution

### Approach

Ignore the curviness of the segments and imagine them as straight diagonals across a unit square. The largest region we could contain would have area 36 (comprising 18 squares of area 2).

To draw a "curvy" grid containing the same area, replace the 22 perimeter segments with 11 "outward"-bulging quarter circle segments and 11 "inward"-bulging segments.

### Getting Area 32

To get an area of 32, base the curve off a region comprising 16 of the 18 squares. Depending on the choice of squares to omit, the perimeter of the remaining region is either 18, 20, 22, or 24.

### Counting

Counting all the cases for removing 2 boxes, and accounting for mirror symmetry:

2 × Binomial[18,9] + 36 × Binomial[20,10] + 56 × Binomial[22,11] + 16 × Binomial[24,12]

### Answer

**89,519,144**

**Solution image:** https://www.janestreet.com/puzzles/arc-edge-acreage-solution.png
