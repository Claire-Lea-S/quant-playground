"""
Jane Street Puzzle - February 2026: Subtiles 2
Solver script

Phase 1: Find valid (a, b, c) such that all labeled cell expressions
         evaluate to positive integers in [1, N].
Phase 2: Fill the grid satisfying count, connectivity, and containment.
Phase 3: Compute answer = max(row_sums) * min(row_sums).
"""

import math
import itertools
from collections import deque
from typing import Dict, List, Tuple, Set, Optional
from copy import deepcopy

# ============================================================
# GRID CONFIGURATION
# ============================================================
ROWS = 13
COLS = 13
TOTAL_CELLS = ROWS * COLS  # 169

# Max possible N: N(N+1)/2 <= 169 => N <= 17
MAX_N = 17


# ============================================================
# EXPRESSION DEFINITIONS
# Each labeled cell maps to a function (a, b, c) -> float
# Returns None if undefined (division by zero, log of <=0, etc.)
# ============================================================
def safe_eval(func, a, b, c):
    """Safely evaluate an expression, returning None on error."""
    try:
        val = func(a, b, c)
        if val is None:
            return None
        if isinstance(val, complex):
            return None
        if math.isnan(val) or math.isinf(val):
            return None
        return val
    except (ZeroDivisionError, ValueError, OverflowError, TypeError):
        return None


LABELED_CELLS = {
    (0, 1):  ("6c - 4b",              lambda a, b, c: 6*c - 4*b),
    (1, 5):  ("8 - b",                lambda a, b, c: 8 - b),
    (2, 0):  ("(a^b - 4)/(6c + 1)",   lambda a, b, c: (a**b - 4) / (6*c + 1)),
    (2, 2):  ("(b + c)/(c - 1)",      lambda a, b, c: (b + c) / (c - 1)),
    (2, 4):  ("b^2 - b/c",            lambda a, b, c: b**2 - b / c),
    (2, 5):  ("sqrt(30 + a)/c",       lambda a, b, c: math.sqrt(30 + a) / c),
    (2, 7):  ("(a + b)/(c - 3a)",     lambda a, b, c: (a + b) / (c - 3*a)),
    (3, 2):  ("(b - 3a)/(a - c)",     lambda a, b, c: (b - 3*a) / (a - c)),
    (3, 4):  ("8a - 2b",              lambda a, b, c: 8*a - 2*b),
    (3, 6):  ("b/(a - c)",            lambda a, b, c: b / (a - c)),
    (3, 8):  ("(b + 9)/sqrt(c - a)",  lambda a, b, c: (b + 9) / math.sqrt(c - a)),
    (4, 0):  ("18/(ac + 1)",          lambda a, b, c: 18 / (a*c + 1)),
    (4, 3):  ("c^b",                  lambda a, b, c: c**b),
    (4, 7):  ("(3 + b^2)/sqrt(3+2c)", lambda a, b, c: (3 + b**2) / math.sqrt(3 + 2*c)),
    (5, 2):  ("b/(a^2 - c^2)",        lambda a, b, c: b / (a**2 - c**2)),
    (5, 10): ("sqrt(a + 2)/a",        lambda a, b, c: math.sqrt(a + 2) / a),
    (6, 1):  ("a^b - 12/a",           lambda a, b, c: a**b - 12 / a),
    (6, 2):  ("2c + c/a",             lambda a, b, c: 2*c + c / a),
    (6, 4):  ("4a - 5b",              lambda a, b, c: 4*a - 5*b),
    (6, 6):  ("c + 2a",               lambda a, b, c: c + 2*a),
    (6, 8):  ("b/(9a - 5c)",          lambda a, b, c: b / (9*a - 5*c)),
    (7, 0):  ("(b^3+2c)/(b+2c)",      lambda a, b, c: (b**3 + 2*c) / (b + 2*c)),
    (7, 7):  ("b/(a - 1)",            lambda a, b, c: b / (a - 1)),
    (8, 1):  ("(c - b)/(2a)",         lambda a, b, c: (c - b) / (2*a)),
    (8, 5):  ("b/(a - c)",            lambda a, b, c: b / (a - c)),
    (8, 10): ("(b + c)/(a - c)",      lambda a, b, c: (b + c) / (a - c)),
    (9, 0):  ("log_c(a)",             lambda a, b, c: math.log(a) / math.log(c)),
    (9, 2):  ("(c^2 - b)/a",          lambda a, b, c: (c**2 - b) / a),
    (9, 4):  ("(b - 1)^2",            lambda a, b, c: (b - 1)**2),
    (9, 6):  ("cbrt(43 - ac)/a",      lambda a, b, c: (abs(43 - a*c)**(1/3) * (1 if 43 - a*c >= 0 else -1)) / a if 43 - a*c != 0 else 0.0),
    (10, 1): ("(b - a)/(a - c)",      lambda a, b, c: (b - a) / (a - c)),
    (10, 3): ("11 - b",               lambda a, b, c: 11 - b),
    (10, 4): ("(b - 2a)/(a - c)",     lambda a, b, c: (b - 2*a) / (a - c)),
    (10, 7): ("(c + 3)/a",            lambda a, b, c: (c + 3) / a),
    (10, 9): ("8c - b/c",             lambda a, b, c: 8*c - b / c),
    (11, 3): ("b^2",                  lambda a, b, c: b**2),
    (12, 6): ("(2^b + 1)/(ac)",       lambda a, b, c: (2**b + 1) / (a*c)),
}


