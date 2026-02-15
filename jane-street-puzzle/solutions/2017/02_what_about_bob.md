# What About Bob? - February 2017 (Solution)

**Puzzle:** [02_what_about_bob.md](../../puzzles/2017/02_what_about_bob.md)

## Official Solution

This month's puzzle proved pretty tricky, and we received many submissions which were very close but not quite right.

The smallest 3 numbers for which Bob will win the game are **11, 22, and 32**.

In fact, for larger numbers, Bob will win if N is congruent to 11, 22, or 0 mod 32.

**Analysis:**
- Alice can obviously win for N=1 up to N=9, and she can also win when N=10 if she says 5 (forcing Bob to pick something other than 5).
- When N=11, Bob wins: If Alice picks some k > 1, Bob will be able to pick 11-k. If Alice picks 1, Bob will be able to pick 5.
- For N = 12 up to N = 20, Alice can win by picking the number which gives Bob the tally of N-11. For N = 21, Alice can also win if she picks 5, since Bob must pick something other than 5.
- When N = 22, Bob wins, for similar reasons as when N = 11.
- When N = 32, Bob wins as well. If Alice says any k other than 5, Bob can say 10-k. If Alice says 5, Bob can say 8, leaving Alice with a remaining sum of 19 but unable to say 8, which again forces a Bob win.
