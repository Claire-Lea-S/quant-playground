# Robot Javelin - December 2025

**Category:** Game Theory / Probability
**URL:** https://www.janestreet.com/puzzles/robot-javelin-index/

## Problem Statement

It's the Robot Javelin finals! The rules:

1. **First throw**: Each robot's initial throw distance is uniformly drawn from [0, 1]
2. **Decision point**: Without knowing the opponent's result, each robot chooses to either keep their distance or discard it
3. **Second throw option**: If discarded, they receive a new distance (also uniform from [0, 1]) which they must keep
4. **Winner**: The robot with the larger final distance wins

Your robot (Java-lin) normally plays the Nash equilibrium strategy. However, the opposing "Spears Robot" has discovered a protocol exploit: they receive one bit of information revealing whether your first throw was above or below a threshold *d* of their choosing—before making their own decision.

Spears has optimized *d* to maximize their winning probability, assuming you remain at equilibrium.

**Challenge:** Determine Java-lin's winning probability if you adapt your strategy optimally while Spears still expects you to play the standard Nash equilibrium.

**Answer format:** Exact terms or decimal to 10 places.
