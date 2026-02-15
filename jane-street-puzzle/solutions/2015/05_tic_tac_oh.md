# Tic Tac Oh... - May 2015 (Solution)

**Puzzle:** [05_tic_tac_oh.md](../../puzzles/2015/05_tic_tac_oh.md)

## Official Solution

The best way to face off against this computer program is to mark a corner. If the program does not select the middle square, you can always win. If it does (1/8), you select one of the 2 spots adjacent to your first mark. If the computer does not block you, you win. If it does block you (1/6), you block them, and have a chance to win. If the computer blocks you again (1/4), it has forced a tie, but otherwise you win.

So, the best strategy yields a 1-(1/8)(1/6)(1/4) = **191/192** chance of winning.

