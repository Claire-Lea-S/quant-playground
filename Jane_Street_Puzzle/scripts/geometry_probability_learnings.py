"""
Geometry and Probability Puzzle Learnings
==========================================
A playbook for solving Jane Street geometry and probability puzzles.

This file contains:
1. Dictionary of puzzle attempts with reasoning
2. Dictionary of key techniques that worked
3. Dictionary of mistakes/misconceptions
4. Helper functions encoding solving patterns

Based on practice with 5 puzzles:
- Beside the Point (Nov 2024) - Geometry
- Arc-edge Acreage (Apr 2023) - Geometry
- Circle Time (Jun 2020) - Geometry
- Sum One, Somewhere (Apr 2025) - Probability
- Bracketology 101 (Apr 2021) - Probability
"""

import math
import random
from typing import Tuple, List, Callable, Dict, Any, Optional
from fractions import Fraction

# Optional numpy import for Monte Carlo functions
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


# =============================================================================
# PUZZLE ATTEMPTS WITH REASONING
# =============================================================================

PUZZLE_ATTEMPTS = {
    "beside_the_point": {
        "date": "2024-11",
        "category": "geometry",
        "problem_summary": """
            Two random points (red R, blue B) uniformly distributed in unit square.
            Find probability that perpendicular bisector of RB intersects the side
            of the square closest to B.
        """,
        "my_approach": """
            1. Set up coordinates with square [0,1] x [0,1]
            2. By symmetry, assume B closest to bottom edge (y=0)
            3. The perpendicular bisector is the locus of equidistant points
            4. Derived formula for x-coordinate of intersection:
               px = (bx^2 + by^2 - rx^2 - ry^2) / (2*(bx - rx))
            5. Need px in [0,1] for solution to exist
            6. Recognized this requires 4D integration with constraints
        """,
        "official_approach": """
            1. Used symmetry to restrict to triangular octant
            2. Identified valid region as SYMMETRIC DIFFERENCE of two circles
               centered at bottom vertices passing through first point
            3. Computed area through integration
        """,
        "answer": "(1 + 2*pi - ln(4))/12 = 0.4914075788",
        "what_i_learned": """
            - The symmetric difference of two circles is a powerful geometric construct
            - When answer has pi and ln terms, expect circle-based geometry
            - Restricting to an octant by symmetry simplifies integration significantly
        """
    },

    "arc_edge_acreage": {
        "date": "2023-04",
        "category": "geometry",
        "problem_summary": """
            On 7x7 grid, draw simple closed curves using quarter-circle arcs.
            Count curves enclosing exactly area 32.
        """,
        "my_approach": """
            1. Recognized quarter circles add/subtract pi/4 to area
            2. For integer area (32), need balanced inward/outward curves
            3. Grid has 36 cells (6x6), so need to exclude 4 cells worth
            4. This is combinatorial counting
        """,
        "official_approach": """
            1. Base case: 18 squares giving area 36
            2. For area 32: omit 2 boxes, giving different perimeter lengths
            3. For each perimeter length, count ways to assign inward/outward curves
            4. Used binomial coefficients: C(n, n/2) for balanced assignments
            5. Four cases by perimeter: 18, 20, 22, 24 segments
        """,
        "answer": "89,519,144",
        "what_i_learned": """
            - For integer area with curved edges, curves MUST balance (same in/out)
            - Decompose into: (which cells excluded) x (curve assignment)
            - Perimeter length determines number of curve choices
            - Final answer = sum over configurations of (count) * C(perimeter, perimeter/2)
        """
    },

    "circle_time": {
        "date": "2020-06",
        "category": "geometry",
        "problem_summary": """
            A 'ring' is 6 equal circles (radius r) with centers on hexagon of side 2r.
            Maximize proportion of large circle C covered by concentric, disjoint rings.
        """,
        "my_approach": """
            1. Each ring occupies annulus from radius r to 3r from center
            2. Assumed simple 1/3 scaling for nested rings
            3. Computed geometric series: sum of 6*pi*r^2 * (1/9)^k
            4. Got 3/4 = 0.75 coverage
        """,
        "official_approach": """
            1. First ring has circles of radius 1/3 (for unit circle C)
            2. CRITICAL: Rotate second ring by 30 degrees
            3. This allows larger second ring than simple nesting
            4. Derived constraint equation for optimal second ring radius
            5. Resulting coverage: 6/(9 - (1 + 2*sqrt(3) - 2*sqrt(1+sqrt(3)))^2)
        """,
        "answer": "0.783464",
        "what_i_learned": """
            - ROTATION can optimize packing beyond simple scaling
            - Don't assume simplest nesting is optimal
            - When circles can be rotated, check if rotation improves fit
            - Answer 0.78 > 0.75 shows 4% improvement from rotation insight
        """
    },

    "sum_one_somewhere": {
        "date": "2025-04",
        "category": "probability",
        "problem_summary": """
            Infinite binary tree, each node labeled 0 (prob p) or 1 (prob 1-p).
            Find p where P(exists infinite path with sum <= 1) = 1/2.
        """,
        "my_approach": """
            1. Defined f(p) = P(exists all-0 path), g(p) = P(exists sum<=1 path)
            2. For f: f = p * (2f - f^2), giving f = (2p-1)/p for p >= 1/2
            3. For g: g = p*(2g - g^2) + (1-p)*(2f - f^2)
            4. Substituted g = 1/2 and derived cubic: 3p^3 - 10p^2 + 12p - 4 = 0
        """,
        "official_approach": """
            Same approach! The solution confirmed:
            1. Recursive decomposition: tree = root + two subtrees
            2. Same recurrence relations
            3. Same cubic equation
        """,
        "answer": "0.5306035754",
        "what_i_learned": """
            - Binary tree problems naturally yield recursive equations
            - P(at least one child succeeds) = 1 - (1-p)^2 = 2p - p^2
            - When answer is irrational, expect polynomial equation
            - Cubic equations common in branching probability problems
        """
    },

    "bracketology_101": {
        "date": "2021-04",
        "category": "probability",
        "problem_summary": """
            16-team tournament, seed X beats Y with prob Y/(X+Y).
            2-seed can secretly swap two teams' bracket positions.
            Find optimal swap to maximize 2-seed's winning probability.
        """,
        "my_approach": """
            1. Recognized swapping affects bracket structure
            2. Thought about weakening 2's path or strengthening 1's opponents
            3. Considered swapping 3 with someone to remove from 2's quarter
        """,
        "official_approach": """
            1. Computed probability distributions recursively through bracket
            2. Evaluated all possible swaps systematically
            3. Swap 3 and 16 is optimal (6.56% improvement)
            4. Moving 3 to 1's side weakens 2's path significantly
        """,
        "answer": "Swap 3 and 16, improvement = 6.55795%",
        "what_i_learned": """
            - Bracket problems require full recursive probability computation
            - Intuition (swap 1 and 2) only gives 1.4% vs optimal 6.6%
            - Best swap often involves moving strong opponent to other bracket half
            - Key is reducing expected opponent strength in your own path
        """
    }
}


