# Andy's Morning Stroll - July 2022 (Solution)

**Puzzle:** [07_andys_morning_stroll.md](../../puzzles/2022/07_andys_morning_stroll.md)

## Official Solution

Andy normally strolls across the hexagons of a soccer ball. The average length of this stroll turns out to be exactly **20**.

The intuition: Imagine Andy took an extremely long stroll on these hexagons without stopping and we chopped that stroll into segments starting and ending at his home square. The symmetry of the ball suggests, in the limit of the length of the stroll going to infinity, exactly 1/20 of the hexagons Andy visits will be his home hexagon. This means the sum of the lengths of all segments divided by the number of segments approaches 20.

We need to compute the probability that his stroll on the kitchen floor will strictly exceed twenty steps. Using a transition matrix construction:

**Answer: p ≈ 0.4480326**
