# Alter/Nate - January 2020 (Solution)

**Puzzle:** [01_alter_nate.md](../../puzzles/2020/01_alter_nate.md)

## Official Solution

Nate (the first player) wins by starting with **3**.

After starting with 3, Nate can force the running total to increment by units of 12:

1. If Alter picks some number X between 2 and 10, Nate chooses 12-X
2. If Alter picks 1, Nate responds by picking 1 as well. Now Alter cannot pick 10 (since this would force the sum of the previous two numbers to be 11), and must pick some other number Y. Nate then picks 10-Y.

This way, Nate forces Alter to choose when the running total is 3, 15, 27, 39, 51, 63, 75, 87, and 99. At 99, Alter is forced to take the total to 100 or greater.