# =============================================================================
# KEY TECHNIQUES THAT WORKED
# =============================================================================

KEY_TECHNIQUES = {
    "symmetry_reduction": {
        "description": "Exploit symmetry to reduce integration domain",
        "when_to_use": "Random points in symmetric regions (squares, circles)",
        "example": "Beside the Point: restricted to triangular octant",
        "benefit": "Reduces 4D integral to simpler region"
    },

    "symmetric_difference_of_circles": {
        "description": "Valid region is where one circle includes but other excludes",
        "when_to_use": "Perpendicular bisector problems, equidistant conditions",
        "example": "Circles centered at edge endpoints passing through point",
        "benefit": "Transforms distance condition into geometric region"
    },

    "balanced_curve_counting": {
        "description": "Integer area requires equal inward/outward curves",
        "when_to_use": "Curved path counting with area constraint",
        "example": "Arc-edge Acreage: n curves needs C(n, n/2) balanced assignments",
        "benefit": "Separates topology from curve direction choices"
    },

    "rotation_optimization": {
        "description": "Rotating nested shapes can improve packing",
        "when_to_use": "Packing circles/polygons in concentric arrangement",
        "example": "Circle Time: 30-degree rotation improved coverage",
        "benefit": "Can gain 5-10% efficiency over naive nesting"
    },

    "recursive_tree_decomposition": {
        "description": "Tree = root + subtrees, gives functional equations",
        "when_to_use": "Probability on infinite trees",
        "formula": "f = p * (2f - f^2) for 'exists path in either subtree'",
        "benefit": "Converts infinite structure to finite equation"
    },

    "bracket_recursion": {
        "description": "Compute round-by-round probability distributions",
        "when_to_use": "Tournament/bracket probability problems",
        "example": "Bracketology: P(X wins round k) from P(opponents in round k)",
        "benefit": "Systematic evaluation of all possible paths"
    },

    "indicator_for_answer_form": {
        "description": "Answer structure hints at method",
        "patterns": {
            "pi terms": "Circle geometry, arc length, or area integration",
            "ln terms": "Ratio comparisons, logarithmic probability",
            "sqrt terms": "Distance formulas, quadratic optimization",
            "cubic/polynomial": "Recursive equations, branching processes",
            "rational": "Combinatorial counting, discrete probability"
        }
    }
}


