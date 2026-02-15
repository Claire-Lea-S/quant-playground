# Bracketology 101 - April 2021 (Solution)

**Puzzle:** [04_bracketology_101.md](../../puzzles/2021/04_bracketology_101.md)

## Official Solution

The most straightforward way to solve this puzzle was to compute the probability distributions of the winners of each match recursively, given each swap.

The most advantageous swap for the 2-seed is to swap seeds **3 and 16**, which increases the 2-seed's probability of winning by **6.55795%**.

One easy mistake to make was to accidentally report the 1-seed's probability of winning after swapping the 2-seed with the 1-seed. This swap is good for the 2-seed, but only increases their probability of winning from 21.6040% to 23.0283%, so 1.4243%.
