"""
Debug script for the mathematical contradiction in the Subtiles 2 puzzle.

Investigations:
1. Remove N<=17 cap: search for (a,b,c) where ALL expressions are just positive integers
2. Try fractional/real variables
3. Exhaustive search with relaxed constraints
4. Identify which expression changes would resolve the contradiction
5. Grid size analysis
"""

import math
import itertools
from collections import Counter

# ============================================================
# EXPRESSION DEFINITIONS (from grid.json / solver_anthropic.py)
# ============================================================
def safe_eval(func, a, b, c):
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

def is_positive_integer(x, tol=1e-9):
    if x is None:
        return False
    if not isinstance(x, (int, float)):
        return False
    if math.isnan(x) or math.isinf(x):
        return False
    return x > tol and abs(x - round(x)) < tol

LABELED_CELLS = {
    (0, 4):   ("6c - 4b",              lambda a, b, c: 6*c - 4*b),
    (1, 6):   ("8 - b",                lambda a, b, c: 8 - b),
    (2, 1):   ("(a^b - 4)/(6c + 1)",   lambda a, b, c: (a**b - 4) / (6*c + 1)),
    (2, 3):   ("(b + c)/(c - 1)",      lambda a, b, c: (b + c) / (c - 1)),
    (2, 5):   ("b^2 - b/c",            lambda a, b, c: b**2 - b / c),
    (2, 7):   ("sqrt(30 + a)/c",       lambda a, b, c: math.sqrt(30 + a) / c),
    (2, 9):   ("(a + b)/(c - 3a)",     lambda a, b, c: (a + b) / (c - 3*a)),
    (3, 4):   ("(b - 3a)/(a - c)",     lambda a, b, c: (b - 3*a) / (a - c)),
    (3, 6):   ("8a - 2b",              lambda a, b, c: 8*a - 2*b),
    (3, 8):   ("b/(a - c)",            lambda a, b, c: b / (a - c)),
    (3, 10):  ("(b + 9)/sqrt(c - a)",  lambda a, b, c: (b + 9) / math.sqrt(c - a)),
    (4, 1):   ("18/(ac + 1)",          lambda a, b, c: 18 / (a*c + 1)),
    (4, 5):   ("c^b",                  lambda a, b, c: c**b),
    (4, 9):   ("(3 + b^2)/sqrt(3+2c)", lambda a, b, c: (3 + b**2) / math.sqrt(3 + 2*c)),
    (5, 3):   ("b/(a^2 - c^2)",        lambda a, b, c: b / (a**2 - c**2)),
    (5, 10):  ("sqrt(a + 2)/a",        lambda a, b, c: math.sqrt(a + 2) / a),
    (6, 2):   ("a^b - 12/a",           lambda a, b, c: a**b - 12 / a),
    (6, 4):   ("2c + c/a",             lambda a, b, c: 2*c + c / a),
    (6, 6):   ("4a - 5b",              lambda a, b, c: 4*a - 5*b),
    (6, 8):   ("c + 2a",               lambda a, b, c: c + 2*a),
    (6, 10):  ("b/(9a - 5c)",          lambda a, b, c: b / (9*a - 5*c)),
    (7, 0):   ("(b^3+2c)/(b+2c)",      lambda a, b, c: (b**3 + 2*c) / (b + 2*c)),
    (7, 8):   ("b/(a - 1)",            lambda a, b, c: b / (a - 1)),
    (8, 2):   ("(c - b)/(2a)",         lambda a, b, c: (c - b) / (2*a)),
    (8, 6):   ("b/(a - c)",            lambda a, b, c: b / (a - c)),
    (8, 10):  ("(b + c)/(a - c)",      lambda a, b, c: (b + c) / (a - c)),
    (9, 2):   ("log_c(a)",             lambda a, b, c: math.log(a) / math.log(c)),
    (9, 4):   ("(c^2 - b)/a",          lambda a, b, c: (c**2 - b) / a),
    (9, 6):   ("(b - 1)^2",            lambda a, b, c: (b - 1)**2),
    (9, 8):   ("cbrt(43 - ac)/a",      lambda a, b, c: (abs(43 - a*c)**(1/3) * (1 if 43 - a*c >= 0 else -1)) / a if 43 - a*c != 0 else 0.0),
    (10, 3):  ("(b - a)/(a - c)",      lambda a, b, c: (b - a) / (a - c)),
    (10, 5):  ("11 - b",               lambda a, b, c: 11 - b),
    (10, 7):  ("(b - 2a)/(a - c)",     lambda a, b, c: (b - 2*a) / (a - c)),
    (10, 9):  ("(c + 3)/a",            lambda a, b, c: (c + 3) / a),
    (10, 11): ("8c - b/c",             lambda a, b, c: 8*c - b / c),
    (11, 5):  ("b^2",                  lambda a, b, c: b**2),
    (12, 8):  ("(2^b + 1)/(ac)",       lambda a, b, c: (2**b + 1) / (a*c)),
}


