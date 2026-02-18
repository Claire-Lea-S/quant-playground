"""
Find the correct (a, b, c) for the Subtiles 2 puzzle.

Approach:
1. From rock-solid expressions, b=2, a∈{2,3}, c∈{2,3,4}, a≠c → 4 candidates
2. For each candidate, evaluate all 37 expressions
3. Identify which expressions fail
4. For failing expressions, generate plausible misreadings
5. Search for variant combination that makes everything work
"""

import math
from itertools import product

MAX_N = 17

# ============================================================
# ALL 37 EXPRESSIONS (current transcription)
# ============================================================
EXPRESSIONS = {
    (0,4):   ("6c - 4b",              lambda a,b,c: 6*c - 4*b),
    (1,6):   ("8 - b",                lambda a,b,c: 8 - b),
    (2,1):   ("(a^b-4)/(6c+1)",       lambda a,b,c: (a**b - 4) / (6*c + 1)),
    (2,3):   ("(b+c)/(c-1)",          lambda a,b,c: (b + c) / (c - 1)),
    (2,5):   ("b^2 - b/c",            lambda a,b,c: b**2 - b / c),
    (2,7):   ("sqrt(30+a)/c",         lambda a,b,c: math.sqrt(30 + a) / c),
    (2,9):   ("(a+b)/(c-3a)",         lambda a,b,c: (a + b) / (c - 3*a)),
    (3,4):   ("(b-3a)/(a-c)",         lambda a,b,c: (b - 3*a) / (a - c)),
    (3,6):   ("8a - 2b",              lambda a,b,c: 8*a - 2*b),
    (3,8):   ("b/(a-c)",              lambda a,b,c: b / (a - c)),
    (3,10):  ("(b+9)/sqrt(c-a)",      lambda a,b,c: (b + 9) / math.sqrt(c - a) if c > a else None),
    (4,1):   ("18/(ac+1)",            lambda a,b,c: 18 / (a*c + 1)),
    (4,5):   ("c^b",                  lambda a,b,c: c**b),
    (4,9):   ("(3+b^2)/sqrt(3+2c)",   lambda a,b,c: (3 + b**2) / math.sqrt(3 + 2*c)),
    (5,3):   ("b/(a^2-c^2)",          lambda a,b,c: b / (a**2 - c**2)),
    (5,10):  ("sqrt(a+2)/a",          lambda a,b,c: math.sqrt(a + 2) / a),
    (6,2):   ("a^b - 12/a",           lambda a,b,c: a**b - 12 / a),
    (6,4):   ("2c + c/a",             lambda a,b,c: 2*c + c / a),
    (6,6):   ("4a - 5b",              lambda a,b,c: 4*a - 5*b),
    (6,8):   ("c + 2a",               lambda a,b,c: c + 2*a),
    (6,10):  ("b/(9a-5c)",            lambda a,b,c: b / (9*a - 5*c)),
    (7,0):   ("(b^3+2c)/(b+2c)",      lambda a,b,c: (b**3 + 2*c) / (b + 2*c)),
    (7,8):   ("b/(a-1)",              lambda a,b,c: b / (a - 1)),
    (8,2):   ("(c-b)/(2a)",           lambda a,b,c: (c - b) / (2*a)),
    (8,6):   ("b/(a-c)",              lambda a,b,c: b / (a - c)),
    (8,10):  ("(b+c)/(a-c)",          lambda a,b,c: (b + c) / (a - c)),
    (9,2):   ("log_c(a)",             lambda a,b,c: math.log(a) / math.log(c) if c > 0 and c != 1 else None),
    (9,4):   ("(c^2-b)/a",            lambda a,b,c: (c**2 - b) / a),
    (9,6):   ("(b-1)^2",              lambda a,b,c: (b - 1)**2),
    (9,8):   ("cbrt(43-ac)/a",        lambda a,b,c: (abs(43 - a*c)**(1/3) * (1 if 43 >= a*c else -1)) / a),
    (10,3):  ("(b-a)/(a-c)",          lambda a,b,c: (b - a) / (a - c)),
    (10,5):  ("11 - b",               lambda a,b,c: 11 - b),
    (10,7):  ("(b-2a)/(a-c)",         lambda a,b,c: (b - 2*a) / (a - c)),
    (10,9):  ("(c+3)/a",              lambda a,b,c: (c + 3) / a),
    (10,11): ("8c - b/c",             lambda a,b,c: 8*c - b / c),
    (11,5):  ("b^2",                  lambda a,b,c: b**2),
    (12,8):  ("(2^b+1)/(ac)",         lambda a,b,c: (2**b + 1) / (a*c)),
}


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


