"""
Comprehensive search for (a, b, c) in the Subtiles 2 puzzle.

For each candidate triple, generates plausible misreadings (variants) of every
expression, then searches for a combination (one variant per expression) where
all 37 evaluate to positive integers in [1, N] with N <= 17, subject to the
count constraint (value k appears at most k times among the 37 labeled cells).

Strategy:
- Start from proven b=2.
- Expand search: a in {2..5}, c in {2..8}, a != c.
- For each (a,b,c), for each expression, generate 10-50 plausible variants.
- Use constraint propagation: for each expression, find which variants produce
  valid positive integers in [1,17]. If any expression has zero valid variants,
  prune that (a,b,c).
- Then search for a consistent assignment (one variant per expression) satisfying
  the count constraint.
"""

import math
from itertools import product
from collections import Counter

MAX_N = 17

# ============================================================
# HELPER FUNCTIONS
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


def is_pos_int(x, tol=1e-9):
    if x is None:
        return False
    if isinstance(x, complex):
        return False
    try:
        return x > tol and abs(x - round(x)) < tol and round(x) <= MAX_N
    except (OverflowError, ValueError):
        return False


def get_int(x, tol=1e-9):
    """Return the integer value if x is a positive integer <= MAX_N, else None."""
    if is_pos_int(x, tol):
        return int(round(x))
    return None


# ============================================================
# EXPRESSION VARIANTS GENERATOR
# ============================================================
# Each expression is identified by its grid position.
# For each, we define the "original" transcription plus many plausible variants.
# Each variant is (description_string, lambda(a,b,c) -> float_or_None)

