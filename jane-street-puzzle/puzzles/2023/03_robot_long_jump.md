# Robot Long Jump - March 2023

**Category:** Game Theory / Probability
**URL:** https://www.janestreet.com/puzzles/robot-long-jump-index/

## Problem Statement

Head-to-head long jump contests consist of rounds in which each robot has a single *attempt* to score.

In an attempt, a robot speeds down the running track (modeled as the numberline) from 0 (the starting line) to 1 (the takeoff point).

A robot moves along this track by drawing a real number uniformly from [0,1] and adding it to the robot's current position. After each of these advances, the robot must decide whether to jump or wait.

- If a robot crosses the takeoff point (at 1) **before jumping**, its attempt receives a score of 0
- If the robot jumps before crossing 1, it draws one final real number from [0,1] and adds it to its current position — this final sum is the score of the attempt

In a head-to-head contest, two robots each have a single attempt without knowing the other's result. In case of a tie (typically because both scored 0), that round is discarded and a new round begins. As soon as one robot scores higher than the other on the same round, that robot is declared the winner!

Assume both robots are programmed to optimize their probability of winning and are aware of each other's strategies. You are watching a match's very first attempt.

**Question:** What is the probability that this attempt scores 0?

**Answer format:** Decimal rounded to 9 digits past the decimal point.
