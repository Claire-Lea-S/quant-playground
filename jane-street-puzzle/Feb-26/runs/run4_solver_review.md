# Run 4: Detailed Solver Code Review

## Overview

Two solvers have been written for the February 2026 Jane Street "Subtiles 2" puzzle:
- `solver_anthropic.py` -- Full pipeline: variable search (Phase 1), grid backtracking (Phase 2), answer computation (Phase 3).
- `solver_openai.py` -- Grid placement only: given usable cells and optional fixed clues, backtrack from N down to 1 placing connected K-ominoes with shape nesting.

This review covers correctness, bugs, performance concerns, and architectural issues.

---

## 1. Grid Dimensions Discrepancy

**CRITICAL ISSUE across both solvers and constraint docs.**

| Source | Grid Size | Total Cells | Max N |
|--------|-----------|-------------|-------|
| `solver_anthropic.py` | 13x13 | 169 | 17 |
| `solver_openai.py` | N/A (uses only labeled cells) | 37 | 8 |
| `constraints.md` | 13x11 | 143 | 16 |
| `constraints_formal.md` | 13x11 | 143 | 16 |
| Puzzle image | Appears 13x13 | 169 | 17 |

The labeled cells have max column index 11 (cell (10,11)), which is consistent with a 13x13 grid (columns 0-12). Looking at the puzzle image, the grid indeed appears to be 13x13. The `constraints.md` files say 13x11, which may be an error -- this needs verification against the puzzle image.

**Verdict:** The puzzle image should be the ground truth. If the grid is 13x13, then `solver_anthropic.py` is correct (169 cells, max N=17). The constraint documents may have a transcription error.

---

## 2. solver_anthropic.py -- Detailed Review

### 2.1 Phase 1: Variable Search (`find_variables`)

**Search ranges:**
```python
a_range=range(1, 30)   # a in [1, 29]
b_range=range(1, 20)   # b in [1, 19]
c_range=range(2, 20)   # c in [2, 19]
```

**BUG: c starts at 2, but the puzzle says a, b, c are positive integers, so c=1 is valid.**

Looking at the expressions:
- `(2,3)`: `(b + c) / (c - 1)` -- division by zero when c=1
- But other expressions might work with c=1 if this particular one is excluded or doesn't matter.

Actually, if c=1, then `(c - 1) = 0` causes division by zero in `(2,3)`, and `log_c(a)` at `(9,2)` requires `log(1) = 0` in the denominator (division by zero). So c=1 is effectively excluded by the constraints. **Starting c at 2 is correct.**

However, the skip condition `if a == c: continue` is too aggressive. While many expressions have `(a - c)` denominators, `safe_eval` already handles ZeroDivisionError. Skipping `a == c` entirely is fine as an optimization since 6+ expressions have `(a - c)` in the denominator, so a=c can never produce valid results.

**Efficiency concern:** The innermost loop iterates over N from 1 to 17 for each (a, b, c). This is wasteful because `evaluate_all` doesn't depend on N -- the N filter is just `max_val`. A better approach:
1. Evaluate expressions once for (a, b, c).
2. If all are positive integers, set N = max(expression values).
3. Check N(N+1)/2 <= TOTAL_CELLS.

This would eliminate 17x redundant evaluations. Current approach is O(29 * 19 * 18 * 17) ~= 168k iterations of `evaluate_all`. Not terrible, but wasteful.

**BUG: The `max_v != N` check is semantically correct** (ensures N equals the max expression value, not larger), but combined with the inner N loop, it means we only find results where N exactly equals the max expression value. This is actually correct behavior -- N is determined by the expressions.

### 2.2 Expression Lambdas vs. grid.json

Cross-checking each expression lambda against grid.json:

