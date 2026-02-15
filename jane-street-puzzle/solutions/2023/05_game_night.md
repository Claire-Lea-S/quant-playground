# Game Night! - May 2023 (Solution)

**Puzzle:** [05_game_night.md](../../puzzles/2023/05_game_night.md)

## Official Solution

### Step 1: Find the Grouped Words

**Clothing 9:** POLO, DRESS, TUXEDO, SHOE, SHORTS, BOOT, CAP, GLOVE, SUIT

**Animal 11:** DUCK, SCORPION, OCTOPUS, CUCKOO, PENGUIN, RABBIT, SHARK, DOG, TURTLE, REINDEER, EAGLE

**Food 9:** SOUP, CHEESE, POTATO, PIE, SALAD, CARROT, PIZZA, HAMBURGER, BISCUIT

### Step 2: Binary Encoding

Convert each row to binary (selected word = 1, unselected = 0), giving numbers 0-31, then convert to letters (1=A, 2=B, etc.).

Example: POLO ENGLAND SKYSCRAPER DRESS TUXEDO → 10011 → 19 → 'S'

Reading down: **SCRABBLESUMODD_**

### Step 3: Recurse with Scrabble Sums

Select words with odd Scrabble sum. Reading down gives: **LONGERTHANFIVE_**

### Step 4: Recurse with Length > 5

Select words with more than five letters. Reading down gives: **MIDDLELETTEROF_**

### Step 5: Final Row

All words in the final row are odd length, so extract the middle letter of each word.

### Answer

**SIEVE**
