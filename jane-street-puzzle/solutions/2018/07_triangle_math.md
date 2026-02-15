# Triangle Math - July 2018 (Solution)

**Puzzle:** [07_triangle_math.md](../../puzzles/2018/07_triangle_math.md)

## Official Solution

**Answer: 2^n − 1**

The solution involves Pick's theorem and modular arithmetic. Each acute triangle can "generate" larger triangles by extending sides to double the area.

The number of acute isosceles triangles at level n is simply n. Each isosceles triangle at level n generates one scalene triangle at level n+1. Each scalene triangle at level n generates 3 triangles at level n+1.

Building a recursive formula leads to the total number being 2^n - 1.

**Solution image:** https://www.janestreet.com/puzzles/Jul18_solution.png