def gen_variants():
    """Return dict: position -> list of (name, func) variants."""
    V = {}

    # Helper: safe sqrt
    def ssqrt(x):
        if x < 0: return None
        return math.sqrt(x)

    # Helper: safe cbrt (real)
    def scbrt(x):
        if x >= 0:
            return x ** (1/3)
        else:
            return -((-x) ** (1/3))

    # Helper: safe log
    def slog(base, arg):
        if base is None or arg is None: return None
        if base <= 0 or base == 1 or arg <= 0: return None
        return math.log(arg) / math.log(base)

    # ---- (0,4): 6c - 4b ----
    V[(0,4)] = [
        ("6c - 4b",              lambda a,b,c: 6*c - 4*b),
        ("6c - 4a",              lambda a,b,c: 6*c - 4*a),
        ("6a - 4b",              lambda a,b,c: 6*a - 4*b),
        ("6c + 4b",              lambda a,b,c: 6*c + 4*b),
        ("6c - 46",              lambda a,b,c: 6*c - 46),
        ("6c - 4c",              lambda a,b,c: 6*c - 4*c),  # = 2c
        ("6b - 4c",              lambda a,b,c: 6*b - 4*c),
        ("6b - 4a",              lambda a,b,c: 6*b - 4*a),
        ("6c - 4",               lambda a,b,c: 6*c - 4),
        ("6c * 4b",              lambda a,b,c: 6*c * 4*b),
        ("6c - 4/b",             lambda a,b,c: 6*c - 4/b if b else None),
    ]

    # ---- (1,6): 8 - b ----
    V[(1,6)] = [
        ("8 - b",                lambda a,b,c: 8 - b),
        ("8 - a",                lambda a,b,c: 8 - a),
        ("8 - c",                lambda a,b,c: 8 - c),
        ("8 + b",                lambda a,b,c: 8 + b),
        ("8/b",                  lambda a,b,c: 8/b if b else None),
        ("8*b",                  lambda a,b,c: 8*b),
        ("8 - 6",                lambda a,b,c: 8 - 6),
        ("b - 8",                lambda a,b,c: b - 8),
    ]

    # ---- (2,1): (a^b - 4)/(6c + 1) ----
    V[(2,1)] = [
        ("(a^b-4)/(6c+1)",       lambda a,b,c: (a**b - 4)/(6*c + 1)),
        ("(a^b-4)/(6a+1)",       lambda a,b,c: (a**b - 4)/(6*a + 1)),
        ("(a^b-4)/(6c-1)",       lambda a,b,c: (a**b - 4)/(6*c - 1) if 6*c != 1 else None),
        ("(c^b-4)/(6c+1)",       lambda a,b,c: (c**b - 4)/(6*c + 1)),
        ("(a^b+4)/(6c+1)",       lambda a,b,c: (a**b + 4)/(6*c + 1)),
        ("(a^b-4)/(6c+a)",       lambda a,b,c: (a**b - 4)/(6*c + a) if 6*c+a else None),
        ("(a^c-4)/(6c+1)",       lambda a,b,c: (a**c - 4)/(6*c + 1)),
        ("(a^b-4)/(6b+1)",       lambda a,b,c: (a**b - 4)/(6*b + 1)),
        ("(a^b-4)/(bc+1)",       lambda a,b,c: (a**b - 4)/(b*c + 1)),
        ("(a^b-4)/(ac+1)",       lambda a,b,c: (a**b - 4)/(a*c + 1)),
        ("(a^b-c)/(6c+1)",       lambda a,b,c: (a**b - c)/(6*c + 1)),
        ("(a^b-4)/(6+c)",        lambda a,b,c: (a**b - 4)/(6 + c)),
        ("(a^b-4)/(6c+b)",       lambda a,b,c: (a**b - 4)/(6*c + b)),
        ("(a^2-4)/(6c+1)",       lambda a,b,c: (a**2 - 4)/(6*c + 1)),
        ("(a^b-4)/(6c)",         lambda a,b,c: (a**b - 4)/(6*c) if c else None),
    ]

    # ---- (2,3): (b+c)/(c-1) ----
    V[(2,3)] = [
        ("(b+c)/(c-1)",          lambda a,b,c: (b + c)/(c - 1) if c != 1 else None),
        ("(b+c)/(a-1)",          lambda a,b,c: (b + c)/(a - 1) if a != 1 else None),
        ("(b+a)/(c-1)",          lambda a,b,c: (b + a)/(c - 1) if c != 1 else None),
        ("(b+a)/(a-1)",          lambda a,b,c: (b + a)/(a - 1) if a != 1 else None),
        ("(a+c)/(c-1)",          lambda a,b,c: (a + c)/(c - 1) if c != 1 else None),
        ("(b+c)/(c+1)",          lambda a,b,c: (b + c)/(c + 1)),
        ("(b-c)/(c-1)",          lambda a,b,c: (b - c)/(c - 1) if c != 1 else None),
        ("(b+c)/(b-1)",          lambda a,b,c: (b + c)/(b - 1) if b != 1 else None),
        ("(b*c)/(c-1)",          lambda a,b,c: (b*c)/(c - 1) if c != 1 else None),
        ("(b+c)^2/(c-1)",        lambda a,b,c: (b + c)**2/(c - 1) if c != 1 else None),
        ("b/(c-1)",              lambda a,b,c: b/(c - 1) if c != 1 else None),
        ("c/(c-1)",              lambda a,b,c: c/(c - 1) if c != 1 else None),
    ]

    # ---- (2,5): b^2 - b/c ----
    V[(2,5)] = [
        ("b^2 - b/c",            lambda a,b,c: b**2 - b/c if c else None),
        ("b^2 - b/a",            lambda a,b,c: b**2 - b/a if a else None),
        ("b^2 - b*c",            lambda a,b,c: b**2 - b*c),
        ("b^2 + b/c",            lambda a,b,c: b**2 + b/c if c else None),
        ("b^2 - a/c",            lambda a,b,c: b**2 - a/c if c else None),
        ("b^c - b/c",            lambda a,b,c: b**c - b/c if c else None),
        ("b^2 - b*a",            lambda a,b,c: b**2 - b*a),
        ("b^2 + b*c",            lambda a,b,c: b**2 + b*c),
        ("b^2 * b/c",            lambda a,b,c: b**2 * b/c if c else None),
        ("b^2 - c/b",            lambda a,b,c: b**2 - c/b if b else None),
        ("b^2 - b",              lambda a,b,c: b**2 - b),
        ("b^2 - 6/c",            lambda a,b,c: b**2 - 6/c if c else None),
        ("b^2 + b/a",            lambda a,b,c: b**2 + b/a if a else None),
        ("b^2 - 1/c",            lambda a,b,c: b**2 - 1/c if c else None),
    ]

    # ---- (2,7): sqrt(30+a)/c ----
    # Looking at image: could be sqrt(3c+a), sqrt(30+a), sqrt(3a+c), etc.
    V[(2,7)] = [
        ("sqrt(30+a)/c",         lambda a,b,c: ssqrt(30+a)/c if c else None),
        ("sqrt(3c+a)/c",         lambda a,b,c: ssqrt(3*c+a)/c if c else None),
        ("sqrt(30+c)/c",         lambda a,b,c: ssqrt(30+c)/c if c else None),
        ("sqrt(30+a)/a",         lambda a,b,c: ssqrt(30+a)/a if a else None),
        ("sqrt(30*a)/c",         lambda a,b,c: ssqrt(30*a)/c if c else None),
        ("sqrt(3a+a)/c",         lambda a,b,c: ssqrt(3*a+a)/c if c else None),
        ("sqrt(3c+a)/a",         lambda a,b,c: ssqrt(3*c+a)/a if a else None),
        ("sqrt(30+a^2)/c",       lambda a,b,c: ssqrt(30+a**2)/c if c else None),
        ("sqrt(3a+c)/c",         lambda a,b,c: ssqrt(3*a+c)/c if c else None),
        ("sqrt(3a+c)/a",         lambda a,b,c: ssqrt(3*a+c)/a if a else None),
        ("sqrt(3c+a^2)/c",       lambda a,b,c: ssqrt(3*c+a**2)/c if c else None),
        ("sqrt(3c+c)/c",         lambda a,b,c: ssqrt(3*c+c)/c if c else None),
        ("sqrt(30-a)/c",         lambda a,b,c: ssqrt(30-a)/c if 30>a and c else None),
        ("sqrt(3c+b)/c",         lambda a,b,c: ssqrt(3*c+b)/c if c else None),
        ("sqrt(3b+a)/c",         lambda a,b,c: ssqrt(3*b+a)/c if c else None),
        ("sqrt(3c-a)/c",         lambda a,b,c: ssqrt(3*c-a)/c if 3*c>a and c else None),
        ("sqrt(30+b)/c",         lambda a,b,c: ssqrt(30+b)/c if c else None),
        ("sqrt(3c+a)/b",         lambda a,b,c: ssqrt(3*c+a)/b if b else None),
        ("sqrt(3a+b)/c",         lambda a,b,c: ssqrt(3*a+b)/c if c else None),
        ("(30+a)/c",             lambda a,b,c: (30+a)/c if c else None),
        ("(3c+a)/c",             lambda a,b,c: (3*c+a)/c if c else None),
        ("(3a+c)/c",             lambda a,b,c: (3*a+c)/c if c else None),
        ("sqrt(3c+a^2)/a",       lambda a,b,c: ssqrt(3*c+a**2)/a if a else None),
    ]

    # ---- (2,9): (a+b)/(c-3a) ----
    # Looking at image: denominator could be c-3a, c-3c (=-2c), c+3a, 3a-c, etc.
    V[(2,9)] = [
        ("(a+b)/(c-3a)",         lambda a,b,c: (a+b)/(c-3*a) if c!=3*a else None),
        ("(a+b)/(c+3a)",         lambda a,b,c: (a+b)/(c+3*a)),
        ("(a+b)/(c-3)",          lambda a,b,c: (a+b)/(c-3) if c!=3 else None),
        ("(a+b)/(3a-c)",         lambda a,b,c: (a+b)/(3*a-c) if 3*a!=c else None),
        ("(a-b)/(c-3a)",         lambda a,b,c: (a-b)/(c-3*a) if c!=3*a else None),
        ("(a+b)/(c-3c)",         lambda a,b,c: (a+b)/(c-3*c) if c else None),
        ("(a+c)/(c-3a)",         lambda a,b,c: (a+c)/(c-3*a) if c!=3*a else None),
        ("(a+b)/(c-a)",          lambda a,b,c: (a+b)/(c-a) if c!=a else None),
        ("(a+b)/(a-c)",          lambda a,b,c: (a+b)/(a-c) if a!=c else None),
        ("(a+b)/(c-3b)",         lambda a,b,c: (a+b)/(c-3*b) if c!=3*b else None),
        ("(a+b)/(3c-a)",         lambda a,b,c: (a+b)/(3*c-a) if 3*c!=a else None),
        ("(a+b)/(c*3a)",         lambda a,b,c: (a+b)/(c*3*a) if c*a else None),
        ("(a+b)/(c-3a^2)",       lambda a,b,c: (a+b)/(c-3*a**2) if c!=3*a**2 else None),
        ("(a+b)/(c^2-3a)",       lambda a,b,c: (a+b)/(c**2-3*a) if c**2!=3*a else None),
        ("(c+b)/(c-3a)",         lambda a,b,c: (c+b)/(c-3*a) if c!=3*a else None),
    ]

    # ---- (3,4): (b-3a)/(a-c) ----
    V[(3,4)] = [
        ("(b-3a)/(a-c)",         lambda a,b,c: (b-3*a)/(a-c) if a!=c else None),
        ("(b-3a)/(c-a)",         lambda a,b,c: (b-3*a)/(c-a) if c!=a else None),
        ("(b+3a)/(a-c)",         lambda a,b,c: (b+3*a)/(a-c) if a!=c else None),
        ("(b-3c)/(a-c)",         lambda a,b,c: (b-3*c)/(a-c) if a!=c else None),
        ("(b-3)/(a-c)",          lambda a,b,c: (b-3)/(a-c) if a!=c else None),
        ("(3a-b)/(a-c)",         lambda a,b,c: (3*a-b)/(a-c) if a!=c else None),
        ("(b-3a)/(a+c)",         lambda a,b,c: (b-3*a)/(a+c) if a+c else None),
        ("(b-3a)^2/(a-c)",       lambda a,b,c: (b-3*a)**2/(a-c) if a!=c else None),
        ("(b-3b)/(a-c)",         lambda a,b,c: (b-3*b)/(a-c) if a!=c else None),  # = -2b/(a-c)
        ("(b*3a)/(a-c)",         lambda a,b,c: (b*3*a)/(a-c) if a!=c else None),
        ("(b-a)/(a-c)",          lambda a,b,c: (b-a)/(a-c) if a!=c else None),
        ("(b^2-3a)/(a-c)",       lambda a,b,c: (b**2-3*a)/(a-c) if a!=c else None),
        ("(b-3a)/(a*c)",         lambda a,b,c: (b-3*a)/(a*c) if a*c else None),
        ("(b-3a^2)/(a-c)",       lambda a,b,c: (b-3*a**2)/(a-c) if a!=c else None),
    ]

    # ---- (3,6): 8a - 2b ----
    V[(3,6)] = [
        ("8a - 2b",              lambda a,b,c: 8*a - 2*b),
        ("8a - 26",              lambda a,b,c: 8*a - 26),
        ("8c - 2b",              lambda a,b,c: 8*c - 2*b),
        ("8a + 2b",              lambda a,b,c: 8*a + 2*b),
        ("8a - 2c",              lambda a,b,c: 8*a - 2*c),
        ("8b - 2a",              lambda a,b,c: 8*b - 2*a),
        ("8a - 2",               lambda a,b,c: 8*a - 2),
        ("8a * 2b",              lambda a,b,c: 8*a * 2*b),
        ("8a - b",               lambda a,b,c: 8*a - b),
        ("8a - 2b^2",            lambda a,b,c: 8*a - 2*b**2),
        ("8a^2 - 2b",            lambda a,b,c: 8*a**2 - 2*b),
        ("8a - 26",              lambda a,b,c: 8*a - 26),
    ]

    # ---- (3,8): b/(a-c) ----
    V[(3,8)] = [
        ("b/(a-c)",              lambda a,b,c: b/(a-c) if a!=c else None),
        ("b/(c-a)",              lambda a,b,c: b/(c-a) if c!=a else None),
        ("a/(a-c)",              lambda a,b,c: a/(a-c) if a!=c else None),
        ("c/(a-c)",              lambda a,b,c: c/(a-c) if a!=c else None),
        ("b/(a+c)",              lambda a,b,c: b/(a+c) if a+c else None),
        ("b/(a*c)",              lambda a,b,c: b/(a*c) if a*c else None),
        ("b^2/(a-c)",            lambda a,b,c: b**2/(a-c) if a!=c else None),
        ("2b/(a-c)",             lambda a,b,c: 2*b/(a-c) if a!=c else None),
        ("b/(a-c)^2",            lambda a,b,c: b/(a-c)**2 if a!=c else None),
    ]

    # ---- (3,10): (b+9)/sqrt(c-a) ----
    # Looking at image more carefully: could be (b+9)/sqrt(c+a), (b+a)/sqrt(c-a), etc.
    V[(3,10)] = [
        ("(b+9)/sqrt(c-a)",      lambda a,b,c: (b+9)/ssqrt(c-a) if c>a and ssqrt(c-a) else None),
        ("(b+9)/sqrt(a-c)",      lambda a,b,c: (b+9)/ssqrt(a-c) if a>c and ssqrt(a-c) else None),
        ("(b+a)/sqrt(c-a)",      lambda a,b,c: (b+a)/ssqrt(c-a) if c>a and ssqrt(c-a) else None),
        ("(b+c)/sqrt(c-a)",      lambda a,b,c: (b+c)/ssqrt(c-a) if c>a and ssqrt(c-a) else None),
        ("(b+9)/sqrt(c+a)",      lambda a,b,c: (b+9)/ssqrt(c+a) if ssqrt(c+a) else None),
        ("(b+9)/(c-a)",          lambda a,b,c: (b+9)/(c-a) if c!=a else None),
        ("(b+9)/(a-c)",          lambda a,b,c: (b+9)/(a-c) if a!=c else None),
        ("(b+a)/sqrt(a-c)",      lambda a,b,c: (b+a)/ssqrt(a-c) if a>c and ssqrt(a-c) else None),
        ("(b+c)/sqrt(a-c)",      lambda a,b,c: (b+c)/ssqrt(a-c) if a>c and ssqrt(a-c) else None),
        ("(b+9)/sqrt(c*a)",      lambda a,b,c: (b+9)/ssqrt(c*a) if c*a>0 else None),
        ("(b+9)/sqrt(c+a^2)",    lambda a,b,c: (b+9)/ssqrt(c+a**2) if ssqrt(c+a**2) else None),
        ("(b+9)/(c+a)",          lambda a,b,c: (b+9)/(c+a) if c+a else None),
        ("(b*9)/sqrt(c-a)",      lambda a,b,c: (b*9)/ssqrt(c-a) if c>a and ssqrt(c-a) else None),
        ("(b+9)/sqrt(c-a^2)",    lambda a,b,c: (b+9)/ssqrt(c-a**2) if c>a**2 else None),
        ("(b+9)^2/sqrt(c-a)",    lambda a,b,c: (b+9)**2/ssqrt(c-a) if c>a and ssqrt(c-a) else None),
    ]

    # ---- (4,1): 18/(ac+1) ----
    V[(4,1)] = [
        ("18/(ac+1)",            lambda a,b,c: 18/(a*c+1)),
        ("18/(a*c-1)",           lambda a,b,c: 18/(a*c-1) if a*c!=1 else None),
        ("18/(a+c+1)",           lambda a,b,c: 18/(a+c+1)),
        ("16/(ac+1)",            lambda a,b,c: 16/(a*c+1)),
        ("18/(a+c)",             lambda a,b,c: 18/(a+c) if a+c else None),
        ("18/(a*c)",             lambda a,b,c: 18/(a*c) if a*c else None),
        ("18/(bc+1)",            lambda a,b,c: 18/(b*c+1)),
        ("18/(ab+1)",            lambda a,b,c: 18/(a*b+1)),
        ("18/(ac+b)",            lambda a,b,c: 18/(a*c+b)),
        ("18/(ac-b)",            lambda a,b,c: 18/(a*c-b) if a*c!=b else None),
        ("1/(ac+1)",             lambda a,b,c: 1/(a*c+1)),
        ("18/(6c+1)",            lambda a,b,c: 18/(6*c+1)),
        ("18/(ac+c)",            lambda a,b,c: 18/(a*c+c) if a*c+c else None),
        ("18/(a+c-1)",           lambda a,b,c: 18/(a+c-1) if a+c!=1 else None),
        ("18/(a^c+1)",           lambda a,b,c: 18/(a**c+1)),
        ("18/(ac^2+1)",          lambda a,b,c: 18/(a*c**2+1)),
        ("18/(a^2*c+1)",         lambda a,b,c: 18/(a**2*c+1)),
        ("18/(2c+1)",            lambda a,b,c: 18/(2*c+1)),
    ]

    # ---- (4,5): c^b ----
    V[(4,5)] = [
        ("c^b",                  lambda a,b,c: c**b),
        ("c*b",                  lambda a,b,c: c*b),
        ("c+b",                  lambda a,b,c: c+b),
        ("c^a",                  lambda a,b,c: c**a),
        ("a^b",                  lambda a,b,c: a**b),
        ("b^c",                  lambda a,b,c: b**c),
        ("c^2",                  lambda a,b,c: c**2),
        ("c^3",                  lambda a,b,c: c**3),
        ("c-b",                  lambda a,b,c: c-b),
        ("c/b",                  lambda a,b,c: c/b if b else None),
        ("a^c",                  lambda a,b,c: a**c),
        ("cb",                   lambda a,b,c: c*b),
    ]

    # ---- (4,9): (3+b^2)/sqrt(3+2c) ----
    V[(4,9)] = [
        ("(3+b^2)/sqrt(3+2c)",   lambda a,b,c: (3+b**2)/ssqrt(3+2*c) if ssqrt(3+2*c) else None),
        ("(3+b^2)/sqrt(3+2a)",   lambda a,b,c: (3+b**2)/ssqrt(3+2*a) if ssqrt(3+2*a) else None),
        ("(a+b^2)/sqrt(3+2c)",   lambda a,b,c: (a+b**2)/ssqrt(3+2*c) if ssqrt(3+2*c) else None),
        ("(3+b^2)/sqrt(a+2c)",   lambda a,b,c: (3+b**2)/ssqrt(a+2*c) if ssqrt(a+2*c) else None),
        ("(3+b^2)/sqrt(3+2c^2)", lambda a,b,c: (3+b**2)/ssqrt(3+2*c**2) if ssqrt(3+2*c**2) else None),
        ("(3+b^2)/sqrt(3+c)",    lambda a,b,c: (3+b**2)/ssqrt(3+c) if ssqrt(3+c) else None),
        ("(3+b^2)/sqrt(3*2c)",   lambda a,b,c: (3+b**2)/ssqrt(3*2*c) if ssqrt(6*c) else None),
        ("(3+b^2)/(3+2c)",       lambda a,b,c: (3+b**2)/(3+2*c) if 3+2*c else None),
        ("(3+b^2)/(3+2a)",       lambda a,b,c: (3+b**2)/(3+2*a) if 3+2*a else None),
        ("(3+b^2)/sqrt(3-2c)",   lambda a,b,c: (3+b**2)/ssqrt(3-2*c) if 3>2*c and ssqrt(3-2*c) else None),
        ("(c+b^2)/sqrt(3+2c)",   lambda a,b,c: (c+b**2)/ssqrt(3+2*c) if ssqrt(3+2*c) else None),
        ("(3+a^2)/sqrt(3+2c)",   lambda a,b,c: (3+a**2)/ssqrt(3+2*c) if ssqrt(3+2*c) else None),
        ("(3+b^2)/sqrt(3+2b)",   lambda a,b,c: (3+b**2)/ssqrt(3+2*b) if ssqrt(3+2*b) else None),
        ("(3+b^2)/sqrt(b+2c)",   lambda a,b,c: (3+b**2)/ssqrt(b+2*c) if ssqrt(b+2*c) else None),
        ("(3+b^2)/sqrt(3+a*c)",  lambda a,b,c: (3+b**2)/ssqrt(3+a*c) if ssqrt(3+a*c) else None),
        ("(3+b)^2/sqrt(3+2c)",   lambda a,b,c: (3+b)**2/ssqrt(3+2*c) if ssqrt(3+2*c) else None),
    ]

    # ---- (5,3): b/(a^2-c^2) ----
    V[(5,3)] = [
        ("b/(a^2-c^2)",          lambda a,b,c: b/(a**2-c**2) if a**2!=c**2 else None),
        ("b/(c^2-a^2)",          lambda a,b,c: b/(c**2-a**2) if c**2!=a**2 else None),
        ("b/(a^2+c^2)",          lambda a,b,c: b/(a**2+c**2)),
        ("a/(a^2-c^2)",          lambda a,b,c: a/(a**2-c**2) if a**2!=c**2 else None),
        ("c/(a^2-c^2)",          lambda a,b,c: c/(a**2-c**2) if a**2!=c**2 else None),
        ("b/((a-c)^2)",          lambda a,b,c: b/((a-c)**2) if a!=c else None),
        ("b/((a+c)^2)",          lambda a,b,c: b/((a+c)**2)),
        ("b/(a-c)^2",            lambda a,b,c: b/(a-c)**2 if a!=c else None),
        ("b^2/(a^2-c^2)",        lambda a,b,c: b**2/(a**2-c**2) if a**2!=c**2 else None),
        ("b/(a^2-c)",            lambda a,b,c: b/(a**2-c) if a**2!=c else None),
        ("b/(a-c^2)",            lambda a,b,c: b/(a-c**2) if a!=c**2 else None),
        ("b/(a^2*c^2)",          lambda a,b,c: b/(a**2*c**2) if a*c else None),
        ("2b/(a^2-c^2)",         lambda a,b,c: 2*b/(a**2-c**2) if a**2!=c**2 else None),
        ("b/(a^b-c^b)",          lambda a,b,c: b/(a**b-c**b) if a**b!=c**b else None),
    ]

    # ---- (5,10): sqrt(a+2)/a ----
    V[(5,10)] = [
        ("sqrt(a+2)/a",          lambda a,b,c: ssqrt(a+2)/a if a and ssqrt(a+2) is not None else None),
        ("sqrt(a+c)/a",          lambda a,b,c: ssqrt(a+c)/a if a and ssqrt(a+c) is not None else None),
        ("sqrt(c+2)/a",          lambda a,b,c: ssqrt(c+2)/a if a and ssqrt(c+2) is not None else None),
        ("sqrt(c+2)/c",          lambda a,b,c: ssqrt(c+2)/c if c and ssqrt(c+2) is not None else None),
        ("sqrt(a+2)/c",          lambda a,b,c: ssqrt(a+2)/c if c and ssqrt(a+2) is not None else None),
        ("sqrt(a+2)*a",          lambda a,b,c: ssqrt(a+2)*a if ssqrt(a+2) is not None else None),
        ("sqrt(a^2+2)/a",        lambda a,b,c: ssqrt(a**2+2)/a if a and ssqrt(a**2+2) is not None else None),
        ("sqrt(a+b)/a",          lambda a,b,c: ssqrt(a+b)/a if a and ssqrt(a+b) is not None else None),
        ("sqrt(a+b)/c",          lambda a,b,c: ssqrt(a+b)/c if c and ssqrt(a+b) is not None else None),
        ("sqrt(a*2)/a",          lambda a,b,c: ssqrt(a*2)/a if a else None),
        ("(a+2)/a",              lambda a,b,c: (a+2)/a if a else None),
        ("sqrt(a+2)/b",          lambda a,b,c: ssqrt(a+2)/b if b and ssqrt(a+2) is not None else None),
        ("sqrt(a+2)^2/a",        lambda a,b,c: (a+2)/a if a else None),
        ("sqrt(a*c)/a",          lambda a,b,c: ssqrt(a*c)/a if a and ssqrt(a*c) is not None else None),
        ("sqrt(a+2b)/a",         lambda a,b,c: ssqrt(a+2*b)/a if a and ssqrt(a+2*b) is not None else None),
    ]

    # ---- (6,2): a^b - 12/a ----
    V[(6,2)] = [
        ("a^b - 12/a",           lambda a,b,c: a**b - 12/a if a else None),
        ("a^b - 12/c",           lambda a,b,c: a**b - 12/c if c else None),
        ("a^b + 12/a",           lambda a,b,c: a**b + 12/a if a else None),
        ("a^b - 1/(2a)",         lambda a,b,c: a**b - 1/(2*a) if a else None),
        ("a^b - 12*a",           lambda a,b,c: a**b - 12*a),
        ("c^b - 12/a",           lambda a,b,c: c**b - 12/a if a else None),
        ("a^b - b/a",            lambda a,b,c: a**b - b/a if a else None),
        ("a^b - 12+a",           lambda a,b,c: a**b - 12+a),
        ("a^b - 12/b",           lambda a,b,c: a**b - 12/b if b else None),
        ("a^b - 1/2*a",          lambda a,b,c: a**b - a/2),
        ("a^b - 12",             lambda a,b,c: a**b - 12),
        ("a^b - 2/a",            lambda a,b,c: a**b - 2/a if a else None),
        ("a^b - a/c",            lambda a,b,c: a**b - a/c if c else None),
        ("a^b + 12/c",           lambda a,b,c: a**b + 12/c if c else None),
        ("a^b - c/a",            lambda a,b,c: a**b - c/a if a else None),
        ("a^b * 12/a",           lambda a,b,c: a**b * 12/a if a else None),
        ("a^b - 1/a",            lambda a,b,c: a**b - 1/a if a else None),
    ]

    # ---- (6,4): 2c + c/a ----
    V[(6,4)] = [
        ("2c + c/a",             lambda a,b,c: 2*c + c/a if a else None),
        ("2c + a/c",             lambda a,b,c: 2*c + a/c if c else None),
        ("2c + c/b",             lambda a,b,c: 2*c + c/b if b else None),
        ("2c - c/a",             lambda a,b,c: 2*c - c/a if a else None),
        ("2c + c*a",             lambda a,b,c: 2*c + c*a),
        ("2a + c/a",             lambda a,b,c: 2*a + c/a if a else None),
        ("2c + c",               lambda a,b,c: 2*c + c),  # = 3c
        ("2a + a/c",             lambda a,b,c: 2*a + a/c if c else None),
        ("2c + a",               lambda a,b,c: 2*c + a),
        ("2c - a/c",             lambda a,b,c: 2*c - a/c if c else None),
        ("2c + b/a",             lambda a,b,c: 2*c + b/a if a else None),
        ("2c^2 + c/a",           lambda a,b,c: 2*c**2 + c/a if a else None),
        ("2c + c/a^2",           lambda a,b,c: 2*c + c/a**2 if a else None),
        ("c + c/a",              lambda a,b,c: c + c/a if a else None),
        ("2c*c/a",               lambda a,b,c: 2*c*c/a if a else None),
    ]

    # ---- (6,6): 4a - 5b ----
    V[(6,6)] = [
        ("4a - 5b",              lambda a,b,c: 4*a - 5*b),
        ("4a + 5b",              lambda a,b,c: 4*a + 5*b),
        ("4c - 5b",              lambda a,b,c: 4*c - 5*b),
        ("4a - 5c",              lambda a,b,c: 4*a - 5*c),
        ("5a - 4b",              lambda a,b,c: 5*a - 4*b),
        ("4a - 56",              lambda a,b,c: 4*a - 56),
        ("4a - 5",               lambda a,b,c: 4*a - 5),
        ("4b - 5a",              lambda a,b,c: 4*b - 5*a),
        ("4a - b",               lambda a,b,c: 4*a - b),
        ("4a*5b",                lambda a,b,c: 4*a*5*b),
        ("4a - 5/b",             lambda a,b,c: 4*a - 5/b if b else None),
        ("4a - 5b^2",            lambda a,b,c: 4*a - 5*b**2),
    ]

    # ---- (6,8): c + 2a ----
    V[(6,8)] = [
        ("c + 2a",               lambda a,b,c: c + 2*a),
        ("c + 2b",               lambda a,b,c: c + 2*b),
        ("a + 2c",               lambda a,b,c: a + 2*c),
        ("c + 2c",               lambda a,b,c: c + 2*c),  # = 3c
        ("c - 2a",               lambda a,b,c: c - 2*a),
        ("c * 2a",               lambda a,b,c: c * 2*a),
        ("c + 2",                lambda a,b,c: c + 2),
        ("c + a",                lambda a,b,c: c + a),
        ("c + 2a^2",             lambda a,b,c: c + 2*a**2),
        ("c^2 + 2a",             lambda a,b,c: c**2 + 2*a),
        ("a + 2b",               lambda a,b,c: a + 2*b),
    ]

    # ---- (6,10): b/(9a-5c) ----
    V[(6,10)] = [
        ("b/(9a-5c)",            lambda a,b,c: b/(9*a-5*c) if 9*a!=5*c else None),
        ("b/(9a+5c)",            lambda a,b,c: b/(9*a+5*c)),
        ("b/(9c-5a)",            lambda a,b,c: b/(9*c-5*a) if 9*c!=5*a else None),
        ("b/(5c-9a)",            lambda a,b,c: b/(5*c-9*a) if 5*c!=9*a else None),
        ("a/(9a-5c)",            lambda a,b,c: a/(9*a-5*c) if 9*a!=5*c else None),
        ("c/(9a-5c)",            lambda a,b,c: c/(9*a-5*c) if 9*a!=5*c else None),
        ("b/(9a-5b)",            lambda a,b,c: b/(9*a-5*b) if 9*a!=5*b else None),
        ("b/(a-5c)",             lambda a,b,c: b/(a-5*c) if a!=5*c else None),
        ("b/(9a-c)",             lambda a,b,c: b/(9*a-c) if 9*a!=c else None),
        ("b/(9a*5c)",            lambda a,b,c: b/(9*a*5*c) if a*c else None),
        ("b/(9-5c)",             lambda a,b,c: b/(9-5*c) if 9!=5*c else None),
        ("b/(9a-5)",             lambda a,b,c: b/(9*a-5) if 9*a!=5 else None),
        ("2b/(9a-5c)",           lambda a,b,c: 2*b/(9*a-5*c) if 9*a!=5*c else None),
        ("b^2/(9a-5c)",          lambda a,b,c: b**2/(9*a-5*c) if 9*a!=5*c else None),
    ]

    # ---- (7,0): (b^3+2c)/(b+2c) ----
    V[(7,0)] = [
        ("(b^3+2c)/(b+2c)",      lambda a,b,c: (b**3+2*c)/(b+2*c) if b+2*c else None),
        ("(b^3+2c)/(b+2a)",      lambda a,b,c: (b**3+2*c)/(b+2*a) if b+2*a else None),
        ("(b^2+2c)/(b+2c)",      lambda a,b,c: (b**2+2*c)/(b+2*c) if b+2*c else None),
        ("(b^3-2c)/(b-2c)",      lambda a,b,c: (b**3-2*c)/(b-2*c) if b!=2*c else None),
        ("(b^3+2a)/(b+2a)",      lambda a,b,c: (b**3+2*a)/(b+2*a) if b+2*a else None),
        ("(b^3+2c)/(b+c)",       lambda a,b,c: (b**3+2*c)/(b+c) if b+c else None),
        ("(b^3+2c)/(b*2c)",      lambda a,b,c: (b**3+2*c)/(b*2*c) if b*c else None),
        ("(b^3+c)/(b+2c)",       lambda a,b,c: (b**3+c)/(b+2*c) if b+2*c else None),
        ("(b^3+2c)/(b+2c^2)",    lambda a,b,c: (b**3+2*c)/(b+2*c**2) if b+2*c**2 else None),
        ("(b^3+2b)/(b+2c)",      lambda a,b,c: (b**3+2*b)/(b+2*c) if b+2*c else None),
        ("(a^3+2c)/(a+2c)",      lambda a,b,c: (a**3+2*c)/(a+2*c) if a+2*c else None),
        ("(b^3+2c^2)/(b+2c)",    lambda a,b,c: (b**3+2*c**2)/(b+2*c) if b+2*c else None),
    ]

    # ---- (7,8): b/(a-1) ----
    V[(7,8)] = [
        ("b/(a-1)",              lambda a,b,c: b/(a-1) if a!=1 else None),
        ("b/(c-1)",              lambda a,b,c: b/(c-1) if c!=1 else None),
        ("a/(a-1)",              lambda a,b,c: a/(a-1) if a!=1 else None),
        ("c/(a-1)",              lambda a,b,c: c/(a-1) if a!=1 else None),
        ("b/(a+1)",              lambda a,b,c: b/(a+1)),
        ("b^2/(a-1)",            lambda a,b,c: b**2/(a-1) if a!=1 else None),
        ("b/(a-c)",              lambda a,b,c: b/(a-c) if a!=c else None),
        ("b/(a-b)",              lambda a,b,c: b/(a-b) if a!=b else None),
        ("b*(a-1)",              lambda a,b,c: b*(a-1)),
        ("2b/(a-1)",             lambda a,b,c: 2*b/(a-1) if a!=1 else None),
    ]

    # ---- (8,2): (c-b)/(2a) ----
    V[(8,2)] = [
        ("(c-b)/(2a)",           lambda a,b,c: (c-b)/(2*a) if a else None),
        ("(c+b)/(2a)",           lambda a,b,c: (c+b)/(2*a) if a else None),
        ("(c-b)/(2c)",           lambda a,b,c: (c-b)/(2*c) if c else None),
        ("(a-b)/(2a)",           lambda a,b,c: (a-b)/(2*a) if a else None),
        ("(c-a)/(2a)",           lambda a,b,c: (c-a)/(2*a) if a else None),
        ("(c-b)/a",              lambda a,b,c: (c-b)/a if a else None),
        ("(b-c)/(2a)",           lambda a,b,c: (b-c)/(2*a) if a else None),
        ("(c-b)/(2b)",           lambda a,b,c: (c-b)/(2*b) if b else None),
        ("(c-b)/2a",             lambda a,b,c: (c-b)/(2*a) if a else None),
        ("(c-b)/(a+c)",          lambda a,b,c: (c-b)/(a+c) if a+c else None),
        ("(c^2-b)/(2a)",         lambda a,b,c: (c**2-b)/(2*a) if a else None),
        ("(c-b^2)/(2a)",         lambda a,b,c: (c-b**2)/(2*a) if a else None),
        ("(c-b)/(2*a)",          lambda a,b,c: (c-b)/(2*a) if a else None),
    ]

    # ---- (8,6): b/(a-c) ----
    V[(8,6)] = [
        ("b/(a-c)",              lambda a,b,c: b/(a-c) if a!=c else None),
        ("b/(c-a)",              lambda a,b,c: b/(c-a) if c!=a else None),
        ("a/(a-c)",              lambda a,b,c: a/(a-c) if a!=c else None),
        ("c/(a-c)",              lambda a,b,c: c/(a-c) if a!=c else None),
        ("b/(a+c)",              lambda a,b,c: b/(a+c) if a+c else None),
        ("b^2/(a-c)",            lambda a,b,c: b**2/(a-c) if a!=c else None),
        ("2b/(a-c)",             lambda a,b,c: 2*b/(a-c) if a!=c else None),
        ("b/(a-c)^2",            lambda a,b,c: b/(a-c)**2 if a!=c else None),
        ("b/(a*c)",              lambda a,b,c: b/(a*c) if a*c else None),
    ]

    # ---- (8,10): (b+c)/(a-c) ----
    V[(8,10)] = [
        ("(b+c)/(a-c)",          lambda a,b,c: (b+c)/(a-c) if a!=c else None),
        ("(b+c)/(c-a)",          lambda a,b,c: (b+c)/(c-a) if c!=a else None),
        ("(b-c)/(a-c)",          lambda a,b,c: (b-c)/(a-c) if a!=c else None),
        ("(b+a)/(a-c)",          lambda a,b,c: (b+a)/(a-c) if a!=c else None),
        ("(b+c)/(a+c)",          lambda a,b,c: (b+c)/(a+c) if a+c else None),
        ("(b*c)/(a-c)",          lambda a,b,c: (b*c)/(a-c) if a!=c else None),
        ("(b+c)^2/(a-c)",        lambda a,b,c: (b+c)**2/(a-c) if a!=c else None),
        ("(a+c)/(a-c)",          lambda a,b,c: (a+c)/(a-c) if a!=c else None),
        ("(b+c)/(a-b)",          lambda a,b,c: (b+c)/(a-b) if a!=b else None),
        ("(b+c)/(a*c)",          lambda a,b,c: (b+c)/(a*c) if a*c else None),
        ("(b+c)*(a-c)",          lambda a,b,c: (b+c)*(a-c)),
    ]

    # ---- (9,2): log_c(a) ----
    V[(9,2)] = [
        ("log_c(a)",             lambda a,b,c: slog(c, a)),
        ("log_a(c)",             lambda a,b,c: slog(a, c)),
        ("log_c(a^2)",           lambda a,b,c: slog(c, a**2)),
        ("log_a(c^2)",           lambda a,b,c: slog(a, c**2)),
        ("c^(1/a)",              lambda a,b,c: c**(1/a) if a else None),
        ("a^(1/c)",              lambda a,b,c: a**(1/c) if c else None),
        ("log_c(b)",             lambda a,b,c: slog(c, b)),
        ("log_b(a)",             lambda a,b,c: slog(b, a)),
        ("log_b(c)",             lambda a,b,c: slog(b, c)),
        ("log_c(a*b)",           lambda a,b,c: slog(c, a*b)),
        ("log_a(b*c)",           lambda a,b,c: slog(a, b*c)),
        ("log_c(a+b)",           lambda a,b,c: slog(c, a+b)),
        ("log_a(b)",             lambda a,b,c: slog(a, b)),
        ("a/c",                  lambda a,b,c: a/c if c else None),
        ("c/a",                  lambda a,b,c: c/a if a else None),
        ("log_2(a)",             lambda a,b,c: slog(2, a)),
        ("log_c(2a)",            lambda a,b,c: slog(c, 2*a)),
    ]

    # ---- (9,4): (c^2-b)/a ----
    V[(9,4)] = [
        ("(c^2-b)/a",            lambda a,b,c: (c**2-b)/a if a else None),
        ("(c^2-b)/c",            lambda a,b,c: (c**2-b)/c if c else None),
        ("(c^2+b)/a",            lambda a,b,c: (c**2+b)/a if a else None),
        ("(c^2-a)/a",            lambda a,b,c: (c**2-a)/a if a else None),
        ("(c^2-6)/a",            lambda a,b,c: (c**2-6)/a if a else None),
        ("(a^2-b)/c",            lambda a,b,c: (a**2-b)/c if c else None),
        ("(c^2-b)/b",            lambda a,b,c: (c**2-b)/b if b else None),
        ("(c^b-b)/a",            lambda a,b,c: (c**b-b)/a if a else None),
        ("(c^2-b)/(a+c)",        lambda a,b,c: (c**2-b)/(a+c) if a+c else None),
        ("(c^2-b)/(a-c)",        lambda a,b,c: (c**2-b)/(a-c) if a!=c else None),
        ("(c^2-b)*a",            lambda a,b,c: (c**2-b)*a),
        ("(c^2-b^2)/a",          lambda a,b,c: (c**2-b**2)/a if a else None),
        ("(c^a-b)/a",            lambda a,b,c: (c**a-b)/a if a else None),
        ("(c^2-b)/(2a)",         lambda a,b,c: (c**2-b)/(2*a) if a else None),
    ]

    # ---- (9,6): (b-1)^2 ----
    V[(9,6)] = [
        ("(b-1)^2",              lambda a,b,c: (b-1)**2),
        ("(b+1)^2",              lambda a,b,c: (b+1)**2),
        ("(b-1)^3",              lambda a,b,c: (b-1)**3),
        ("(a-1)^2",              lambda a,b,c: (a-1)**2),
        ("(c-1)^2",              lambda a,b,c: (c-1)**2),
        ("b^2-1",                lambda a,b,c: b**2-1),
        ("(b-c)^2",              lambda a,b,c: (b-c)**2),
        ("(b-a)^2",              lambda a,b,c: (b-a)**2),
        ("b-1^2",                lambda a,b,c: b-1),
        ("(b-1)*2",              lambda a,b,c: (b-1)*2),
    ]

    # ---- (9,8): cbrt(43-ac)/a ----
    # "43" could be "4b" (=8), "4^3" (=64), "4a", "4c", etc.
    V[(9,8)] = [
        ("cbrt(43-ac)/a",        lambda a,b,c: scbrt(43-a*c)/a if a else None),
        ("cbrt(43-ac)/c",        lambda a,b,c: scbrt(43-a*c)/c if c else None),
        ("cbrt(4a-ac)/a",        lambda a,b,c: scbrt(4*a-a*c)/a if a else None),
        ("cbrt(43-bc)/a",        lambda a,b,c: scbrt(43-b*c)/a if a else None),
        ("cbrt(43+ac)/a",        lambda a,b,c: scbrt(43+a*c)/a if a else None),
        ("cbrt(4b-ac)/a",        lambda a,b,c: scbrt(4*b-a*c)/a if a else None),
        ("cbrt(64-ac)/a",        lambda a,b,c: scbrt(64-a*c)/a if a else None),  # 4^3=64
        ("cbrt(4c-ac)/a",        lambda a,b,c: scbrt(4*c-a*c)/a if a else None),
        ("cbrt(43-a)/a",         lambda a,b,c: scbrt(43-a)/a if a else None),
        ("cbrt(43-ac)/(a+c)",    lambda a,b,c: scbrt(43-a*c)/(a+c) if a+c else None),
        ("cbrt(4^3-ac)/a",       lambda a,b,c: scbrt(64-a*c)/a if a else None),
        ("(43-ac)/a",            lambda a,b,c: (43-a*c)/a if a else None),
        ("cbrt(43-a*c)*a",       lambda a,b,c: scbrt(43-a*c)*a),
        ("cbrt(4^3-a*c)/a",      lambda a,b,c: scbrt(64-a*c)/a if a else None),
        ("cbrt(43-ab)/a",        lambda a,b,c: scbrt(43-a*b)/a if a else None),
        ("cbrt(43-ac)/b",        lambda a,b,c: scbrt(43-a*c)/b if b else None),
        ("cbrt(43-a^2)/a",       lambda a,b,c: scbrt(43-a**2)/a if a else None),
        ("cbrt(4*3-ac)/a",       lambda a,b,c: scbrt(12-a*c)/a if a else None),
        ("cbrt(43-2c)/a",        lambda a,b,c: scbrt(43-2*c)/a if a else None),
        ("cbrt(a*c-43)/a",       lambda a,b,c: scbrt(a*c-43)/a if a else None),
    ]

    # ---- (10,3): (b-a)/(a-c) ----
    V[(10,3)] = [
        ("(b-a)/(a-c)",          lambda a,b,c: (b-a)/(a-c) if a!=c else None),
        ("(b-a)/(c-a)",          lambda a,b,c: (b-a)/(c-a) if c!=a else None),
        ("(a-b)/(a-c)",          lambda a,b,c: (a-b)/(a-c) if a!=c else None),
        ("(b+a)/(a-c)",          lambda a,b,c: (b+a)/(a-c) if a!=c else None),
        ("(b-c)/(a-c)",          lambda a,b,c: (b-c)/(a-c) if a!=c else None),
        ("(b-a)/(a+c)",          lambda a,b,c: (b-a)/(a+c) if a+c else None),
        ("(b-a)^2/(a-c)",        lambda a,b,c: (b-a)**2/(a-c) if a!=c else None),
        ("(b-a)/(a*c)",          lambda a,b,c: (b-a)/(a*c) if a*c else None),
        ("(b*a)/(a-c)",          lambda a,b,c: (b*a)/(a-c) if a!=c else None),
        ("(b-a)/(a-c)^2",        lambda a,b,c: (b-a)/(a-c)**2 if a!=c else None),
    ]

    # ---- (10,5): 11 - b ----
    V[(10,5)] = [
        ("11 - b",               lambda a,b,c: 11 - b),
        ("11 - a",               lambda a,b,c: 11 - a),
        ("11 - c",               lambda a,b,c: 11 - c),
        ("11 + b",               lambda a,b,c: 11 + b),
        ("11/b",                 lambda a,b,c: 11/b if b else None),
        ("11*b",                 lambda a,b,c: 11*b),
        ("b - 11",               lambda a,b,c: b - 11),
        ("11 - 6",               lambda a,b,c: 11 - 6),
    ]

    # ---- (10,7): (b-2a)/(a-c) ----
    V[(10,7)] = [
        ("(b-2a)/(a-c)",         lambda a,b,c: (b-2*a)/(a-c) if a!=c else None),
        ("(b-2a)/(c-a)",         lambda a,b,c: (b-2*a)/(c-a) if c!=a else None),
        ("(b+2a)/(a-c)",         lambda a,b,c: (b+2*a)/(a-c) if a!=c else None),
        ("(b-2c)/(a-c)",         lambda a,b,c: (b-2*c)/(a-c) if a!=c else None),
        ("(2a-b)/(a-c)",         lambda a,b,c: (2*a-b)/(a-c) if a!=c else None),
        ("(b-2a)/(a+c)",         lambda a,b,c: (b-2*a)/(a+c) if a+c else None),
        ("(b-2a)^2/(a-c)",       lambda a,b,c: (b-2*a)**2/(a-c) if a!=c else None),
        ("(b-a)/(a-c)",          lambda a,b,c: (b-a)/(a-c) if a!=c else None),
        ("(b*2a)/(a-c)",         lambda a,b,c: (b*2*a)/(a-c) if a!=c else None),
        ("(2b-a)/(a-c)",         lambda a,b,c: (2*b-a)/(a-c) if a!=c else None),
        ("(b-2a)/(a*c)",         lambda a,b,c: (b-2*a)/(a*c) if a*c else None),
        ("(b-2a)/(b-c)",         lambda a,b,c: (b-2*a)/(b-c) if b!=c else None),
    ]

    # ---- (10,9): (c+3)/a ----
    V[(10,9)] = [
        ("(c+3)/a",              lambda a,b,c: (c+3)/a if a else None),
        ("(c+a)/a",              lambda a,b,c: (c+a)/a if a else None),
        ("(c+3)/c",              lambda a,b,c: (c+3)/c if c else None),
        ("(c+b)/a",              lambda a,b,c: (c+b)/a if a else None),
        ("(c^2+3)/a",            lambda a,b,c: (c**2+3)/a if a else None),
        ("(c+3)/(a+c)",          lambda a,b,c: (c+3)/(a+c) if a+c else None),
        ("(a+3)/c",              lambda a,b,c: (a+3)/c if c else None),
        ("(c+3)/b",              lambda a,b,c: (c+3)/b if b else None),
        ("(c+3)/(a-c)",          lambda a,b,c: (c+3)/(a-c) if a!=c else None),
        ("(c-3)/a",              lambda a,b,c: (c-3)/a if a else None),
        ("(c+3)*a",              lambda a,b,c: (c+3)*a),
        ("(c+a)/c",              lambda a,b,c: (c+a)/c if c else None),
        ("(c+3)/(a*c)",          lambda a,b,c: (c+3)/(a*c) if a*c else None),
        ("(c+3)/(2a)",           lambda a,b,c: (c+3)/(2*a) if a else None),
    ]

    # ---- (10,11): 8c - b/c ----
    V[(10,11)] = [
        ("8c - b/c",             lambda a,b,c: 8*c - b/c if c else None),
        ("8c + b/c",             lambda a,b,c: 8*c + b/c if c else None),
        ("8c - a/c",             lambda a,b,c: 8*c - a/c if c else None),
        ("8c - b/a",             lambda a,b,c: 8*c - b/a if a else None),
        ("8a - b/c",             lambda a,b,c: 8*a - b/c if c else None),
        ("8c - b*c",             lambda a,b,c: 8*c - b*c),
        ("8c - c/b",             lambda a,b,c: 8*c - c/b if b else None),
        ("8c + a/c",             lambda a,b,c: 8*c + a/c if c else None),
        ("8c - b",               lambda a,b,c: 8*c - b),
        ("8c/b - c",             lambda a,b,c: 8*c/b - c if b else None),
        ("8b - b/c",             lambda a,b,c: 8*b - b/c if c else None),
        ("8c^2 - b/c",           lambda a,b,c: 8*c**2 - b/c if c else None),
        ("8c - b^2/c",           lambda a,b,c: 8*c - b**2/c if c else None),
    ]

    # ---- (11,5): b^2 ----
    V[(11,5)] = [
        ("b^2",                  lambda a,b,c: b**2),
        ("b^a",                  lambda a,b,c: b**a),
        ("b^c",                  lambda a,b,c: b**c),
        ("b*2",                  lambda a,b,c: b*2),
        ("b+2",                  lambda a,b,c: b+2),
        ("b-2",                  lambda a,b,c: b-2),
        ("b^3",                  lambda a,b,c: b**3),
        ("a^2",                  lambda a,b,c: a**2),
        ("c^2",                  lambda a,b,c: c**2),
        ("2b",                   lambda a,b,c: 2*b),
    ]

    # ---- (12,8): (2^b+1)/(ac) ----
    V[(12,8)] = [
        ("(2^b+1)/(ac)",         lambda a,b,c: (2**b+1)/(a*c) if a*c else None),
        ("(2^b+1)/(a+c)",        lambda a,b,c: (2**b+1)/(a+c) if a+c else None),
        ("(2^b-1)/(ac)",         lambda a,b,c: (2**b-1)/(a*c) if a*c else None),
        ("(2^b+1)/(bc)",         lambda a,b,c: (2**b+1)/(b*c) if b*c else None),
        ("(2^a+1)/(ac)",         lambda a,b,c: (2**a+1)/(a*c) if a*c else None),
        ("(2^b+1)/ac",           lambda a,b,c: (2**b+1)/(a*c) if a*c else None),
        ("(2^b+1)/(ab)",         lambda a,b,c: (2**b+1)/(a*b) if a*b else None),
        ("(2^b+a)/(ac)",         lambda a,b,c: (2**b+a)/(a*c) if a*c else None),
        ("(2^b+c)/(ac)",         lambda a,b,c: (2**b+c)/(a*c) if a*c else None),
        ("(2^c+1)/(ac)",         lambda a,b,c: (2**c+1)/(a*c) if a*c else None),
        ("(2^b+1)/(a-c)",        lambda a,b,c: (2**b+1)/(a-c) if a!=c else None),
        ("(2^b+1)*ac",           lambda a,b,c: (2**b+1)*a*c),
        ("(2b+1)/(ac)",          lambda a,b,c: (2*b+1)/(a*c) if a*c else None),
        ("(2^b+1)/(a^2*c)",      lambda a,b,c: (2**b+1)/(a**2*c) if a*c else None),
        ("(2^b+1)/(2c)",         lambda a,b,c: (2**b+1)/(2*c) if c else None),
    ]

    return V