| Cell | grid.json | Lambda | Match? |
|------|-----------|--------|--------|
| (0,4) | `6c - 4b` | `6*c - 4*b` | YES |
| (1,6) | `8 - b` | `8 - b` | YES |
| (2,1) | `(a^b - 4) / (6c + 1)` | `(a**b - 4) / (6*c + 1)` | YES |
| (2,3) | `(b + c) / (c - 1)` | `(b + c) / (c - 1)` | YES |
| (2,5) | `b^2 - b/c` | `b**2 - b / c` | YES |
| (2,7) | `sqrt(30 + a) / c` | `math.sqrt(30 + a) / c` | YES |
| (2,9) | `(a + b) / (c - 3a)` | `(a + b) / (c - 3*a)` | YES |
| (3,4) | `(b - 3a) / (a - c)` | `(b - 3*a) / (a - c)` | YES |
| (3,6) | `8a - 2b` | `8*a - 2*b` | YES |
| (3,8) | `b / (a - c)` | `b / (a - c)` | YES |
| (3,10) | `(b + 9) / sqrt(c - a)` | `(b + 9) / math.sqrt(c - a)` | YES |
| (4,1) | `18 / (ac + 1)` | `18 / (a*c + 1)` | YES |
| (4,5) | `c^b` | `c**b` | YES |
| (4,9) | `(3 + b^2) / sqrt(3 + 2c)` | `(3 + b**2) / math.sqrt(3 + 2*c)` | YES |
| (5,3) | `b / (a^2 - c^2)` | `b / (a**2 - c**2)` | YES |
| (5,10) | `sqrt(a + 2) / a` | `math.sqrt(a + 2) / a` | YES |
| (6,2) | `a^b - 12/a` | `a**b - 12 / a` | YES |
| (6,4) | `2c + c/a` | `2*c + c / a` | YES |
| (6,6) | `4a - 5b` | `4*a - 5*b` | YES |
| (6,8) | `c + 2a` | `c + 2*a` | YES |
| (6,10) | `b / (9a - 5c)` | `b / (9*a - 5*c)` | YES |
| (7,0) | `(b^3 + 2c) / (b + 2c)` | `(b**3 + 2*c) / (b + 2*c)` | YES |
| (7,8) | `b / (a - 1)` | `b / (a - 1)` | YES |
| (8,2) | `(c - b) / (2a)` | `(c - b) / (2*a)` | YES |
| (8,6) | `b / (a - c)` | `b / (a - c)` | YES |
| (8,10) | `(b + c) / (a - c)` | `(b + c) / (a - c)` | YES |
| (9,2) | `log_c(a)` | `math.log(a) / math.log(c)` | YES |
| (9,4) | `(c^2 - b) / a` | `(c**2 - b) / a` | YES |
| (9,6) | `(b - 1)^2` | `(b - 1)**2` | YES |
| (9,8) | `cbrt(43 - ac) / a` | `(abs(43-a*c)**(1/3) * sign) / a` | CLOSE (see below) |
| (10,3) | `(b - a) / (a - c)` | `(b - a) / (a - c)` | YES |
| (10,5) | `11 - b` | `11 - b` | YES |
| (10,7) | `(b - 2a) / (a - c)` | `(b - 2*a) / (a - c)` | YES |
| (10,9) | `(c + 3) / a` | `(c + 3) / a` | YES |
| (10,11) | `8c - b/c` | `8*c - b / c` | YES |
| (11,5) | `b^2` | `b**2` | YES |
| (12,8) | `(2^b + 1) / (ac)` | `(2**b + 1) / (a*c)` | YES |

**All lambdas match grid.json.** The cube root at (9,8) uses a sign-preserving implementation for negative arguments, which is appropriate.

Note: Whether grid.json itself matches the puzzle image is a separate question (handled by the image-verifier task).

### 2.3 safe_eval

```python
def safe_eval(func, a, b, c):
    try:
        val = func(a, b, c)
        if val is None: return None
        if isinstance(val, complex): return None
        if math.isnan(val) or math.isinf(val): return None
        return val
    except (ZeroDivisionError, ValueError, OverflowError, TypeError):
        return None
```

**Looks correct.** Handles:
- Division by zero (ZeroDivisionError)
- sqrt of negative (ValueError)
- Huge exponents (OverflowError)
- Complex results (complex check)
- NaN/Inf results

**Minor issue:** `math.sqrt(-1)` raises ValueError in Python, not complex. But `(-1)**0.5` returns a complex number in Python 3. The `isinstance(val, complex)` check handles the latter case. Good.

### 2.4 is_positive_integer

```python
def is_positive_integer(x, tol=1e-9):
    if x is None: return False
    if not isinstance(x, (int, float)): return False
    if math.isnan(x) or math.isinf(x): return False
    return x > tol and abs(x - round(x)) < tol
```

**Correct.** The tolerance of 1e-9 is appropriate for floating-point arithmetic. The `x > tol` check ensures the value is strictly positive (not zero or negative).

