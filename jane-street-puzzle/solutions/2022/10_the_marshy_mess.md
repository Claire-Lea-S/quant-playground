# The Marshy Mess - October 2022 (Solution)

**Puzzle:** [10_the_marshy_mess.md](../../puzzles/2022/10_the_marshy_mess.md)

## Official Solution

Solve the Hashi (a.k.a. Bridges) logic puzzle with a twist: each of the four puzzles had exactly one inaccurate number.

Solving the four puzzles revealed the correct numbers to be 5, 4, 3, and 1, and also gave a secret message: the doubled bridges spelled out the words "Prob" "no ACES" "givEn" "ShaPE".

The references to packs of playing cards connected with this message to imply we were asking for the probability a bridge hand would have no aces given the shape 5-4-3-1 of the corrected islands.

This can be found going suit-by-suit: a hand with shape 5-4-3-1 would have probability:
8 × 9 × 10 × 12 / 13^4 = **8640/28561 ≈ 0.3025104**

**Solution image:** https://www.janestreet.com/puzzles/the-marshy-mess-solution-fixed.png
