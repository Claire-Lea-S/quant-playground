# solver.py
# Solves the "nested K-omino" placement puzzle on a given set of usable cells
# (a subset of grid coordinates). Each k appears exactly k times (for k=1..N),
# each k-cells form an orthogonally connected polyomino, and for k>1 the k-omino
# must contain the (k-1)-omino shape up to rotation/reflection (free polyominoes).
#
# The script uses backtracking:
# - choose N (or take fixed N)
# - assign a connected region of size k for each k from N down to 1
# - enforce fixed clues (optional): cell -> fixed number
# - enforce nesting in SHAPE space (not spatial nesting): shape(k-1) must be
#   congruent to shape(k) with one cell removed (leaving a connected (k-1)-shape)
#
# Coordinates are (r, c). Adjacency is 4-neighbour.

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, List, Optional, Set, Tuple

Coord = Tuple[int, int]


# ----------------------------
# 1) Input: usable cells + optional fixed labels
# ----------------------------

# Replace this with the usable cells from your first grid (the cells that may contain numbers)
USABLE_CELLS: List[Coord] = [
    (0, 4),
    (1, 6),
    (2, 1), (2, 3), (2, 5), (2, 7), (2, 9),
    (3, 4), (3, 6), (3, 8), (3, 10),
    (4, 1), (4, 5), (4, 9),
    (5, 3), (5, 10),
    (6, 2), (6, 4), (6, 6), (6, 8), (6, 10),
    (7, 0), (7, 8),
    (8, 2), (8, 6), (8, 10),
    (9, 2), (9, 4), (9, 6), (9, 8),
    (10, 3), (10, 5), (10, 7), (10, 9), (10, 11),
    (11, 5),
    (12, 8),
]

# Optional fixed clues: { (r,c): value }  (leave empty if none are fixed yet)
FIXED: Dict[Coord, int] = {
    # example:
    # (0, 4): 7
}

# If you already know N, set it here; else set to None to auto-pick the largest feasible N
FORCE_N: Optional[int] = None


# ----------------------------
# 2) Geometry helpers
# ----------------------------

def neighbors4(p: Coord) -> List[Coord]:
    r, c = p
    return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]


def is_connected(cells: Set[Coord]) -> bool:
    if not cells:
        return False
    stack = [next(iter(cells))]
    seen = set()
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        for y in neighbors4(x):
            if y in cells and y not in seen:
                stack.append(y)
    return len(seen) == len(cells)


# ----------------------------
# 3) Shape canonicalization (free polyomino: rotations + reflections)
# ----------------------------

def normalize_shape(points: Iterable[Coord]) -> Tuple[Coord, ...]:
    pts = list(points)
    min_r = min(r for r, _ in pts)
    min_c = min(c for _, c in pts)
    shifted = sorted((r - min_r, c - min_c) for r, c in pts)
    return tuple(shifted)


def transforms(points: Iterable[Coord]) -> List[List[Coord]]:
    # 8 symmetries of the square: rotations + reflections
    pts = list(points)

    def rot90(p: Coord) -> Coord:
        r, c = p
        return (c, -r)

    def reflect(p: Coord) -> Coord:
        r, c = p
        return (r, -c)

    out = []
    current = pts
    for _ in range(4):
        out.append(current)
        out.append([reflect(p) for p in current])
        current = [rot90(p) for p in current]
    return out


def canonical_shape(points: Iterable[Coord]) -> Tuple[Coord, ...]:
    # Represent shape relative to its own origin, modulo rotations/reflections
    best = None
    pts = list(points)
    for tpts in transforms(pts):
        norm = normalize_shape(tpts)
        if best is None or norm < best:
            best = norm
    assert best is not None
    return best


# ----------------------------
# 4) Nesting condition in shape-space
# ----------------------------

def shape_contains_prev(shape_k: Tuple[Coord, ...], shape_km1: Tuple[Coord, ...]) -> bool:
    """
    Returns True if shape_k contains shape_km1 up to congruence, i.e.
    by removing exactly one cell from shape_k you can obtain a connected shape
    congruent to shape_km1
    """
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