# ============================================================
# PHASE 1: VARIABLE DISCOVERY
# ============================================================
def is_positive_integer(x: Optional[float], tol: float = 1e-9) -> bool:
    """Check if x is a positive integer (within tolerance)."""
    if x is None:
        return False
    if not isinstance(x, (int, float)):
        return False
    if math.isnan(x) or math.isinf(x):
        return False
    return x > tol and abs(x - round(x)) < tol


def evaluate_all(a: int, b: int, c: int, max_val: int = MAX_N) -> Optional[Dict]:
    """
    Evaluate all expressions for given (a, b, c).
    Returns dict of {(r,c): int_value} if ALL are positive integers <= max_val.
    Returns None otherwise.
    """
    values = {}
    for pos, (name, func) in LABELED_CELLS.items():
        v = safe_eval(func, a, b, c)
        if not is_positive_integer(v) or round(v) > max_val:
            return None
        values[pos] = int(round(v))
    return values


def find_variables(a_range=range(1, 30), b_range=range(1, 20), c_range=range(2, 20)):
    """
    Brute-force search for (a, b, c) that make all expressions valid.
    Returns list of (a, b, c, N, cell_values) tuples.
    """
    results = []
    for a in a_range:
        for b in b_range:
            for c in c_range:
                if a == c:
                    # a - c = 0 causes many divisions by zero, skip
                    # (unless we handle it, but most expressions need a != c)
                    continue
                for N in range(1, MAX_N + 1):
                    values = evaluate_all(a, b, c, max_val=N)
                    if values is None:
                        continue
                    # Check: max expression value determines minimum N
                    max_v = max(values.values())
                    if max_v != N:
                        continue
                    # Check total fill fits in grid
                    total_fill = N * (N + 1) // 2
                    if total_fill > TOTAL_CELLS:
                        continue
                    # Check count feasibility: for each value k,
                    # number of labeled cells with value k must be <= k
                    from collections import Counter
                    counts = Counter(values.values())
                    feasible = True
                    for k, cnt in counts.items():
                        if cnt > k:
                            feasible = False
                            break
                    if feasible:
                        results.append((a, b, c, N, values))
    return results


def diagnose_variables(a: int, b: int, c: int, max_val: int = MAX_N):
    """
    Print diagnostic: which expressions pass/fail for given (a, b, c).
    """
    print(f"\n--- Diagnosing a={a}, b={b}, c={c} (max_val={max_val}) ---")
    passed = 0
    failed = 0
    for pos, (name, func) in sorted(LABELED_CELLS.items()):
        v = safe_eval(func, a, b, c)
        if is_positive_integer(v) and round(v) <= max_val:
            print(f"  {pos} {name:30s} = {v:10.4f} -> {int(round(v)):3d}  OK")
            passed += 1
        else:
            v_str = f"{v:.4f}" if v is not None else "UNDEFINED"
            print(f"  {pos} {name:30s} = {v_str:>10s}       FAIL")
            failed += 1
    print(f"  Passed: {passed}/{passed+failed}")