# ============================================================
# INVESTIGATION 1: Remove the N cap entirely
# Search for (a,b,c) where ALL expressions are positive integers
# (no upper bound constraint at all)
# ============================================================
def investigation_1_no_cap():
    print("=" * 70)
    print("INVESTIGATION 1: Search with NO upper bound on expression values")
    print("=" * 70)

    results = []
    for a in range(1, 50):
        for b in range(1, 20):
            for c in range(2, 50):
                if a == c:
                    continue
                all_valid = True
                max_val = 0
                for pos, (name, func) in LABELED_CELLS.items():
                    v = safe_eval(func, a, b, c)
                    if not is_positive_integer(v):
                        all_valid = False
                        break
                    max_val = max(max_val, int(round(v)))
                if all_valid:
                    results.append((a, b, c, max_val))

    if results:
        print(f"\nFound {len(results)} valid assignment(s) with no upper bound:")
        for a, b, c, max_v in results[:20]:
            print(f"  a={a}, b={b}, c={c}, max_expression_value={max_v}")
    else:
        print("\nNo valid (a, b, c) found even without upper bound!")
        print("This confirms the contradiction is fundamental, not due to the N cap.")

    return results


# ============================================================
# INVESTIGATION 2: Detailed analysis of the contradiction
# ============================================================
def investigation_2_contradiction_detail():
    print("\n" + "=" * 70)
    print("INVESTIGATION 2: Detailed contradiction analysis")
    print("=" * 70)

    print("\nKey expressions in the contradiction:")
    print("  (3,6):  8a - 2b  >= 1  (positive integer)")
    print("  (6,6):  4a - 5b  >= 1  (positive integer)")
    print("  (9,6):  (b-1)^2  >= 1  (positive integer)")
    print("  (11,5): b^2      >= 1  (positive integer)")
    print("  (10,5): 11 - b   >= 1  (positive integer)")
    print("  (1,6):  8 - b    >= 1  (positive integer)")

    print("\nFrom (1,6): 8 - b >= 1 => b <= 7")
    print("From (10,5): 11 - b >= 1 => b <= 10")
    print("From (9,6): (b-1)^2 >= 1 => b >= 2 (also b != 1)")

    print("\nSo b in {2, 3, 4, 5, 6, 7}")

    print("\nFor each b, analyzing 8a - 2b >= 1 and 4a - 5b >= 1:")
    print("  8a - 2b >= 1  =>  a >= (2b + 1)/8")
    print("  4a - 5b >= 1  =>  a >= (5b + 1)/4")

    print("\nNow, there is NO upper bound constraint from just these two expressions")
    print("(unless we impose an N cap). Let me check what other expressions constrain a from above...\n")

    # Expressions that constrain a from above (for various b, c):
    # (5,10): sqrt(a + 2)/a >= 1 => sqrt(a+2) >= a => a+2 >= a^2 => a^2 - a - 2 <= 0 => a <= 2
    # Wait! (5,10) just needs to be a positive integer, not >= 1 specifically, but it IS >= 1.
    # sqrt(a+2)/a = positive integer k >= 1
    # => sqrt(a+2) = ka => a+2 = k^2 * a^2 => k^2 * a^2 - a - 2 = 0
    # => a = (1 + sqrt(1 + 8k^2)) / (2k^2)

    print("Expression (5,10): sqrt(a+2)/a must be a positive integer k")
    print("  sqrt(a+2)/a = k  =>  a+2 = k^2 * a^2  =>  k^2*a^2 - a - 2 = 0")
    print("  a = (1 + sqrt(1 + 8k^2)) / (2k^2)")
    print()
    for k in range(1, 10):
        disc = 1 + 8*k*k
        sqrt_disc = math.sqrt(disc)
        a = (1 + sqrt_disc) / (2*k*k)
        print(f"  k={k}: a = {a:.6f}", end="")
        if abs(a - round(a)) < 1e-9 and round(a) >= 1:
            print(f"  => a = {int(round(a))} (INTEGER!)")
        else:
            print()

    print("\nSo (5,10) forces a = 2 (when k=1, sqrt(4)/2 = 1)")
    print("  Or k must yield an integer a. Only k=1 => a=2 works.")

    print("\nWith a = 2:")
    print("  (3,6): 8*2 - 2b = 16 - 2b >= 1 => b <= 7 (OK)")
    print("  (6,6): 4*2 - 5b = 8 - 5b >= 1 => b <= 1")
    print("  But b >= 2 from (9,6). CONTRADICTION!")

    print("\n  Alternatively, a = 2, b = 1:")
    print("  (9,6): (1-1)^2 = 0, NOT a positive integer. CONTRADICTION!")

    print("\nTHIS IS THE CORE CONTRADICTION:")
    print("  (5,10) forces a = 2")
    print("  (6,6) with a = 2 forces b <= 1")
    print("  (9,6) forces b >= 2")
    print("  => No valid b exists.")


