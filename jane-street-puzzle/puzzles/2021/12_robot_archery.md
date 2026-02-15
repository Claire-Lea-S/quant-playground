# Robot Archery - December 2021

**Category:** Game Theory / Probability
**URL:** https://www.janestreet.com/puzzles/robot-archery-index/

## Problem Statement

Four robots have qualified for the Robot Archery finals:

| Robot | Seed |
|-------|------|
| Aaron | 1 |
| Barron | 2 |
| Caren | 3 |
| Darrin | 4 |

The robots take turns shooting arrows at a target, starting with Aaron and proceeding in order by seed.

When it is a given robot's turn, they shoot a single arrow:
- If it is closer to the center of the target than *all* previous arrows by all players, that robot remains in the tournament, going to the back of the queue to await their next turn
- Otherwise that robot is eliminated immediately

The last robot remaining in the queue is the winner.

Each robot is equally skilled: for any region R on the target with nonzero area, the robots all have the same positive probability of landing an arrow within R on any given shot.

**Question:** To ten decimal places, what is the probability that **Darrin** will be this year's winner?
