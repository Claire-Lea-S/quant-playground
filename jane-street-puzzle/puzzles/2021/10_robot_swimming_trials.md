# Robot Swimming Trials - October 2021

**Category:** Game Theory / Probability
**URL:** https://www.janestreet.com/puzzles/robot-swimming-trials-index/

## Problem Statement

In the Robot Swimming Trials, 3*N* identical robots compete for *N* equivalent spots in the finals by swimming *N* races.

Each robot precommits to spending a certain amount of its fuel in each race (an N-tuple of nonnegative real numbers summing to 1). After all races are run, spots in the finals are given to the winners of the races, moving from fastest winner to slowest. Once a robot wins a race, it is ineligible to win another race. A robot's speed is strictly increasing in the amount of fuel it spends. Ties are broken by randomly choosing the winner among robots that spent the same amount of fuel.

Over the history of the RST, the metagame settled into what was widely believed to be the Nash equilibrium: each robot uniformly randomly selects a race and devotes all of their fuel to it (the **discrete strategy**).

However, rumors are circulating that for a large enough *N*, the discrete strategy is NOT the Nash equilibrium.

**Questions:**
1. What is the smallest *N* for which the trial does **not** have the discrete strategy as the Nash equilibrium?
2. For this *N*, if the other 3*N*-1 robots naively play the discrete strategy and your robot plays optimally, with what probability *p* will you make the finals?

**Answer format:** "*N*, *p*" (with *p* rounded to 6 significant digits)