# ----------------------------
# 5) Enumerate connected subsets of given size among remaining usable cells
# ----------------------------

def connected_subsets_of_size(
    remaining: Set[Coord],
    size: int,
    must_include: Set[Coord],
) -> Iterable[Set[Coord]]:
    """
    Generate connected subsets of 'remaining' of given 'size' that include all 'must_include'
    """
    if size < len(must_include):
        return
    if not must_include:
        # choose any seed
        for seed in remaining:
            yield from _grow_connected_from_seed(remaining, size, {seed})
        return

    # Start from the forced cells; if they are not connected, we still can connect them
    # by adding intermediate cells, but only if such cells exist in remaining.
    # Use a frontier growth that keeps a connected "core" and gradually absorbs forced cells.
    # Implementation: start from one forced cell seed, and require all forced cells to be included by the end.
    seed = next(iter(must_include))
    initial = {seed}
    yield from _grow_with_forced(remaining, size, initial, must_include)


def _frontier(cells: Set[Coord], remaining: Set[Coord]) -> Set[Coord]:
    f = set()
    for p in cells:
        for q in neighbors4(p):
            if q in remaining and q not in cells:
                f.add(q)
    return f


def _grow_connected_from_seed(remaining: Set[Coord], size: int, seed_set: Set[Coord]) -> Iterable[Set[Coord]]:
    # Simple connected growth
    stack: List[Tuple[Set[Coord], Set[Coord]]] = []
    stack.append((set(seed_set), _frontier(seed_set, remaining)))

    while stack:
        cells, fr = stack.pop()
        if len(cells) == size:
            if is_connected(cells):
                yield cells
            continue
        # prune: not enough remaining frontier + existing cells to reach size
        if len(cells) + len(fr) < size:
            continue
        # expand by choosing next cell from frontier
        fr_list = list(fr)
        for i, nxt in enumerate(fr_list):
            new_cells = set(cells)
            new_cells.add(nxt)
            new_fr = set(fr)
            new_fr.remove(nxt)
            # add new frontier from nxt
            for q in neighbors4(nxt):
                if q in remaining and q not in new_cells:
                    new_fr.add(q)
            stack.append((new_cells, new_fr))


def _grow_with_forced(
    remaining: Set[Coord],
    size: int,
    cells: Set[Coord],
    forced: Set[Coord],
) -> Iterable[Set[Coord]]:
    # Grow connected set from 'cells' while ensuring 'forced' ⊆ final set
    stack: List[Tuple[Set[Coord], Set[Coord]]] = []
    stack.append((set(cells), _frontier(cells, remaining)))

    while stack:
        cur, fr = stack.pop()
        if len(cur) == size:
            if forced.issubset(cur) and is_connected(cur):
                yield cur
            continue

        # prune: if missing forced cells cannot fit
        missing = forced - cur
        if len(cur) + len(fr) < size:
            continue
        if len(cur) + len(fr) < size:
            continue
        if len(cur) + len(fr) < len(cur) + len(missing):
            continue

        # expand
        fr_list = list(fr)

        # heuristic: prefer adding forced-adjacent candidates
        fr_list.sort(key=lambda p: 0 if p in forced else 1)

        for nxt in fr_list:
            new_cur = set(cur)
            new_cur.add(nxt)
            new_fr = set(fr)
            new_fr.remove(nxt)
            for q in neighbors4(nxt):
                if q in remaining and q not in new_cur:
                    new_fr.add(q)
            stack.append((new_cur, new_fr))


# ----------------------------
# 6) Main backtracking solver
# ----------------------------

@dataclass(frozen=True)
class Placement:
    k: int
    cells: FrozenSet[Coord]
    shape: Tuple[Coord, ...]


def choose_max_feasible_n(num_cells: int, fixed: Dict[Coord, int]) -> int:
    max_fixed = max(fixed.values(), default=0)
    # Largest N with 1+2+...+N <= num_cells and N >= max_fixed
    n = 0
    total = 0
    while True:
        if total + (n + 1) > num_cells:
            break
        n += 1
        total += n
    if n < max_fixed:
        raise ValueError(f"Infeasible: max fixed value {max_fixed} exceeds max possible N {n}")
    return n