### 2.5 Phase 2: GridSolver Backtracking

**CRITICAL BUG: Massive search space, practically unsolvable.**

The `solve()` method iterates over ALL empty cells (169 - 37 = 132 cells) and for each tries values 0 through N. This is a branching factor of up to 18 at each of 132 cells, giving a search tree of ~18^132 -- completely intractable.

**Problems with the backtracking approach:**

1. **No early termination on connectivity:** Connectivity and containment are only checked at the very end (`idx == len(cells)`). This means the solver explores the entire tree before validating constraints.

2. **Adjacency check has a bug (lines 344-354):**
```python
existing_k = [(er, ec) for er in range(self.rows) for ec in range(self.cols)
              if self.grid[er][ec] == k]
if existing_k:
    if not any((nr, nc) == (r, c) or
               (abs(nr - r) + abs(nc - c) == 1 and self.grid[nr][nc] == k)
               for nr, nc in existing_k):
        adjacent = any(abs(er - r) + abs(ec - c) == 1
                       for er, ec in existing_k)
        if not adjacent:
            continue
```

This code is confusing and partially redundant:
- The first `any(...)` checks if (r,c) IS an existing k-cell (impossible since it's empty) OR if some existing k-cell is adjacent AND has value k (redundant since we filtered by value k).
- The second `adjacent` check actually does the right thing: checks if (r,c) is adjacent to any existing k-cell.
- The overall logic works but is unnecessarily convoluted. The whole block should just be:
```python
if existing_k:
    if not any(abs(er - r) + abs(ec - c) == 1 for er, ec in existing_k):
        continue
```

3. **O(rows*cols) scan for existing_k on every cell/value pair:** This scans the entire grid to find cells with value k, on every recursive call. Should cache cell positions per value.

4. **No pruning on remaining capacity:** The only pruning is checking if enough cells remain to fill `remaining_needed`, but this doesn't account for individual value capacities.

**Verdict: This solver is architecturally correct but will never terminate for non-trivial inputs due to exponential search space without adequate pruning.**

### 2.6 shape_contains (Containment Check)

```python
@staticmethod
def shape_contains(big, small):
    big_set = set(big)
    for oriented_small in GridSolver.all_orientations(small):
        for dr in range(-20, 21):
            for dc in range(-20, 21):
                translated = {(r + dr, c + dc) for r, c in oriented_small}
                if translated.issubset(big_set):
                    return True
    return False
```

**Functionally correct but wildly inefficient:**
- Iterates over 41 * 41 = 1681 translations for each of up to 8 orientations.
- Total: up to 13,448 subset checks per containment test.
- **Better approach:** For each orientation, compute the valid translation range from the bounding boxes, reducing to O(|big|) translations.
- Or even better: for each orientation, for each cell in the oriented small shape, try anchoring it to each cell in big, then check if all other cells are in big. This is O(|big| * |small| * 8).

However, since shapes are at most 17 cells, the current approach is acceptable for correctness verification, just slow.

**The range [-20, 21] is sufficient** since shapes are normalized to origin and big shapes are at most 17 cells, so offsets beyond ~17 are unnecessary. Could be tightened.

### 2.7 Connectivity Check

```python
def is_connected(self, value):
    cells = [(r, c) for r in range(self.rows) for c in range(self.cols)
             if self.grid[r][c] == value]
    if len(cells) <= 1:
        return True
    visited = {cells[0]}
    queue = deque([cells[0]])
    cell_set = set(cells)
    while queue:
        r, c = queue.popleft()
        for nr, nc in self.neighbors(r, c):
            if (nr, nc) in cell_set and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return len(visited) == len(cells)
```

**Correct.** Standard BFS connectivity check. Only concern: called for ALL values at the end, meaning O(N * rows * cols) to find cells per value. Could be cached.

### 2.8 all_orientations

```python
transforms = [
    lambda r, c: (r, c),       # identity
    lambda r, c: (c, -r),      # 90 CW
    lambda r, c: (-r, -c),     # 180
    lambda r, c: (-c, r),      # 270 CW
    lambda r, c: (r, -c),      # reflect H
    lambda r, c: (-r, c),      # reflect V
    lambda r, c: (c, r),       # reflect diag
    lambda r, c: (-c, -r),     # reflect anti-diag
]
```

**Correct.** These are the 8 elements of the dihedral group D4. The deduplication via `seen` set handles cases where some orientations produce the same normalized shape (e.g., a square is invariant under all 8).

### 2.9 Phase 3: Answer Computation

```python
def compute_answer(grid, labeled_positions):
    row_sums = []
    for r in range(len(grid)):
        s = sum(grid[r][c] for c in range(len(grid[0]))
                if (r, c) in labeled_positions)
        row_sums.append(s)
    nonzero_sums = [s for s in row_sums if s > 0]
    min_s = min(nonzero_sums)
    max_s = max(nonzero_sums)
    return min_s, max_s, min_s * max_s
```

**Correct.** Computes row sums over labeled cells only, then takes min/max of rows that have at least one labeled cell. Matches the puzzle instructions: "compute, in each row, the sum of the labeled cells. The answer is the product of the maximum and minimum row sums."

**Note:** The puzzle says "row sums" -- it's ambiguous whether rows without labeled cells should count (with sum 0). The solver excludes them (`nonzero_sums`), which is the reasonable interpretation since including zero-sum rows would make the minimum always 0 and the answer always 0.

---

## 3. solver_openai.py -- Detailed Review

### 3.1 CRITICAL BUG: USABLE_CELLS Too Restrictive

```python
USABLE_CELLS: List[Coord] = [
    (0, 4),
    (1, 6),
    (2, 1), (2, 3), (2, 5), (2, 7), (2, 9),
    ...  # 37 cells total
]
```

**This is the most critical bug in the entire codebase.** USABLE_CELLS only contains the 37 labeled cells. But the puzzle grid has ALL cells usable -- labeled cells have fixed values from expressions, while all other cells can be filled with any value or left empty.

With only 37 usable cells, the max feasible N is 8 (since 8*9/2 = 36 <= 37, but 9*10/2 = 45 > 37). This severely constrains the problem and will likely yield no solution or a wrong solution.

**Fix:** USABLE_CELLS should contain ALL cells of the 13x13 (or 13x11, depending on actual grid size) grid:
```python
USABLE_CELLS = [(r, c) for r in range(13) for c in range(13)]
```

And the FIXED dict should contain the evaluated expression values:
```python
FIXED = {(0,4): val_04, (1,6): val_16, ...}  # from Phase 1
```

### 3.2 Polyomino Enumeration (`connected_subsets_of_size`)

The enumeration generates connected subsets of a given size from remaining cells, with optional forced inclusion.

**BUG: Duplicate enumeration.** In `connected_subsets_of_size` when `must_include` is empty:
```python
for seed in remaining:
    yield from _grow_connected_from_seed(remaining, size, {seed})
```

This will generate the SAME connected subset multiple times -- once for each cell that could be a seed. For example, a 3-cell connected region {A, B, C} will be generated when seeding from A, B, and C separately. This causes massive redundancy.

**Fix:** Use a canonical ordering to ensure each subset is generated exactly once. For example, only seed from the lexicographically smallest cell.

**Additional issue in `_grow_connected_from_seed`:** The growth explores all possible orderings of adding frontier cells, leading to the same subset being generated via different orderings. The `is_connected` check at the end is redundant since growth from a seed along the frontier always produces connected sets.

### 3.3 shape_contains_prev (Nesting Condition)

```python
def shape_contains_prev(shape_k, shape_km1):
    sk = list(shape_k)
    target = shape_km1
    sk_set = set(sk)
    for removed in sk:
        rem_set = set(sk_set)
        rem_set.remove(removed)
        if not is_connected({(r, c) for (r, c) in rem_set}):
            continue
        cand = canonical_shape(rem_set)
        if cand == target:
            return True
    return False
```

**IMPORTANT SEMANTIC QUESTION: Is this the correct interpretation of "contain"?**

The puzzle says: "for each K > 1 the K-omino must 'contain' the shape formed by the (K-1)'s."

There are two possible interpretations:

**Interpretation A (solver_openai):** The (K-1)-omino shape must be obtainable by removing exactly one cell from the K-omino (leaving a connected shape). This means shape(K-1) is a sub-polyomino of shape(K).

**Interpretation B (solver_anthropic):** The (K-1)-omino shape, under some rotation/reflection, can be translated to fit entirely within the K-omino. This is geometric containment -- the smaller shape fits inside the bigger one.

These are **different** constraints! Interpretation A is strictly stronger -- it requires the (K-1)-omino to be shape(K) minus exactly one cell. Interpretation B allows the (K-1)-omino to fit inside shape(K) at any position.

**Looking at the puzzle wording:** "the K-omino must 'contain' the shape formed by the (K-1)'s. (Rotations and reflections are allowed.)"

And from `constraints_formal.md`:
```
{T_i(p) + (dr, dc) : p in norm(shape(k-1))} subset shape(k)
```

This is Interpretation B -- geometric containment (subset relationship after transformation). **solver_anthropic.py is correct; solver_openai.py uses a stricter condition that may miss valid solutions.**

However, Interpretation A implies Interpretation B (if you can remove one cell to get shape(K-1), then shape(K-1) certainly fits inside shape(K)). So solver_openai won't produce invalid solutions, but it may fail to find solutions that exist under the true constraint.

**In practice for this puzzle, the containment must be cell-removal based** because the shapes grow by exactly one cell at each level (K cells for value K, K-1 cells for value K-1). Since K-omino has K cells and (K-1)-omino has K-1 cells, and the (K-1)-omino must geometrically fit inside the K-omino, this means the K-omino is the (K-1)-omino plus one extra cell. So **both interpretations are actually equivalent here** given the count constraint.

**Proof:** If |shape(K)| = K and |shape(K-1)| = K-1, and shape(K-1) (up to rigid transformation) is a subset of shape(K), then since we map K-1 cells into K cells, there's exactly one uncovered cell. So shape(K) = T(shape(K-1)) + one cell. And since shape(K) is connected and shape(K-1) is connected, the remainder after removing the one cell is still connected (it's the transformed (K-1)-omino which is connected). So the "remove one cell" condition is equivalent to "geometric containment" given the exact size constraints.