def is_pos_int(x, tol=1e-9):
    if x is None:
        return False
    if isinstance(x, complex):
        return False
    return x > tol and abs(x - round(x)) < tol and round(x) <= MAX_N


# ============================================================
# PHASE 1: Test all 4 candidates
# ============================================================
print("=" * 70)
print("PHASE 1: Testing all 4 candidate (a, b, c) triples")
print("=" * 70)

candidates = [
    (2, 2, 3),
    (2, 2, 4),
    (3, 2, 2),
    (3, 2, 4),
]

results = {}
for a, b, c in candidates:
    print(f"\n{'─'*70}")
    print(f"  a={a}, b={b}, c={c}  (a-c={a-c})")
    print(f"{'─'*70}")

    passed = []
    failed = []
    for pos, (name, func) in sorted(EXPRESSIONS.items()):
        v = safe_eval(func, a, b, c)
        ok = is_pos_int(v)
        val_str = f"{v:.4f}" if v is not None else "UNDEF"
        int_val = int(round(v)) if ok else None

        if ok:
            passed.append((pos, name, int_val))
            print(f"  ✓ {str(pos):10s} {name:28s} = {int_val:3d}")
        else:
            failed.append((pos, name, v))
            print(f"  ✗ {str(pos):10s} {name:28s} = {val_str:>10s}")

    print(f"\n  Score: {len(passed)}/{len(EXPRESSIONS)}")
    print(f"  Failing: {[p for p,_,_ in failed]}")
    results[(a,b,c)] = {"passed": passed, "failed": failed}

# ============================================================
# PHASE 2: For each candidate, show what values the passing expressions give
# ============================================================
print("\n\n" + "=" * 70)
print("PHASE 2: Value summary for each candidate")
print("=" * 70)

for (a,b,c), res in results.items():
    passed = res["passed"]
    print(f"\n  a={a}, b={b}, c={c}: {len(passed)}/37 pass")
    if passed:
        values = sorted(set(v for _,_,v in passed))
        print(f"  Distinct values: {values}")
        max_v = max(v for _,_,v in passed)
        print(f"  Max value: {max_v} (implies N ≥ {max_v})")
        from collections import Counter
        val_counts = Counter(v for _,_,v in passed)
        for v, cnt in sorted(val_counts.items()):
            feasible = "✓" if cnt <= v else "✗ TOO MANY"
            print(f"    Value {v:2d}: appears {cnt}x (need ≤ {v}) {feasible}")

# ============================================================
# PHASE 3: Generate variants for failing expressions
# ============================================================
print("\n\n" + "=" * 70)
print("PHASE 3: Variant analysis for failing expressions")
print("=" * 70)