# ============================================================
# PHASE 2: GRID FILLING (backtracking with constraint propagation)
# ============================================================
class GridSolver:
    """Solve the grid placement problem given fixed cell values."""

    def __init__(self, rows: int, cols: int, N: int,
                 fixed_cells: Dict[Tuple[int, int], int]):
        self.rows = rows
        self.cols = cols
        self.N = N
        self.fixed = fixed_cells
        self.total_fill = N * (N + 1) // 2

        # grid[r][c] = 0 (empty) or 1..N
        self.grid = [[0] * cols for _ in range(rows)]
        for (r, c), v in fixed_cells.items():
            self.grid[r][c] = v

        # Track how many cells are placed for each value
        from collections import Counter
        fixed_counts = Counter(fixed_cells.values())
        self.placed = {k: fixed_counts.get(k, 0) for k in range(1, N + 1)}

    def neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Return orthogonal neighbors of (r, c)."""
        result = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                result.append((nr, nc))
        return result

    def is_connected(self, value: int) -> bool:
        """Check if all cells with given value form a connected region."""
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

    def get_shape(self, value: int) -> Set[Tuple[int, int]]:
        """Get normalized shape (translated to origin) for a value."""
        cells = [(r, c) for r in range(self.rows) for c in range(self.cols)
                 if self.grid[r][c] == value]
        if not cells:
            return set()
        min_r = min(r for r, c in cells)
        min_c = min(c for r, c in cells)
        return frozenset((r - min_r, c - min_c) for r, c in cells)

    @staticmethod
    def all_orientations(shape: Set[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
        """Generate all 8 rotations/reflections of a shape, normalized."""
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
        orientations = []
        seen = set()
        for t in transforms:
            transformed = {t(r, c) for r, c in shape}
            min_r = min(r for r, c in transformed)
            min_c = min(c for r, c in transformed)
            normalized = frozenset((r - min_r, c - min_c) for r, c in transformed)
            if normalized not in seen:
                seen.add(normalized)
                orientations.append(normalized)
        return orientations

    @staticmethod
    def shape_contains(big: Set[Tuple[int, int]],
                       small: Set[Tuple[int, int]]) -> bool:
        """
        Check if big polyomino contains small polyomino
        (some rotation/reflection of small fits inside big).
        """
        if not small:
            return True
        big_set = set(big)
        for oriented_small in GridSolver.all_orientations(small):
            # Try all translations
            for dr in range(-20, 21):
                for dc in range(-20, 21):
                    translated = {(r + dr, c + dc) for r, c in oriented_small}
                    if translated.issubset(big_set):
                        return True
        return False

    def check_all_containment(self) -> bool:
        """Check containment constraint for all K > 1."""
        shapes = {}
        for k in range(1, self.N + 1):
            shapes[k] = self.get_shape(k)
        for k in range(2, self.N + 1):
            if not self.shape_contains(shapes[k], shapes[k - 1]):
                return False
        return True

    def check_all_connectivity(self) -> bool:
        """Check connectivity for all values."""
        for k in range(1, self.N + 1):
            if not self.is_connected(k):
                return False
        return True

    def solve(self) -> Optional[List[List[int]]]:
        """
        Solve the grid using backtracking.
        Returns the filled grid or None.
        """
        # Find empty cells that need to be filled
        empty_cells = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.fixed:
                    empty_cells.append((r, c))

        return self._backtrack(empty_cells, 0)

    def _backtrack(self, cells: List[Tuple[int, int]], idx: int) -> Optional[List[List[int]]]:
        """Recursive backtracking solver."""
        if idx == len(cells):
            # All cells assigned, check final constraints
            total_placed = sum(self.placed.values())
            if total_placed != self.total_fill:
                return None
            if not self.check_all_connectivity():
                return None
            if not self.check_all_containment():
                return None
            return [row[:] for row in self.grid]

        r, c = cells[idx]

        # Try value 0 (empty)
        remaining_cells = len(cells) - idx - 1
        remaining_needed = self.total_fill - sum(self.placed.values())
        if remaining_needed <= remaining_cells:
            # Can afford to leave this cell empty
            self.grid[r][c] = 0
            result = self._backtrack(cells, idx + 1)
            if result:
                return result

        # Try values 1..N
        for k in range(1, self.N + 1):
            if self.placed[k] >= k:
                continue  # Already have enough of this value

            # Check adjacency: k must be connectable
            # (either first cell of this value, or adjacent to existing k-cell)
            existing_k = [(er, ec) for er in range(self.rows) for ec in range(self.cols)
                          if self.grid[er][ec] == k]
            if existing_k:
                # Must be adjacent to at least one existing k-cell
                if not any((nr, nc) == (r, c) or
                           (abs(nr - r) + abs(nc - c) == 1 and self.grid[nr][nc] == k)
                           for nr, nc in existing_k):
                    adjacent = any(abs(er - r) + abs(ec - c) == 1
                                   for er, ec in existing_k)
                    if not adjacent:
                        continue

            self.grid[r][c] = k
            self.placed[k] += 1

            result = self._backtrack(cells, idx + 1)
            if result:
                return result

            self.grid[r][c] = 0
            self.placed[k] -= 1

        return None


# ============================================================
# PHASE 3: ANSWER COMPUTATION
# ============================================================
def compute_answer(grid: List[List[int]],
                   labeled_positions: Set[Tuple[int, int]]) -> Tuple[int, int, int]:
    """
    Compute row sums (of labeled cells only) and return
    (min_row_sum, max_row_sum, answer).
    """
    row_sums = []
    for r in range(len(grid)):
        s = sum(grid[r][c] for c in range(len(grid[0]))
                if (r, c) in labeled_positions)
        row_sums.append(s)

    # Only consider rows that have labeled cells
    nonzero_sums = [s for s in row_sums if s > 0]
    if not nonzero_sums:
        return 0, 0, 0

    min_s = min(nonzero_sums)
    max_s = max(nonzero_sums)
    return min_s, max_s, min_s * max_s


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("Jane Street Puzzle - February 2026: Subtiles 2")
    print("=" * 60)
    print(f"\nGrid: {ROWS}x{COLS} = {TOTAL_CELLS} cells")
    print(f"Max N: {MAX_N} (N(N+1)/2 = {MAX_N*(MAX_N+1)//2} <= {TOTAL_CELLS})")
    print(f"Labeled cells: {len(LABELED_CELLS)}")

    # ----------------------------------------------------------
    # Phase 1: Find valid variable assignments
    # ----------------------------------------------------------
    print("\n" + "=" * 60)
    print("PHASE 1: Searching for valid (a, b, c)...")
    print("=" * 60)

    results = find_variables(
        a_range=range(1, 30),
        b_range=range(1, 20),
        c_range=range(2, 20),
    )

    if results:
        print(f"\nFound {len(results)} valid assignment(s):")
        for a, b, c, N, values in results:
            print(f"\n  a={a}, b={b}, c={c}, N={N}")
            print(f"  Total fill: {N*(N+1)//2} cells")
            print(f"  Cell values: {dict(sorted(values.items()))}")
    else:
        print("\nNo valid (a, b, c) found with current expressions.")
        print("Running diagnostics on likely candidates...\n")

        # Try some promising candidates and show what fails
        best_score = 0
        candidates = []
        for a in range(1, 25):
            for b in range(1, 12):
                for c in range(2, 20):
                    score = 0
                    for pos, (name, func) in LABELED_CELLS.items():
                        v = safe_eval(func, a, b, c)
                        if is_positive_integer(v) and round(v) <= MAX_N:
                            score += 1
                    if score > best_score - 3:
                        candidates.append((score, a, b, c))
                        if score > best_score:
                            best_score = score

        candidates = [(s, a, b, c) for s, a, b, c in candidates if s >= best_score - 2]
        candidates.sort(reverse=True)
        print(f"Best candidates (top 10, best score = {best_score}/{len(LABELED_CELLS)}):")
        for score, a, b, c in candidates[:10]:
            print(f"  a={a}, b={b}, c={c}: {score}/{len(LABELED_CELLS)} expressions valid")
        for score, a, b, c in candidates[:3]:
            diagnose_variables(a, b, c)

        print("\n" + "-" * 60)
        print("HINT: Some expressions may be misread from the image.")
        print("Check the expressions that FAIL above and compare with")
        print("the original puzzle image.")
        return

    # ----------------------------------------------------------
    # Phase 2: Fill the grid (for each valid assignment)
    # ----------------------------------------------------------
    for a, b, c, N, values in results:
        print(f"\n{'=' * 60}")
        print(f"PHASE 2: Filling grid for a={a}, b={b}, c={c}, N={N}")
        print("=" * 60)

        solver = GridSolver(ROWS, COLS, N, values)
        solution = solver.solve()

        if solution is None:
            print("  No valid grid filling found.")
            continue

        # Print solution
        print("\nSolution grid:")
        for r in range(ROWS):
            row_str = ""
            for cc in range(COLS):
                v = solution[r][cc]
                if v == 0:
                    row_str += "  . "
                else:
                    marker = "*" if (r, cc) in values else " "
                    row_str += f"{v:3d}{marker}"
            print(f"  Row {r:2d}: {row_str}")

        # Phase 3: Compute answer
        min_s, max_s, answer = compute_answer(solution, set(values.keys()))
        print(f"\nRow sums (labeled cells only):")
        for r in range(ROWS):
            labeled_in_row = [(r, cc) for cc in range(COLS) if (r, cc) in values]
            if labeled_in_row:
                s = sum(solution[r][cc] for _, cc in labeled_in_row)
                cells_str = " + ".join(f"{solution[r][cc]}" for _, cc in labeled_in_row)
                print(f"  Row {r:2d}: {cells_str} = {s}")

        print(f"\n  Min row sum: {min_s}")
        print(f"  Max row sum: {max_s}")
        print(f"\n  >>> ANSWER = {min_s} * {max_s} = {answer} <<<")


if __name__ == "__main__":
    main()