# ============================================================
# MAIN SEARCH
# ============================================================
def find_valid_values(variants_dict, a, b, c):
    """
    For each expression position, find which variant values are valid
    (positive integer in [1, MAX_N]).
    Returns dict: pos -> list of (variant_name, int_value)
    Returns None if any position has zero valid variants.
    """
    pos_options = {}
    for pos, variants in variants_dict.items():
        valid = []
        for vname, vfunc in variants:
            val = safe_eval(vfunc, a, b, c)
            iv = get_int(val)
            if iv is not None:
                valid.append((vname, iv))
        if not valid:
            return None  # This position can't be satisfied
        # Deduplicate by value (keep first name for each value)
        seen_vals = {}
        for vname, iv in valid:
            if iv not in seen_vals:
                seen_vals[iv] = vname
        pos_options[pos] = [(name, val) for val, name in sorted(seen_vals.items())]
    return pos_options


def check_count_constraint(value_assignment):
    """
    Check: for each value k in [1, MAX_N], the number of positions
    assigned value k must be <= k.
    """
    counts = Counter(value_assignment.values())
    for k, cnt in counts.items():
        if cnt > k:
            return False
    return True


def search_assignments(pos_options, positions, idx, current_assignment, value_counts):
    """
    Backtracking search: assign one value to each position such that
    count(k) <= k for all k.
    Returns a valid assignment dict or None.
    """
    if idx == len(positions):
        return dict(current_assignment)

    pos = positions[idx]
    for vname, val in pos_options[pos]:
        # Check if adding this value would violate count constraint
        if value_counts.get(val, 0) >= val:
            continue  # Would exceed count limit for this value

        current_assignment[pos] = (vname, val)
        value_counts[val] = value_counts.get(val, 0) + 1

        result = search_assignments(pos_options, positions, idx + 1,
                                    current_assignment, value_counts)
        if result is not None:
            return result

        del current_assignment[pos]
        value_counts[val] -= 1
        if value_counts[val] == 0:
            del value_counts[val]

    return None