# For each expression, define plausible variants
# Format: (name, lambda)
def make_variants(pos, original_name):
    """Generate plausible misreadings for an expression."""
    variants = []

    # The original is always a variant
    variants.append(("ORIGINAL: " + original_name, EXPRESSIONS[pos][1]))

    # Position-specific variants based on what could be misread
    if pos == (2,1):  # (a^b-4)/(6c+1)
        variants.append(("(a^b-4)/(6a+1)", lambda a,b,c: (a**b-4)/(6*a+1)))
        variants.append(("(a^b-4)/(6c-1)", lambda a,b,c: (a**b-4)/(6*c-1)))
        variants.append(("(c^b-4)/(6c+1)", lambda a,b,c: (c**b-4)/(6*c+1)))
        variants.append(("(a^b+4)/(6c+1)", lambda a,b,c: (a**b+4)/(6*c+1)))
        variants.append(("(a^b-4)/(6c+a)", lambda a,b,c: (a**b-4)/(6*c+a)))
        variants.append(("(a^c-4)/(6c+1)", lambda a,b,c: (a**c-4)/(6*c+1)))

    elif pos == (2,5):  # b^2 - b/c
        variants.append(("b^2 - b*c", lambda a,b,c: b**2 - b*c))
        variants.append(("b^2 - a/c", lambda a,b,c: b**2 - a/c))
        variants.append(("b^2 + b/c", lambda a,b,c: b**2 + b/c))
        variants.append(("b^2 - b/a", lambda a,b,c: b**2 - b/a))
        variants.append(("b^c - b/c", lambda a,b,c: b**c - b/c))

    elif pos == (2,7):  # sqrt(30+a)/c
        variants.append(("sqrt(3c+a)/c", lambda a,b,c: math.sqrt(3*c+a)/c))
        variants.append(("sqrt(30+c)/c", lambda a,b,c: math.sqrt(30+c)/c))
        variants.append(("sqrt(30+a)/a", lambda a,b,c: math.sqrt(30+a)/a))
        variants.append(("sqrt(30*a)/c", lambda a,b,c: math.sqrt(30*a)/c))
        variants.append(("sqrt(3a+a)/c", lambda a,b,c: math.sqrt(3*a+a)/c))
        variants.append(("sqrt(3c+a)/a", lambda a,b,c: math.sqrt(3*c+a)/a))
        variants.append(("sqrt(30+a²)/c", lambda a,b,c: math.sqrt(30+a**2)/c))
        variants.append(("sqrt(3a+c)/c", lambda a,b,c: math.sqrt(3*a+c)/c))
        variants.append(("sqrt(3a+c)/a", lambda a,b,c: math.sqrt(3*a+c)/a))
        variants.append(("sqrt(3c+a²)/c", lambda a,b,c: math.sqrt(3*c+a**2)/c))
        variants.append(("sqrt(3c+c)/c", lambda a,b,c: math.sqrt(3*c+c)/c))
        variants.append(("sqrt(30-a)/c", lambda a,b,c: math.sqrt(30-a)/c if 30>a else None))

    elif pos == (2,9):  # (a+b)/(c-3a)
        variants.append(("(a+b)/(c+3a)", lambda a,b,c: (a+b)/(c+3*a)))
        variants.append(("(a+b)/(c-3)", lambda a,b,c: (a+b)/(c-3) if c!=3 else None))
        variants.append(("(a+b)/(3a-c)", lambda a,b,c: (a+b)/(3*a-c) if 3*a!=c else None))
        variants.append(("(a-b)/(c-3a)", lambda a,b,c: (a-b)/(c-3*a) if c!=3*a else None))
        variants.append(("(a+b)/(c-3c)", lambda a,b,c: (a+b)/(c-3*c) if c!=0 else None))  # = (a+b)/(-2c)

    elif pos == (3,4):  # (b-3a)/(a-c)
        variants.append(("(b-3a)/(c-a)", lambda a,b,c: (b-3*a)/(c-a) if c!=a else None))
        variants.append(("(b+3a)/(a-c)", lambda a,b,c: (b+3*a)/(a-c) if a!=c else None))
        variants.append(("(b-3c)/(a-c)", lambda a,b,c: (b-3*c)/(a-c) if a!=c else None))
        variants.append(("(b-3)/(a-c)", lambda a,b,c: (b-3)/(a-c) if a!=c else None))

    elif pos == (3,6):  # 8a - 2b
        variants.append(("8a - 26", lambda a,b,c: 8*a - 26))
        variants.append(("8c - 2b", lambda a,b,c: 8*c - 2*b))
        variants.append(("8a + 2b", lambda a,b,c: 8*a + 2*b))
        variants.append(("8a - 2c", lambda a,b,c: 8*a - 2*c))

    elif pos == (3,8):  # b/(a-c)
        variants.append(("b/(c-a)", lambda a,b,c: b/(c-a) if c!=a else None))
        variants.append(("a/(a-c)", lambda a,b,c: a/(a-c) if a!=c else None))
        variants.append(("c/(a-c)", lambda a,b,c: c/(a-c) if a!=c else None))

    elif pos == (3,10):  # (b+9)/sqrt(c-a)
        variants.append(("(b+9)/sqrt(a-c)", lambda a,b,c: (b+9)/math.sqrt(a-c) if a>c else None))
        variants.append(("(b+a)/sqrt(c-a)", lambda a,b,c: (b+a)/math.sqrt(c-a) if c>a else None))
        variants.append(("(b+c)/sqrt(c-a)", lambda a,b,c: (b+c)/math.sqrt(c-a) if c>a else None))
        variants.append(("(b+9)/sqrt(c+a)", lambda a,b,c: (b+9)/math.sqrt(c+a)))

    elif pos == (4,1):  # 18/(ac+1)
        variants.append(("18/(a*c-1)", lambda a,b,c: 18/(a*c-1) if a*c!=1 else None))
        variants.append(("18/(a+c+1)", lambda a,b,c: 18/(a+c+1)))
        variants.append(("16/(ac+1)", lambda a,b,c: 16/(a*c+1)))
        variants.append(("18/(a+c)", lambda a,b,c: 18/(a+c)))
        variants.append(("18/(a*c)", lambda a,b,c: 18/(a*c)))
        variants.append(("18/(bc+1)", lambda a,b,c: 18/(b*c+1)))

    elif pos == (4,9):  # (3+b^2)/sqrt(3+2c)
        variants.append(("(3+b^2)/sqrt(3+2a)", lambda a,b,c: (3+b**2)/math.sqrt(3+2*a)))
        variants.append(("(3+b^2)/sqrt(3+2c)", lambda a,b,c: (3+b**2)/math.sqrt(3+2*c)))
        variants.append(("(a+b^2)/sqrt(3+2c)", lambda a,b,c: (a+b**2)/math.sqrt(3+2*c)))
        variants.append(("(3+b^2)/sqrt(a+2c)", lambda a,b,c: (3+b**2)/math.sqrt(a+2*c)))
        variants.append(("(3+b²)/sqrt(3+2c²)", lambda a,b,c: (3+b**2)/math.sqrt(3+2*c**2)))

    elif pos == (5,3):  # b/(a^2-c^2)
        variants.append(("b/(c^2-a^2)", lambda a,b,c: b/(c**2-a**2) if c**2!=a**2 else None))
        variants.append(("b/(a^2+c^2)", lambda a,b,c: b/(a**2+c**2)))
        variants.append(("a/(a^2-c^2)", lambda a,b,c: a/(a**2-c**2) if a**2!=c**2 else None))
        variants.append(("c/(a^2-c^2)", lambda a,b,c: c/(a**2-c**2) if a**2!=c**2 else None))

    elif pos == (5,10):  # sqrt(a+2)/a
        variants.append(("sqrt(a+c)/a", lambda a,b,c: math.sqrt(a+c)/a))
        variants.append(("sqrt(c+2)/a", lambda a,b,c: math.sqrt(c+2)/a))
        variants.append(("sqrt(c+2)/c", lambda a,b,c: math.sqrt(c+2)/c))
        variants.append(("sqrt(a+2)/c", lambda a,b,c: math.sqrt(a+2)/c))
        variants.append(("sqrt(a+2)*a", lambda a,b,c: math.sqrt(a+2)*a))
        variants.append(("sqrt(a²+2)/a", lambda a,b,c: math.sqrt(a**2+2)/a))
        variants.append(("sqrt(a+b)/a", lambda a,b,c: math.sqrt(a+b)/a))

    elif pos == (6,2):  # a^b - 12/a
        variants.append(("a^b - 12/c", lambda a,b,c: a**b - 12/c))
        variants.append(("a^b + 12/a", lambda a,b,c: a**b + 12/a))
        variants.append(("a^b - 1/2a", lambda a,b,c: a**b - 1/(2*a)))
        variants.append(("a^b - 12*a", lambda a,b,c: a**b - 12*a))
        variants.append(("c^b - 12/a", lambda a,b,c: c**b - 12/a))
        variants.append(("a^b - 1/(2a)", lambda a,b,c: a**b - 1/(2*a)))
        variants.append(("a^b - 12/c", lambda a,b,c: a**b - 12/c))
        variants.append(("a^b - b/a", lambda a,b,c: a**b - b/a))

    elif pos == (6,4):  # 2c + c/a
        variants.append(("2c + a/c", lambda a,b,c: 2*c + a/c))
        variants.append(("2c + c/b", lambda a,b,c: 2*c + c/b))
        variants.append(("2c - c/a", lambda a,b,c: 2*c - c/a))
        variants.append(("2c + c*a", lambda a,b,c: 2*c + c*a))
        variants.append(("2a + c/a", lambda a,b,c: 2*a + c/a))

    elif pos == (6,6):  # 4a - 5b
        variants.append(("4a + 5b", lambda a,b,c: 4*a + 5*b))
        variants.append(("4c - 5b", lambda a,b,c: 4*c - 5*b))
        variants.append(("4a - 5c", lambda a,b,c: 4*a - 5*c))
        variants.append(("5a - 4b", lambda a,b,c: 5*a - 4*b))
        variants.append(("4a - 56", lambda a,b,c: 4*a - 56))

    elif pos == (6,10):  # b/(9a-5c)
        variants.append(("b/(9a+5c)", lambda a,b,c: b/(9*a+5*c)))
        variants.append(("b/(9c-5a)", lambda a,b,c: b/(9*c-5*a) if 9*c!=5*a else None))
        variants.append(("b/(5c-9a)", lambda a,b,c: b/(5*c-9*a) if 5*c!=9*a else None))
        variants.append(("a/(9a-5c)", lambda a,b,c: a/(9*a-5*c) if 9*a!=5*c else None))

    elif pos == (7,0):  # (b^3+2c)/(b+2c)
        variants.append(("(b^3+2c)/(b+2a)", lambda a,b,c: (b**3+2*c)/(b+2*a)))
        variants.append(("(b^2+2c)/(b+2c)", lambda a,b,c: (b**2+2*c)/(b+2*c)))
        variants.append(("(b^3-2c)/(b-2c)", lambda a,b,c: (b**3-2*c)/(b-2*c) if b!=2*c else None))
        variants.append(("(b^3+2a)/(b+2a)", lambda a,b,c: (b**3+2*a)/(b+2*a)))
        variants.append(("(b^3+2c)/(b+2c)", lambda a,b,c: (b**3+2*c)/(b+2*c)))

    elif pos == (8,2):  # (c-b)/(2a)
        variants.append(("(c+b)/(2a)", lambda a,b,c: (c+b)/(2*a)))
        variants.append(("(c-b)/(2c)", lambda a,b,c: (c-b)/(2*c)))
        variants.append(("(a-b)/(2a)", lambda a,b,c: (a-b)/(2*a)))
        variants.append(("(c-a)/(2a)", lambda a,b,c: (c-a)/(2*a)))
        variants.append(("(c-b)/a", lambda a,b,c: (c-b)/a))

    elif pos == (8,6):  # b/(a-c)
        variants.append(("b/(c-a)", lambda a,b,c: b/(c-a) if c!=a else None))
        variants.append(("a/(a-c)", lambda a,b,c: a/(a-c) if a!=c else None))

    elif pos == (8,10):  # (b+c)/(a-c)
        variants.append(("(b+c)/(c-a)", lambda a,b,c: (b+c)/(c-a) if c!=a else None))
        variants.append(("(b-c)/(a-c)", lambda a,b,c: (b-c)/(a-c) if a!=c else None))
        variants.append(("(b+a)/(a-c)", lambda a,b,c: (b+a)/(a-c) if a!=c else None))

    elif pos == (9,2):  # log_c(a)
        variants.append(("log_a(c)", lambda a,b,c: math.log(c)/math.log(a) if a>0 and a!=1 else None))
        variants.append(("log_c(a²)", lambda a,b,c: math.log(a**2)/math.log(c) if c>0 and c!=1 else None))
        variants.append(("log_a(c²)", lambda a,b,c: math.log(c**2)/math.log(a) if a>0 and a!=1 else None))

    elif pos == (9,4):  # (c^2-b)/a
        variants.append(("(c^2-b)/c", lambda a,b,c: (c**2-b)/c))
        variants.append(("(c^2+b)/a", lambda a,b,c: (c**2+b)/a))
        variants.append(("(c^2-a)/a", lambda a,b,c: (c**2-a)/a))
        variants.append(("(c^2-6)/a", lambda a,b,c: (c**2-6)/a))
        variants.append(("(a^2-b)/c", lambda a,b,c: (a**2-b)/c))

    elif pos == (9,8):  # cbrt(43-ac)/a
        variants.append(("cbrt(43-ac)/c", lambda a,b,c: (abs(43-a*c)**(1/3)*(1 if 43>=a*c else -1))/c))
        variants.append(("cbrt(4a-ac)/a", lambda a,b,c: (abs(4*a-a*c)**(1/3)*(1 if 4*a>=a*c else -1))/a))
        variants.append(("cbrt(43-bc)/a", lambda a,b,c: (abs(43-b*c)**(1/3)*(1 if 43>=b*c else -1))/a))
        variants.append(("cbrt(43+ac)/a", lambda a,b,c: ((43+a*c)**(1/3))/a))
        variants.append(("cbrt(4b-ac)/a", lambda a,b,c: (abs(4*b-a*c)**(1/3)*(1 if 4*b>=a*c else -1))/a))
        variants.append(("cbrt(4³-ac)/a", lambda a,b,c: ((64-a*c)**(1/3))/a if 64>=a*c else None))

    elif pos == (10,3):  # (b-a)/(a-c)
        variants.append(("(b-a)/(c-a)", lambda a,b,c: (b-a)/(c-a) if c!=a else None))
        variants.append(("(a-b)/(a-c)", lambda a,b,c: (a-b)/(a-c) if a!=c else None))
        variants.append(("(b+a)/(a-c)", lambda a,b,c: (b+a)/(a-c) if a!=c else None))

    elif pos == (10,7):  # (b-2a)/(a-c)
        variants.append(("(b-2a)/(c-a)", lambda a,b,c: (b-2*a)/(c-a) if c!=a else None))
        variants.append(("(b+2a)/(a-c)", lambda a,b,c: (b+2*a)/(a-c) if a!=c else None))
        variants.append(("(b-2c)/(a-c)", lambda a,b,c: (b-2*c)/(a-c) if a!=c else None))
        variants.append(("(2a-b)/(a-c)", lambda a,b,c: (2*a-b)/(a-c) if a!=c else None))

    elif pos == (10,9):  # (c+3)/a
        variants.append(("(c+a)/a", lambda a,b,c: (c+a)/a))
        variants.append(("(c+3)/c", lambda a,b,c: (c+3)/c))
        variants.append(("(c+b)/a", lambda a,b,c: (c+b)/a))
        variants.append(("(c²+3)/a", lambda a,b,c: (c**2+3)/a))
        variants.append(("(c+3)/(a+c)", lambda a,b,c: (c+3)/(a+c)))
        variants.append(("(a+3)/c", lambda a,b,c: (a+3)/c))

    elif pos == (10,11):  # 8c - b/c
        variants.append(("8c + b/c", lambda a,b,c: 8*c + b/c))
        variants.append(("8c - a/c", lambda a,b,c: 8*c - a/c))
        variants.append(("8c - b/a", lambda a,b,c: 8*c - b/a))
        variants.append(("8a - b/c", lambda a,b,c: 8*a - b/c))
        variants.append(("8c - b*c", lambda a,b,c: 8*c - b*c))

    elif pos == (12,8):  # (2^b+1)/(ac)
        variants.append(("(2^b+1)/(a+c)", lambda a,b,c: (2**b+1)/(a+c)))
        variants.append(("(2^b+1)/(a*c)", lambda a,b,c: (2**b+1)/(a*c)))
        variants.append(("(2^b-1)/(ac)", lambda a,b,c: (2**b-1)/(a*c)))
        variants.append(("(2^b+1)/(bc)", lambda a,b,c: (2**b+1)/(b*c)))
        variants.append(("(2^a+1)/(ac)", lambda a,b,c: (2**a+1)/(a*c)))
        variants.append(("(2^b+1)/ac = (2^b+1)/(a*c)", lambda a,b,c: (2**b+1)/(a*c)))

    return variants


