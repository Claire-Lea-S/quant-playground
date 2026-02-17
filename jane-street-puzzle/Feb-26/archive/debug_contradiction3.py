"""
Extended investigation: Given no pair removal works, there must be MULTIPLE
expression misreadings. Let's try deeper analyses.

Key insight from previous run: a=34, c in {1,2,4,8} makes both sqrt expressions
work IF (5,10) is sqrt(a+2) instead of sqrt(a+2)/a.

But that's too aggressive. Let's try triple removal and variant-based approaches.
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


def count_valid(cells_dict, a, b, c):
    """Count how many expressions are valid positive integers."""
    count = 0
    valid = []
    invalid = []
    for pos, (name, func) in sorted(cells_dict.items()):
        v = safe_eval(func, a, b, c)
        if is_positive_integer(v):
            count += 1
            valid.append((pos, name, int(round(v))))
        else:
            invalid.append((pos, name, v))
    return count, valid, invalid


# ============================================================
# Try all (a,b,c) combinations and find the MAXIMUM number
# of simultaneously satisfiable expressions
# ============================================================
def investigation_max_satisfiable():
    print("=" * 70)
    print("MAX SATISFIABLE EXPRESSIONS (extended search)")
    print("=" * 70)

    best_score = 0
    best_results = []

    for a in range(1, 50):
        for b in range(1, 12):
            for c in range(2, 50):
                if a == c:
                    continue
                score, valid, invalid = count_valid(LABELED_CELLS, a, b, c)
                if score > best_score:
                    best_score = score
                    best_results = [(a, b, c, valid, invalid)]
                elif score == best_score:
                    best_results.append((a, b, c, valid, invalid))

    print(f"\nMax valid expressions: {best_score}/{len(LABELED_CELLS)}")
    print(f"Number of candidates at max: {len(best_results)}")
    print(f"\nTop candidates:")
    for a, b, c, valid, invalid in best_results[:5]:
        print(f"\n  a={a}, b={b}, c={c}: {len(valid)}/{len(LABELED_CELLS)}")
        print(f"  Valid: {[(p, n, v) for p, n, v in valid]}")
        print(f"  Invalid ({len(invalid)}):")
        for pos, name, v in invalid:
            v_str = f"{v:.6f}" if v is not None else "UNDEFINED"
            print(f"    {pos} {name}: {v_str}")

    return best_results


# ============================================================
# What if multiple expressions are wrong? Try exhaustive
# replacement of the TWO critical sqrt expressions.
# ============================================================
def investigation_sqrt_variants():
    print("\n" + "=" * 70)
    print("EXHAUSTIVE SQRT EXPRESSION VARIANTS")
    print("=" * 70)

    print("\nTrying all plausible variants of BOTH (5,10) and (2,7) simultaneously:")

    variants_510 = {
        "sqrt(a+2)/a":    lambda a, b, c: math.sqrt(a + 2) / a,
        "sqrt(a+2)/c":    lambda a, b, c: math.sqrt(a + 2) / c,
        "sqrt(a+2)/b":    lambda a, b, c: math.sqrt(a + 2) / b,
        "sqrt(c+2)/a":    lambda a, b, c: math.sqrt(c + 2) / a,
        "sqrt(c+2)/c":    lambda a, b, c: math.sqrt(c + 2) / c,
        "sqrt(b+2)/a":    lambda a, b, c: math.sqrt(b + 2) / a,
        "sqrt(a*2)/a":    lambda a, b, c: math.sqrt(2*a) / a,
        "(a+2)/a":        lambda a, b, c: (a + 2) / a,
        "sqrt(a+2)":      lambda a, b, c: math.sqrt(a + 2),
        "(a+2)^2/a":      lambda a, b, c: (a + 2)**2 / a,
    }

    variants_27 = {
        "sqrt(30+a)/c":   lambda a, b, c: math.sqrt(30 + a) / c,
        "sqrt(30+c)/c":   lambda a, b, c: math.sqrt(30 + c) / c,
        "sqrt(30+a)/a":   lambda a, b, c: math.sqrt(30 + a) / a,
        "sqrt(30+c)/a":   lambda a, b, c: math.sqrt(30 + c) / a,
        "sqrt(30*a)/c":   lambda a, b, c: math.sqrt(30*a) / c,
        "sqrt(3a+c)/c":   lambda a, b, c: math.sqrt(3*a + c) / c,
        "(30+a)/c":       lambda a, b, c: (30 + a) / c,
        "sqrt(30+a)":     lambda a, b, c: math.sqrt(30 + a),
        "sqrt(30+b)/c":   lambda a, b, c: math.sqrt(30 + b) / c,
        "sqrt(3c+a)/c":   lambda a, b, c: math.sqrt(3*c + a) / c,
    }

    for name510, func510 in variants_510.items():
        for name27, func27 in variants_27.items():
            variant = dict(LABELED_CELLS)
            variant[(5, 10)] = (name510, func510)
            variant[(2, 7)] = (name27, func27)

            found = False
            for a in range(1, 40):
                if found:
                    break
                for b in range(1, 10):
                    if found:
                        break
                    for c in range(2, 40):
                        if a == c:
                            continue
                        all_valid = True
                        for pos, (name, func) in variant.items():
                            v = safe_eval(func, a, b, c)
                            if not is_positive_integer(v):
                                all_valid = False
                                break
                        if all_valid:
                            print(f"  SOLUTION with (5,10)={name510}, (2,7)={name27}: "
                                  f"a={a}, b={b}, c={c}")
                            found = True
                            break
            # Don't print negatives - too many


# ============================================================
# Which N expressions do the best candidates fail on?
# Group by failure signature.
# ============================================================
def investigation_failure_signatures():
    print("\n" + "=" * 70)
    print("FAILURE SIGNATURE ANALYSIS")
    print("=" * 70)

    # For each (a,b,c) that scores well, note which expressions fail
    # Find the most commonly failing expressions
    fail_counts = Counter()

    for a in range(1, 40):
        for b in range(1, 10):
            for c in range(2, 40):
                if a == c:
                    continue
                score, valid, invalid = count_valid(LABELED_CELLS, a, b, c)
                if score >= 19:  # Only look at good candidates
                    for pos, name, v in invalid:
                        fail_counts[pos] += 1

    print("\nMost commonly failing expressions (among candidates scoring >= 19/37):")
    for pos, count in fail_counts.most_common(20):
        name = LABELED_CELLS[pos][0]
        print(f"  {pos} {name}: fails {count} times")


# ============================================================
# Try a completely different approach: fix a=34, c=4 (from sqrt analysis)
# and see what expressions look like
# ============================================================
def investigation_a34():
    print("\n" + "=" * 70)
    print("INVESTIGATION: a=34, exploring what happens")
    print("=" * 70)

    # With a=34: sqrt(36) = 6, so (5,10) = 6/34 (not integer unless reinterpreted)
    # sqrt(64) = 8, so (2,7) = 8/c (integer when c | 8)

    for b in range(2, 8):
        for c in [2, 4, 8]:
            score, valid, invalid = count_valid(LABELED_CELLS, 34, b, c)
            if score >= 10:
                print(f"\n  a=34, b={b}, c={c}: {score}/37 valid")
                print(f"  Valid: {[(p, v) for p, _, v in valid]}")

    # What about smaller a values that make both sqrts work differently?
    print("\n\n--- Checking all a where BOTH sqrt(a+2) and sqrt(30+a) are perfect squares ---")
    for a in range(1, 1000):
        s1 = math.sqrt(a + 2)
        s2 = math.sqrt(30 + a)
        if abs(s1 - round(s1)) < 1e-9 and abs(s2 - round(s2)) < 1e-9:
            print(f"  a={a}: sqrt({a+2})={int(round(s1))}, sqrt({30+a})={int(round(s2))}")

    # a=34 is the only one in a reasonable range!
    # With a=34: sqrt(36)=6, sqrt(64)=8
    # (5,10) = 6/34 - not integer
    # (2,7) = 8/c - works for c in {1,2,4,8}

    # So if (5,10) is really sqrt(a+2) / something_else, what divisor of 6 works?
    # 6/1=6, 6/2=3, 6/3=2, 6/6=1
    # If (5,10) = sqrt(a+2)/b: 6/b integer => b in {1,2,3,6}
    # If (5,10) = sqrt(a+2)/c: 6/c integer => c in {1,2,3,6}

    print("\n\n--- a=34: what if (5,10) = sqrt(a+2)/c and (2,7) = sqrt(30+a)/c? ---")
    a = 34
    for b in range(2, 8):
        for c in [1, 2, 3, 6]:
            v510 = math.sqrt(a + 2) / c
            v27 = math.sqrt(30 + a) / c
            if is_positive_integer(v510) and is_positive_integer(v27):
                variant = dict(LABELED_CELLS)
                variant[(5, 10)] = ("sqrt(a+2)/c", lambda a, b, c: math.sqrt(a + 2) / c)
                score, valid, invalid = count_valid(variant, a, b, c)
                print(f"  a=34, b={b}, c={c}: (5,10)={v510:.0f}, (2,7)={v27:.0f}, score={score}/37")


if __name__ == "__main__":
    investigation_max_satisfiable()
    investigation_failure_signatures()
    investigation_a34()
    print("\n\nRunning exhaustive sqrt variant search (may be slow)...")
    investigation_sqrt_variants()