**Verdict: Both interpretations are equivalent given the count constraint. solver_openai's approach is correct in this specific context.**

### 3.4 Backtracking Order (N down to 1)

```python
def backtrack(k: int) -> bool:
    if k == 0:
        return True
    # ... place k-omino, then recurse to k-1
```

**This is a good design choice.** Placing larger polyominoes first is generally better because:
1. Larger polyominoes have fewer valid placements, so the branching factor is lower at the top of the search tree.
2. The nesting constraint can be checked immediately (does shape(K-1) fit in shape(K)?).
3. Pruning is more effective -- placing the big pieces first eliminates more of the search space.

However, this conflicts with the nesting check: when placing K, we need to verify that shape(K-1) can fit in shape(K). But shape(K-1) isn't placed yet! The solver handles this by checking the constraint when placing K-1 (does shape(K-1) fit in shape(K), the already-placed one?). This is correct.

### 3.5 Shape Canonicalization

```python
def transforms(points):
    def rot90(p): return (c, -r)
    def reflect(p): return (r, -c)
    out = []
    current = pts
    for _ in range(4):
        out.append(current)
        out.append([reflect(p) for p in current])
        current = [rot90(p) for p in current]
    return out
```

**Correct.** Generates all 8 orientations via 4 rotations x 2 (with/without reflection).