# =============================================================================
# MISTAKES AND MISCONCEPTIONS
# =============================================================================

MISTAKES = {
    "assuming_simple_nesting": {
        "description": "Assumed nested rings scale by simple ratio",
        "puzzle": "Circle Time",
        "wrong_answer": "0.75 (simple 1/3 scaling)",
        "correct_answer": "0.783464 (with rotation)",
        "lesson": "Always check if rotation/offset improves packing"
    },

    "missing_symmetric_difference": {
        "description": "Set up coordinate integral instead of geometric region",
        "puzzle": "Beside the Point",
        "consequence": "Complex 4D integral vs elegant circle intersection",
        "lesson": "Look for geometric interpretation of algebraic conditions"
    },

    "intuitive_but_suboptimal_swap": {
        "description": "Swapping obvious candidates (1 and 2) not optimal",
        "puzzle": "Bracketology 101",
        "wrong_swap": "1 and 2 (1.4% improvement)",
        "correct_swap": "3 and 16 (6.6% improvement)",
        "lesson": "Must compute all options; intuition fails for bracket structure"
    },

    "forgetting_half_condition": {
        "description": "For p<1/2, all-zero path probability is 0",
        "puzzle": "Sum One, Somewhere",
        "consequence": "Must handle p>=1/2 case separately",
        "lesson": "Check boundary conditions in probability equations"
    }
}


# =============================================================================
# HELPER FUNCTIONS - SOLVING PATTERNS
# =============================================================================

def perpendicular_bisector_x_intercept(
    bx: float, by: float, rx: float, ry: float
) -> float | None:
    """
    Find x-coordinate where perpendicular bisector of (bx,by)-(rx,ry)
    intersects the x-axis (y=0).

    Returns None if bisector is parallel to x-axis (rx == bx).

    Used in: Beside the Point type problems
    """
    if abs(bx - rx) < 1e-12:
        return None  # Vertical line, bisector is horizontal

    return (bx**2 + by**2 - rx**2 - ry**2) / (2 * (bx - rx))


def point_closest_to_edge(x: float, y: float, size: float = 1.0) -> str:
    """
    Determine which edge of [0,size] x [0,size] square is closest to point (x,y).

    Returns: 'bottom', 'top', 'left', or 'right'

    Used in: Problems involving nearest boundary
    """
    distances = {
        'bottom': y,
        'top': size - y,
        'left': x,
        'right': size - x
    }
    return min(distances, key=distances.get)