# ============================================================
# INVESTIGATION 3: What if variables can be non-integer?
# ============================================================
def investigation_3_noninteger_vars():
    print("\n" + "=" * 70)
    print("INVESTIGATION 3: Can variables be non-integer?")
    print("=" * 70)

    print("\nThe instructions say: 'Place positive integers in some of the cells'")
    print("The CELL VALUES must be positive integers, but what about a, b, c?")
    print("\nFrom the example: 'After solving for x=2, y=6 (middle), the grid can be completed'")
    print("In the example, x and y are integers. But the puzzle says nothing explicit about")
    print("whether a, b, c must be integers.\n")

    print("However, let's check: can a, b, c be non-integer and still make all expressions integer?\n")

    # Key constraint: (9,2) is log_c(a) which must be a positive integer.
    # log_c(a) = k  =>  a = c^k
    # (4,5) is c^b which must be a positive integer.
    # (11,5) is b^2 which must be a positive integer.
    # (1,6) is 8-b which must be a positive integer => b is an integer

    print("Analysis of variable integrality:")
    print()
    print("b MUST be integer:")
    print("  (1,6):  8 - b must be a positive integer => b is an integer")
    print("  (10,5): 11 - b must be a positive integer => b is an integer [CONFIRMED]")
    print("  (11,5): b^2 must be a positive integer => b^2 is a positive integer")
    print("  (9,6):  (b-1)^2 must be a positive integer => (b-1)^2 is a positive integer")
    print("  Combined: b is an integer (from 8-b being integer)")
    print()

    print("a MUST be integer (or at least rational):")
    print("  (5,10): sqrt(a+2)/a must be a positive integer k")
    print("          => a+2 = k^2*a^2, only works for specific a values")
    print("  (6,8):  c + 2a must be a positive integer")
    print("  (3,6):  8a - 2b must be a positive integer (b integer => 8a is integer => a is rational)")
    print("  (6,6):  4a - 5b must be a positive integer => 4a is integer => a = n/4 for some n")
    print("  Combined with 8a integer: a = n/8 for some n. With 4a integer: a = m/4.")
    print("  8a - 2b integer and 4a - 5b integer are both satisfied if a is integer.")
    print()

    # Check: does a = n/2 or a = n/4 help?
    print("Testing a = n/4 (quarter-integer values):")
    for a_num in range(1, 80):  # a = a_num/4
        a = a_num / 4.0
        for b in range(2, 8):
            for c_num in range(1, 80):  # c = c_num/4
                c = c_num / 4.0
                if abs(a - c) < 1e-12:
                    continue
                all_valid = True
                for pos, (name, func) in LABELED_CELLS.items():
                    v = safe_eval(func, a, b, c)
                    if not is_positive_integer(v):
                        all_valid = False
                        break
                if all_valid:
                    print(f"  FOUND: a={a}, b={b}, c={c}")
    print("  (search complete)")

    print("\nTesting a = n/2 (half-integer values):")
    found_half = False
    for a_num in range(1, 100):  # a = a_num/2
        a = a_num / 2.0
        for b in range(2, 8):
            for c_num in range(1, 100):  # c = c_num/2
                c = c_num / 2.0
                if abs(a - c) < 1e-12:
                    continue
                if c < 0.5:
                    continue
                all_valid = True
                for pos, (name, func) in LABELED_CELLS.items():
                    v = safe_eval(func, a, b, c)
                    if not is_positive_integer(v):
                        all_valid = False
                        break
                if all_valid:
                    print(f"  FOUND: a={a}, b={b}, c={c}")
                    found_half = True
    if not found_half:
        print("  No solutions found with half-integer values either.")


