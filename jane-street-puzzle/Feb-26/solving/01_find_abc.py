"""
Comprehensive search for (a, b, c) in the Subtiles 2 puzzle.
V3: Expanded variants for ALL forced-to-1 positions for (3,2,2).

Five positions forced to value=1 for a=3,b=2,c=2:
  (2,1), (2,7), (4,9), (5,10), (9,2)
Count constraint allows only 1 cell with value 1.
Need non-1 variants for at least 4 of these 5.

Previous work found non-1 variants for (2,7) and (4,9).
This version adds non-1 variants for (5,10) and (9,2).
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
    if is_pos_int(x, tol):
        return int(round(x))
    return None


# ============================================================
# EXPRESSION VARIANTS GENERATOR
# ============================================================
def gen_variants():
    V = {}

    def ssqrt(x):
        if x is None or x < 0: return None
        return math.sqrt(x)

    def scbrt(x):
        if x is None: return None
        if x >= 0: return x ** (1/3)
        return -((-x) ** (1/3))

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
        ("6c - 4c",              lambda a,b,c: 6*c - 4*c),
        ("6b - 4c",              lambda a,b,c: 6*b - 4*c),
        ("6b - 4a",              lambda a,b,c: 6*b - 4*a),
        ("6c - 4",               lambda a,b,c: 6*c - 4),
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
    ]

    # ---- (2,1): (a^b - 4)/(6c + 1) ----
    V[(2,1)] = [
        ("(a^b-4)/(6c+1)",       lambda a,b,c: (a**b - 4)/(6*c + 1)),
        ("(a^b-4)/(6a+1)",       lambda a,b,c: (a**b - 4)/(6*a + 1)),
        ("(a^b-4)/(6c-1)",       lambda a,b,c: (a**b - 4)/(6*c - 1) if 6*c != 1 else None),
        ("(c^b-4)/(6c+1)",       lambda a,b,c: (c**b - 4)/(6*c + 1)),
        ("(a^b+4)/(6c+1)",       lambda a,b,c: (a**b + 4)/(6*c + 1)),
        ("(a^c-4)/(6c+1)",       lambda a,b,c: (a**c - 4)/(6*c + 1)),
        ("(a^b-4)/(6b+1)",       lambda a,b,c: (a**b - 4)/(6*b + 1)),
        ("(a^b-4)/(bc+1)",       lambda a,b,c: (a**b - 4)/(b*c + 1)),
        ("(a^b-4)/(ac+1)",       lambda a,b,c: (a**b - 4)/(a*c + 1)),
        ("(a^b-c)/(6c+1)",       lambda a,b,c: (a**b - c)/(6*c + 1)),
        ("(a^b-4)/(6+c)",        lambda a,b,c: (a**b - 4)/(6 + c)),
        ("(a^b-4)/(6c+b)",       lambda a,b,c: (a**b - 4)/(6*c + b)),
        ("(a^2-4)/(6c+1)",       lambda a,b,c: (a**2 - 4)/(6*c + 1)),
        ("(a^b-4)/(6c)",         lambda a,b,c: (a**b - 4)/(6*c) if c else None),
        ("(a^b-a)/(6c+1)",       lambda a,b,c: (a**b - a)/(6*c + 1)),
        ("(a^b-b)/(6c+1)",       lambda a,b,c: (a**b - b)/(6*c + 1)),
        ("(a^b*4)/(6c+1)",       lambda a,b,c: (a**b * 4)/(6*c + 1)),
        ("(a^b-4)/(c+1)",        lambda a,b,c: (a**b - 4)/(c + 1)),
        ("(a^b-4)/(b+1)",        lambda a,b,c: (a**b - 4)/(b + 1)),
        ("(a*b-4)/(6c+1)",       lambda a,b,c: (a*b - 4)/(6*c + 1)),
        ("(a+b-4)/(6c+1)",       lambda a,b,c: (a+b - 4)/(6*c + 1)),
        ("(a^b-4)/(6c+c)",       lambda a,b,c: (a**b - 4)/(6*c + c)),
        ("(a^b-4)/(b*c+1)",      lambda a,b,c: (a**b - 4)/(b*c + 1)),
        ("(a+b)/(6c+1)",         lambda a,b,c: (a+b)/(6*c + 1)),
        ("(a*b)/(6c+1)",         lambda a,b,c: (a*b)/(6*c + 1)),
        ("(a^2-4)/(bc+1)",       lambda a,b,c: (a**2 - 4)/(b*c + 1)),
        ("(a^2-4)/(ac+1)",       lambda a,b,c: (a**2 - 4)/(a*c + 1)),
        ("(a^2+4)/(6c+1)",       lambda a,b,c: (a**2 + 4)/(6*c + 1)),
        ("(a^b-c^2)/(6c+1)",     lambda a,b,c: (a**b - c**2)/(6*c + 1)),
        ("(a^b-c)/(bc+1)",       lambda a,b,c: (a**b - c)/(b*c + 1)),
        ("(a^b-a)/(bc+1)",       lambda a,b,c: (a**b - a)/(b*c + 1)),
        ("(a^b-b)/(bc+1)",       lambda a,b,c: (a**b - b)/(b*c + 1)),
        ("(c^b-4)/(6a+1)",       lambda a,b,c: (c**b - 4)/(6*a + 1)),
        ("a^b/(6c+1)",           lambda a,b,c: a**b/(6*c + 1)),
        ("(a^b+c)/(6c+1)",       lambda a,b,c: (a**b + c)/(6*c + 1)),
        ("(a^b+a)/(6c+1)",       lambda a,b,c: (a**b + a)/(6*c + 1)),
        ("(a^b+b)/(6c+1)",       lambda a,b,c: (a**b + b)/(6*c + 1)),
        ("(a^b-4)/(b+c+1)",      lambda a,b,c: (a**b - 4)/(b+c + 1)),
        ("(a^b-4)/(a+c+1)",      lambda a,b,c: (a**b - 4)/(a+c + 1)),
        ("(a^b-4)/(a+b+1)",      lambda a,b,c: (a**b - 4)/(a+b + 1)),
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
        ("b^2 - c/b",            lambda a,b,c: b**2 - c/b if b else None),
        ("b^2 - b",              lambda a,b,c: b**2 - b),
        ("b^2 - 6/c",            lambda a,b,c: b**2 - 6/c if c else None),
        ("b^2 + b/a",            lambda a,b,c: b**2 + b/a if a else None),
        ("b^2 - 1/c",            lambda a,b,c: b**2 - 1/c if c else None),
    ]

    # ---- (2,7): sqrt(30+a)/c ----
    # For a=3,b=2,c=2: most sqrt variants give 1. Need non-1 alternatives.
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
        ("sqrt(30-a)/c",         lambda a,b,c: ssqrt(30-a)/c if 30>a and c else None),
        ("sqrt(3c+b)/c",         lambda a,b,c: ssqrt(3*c+b)/c if c else None),
        ("sqrt(3b+a)/c",         lambda a,b,c: ssqrt(3*b+a)/c if c else None),
        ("sqrt(3c-a)/c",         lambda a,b,c: ssqrt(3*c-a)/c if 3*c>a and c else None),
        ("sqrt(30+b)/c",         lambda a,b,c: ssqrt(30+b)/c if c else None),
        ("sqrt(3c+a)/b",         lambda a,b,c: ssqrt(3*c+a)/b if b else None),
        # NO-sqrt versions -- for (3,2,2) these break the value=1 logjam
        ("(30+a)/c",             lambda a,b,c: (30+a)/c if c else None),       # 33/2 no
        ("(3c+a)/c",             lambda a,b,c: (3*c+a)/c if c else None),       # 9/2 no
        ("(3a+c)/c",             lambda a,b,c: (3*a+c)/c if c else None),       # 11/2 no
        ("(30+a)/a",             lambda a,b,c: (30+a)/a if a else None),         # 11 YES
        ("(30+c)/c",             lambda a,b,c: (30+c)/c if c else None),         # 16 YES
        ("(30+c)/a",             lambda a,b,c: (30+c)/a if a else None),
        ("(30+a)/(a+c)",         lambda a,b,c: (30+a)/(a+c) if a+c else None),
        ("(3c+a)/a",             lambda a,b,c: (3*c+a)/a if a else None),        # 3 YES
        ("(3a+c)/a",             lambda a,b,c: (3*a+c)/a if a else None),
        ("(3c+a)/b",             lambda a,b,c: (3*c+a)/b if b else None),
        ("(3a+b)/c",             lambda a,b,c: (3*a+b)/c if c else None),
        ("(3c+b)/c",             lambda a,b,c: (3*c+b)/c if c else None),        # 4 YES
        ("(3c+b)/a",             lambda a,b,c: (3*c+b)/a if a else None),
        ("(3b+a)/c",             lambda a,b,c: (3*b+a)/c if c else None),
        ("(3b+c)/c",             lambda a,b,c: (3*b+c)/c if c else None),
        ("(3b+a)/a",             lambda a,b,c: (3*b+a)/a if a else None),        # 3 YES
        ("(3a+b)/a",             lambda a,b,c: (3*a+b)/a if a else None),
        ("(30+b)/a",             lambda a,b,c: (30+b)/a if a else None),
        ("(30+a*c)/c",           lambda a,b,c: (30+a*c)/c if c else None),
        ("(30-a)/c",             lambda a,b,c: (30-a)/c if c else None),
        ("(30-c)/a",             lambda a,b,c: (30-c)/a if a else None),
        ("(30-a)/a",             lambda a,b,c: (30-a)/a if a else None),         # 9 YES
        ("(30-c)/c",             lambda a,b,c: (30-c)/c if c else None),         # 14 YES
    ]

    # ---- (2,9): (a+b)/(c-3a) ----
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
        ("(b-a)/(a-c)",          lambda a,b,c: (b-a)/(a-c) if a!=c else None),
        ("(b^2-3a)/(a-c)",       lambda a,b,c: (b**2-3*a)/(a-c) if a!=c else None),
        ("(b-3a)/(a*c)",         lambda a,b,c: (b-3*a)/(a*c) if a*c else None),
        ("(b-3a^2)/(a-c)",       lambda a,b,c: (b-3*a**2)/(a-c) if a!=c else None),
    ]

    # ---- (3,6): 8a - 2b ----
    V[(3,6)] = [
        ("8a - 2b",              lambda a,b,c: 8*a - 2*b),
        ("8c - 2b",              lambda a,b,c: 8*c - 2*b),
        ("8a + 2b",              lambda a,b,c: 8*a + 2*b),
        ("8a - 2c",              lambda a,b,c: 8*a - 2*c),
        ("8b - 2a",              lambda a,b,c: 8*b - 2*a),
        ("8a - 2",               lambda a,b,c: 8*a - 2),
        ("8a - b",               lambda a,b,c: 8*a - b),
        ("8a - 2b^2",            lambda a,b,c: 8*a - 2*b**2),
        ("8a^2 - 2b",            lambda a,b,c: 8*a**2 - 2*b),
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
        ("(b+9)/(c+a)",          lambda a,b,c: (b+9)/(c+a) if c+a else None),
        ("(b+a)/sqrt(c+a)",      lambda a,b,c: (b+a)/ssqrt(c+a) if ssqrt(c+a) else None),
        ("(b+c)/sqrt(c+a)",      lambda a,b,c: (b+c)/ssqrt(c+a) if ssqrt(c+a) else None),
        ("(b+9)/cbrt(c-a)",      lambda a,b,c: (b+9)/scbrt(c-a) if c!=a and scbrt(c-a) else None),
        ("(b+9)*(c-a)",          lambda a,b,c: (b+9)*(c-a)),
        ("(b+9)*sqrt(c-a)",      lambda a,b,c: (b+9)*ssqrt(c-a) if c>a else None),
        ("(b+9)*sqrt(a-c)",      lambda a,b,c: (b+9)*ssqrt(a-c) if a>c else None),
        ("(b+1)/sqrt(c-a)",      lambda a,b,c: (b+1)/ssqrt(c-a) if c>a and ssqrt(c-a) else None),
        ("(b^2+9)/sqrt(c-a)",    lambda a,b,c: (b**2+9)/ssqrt(c-a) if c>a and ssqrt(c-a) else None),
        ("(b+9)/sqrt(a+c)",      lambda a,b,c: (b+9)/ssqrt(a+c) if ssqrt(a+c) else None),
        ("(b+9)/sqrt(c)",        lambda a,b,c: (b+9)/ssqrt(c) if ssqrt(c) else None),
        ("(b+9)/sqrt(a)",        lambda a,b,c: (b+9)/ssqrt(a) if ssqrt(a) else None),
        ("(b+9)/sqrt(ac)",       lambda a,b,c: (b+9)/ssqrt(a*c) if a*c > 0 else None),
        ("(b+9)/(c-a)^2",        lambda a,b,c: (b+9)/(c-a)**2 if c!=a else None),
        ("(b+9)/(a+c)^2",        lambda a,b,c: (b+9)/(a+c)**2 if a+c else None),
        ("(b*9)/sqrt(c+a)",      lambda a,b,c: (b*9)/ssqrt(c+a) if ssqrt(c+a) else None),
        ("(b+9)/sqrt(c^2-a)",    lambda a,b,c: (b+9)/ssqrt(c**2-a) if c**2>a else None),
        ("(b+9)/sqrt(c-a^2)",    lambda a,b,c: (b+9)/ssqrt(c-a**2) if c>a**2 else None),
        ("(b+9)/sqrt(c^2-a^2)",  lambda a,b,c: (b+9)/ssqrt(c**2-a**2) if c**2>a**2 else None),
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
        ("18/(6c+1)",            lambda a,b,c: 18/(6*c+1)),
        ("18/(a+c-1)",           lambda a,b,c: 18/(a+c-1) if a+c!=1 else None),
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
        ("c-b",                  lambda a,b,c: c-b),
        ("c/b",                  lambda a,b,c: c/b if b else None),
        ("a^c",                  lambda a,b,c: a**c),
    ]

    # ---- (4,9): (3+b^2)/sqrt(3+2c) ----
    # For (3,2,2): forced to 1 via (3+b^2)/(3+2c)=7/7=1. Need non-1 alternatives.
    V[(4,9)] = [
        ("(3+b^2)/sqrt(3+2c)",   lambda a,b,c: (3+b**2)/ssqrt(3+2*c) if ssqrt(3+2*c) else None),
        ("(3+b^2)/sqrt(3+2a)",   lambda a,b,c: (3+b**2)/ssqrt(3+2*a) if ssqrt(3+2*a) else None),
        ("(a+b^2)/sqrt(3+2c)",   lambda a,b,c: (a+b**2)/ssqrt(3+2*c) if ssqrt(3+2*c) else None),
        ("(3+b^2)/sqrt(a+2c)",   lambda a,b,c: (3+b**2)/ssqrt(a+2*c) if ssqrt(a+2*c) else None),
        ("(3+b^2)/sqrt(3+c)",    lambda a,b,c: (3+b**2)/ssqrt(3+c) if ssqrt(3+c) else None),
        ("(3+b^2)/(3+2c)",       lambda a,b,c: (3+b**2)/(3+2*c) if 3+2*c else None),
        ("(3+b^2)/(3+2a)",       lambda a,b,c: (3+b**2)/(3+2*a) if 3+2*a else None),
        ("(c+b^2)/sqrt(3+2c)",   lambda a,b,c: (c+b**2)/ssqrt(3+2*c) if ssqrt(3+2*c) else None),
        ("(3+a^2)/sqrt(3+2c)",   lambda a,b,c: (3+a**2)/ssqrt(3+2*c) if ssqrt(3+2*c) else None),
        ("(3+b^2)/sqrt(3+2b)",   lambda a,b,c: (3+b**2)/ssqrt(3+2*b) if ssqrt(3+2*b) else None),
        ("(3+b^2)/sqrt(b+2c)",   lambda a,b,c: (3+b**2)/ssqrt(b+2*c) if ssqrt(b+2*c) else None),
        ("(3+b^2)/sqrt(3+a*c)",  lambda a,b,c: (3+b**2)/ssqrt(3+a*c) if ssqrt(3+a*c) else None),
        ("(3+b)^2/sqrt(3+2c)",   lambda a,b,c: (3+b)**2/ssqrt(3+2*c) if ssqrt(3+2*c) else None),
        # NO-sqrt versions
        ("(3+b^2)/(3+c)",        lambda a,b,c: (3+b**2)/(3+c) if 3+c else None),
        ("(3+b^2)/(a+2c)",       lambda a,b,c: (3+b**2)/(a+2*c) if a+2*c else None),
        ("(3+b^2)/(b+2c)",       lambda a,b,c: (3+b**2)/(b+2*c) if b+2*c else None),
        ("(3+a^2)/(3+2c)",       lambda a,b,c: (3+a**2)/(3+2*c) if 3+2*c else None),
        ("(a+b^2)/(3+2c)",       lambda a,b,c: (a+b**2)/(3+2*c) if 3+2*c else None),
        ("(3+b^2)/(a+c)",        lambda a,b,c: (3+b**2)/(a+c) if a+c else None),
        ("(3+b^2)/a",            lambda a,b,c: (3+b**2)/a if a else None),
        ("(3+b^2)/c",            lambda a,b,c: (3+b**2)/c if c else None),
        ("(3+b^2)/b",            lambda a,b,c: (3+b**2)/b if b else None),
        ("(3+b^2)*(3+2c)",       lambda a,b,c: (3+b**2)*(3+2*c)),
        ("(a+b^2)/(a+c)",        lambda a,b,c: (a+b**2)/(a+c) if a+c else None),
        ("(a^2+b)/(3+2c)",       lambda a,b,c: (a**2+b)/(3+2*c) if 3+2*c else None),
        ("(3+b^2)/(c+1)",        lambda a,b,c: (3+b**2)/(c+1) if c+1 else None),
        # Key non-1 variants for (3,2,2): denominator = (a-c) = 1
        ("(3+b^2)/(a-c)",        lambda a,b,c: (3+b**2)/(a-c) if a!=c else None),  # 7
        ("(a+b^2)/(a-c)",        lambda a,b,c: (a+b**2)/(a-c) if a!=c else None),  # 7
        ("(3+a^2)/(a-c)",        lambda a,b,c: (3+a**2)/(a-c) if a!=c else None),  # 12
        ("(c+b^2)/(a-c)",        lambda a,b,c: (c+b**2)/(a-c) if a!=c else None),  # 6
        ("(3+b^2)/(c-a)",        lambda a,b,c: (3+b**2)/(c-a) if c!=a else None),
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
        ("b^2/(a^2-c^2)",        lambda a,b,c: b**2/(a**2-c**2) if a**2!=c**2 else None),
        ("b/(a^2-c)",            lambda a,b,c: b/(a**2-c) if a**2!=c else None),
        ("b/(a-c^2)",            lambda a,b,c: b/(a-c**2) if a!=c**2 else None),
        ("2b/(a^2-c^2)",         lambda a,b,c: 2*b/(a**2-c**2) if a**2!=c**2 else None),
        ("b/(a^b-c^b)",          lambda a,b,c: b/(a**b-c**b) if a**b!=c**b else None),
        ("b/(a^2*c^2)",          lambda a,b,c: b/(a**2*c**2) if a*c else None),
        ("b*(a^2-c^2)",          lambda a,b,c: b*(a**2-c**2)),
        ("b*(c^2-a^2)",          lambda a,b,c: b*(c**2-a**2)),
        ("b/(a^2-c*2)",          lambda a,b,c: b/(a**2-c*2) if a**2!=c*2 else None),
        ("b/(a*2-c^2)",          lambda a,b,c: b/(a*2-c**2) if a*2!=c**2 else None),
        ("b/(a^2-2c)",           lambda a,b,c: b/(a**2-2*c) if a**2!=2*c else None),
        ("b/(2a-c^2)",           lambda a,b,c: b/(2*a-c**2) if 2*a!=c**2 else None),
        ("b/(a^2-c^b)",          lambda a,b,c: b/(a**2-c**b) if a**2!=c**b else None),
        ("b/(a^b-c^2)",          lambda a,b,c: b/(a**b-c**2) if a**b!=c**2 else None),
        ("b/(a^2-c)^2",          lambda a,b,c: b/(a**2-c)**2 if a**2!=c else None),
    ]

    # ---- (5,10): sqrt(a+2)/a ----
    # For (3,2,2): all sqrt variants give 1. MUST break the value=1 logjam.
    # Key non-1 variants for (3,2,2):
    #   (a+2)*c = 5*2 = 10, (c+2)*c = 4*2 = 8, (a+2)*a = 5*3 = 15,
    #   (c+2)*a = 4*3 = 12, a+c = 5, a*c = 6, a^c = 9, c^a = 8
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
        ("(a+2)/a",              lambda a,b,c: (a+2)/a if a else None),
        ("sqrt(a+2)/b",          lambda a,b,c: ssqrt(a+2)/b if b and ssqrt(a+2) is not None else None),
        ("sqrt(a*c)/a",          lambda a,b,c: ssqrt(a*c)/a if a and ssqrt(a*c) is not None else None),
        ("sqrt(a+2b)/a",         lambda a,b,c: ssqrt(a+2*b)/a if a and ssqrt(a+2*b) is not None else None),
        ("sqrt(a+2)/a^2",        lambda a,b,c: ssqrt(a+2)/a**2 if a and ssqrt(a+2) is not None else None),
        ("sqrt(a*2)/a",          lambda a,b,c: ssqrt(a*2)/a if a else None),
        ("sqrt(a+b)/b",          lambda a,b,c: ssqrt(a+b)/b if b and ssqrt(a+b) is not None else None),
        ("sqrt(c+b)/a",          lambda a,b,c: ssqrt(c+b)/a if a and ssqrt(c+b) is not None else None),
        ("sqrt(c+b)/c",          lambda a,b,c: ssqrt(c+b)/c if c and ssqrt(c+b) is not None else None),
        # === NON-SQRT VERSIONS to break value=1 ===
        # Maybe the sqrt sign is misread, or the expression is simpler
        ("(a+2)/c",              lambda a,b,c: (a+2)/c if c else None),
        # (3,2,2): 5/2 = 2.5 no
        ("(c+2)/a",              lambda a,b,c: (c+2)/a if a else None),
        # (3,2,2): 4/3 no
        ("(a+2)*c",              lambda a,b,c: (a+2)*c),
        # (3,2,2): 5*2 = 10 YES
        ("(c+2)*c",              lambda a,b,c: (c+2)*c),
        # (3,2,2): 4*2 = 8 YES
        ("(a+2)*a",              lambda a,b,c: (a+2)*a),
        # (3,2,2): 5*3 = 15 YES
        ("(c+2)*a",              lambda a,b,c: (c+2)*a),
        # (3,2,2): 4*3 = 12 YES
        ("(a+c)/a",              lambda a,b,c: (a+c)/a if a else None),
        # (3,2,2): 5/3 no
        ("(a+c)/c",              lambda a,b,c: (a+c)/c if c else None),
        # (3,2,2): 5/2 = 2.5 no
        ("(a+b)/c",              lambda a,b,c: (a+b)/c if c else None),
        # (3,2,2): 5/2 = 2.5 no
        ("(a+b)/a",              lambda a,b,c: (a+b)/a if a else None),
        # (3,2,2): 5/3 no
        ("(a+2)/(a-c)",          lambda a,b,c: (a+2)/(a-c) if a!=c else None),
        # (3,2,2): 5/1 = 5 YES
        ("(c+2)/(a-c)",          lambda a,b,c: (c+2)/(a-c) if a!=c else None),
        # (3,2,2): 4/1 = 4 YES
        ("(a+2)/(c-1)",          lambda a,b,c: (a+2)/(c-1) if c!=1 else None),
        # (3,2,2): 5/1 = 5 YES
        ("(a+b)/(a-c)",          lambda a,b,c: (a+b)/(a-c) if a!=c else None),
        # (3,2,2): 5/1 = 5 YES
        ("(c+b)/(a-c)",          lambda a,b,c: (c+b)/(a-c) if a!=c else None),
        # (3,2,2): 4/1 = 4 YES
        ("(a-c+2)/a",            lambda a,b,c: (a-c+2)/a if a else None),
        # (3,2,2): 3/3 = 1 no (still 1)
        ("sqrt(a+2)*c",          lambda a,b,c: ssqrt(a+2)*c if ssqrt(a+2) is not None else None),
        # (3,2,2): sqrt(5)*2 ≈ 4.47 no
        ("sqrt(c+2)*a",          lambda a,b,c: ssqrt(c+2)*a if ssqrt(c+2) is not None else None),
        # (3,2,2): 2*3 = 6 YES
        ("sqrt(c+2)*c",          lambda a,b,c: ssqrt(c+2)*c if ssqrt(c+2) is not None else None),
        # (3,2,2): 2*2 = 4 YES
        ("(a+2)*(a-c)",          lambda a,b,c: (a+2)*(a-c)),
        # (3,2,2): 5*1 = 5 YES
        ("(a+2)/b",              lambda a,b,c: (a+2)/b if b else None),
        # (3,2,2): 5/2 = 2.5 no
        ("(c+2)/b",              lambda a,b,c: (c+2)/b if b else None),
        # (3,2,2): 4/2 = 2 YES
        ("(a*2)/c",              lambda a,b,c: (a*2)/c if c else None),
        # (3,2,2): 6/2 = 3 YES
        ("(c*2)/a",              lambda a,b,c: (c*2)/a if a else None),
        # (3,2,2): 4/3 no
        ("(a+2)^2/a",            lambda a,b,c: (a+2)**2/a if a else None),
        # (3,2,2): 25/3 no
        ("a^2+2",                lambda a,b,c: a**2+2),
        # (3,2,2): 11 YES
        ("c^2+2",                lambda a,b,c: c**2+2),
        # (3,2,2): 6 YES
        ("a+2+c",                lambda a,b,c: a+2+c),
        # (3,2,2): 7 YES
    ]

    # ---- (6,2): a^b - 12/a ----
    V[(6,2)] = [
        ("a^b - 12/a",           lambda a,b,c: a**b - 12/a if a else None),
        ("a^b - 12/c",           lambda a,b,c: a**b - 12/c if c else None),
        ("a^b + 12/a",           lambda a,b,c: a**b + 12/a if a else None),
        ("a^b - 12*a",           lambda a,b,c: a**b - 12*a),
        ("c^b - 12/a",           lambda a,b,c: c**b - 12/a if a else None),
        ("a^b - b/a",            lambda a,b,c: a**b - b/a if a else None),
        ("a^b - 12+a",           lambda a,b,c: a**b - 12+a),
        ("a^b - 12/b",           lambda a,b,c: a**b - 12/b if b else None),
        ("a^b - 12",             lambda a,b,c: a**b - 12),
        ("a^b - 2/a",            lambda a,b,c: a**b - 2/a if a else None),
        ("a^b - a/c",            lambda a,b,c: a**b - a/c if c else None),
        ("a^b - c/a",            lambda a,b,c: a**b - c/a if a else None),
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
        ("2c + c",               lambda a,b,c: 2*c + c),
        ("2a + a/c",             lambda a,b,c: 2*a + a/c if c else None),
        ("2c + a",               lambda a,b,c: 2*c + a),
        ("2c + b/a",             lambda a,b,c: 2*c + b/a if a else None),
        ("c + c/a",              lambda a,b,c: c + c/a if a else None),
    ]

    # ---- (6,6): 4a - 5b ----
    V[(6,6)] = [
        ("4a - 5b",              lambda a,b,c: 4*a - 5*b),
        ("4a + 5b",              lambda a,b,c: 4*a + 5*b),
        ("4c - 5b",              lambda a,b,c: 4*c - 5*b),
        ("4a - 5c",              lambda a,b,c: 4*a - 5*c),
        ("5a - 4b",              lambda a,b,c: 5*a - 4*b),
        ("4a - 5",               lambda a,b,c: 4*a - 5),
        ("4b - 5a",              lambda a,b,c: 4*b - 5*a),
        ("4a - b",               lambda a,b,c: 4*a - b),
        ("4a - 5/b",             lambda a,b,c: 4*a - 5/b if b else None),
    ]

    # ---- (6,8): c + 2a ----
    V[(6,8)] = [
        ("c + 2a",               lambda a,b,c: c + 2*a),
        ("c + 2b",               lambda a,b,c: c + 2*b),
        ("a + 2c",               lambda a,b,c: a + 2*c),
        ("c + 2c",               lambda a,b,c: c + 2*c),
        ("c - 2a",               lambda a,b,c: c - 2*a),
        ("c * 2a",               lambda a,b,c: c * 2*a),
        ("c + 2",                lambda a,b,c: c + 2),
        ("c + a",                lambda a,b,c: c + a),
        ("c + 2a^2",             lambda a,b,c: c + 2*a**2),
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
        ("b/(9-5c)",             lambda a,b,c: b/(9-5*c) if 9!=5*c else None),
        ("b/(9a-5)",             lambda a,b,c: b/(9*a-5) if 9*a!=5 else None),
        ("2b/(9a-5c)",           lambda a,b,c: 2*b/(9*a-5*c) if 9*a!=5*c else None),
        ("b^2/(9a-5c)",          lambda a,b,c: b**2/(9*a-5*c) if 9*a!=5*c else None),
        ("b/(a^2-5c)",           lambda a,b,c: b/(a**2-5*c) if a**2!=5*c else None),
        ("b/(9+a-5c)",           lambda a,b,c: b/(9+a-5*c) if 9+a!=5*c else None),
        ("b/(9a-c^2)",           lambda a,b,c: b/(9*a-c**2) if 9*a!=c**2 else None),
        ("b/(9a-(5+c))",         lambda a,b,c: b/(9*a-5-c) if 9*a!=5+c else None),
        ("b/(a-c)",              lambda a,b,c: b/(a-c) if a!=c else None),
        ("b*(9a-5c)",            lambda a,b,c: b*(9*a-5*c)),
        ("b/(9/a-5/c)",          lambda a,b,c: b/(9/a-5/c) if a and c and 9/a!=5/c else None),
        ("b/(a*c-5)",            lambda a,b,c: b/(a*c-5) if a*c!=5 else None),
        ("b/(9a-5c^2)",          lambda a,b,c: b/(9*a-5*c**2) if 9*a!=5*c**2 else None),
        ("a/(9b-5c)",            lambda a,b,c: a/(9*b-5*c) if 9*b!=5*c else None),
        ("c/(9b-5a)",            lambda a,b,c: c/(9*b-5*a) if 9*b!=5*a else None),
        ("b/(9c-5a)",            lambda a,b,c: b/(9*c-5*a) if 9*c!=5*a else None),
        ("b/(9*(a-c))",          lambda a,b,c: b/(9*(a-c)) if a!=c else None),
        ("b/((9a-5)*c)",         lambda a,b,c: b/((9*a-5)*c) if (9*a-5)*c else None),
        ("b/(9*(a-5)*c)",        lambda a,b,c: b/(9*(a-5)*c) if (a-5)*c else None),
    ]

    # ---- (7,0): (b^3+2c)/(b+2c) ----
    V[(7,0)] = [
        ("(b^3+2c)/(b+2c)",      lambda a,b,c: (b**3+2*c)/(b+2*c) if b+2*c else None),
        ("(b^3+2c)/(b+2a)",      lambda a,b,c: (b**3+2*c)/(b+2*a) if b+2*a else None),
        ("(b^2+2c)/(b+2c)",      lambda a,b,c: (b**2+2*c)/(b+2*c) if b+2*c else None),
        ("(b^3+2a)/(b+2a)",      lambda a,b,c: (b**3+2*a)/(b+2*a) if b+2*a else None),
        ("(b^3+2c)/(b+c)",       lambda a,b,c: (b**3+2*c)/(b+c) if b+c else None),
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
        ("b*(a-1)",              lambda a,b,c: b*(a-1)),
    ]

    # ---- (8,2): (c-b)/(2a) ----
    # For (3,2,2): c=b=2, so c-b=0 => fraction=0. Need non-(c-b) reading.
    V[(8,2)] = [
        ("(c-b)/(2a)",           lambda a,b,c: (c-b)/(2*a) if a else None),
        ("(c+b)/(2a)",           lambda a,b,c: (c+b)/(2*a) if a else None),
        ("(c-b)/(2c)",           lambda a,b,c: (c-b)/(2*c) if c else None),
        ("(a-b)/(2a)",           lambda a,b,c: (a-b)/(2*a) if a else None),
        ("(c-a)/(2a)",           lambda a,b,c: (c-a)/(2*a) if a else None),
        ("(c-b)/a",              lambda a,b,c: (c-b)/a if a else None),
        ("(b-c)/(2a)",           lambda a,b,c: (b-c)/(2*a) if a else None),
        ("(c-b)/(2b)",           lambda a,b,c: (c-b)/(2*b) if b else None),
        ("(c^2-b)/(2a)",         lambda a,b,c: (c**2-b)/(2*a) if a else None),
        ("(c-b^2)/(2a)",         lambda a,b,c: (c-b**2)/(2*a) if a else None),
        ("(c*b)/(2a)",           lambda a,b,c: (c*b)/(2*a) if a else None),
        ("(c/b)/(2a)",           lambda a,b,c: (c/b)/(2*a) if a and b else None),
        ("(c^b)/(2a)",           lambda a,b,c: (c**b)/(2*a) if a else None),
        ("c/(2a)",               lambda a,b,c: c/(2*a) if a else None),
        ("b/(2a)",               lambda a,b,c: b/(2*a) if a else None),
        ("(a+b)/(2a)",           lambda a,b,c: (a+b)/(2*a) if a else None),
        ("(a+c)/(2a)",           lambda a,b,c: (a+c)/(2*a) if a else None),
        ("(a+b)/(2c)",           lambda a,b,c: (a+b)/(2*c) if c else None),
        ("(a-b)/(2c)",           lambda a,b,c: (a-b)/(2*c) if c else None),
        ("(a+c)/(2c)",           lambda a,b,c: (a+c)/(2*c) if c else None),
        ("(a+c)/(2b)",           lambda a,b,c: (a+c)/(2*b) if b else None),
        ("(a-c)/(2a)",           lambda a,b,c: (a-c)/(2*a) if a else None),
        ("(a-c)/(2c)",           lambda a,b,c: (a-c)/(2*c) if c else None),
        ("(a-c)/(2b)",           lambda a,b,c: (a-c)/(2*b) if b else None),
        ("(b-a)/(2c)",           lambda a,b,c: (b-a)/(2*c) if c else None),
        ("(b-a)/(2a)",           lambda a,b,c: (b-a)/(2*a) if a else None),
        ("(b+a)/(2c)",           lambda a,b,c: (b+a)/(2*c) if c else None),
        ("(c*b)/(2+a)",          lambda a,b,c: (c*b)/(2+a)),
        ("(c+b)/(2+a)",          lambda a,b,c: (c+b)/(2+a)),
        ("(c*b)/(a+c)",          lambda a,b,c: (c*b)/(a+c) if a+c else None),
        ("(c+b)/a",              lambda a,b,c: (c+b)/a if a else None),
        ("(c+b)/c",              lambda a,b,c: (c+b)/c if c else None),
        ("(c+b)/b",              lambda a,b,c: (c+b)/b if b else None),
        # Key variants for (3,2,2) using (a-c) denominator = 1
        ("(a-b)/(a-c)",          lambda a,b,c: (a-b)/(a-c) if a!=c else None),     # 1
        ("(a+b)/(a-c)",          lambda a,b,c: (a+b)/(a-c) if a!=c else None),     # 5
        ("(c+b)/(a-c)",          lambda a,b,c: (c+b)/(a-c) if a!=c else None),     # 4
        ("(a*b)/(2a)",           lambda a,b,c: (a*b)/(2*a) if a else None),         # b/2=1
        ("(a*c)/(2a)",           lambda a,b,c: (a*c)/(2*a) if a else None),         # c/2=1
        ("(a^2-b)/(a-c)",        lambda a,b,c: (a**2-b)/(a-c) if a!=c else None),  # 7
        # Non-fraction forms
        ("c^b + 2a",             lambda a,b,c: c**b + 2*a),                         # 10
        ("c + b + 2a",           lambda a,b,c: c + b + 2*a),                        # 10
        ("c*b + 2a",             lambda a,b,c: c*b + 2*a),                          # 10
        ("c - b + 2a",           lambda a,b,c: c - b + 2*a),                        # 6
        ("c/b + 2a",             lambda a,b,c: c/b + 2*a if b else None),           # 7
        ("c^2 + 2a",             lambda a,b,c: c**2 + 2*a),                         # 10
        ("(c^2+b)/(2a)",         lambda a,b,c: (c**2+b)/(2*a) if a else None),
        ("c - b/(2a)",           lambda a,b,c: c - b/(2*a) if a else None),
        ("c + b/(2a)",           lambda a,b,c: c + b/(2*a) if a else None),
        ("c^b/(2a)",             lambda a,b,c: c**b/(2*a) if a else None),
        ("c^a/(2a)",             lambda a,b,c: c**a/(2*a) if a else None),
        ("a^b/(2a)",             lambda a,b,c: a**b/(2*a) if a else None),
        ("(a^2-b*c)/(2a)",       lambda a,b,c: (a**2-b*c)/(2*a) if a else None),
        ("a^2/(a-c)",            lambda a,b,c: a**2/(a-c) if a!=c else None),        # 9
        ("c^2/(a-c)",            lambda a,b,c: c**2/(a-c) if a!=c else None),        # 4
        ("b^2/(a-c)",            lambda a,b,c: b**2/(a-c) if a!=c else None),        # 4
        ("(c*b)/(a-c)",          lambda a,b,c: (c*b)/(a-c) if a!=c else None),       # 4
        ("(c^b)/(a-c)",          lambda a,b,c: (c**b)/(a-c) if a!=c else None),      # 4
        ("(a*b)/(a-c)",          lambda a,b,c: (a*b)/(a-c) if a!=c else None),       # 6
        ("c^(b/2)*a",            lambda a,b,c: c**(b/2)*a),                          # 6 (unlikely)
        # Simple arithmetic
        ("a - b",                lambda a,b,c: a - b),
        ("a + b",                lambda a,b,c: a + b),
        ("a * b",                lambda a,b,c: a * b),
        ("a / b",                lambda a,b,c: a / b if b else None),
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
        ("(a+c)/(a-c)",          lambda a,b,c: (a+c)/(a-c) if a!=c else None),
        ("(b+c)/(a-b)",          lambda a,b,c: (b+c)/(a-b) if a!=b else None),
        ("(b+c)/(a*c)",          lambda a,b,c: (b+c)/(a*c) if a*c else None),
        ("(b+c)*(a-c)",          lambda a,b,c: (b+c)*(a-c)),
    ]

    # ---- (9,2): log_c(a) ----
    # For (3,2,2): log_2(3) ≈ 1.585 (not integer)
    # log_c(b) = log_2(2) = 1 (forced to 1)
    # MUST break value=1 logjam with non-log variants.
    # Key non-1 values for (3,2,2):
    #   a+c=5, a*c=6, a^c=9, c^a=8, a-c=1 (no), a+b=5, a*b=6
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
        ("a/c",                  lambda a,b,c: a/c if c else None),
        ("c/a",                  lambda a,b,c: c/a if a else None),
        ("log_2(a)",             lambda a,b,c: slog(2, a)),
        ("log_c(2a)",            lambda a,b,c: slog(c, 2*a)),
        # === NON-LOG VERSIONS to break value=1 ===
        # Maybe "log" is misread or the expression is simpler
        ("a^c",                  lambda a,b,c: a**c),
        # (3,2,2): 9 YES
        ("c^a",                  lambda a,b,c: c**a),
        # (3,2,2): 8 YES
        ("a+c",                  lambda a,b,c: a+c),
        # (3,2,2): 5 YES
        ("a*c",                  lambda a,b,c: a*c),
        # (3,2,2): 6 YES
        ("a+b",                  lambda a,b,c: a+b),
        # (3,2,2): 5 YES
        ("a*b",                  lambda a,b,c: a*b),
        # (3,2,2): 6 YES
        ("a-c",                  lambda a,b,c: a-c),
        # (3,2,2): 1 (still 1, but needed for completeness)
        ("c-a",                  lambda a,b,c: c-a),
        # (3,2,2): -1 no
        ("a+b+c",                lambda a,b,c: a+b+c),
        # (3,2,2): 7 YES
        ("a*b+c",                lambda a,b,c: a*b+c),
        # (3,2,2): 8 YES
        ("a*c+b",                lambda a,b,c: a*c+b),
        # (3,2,2): 8 YES
        ("a*b*c",                lambda a,b,c: a*b*c),
        # (3,2,2): 12 YES
        ("a^2-c",                lambda a,b,c: a**2-c),
        # (3,2,2): 7 YES
        ("c^2+a",                lambda a,b,c: c**2+a),
        # (3,2,2): 7 YES
        ("a^2/c",                lambda a,b,c: a**2/c if c else None),
        # (3,2,2): 9/2 = 4.5 no
        ("c^2/a",                lambda a,b,c: c**2/a if a else None),
        # (3,2,2): 4/3 no
        ("a^2+c",                lambda a,b,c: a**2+c),
        # (3,2,2): 11 YES
        ("a^2-b",                lambda a,b,c: a**2-b),
        # (3,2,2): 7 YES
        ("(a+c)/(a-c)",          lambda a,b,c: (a+c)/(a-c) if a!=c else None),
        # (3,2,2): 5/1 = 5 YES
        ("(a*c)/(a-c)",          lambda a,b,c: (a*c)/(a-c) if a!=c else None),
        # (3,2,2): 6/1 = 6 YES
        ("log_c(a^b)",           lambda a,b,c: slog(c, a**b)),
        # (3,2,2): log_2(9) ≈ 3.17 no
        ("log_c(a)*b",           lambda a,b,c: slog(c, a)*b if slog(c, a) else None),
        # (3,2,2): 1.585*2 ≈ 3.17 no
        ("b*log_c(a)",           lambda a,b,c: b*slog(c, a) if slog(c, a) else None),
        # same as above
        # Maybe it's log_a(b^c) = log_3(4) ≈ 1.26. No.
        # log_a(c^b) = log_3(4) ≈ 1.26. No.
        # log_b(a^c) = log_2(9) ≈ 3.17. No.
        # log_b(c^a) = log_2(8) = 3. YES!
        ("log_b(c^a)",           lambda a,b,c: slog(b, c**a)),
        # (3,2,2): log_2(8) = 3 YES
        ("log_b(a^c)",           lambda a,b,c: slog(b, a**c)),
        # (3,2,2): log_2(9) ≈ 3.17 no
        # log_c(b^a) = log_2(8) = 3. YES!
        ("log_c(b^a)",           lambda a,b,c: slog(c, b**a)),
        # (3,2,2): log_2(8) = 3 YES
    ]

    # ---- (9,4): (c^2-b)/a ----
    V[(9,4)] = [
        ("(c^2-b)/a",            lambda a,b,c: (c**2-b)/a if a else None),
        ("(c^2-b)/c",            lambda a,b,c: (c**2-b)/c if c else None),
        ("(c^2+b)/a",            lambda a,b,c: (c**2+b)/a if a else None),
        ("(c^2-a)/a",            lambda a,b,c: (c**2-a)/a if a else None),
        ("(a^2-b)/c",            lambda a,b,c: (a**2-b)/c if c else None),
        ("(c^2-b)/b",            lambda a,b,c: (c**2-b)/b if b else None),
        ("(c^b-b)/a",            lambda a,b,c: (c**b-b)/a if a else None),
        ("(c^2-b)/(a+c)",        lambda a,b,c: (c**2-b)/(a+c) if a+c else None),
        ("(c^2-b)/(a-c)",        lambda a,b,c: (c**2-b)/(a-c) if a!=c else None),
        ("(c^2-b^2)/a",          lambda a,b,c: (c**2-b**2)/a if a else None),
        ("(c^2-b)/(2a)",         lambda a,b,c: (c**2-b)/(2*a) if a else None),
    ]

    # ---- (9,6): (b-1)^2 ----
    V[(9,6)] = [
        ("(b-1)^2",              lambda a,b,c: (b-1)**2),
        ("(b+1)^2",              lambda a,b,c: (b+1)**2),
        ("(a-1)^2",              lambda a,b,c: (a-1)**2),
        ("(c-1)^2",              lambda a,b,c: (c-1)**2),
        ("b^2-1",                lambda a,b,c: b**2-1),
        ("(b-c)^2",              lambda a,b,c: (b-c)**2),
        ("(b-a)^2",              lambda a,b,c: (b-a)**2),
        ("(b-1)*2",              lambda a,b,c: (b-1)*2),
    ]

    # ---- (9,8): cbrt(43-ac)/a ----
    # Key discovery: "43" is actually "4*3" = 12, giving (12-ac)/a
    V[(9,8)] = [
        ("cbrt(43-ac)/a",        lambda a,b,c: scbrt(43-a*c)/a if a else None),
        ("(12-ac)/a",            lambda a,b,c: (12-a*c)/a if a else None),
        # (3,2,2): (12-6)/3 = 2. YES!
        # (2,2,3): (12-6)/2 = 3. YES!
        ("(12-ac)/c",            lambda a,b,c: (12-a*c)/c if c else None),
        ("(12+ac)/a",            lambda a,b,c: (12+a*c)/a if a else None),
        ("(12-bc)/a",            lambda a,b,c: (12-b*c)/a if a else None),
        ("(12-ac)/b",            lambda a,b,c: (12-a*c)/b if b else None),
        ("(43-ac)/a",            lambda a,b,c: (43-a*c)/a if a else None),
        ("(64-ac)/a",            lambda a,b,c: (64-a*c)/a if a else None),
        ("cbrt(43-ac)/c",        lambda a,b,c: scbrt(43-a*c)/c if c else None),
        ("cbrt(33-ac)/a",        lambda a,b,c: scbrt(33-a*c)/a if a else None),
        ("cbrt(14-ac)/a",        lambda a,b,c: scbrt(14-a*c)/a if a else None),
        ("(13-ac)/a",            lambda a,b,c: (13-a*c)/a if a else None),
        ("(11-ac)/a",            lambda a,b,c: (11-a*c)/a if a else None),
        ("(14-ac)/a",            lambda a,b,c: (14-a*c)/a if a else None),
        ("(10-ac)/a",            lambda a,b,c: (10-a*c)/a if a else None),
        ("sqrt(43-ac)/a",        lambda a,b,c: ssqrt(43-a*c)/a if 43>a*c and a else None),
        ("cbrt(43-ac)*a",        lambda a,b,c: scbrt(43-a*c)*a),
    ]

    # ---- (10,3): (b-a)/(a-c) ----
    V[(10,3)] = [
        ("(b-a)/(a-c)",          lambda a,b,c: (b-a)/(a-c) if a!=c else None),
        ("(b-a)/(c-a)",          lambda a,b,c: (b-a)/(c-a) if c!=a else None),
        ("(a-b)/(a-c)",          lambda a,b,c: (a-b)/(a-c) if a!=c else None),
        ("(b+a)/(a-c)",          lambda a,b,c: (b+a)/(a-c) if a!=c else None),
        ("(b-c)/(a-c)",          lambda a,b,c: (b-c)/(a-c) if a!=c else None),
        ("(b-a)/(a+c)",          lambda a,b,c: (b-a)/(a+c) if a+c else None),
        ("(b-a)/(a*c)",          lambda a,b,c: (b-a)/(a*c) if a*c else None),
        ("(b*a)/(a-c)",          lambda a,b,c: (b*a)/(a-c) if a!=c else None),
    ]

    # ---- (10,5): 11 - b ----
    V[(10,5)] = [
        ("11 - b",               lambda a,b,c: 11 - b),
        ("11 - a",               lambda a,b,c: 11 - a),
        ("11 - c",               lambda a,b,c: 11 - c),
        ("11 + b",               lambda a,b,c: 11 + b),
        ("11/b",                 lambda a,b,c: 11/b if b else None),
        ("11*b",                 lambda a,b,c: 11*b),
    ]

    # ---- (10,7): (b-2a)/(a-c) ----
    V[(10,7)] = [
        ("(b-2a)/(a-c)",         lambda a,b,c: (b-2*a)/(a-c) if a!=c else None),
        ("(b-2a)/(c-a)",         lambda a,b,c: (b-2*a)/(c-a) if c!=a else None),
        ("(b+2a)/(a-c)",         lambda a,b,c: (b+2*a)/(a-c) if a!=c else None),
        ("(b-2c)/(a-c)",         lambda a,b,c: (b-2*c)/(a-c) if a!=c else None),
        ("(2a-b)/(a-c)",         lambda a,b,c: (2*a-b)/(a-c) if a!=c else None),
        ("(b-2a)/(a+c)",         lambda a,b,c: (b-2*a)/(a+c) if a+c else None),
        ("(b-a)/(a-c)",          lambda a,b,c: (b-a)/(a-c) if a!=c else None),
        ("(2b-a)/(a-c)",         lambda a,b,c: (2*b-a)/(a-c) if a!=c else None),
        ("(b-2a)/(a*c)",         lambda a,b,c: (b-2*a)/(a*c) if a*c else None),
    ]

    # ---- (10,9): (c+3)/a ----
    V[(10,9)] = [
        ("(c+3)/a",              lambda a,b,c: (c+3)/a if a else None),
        ("(c+a)/a",              lambda a,b,c: (c+a)/a if a else None),
        ("(c+3)/c",              lambda a,b,c: (c+3)/c if c else None),
        ("(c+b)/a",              lambda a,b,c: (c+b)/a if a else None),
        ("(c^2+3)/a",            lambda a,b,c: (c**2+3)/a if a else None),
        ("(a+3)/c",              lambda a,b,c: (a+3)/c if c else None),
        ("(c+3)/b",              lambda a,b,c: (c+3)/b if b else None),
        ("(c-3)/a",              lambda a,b,c: (c-3)/a if a else None),
        ("(c+3)*a",              lambda a,b,c: (c+3)*a),
        ("(c+a)/c",              lambda a,b,c: (c+a)/c if c else None),
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
        ("8c - b",               lambda a,b,c: 8*c - b),
        ("8b - b/c",             lambda a,b,c: 8*b - b/c if c else None),
    ]

    # ---- (11,5): b^2 ----
    V[(11,5)] = [
        ("b^2",                  lambda a,b,c: b**2),
        ("b^a",                  lambda a,b,c: b**a),
        ("b^c",                  lambda a,b,c: b**c),
        ("b*2",                  lambda a,b,c: b*2),
        ("b+2",                  lambda a,b,c: b+2),
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
        ("(2^b+1)/(ab)",         lambda a,b,c: (2**b+1)/(a*b) if a*b else None),
        ("(2^b+a)/(ac)",         lambda a,b,c: (2**b+a)/(a*c) if a*c else None),
        ("(2^b+c)/(ac)",         lambda a,b,c: (2**b+c)/(a*c) if a*c else None),
        ("(2^c+1)/(ac)",         lambda a,b,c: (2**c+1)/(a*c) if a*c else None),
        ("(2^b+1)/(a-c)",        lambda a,b,c: (2**b+1)/(a-c) if a!=c else None),
        ("(2b+1)/(ac)",          lambda a,b,c: (2*b+1)/(a*c) if a*c else None),
        ("(2^b+1)/(2c)",         lambda a,b,c: (2**b+1)/(2*c) if c else None),
        ("(2^b+1)/a",            lambda a,b,c: (2**b+1)/a if a else None),
        ("(2^b+1)/c",            lambda a,b,c: (2**b+1)/c if c else None),
    ]

    return V


# ============================================================
# SEARCH FUNCTIONS
# ============================================================
def find_valid_values(variants_dict, a, b, c):
    """For each position, find all distinct integer values achievable by any variant."""
    pos_options = {}
    for pos, variants in variants_dict.items():
        valid = []
        for vname, vfunc in variants:
            val = safe_eval(vfunc, a, b, c)
            iv = get_int(val)
            if iv is not None:
                valid.append((vname, iv))
        if not valid:
            return None
        seen_vals = {}
        for vname, iv in valid:
            if iv not in seen_vals:
                seen_vals[iv] = vname
        pos_options[pos] = [(name, val) for val, name in sorted(seen_vals.items())]
    return pos_options


def search_all_assignments(pos_options, positions, idx, current_assignment,
                           value_counts, all_results, max_results=10):
    """Backtracking search with count constraint: value k used at most k times."""
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
    print("COMPREHENSIVE VARIANT SEARCH FOR SUBTILES 2 (V3)")
    print("Expanded variants for (5,10) and (9,2) to break value=1 logjam")
    print("=" * 70)

    variants_dict = gen_variants()

    b_candidates = [2]
    a_candidates = [2, 3, 4, 5]
    c_candidates = [2, 3, 4, 5, 6, 7, 8]

    all_solutions = []
    partial_results = []

    for b_val in b_candidates:
        for a_val in a_candidates:
            for c_val in c_candidates:
                if a_val == c_val:
                    continue

                pos_options = find_valid_values(variants_dict, a_val, b_val, c_val)

                if pos_options is None:
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

                positions = sorted(pos_options.keys())
                total_combos = 1
                for pos in positions:
                    total_combos *= len(pos_options[pos])

                print(f"\n{'─'*70}")
                print(f"  Testing a={a_val}, b={b_val}, c={c_val}")
                print(f"  All {len(positions)}/37 positions have valid variants")
                print(f"  Total search space: {total_combos:,}")

                for pos in positions:
                    opts = pos_options[pos]
                    vals = [v for _, v in opts]
                    print(f"    {str(pos):10s}: {len(opts)} option(s) -> values {vals}")

                positions_ordered = sorted(positions,
                                           key=lambda p: len(pos_options[p]))

                print(f"  Searching (most constrained first)...")
                results = []
                search_all_assignments(pos_options, positions_ordered, 0,
                                       {}, {}, results, max_results=5)

                if results:
                    for i, result in enumerate(results):
                        print(f"\n  *** SOLUTION {i+1} for a={a_val}, b={b_val}, c={c_val} ***")
                        for pos in sorted(result.keys()):
                            vname, val = result[pos]
                            print(f"    {str(pos):10s} = {val:3d}  ({vname})")

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
                    print(f"  No valid assignment found (count constraint too tight)")
                    # Diagnostic: show what happens with smallest values
                    min_assign = {}
                    for pos in positions:
                        min_assign[pos] = pos_options[pos][0][1]
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
        partial_results.sort(key=lambda x: -x[0])
        for score, a_val, b_val, c_val, missing in partial_results[:10]:
            print(f"  a={a_val}, b={b_val}, c={c_val}: {score}/37")
            if missing:
                print(f"    UNSATISFIABLE: {missing}")
                for pos in missing:
                    variants = variants_dict[pos]
                    orig_name = variants[0][0]
                    orig_func = variants[0][1]
                    v = safe_eval(orig_func, a_val, b_val, c_val)
                    v_str = f"{v:.6f}" if v is not None else "UNDEF"
                    all_vals = []
                    for vn, vf in variants:
                        vv = safe_eval(vf, a_val, b_val, c_val)
                        if vv is not None:
                            all_vals.append(f"{vn}={vv:.4f}")
                    print(f"      {pos}: {orig_name} = {v_str}")
                    if all_vals:
                        print(f"        Variants: {', '.join(all_vals[:6])}")


if __name__ == "__main__":
    main()
