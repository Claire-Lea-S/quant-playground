# Robot Capture-the-Flag - April 2024

**Category:** Game Theory / Geometry
**URL:** https://www.janestreet.com/puzzles/robot-capture-the-flag-index/

## Problem Statement

Two robots, Aaron and Erin, begin at the center of a unit circle. A flag is randomly placed inside the circle.

**Information asymmetry:**
- Aaron learns the flag's distance (r) from center
- Erin learns only its direction (θ) in polar coordinates

**Rules:**
- Each robot may make a single move after the flag is placed
- Robots act without knowledge of each other's actions
- Movement must stay within the circle boundaries
- Erin is programmed to play a fixed distance *e* along the detected angle θ

**Winning Condition:** Whichever robot is closer to the flag after these moves captures the flag and is declared the winner.

**Challenge:** Determine the probability Aaron wins, assuming optimal play by both robots, given Erin's fixed-distance movement strategy.

**Answer format:** 10 decimal places.