```python
def canonical_shape(points):
    best = None
    for tpts in transforms(pts):
        norm = normalize_shape(tpts)
        if best is None or norm < best:
            best = norm
    return best
```

**Correct.** Picks lexicographically smallest normalized form across all 8 orientations. This is a valid canonical form for free polyominoes.

### 3.6 Performance Concerns

Even with the USABLE_CELLS bug fixed, the solver faces severe performance challenges:

1. **Exponential polyomino enumeration:** For K=17, enumerating all connected subsets of size 17 from 169 cells is astronomically expensive. The number of 17-cell connected subsets of a 13x13 grid is enormous.

2. **No spatial constraint propagation:** The solver doesn't use the grid structure to prune. For example, if fixed cells for value K are far apart, many candidate regions are infeasible.

3. **Memory:** `shape_to_regions` stores all candidate regions for each K, which could be massive.

**Practical viability:** This solver would need significant optimization to work on the full 169-cell grid. Possible improvements:
- Incremental growth from fixed cells
- Cell-by-cell backtracking (like solver_anthropic) but with value-group awareness
- Constraint propagation on which values can go in each cell
- Using the nesting constraint to restrict shape search (only try shapes that extend the previous shape by one cell)

---

## 4. Summary of Issues

### Critical Bugs

| # | Solver | Issue | Impact |
|---|--------|-------|--------|
| 1 | openai | USABLE_CELLS only has 37 labeled cells, not all grid cells | Wrong N, wrong/no solution |
| 2 | anthropic | Grid backtracking has O(18^132) search space, no meaningful pruning | Will never terminate |
| 3 | Both | Grid size ambiguity (13x13 vs 13x11) in constraint docs | May affect max N |

