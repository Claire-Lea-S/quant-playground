# Dogs Playing Poker - August 2025 (Solution)

**Puzzle:** [08_dogs_playing_poker.md](../../puzzles/2025/08_dogs_playing_poker.md)

## Official Solution

This puzzle was inspired by the kitsch classic painting Dogs Playing Poker. We are told there are clues about what the middle pooch is holding, in the cards and emotions of the other dogs (and one cat) at the table.

### The Pattern

Every face is a version of a standard emoji. The names of these emojis can be indexed into by the card holdings (all numbers 1-10, interpreting aces as 1). Reading the letters for each card from left to right gives the first clue.

For example, the leftmost pooch, clearly quite FLUSHED, has a 4 of clubs and a 5 of hearts, which correspond to the fourth and fifth letters of FLUSHED: 'S' and 'H'.

Reading these 16 letters off left to right and adding spaces gives: **SHIFT BY CHIP COUNT**

### Second Step

Take these same letters and shift them forward in the alphabet by the number of chips piled nearest to the card they correspond to.

| # | Emoji | Name | L Card | R Card | Letters | L Chips | R Chips | Shifted |
|---|-------|------|--------|--------|---------|---------|---------|---------|
| 1 | 😳 | FLUSHED | 4 | 5 | SH | 1 | 0 | TH |
| 2 | 🤤 | DROOLINGFACE | 6 | 8 | IF | 22 | 23 | EC |
| 3 | 🤠 | COWBOYHATFACE | 9 | 4 | TB | 7 | 12 | AN |
| 4 | 🥴 | WOOZYFACE | 5 | 8 | YC | 10 | 11 | IN |
| 5 | 😧 | ANGUISHED | 7 | 5 | HI | 23 | 6 | EO |
| 6 | 😾 | POUTINGCAT | 1 | 8 | PC | 16 | 0 | FC |
| 7 | 😖 | CONFOUNDED | 5 | 6 | OU | 23 | 0 | LU |
| 8 | 😝 | SQUINTINGFACE… | 8 | 6 | NT | 14 | 25 | BS |

The shifted letters spell out: **THE CANINE OF CLUBS**

### Final Answer

"Canine of clubs" is a nickname for the Texas Hold'em hand **Kc,9c**, since saying "K-9" out loud sounds like the word "canine".

**Answer: Kc,9c**