def search_all_assignments(pos_options, positions, idx, current_assignment,
                           value_counts, all_results, max_results=10):
    """
    Find ALL valid assignments (up to max_results).
    """
    if len(all_results) >= max_results:
        return

    if idx == len(positions):
        all_results.append(dict(current_assignment))
        return

    pos = positions[idx]
    for vname, val in pos_options[pos]:
        if value_counts.get(val, 0) >= val:
            continue

        current_assignment[pos] = (vname, val)
        value_counts[val] = value_counts.get(val, 0) + 1

        search_all_assignments(pos_options, positions, idx + 1,
                               current_assignment, value_counts,
                               all_results, max_results)

        del current_assignment[pos]
        value_counts[val] -= 1
        if value_counts[val] == 0:
            del value_counts[val]


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 70)
    print("COMPREHENSIVE VARIANT SEARCH FOR SUBTILES 2")
    print("=" * 70)

    variants_dict = gen_variants()

    # Expanded search space
    # b is proven = 2, but let's also try b in {1, 2, 3} just in case
    b_candidates = [2]  # Almost certainly b=2 from multiple independent constraints
    a_candidates = [2, 3, 4, 5]
    c_candidates = [2, 3, 4, 5, 6, 7, 8]

    all_solutions = []
    partial_results = []

    for b_val in b_candidates:
        for a_val in a_candidates:
            for c_val in c_candidates:
                if a_val == c_val:
                    continue  # Many expressions have (a-c) in denominator

                # Find valid variant values for each position
                pos_options = find_valid_values(variants_dict, a_val, b_val, c_val)

                if pos_options is None:
                    # Count how many can be satisfied
                    count = 0
                    missing = []
                    for pos, variants in sorted(variants_dict.items()):
                        found = False
                        for vname, vfunc in variants:
                            val = safe_eval(vfunc, a_val, b_val, c_val)
                            if get_int(val) is not None:
                                found = True
                                count += 1
                                break
                        if not found:
                            missing.append(pos)
                    partial_results.append((count, a_val, b_val, c_val, missing))
                    continue

                # Count how many positions and how many options each has
                positions = sorted(pos_options.keys())
                num_positions = len(positions)
                total_combos = 1
                for pos in positions:
                    total_combos *= len(pos_options[pos])

                print(f"\n{'─'*70}")
                print(f"  Testing a={a_val}, b={b_val}, c={c_val}")
                print(f"  All {num_positions}/37 positions have at least one valid variant")
                print(f"  Total search space: {total_combos:,}")

                # Show per-position options
                for pos in positions:
                    opts = pos_options[pos]
                    vals = [v for _, v in opts]
                    print(f"    {str(pos):10s}: {len(opts)} option(s) -> values {vals}")

                # Order positions by number of options (most constrained first)
                positions_ordered = sorted(positions, key=lambda p: len(pos_options[p]))

                print(f"  Searching (most constrained first)...")
                results = []
                search_all_assignments(pos_options, positions_ordered, 0,
                                       {}, {}, results, max_results=5)

                if results:
                    for i, result in enumerate(results):
                        print(f"\n  *** SOLUTION {i+1} FOUND for a={a_val}, b={b_val}, c={c_val} ***")
                        vals = {}
                        for pos in sorted(result.keys()):
                            vname, val = result[pos]
                            vals[pos] = val
                            print(f"    {str(pos):10s} = {val:3d}  ({vname})")

                        # Verify count constraint
                        val_counts = Counter(v for _, v in result.values())
                        max_val = max(v for _, v in result.values())
                        print(f"\n    N = {max_val}")
                        print(f"    Value counts:")
                        ok = True
                        for k in sorted(val_counts.keys()):
                            cnt = val_counts[k]
                            status = "OK" if cnt <= k else "VIOLATED"
                            if cnt > k:
                                ok = False
                            print(f"      value {k:2d}: {cnt}x (limit {k}) {status}")

                        if ok:
                            print(f"\n    COUNT CONSTRAINT SATISFIED!")
                            all_solutions.append((a_val, b_val, c_val, max_val, result))
                        else:
                            print(f"\n    Count constraint VIOLATED")
                else:
                    # Debug: show what went wrong - which values are over-subscribed?
                    print(f"  No valid assignment found (count constraint too tight)")
                    # Show value demand
                    val_demand = Counter()
                    for pos in positions:
                        for _, v in pos_options[pos]:
                            pass  # just counting unique values
                    # Show min-value assignment (ignoring count constraint)
                    min_assign = {}
                    for pos in positions:
                        min_assign[pos] = pos_options[pos][0][1]  # smallest value
                    min_counts = Counter(min_assign.values())
                    print(f"    If we pick smallest value for each:")
                    for k in sorted(min_counts.keys()):
                        cnt = min_counts[k]
                        status = "OK" if cnt <= k else f"OVER by {cnt-k}"
                        print(f"      value {k:2d}: {cnt}x (limit {k}) {status}")

    # ============================================================
    # SUMMARY
    # ============================================================
    print("\n\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    if all_solutions:
        print(f"\nFound {len(all_solutions)} valid solution(s):\n")
        for i, (a_val, b_val, c_val, N, result) in enumerate(all_solutions):
            print(f"  Solution {i+1}: a={a_val}, b={b_val}, c={c_val}, N={N}")
            print(f"  Variant choices:")
            for pos in sorted(result.keys()):
                vname, val = result[pos]
                print(f"    {str(pos):10s} = {val:3d}  ({vname})")
            print()
    else:
        print("\nNo complete solutions found.")
        print("Showing best partial results...\n")

        # Combine partials from both sources
        # partial_results has (count, a, b, c, missing_positions) for cases with no pos_options
        partial_results.sort(key=lambda x: -x[0])

        print(f"  Best candidates (by #expressions individually satisfiable):")
        for score, a_val, b_val, c_val, missing in partial_results[:15]:
            print(f"\n    a={a_val}, b={b_val}, c={c_val}: {score}/37 expressions satisfiable")
            if missing:
                print(f"      UNSATISFIABLE positions: {missing}")
                # Show what values the original expressions produce
                for pos in missing:
                    variants = variants_dict[pos]
                    orig_name = variants[0][0]
                    orig_func = variants[0][1]
                    v = safe_eval(orig_func, a_val, b_val, c_val)
                    v_str = f"{v:.6f}" if v is not None else "UNDEF"
                    # Also show all variant values
                    all_vals = []
                    for vn, vf in variants:
                        vv = safe_eval(vf, a_val, b_val, c_val)
                        if vv is not None:
                            all_vals.append(f"{vn}={vv:.4f}")
                    print(f"        {pos} original: {orig_name} = {v_str}")
                    if all_vals:
                        print(f"          All variant values: {', '.join(all_vals[:8])}")


if __name__ == "__main__":
    main()