# ============================================================
# INVESTIGATION 4: What grid size would work?
# ============================================================
def investigation_4_grid_size():
    print("\n" + "=" * 70)
    print("INVESTIGATION 4: Grid size analysis")
    print("=" * 70)

    print("\nThe constraints.md says 13x11 (143 cells, N<=16)")
    print("The solver_anthropic.py says 13x13 (169 cells, N<=17)")
    print("The grid_layout.json says 13x13")
    print()
    print("Looking at the labeled cells, the max column index is 11 (at (10,11)).")
    print("Could the grid actually be 13x12? That gives 156 cells, N<=16.")
    print("Or 13x13 giving 169 cells, N<=17.")
    print()

    # The N cap doesn't matter since we showed there's no solution even without it
    print("But as shown in Investigation 1, even with NO upper bound, there's no solution.")
    print("The grid size is irrelevant to the contradiction.")
    print("The issue is purely in the expression definitions.")


# ============================================================
# INVESTIGATION 5: Which single expression change fixes things?
# ============================================================
def investigation_5_expression_fixes():
    print("\n" + "=" * 70)
    print("INVESTIGATION 5: Which expression change(s) would resolve the contradiction?")
    print("=" * 70)

    print("\nThe contradiction chain:")
    print("  (5,10): sqrt(a+2)/a => forces a=2")
    print("  (6,6): 4a-5b with a=2 => 8-5b >= 1 => b <= 1")
    print("  (9,6): (b-1)^2 >= 1 => b >= 2")
    print()

    # Let's try plausible OCR-like misreadings of expressions and see which ones
    # open up solutions

    # Create variants of expressions and test
    def test_variant(desc, variant_cells, a_range=range(1,30), b_range=range(1,12), c_range=range(2,30)):
        """Test if a variant set of expressions has any solution."""
        solutions = []
        for a in a_range:
            for b in b_range:
                for c in c_range:
                    if a == c:
                        continue
                    all_valid = True
                    max_val = 0
                    for pos, (name, func) in variant_cells.items():
                        v = safe_eval(func, a, b, c)
                        if not is_positive_integer(v):
                            all_valid = False
                            break
                        max_val = max(max_val, int(round(v)))
                    if all_valid:
                        solutions.append((a, b, c, max_val))
        return solutions

    # Variant 1: (5,10) could be "sqrt(a+2)*a" instead of "sqrt(a+2)/a"
    print("--- Variant 1: (5,10) = sqrt(a+2)*a instead of sqrt(a+2)/a ---")
    v1 = dict(LABELED_CELLS)
    v1[(5,10)] = ("sqrt(a+2)*a", lambda a, b, c: math.sqrt(a + 2) * a)
    sols = test_variant("v1", v1)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")

    # Variant 2: (6,6) could be "4a - 5c" instead of "4a - 5b"
    print("\n--- Variant 2: (6,6) = 4a - 5c instead of 4a - 5b ---")
    v2 = dict(LABELED_CELLS)
    v2[(6,6)] = ("4a - 5c", lambda a, b, c: 4*a - 5*c)
    sols = test_variant("v2", v2)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")

    # Variant 3: (3,6) could be "8a - 26" (constant) instead of "8a - 2b"
    print("\n--- Variant 3: (3,6) = 8a - 26 instead of 8a - 2b ---")
    v3 = dict(LABELED_CELLS)
    v3[(3,6)] = ("8a - 26", lambda a, b, c: 8*a - 26)
    sols = test_variant("v3", v3)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")

    # Variant 4: (6,6) could be "4a + 5b" (addition, not subtraction)
    print("\n--- Variant 4: (6,6) = 4a + 5b instead of 4a - 5b ---")
    v4 = dict(LABELED_CELLS)
    v4[(6,6)] = ("4a + 5b", lambda a, b, c: 4*a + 5*b)
    sols = test_variant("v4", v4)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")

    # Variant 5: (3,6) could be "8a - 2c" instead of "8a - 2b"
    print("\n--- Variant 5: (3,6) = 8a - 2c instead of 8a - 2b ---")
    v5 = dict(LABELED_CELLS)
    v5[(3,6)] = ("8a - 2c", lambda a, b, c: 8*a - 2*c)
    sols = test_variant("v5", v5)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")

    # Variant 6: (6,6) could be "4c - 5b" instead of "4a - 5b"
    print("\n--- Variant 6: (6,6) = 4c - 5b instead of 4a - 5b ---")
    v6 = dict(LABELED_CELLS)
    v6[(6,6)] = ("4c - 5b", lambda a, b, c: 4*c - 5*b)
    sols = test_variant("v6", v6)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")

    # Variant 7: (5,10) is actually "sqrt(a+2)/c" (not /a)
    print("\n--- Variant 7: (5,10) = sqrt(a+2)/c instead of sqrt(a+2)/a ---")
    v7 = dict(LABELED_CELLS)
    v7[(5,10)] = ("sqrt(a+2)/c", lambda a, b, c: math.sqrt(a + 2) / c)
    sols = test_variant("v7", v7)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")

    # Variant 8: (6,6) could be "4a - 5b" but maybe it's really "4c - 5b"
    # (confusion of a and c in the image)
    # Already done as variant 6

    # Variant 9: (3,6) is "8c - 2b" instead of "8a - 2b"
    print("\n--- Variant 9: (3,6) = 8c - 2b instead of 8a - 2b ---")
    v9 = dict(LABELED_CELLS)
    v9[(3,6)] = ("8c - 2b", lambda a, b, c: 8*c - 2*b)
    sols = test_variant("v9", v9)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")

    # Variant 10: What if (6,6) is "4a - 5" (just a constant minus) instead of "4a - 5b"?
    print("\n--- Variant 10: (6,6) = 4a - 5 instead of 4a - 5b ---")
    v10 = dict(LABELED_CELLS)
    v10[(6,6)] = ("4a - 5", lambda a, b, c: 4*a - 5)
    sols = test_variant("v10", v10)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")

    # Variant 11: What if (3,6) is "8a - 2b" but (5,10) is something else entirely?
    # Like sqrt(a+2) without the division
    print("\n--- Variant 11: (5,10) = sqrt(a+2) (no division) ---")
    v11 = dict(LABELED_CELLS)
    v11[(5,10)] = ("sqrt(a+2)", lambda a, b, c: math.sqrt(a + 2))
    sols = test_variant("v11", v11)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")

    # Variant 12: What if (6,6) is "4a - b" instead of "4a - 5b"?
    print("\n--- Variant 12: (6,6) = 4a - b instead of 4a - 5b ---")
    v12 = dict(LABELED_CELLS)
    v12[(6,6)] = ("4a - b", lambda a, b, c: 4*a - b)
    sols = test_variant("v12", v12)
    if sols:
        print(f"  Solutions found: {len(sols)}")
        for s in sols[:5]:
            print(f"    a={s[0]}, b={s[1]}, c={s[2]}, max={s[3]}")
    else:
        print("  No solutions")