def area_ring_of_circles(r: float, n_circles: int = 6) -> float:
    """
    Calculate area of n_circles equal circles of radius r arranged in a ring.

    Used in: Circle packing problems
    """
    return n_circles * math.pi * r**2


def ring_annulus_bounds(r: float, hexagon_scale: float = 2.0) -> Tuple[float, float]:
    """
    For circles of radius r with centers on hexagon of side (hexagon_scale * r),
    return (inner_radius, outer_radius) of the annulus occupied by the ring.

    Default: hexagon side = 2r (tangent circles)

    Used in: Circle Time type problems
    """
    center_distance = hexagon_scale * r  # Distance from ring center to circle centers
    return (center_distance - r, center_distance + r)


def geometric_series_sum(first_term: float, ratio: float, n_terms: int = None) -> float:
    """
    Sum of geometric series: a + ar + ar^2 + ...

    If n_terms is None, returns infinite sum (requires |ratio| < 1)

    Used in: Nested ring/circle problems
    """
    if n_terms is None:
        if abs(ratio) >= 1:
            raise ValueError("Infinite series requires |ratio| < 1")
        return first_term / (1 - ratio)
    else:
        if abs(ratio - 1) < 1e-12:
            return first_term * n_terms
        return first_term * (1 - ratio**n_terms) / (1 - ratio)


def binary_tree_path_probability(
    p_zero: float,
    target_sum: int = 0
) -> float:
    """
    Probability that infinite binary tree (nodes 0 with prob p, 1 with prob 1-p)
    contains an infinite downward path with sum exactly target_sum.

    Uses recursive formula: f = p * (2f - f^2) for sum=0

    Used in: Sum One, Somewhere type problems
    """
    if target_sum != 0:
        raise NotImplementedError("Only sum=0 implemented; sum>0 requires more complex recurrence")

    if p_zero < 0.5:
        return 0.0  # Below critical probability, no infinite all-zero path exists

    # f = p(2f - f^2) => f(1 - 2p + pf) = 0 => f = 0 or f = (2p-1)/p
    return (2 * p_zero - 1) / p_zero


def solve_sum_one_somewhere_cubic() -> float:
    """
    Solve 3p^3 - 10p^2 + 12p - 4 = 0 for the root in (0.5, 1).

    This is the p where P(exists path with sum <= 1) = 1/2.

    Returns: p approximately 0.5306035754
    """
    if HAS_NUMPY:
        # Use numpy for precise root finding
        coeffs = [3, -10, 12, -4]
        roots = np.roots(coeffs)
        for root in roots:
            if np.isreal(root) and 0.5 < root.real < 1:
                return root.real

    # Fallback: Newton-Raphson method
    def f(p):
        return 3*p**3 - 10*p**2 + 12*p - 4

    def fprime(p):
        return 9*p**2 - 20*p + 12

    p = 0.53  # Initial guess
    for _ in range(50):
        p = p - f(p) / fprime(p)

    return p


def bracket_win_probability(
    seed_x: int,
    seed_y: int
) -> float:
    """
    Probability that seed X beats seed Y in head-to-head matchup.
    Formula: P(X beats Y) = Y / (X + Y)

    Used in: Bracketology type problems
    """
    return seed_y / (seed_x + seed_y)


def compute_tournament_probability(
    seed: int,
    bracket_positions: Dict[int, int],
    n_teams: int = 16
) -> float:
    """
    Compute probability that given seed wins the tournament.

    bracket_positions: maps seed -> bracket position (1-16)
    Standard bracket: position 1 plays 16, 2 plays 15, etc.

    This is a simplified version; full implementation would need
    recursive probability through all rounds.

    Used in: Bracketology 101 type problems
    """
    # This would require full bracket simulation
    # Placeholder for the pattern
    raise NotImplementedError(
        "Full bracket computation requires recursive evaluation. "
        "Pattern: P(seed wins round k) depends on P(each possible opponent in round k)"
    )