# ============================================================
# PHASE 3: For each candidate, test variants
# ============================================================
print("\n\n" + "=" * 70)
print("PHASE 3: Testing expression variants for each candidate")
print("=" * 70)

best_overall = (0, None, None, None)

for a, b, c in candidates:
    print(f"\n{'─'*70}")
    print(f"  Testing variants for a={a}, b={b}, c={c}")
    print(f"{'─'*70}")

    res = results[(a,b,c)]
    failing_positions = [p for p,_,_ in res["failed"]]

    # For each failing position, find which variants work
    working_variants = {}  # pos -> list of (name, value) that work

    for pos in failing_positions:
        variants = make_variants(pos, EXPRESSIONS[pos][0])
        working = []
        for vname, vfunc in variants:
            v = safe_eval(vfunc, a, b, c)
            if is_pos_int(v):
                working.append((vname, int(round(v))))
        working_variants[pos] = working

    # Count how many failing expressions can be fixed
    fixable = sum(1 for pos in failing_positions if working_variants[pos])
    unfixable = [pos for pos in failing_positions if not working_variants[pos]]

    total_score = len(res["passed"]) + fixable
    print(f"\n  Original score: {len(res['passed'])}/37")
    print(f"  Fixable failing expressions: {fixable}/{len(failing_positions)}")
    print(f"  POTENTIAL score with variants: {total_score}/37")

    if unfixable:
        print(f"\n  UNFIXABLE expressions (no variant works):")
        for pos in unfixable:
            name = EXPRESSIONS[pos][0]
            v = safe_eval(EXPRESSIONS[pos][1], a, b, c)
            v_str = f"{v:.4f}" if v is not None else "UNDEF"
            print(f"    {pos}: {name} = {v_str}")

    if fixable > 0:
        print(f"\n  Working variants for fixable expressions:")
        for pos in failing_positions:
            if working_variants[pos]:
                print(f"    {pos}:")
                for vname, vval in working_variants[pos]:
                    print(f"      {vname} = {vval}")

    if total_score > best_overall[0]:
        best_overall = (total_score, a, b, c)

