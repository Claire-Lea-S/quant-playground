# Subtiles 2 — Jane Street Puzzle, February 2026

## Puzzle Summary
- 13x13 grid (169 cells)
- Place values 1..N; value K appears exactly K times as a connected K-omino
- Each K-omino must "contain" the (K-1)-omino shape (rotations/reflections allowed)
- 37 labeled cells have algebraic expressions in unknowns a, b, c
- **Goal**: Find a, b, c → fill grid → Answer = min(row_sum) × max(row_sum)

## Directory Structure
```
Feb-26/
├── STATUS.md              ← You are here
├── instruction/
│   ├── puzzle-image.png   ← Original puzzle image
│   └── instructions.md    ← Puzzle rules
├── solving/               ← Active work (numbered scripts)
│   └── 01_find_abc.py     ← Step 1: brute-force search for a, b, c
└── archive/               ← Old approaches (dead ends, run reports)
```

## Solution Pipeline
1. **Find a, b, c** — determine the three unknowns (`01_find_abc.py`)
2. **Compute cell values** — evaluate all 37 expressions
3. **Fill the grid** — place K-ominoes satisfying containment
4. **Compute answer** — min(row_sum) × max(row_sum)

## What We Know

### Proven facts (from original expressions):
- **b = 2** (forced by intersection of b², 8-b, 11-b, (b-1)²)
- **c ∈ {2, 3, 4}** (from c^b ≤ 17 and 6c-4b ≥ 1)
- **a ∈ {2, 3}** (from b/(a-1) = 2/(a-1) must be positive integer)
- **a ≠ c** (division by zero otherwise)
- Only **4 candidates**: (2,2,3), (2,2,4), (3,2,2), (3,2,4)

### Problem:
With original expressions, best candidate is (3,2,2) scoring only **17/37**.
20 expressions evaluate to non-integers, negatives, or undefined.

## Current Step
**Running `01_find_abc.py`** — wide brute-force search (a,b,c ∈ [1,30])
to confirm or disprove the 4-candidate theory.
