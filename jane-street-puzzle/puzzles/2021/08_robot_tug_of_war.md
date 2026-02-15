# Robot Tug-of-War - August 2021

**Category:** Game Theory / Probability
**URL:** https://www.janestreet.com/puzzles/robot-tug-of-war-index/

## Problem Statement

In each one-on-one matchup, two robots are tied together with a rope. The center of the rope has a marker that begins above position 0 on the ground.

The robots alternate pulling on the rope:
- The first robot pulls in the positive direction towards 1
- The second robot pulls in the negative direction towards -1
- Each pull moves the marker a uniformly random draw from [0,1] towards the pulling robot
- If the marker first leaves the interval [-½, ½] past ½, the first robot wins
- If it first leaves the interval past -½, the second robot wins

The organizers noticed that the robot going second is at a disadvantage. They want to handicap the first robot by changing the initial position of the marker to be at some negative real number.

**Question:** Find the position of the marker that makes each matchup a 50-50 competition between the robots (to seven significant digits).
