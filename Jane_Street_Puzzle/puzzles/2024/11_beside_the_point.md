# Beside the Point - November 2024

**Category:** Geometric Probability
**Difficulty:** Medium-Hard
**URL:** https://www.janestreet.com/puzzles/beside-the-point-index/

## Problem Statement

Two random points—one red and one blue—are selected uniformly and independently from within a square's interior.

**Question:** What is the probability that a point exists on the side of the square nearest to the blue point that maintains equal distance to both colored points?

**Answer format:** Ten decimal places (or exact answer accepted)

## Key Concepts to Apply

- Geometric probability
- Perpendicular bisectors
- Area calculations with integration
- Symmetry arguments

## Visual Intuition

For a point on an edge to be equidistant to both the red and blue points, the perpendicular bisector of the segment connecting them must intersect that edge.

The "nearest edge to the blue point" constraint adds complexity—you need to consider which of the 4 edges is closest based on blue's position.

## Hints for Solving

1. Use symmetry: divide the square into 8 triangular regions
2. For a point in one octant, determine valid positions for the second point
3. The valid region forms a symmetric difference of two circles
4. Integrate over all positions to find the total probability

## My Attempt

[Write your solution approach here]

---

## Official Solution

### Approach
"Given the first point, without loss of generality uniformly selected from a lower triangular octant of the square outlined in black above, the second point would need to be in the blue-shaded symmetric difference of two circles centered at the bottom vertices."

### Mathematical Setup
The problem reduces to computing the area of regions where the perpendicular bisector of the two points intersects the nearest edge.

### Final Answer
**(1 + 2π - ln(4))/12 ≈ 0.4914075788**

### Breakdown
- The 1 comes from base cases
- The 2π comes from circular arc areas
- The -ln(4) comes from logarithmic integration terms
- All divided by 12 from the octant symmetry

## Lessons Learned

1. Geometric probability problems often benefit from symmetry reduction
2. The perpendicular bisector interpretation is key
3. Exact answers involving π and ln are common in these problems
4. Breaking into octants simplifies the "nearest edge" constraint
