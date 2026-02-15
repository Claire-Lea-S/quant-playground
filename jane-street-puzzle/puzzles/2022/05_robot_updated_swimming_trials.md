# Robot Updated Swimming Trials - May 2022

**Category:** Game Theory
**URL:** https://www.janestreet.com/puzzles/robot-updated-swimming-trials-index/

## Problem Statement

This is a follow-up to the October 2021 Robot Swimming Trials puzzle.

The tournament directors choose a positive integer *N*, and then 3*N* robots are invited to compete in the trials, which are *N* races between all 3*N* robots. The robots commit to using a schedule of their identical fuel amounts to the *N* races, and on a given race whatever robot burns the most fuel wins (ties are split uniformly randomly).

All robots swim in all races according to their schedules, and then *N* distinct winners are determined by successively selecting the robot from the remaining races that spent the most fuel and finished ahead of all other robots that haven't yet won a race.

The discrete strategy is one in which a robot chooses a race uniformly randomly and assigns all of its fuel to that race.

With *N* = 8 (24 robots, 8 races), the discrete strategy is no longer optimal. The metagame evolved and eventually settled into a Nash equilibrium in which a given competitor chooses the discrete strategy with a certain probability *p*, and otherwise elects for an allotment that distributes nonzero fuel to at least two races.

**Find *p***, the probability a robot using the Nash equilibrium strategy devotes all of its fuel to a single race, to 6 significant digits.