### Moderate Bugs

| # | Solver | Issue | Impact |
|---|--------|-------|--------|
| 4 | anthropic | Adjacency check code (lines 344-354) is confusing with dead logic | Correctness OK but hard to maintain |
| 5 | openai | Duplicate polyomino enumeration (seeds from every cell) | Exponential slowdown |
| 6 | openai | `_grow_with_forced` has duplicate pruning line (`len(cur) + len(fr) < size` appears twice) | Minor, no functional impact |

### Correctness Verified

| Component | Solver | Status |
|-----------|--------|--------|
| Expression lambdas vs grid.json | anthropic | All 37 match |
| safe_eval error handling | anthropic | Correct |
| is_positive_integer | anthropic | Correct |
| All 8 dihedral transformations | both | Correct |
| Connectivity (BFS) | both | Correct |
| Containment semantics | both | Equivalent given count constraint |
| Answer computation | anthropic | Correct |
| Backtracking order (N down to 1) | openai | Good design choice |
| Shape canonicalization | openai | Correct |

### Recommendations

1. **Fix USABLE_CELLS in solver_openai.py** to include ALL grid cells (most critical fix).
2. **Verify grid dimensions** from the puzzle image (13x13 vs 13x11).
3. **Redesign the grid-filling strategy** -- neither solver's Phase 2 approach will scale. Recommended approach:
   - Use the nesting constraint constructively: start with the 1-omino (1 cell), extend to 2-omino (add 1 adjacent cell), extend to 3-omino (add 1 adjacent cell), etc.
   - This is the "incremental growth" approach: each K-omino is the (K-1)-omino plus one adjacent cell.
   - This drastically reduces the search space since at each level you only choose which ONE cell to add.
   - Fixed cell values constrain which cells MUST be in specific regions.
4. **Merge Phase 1 (variable search) from solver_anthropic into solver_openai** or create a unified solver.
5. **Consider parallel exploration** of (a, b, c) candidates if Phase 1 is slow.

---

## 5. Key Insight for Improved Solver Design

Given the equivalence proven in Section 3.3, the K-omino is always the (K-1)-omino plus exactly one adjacent cell. This means the entire solution is determined by:

1. Choosing the position of the 1-omino (1 cell).
2. For K = 2, 3, ..., N: choosing which one adjacent cell to add to the (K-1)-omino to form the K-omino.

The newly added cell gets value K. The total search is:

- Step 1: Choose 1 cell from ~169 options.
- Step K: Choose 1 cell from the perimeter of the current polyomino (typically 2K + O(1) cells).

This gives a search tree of roughly 169 * 4 * 6 * 8 * ... * (2N+2) -- still large but with aggressive pruning from fixed cell constraints, vastly more tractable than the current approaches.

**Critical constraint:** Each cell added at step K must ensure that value K doesn't conflict with fixed cell assignments. Specifically:
- If a fixed cell has value K, then that cell MUST be the one added at step K (or already part of the polyomino with value K -- but wait, each value K appears exactly K times, and only one cell is added at step K to make the K-omino from the (K-1)-omino... this means cell values aren't all K for the K-omino!)

**Wait -- important clarification:** The K-omino has K cells, ALL of which contain value K. So when growing from (K-1)-omino to K-omino, the new cell gets value K, and the K-1 cells that previously had value K-1 now... no, they keep their values. Each cell has exactly ONE value. The K-omino is the set of cells with value K. The (K-1)-omino is the set of cells with value K-1. These are DISJOINT sets.

So the containment means the SHAPE of the (K-1)-omino fits inside the SHAPE of the K-omino, not that they share cells. This is pure shape containment in the normalized shape space.

This makes the problem significantly harder than incremental growth, because the K-omino and (K-1)-omino occupy DIFFERENT cells on the grid. The shapes just need to be related.

**Revised approach:** solver_openai's backtracking from N down to 1 with shape-space nesting is actually the right structure. The key optimization is to precompute valid shapes at each level and use the shape constraint to prune.
