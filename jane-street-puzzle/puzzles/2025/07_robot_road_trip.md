# Robot Road Trip - July 2025

**Category:** Optimization / Probability
**URL:** https://www.janestreet.com/puzzles/robot-road-trip-index/

## Problem Statement

Robot cars have a top speed (which they prefer to maintain at all times while driving) that's a real number randomly drawn uniformly between 1 and 2 miles per minute. A two-lane highway for robot cars has a fast lane (with minimum speed *a*) and a slow lane (with maximum speed *a*).

When a faster car overtakes a slower car in the same lane, the slower car is required to decelerate to either change lanes (if both cars start in the fast lane) or stop on the shoulder (if both cars start in the slow lane). Robot cars decelerate and accelerate at a constant rate of 1 mile per minute per minute, timed so the faster, overtaking car doesn't have to change speed at all, and passing happens instantaneously.

If cars rarely meet (so you never have to consider a car meeting more than one other car on its trip), and you want to minimize the miles not driven due to passing, what should *a* be set to, in miles per minute?

**Example:** Suppose *a* = 1.2 miles per minute. If a 1.8 mph car overtakes a 1.1 mph car, neither slows down (different lanes). If it overtakes a 1.7 mph car, the slower car decelerates/accelerates to switch lanes, costing 0.25 miles. If a 1.1 mph car overtakes a 1.0 mph car in the slow lane, it loses exactly 1 mile.

**Mathematical clarification:** Assume all car trips are of constant length N. Define f(z, N) to be the value of *a* that minimizes the expected lost distance per car trip due to passing.

**Find:** the limit of [the limit of f(z, N) as z → 0+] as N → ∞

**Answer format:** 10 decimal places