# ============================================================
# INVESTIGATION 6: Best-score analysis - which expressions fail?
# ============================================================
def investigation_6_best_candidates():
    print("\n" + "=" * 70)
    print("INVESTIGATION 6: Best candidate analysis (no N cap)")
    print("=" * 70)

    best_score = 0
    candidates = []

    for a in range(1, 30):
        for b in range(1, 12):
            for c in range(2, 30):
                if a == c:
                    continue
                score = 0
                failing = []
                for pos, (name, func) in LABELED_CELLS.items():
                    v = safe_eval(func, a, b, c)
                    if is_positive_integer(v):
                        score += 1
                    else:
                        failing.append((pos, name, v))
                if score >= best_score - 1:
                    candidates.append((score, a, b, c, failing))
                    if score > best_score:
                        best_score = score

    candidates.sort(reverse=True)
    top = [x for x in candidates if x[0] >= best_score - 1]

    print(f"\nBest score: {best_score}/{len(LABELED_CELLS)}")
    print(f"\nTop candidates (within 1 of best):")
    for score, a, b, c, failing in top[:15]:
        print(f"\n  a={a}, b={b}, c={c}: {score}/{len(LABELED_CELLS)} valid")
        print(f"  Failing expressions:")
        for pos, name, v in failing:
            v_str = f"{v:.4f}" if v is not None else "UNDEFINED"
            print(f"    {pos} {name}: {v_str}")


