"""
Extended debug: pair removal, and deeper image-verification analysis.
"""

import math
from collections import Counter

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
# Find which pair of expressions, when removed, allows a solution
# ============================================================
def pair_removal_search():
    print("=" * 70)
    print("PAIR REMOVAL SEARCH")
    print("=" * 70)

    positions = sorted(LABELED_CELLS.keys())
    found_pairs = []

    total_pairs = len(positions) * (len(positions) - 1) // 2
    checked = 0

    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            checked += 1
            if checked % 50 == 0:
                print(f"  Checked {checked}/{total_pairs} pairs...")

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

    print(f"\nChecked all {total_pairs} pairs.")
    if found_pairs:
        print(f"\nFound {len(found_pairs)} pairs that allow solutions:")
        for p1, n1, p2, n2, a, b, c in found_pairs:
            print(f"  Remove {p1}({n1}) + {p2}({n2}): a={a}, b={b}, c={c}")
    else:
        print("\nNo pair removal produces a solution.")

    return found_pairs


# ============================================================
# Analyze mutual constraints carefully
# ============================================================
def deep_constraint_analysis():
    print("\n" + "=" * 70)
    print("DEEP CONSTRAINT ANALYSIS")
    print("=" * 70)

    print("\n--- Constraints that force specific variable values ---\n")

    print("(5,10): sqrt(a+2)/a = k (positive integer)")
    print("  => a+2 = k^2*a^2, only k=1 gives integer a=2.")
    print("  FORCES: a = 2\n")

    print("(2,7): sqrt(30+a)/c = k => sqrt(32)/c = k => c = sqrt(32)/k = 4*sqrt(2)/k")
    print("  For c to be a positive integer: 4*sqrt(2)/k must be integer.")
    print("  sqrt(2) is irrational, so no k makes this integer!")
    print("  CONTRADICTION already at (2,7) if a=2!")

    print("\n  Let me verify: sqrt(30+2)/c = sqrt(32)/c = 4*sqrt(2)/c")
    for c in range(1, 30):
        val = math.sqrt(32) / c
        if is_positive_integer(val):
            print(f"    c={c}: {val} -- IS integer")
        elif abs(val - round(val)) < 0.01:
            print(f"    c={c}: {val:.6f} -- CLOSE to integer")
    print("  No integer c makes sqrt(32)/c an integer. (2,7) alone blocks a=2!")
    print()

    print("BUT WAIT: If a != 2, then (5,10) cannot be a positive integer.")
    print("So (5,10) AND (2,7) TOGETHER are fundamentally incompatible.")
    print("This is the most minimal contradiction!\n")

    print("Let's verify by checking ONLY these two constraints:")
    for a in range(1, 100):
        v1 = math.sqrt(a + 2) / a
        if is_positive_integer(v1):
            for c in range(1, 100):
                v2 = math.sqrt(30 + a) / c
                if is_positive_integer(v2):
                    print(f"  a={a}, c={c}: (5,10)={v1}, (2,7)={v2} -- BOTH INTEGER!")

    print("  No (a, c) found. Confirmed: (5,10) and (2,7) are incompatible.\n")

    print("=" * 70)
    print("MINIMUM CONTRADICTION IDENTIFIED")
    print("=" * 70)
    print()
    print("Expression (5,10) = sqrt(a+2)/a")
    print("Expression (2,7)  = sqrt(30+a)/c")
    print()
    print("For (5,10) to be a positive integer:")
    print("  sqrt(a+2)/a = k => a+2 = k^2*a^2")
    print("  Only solution: k=1, a=2")
    print()
    print("For (2,7) with a=2:")
    print("  sqrt(32)/c must be a positive integer")
    print("  sqrt(32) = 4*sqrt(2) is irrational")
    print("  No integer c works.")
    print()
    print("These TWO expressions alone make the system unsolvable.")
    print("At least one of them must be transcribed incorrectly from the image.")