def quarter_circle_area_contribution(
    curving_outward: bool
) -> float:
    """
    Area contribution of a quarter-circle arc on unit grid.

    If curving outward: adds pi/4 - (cell corner triangle) to enclosed area
    If curving inward: subtracts pi/4 - (cell corner triangle) from enclosed area

    For integer enclosed area, need equal outward and inward curves.

    Used in: Arc-edge Acreage type problems
    """
    # Quarter circle area = pi/4
    # Cell corner (right triangle with legs 1) area = 1/2
    # Net contribution depends on orientation
    quarter_circle = math.pi / 4
    if curving_outward:
        return quarter_circle  # Adds to enclosed area
    else:
        return -quarter_circle  # Subtracts from enclosed area


def count_balanced_curve_assignments(perimeter_length: int) -> int:
    """
    Count ways to assign inward/outward to perimeter curves
    such that they balance (equal numbers of each).

    Requires even perimeter_length.

    Returns: C(n, n/2) where n = perimeter_length

    Used in: Arc-edge Acreage type problems
    """
    if perimeter_length % 2 != 0:
        return 0  # Cannot balance odd number

    n = perimeter_length
    k = n // 2
    return math.comb(n, k)


# =============================================================================
# MONTE CARLO VERIFICATION HELPERS
# =============================================================================

def monte_carlo_beside_the_point(n_samples: int = 100000) -> float:
    """
    Verify Beside the Point answer via Monte Carlo simulation.

    Expected: ~0.4914
    """
    count = 0
    rand = random.random  # Use stdlib random

    for _ in range(n_samples):
        # Random points in unit square
        bx, by = rand(), rand()
        rx, ry = rand(), rand()

        # Find closest edge to blue point
        closest = point_closest_to_edge(bx, by)

        # Check if perpendicular bisector intersects that edge
        if closest == 'bottom':
            px = perpendicular_bisector_x_intercept(bx, by, rx, ry)
            if px is not None and 0 <= px <= 1:
                count += 1
        elif closest == 'top':
            # Mirror problem
            px = perpendicular_bisector_x_intercept(bx, 1-by, rx, 1-ry)
            if px is not None and 0 <= px <= 1:
                count += 1
        elif closest == 'left':
            # Rotate problem
            py = perpendicular_bisector_x_intercept(by, bx, ry, rx)
            if py is not None and 0 <= py <= 1:
                count += 1
        elif closest == 'right':
            py = perpendicular_bisector_x_intercept(by, 1-bx, ry, 1-rx)
            if py is not None and 0 <= py <= 1:
                count += 1

    return count / n_samples


def monte_carlo_binary_tree_path(
    p_zero: float,
    max_depth: int = 50,
    n_samples: int = 10000
) -> Tuple[float, float]:
    """
    Estimate probability of infinite path with sum 0 and sum <= 1.

    Uses finite depth approximation.

    Returns: (prob_sum_0, prob_sum_at_most_1)
    """
    count_sum_0 = 0
    count_sum_1 = 0

    for _ in range(n_samples):
        # Generate tree and check for paths
        has_sum_0_path = _check_path_sum_0(p_zero, max_depth)
        has_sum_1_path = _check_path_sum_at_most_1(p_zero, max_depth)

        if has_sum_0_path:
            count_sum_0 += 1
        if has_sum_1_path:
            count_sum_1 += 1

    return count_sum_0 / n_samples, count_sum_1 / n_samples


def _check_path_sum_0(p: float, depth: int) -> bool:
    """Check if random tree has path of all zeros to given depth."""
    if depth == 0:
        return True

    # Root
    if random.random() >= p:  # Node is 1
        return False

    # Check both children
    return _check_path_sum_0(p, depth-1) or _check_path_sum_0(p, depth-1)