def solve() -> Optional[Dict[Coord, int]]:
    usable = set(USABLE_CELLS)

    # Validate fixed cells are within usable set
    for p in FIXED:
        if p not in usable:
            raise ValueError(f"Fixed cell {p} not in usable set")

    if FORCE_N is None:
        N = choose_max_feasible_n(len(usable), FIXED)
    else:
        N = FORCE_N
        if N * (N + 1) // 2 > len(usable):
            raise ValueError("FORCE_N too large for number of usable cells")
        if max(FIXED.values(), default=0) > N:
            raise ValueError("FORCE_N smaller than some fixed clue value")

    # Precompute forced cells per k
    forced_by_k: Dict[int, Set[Coord]] = {k: set() for k in range(1, N + 1)}
    for p, v in FIXED.items():
        if 1 <= v <= N:
            forced_by_k[v].add(p)
        else:
            raise ValueError(f"Fixed value {v} at {p} is outside 1..N")

    # Backtracking from k=N down to 1
    assignments: Dict[Coord, int] = {p: 0 for p in usable}
    used: Set[Coord] = set()
    placements: Dict[int, Placement] = {}

    def backtrack(k: int) -> bool:
        if k == 0:
            return True

        remaining = usable - used

        # must include fixed cells for this k
        must = forced_by_k[k]
        if not must.issubset(remaining):
            return False

        # generate candidate connected regions of size k
        # heuristic: sort candidates by shape rarity (approx) by deduplicating shapes early
        shape_to_regions: Dict[Tuple[Coord, ...], List[Set[Coord]]] = {}

        for region in connected_subsets_of_size(remaining, k, must):
            # enforce that region does not include cells fixed to other values
            ok = True
            for p in region:
                if p in FIXED and FIXED[p] != k:
                    ok = False
                    break
            if not ok:
                continue

            shp = canonical_shape(region)
            shape_to_regions.setdefault(shp, []).append(region)

        # If we already placed k+1, enforce nesting in shape space:
        # shape(k) must be obtainable by removing one cell from shape(k+1)
        if k < N:
            next_shape = placements[k + 1].shape
            valid_shapes = []
            for shp in shape_to_regions.keys():
                if shape_contains_prev(next_shape, shp):
                    valid_shapes.append(shp)
            shapes_iter = valid_shapes
        else:
            shapes_iter = list(shape_to_regions.keys())

        # Heuristic: fewer placements first
        shapes_iter.sort(key=lambda s: len(shape_to_regions[s]))

        for shp in shapes_iter:
            for region in shape_to_regions[shp]:
                # commit
                for p in region:
                    assignments[p] = k
                used.update(region)
                placements[k] = Placement(k=k, cells=frozenset(region), shape=shp)

                if backtrack(k - 1):
                    return True

                # undo
                used.difference_update(region)
                del placements[k]
                for p in region:
                    assignments[p] = 0

        return False

    ok = backtrack(N)
    if not ok:
        return None

    # Remove unused (0) cells from output if desired; keep full map for clarity
    return assignments


def print_solution(assignments: Dict[Coord, int]) -> None:
    usable = set(USABLE_CELLS)
    rows = [r for r, _ in usable]
    cols = [c for _, c in usable]
    rmin, rmax = min(rows), max(rows)
    cmin, cmax = min(cols), max(cols)

    # print a compact grid view (only bounding box)
    for r in range(rmin, rmax + 1):
        row_cells = []
        for c in range(cmin, cmax + 1):
            p = (r, c)
            if p in usable:
                v = assignments[p]
                row_cells.append(f"{v:2d}" if v != 0 else " .")
            else:
                row_cells.append("  ")
        print(" ".join(row_cells))


if __name__ == "__main__":
    sol = solve()
    if sol is None:
        print("No solution found")
    else:
        print_solution(sol)
