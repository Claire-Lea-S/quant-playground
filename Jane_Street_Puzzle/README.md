# Jane Street Puzzle Training System

A comprehensive collection of Jane Street monthly puzzles (2015-2026) designed for learning and improving problem-solving skills.

## Purpose

This repository contains:
1. **Puzzle Archive**: All Jane Street puzzles with descriptions and solutions
2. **Learning System**: Practice solving puzzles and compare with official solutions
3. **Pattern Recognition**: Categorized puzzles by type to identify solving strategies

## Puzzle Categories

Based on analysis of 120+ puzzles, they fall into these main categories:

### 1. Probability/Game Theory ("Robot" series)
- Robot Javelin, Robot Baseball, Robot Capture-the-Flag, Robot Road Trip
- Robot Swimming Trials, Robot Weightlifting, Robot Tug-of-War, Robot Archery
- Focus: Nash equilibrium, optimal strategies, probability calculations

### 2. Grid/Constraint Puzzles
- **Hooks Series**: Hooks 1-11 (grid partitioning + number placement)
- **Knight Moves Series**: Knight Moves 1-6
- **Number Cross Series**: Number Cross 1-5
- **Block Party Series**: Block Party 1-4
- **Hall of Mirrors Series**: Laser reflection puzzles

### 3. Mathematical/Geometric
- Beside the Point, Arc-edge Acreage, Circle Time
- Sum One Somewhere, Some Ones Somewhere
- Focus: Probability, geometry, analysis

### 4. Word/Visual Puzzles
- Dogs Playing Poker, Games Night, Poetry in Motion
- Focus: Decoding, pattern recognition

### 5. Logic/Sudoku Variants
- Remote Sudoku, Somewhat Square Sudoku, Rather Square Sudoku
- Fences series, Twenty Four Seven series

## Directory Structure

```
Jane_Street_Puzzle/
├── README.md
├── puzzle_catalog.json          # Complete puzzle database
├── puzzles/                     # Individual puzzle files
│   ├── 2026/
│   ├── 2025/
│   ├── ...
├── solutions/                   # Solution explanations
├── my_attempts/                 # Your solution attempts
├── analysis/                    # Pattern analysis and learnings
└── scripts/                     # Helper scripts for practice
```

## How to Use

1. **Browse puzzles**: Check `puzzle_catalog.json` for the full list
2. **Pick a puzzle**: Read the puzzle in `puzzles/YYYY/puzzle_name.md`
3. **Attempt solution**: Write your solution in `my_attempts/`
4. **Compare**: Check official solution in `solutions/`
5. **Learn**: Document insights in `analysis/`

## Puzzle Solving Tips (from patterns observed)

### For Robot/Game Theory Puzzles:
- Look for Nash equilibrium conditions
- Use backward induction from end states
- Set up indifference equations

### For Grid Puzzles:
- Start with most constrained cells
- Use parity arguments
- Check connectivity requirements

### For Mathematical Puzzles:
- Set up the problem formally with variables
- Look for symmetry to simplify
- Use calculus for optimization

## Sources

All puzzles from [Jane Street Puzzles](https://www.janestreet.com/puzzles/)
