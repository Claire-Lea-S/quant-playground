# Jane Street Puzzle Training System

A comprehensive collection of Jane Street monthly puzzles (2015-2026) designed for learning and improving problem-solving skills.

## Folder Structure

```
Jane_Street_Puzzle/
│
├── puzzles/                        # SOLVING SIDE (AI reads this)
│   ├── 2015/ ... 2026/             # Puzzle files + images
│   │   ├── {month}_{name}.md
│   │   └── {month}_{name}_1.png
│   ├── strategy/                   # Solving strategies by category
│   ├── hints/                      # AI-generated hints (no answers!)
│   ├── attempts/
│   │   └── my_answers.json         # AI records answers here
│   ├── scripts/solvers/            # Computational solvers
│   └── puzzle_catalog.json         # Puzzle metadata
│
├── solutions/                      # ANSWER SIDE (AI never reads this!)
│   ├── 2015/ ... 2026/             # Solution files + images
│   │   └── {month}_{name}.md
│   ├── attempts/                   # Comparison results
│   │   ├── results.csv             # Detailed results per puzzle
│   │   ├── summary.txt             # Score summary by category
│   │   └── attempts_log.csv        # Historical logs
│   └── scripts/
│       └── compare_answers.py      # Compares answers with solutions
│
├── .cursor/skills/solve-puzzle/    # AI solving skill
└── README.md
```

## Two-Phase Workflow

### Phase 1: SOLVE (AI skill)
The AI reads from `puzzles/` only and records answers:

```bash
# AI runs the solve-puzzle skill
# Reads: puzzles/{year}/*.md + images
# Writes: puzzles/attempts/my_answers.json
```

**The AI NEVER reads from `solutions/` folder!**

### Phase 2: COMPARE (Python script)
After solving, run the comparison script:

```bash
python solutions/scripts/compare_answers.py
```

This reads both `puzzles/attempts/my_answers.json` and `solutions/{year}/*.md` to produce:
- `puzzles/attempts/results.csv` - detailed results
- `puzzles/attempts/summary.txt` - score by category

## Puzzle Categories

| Category | Examples |
|----------|----------|
| game_theory | Robot Javelin, Robot Baseball, Tic Tac Oh |
| grid_puzzle | Hooks series, Knight Moves, Number Cross |
| geometry | Beside the Point, Circle Time, Arc-edge Acreage |
| probability | Professor Rando, Bracketology, Swing Time |
| word_puzzle | Ticker Treat, Scraggle, Poetry in Motion |
| visual_puzzle | Dogs Playing Poker, Games Night |
| number_theory | Split Division, What a Trit, Expelled |
| combinatorics | Pair Dance, Triangle Math, Triads |

## Quick Start

1. **AI solves puzzles**: Run the solve-puzzle skill
2. **Check results**: `python solutions/scripts/compare_answers.py`
3. **Review hints**: See `puzzles/hints/{year}/` for insights
4. **Study strategies**: Read `puzzles/strategy/{category}.md`

## Sources

All puzzles from [Jane Street Puzzles](https://www.janestreet.com/puzzles/)