print(f"\n\n{'='*70}")
print(f"BEST CANDIDATE: a={best_overall[1]}, b={best_overall[2]}, c={best_overall[3]}")
print(f"Potential score: {best_overall[0]}/37")
print(f"{'='*70}")

# ============================================================
# PHASE 4: For the best candidate, show the full picture
# ============================================================
if best_overall[0] == 37:
    a, b, c = best_overall[1], best_overall[2], best_overall[3]
    print(f"\n*** PERFECT SCORE! All 37 expressions can be satisfied! ***")
    print(f"    a={a}, b={b}, c={c}")
    # Show which variant to use for each position
elif best_overall[0] > 30:
    a, b, c = best_overall[1], best_overall[2], best_overall[3]
    print(f"\n*** VERY CLOSE ({best_overall[0]}/37)! ***")
    res = results[(a,b,c)]
    print(f"    Passing expressions: {len(res['passed'])}")
    print(f"    Failed but fixable: {best_overall[0] - len(res['passed'])}")
    failing_positions = [p for p,_,_ in res["failed"]]
    unfixable = [p for p in failing_positions if not make_variants(p, EXPRESSIONS[p][0]) or
                 not any(is_pos_int(safe_eval(vf, a, b, c)) for _, vf in make_variants(p, EXPRESSIONS[p][0]))]
    if unfixable:
        print(f"    Still unfixable: {unfixable}")