def _check_path_sum_at_most_1(p: float, depth: int, sum_so_far: int = 0) -> bool:
    """Check if random tree has path with sum <= 1 to given depth."""
    if sum_so_far > 1:
        return False
    if depth == 0:
        return True

    # Root value
    node_value = 0 if random.random() < p else 1
    new_sum = sum_so_far + node_value

    if new_sum > 1:
        return False

    # Check both children
    return (_check_path_sum_at_most_1(p, depth-1, new_sum) or
            _check_path_sum_at_most_1(p, depth-1, new_sum))


# =============================================================================
# SUMMARY: PLAYBOOK FOR FUTURE PUZZLES
# =============================================================================

PLAYBOOK = """
GEOMETRY/PROBABILITY PUZZLE PLAYBOOK
=====================================

1. IDENTIFY THE ANSWER FORM
   - Has pi? => Circle geometry, integration over arcs
   - Has ln? => Ratio conditions, logarithmic probability
   - Has sqrt? => Distance formulas, optimization
   - Polynomial root? => Recursive/branching structure
   - Integer? => Combinatorial counting

2. GEOMETRY PROBLEMS
   a) Look for SYMMETRY to reduce dimensions
   b) Translate algebraic conditions to GEOMETRIC REGIONS
      - "Equidistant" => perpendicular bisector
      - "Closer to X than Y" => half-plane bounded by bisector
   c) For curved boundaries, check if pi terms must CANCEL
   d) For packing problems, try ROTATION of nested shapes

3. PROBABILITY ON TREES
   a) Use recursive decomposition: f(tree) = g(f(left), f(right))
   b) "Either subtree succeeds" => P = 1 - (1-p)^2 = 2p - p^2
   c) Watch for CRITICAL THRESHOLDS (e.g., p = 1/2 for survival)
   d) Expect POLYNOMIAL equations for exact answers

4. TOURNAMENT/BRACKET PROBLEMS
   a) Compute probabilities RECURSIVELY through rounds
   b) Don't trust intuition for optimal strategy
   c) ENUMERATE all possibilities when feasible
   d) Key insight: move strong opponents to OTHER bracket half

5. COUNTING WITH CONSTRAINTS
   a) Decompose: (structure choices) x (within-structure choices)
   b) For balanced conditions: use binomial coefficients C(n, n/2)
   c) Group by invariant (e.g., perimeter length)

6. VERIFICATION
   - Monte Carlo simulation is invaluable
   - Check answer has correct limiting behavior
   - Verify special cases (p=0, p=1, degenerate geometry)
"""

if __name__ == "__main__":
    print("=" * 60)
    print("GEOMETRY & PROBABILITY PUZZLE LEARNINGS")
    print("=" * 60)

    print("\n--- Puzzle Attempts ---")
    for name, data in PUZZLE_ATTEMPTS.items():
        print(f"\n{name.upper()}")
        print(f"  Answer: {data['answer']}")

    print("\n--- Key Techniques ---")
    for name, data in KEY_TECHNIQUES.items():
        print(f"\n{name}: {data['description']}")

    print("\n--- Common Mistakes ---")
    for name, data in MISTAKES.items():
        print(f"\n{name}: {data['lesson']}")

    print("\n--- Verification: Beside the Point ---")
    expected = (1 + 2*math.pi - math.log(4)) / 12
    print(f"  Expected: {expected:.10f}")
    # Uncomment to run Monte Carlo (takes a few seconds)
    # mc_result = monte_carlo_beside_the_point(100000)
    # print(f"  Monte Carlo: {mc_result:.6f}")

    print("\n--- Verification: Sum One Somewhere ---")
    p_solution = solve_sum_one_somewhere_cubic()
    print(f"  p = {p_solution:.10f}")

    print("\n" + PLAYBOOK)