# ============================================================
# INVESTIGATION 7: Systematic single-expression removal
# ============================================================
def investigation_7_removal():
    print("\n" + "=" * 70)
    print("INVESTIGATION 7: Which single expression, if removed, allows a solution?")
    print("=" * 70)

    for remove_pos in sorted(LABELED_CELLS.keys()):
        remove_name = LABELED_CELLS[remove_pos][0]
        reduced = {k: v for k, v in LABELED_CELLS.items() if k != remove_pos}

        found = False
        for a in range(1, 30):
            if found:
                break
            for b in range(1, 12):
                if found:
                    break
                for c in range(2, 30):
                    if a == c:
                        continue
                    all_valid = True
                    for pos, (name, func) in reduced.items():
                        v = safe_eval(func, a, b, c)
                        if not is_positive_integer(v):
                            all_valid = False
                            break
                    if all_valid:
                        print(f"  Removing {remove_pos} ({remove_name}): SOLUTION EXISTS "
                              f"a={a}, b={b}, c={c}")
                        found = True
                        break
        if not found:
            print(f"  Removing {remove_pos} ({remove_name}): still no solution")


# ============================================================
# INVESTIGATION 8: Systematic check - try each pair of expressions removed
# ============================================================
def investigation_8_pair_removal():
    print("\n" + "=" * 70)
    print("INVESTIGATION 8: Which pair of expressions, if removed, allows a solution?")
    print("=" * 70)

    positions = sorted(LABELED_CELLS.keys())
    found_pairs = []

    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            p1, p2 = positions[i], positions[j]
            reduced = {k: v for k, v in LABELED_CELLS.items()
                       if k != p1 and k != p2}

            found = False
            for a in range(1, 25):
                if found:
                    break
                for b in range(1, 10):
                    if found:
                        break
                    for c in range(2, 25):
                        if a == c:
                            continue
                        all_valid = True
                        for pos, (name, func) in reduced.items():
                            v = safe_eval(func, a, b, c)
                            if not is_positive_integer(v):
                                all_valid = False
                                break
                        if all_valid:
                            n1 = LABELED_CELLS[p1][0]
                            n2 = LABELED_CELLS[p2][0]
                            found_pairs.append((p1, n1, p2, n2, a, b, c))
                            found = True
                            break

    if found_pairs:
        print(f"\nFound {len(found_pairs)} pairs that allow solutions:")
        for p1, n1, p2, n2, a, b, c in found_pairs:
            print(f"  Remove {p1}({n1}) + {p2}({n2}): a={a}, b={b}, c={c}")
    else:
        print("\nNo pair removal produces a solution (very surprising)")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    investigation_1_no_cap()
    investigation_2_contradiction_detail()
    investigation_3_noninteger_vars()
    investigation_4_grid_size()
    investigation_5_expression_fixes()
    investigation_6_best_candidates()
    investigation_7_removal()
    # investigation_8 is slow, run separately if needed
    print("\n\nDone. Run investigation_8_pair_removal() separately if needed (slow).")
