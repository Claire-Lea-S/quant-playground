# Eldrow - February 2022

**Category:** Word Puzzle
**URL:** https://www.janestreet.com/puzzles/eldrow-index/

## Problem Statement

The daily puzzle game Wordle has taken the world by storm! In Wordle, players try to track down the mystery five-letter word in as few guesses as possible, with each guess returning letter coloring (green for correct position, yellow for wrong position, gray for not in word).

We are playing *Eldrow*, the game of searching for the longest possible chain of hard-mode guesses.

In hard-mode, every subsequent guess has to satisfy all clues left by previous guesses (each guess has to have a possibility of being the mystery word conditional on the responses of all previous guesses).

**Challenge:** What is the longest hard-mode guess sequence you can find?

Submit your answer as a comma-separated list of words from the official Wordle word list, in the order guessed, with the final word being the chosen target word.

**Note:** There is a fairly straightforward proof that an (unachievable) upper bound on the length of an Eldrow sequence is 26 words.
