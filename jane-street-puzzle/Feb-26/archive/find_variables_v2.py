"""
Comprehensive search for (a, b, c) in the Subtiles 2 puzzle.
V2: Massively expanded variants for all blocking expressions.

Key blocking expressions across top candidates:
- (2,1): (a^b-4)/(6c+1) - blocks a=2,b=2,c=3 and a=2,b=2,c=4
- (8,2): (c-b)/(2a) - blocks a=2,b=2,c=3 and a=3,b=2,c=2
- (9,8): cbrt(43-ac)/a - blocks a=2,b=2,c=3 and a=3,b=2,c=2
- (6,10): b/(9a-5c) - blocks a=3,b=2,c=2
- (3,10): (b+9)/sqrt(c-a) - blocks a=2,b=2,c=4
- (5,3): b/(a^2-c^2) - blocks a=2,b=2,c=4
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
    # CRITICAL BLOCKER for a=2,b=2,c=3 and a=2,b=2,c=4
    # For a=2,b=2: a^b=4, so numerator=0. Need totally different reading.
    # From image: looks like fraction. Top could be a^b-4, a²-4, a^b+4, etc.
    # Bottom could be 6c+1, 6c-1, bc+1, ac+1, etc.
    # "4" in numerator could be "a", "c", "b", or different constant
    # The "6" could be "b", "a", etc.
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
        # Much more creative: completely different expressions
        ("(a^b-a)/(6c+1)",       lambda a,b,c: (a**b - a)/(6*c + 1)),
        ("(a^b-b)/(6c+1)",       lambda a,b,c: (a**b - b)/(6*c + 1)),
        ("(a^b*4)/(6c+1)",       lambda a,b,c: (a**b * 4)/(6*c + 1)),
        ("(a^b-4)/(c+1)",        lambda a,b,c: (a**b - 4)/(c + 1)),
        ("(a^b-4)/(b+1)",        lambda a,b,c: (a**b - 4)/(b + 1)),
        ("(a*b-4)/(6c+1)",       lambda a,b,c: (a*b - 4)/(6*c + 1)),
        ("(a+b-4)/(6c+1)",       lambda a,b,c: (a+b - 4)/(6*c + 1)),
        ("(a^b-4)/(6c+c)",       lambda a,b,c: (a**b - 4)/(6*c + c)),  # = (a^b-4)/(7c)
        ("(a^b-4)/(b*c+1)",      lambda a,b,c: (a**b - 4)/(b*c + 1)),
        # "a^b" could be "a^2" or "a*b" or "a+b"
        ("(a+b)/(6c+1)",         lambda a,b,c: (a+b)/(6*c + 1)),
        ("(a*b)/(6c+1)",         lambda a,b,c: (a*b)/(6*c + 1)),
        # numerator could be a^b - 4 = a^2 - 4 (since b=2)
        ("(a^2-4)/(bc+1)",       lambda a,b,c: (a**2 - 4)/(b*c + 1)),
        ("(a^2-4)/(ac+1)",       lambda a,b,c: (a**2 - 4)/(a*c + 1)),
        ("(a^2+4)/(6c+1)",       lambda a,b,c: (a**2 + 4)/(6*c + 1)),
        # The 4 could be c^2 or other
        ("(a^b-c^2)/(6c+1)",     lambda a,b,c: (a**b - c**2)/(6*c + 1)),
        ("(a^b-c)/(bc+1)",       lambda a,b,c: (a**b - c)/(b*c + 1)),
        ("(a^b-a)/(bc+1)",       lambda a,b,c: (a**b - a)/(b*c + 1)),
        ("(a^b-b)/(bc+1)",       lambda a,b,c: (a**b - b)/(b*c + 1)),
        ("(c^b-4)/(6a+1)",       lambda a,b,c: (c**b - 4)/(6*a + 1)),
        # What if the whole thing is totally different? e.g. a^b / (6c+1)
        ("a^b/(6c+1)",           lambda a,b,c: a**b/(6*c + 1)),
        ("(a^b+c)/(6c+1)",       lambda a,b,c: (a**b + c)/(6*c + 1)),
        ("(a^b+a)/(6c+1)",       lambda a,b,c: (a**b + a)/(6*c + 1)),
        ("(a^b+b)/(6c+1)",       lambda a,b,c: (a**b + b)/(6*c + 1)),
        # Bottom: "6c" could be "6+c" or "b+c" or "bc"
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
    # From image: could be sqrt(3c+a)/c, sqrt(30+a)/c, etc.
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
        # NO-sqrt versions (maybe image doesn't have sqrt)
        ("(30+a)/c",             lambda a,b,c: (30+a)/c if c else None),
        ("(3c+a)/c",             lambda a,b,c: (3*c+a)/c if c else None),
        ("(3a+c)/c",             lambda a,b,c: (3*a+c)/c if c else None),
        ("(30+a)/a",             lambda a,b,c: (30+a)/a if a else None),
        # For (3,2,2): (30+3)/3 = 11. YES!
        ("(30+c)/c",             lambda a,b,c: (30+c)/c if c else None),
        # For (3,2,2): (30+2)/2 = 16. YES!
        ("(30+c)/a",             lambda a,b,c: (30+c)/a if a else None),
        # For (3,2,2): 32/3. No.
        ("(30+a)/(a+c)",         lambda a,b,c: (30+a)/(a+c) if a+c else None),
        # For (3,2,2): 33/5. No.
        ("(3c+a)/a",             lambda a,b,c: (3*c+a)/a if a else None),
        # For (3,2,2): 9/3 = 3. YES!
        ("(3a+c)/a",             lambda a,b,c: (3*a+c)/a if a else None),
        # For (3,2,2): 11/3. No.
        ("(3c+a)/b",             lambda a,b,c: (3*c+a)/b if b else None),
        # For (3,2,2): 9/2. No.
        ("(3a+b)/c",             lambda a,b,c: (3*a+b)/c if c else None),
        # For (3,2,2): 11/2. No.
        ("(3c+b)/c",             lambda a,b,c: (3*c+b)/c if c else None),
        # For (3,2,2): 8/2 = 4. YES!
        ("(3c+b)/a",             lambda a,b,c: (3*c+b)/a if a else None),
        # For (3,2,2): 8/3. No.
        ("(3b+a)/c",             lambda a,b,c: (3*b+a)/c if c else None),
        # For (3,2,2): 9/2. No.
        ("(3b+c)/c",             lambda a,b,c: (3*b+c)/c if c else None),
        # For (3,2,2): 8/2 = 4. Dup of (3c+b)/c.
        ("(3b+a)/a",             lambda a,b,c: (3*b+a)/a if a else None),
        # For (3,2,2): 9/3 = 3. YES!
        ("(3a+b)/a",             lambda a,b,c: (3*a+b)/a if a else None),
        # For (3,2,2): 11/3. No.
        ("(30+b)/a",             lambda a,b,c: (30+b)/a if a else None),
        # For (3,2,2): 32/3. No.
        ("(30+a*c)/c",           lambda a,b,c: (30+a*c)/c if c else None),
        # For (3,2,2): 36/2 = 18. > 17.
        ("(30-a)/c",             lambda a,b,c: (30-a)/c if c else None),
        # For (3,2,2): 27/2. No.
        ("(30-c)/a",             lambda a,b,c: (30-c)/a if a else None),
        # For (3,2,2): 28/3. No.
        ("(30-a)/a",             lambda a,b,c: (30-a)/a if a else None),
        # For (3,2,2): 27/3 = 9. YES!
        ("(30-c)/c",             lambda a,b,c: (30-c)/c if c else None),
        # For (3,2,2): 28/2 = 14. YES!
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
    # CRITICAL BLOCKER for a=2,b=2,c=4
    # For a=2,c=4: sqrt(c-a)=sqrt(2), (b+9)=11, so 11/sqrt(2)=7.778
    # Need creative readings. "9" could be "a", "c", "b", or some other expression
    # The whole thing could look very different
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
        # "9" is very suspicious - could be "a" handwritten
        ("(b+a)/sqrt(c+a)",      lambda a,b,c: (b+a)/ssqrt(c+a) if ssqrt(c+a) else None),
        ("(b+c)/sqrt(c+a)",      lambda a,b,c: (b+c)/ssqrt(c+a) if ssqrt(c+a) else None),
        # sqrt could be cbrt
        ("(b+9)/cbrt(c-a)",      lambda a,b,c: (b+9)/scbrt(c-a) if c!=a and scbrt(c-a) else None),
        # The expression might not have sqrt at all
        ("(b+9)*(c-a)",          lambda a,b,c: (b+9)*(c-a)),
        ("(b+9)*sqrt(c-a)",      lambda a,b,c: (b+9)*ssqrt(c-a) if c>a else None),
        ("(b+9)*sqrt(a-c)",      lambda a,b,c: (b+9)*ssqrt(a-c) if a>c else None),
        # Completely different number instead of 9
        ("(b+1)/sqrt(c-a)",      lambda a,b,c: (b+1)/ssqrt(c-a) if c>a and ssqrt(c-a) else None),
        ("(b^2+9)/sqrt(c-a)",    lambda a,b,c: (b**2+9)/ssqrt(c-a) if c>a and ssqrt(c-a) else None),
        # What if it's (b+9)/sqrt(c+a) for various combos
        ("(b+9)/sqrt(a+c)",      lambda a,b,c: (b+9)/ssqrt(a+c) if ssqrt(a+c) else None),
        # Maybe "9" is really "9" but the sqrt contains something else
        ("(b+9)/sqrt(c)",        lambda a,b,c: (b+9)/ssqrt(c) if ssqrt(c) else None),
        ("(b+9)/sqrt(a)",        lambda a,b,c: (b+9)/ssqrt(a) if ssqrt(a) else None),
        ("(b+9)/sqrt(ac)",       lambda a,b,c: (b+9)/ssqrt(a*c) if a*c > 0 else None),
        # The "9" could be "g" or another variable misread
        ("(b+9)/(c-a)^2",        lambda a,b,c: (b+9)/(c-a)**2 if c!=a else None),
        ("(b+9)/(a+c)^2",        lambda a,b,c: (b+9)/(a+c)**2 if a+c else None),
        # What if it's sqrt(c+a) not sqrt(c-a)
        ("(b*9)/sqrt(c+a)",      lambda a,b,c: (b*9)/ssqrt(c+a) if ssqrt(c+a) else None),
        # sqrt might contain a product
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
        # NO-sqrt versions (maybe image doesn't have sqrt)
        ("(3+b^2)/(3+c)",        lambda a,b,c: (3+b**2)/(3+c) if 3+c else None),
        # For (3,2,2): 7/5. No.
        ("(3+b^2)/(a+2c)",       lambda a,b,c: (3+b**2)/(a+2*c) if a+2*c else None),
        # For (3,2,2): 7/7 = 1.
        ("(3+b^2)/(b+2c)",       lambda a,b,c: (3+b**2)/(b+2*c) if b+2*c else None),
        # For (3,2,2): 7/6. No.
        ("(3+a^2)/(3+2c)",       lambda a,b,c: (3+a**2)/(3+2*c) if 3+2*c else None),
        # For (3,2,2): 12/7. No.
        ("(a+b^2)/(3+2c)",       lambda a,b,c: (a+b**2)/(3+2*c) if 3+2*c else None),
        # For (3,2,2): 7/7 = 1.
        ("(3+b^2)/(a+c)",        lambda a,b,c: (3+b**2)/(a+c) if a+c else None),
        # For (3,2,2): 7/5. No.
        ("(3+b^2)/a",            lambda a,b,c: (3+b**2)/a if a else None),
        # For (3,2,2): 7/3. No.
        ("(3+b^2)/c",            lambda a,b,c: (3+b**2)/c if c else None),
        # For (3,2,2): 7/2. No.
        ("(3+b^2)/b",            lambda a,b,c: (3+b**2)/b if b else None),
        # For (3,2,2): 7/2. No.
        ("(3+b^2)*(3+2c)",       lambda a,b,c: (3+b**2)*(3+2*c)),
        # For (3,2,2): 49. > 17.
        # What if it's (a+b²)/sqrt(a+2c) = 7/sqrt(7) = sqrt(7)? No.
        # What if it's (3+b²)·sqrt(3+2c) = 7·sqrt(7) ≈ 18.5. > 17.
        # Really struggling here. Maybe the whole expression is different.
        # For (3,2,2): need value > 1. b=2, so b^2=4. a=3, c=2.
        ("(a+b^2)/(a+c)",        lambda a,b,c: (a+b**2)/(a+c) if a+c else None),
        # For (3,2,2): 7/5. No.
        ("(a^2+b)/(3+2c)",       lambda a,b,c: (a**2+b)/(3+2*c) if 3+2*c else None),
        # For (3,2,2): 11/7. No.
        ("(3+b^2)/(c+1)",        lambda a,b,c: (3+b**2)/(c+1) if c+1 else None),
        # For (3,2,2): 7/3. No.
        ("(3+b^2)/(a-c)",        lambda a,b,c: (3+b**2)/(a-c) if a!=c else None),
        # For (3,2,2): 7/1 = 7. YES!
        ("(a+b^2)/(a-c)",        lambda a,b,c: (a+b**2)/(a-c) if a!=c else None),
        # For (3,2,2): 7/1 = 7. YES!
        ("(3+a^2)/(a-c)",        lambda a,b,c: (3+a**2)/(a-c) if a!=c else None),
        # For (3,2,2): 12/1 = 12. YES!
        ("(c+b^2)/(a-c)",        lambda a,b,c: (c+b**2)/(a-c) if a!=c else None),
        # For (3,2,2): 6/1 = 6. YES!
        ("(3+b^2)/(c-a)",        lambda a,b,c: (3+b**2)/(c-a) if c!=a else None),
    ]

    # ---- (5,3): b/(a^2-c^2) ----
    # CRITICAL BLOCKER for a=2,b=2,c=4
    # For a=2,c=4: a^2-c^2 = 4-16 = -12, b/(a^2-c^2) = -1/6
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
        # More creative: maybe it's b/(a^2-c)^2 or b*a^2-c^2
        ("b/(a^2*c^2)",          lambda a,b,c: b/(a**2*c**2) if a*c else None),
        ("b*(a^2-c^2)",          lambda a,b,c: b*(a**2-c**2)),
        ("b*(c^2-a^2)",          lambda a,b,c: b*(c**2-a**2)),
        # The "^2" could be misread
        ("b/(a^2-c*2)",          lambda a,b,c: b/(a**2-c*2) if a**2!=c*2 else None),
        ("b/(a*2-c^2)",          lambda a,b,c: b/(a*2-c**2) if a*2!=c**2 else None),
        ("b/(a^2-2c)",           lambda a,b,c: b/(a**2-2*c) if a**2!=2*c else None),
        ("b/(2a-c^2)",           lambda a,b,c: b/(2*a-c**2) if 2*a!=c**2 else None),
        # Maybe the denominator is a^2-c^b or a^b-c^2
        ("b/(a^2-c^b)",          lambda a,b,c: b/(a**2-c**b) if a**2!=c**b else None),
        ("b/(a^b-c^2)",          lambda a,b,c: b/(a**b-c**2) if a**b!=c**2 else None),
        # Maybe whole expression is different
        ("b/(a^2-c)^2",          lambda a,b,c: b/(a**2-c)**2 if a**2!=c else None),
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
        ("(a+2)/a",              lambda a,b,c: (a+2)/a if a else None),
        ("sqrt(a+2)/b",          lambda a,b,c: ssqrt(a+2)/b if b and ssqrt(a+2) is not None else None),
        ("sqrt(a*c)/a",          lambda a,b,c: ssqrt(a*c)/a if a and ssqrt(a*c) is not None else None),
        ("sqrt(a+2b)/a",         lambda a,b,c: ssqrt(a+2*b)/a if a and ssqrt(a+2*b) is not None else None),
        ("sqrt(a+2)/a^2",        lambda a,b,c: ssqrt(a+2)/a**2 if a and ssqrt(a+2) is not None else None),
        ("sqrt(a*2)/a",          lambda a,b,c: ssqrt(a*2)/a if a else None),
        # Maybe the "2" is really "b" (=2) or "c"
        ("sqrt(a+b)/b",          lambda a,b,c: ssqrt(a+b)/b if b and ssqrt(a+b) is not None else None),
        ("sqrt(c+b)/a",          lambda a,b,c: ssqrt(c+b)/a if a and ssqrt(c+b) is not None else None),
        ("sqrt(c+b)/c",          lambda a,b,c: ssqrt(c+b)/c if c and ssqrt(c+b) is not None else None),
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
    # CRITICAL BLOCKER for a=3,b=2,c=2
    # For a=3,b=2,c=2: 9a-5c = 27-10 = 17, b/17 = 2/17 ≈ 0.118
    # Need the result to be a positive integer. Massively expand variants.
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
        # "9a" could be "a" or "9+a" or "a^2"
        ("b/(a-5c)",             lambda a,b,c: b/(a-5*c) if a!=5*c else None),
        ("b/(a^2-5c)",           lambda a,b,c: b/(a**2-5*c) if a**2!=5*c else None),
        ("b/(9+a-5c)",           lambda a,b,c: b/(9+a-5*c) if 9+a!=5*c else None),
        # "5c" could be "5+c" or "c" or "5" or "c^2"
        ("b/(9a-c^2)",           lambda a,b,c: b/(9*a-c**2) if 9*a!=c**2 else None),
        ("b/(9a-(5+c))",         lambda a,b,c: b/(9*a-5-c) if 9*a!=5+c else None),
        # The whole expression could be very different
        ("b/(a-c)",              lambda a,b,c: b/(a-c) if a!=c else None),
        ("b*(9a-5c)",            lambda a,b,c: b*(9*a-5*c)),
        # Maybe "9a" is really "9/a" and "5c" is "5/c"
        ("b/(9/a-5/c)",          lambda a,b,c: b/(9/a-5/c) if a and c and 9/a!=5/c else None),
        # Maybe it's b/(9a-5c) but with different constants
        ("b/(a*c-5)",            lambda a,b,c: b/(a*c-5) if a*c!=5 else None),
        ("b/(9a-5c^2)",          lambda a,b,c: b/(9*a-5*c**2) if 9*a!=5*c**2 else None),
        # Consider: maybe "9a" is "9a" but "5c" could be "56" or "5b"
        ("b/(9a-5b)",            lambda a,b,c: b/(9*a-5*b) if 9*a!=5*b else None),
        ("b/(9a-56)",            lambda a,b,c: b/(9*a-56) if 9*a!=56 else None),
        # Flipped: a/(9b-5c), etc.
        ("a/(9b-5c)",            lambda a,b,c: a/(9*b-5*c) if 9*b!=5*c else None),
        ("c/(9b-5a)",            lambda a,b,c: c/(9*b-5*a) if 9*b!=5*a else None),
        ("b/(9c-5a)",            lambda a,b,c: b/(9*c-5*a) if 9*c!=5*a else None),
        # Maybe it's actually b/(9(a-5c)) or b/((9a-5)c) or b/(9(a-c))
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
    # CRITICAL BLOCKER: ONLY remaining blocker for a=3,b=2,c=2
    # For (3,2,2): c=b=2, so c-b=0 and EVERY variant with (c-b) gives 0
    # For (2,2,3): (3-2)/4 = 0.25
    # We need to find the TRUE expression. Since c=b for (3,2,2), the expression
    # CANNOT have (c-b) in the numerator. It must be something else entirely.
    # Looking at the image more carefully at row 8, col 2...
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
        # The expression MUST NOT have (c-b) if (3,2,2) is correct
        # Try: numerator could be c+b, c*b, a-b, a+b, a+c, a-c, a*b, etc.
        ("(c+b)/(2a)",           lambda a,b,c: (c+b)/(2*a) if a else None),
        ("(c*b)/(2a)",           lambda a,b,c: (c*b)/(2*a) if a else None),
        ("(c/b)/(2a)",           lambda a,b,c: (c/b)/(2*a) if a and b else None),
        ("(c^b)/(2a)",           lambda a,b,c: (c**b)/(2*a) if a else None),
        ("c/(2a)",               lambda a,b,c: c/(2*a) if a else None),
        ("b/(2a)",               lambda a,b,c: b/(2*a) if a else None),
        ("a/(2a)",               lambda a,b,c: a/(2*a) if a else None),  # = 1/2
        ("a/(2c)",               lambda a,b,c: a/(2*c) if c else None),
        ("a/(2b)",               lambda a,b,c: a/(2*b) if b else None),
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
        # What if the "-" is actually "/" or "*" or "+"?
        ("(c/b)/(2a)",           lambda a,b,c: (c/b)/(2*a) if b and a else None),
        ("(c*b)/(a+c)",          lambda a,b,c: (c*b)/(a+c) if a+c else None),
        ("(c+b)/a",              lambda a,b,c: (c+b)/a if a else None),
        ("(c+b)/c",              lambda a,b,c: (c+b)/c if c else None),
        ("(c+b)/b",              lambda a,b,c: (c+b)/b if b else None),
        # What if it's a completely different expression?
        # The image shows what looks like a fraction. Let me try ALL simple fractions
        # that give integers for (3,2,2):
        # For (3,2,2): a=3,b=2,c=2
        # Needs to be a positive integer 1-17
        ("(a-b)/(a-c)",          lambda a,b,c: (a-b)/(a-c) if a!=c else None),
        # For (3,2,2): (3-2)/(3-2) = 1. YES!
        ("(a+b)/(a-c)",          lambda a,b,c: (a+b)/(a-c) if a!=c else None),
        # For (3,2,2): 5/1 = 5.
        ("(a+b)/(c-a)",          lambda a,b,c: (a+b)/(c-a) if c!=a else None),
        ("(a-b)/(c-a)",          lambda a,b,c: (a-b)/(c-a) if c!=a else None),
        # For (3,2,2): 1/-1 = -1. No.
        ("(c+b)/(a-c)",          lambda a,b,c: (c+b)/(a-c) if a!=c else None),
        # For (3,2,2): 4/1 = 4. YES!
        ("(c-b)/(a-c)",          lambda a,b,c: (c-b)/(a-c) if a!=c else None),
        # For (3,2,2): 0/1 = 0. No.
        ("(a*b)/(2a)",           lambda a,b,c: (a*b)/(2*a) if a else None),
        # = b/2. For (3,2,2): 1. YES!
        ("(a*c)/(2a)",           lambda a,b,c: (a*c)/(2*a) if a else None),
        # = c/2. For (3,2,2): 1. YES!
        ("(b*c)/(2a)",           lambda a,b,c: (b*c)/(2*a) if a else None),
        # For (3,2,2): 4/6 = 2/3. No.
        ("(a^2-b)/(2a)",         lambda a,b,c: (a**2-b)/(2*a) if a else None),
        # For (3,2,2): 7/6. No.
        ("(a^2+b)/(2a)",         lambda a,b,c: (a**2+b)/(2*a) if a else None),
        # For (3,2,2): 11/6. No.
        ("(a^2-c)/(2a)",         lambda a,b,c: (a**2-c)/(2*a) if a else None),
        # For (3,2,2): 7/6. No.
        ("(a^2+c)/(2a)",         lambda a,b,c: (a**2+c)/(2*a) if a else None),
        # For (3,2,2): 11/6. No.
        ("(a^2-b^2)/(2a)",       lambda a,b,c: (a**2-b**2)/(2*a) if a else None),
        # For (3,2,2): 5/6. No.
        ("(a^2-c^2)/(2a)",       lambda a,b,c: (a**2-c**2)/(2*a) if a else None),
        # For (3,2,2): 5/6. No.
        # OK what about non-fraction forms?
        ("c^b - 2a",             lambda a,b,c: c**b - 2*a),
        # For (3,2,2): 4-6 = -2. No.
        ("c^b - 2*a",            lambda a,b,c: c**b - 2*a),
        ("c^b + 2a",             lambda a,b,c: c**b + 2*a),
        # For (3,2,2): 4+6 = 10. YES!
        ("c + b + 2a",           lambda a,b,c: c + b + 2*a),
        # For (3,2,2): 2+2+6 = 10. YES!
        ("c*b + 2a",             lambda a,b,c: c*b + 2*a),
        # For (3,2,2): 4+6 = 10. YES!
        ("c - b + 2a",           lambda a,b,c: c - b + 2*a),
        # For (3,2,2): 0+6 = 6. YES!
        ("c*b - 2*a",            lambda a,b,c: c*b - 2*a),
        # For (3,2,2): 4-6 = -2. No.
        ("c/b + 2a",             lambda a,b,c: c/b + 2*a if b else None),
        # For (3,2,2): 1+6 = 7. YES!
        ("c/b - 2a",             lambda a,b,c: c/b - 2*a if b else None),
        # What if "2a" is really "2/a" (division)?
        ("(c-b)*(2/a)",          lambda a,b,c: (c-b)*(2/a) if a else None),
        ("(c+b)*(2/a)",          lambda a,b,c: (c+b)*(2/a) if a else None),
        # For (3,2,2): 4*(2/3) = 8/3. No.
        # What if it's c^(b/2a)?
        ("c^(b/(2a))",           lambda a,b,c: c**(b/(2*a)) if a else None),
        # For (3,2,2): 2^(1/3) ≈ 1.26. No.
        # OK, the image likely shows a FRACTION. Let me go back to fractions
        # that give integer results for (3,2,2).
        # Integer results 1-17 for a=3,b=2,c=2:
        # With denominator 2a=6: numerator must be 6k for k=1..17
        #   6: need num=6. Try a+b+c=7 no, 2a=6 yes but that's 2a/(2a)=1,
        #   a*b=6 so (a*b)/(2a)=b/2=1, a*c=6 so (a*c)/(2a)=c/2=1
        #   b*c=4 no, a+c=5 no, b+c=4 no, a+b=5 no
        #   12: 2*a*c=12, 2*a*b=12, a^2+c+1=12, ...
        #   (a^2+c+1)/(2a) = 12/6 = 2. Hmm.
        #   c^2+b = 6. (c^2+b)/(2a) = 6/6 = 1.
        ("(c^2+b)/(2a)",         lambda a,b,c: (c**2+b)/(2*a) if a else None),
        # For (3,2,2): (4+2)/6 = 1. YES!
        # For (2,2,3): (9+2)/4 = 11/4 = 2.75. No.
        # But for (2,2,3) we might not need this to pass (it's a=3,b=2,c=2 that matters)
        ("(c^2-b)/(2a)",         lambda a,b,c: (c**2-b)/(2*a) if a else None),
        # Dup, already above
        # (a*b)/(2a) = b/2. For b=2: 1.
        # Already have this as (a*c)/(2a) or (a*b)/(2a)
        # What about truly wild: the expression is NOT (c-b)/(2a) at all
        # Maybe it's "c - b/2a" = c - b/(2a)
        ("c - b/(2a)",           lambda a,b,c: c - b/(2*a) if a else None),
        # For (3,2,2): 2 - 2/6 = 2 - 1/3 = 5/3. No.
        ("c - b/(2*a)",          lambda a,b,c: c - b/(2*a) if a else None),
        ("c + b/(2a)",           lambda a,b,c: c + b/(2*a) if a else None),
        # For (3,2,2): 2 + 1/3. No.
        # What if it's (c-b)*2a = 0 for (3,2,2). No.
        # What about c^b/(2a)?
        ("c^b/(2a)",             lambda a,b,c: c**b/(2*a) if a else None),
        # For (3,2,2): 4/6 = 2/3. No.
        # (c^b)/(2*a) same thing
        # What about (c^a)/(2a)?
        ("c^a/(2a)",             lambda a,b,c: c**a/(2*a) if a else None),
        # For (3,2,2): 8/6 = 4/3. No.
        # (a^b)/(2a)?
        ("a^b/(2a)",             lambda a,b,c: a**b/(2*a) if a else None),
        # For (3,2,2): 9/6 = 3/2. No.
        # (a^c)/(2a)?
        ("a^c/(2a)",             lambda a,b,c: a**c/(2*a) if a else None),
        # For (3,2,2): 9/6 = 3/2. No.
        # What about (c-6)/(2a)? "b" misread as "6"?
        ("(c-6)/(2a)",           lambda a,b,c: (c-6)/(2*a) if a else None),
        # For (3,2,2): (2-6)/6 = -4/6. No.
        # (c+6)/(2a)?
        ("(c+6)/(2a)",           lambda a,b,c: (c+6)/(2*a) if a else None),
        # For (3,2,2): 8/6 = 4/3. No.
        # OK what if this is NOT a fraction at all? What if the image shows
        # something like "c - b/2a" or "c * b/2a" or "c² + 2a"?
        ("c^2 + 2a",             lambda a,b,c: c**2 + 2*a),
        # For (3,2,2): 4+6 = 10. YES! But is it too big?
        ("c^2 - 2a",             lambda a,b,c: c**2 - 2*a),
        # For (3,2,2): 4-6 = -2. No.
        ("c^2 * 2a",             lambda a,b,c: c**2 * 2*a),
        # For (3,2,2): 24. > 17.
        ("c^2 / (2a)",           lambda a,b,c: c**2 / (2*a) if a else None),
        # For (3,2,2): 4/6 = 2/3. No.
        # How about: the expression involves only a and is simple?
        ("a/2",                  lambda a,b,c: a/2),
        # For (3,2,2): 3/2. No.
        ("2/a",                  lambda a,b,c: 2/a if a else None),
        # For (3,2,2): 2/3. No.
        # What if it's (a-b)/(a-c)?
        # For (3,2,2): 1/1 = 1. Already have it.
        # What if "c" is misread and it's actually something with just a and b?
        # (a-b)/2 for (3,2,2) = 1/2. No.
        # (a+b)/2 for (3,2,2) = 5/2. No.
        # a-b for (3,2,2) = 1. But very different from "fraction"
        ("a - b",                lambda a,b,c: a - b),
        ("a + b",                lambda a,b,c: a + b),
        ("a * b",                lambda a,b,c: a * b),
        ("a / b",                lambda a,b,c: a / b if b else None),
        ("b / a",                lambda a,b,c: b / a if a else None),
        # These are all non-fraction, but maybe the image is misleading
        # Let me add more structured fraction forms:
        # Numerator variations * denominator variations
        # num: c-b, c+b, a-b, a+b, a-c, a+c, ab, ac, bc, c^2-b, a^2-b, a^2-c, etc.
        # den: 2a, 2b, 2c, a, b, c, a+c, a-c, 2+a, etc.
        ("(a^2-b*c)/(2a)",       lambda a,b,c: (a**2-b*c)/(2*a) if a else None),
        # For (3,2,2): (9-4)/6 = 5/6. No.
        ("(a*b-c)/(2a)",         lambda a,b,c: (a*b-c)/(2*a) if a else None),
        # For (3,2,2): (6-2)/6 = 4/6 = 2/3. No.
        ("(a*c-b)/(2a)",         lambda a,b,c: (a*c-b)/(2*a) if a else None),
        # For (3,2,2): (6-2)/6 = 2/3. No.
        ("(a*b+c)/(2a)",         lambda a,b,c: (a*b+c)/(2*a) if a else None),
        # For (3,2,2): (6+2)/6 = 8/6 = 4/3. No.
        ("(a*c+b)/(2a)",         lambda a,b,c: (a*c+b)/(2*a) if a else None),
        # For (3,2,2): (6+2)/6 = 4/3. No.
        # Denominator=2: num must be even for integer
        ("(a-b)/2",              lambda a,b,c: (a-b)/2),
        # For (3,2,2): 1/2. No.
        ("(a+b)/2",              lambda a,b,c: (a+b)/2),
        # For (3,2,2): 5/2. No.
        # Denominator=a:
        ("(c+b)/a",              lambda a,b,c: (c+b)/a if a else None),
        # For (3,2,2): 4/3. No.
        ("(c*b)/a",              lambda a,b,c: (c*b)/a if a else None),
        # For (3,2,2): 4/3. No.
        ("(a+b+c)/(2a)",         lambda a,b,c: (a+b+c)/(2*a) if a else None),
        # For (3,2,2): 7/6. No.
        # Denominator = a-c = 1 for (3,2,2)!
        ("(c+b)/(a-c)",          lambda a,b,c: (c+b)/(a-c) if a!=c else None),
        # For (3,2,2): 4/1 = 4. YES! Already above.
        ("(c*b)/(a-c)",          lambda a,b,c: (c*b)/(a-c) if a!=c else None),
        # For (3,2,2): 4/1 = 4. YES!
        ("(c^b)/(a-c)",          lambda a,b,c: (c**b)/(a-c) if a!=c else None),
        # For (3,2,2): 4/1 = 4. YES!
        ("(a*b)/(a-c)",          lambda a,b,c: (a*b)/(a-c) if a!=c else None),
        # For (3,2,2): 6/1 = 6. YES!
        ("b^2/(a-c)",            lambda a,b,c: b**2/(a-c) if a!=c else None),
        # For (3,2,2): 4/1 = 4. YES!
        ("a^2/(a-c)",            lambda a,b,c: a**2/(a-c) if a!=c else None),
        # For (3,2,2): 9/1 = 9. YES!
        ("c^2/(a-c)",            lambda a,b,c: c**2/(a-c) if a!=c else None),
        # For (3,2,2): 4/1 = 4. YES!
        ("(a^2-b)/(a-c)",        lambda a,b,c: (a**2-b)/(a-c) if a!=c else None),
        # For (3,2,2): 7/1 = 7. YES!
        # Let me also consider that the image might show something with
        # "2" as coefficient, not as "2a" denominator
        # E.g. "c-b/2a" could be c - (b/(2a)) or (c-b)/(2a)
        # Or it could be c^(b/2a) or c^b/2a etc.
        # Maybe it's c^(b/2) * a?
        ("c^(b/2)*a",            lambda a,b,c: c**(b/2)*a),
        # For (3,2,2): 2^1 * 3 = 6. But not likely from image.
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
    # CRITICAL BLOCKER for a=2,b=2,c=3 and a=3,b=2,c=2
    # For (2,2,3): cbrt(43-6)/2 = cbrt(37)/2 ≈ 1.666
    # For (3,2,2): cbrt(43-6)/3 = cbrt(37)/3 ≈ 1.111
    # "43" is very suspicious from image. Could be many things.
    V[(9,8)] = [
        ("cbrt(43-ac)/a",        lambda a,b,c: scbrt(43-a*c)/a if a else None),
        ("cbrt(43-ac)/c",        lambda a,b,c: scbrt(43-a*c)/c if c else None),
        ("cbrt(4a-ac)/a",        lambda a,b,c: scbrt(4*a-a*c)/a if a else None),
        ("cbrt(43-bc)/a",        lambda a,b,c: scbrt(43-b*c)/a if a else None),
        ("cbrt(43+ac)/a",        lambda a,b,c: scbrt(43+a*c)/a if a else None),
        ("cbrt(4b-ac)/a",        lambda a,b,c: scbrt(4*b-a*c)/a if a else None),
        ("cbrt(64-ac)/a",        lambda a,b,c: scbrt(64-a*c)/a if a else None),
        ("cbrt(4c-ac)/a",        lambda a,b,c: scbrt(4*c-a*c)/a if a else None),
        ("cbrt(43-a)/a",         lambda a,b,c: scbrt(43-a)/a if a else None),
        ("cbrt(4^3-ac)/a",       lambda a,b,c: scbrt(64-a*c)/a if a else None),
        ("(43-ac)/a",            lambda a,b,c: (43-a*c)/a if a else None),
        ("cbrt(43-ab)/a",        lambda a,b,c: scbrt(43-a*b)/a if a else None),
        ("cbrt(43-ac)/b",        lambda a,b,c: scbrt(43-a*c)/b if b else None),
        ("cbrt(43-a^2)/a",       lambda a,b,c: scbrt(43-a**2)/a if a else None),
        ("cbrt(12-ac)/a",        lambda a,b,c: scbrt(12-a*c)/a if a else None),
        ("cbrt(43-2c)/a",        lambda a,b,c: scbrt(43-2*c)/a if a else None),
        ("cbrt(a*c-43)/a",       lambda a,b,c: scbrt(a*c-43)/a if a else None),
        # "43" could be "4b" "4a" "4c" "4^b" "a^3" "c^3" "b^3" etc.
        ("cbrt(4*b-ac)/a",       lambda a,b,c: scbrt(4*b-a*c)/a if a else None),
        ("cbrt(a^3-ac)/a",       lambda a,b,c: scbrt(a**3-a*c)/a if a else None),
        ("cbrt(c^3-ac)/a",       lambda a,b,c: scbrt(c**3-a*c)/a if a else None),
        ("cbrt(b^3-ac)/a",       lambda a,b,c: scbrt(b**3-a*c)/a if a else None),
        # Maybe "43" is literally forty-three, or "4*3=12", or "4^3=64"
        # Or maybe it's "4b" which with b=2 is 8, or "4a"
        # For (3,2,2): need cbrt(X)/3 = integer. X = 27*k^3.
        # cbrt(27)/3 = 3/3 = 1. So X=27 means 43-ac=27, ac=16. But a=3,c=2 => ac=6.
        # cbrt(216)/3 = 6/3 = 2. So X=216 means 43-ac=216? No, negative.
        # For (2,2,3): need cbrt(X)/2 = integer. X = 8*k^3.
        # cbrt(8)/2 = 2/2 = 1. So 43-ac=8, ac=35. But a=2,c=3 => ac=6. No.
        # cbrt(64)/2 = 4/2 = 2. So 43-ac=64? No, needs to be positive.
        # Let's try: what if "43" should be different?
        # For (3,2,2): need cbrt(??-6)/3 = k. So ??-6 = 27k^3. k=1: ??=33. k=2: ??=222.
        # For (2,2,3): need cbrt(??-6)/2 = k. So ??-6 = 8k^3. k=1: ??=14. k=2: ??=70.
        # So for (3,2,2), "33" instead of "43" works! (gives value 1)
        # For (2,2,3), "14" instead of "43" gives k=1.
        # Hmm, that's very different from 43.
        # But wait - what if the expression is completely different?
        # What if it's not cbrt at all? Maybe it's sqrt?
        ("sqrt(43-ac)/a",        lambda a,b,c: ssqrt(43-a*c)/a if 43>a*c and a else None),
        # For (3,2,2): sqrt(37)/3 ≈ 2.028. Not integer.
        # For (2,2,3): sqrt(37)/2 ≈ 3.041. Not integer.
        # What about (43-ac)^(1/3)? That's the same as cbrt.
        # What if it's (4^3-ac)/a = (64-ac)/a? For (3,2,2): (64-6)/3 = 58/3. No.
        # What if "43" is "4b" = 8? cbrt(8-6)/3 = cbrt(2)/3. No.
        # What if "43" is "4a"? For (3,2,2): cbrt(12-6)/3 = cbrt(6)/3. No.
        # What if the expression is NOT cbrt but something else entirely?
        # Maybe it's (4³ - ac)/a = (64-ac)/a (no cube root)
        ("(64-ac)/a",            lambda a,b,c: (64-a*c)/a if a else None),
        ("(43-ac)/c",            lambda a,b,c: (43-a*c)/c if c else None),
        # (4^3-ac)/a for (3,2,2) = 58/3. No.
        # What if "ac" is "a+c"? cbrt(43-(a+c))/a
        ("cbrt(43-(a+c))/a",     lambda a,b,c: scbrt(43-a-c)/a if a else None),
        # For (3,2,2): cbrt(43-5)/3 = cbrt(38)/3 ≈ 1.12. No.
        # For (2,2,3): cbrt(43-5)/2 = cbrt(38)/2 ≈ 1.68. No.
        # What about cbrt(a^3-ac)/a = cbrt(a^2*(a-c))/a = cbrt(a-c)*a^(2/3)/a
        # For (3,2,2): cbrt(27-6)/3 = cbrt(21)/3 ≈ 0.92. No.
        # What if the "cbrt" is wrong and it's actually just the expression WITHOUT cbrt?
        ("(43-ac)^2/a",          lambda a,b,c: (43-a*c)**2/a if a else None),
        # For (3,2,2): 37^2/3 = 1369/3. No.
        # What if it's cbrt(a^3 + c)/a? For (3,2,2): cbrt(29)/3 ≈ 1.03. No.
        # What if the whole expression is something COMPLETELY different?
        # Let me try systematic: for (3,2,2) and (2,2,3), what integer values 1-17
        # can be produced?
        # Need: cbrt(EXPR)/a = k => EXPR = (ka)^3
        # For a=3: EXPR = 27k^3. k=1 => 27, k=2 => 216
        # For a=2: EXPR = 8k^3. k=1 => 8, k=2 => 64, k=3 => 216, k=4 => 512>
        # So for a=3: "??-ac" = "??-6" = 27 => "??" = 33
        # For a=2: "??-ac" = "??-6" = 8 => "??" = 14
        # Neither 33 nor 14 looks like "43" in handwriting...
        # BUT: what if ac is wrong? Maybe it's a+c or a-c or bc
        # For a=3,b=2,c=2: if "ac" is "bc": 43-4=39. cbrt(39)/3 ≈ 1.13. No.
        # If "ac" is "a+c": 43-5=38. cbrt(38)/3. No.
        # If "ac" is "a^c": 43-9=34. cbrt(34)/3. No.
        # If "ac" is "c^a": 43-8=35. cbrt(35)/3. No.
        # What if it's cbrt(43-ac)*a? For (3,2,2): cbrt(37)*3 ≈ 9.99. Close to 10!
        ("cbrt(43-ac)*a",        lambda a,b,c: scbrt(43-a*c)*a),
        # cbrt(37)*3 = 3.332*3 = 9.997 ≈ 10! That's very close but not exact.
        # What about cbrt(43-a*c)*c? For (3,2,2): cbrt(37)*2 ≈ 6.665. No.
        # Hmm, 37^(1/3) = 3.3322... not exact.
        # What if it's really 37? cbrt(37)*3 ≈ 9.997. NOT exactly 10.
        # What about cbrt(37+ac) = cbrt(43)? For (3,2,2): cbrt(43)/3. No.
        # I think the "43" might actually be correct and this expression
        # is genuinely blocking these candidates.
        # Let me try even wilder variants:
        ("cbrt(4*3*a-c)/a",      lambda a,b,c: scbrt(12*a-c)/a if a else None),
        ("cbrt(4*3*c-a)/a",      lambda a,b,c: scbrt(12*c-a)/a if a else None),
        # For (3,2,2): cbrt(36-2)/3 = cbrt(34)/3. No.
        # For (3,2,2): cbrt(24-3)/3 = cbrt(21)/3. No.
        # What if expression is (4^3 - a*c)/a (just division, no cbrt)?
        # (64-6)/3 = 58/3. No.
        # What if it's cbrt(4^b - ac)/a? = cbrt(16-ac)/a
        ("cbrt(4^b-ac)/a",       lambda a,b,c: scbrt(4**b-a*c)/a if a else None),
        # For (3,2,2): cbrt(16-6)/3 = cbrt(10)/3 ≈ 0.72. No.
        # What if it's (4b - ac)/a? = (8-6)/3 = 2/3. No.
        # What if it's (4^a - bc)/a?
        ("cbrt(4^a-bc)/a",       lambda a,b,c: scbrt(4**a-b*c)/a if a else None),
        # For (3,2,2): cbrt(64-4)/3 = cbrt(60)/3 ≈ 1.30. No.
        # What if it's cbrt(a^3+c)/a = cbrt(a^3+c)/a
        ("cbrt(a^3+c)/a",        lambda a,b,c: scbrt(a**3+c)/a if a else None),
        # For (3,2,2): cbrt(29)/3 ≈ 1.02. No.
        # What if it's (a^3-4c)/a?
        ("(a^3-4c)/a",           lambda a,b,c: (a**3-4*c)/a if a else None),
        # For (3,2,2): (27-8)/3 = 19/3. No.
        # What if it's (a^3+4c)/a?
        ("(a^3+4c)/a",           lambda a,b,c: (a**3+4*c)/a if a else None),
        # For (3,2,2): (27+8)/3 = 35/3. No.
        # What if cbrt is over different stuff?
        ("cbrt(a*c+43)/a",       lambda a,b,c: scbrt(a*c+43)/a if a else None),
        # For (3,2,2): cbrt(49)/3 ≈ 1.22. No.
        # What if the constant is different? Try 35:
        ("cbrt(35-ac)/a",        lambda a,b,c: scbrt(35-a*c)/a if a else None),
        # For (3,2,2): cbrt(29)/3. No.
        ("cbrt(33-ac)/a",        lambda a,b,c: scbrt(33-a*c)/a if a else None),
        # For (3,2,2): cbrt(27)/3 = 3/3 = 1! YES!
        # For (2,2,3): cbrt(27)/2 = 3/2 = 1.5. No.
        ("cbrt(14-ac)/a",        lambda a,b,c: scbrt(14-a*c)/a if a else None),
        # For (2,2,3): cbrt(8)/2 = 2/2 = 1. YES!
        # For (3,2,2): cbrt(8)/3 = 2/3. No.
        # So 33 works for (3,2,2), 14 works for (2,2,3).
        # Neither is close to 43 visually...
        # BUT: what if it's cbrt(a^3+ac)/a = cbrt(a(a^2+c))/a?
        ("cbrt(a^3+ac)/a",       lambda a,b,c: scbrt(a**3+a*c)/a if a else None),
        # For (3,2,2): cbrt(27+6)/3 = cbrt(33)/3 ≈ 1.07. No.
        # What if the denominator is different? cbrt(43-ac)/(a-1)?
        ("cbrt(43-ac)/(a-1)",    lambda a,b,c: scbrt(43-a*c)/(a-1) if a!=1 else None),
        # For (3,2,2): cbrt(37)/2 ≈ 1.67. No.
        # For (2,2,3): cbrt(37)/1 ≈ 3.33. No.
        # cbrt(43-ac)/(a+c)?
        ("cbrt(43-ac)/(a+c)",    lambda a,b,c: scbrt(43-a*c)/(a+c) if a+c else None),
        # For (3,2,2): cbrt(37)/5 ≈ 0.67. No.
        # What about something completely different: (43-ac)/a^2
        ("(43-ac)/a^2",          lambda a,b,c: (43-a*c)/a**2 if a else None),
        # For (3,2,2): 37/9 ≈ 4.11. No.
        # (4a-c)/a?
        ("(4a-c)/a",             lambda a,b,c: (4*a-c)/a if a else None),
        # For (3,2,2): (12-2)/3 = 10/3. No.
        # (4a+c)/a?
        ("(4a+c)/a",             lambda a,b,c: (4*a+c)/a if a else None),
        # For (3,2,2): (12+2)/3 = 14/3. No.
        # I'll try more constant variations. "43" as handwritten...
        # Maybe "43" is actually "4³" = 64?
        ("cbrt(4^3-ac)/a [=cbrt(64-ac)/a]", lambda a,b,c: scbrt(64-a*c)/a if a else None),
        # For (3,2,2): cbrt(58)/3 ≈ 1.29. No.
        # For (2,2,3): cbrt(58)/2 ≈ 1.94. No.
        # What if "4^3" means "4 cubed" and the cbrt cancels:
        # cbrt(4^3 - ac)/a = cbrt(64-ac)/a. Already tried.
        # Maybe the expression has no cube root and is (4-3ac)/a or (4+3ac)/a?
        ("(4-3*ac)/a",           lambda a,b,c: (4-3*a*c)/a if a else None),
        ("(4+3*ac)/a",           lambda a,b,c: (4+3*a*c)/a if a else None),
        # For (3,2,2): (4+18)/3 = 22/3. No. (4-18)/3 = -14/3. No.
        # (43-a*c) as an exponent?
        # What if the expression is (4*3-a*c)/a = (12-ac)/a?
        ("(12-ac)/a",            lambda a,b,c: (12-a*c)/a if a else None),
        # For (3,2,2): (12-6)/3 = 2. YES!
        # For (2,2,3): (12-6)/2 = 3. YES!
        # BOTH WORK! This is huge. "4*3" misread as "43"!
        # But wait, is "4*3-ac" a plausible reading? In the image, "43" might be "4·3"
        # Or maybe the expression is really (12-ac)/a without the cube root at all.
        ("(12-ac)/c",            lambda a,b,c: (12-a*c)/c if c else None),
        # For (3,2,2): (12-6)/2 = 3. YES!
        # For (2,2,3): (12-6)/3 = 2. YES!
        # Also try (12+ac)/a, (12-bc)/a, etc.
        ("(12+ac)/a",            lambda a,b,c: (12+a*c)/a if a else None),
        ("(12-bc)/a",            lambda a,b,c: (12-b*c)/a if a else None),
        ("(12-ac)/b",            lambda a,b,c: (12-a*c)/b if b else None),
        # cbrt(12-ac)/a
        # For (3,2,2): cbrt(6)/3 ≈ 0.61. No.
        # So the non-cbrt version (12-ac)/a is the key!
        # What if it's (4*3 - ac)/a with explicit multiplication?
        # Or (4·3-ac)/a = 12-ac)/a
        # Let me also try nearby: (13-ac)/a, (11-ac)/a, etc.
        ("(13-ac)/a",            lambda a,b,c: (13-a*c)/a if a else None),
        ("(11-ac)/a",            lambda a,b,c: (11-a*c)/a if a else None),
        ("(14-ac)/a",            lambda a,b,c: (14-a*c)/a if a else None),
        ("(10-ac)/a",            lambda a,b,c: (10-a*c)/a if a else None),
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
    print("COMPREHENSIVE VARIANT SEARCH FOR SUBTILES 2 (V2)")
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

                positions_ordered = sorted(positions, key=lambda p: len(pos_options[p]))

                print(f"  Searching (most constrained first)...")
                results = []
                search_all_assignments(pos_options, positions_ordered, 0,
                                       {}, {}, results, max_results=5)

                if results:
                    for i, result in enumerate(results):
                        print(f"\n  *** SOLUTION {i+1} FOUND for a={a_val}, b={b_val}, c={c_val} ***")
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