# ============================================================
# What are likely misreadings from the image?
# ============================================================
def likely_misreadings():
    print("\n" + "=" * 70)
    print("LIKELY IMAGE MISREADINGS")
    print("=" * 70)

    print("\nThe two expressions that form the minimum contradiction:")
    print("  (5,10): sqrt(a+2)/a")
    print("  (2,7):  sqrt(30+a)/c")
    print()
    print("Possible misreadings of (5,10):")
    print("  - sqrt(a+2)/c  (a vs c confusion)")
    print("  - sqrt(c+2)/a  (a vs c swap)")
    print("  - sqrt(a+2)/b")
    print("  - (a+2)/a  (no sqrt)")
    print("  - sqrt(a*2)/a  = sqrt(2a)/a")
    print()
    print("Possible misreadings of (2,7):")
    print("  - sqrt(30+c)/c  (a vs c)")
    print("  - sqrt(30+a)/a  (c vs a)")
    print("  - sqrt(30*a)/c")
    print("  - sqrt(3c+a)/c")
    print("  - (30+a)/c  (no sqrt)")
    print()

    # Test each variant
    variants = {
        "(5,10) = sqrt(a+2)/c":        lambda a, b, c: math.sqrt(a + 2) / c,
        "(5,10) = sqrt(c+2)/a":        lambda a, b, c: math.sqrt(c + 2) / a,
        "(5,10) = sqrt(a+2)/b":        lambda a, b, c: math.sqrt(a + 2) / b,
        "(5,10) = (a+2)/a":            lambda a, b, c: (a + 2) / a,
        "(5,10) = sqrt(2a)/a":         lambda a, b, c: math.sqrt(2*a) / a,
        "(2,7) = sqrt(30+c)/c":        lambda a, b, c: math.sqrt(30 + c) / c,
        "(2,7) = sqrt(30+a)/a":        lambda a, b, c: math.sqrt(30 + a) / a,
        "(2,7) = sqrt(30*a)/c":        lambda a, b, c: math.sqrt(30*a) / c,
        "(2,7) = sqrt(3c+a)/c":        lambda a, b, c: math.sqrt(3*c + a) / c,
        "(2,7) = (30+a)/c":            lambda a, b, c: (30 + a) / c,
        "(2,7) = sqrt(30+a)/(c)":      lambda a, b, c: math.sqrt(30 + a) / c,  # same
    }

    for desc, func in variants.items():
        # Determine which cell to replace
        if desc.startswith("(5,10)"):
            pos = (5, 10)
        else:
            pos = (2, 7)

        variant_cells = dict(LABELED_CELLS)
        variant_cells[pos] = (desc, func)

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
                    for p, (name, f) in variant_cells.items():
                        v = safe_eval(f, a, b, c)
                        if not is_positive_integer(v):
                            all_valid = False
                            break
                    if all_valid:
                        found = True
                        print(f"  {desc}: SOLUTION a={a}, b={b}, c={c}")
                        break
        if not found:
            print(f"  {desc}: no solution")


# ============================================================
# Try fixing BOTH (5,10) and (2,7) simultaneously
# ============================================================
def try_both_fixed():
    print("\n" + "=" * 70)
    print("TESTING JOINT FIXES OF (5,10) AND (2,7)")
    print("=" * 70)

    # For (5,10): what values of a make sqrt(a+2) rational?
    # a+2 = perfect square => a = k^2 - 2
    # So a in {-1, 2, 7, 14, 23, 34, ...}
    # Positive: a in {2, 7, 14, 23, 34, 47, 62, ...}
    print("\nValues of a where sqrt(a+2) is rational (a+2 perfect square):")
    good_a = []
    for a in range(1, 100):
        s = math.sqrt(a + 2)
        if abs(s - round(s)) < 1e-9:
            good_a.append(a)
    print(f"  {good_a[:15]}")

    print("\nValues of (a,c) where sqrt(30+a)/c is a positive integer:")
    for a in good_a[:15]:
        for c in range(1, 50):
            v = math.sqrt(30 + a) / c
            if is_positive_integer(v):
                print(f"  a={a}, c={c}: sqrt({30+a})/c = {v}")

    print("\nNow checking (5,10) = sqrt(a+2)/a for these a values:")
    for a in good_a[:15]:
        v = math.sqrt(a+2) / a
        print(f"  a={a}: sqrt({a+2})/a = {v:.6f}", end="")
        if is_positive_integer(v):
            print(" INTEGER!")
        else:
            print()

    # So what if (5,10) is actually sqrt(a+2) (not divided by a)?
    print("\n\nWhat if (5,10) is just sqrt(a+2)?")
    print("Then a+2 must be a perfect square. a in {2, 7, 14, 23, 34, ...}")
    print("Combined with (2,7) = sqrt(30+a)/c:")
    for a in good_a[:15]:
        for c in range(1, 50):
            v27 = math.sqrt(30 + a) / c
            if is_positive_integer(v27):
                v510 = math.sqrt(a + 2)
                if is_positive_integer(v510):
                    print(f"  a={a}, c={c}: (5,10)=sqrt({a+2})={v510:.0f}, (2,7)=sqrt({30+a})/{c}={v27:.0f}")


if __name__ == "__main__":
    deep_constraint_analysis()
    likely_misreadings()
    try_both_fixed()
    print("\n\nNow running pair removal (may be slow)...")
    pair_removal_search()
