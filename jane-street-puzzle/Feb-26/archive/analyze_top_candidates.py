"""
Focused analysis of top 2 candidates:
  a=4, b=2, c=2 (35/37)
  a=4, b=2, c=3 (35/37)

For each: list all variant values per cell, check count constraint feasibility.
Also try more creative variants for the 2 failing expressions.
"""
import math
from collections import Counter

MAX_N = 17

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

def is_pos_int(x, tol=1e-9):
    if x is None: return False
    try:
        return x > tol and abs(x - round(x)) < tol and round(x) <= MAX_N
    except:
        return False

def get_int(x, tol=1e-9):
    if is_pos_int(x, tol): return int(round(x))
    return None

def safe(f, a, b, c):
    try:
        v = f(a, b, c)
        if v is None or isinstance(v, complex): return None
        if math.isnan(v) or math.isinf(v): return None
        return v
    except:
        return None

# All variant expressions — same as find_variables_v2.py but condensed
# Each entry: list of (name, lambda)
def build_variants():
    V = {}

    V[(0,4)] = [
        ("6c-4b", lambda a,b,c: 6*c-4*b),
        ("6c-4a", lambda a,b,c: 6*c-4*a),
        ("6a-4b", lambda a,b,c: 6*a-4*b),
        ("6c+4b", lambda a,b,c: 6*c+4*b),
        ("6b-4c", lambda a,b,c: 6*b-4*c),
        ("6b-4a", lambda a,b,c: 6*b-4*a),
        ("6c-4", lambda a,b,c: 6*c-4),
    ]
    V[(1,6)] = [
        ("8-b", lambda a,b,c: 8-b),
        ("8-a", lambda a,b,c: 8-a),
        ("8-c", lambda a,b,c: 8-c),
        ("8+b", lambda a,b,c: 8+b),
        ("8/b", lambda a,b,c: 8/b if b else None),
        ("8*b", lambda a,b,c: 8*b),
    ]
    V[(2,1)] = [
        ("(a^b-4)/(6c+1)", lambda a,b,c: (a**b-4)/(6*c+1)),
        ("(a^b-4)/(6a+1)", lambda a,b,c: (a**b-4)/(6*a+1)),
        ("(a^b-4)/(6c-1)", lambda a,b,c: (a**b-4)/(6*c-1) if 6*c!=1 else None),
        ("(c^b-4)/(6c+1)", lambda a,b,c: (c**b-4)/(6*c+1)),
        ("(a^b+4)/(6c+1)", lambda a,b,c: (a**b+4)/(6*c+1)),
        ("(a^c-4)/(6c+1)", lambda a,b,c: (a**c-4)/(6*c+1)),
        ("(a^b-4)/(6b+1)", lambda a,b,c: (a**b-4)/(6*b+1)),
        ("(a^b-4)/(bc+1)", lambda a,b,c: (a**b-4)/(b*c+1)),
        ("(a^b-4)/(ac+1)", lambda a,b,c: (a**b-4)/(a*c+1)),
        ("(a^b-c)/(6c+1)", lambda a,b,c: (a**b-c)/(6*c+1)),
        ("(a^b-4)/(6+c)", lambda a,b,c: (a**b-4)/(6+c)),
        ("(a^b-4)/(6c+b)", lambda a,b,c: (a**b-4)/(6*c+b)),
        ("(a^2-4)/(6c+1)", lambda a,b,c: (a**2-4)/(6*c+1)),
        ("(a^b-a)/(6c+1)", lambda a,b,c: (a**b-a)/(6*c+1)),
        ("(a^b-b)/(6c+1)", lambda a,b,c: (a**b-b)/(6*c+1)),
        ("(a^b-4)/(c+1)", lambda a,b,c: (a**b-4)/(c+1)),
        ("(a^b-4)/(b+1)", lambda a,b,c: (a**b-4)/(b+1)),
        ("(a*b-4)/(6c+1)", lambda a,b,c: (a*b-4)/(6*c+1)),
        ("(a^b-4)/(b*c+1)", lambda a,b,c: (a**b-4)/(b*c+1)),
        ("(a^2-4)/(bc+1)", lambda a,b,c: (a**2-4)/(b*c+1)),
        ("(a^2-4)/(ac+1)", lambda a,b,c: (a**2-4)/(a*c+1)),
        ("(c^b-4)/(6a+1)", lambda a,b,c: (c**b-4)/(6*a+1)),
        ("(a^b-4)/(a+c+1)", lambda a,b,c: (a**b-4)/(a+c+1)),
    ]
    V[(2,3)] = [
        ("(b+c)/(c-1)", lambda a,b,c: (b+c)/(c-1) if c!=1 else None),
        ("(b+c)/(a-1)", lambda a,b,c: (b+c)/(a-1) if a!=1 else None),
        ("(b+a)/(c-1)", lambda a,b,c: (b+a)/(c-1) if c!=1 else None),
        ("(b+a)/(a-1)", lambda a,b,c: (b+a)/(a-1) if a!=1 else None),
        ("(a+c)/(c-1)", lambda a,b,c: (a+c)/(c-1) if c!=1 else None),
        ("(b+c)/(c+1)", lambda a,b,c: (b+c)/(c+1)),
        ("(b-c)/(c-1)", lambda a,b,c: (b-c)/(c-1) if c!=1 else None),
        ("(b+c)/(b-1)", lambda a,b,c: (b+c)/(b-1) if b!=1 else None),
        ("(b*c)/(c-1)", lambda a,b,c: (b*c)/(c-1) if c!=1 else None),
    ]
    V[(2,5)] = [
        ("b²-b/c", lambda a,b,c: b**2-b/c if c else None),
        ("b²-b/a", lambda a,b,c: b**2-b/a if a else None),
        ("b²-b*c", lambda a,b,c: b**2-b*c),
        ("b²+b/c", lambda a,b,c: b**2+b/c if c else None),
        ("b²-a/c", lambda a,b,c: b**2-a/c if c else None),
        ("b²-b*a", lambda a,b,c: b**2-b*a),
        ("b²+b*c", lambda a,b,c: b**2+b*c),
        ("b²-b", lambda a,b,c: b**2-b),
        ("b²+b/a", lambda a,b,c: b**2+b/a if a else None),
    ]
    V[(2,7)] = [
        ("√(30+a)/c", lambda a,b,c: ssqrt(30+a)/c if c else None),
        ("√(3c+a)/c", lambda a,b,c: ssqrt(3*c+a)/c if c else None),
        ("√(30+a)/a", lambda a,b,c: ssqrt(30+a)/a if a else None),
        ("√(3c+a)/a", lambda a,b,c: ssqrt(3*c+a)/a if a else None),
        ("(30+a)/c", lambda a,b,c: (30+a)/c if c else None),
        ("(3c+a)/c", lambda a,b,c: (3*c+a)/c if c else None),
        ("(30+c)/c", lambda a,b,c: (30+c)/c if c else None),
        ("(3c+a)/a", lambda a,b,c: (3*c+a)/a if a else None),
        ("(3c+b)/c", lambda a,b,c: (3*c+b)/c if c else None),
        ("(30-a)/a", lambda a,b,c: (30-a)/a if a else None),
        ("(30-c)/c", lambda a,b,c: (30-c)/c if c else None),
        ("(30+a)/(a+c)", lambda a,b,c: (30+a)/(a+c) if a+c else None),
        ("(3a+c)/c", lambda a,b,c: (3*a+c)/c if c else None),
        ("(3b+a)/a", lambda a,b,c: (3*b+a)/a if a else None),
        ("(3a+b)/c", lambda a,b,c: (3*a+b)/c if c else None),
    ]
    V[(2,9)] = [
        ("(a+b)/(c-3a)", lambda a,b,c: (a+b)/(c-3*a) if c!=3*a else None),
        ("(a+b)/(c+3a)", lambda a,b,c: (a+b)/(c+3*a)),
        ("(a+b)/(3a-c)", lambda a,b,c: (a+b)/(3*a-c) if 3*a!=c else None),
        ("(a+b)/(a-c)", lambda a,b,c: (a+b)/(a-c) if a!=c else None),
        ("(a+b)/(c-a)", lambda a,b,c: (a+b)/(c-a) if c!=a else None),
        ("(a+b)/(3c-a)", lambda a,b,c: (a+b)/(3*c-a) if 3*c!=a else None),
        ("(a+b)/(c-3b)", lambda a,b,c: (a+b)/(c-3*b) if c!=3*b else None),
    ]
    V[(3,4)] = [
        ("(b-3a)/(a-c)", lambda a,b,c: (b-3*a)/(a-c) if a!=c else None),
        ("(b-3a)/(c-a)", lambda a,b,c: (b-3*a)/(c-a) if c!=a else None),
        ("(b+3a)/(a-c)", lambda a,b,c: (b+3*a)/(a-c) if a!=c else None),
        ("(b-3c)/(a-c)", lambda a,b,c: (b-3*c)/(a-c) if a!=c else None),
        ("(3a-b)/(a-c)", lambda a,b,c: (3*a-b)/(a-c) if a!=c else None),
        ("(b-3a)/(a+c)", lambda a,b,c: (b-3*a)/(a+c) if a+c else None),
        ("(b-a)/(a-c)", lambda a,b,c: (b-a)/(a-c) if a!=c else None),
        ("(b²-3a)/(a-c)", lambda a,b,c: (b**2-3*a)/(a-c) if a!=c else None),
    ]
    V[(3,6)] = [
        ("8a-2b", lambda a,b,c: 8*a-2*b),
        ("8c-2b", lambda a,b,c: 8*c-2*b),
        ("8a+2b", lambda a,b,c: 8*a+2*b),
        ("8a-2c", lambda a,b,c: 8*a-2*c),
        ("8b-2a", lambda a,b,c: 8*b-2*a),
        ("8a-2", lambda a,b,c: 8*a-2),
        ("8a-b", lambda a,b,c: 8*a-b),
    ]
    V[(3,8)] = [
        ("b/(a-c)", lambda a,b,c: b/(a-c) if a!=c else None),
        ("b/(c-a)", lambda a,b,c: b/(c-a) if c!=a else None),
        ("a/(a-c)", lambda a,b,c: a/(a-c) if a!=c else None),
        ("c/(a-c)", lambda a,b,c: c/(a-c) if a!=c else None),
        ("b/(a+c)", lambda a,b,c: b/(a+c) if a+c else None),
        ("b/(a*c)", lambda a,b,c: b/(a*c) if a*c else None),
    ]
    V[(3,10)] = [
        ("(b+9)/√(c-a)", lambda a,b,c: (b+9)/ssqrt(c-a) if c>a else None),
        ("(b+9)/√(a-c)", lambda a,b,c: (b+9)/ssqrt(a-c) if a>c else None),
        ("(b+9)/√(c+a)", lambda a,b,c: (b+9)/ssqrt(c+a)),
        ("(b+9)/(c-a)", lambda a,b,c: (b+9)/(c-a) if c!=a else None),
        ("(b+9)/(a-c)", lambda a,b,c: (b+9)/(a-c) if a!=c else None),
        ("(b+a)/√(a-c)", lambda a,b,c: (b+a)/ssqrt(a-c) if a>c else None),
        ("(b+c)/√(a-c)", lambda a,b,c: (b+c)/ssqrt(a-c) if a>c else None),
        # More creative: what if "9" is actually "a" or "c"?
        ("(b+a)/(a-c)", lambda a,b,c: (b+a)/(a-c) if a!=c else None),
        ("(b+c)/(a-c)", lambda a,b,c: (b+c)/(a-c) if a!=c else None),
        ("(b+a)/(c-a)", lambda a,b,c: (b+a)/(c-a) if c!=a else None),
        ("(b+c)/(c-a)", lambda a,b,c: (b+c)/(c-a) if c!=a else None),
        ("(b+9)/(a+c)", lambda a,b,c: (b+9)/(a+c) if a+c else None),
        # What if b+9 is b·9 or b^9?
        ("(b*9)/√(a-c)", lambda a,b,c: (b*9)/ssqrt(a-c) if a>c else None),
        # What if it's (b+9)/√(c*a)?
        ("(b+9)/√(c*a)", lambda a,b,c: (b+9)/ssqrt(c*a) if c*a>0 else None),
        # What if it's (a+9)/√(c-a) etc?
        ("(a+9)/√(a-c)", lambda a,b,c: (a+9)/ssqrt(a-c) if a>c else None),
        ("(c+9)/√(a-c)", lambda a,b,c: (c+9)/ssqrt(a-c) if a>c else None),
        # What if the sqrt is over the whole thing?
        ("√((b+9)/(a-c))", lambda a,b,c: ssqrt((b+9)/(a-c)) if a>c else None),
        # What if it's (b+9)·√(a-c)?
        ("(b+9)*√(a-c)", lambda a,b,c: (b+9)*ssqrt(a-c) if a>c else None),
        # What if it's (b+9)/(c²-a)?
        ("(b+9)/(c²-a)", lambda a,b,c: (b+9)/(c**2-a) if c**2!=a else None),
        ("(b+9)/(a-c²)", lambda a,b,c: (b+9)/(a-c**2) if a!=c**2 else None),
        ("(b+9)/(a²-c)", lambda a,b,c: (b+9)/(a**2-c) if a**2!=c else None),
    ]
    V[(4,1)] = [
        ("18/(ac+1)", lambda a,b,c: 18/(a*c+1)),
        ("18/(a+c+1)", lambda a,b,c: 18/(a+c+1)),
        ("18/(ac-1)", lambda a,b,c: 18/(a*c-1) if a*c!=1 else None),
        ("18/(bc+1)", lambda a,b,c: 18/(b*c+1)),
        ("18/(a+c)", lambda a,b,c: 18/(a+c) if a+c else None),
        ("18/(a*b+1)", lambda a,b,c: 18/(a*b+1)),
    ]
    V[(4,5)] = [
        ("c^b", lambda a,b,c: c**b),
        ("c^a", lambda a,b,c: c**a),
        ("a^b", lambda a,b,c: a**b),
        ("a^c", lambda a,b,c: a**c),
        ("c*b", lambda a,b,c: c*b),
        ("c+b", lambda a,b,c: c+b),
        ("a*b", lambda a,b,c: a*b),
        ("b^c", lambda a,b,c: b**c),
        ("b^a", lambda a,b,c: b**a),
    ]
    V[(4,9)] = [
        ("(3+b²)/√(3+2c)", lambda a,b,c: (3+b**2)/ssqrt(3+2*c)),
        ("(3+b²)/√(3+2a)", lambda a,b,c: (3+b**2)/ssqrt(3+2*a)),
        ("(3+a²)/√(3+2c)", lambda a,b,c: (3+a**2)/ssqrt(3+2*c)),
        ("(3+b²)/(3+2c)", lambda a,b,c: (3+b**2)/(3+2*c)),
        ("(3+b²)/(3+2a)", lambda a,b,c: (3+b**2)/(3+2*a)),
        ("(a+b²)/√(3+2c)", lambda a,b,c: (a+b**2)/ssqrt(3+2*c)),
        ("(c+b²)/√(3+2c)", lambda a,b,c: (c+b**2)/ssqrt(3+2*c)),
        ("(3+b²)/√(a+2c)", lambda a,b,c: (3+b**2)/ssqrt(a+2*c)),
    ]
    V[(5,3)] = [
        ("b/(a²-c²)", lambda a,b,c: b/(a**2-c**2) if a**2!=c**2 else None),
        ("b/(c²-a²)", lambda a,b,c: b/(c**2-a**2) if c**2!=a**2 else None),
        ("b/(a²+c²)", lambda a,b,c: b/(a**2+c**2)),
        ("a/(a²-c²)", lambda a,b,c: a/(a**2-c**2) if a**2!=c**2 else None),
        ("c/(a²-c²)", lambda a,b,c: c/(a**2-c**2) if a**2!=c**2 else None),
        ("b/((a-c)²)", lambda a,b,c: b/((a-c)**2) if a!=c else None),
        ("b/((a+c)²)", lambda a,b,c: b/((a+c)**2)),
        # More creative variants
        ("b/(a-c)", lambda a,b,c: b/(a-c) if a!=c else None),
        ("b/(c-a)", lambda a,b,c: b/(c-a) if c!=a else None),
        ("b/(a+c)", lambda a,b,c: b/(a+c) if a+c else None),
        ("b/(a*c)", lambda a,b,c: b/(a*c) if a*c else None),
        # What if it's b·(a²-c²)?
        ("b*(a²-c²)", lambda a,b,c: b*(a**2-c**2)),
        # What if the exponent is different?
        ("b/(a³-c³)", lambda a,b,c: b/(a**3-c**3) if a**3!=c**3 else None),
        ("b/(a-c²)", lambda a,b,c: b/(a-c**2) if a!=c**2 else None),
        ("b/(a²-c)", lambda a,b,c: b/(a**2-c) if a**2!=c else None),
        # What if b is in the denominator?
        ("a/(a-c)²", lambda a,b,c: a/((a-c)**2) if a!=c else None),
        # What if it's (a²-c²)/b?
        ("(a²-c²)/b", lambda a,b,c: (a**2-c**2)/b if b else None),
        # What if it's b²/(a²-c²)?
        ("b²/(a²-c²)", lambda a,b,c: b**2/(a**2-c**2) if a**2!=c**2 else None),
        # What if it's ab/(a²-c²) = a/(a+c) when factored?
        ("a*b/(a²-c²)", lambda a,b,c: a*b/(a**2-c**2) if a**2!=c**2 else None),
    ]
    V[(5,10)] = [
        ("√(a+2)/a", lambda a,b,c: ssqrt(a+2)/a if a else None),
        ("√(a+c)/a", lambda a,b,c: ssqrt(a+c)/a if a else None),
        ("√(c+2)/a", lambda a,b,c: ssqrt(c+2)/a if a else None),
        ("√(c+2)/c", lambda a,b,c: ssqrt(c+2)/c if c else None),
        ("√(a+2)/c", lambda a,b,c: ssqrt(a+2)/c if c else None),
        ("(a+2)/a", lambda a,b,c: (a+2)/a if a else None),
        ("(a+c)/a", lambda a,b,c: (a+c)/a if a else None),
        ("(c+2)/c", lambda a,b,c: (c+2)/c if c else None),
        ("(a+2)/c", lambda a,b,c: (a+2)/c if c else None),
        ("√(a+2)*a", lambda a,b,c: ssqrt(a+2)*a),
        ("√(a+2)*c", lambda a,b,c: ssqrt(a+2)*c),
        ("(a+2)/(a+c)", lambda a,b,c: (a+2)/(a+c)),
        ("(a+b)/a", lambda a,b,c: (a+b)/a if a else None),
    ]
    V[(6,2)] = [
        ("a^b-12/a", lambda a,b,c: a**b-12/a if a else None),
        ("a^b-12/c", lambda a,b,c: a**b-12/c if c else None),
        ("a^b+12/a", lambda a,b,c: a**b+12/a if a else None),
        ("a^b-12*a", lambda a,b,c: a**b-12*a),
        ("c^b-12/a", lambda a,b,c: c**b-12/a if a else None),
        ("a^b-12", lambda a,b,c: a**b-12),
        ("a^b-1/a", lambda a,b,c: a**b-1/a if a else None),
        ("a^b-12/b", lambda a,b,c: a**b-12/b if b else None),
        ("a^b-a/c", lambda a,b,c: a**b-a/c if c else None),
    ]
    V[(6,4)] = [
        ("2c+c/a", lambda a,b,c: 2*c+c/a if a else None),
        ("2c+a/c", lambda a,b,c: 2*c+a/c if c else None),
        ("2a+c/a", lambda a,b,c: 2*a+c/a if a else None),
        ("2a+a/c", lambda a,b,c: 2*a+a/c if c else None),
        ("2c+c/b", lambda a,b,c: 2*c+c/b if b else None),
        ("2c-c/a", lambda a,b,c: 2*c-c/a if a else None),
        ("2c*c/a", lambda a,b,c: 2*c*c/a if a else None),
        ("2c+b/a", lambda a,b,c: 2*c+b/a if a else None),
        ("2c+b/c", lambda a,b,c: 2*c+b/c if c else None),
    ]
    V[(6,6)] = [
        ("4a-5b", lambda a,b,c: 4*a-5*b),
        ("4a+5b", lambda a,b,c: 4*a+5*b),
        ("4c-5b", lambda a,b,c: 4*c-5*b),
        ("4a-5c", lambda a,b,c: 4*a-5*c),
        ("5a-4b", lambda a,b,c: 5*a-4*b),
        ("4a-5", lambda a,b,c: 4*a-5),
        ("4a-b", lambda a,b,c: 4*a-b),
    ]
    V[(6,8)] = [
        ("c+2a", lambda a,b,c: c+2*a),
        ("c+2b", lambda a,b,c: c+2*b),
        ("a+2c", lambda a,b,c: a+2*c),
        ("a+2b", lambda a,b,c: a+2*b),
        ("c+2*c", lambda a,b,c: c+2*c),
        ("c*2a", lambda a,b,c: c*2*a),
        ("c+a", lambda a,b,c: c+a),
        ("c-2a", lambda a,b,c: c-2*a),
    ]
    V[(6,10)] = [
        ("b/(9a-5c)", lambda a,b,c: b/(9*a-5*c) if 9*a!=5*c else None),
        ("b/(9a+5c)", lambda a,b,c: b/(9*a+5*c)),
        ("b/(9c-5a)", lambda a,b,c: b/(9*c-5*a) if 9*c!=5*a else None),
        ("b/(5c-9a)", lambda a,b,c: b/(5*c-9*a) if 5*c!=9*a else None),
        ("a/(9a-5c)", lambda a,b,c: a/(9*a-5*c) if 9*a!=5*c else None),
        ("c/(9a-5c)", lambda a,b,c: c/(9*a-5*c) if 9*a!=5*c else None),
        ("b/(9a-5b)", lambda a,b,c: b/(9*a-5*b) if 9*a!=5*b else None),
        ("b/(a-5c)", lambda a,b,c: b/(a-5*c) if a!=5*c else None),
    ]
    V[(7,0)] = [
        ("(b³+2c)/(b+2c)", lambda a,b,c: (b**3+2*c)/(b+2*c) if b+2*c else None),
        ("(b³+2c)/(b+2a)", lambda a,b,c: (b**3+2*c)/(b+2*a) if b+2*a else None),
        ("(b²+2c)/(b+2c)", lambda a,b,c: (b**2+2*c)/(b+2*c) if b+2*c else None),
        ("(b³+2a)/(b+2a)", lambda a,b,c: (b**3+2*a)/(b+2*a) if b+2*a else None),
        ("(a³+2c)/(a+2c)", lambda a,b,c: (a**3+2*c)/(a+2*c) if a+2*c else None),
        ("(b³+2c)/(b+c)", lambda a,b,c: (b**3+2*c)/(b+c) if b+c else None),
        ("(b³+2c)/(b*2c)", lambda a,b,c: (b**3+2*c)/(b*2*c) if b*c else None),
        ("(b³+2c)/(a+2c)", lambda a,b,c: (b**3+2*c)/(a+2*c) if a+2*c else None),
    ]
    V[(7,8)] = [
        ("b/(a-1)", lambda a,b,c: b/(a-1) if a!=1 else None),
        ("a/(a-1)", lambda a,b,c: a/(a-1) if a!=1 else None),
        ("c/(a-1)", lambda a,b,c: c/(a-1) if a!=1 else None),
        ("b/(c-1)", lambda a,b,c: b/(c-1) if c!=1 else None),
        ("b/(a+1)", lambda a,b,c: b/(a+1)),
        ("b/(a-c)", lambda a,b,c: b/(a-c) if a!=c else None),
        ("a/(c-1)", lambda a,b,c: a/(c-1) if c!=1 else None),
    ]
    V[(8,2)] = [
        ("(c-b)/(2a)", lambda a,b,c: (c-b)/(2*a) if a else None),
        ("(c-b)/(2c)", lambda a,b,c: (c-b)/(2*c) if c else None),
        ("(c+b)/(2a)", lambda a,b,c: (c+b)/(2*a) if a else None),
        ("(a-b)/(2a)", lambda a,b,c: (a-b)/(2*a) if a else None),
        ("(a-b)/(2c)", lambda a,b,c: (a-b)/(2*c) if c else None),
        ("(c-b)*2a", lambda a,b,c: (c-b)*2*a),
        ("(c-b)/(2b)", lambda a,b,c: (c-b)/(2*b) if b else None),
        ("(b-c)/(2a)", lambda a,b,c: (b-c)/(2*a) if a else None),
        ("(c-a)/(2b)", lambda a,b,c: (c-a)/(2*b) if b else None),
        ("(a-c)/(2b)", lambda a,b,c: (a-c)/(2*b) if b else None),
    ]
    V[(8,6)] = [
        ("b/(a-c)", lambda a,b,c: b/(a-c) if a!=c else None),
        ("b/(c-a)", lambda a,b,c: b/(c-a) if c!=a else None),
        ("a/(a-c)", lambda a,b,c: a/(a-c) if a!=c else None),
        ("c/(a-c)", lambda a,b,c: c/(a-c) if a!=c else None),
        ("b/(a+c)", lambda a,b,c: b/(a+c) if a+c else None),
        ("b²/(a-c)", lambda a,b,c: b**2/(a-c) if a!=c else None),
    ]
    V[(8,10)] = [
        ("(b+c)/(a-c)", lambda a,b,c: (b+c)/(a-c) if a!=c else None),
        ("(b+c)/(c-a)", lambda a,b,c: (b+c)/(c-a) if c!=a else None),
        ("(b+a)/(a-c)", lambda a,b,c: (b+a)/(a-c) if a!=c else None),
        ("(b-c)/(a-c)", lambda a,b,c: (b-c)/(a-c) if a!=c else None),
        ("(a+c)/(a-c)", lambda a,b,c: (a+c)/(a-c) if a!=c else None),
        ("(b+c)/(a+c)", lambda a,b,c: (b+c)/(a+c) if a+c else None),
    ]
    V[(9,2)] = [
        ("log_c(a)", lambda a,b,c: slog(c, a)),
        ("log_a(c)", lambda a,b,c: slog(a, c)),
        ("log_c(b)", lambda a,b,c: slog(c, b)),
        ("log_a(b)", lambda a,b,c: slog(a, b)),
        ("log_b(a)", lambda a,b,c: slog(b, a)),
        ("log_b(c)", lambda a,b,c: slog(b, c)),
    ]
    V[(9,4)] = [
        ("(c²-b)/a", lambda a,b,c: (c**2-b)/a if a else None),
        ("(c²-b)/c", lambda a,b,c: (c**2-b)/c if c else None),
        ("(c²+b)/a", lambda a,b,c: (c**2+b)/a if a else None),
        ("(c²-a)/a", lambda a,b,c: (c**2-a)/a if a else None),
        ("(a²-b)/c", lambda a,b,c: (a**2-b)/c if c else None),
        ("(a²-b)/a", lambda a,b,c: (a**2-b)/a if a else None),
        ("(c²-b)/b", lambda a,b,c: (c**2-b)/b if b else None),
        ("(a²-c)/b", lambda a,b,c: (a**2-c)/b if b else None),
        ("(a²+b)/c", lambda a,b,c: (a**2+b)/c if c else None),
    ]
    V[(9,6)] = [
        ("(b-1)²", lambda a,b,c: (b-1)**2),
        ("(a-1)²", lambda a,b,c: (a-1)**2),
        ("(c-1)²", lambda a,b,c: (c-1)**2),
        ("(b+1)²", lambda a,b,c: (b+1)**2),
        ("(b-1)³", lambda a,b,c: (b-1)**3),
        ("b²-1", lambda a,b,c: b**2-1),
    ]
    V[(9,8)] = [
        ("∛(43-ac)/a", lambda a,b,c: scbrt(43-a*c)/a if a else None),
        ("∛(43-ac)/c", lambda a,b,c: scbrt(43-a*c)/c if c else None),
        ("∛(4a-ac)/a", lambda a,b,c: scbrt(4*a-a*c)/a if a else None),
        ("∛(43-bc)/a", lambda a,b,c: scbrt(43-b*c)/a if a else None),
        ("∛(43+ac)/a", lambda a,b,c: scbrt(43+a*c)/a if a else None),
        ("∛(43-ab)/a", lambda a,b,c: scbrt(43-a*b)/a if a else None),
        ("∛(43-ac)/b", lambda a,b,c: scbrt(43-a*c)/b if b else None),
        ("(43-ac)/a", lambda a,b,c: (43-a*c)/a if a else None),
        ("∛(43-a)/c", lambda a,b,c: scbrt(43-a)/c if c else None),
        ("∛(43-c)/a", lambda a,b,c: scbrt(43-c)/a if a else None),
        # What if 43 is 4·3 = 12? Or 4^3=64?
        ("∛(4*3-ac)/a", lambda a,b,c: scbrt(12-a*c)/a if a else None),
        # What if 43 is really "4c" or "4a" or "4b"?
        ("∛(4c-ac)/a", lambda a,b,c: scbrt(4*c-a*c)/a if a else None),
        ("∛(4b-ac)/a", lambda a,b,c: scbrt(4*b-a*c)/a if a else None),
        # What if 43 is 33?
        ("∛(33-ac)/a", lambda a,b,c: scbrt(33-a*c)/a if a else None),
        # What if it's (43-ac)^(1/a)?
        ("(43-ac)^(1/a)", lambda a,b,c: (43-a*c)**(1/a) if 43>a*c and a else None),
    ]
    V[(10,3)] = [
        ("(b-a)/(a-c)", lambda a,b,c: (b-a)/(a-c) if a!=c else None),
        ("(b-a)/(c-a)", lambda a,b,c: (b-a)/(c-a) if c!=a else None),
        ("(a-b)/(a-c)", lambda a,b,c: (a-b)/(a-c) if a!=c else None),
        ("(b-c)/(a-c)", lambda a,b,c: (b-c)/(a-c) if a!=c else None),
        ("(b+a)/(a-c)", lambda a,b,c: (b+a)/(a-c) if a!=c else None),
        ("(b-a)/(a+c)", lambda a,b,c: (b-a)/(a+c) if a+c else None),
    ]
    V[(10,5)] = [
        ("11-b", lambda a,b,c: 11-b),
        ("11-a", lambda a,b,c: 11-a),
        ("11-c", lambda a,b,c: 11-c),
        ("11+b", lambda a,b,c: 11+b),
        ("11*b", lambda a,b,c: 11*b),
        ("11/b", lambda a,b,c: 11/b if b else None),
    ]
    V[(10,7)] = [
        ("(b-2a)/(a-c)", lambda a,b,c: (b-2*a)/(a-c) if a!=c else None),
        ("(b-2a)/(c-a)", lambda a,b,c: (b-2*a)/(c-a) if c!=a else None),
        ("(b+2a)/(a-c)", lambda a,b,c: (b+2*a)/(a-c) if a!=c else None),
        ("(b-2c)/(a-c)", lambda a,b,c: (b-2*c)/(a-c) if a!=c else None),
        ("(2a-b)/(a-c)", lambda a,b,c: (2*a-b)/(a-c) if a!=c else None),
        ("(b-2a)/(a+c)", lambda a,b,c: (b-2*a)/(a+c) if a+c else None),
    ]
    V[(10,9)] = [
        ("(c+3)/a", lambda a,b,c: (c+3)/a if a else None),
        ("(c+3)/c", lambda a,b,c: (c+3)/c if c else None),
        ("(a+3)/a", lambda a,b,c: (a+3)/a if a else None),
        ("(a+3)/c", lambda a,b,c: (a+3)/c if c else None),
        ("(c+3)/b", lambda a,b,c: (c+3)/b if b else None),
        ("(c+a)/a", lambda a,b,c: (c+a)/a if a else None),
        ("(c+a)/c", lambda a,b,c: (c+a)/c if c else None),
        ("(b+3)/a", lambda a,b,c: (b+3)/a if a else None),
    ]
    V[(10,11)] = [
        ("8c-b/c", lambda a,b,c: 8*c-b/c if c else None),
        ("8c+b/c", lambda a,b,c: 8*c+b/c if c else None),
        ("8c-a/c", lambda a,b,c: 8*c-a/c if c else None),
        ("8c-b/a", lambda a,b,c: 8*c-b/a if a else None),
        ("8a-b/c", lambda a,b,c: 8*a-b/c if c else None),
        ("8c-b*c", lambda a,b,c: 8*c-b*c),
        ("8a-b/a", lambda a,b,c: 8*a-b/a if a else None),
        ("8c-b", lambda a,b,c: 8*c-b),
        ("8a-b*a", lambda a,b,c: 8*a-b*a),
        ("8a-b", lambda a,b,c: 8*a-b),
    ]
    V[(11,5)] = [
        ("b²", lambda a,b,c: b**2),
        ("a²", lambda a,b,c: a**2),
        ("c²", lambda a,b,c: c**2),
        ("b*a", lambda a,b,c: b*a),
        ("b*c", lambda a,b,c: b*c),
        ("b+c", lambda a,b,c: b+c),
    ]
    V[(12,8)] = [
        ("(2^b+1)/(ac)", lambda a,b,c: (2**b+1)/(a*c) if a*c else None),
        ("(2^b+1)/(a+c)", lambda a,b,c: (2**b+1)/(a+c) if a+c else None),
        ("(2^b-1)/(ac)", lambda a,b,c: (2**b-1)/(a*c) if a*c else None),
        ("(2^b+1)/(bc)", lambda a,b,c: (2**b+1)/(b*c) if b*c else None),
        ("(2^a+1)/(ac)", lambda a,b,c: (2**a+1)/(a*c) if a*c else None),
        ("(2^b+1)/(ab)", lambda a,b,c: (2**b+1)/(a*b) if a*b else None),
        ("(2^a+1)/(bc)", lambda a,b,c: (2**a+1)/(b*c) if b*c else None),
        ("(2^b+1)/(a-c)", lambda a,b,c: (2**b+1)/(a-c) if a!=c else None),
        ("(2^b+a)/(ac)", lambda a,b,c: (2**b+a)/(a*c) if a*c else None),
        ("(2^b+c)/(ac)", lambda a,b,c: (2**b+c)/(a*c) if a*c else None),
        ("(2^a+1)/(a+c)", lambda a,b,c: (2**a+1)/(a+c) if a+c else None),
    ]
    return V

# ============================================================
# MAIN ANALYSIS
# ============================================================

VARIANTS = build_variants()

candidates = [
    (4, 2, 2),
    (4, 2, 3),
    (3, 2, 2),
    (2, 2, 3),
    (3, 2, 4),
]

for a, b, c in candidates:
    print("=" * 70)
    print(f"  CANDIDATE: a={a}, b={b}, c={c}")
    print("=" * 70)

    all_options = {}  # pos -> list of (name, value)

    for pos in sorted(VARIANTS.keys()):
        options = []
        for name, func in VARIANTS[pos]:
            v = safe(func, a, b, c)
            iv = get_int(v)
            if iv is not None:
                options.append((name, iv))
        all_options[pos] = options

    sat_count = sum(1 for opts in all_options.values() if opts)
    unsat = [pos for pos in sorted(VARIANTS.keys()) if not all_options[pos]]

    print(f"  Satisfiable: {sat_count}/37, Unsatisfiable: {37-sat_count}")
    if unsat:
        print(f"  Unsatisfiable positions: {unsat}")

    print(f"\n  All positions and possible values:")
    for pos in sorted(VARIANTS.keys()):
        opts = all_options[pos]
        if opts:
            vals = sorted(set(v for _, v in opts))
            names = [(n, v) for n, v in opts]
            print(f"    {str(pos):10s}: values={vals}")
            for n, v in names:
                print(f"      {n:35s} -> {v}")
        else:
            print(f"    {str(pos):10s}: *** NO VALID VARIANT ***")
            # Show what we got
            for name, func in VARIANTS[pos]:
                v = safe(func, a, b, c)
                v_str = f"{v:.4f}" if v is not None else "UNDEF"
                print(f"      {name:35s} -> {v_str}")

    # Count constraint check
    print(f"\n  COUNT CONSTRAINT ANALYSIS:")
    if unsat:
        print(f"  (Skipping full solver — {len(unsat)} unsatisfiable positions)")
        print(f"  Checking feasibility for {sat_count} satisfiable positions...")

    # For each satisfiable position, get the set of possible values
    pos_values = {}
    for pos in sorted(VARIANTS.keys()):
        if all_options[pos]:
            vals = sorted(set(v for _, v in all_options[pos]))
            pos_values[pos] = vals

    # Quick check: for each possible value, how many positions CAN produce it?
    from collections import defaultdict
    value_producers = defaultdict(list)
    for pos, vals in pos_values.items():
        for v in vals:
            value_producers[v].append(pos)

    print(f"\n  Value distribution (how many cells CAN produce each value):")
    for v in sorted(value_producers.keys()):
        prods = value_producers[v]
        limit = v  # count constraint: value k appears at most k times
        status = "OK" if len(prods) <= limit else f"TIGHT ({len(prods)} producers, limit {limit})"
        print(f"    value {v:2d}: {len(prods):2d} possible producers (limit {v:2d}) {status}")

    # Greedy check: try to assign each position the LARGEST possible value
    # to spread out the counts
    print(f"\n  Greedy assignment (prefer larger values):")
    counts = Counter()
    assignment = {}
    failed_positions = []

    # Sort positions by number of options (most constrained first)
    sorted_positions = sorted(pos_values.keys(), key=lambda p: len(pos_values[p]))

    for pos in sorted_positions:
        vals = pos_values[pos]
        # Try values from largest to smallest
        assigned = False
        for v in sorted(vals, reverse=True):
            if counts[v] < v:
                assignment[pos] = v
                counts[v] += 1
                assigned = True
                break
        if not assigned:
            # Try any value
            for v in sorted(vals):
                if counts[v] < v:
                    assignment[pos] = v
                    counts[v] += 1
                    assigned = True
                    break
            if not assigned:
                failed_positions.append(pos)

    if failed_positions:
        print(f"    FAILED to assign {len(failed_positions)} positions: {failed_positions}")
    else:
        print(f"    SUCCESS! All {len(assignment)} positions assigned.")

    print(f"    Assignment:")
    for pos in sorted(assignment.keys()):
        print(f"      {str(pos):10s} = {assignment[pos]:2d}")

    if not failed_positions:
        print(f"\n    Value counts:")
        for v in sorted(counts.keys()):
            print(f"      value {v:2d}: used {counts[v]}x (limit {v})")

        # Compute row sums
        rows = defaultdict(list)
        for (r, col), val in assignment.items():
            rows[r].append(val)

        print(f"\n    Row sums (labeled cells only):")
        row_sums = {}
        for r in sorted(rows.keys()):
            s = sum(rows[r])
            row_sums[r] = s
            print(f"      row {r:2d}: {rows[r]} = {s}")

        nonzero_sums = [s for s in row_sums.values() if s > 0]
        if nonzero_sums:
            min_s = min(nonzero_sums)
            max_s = max(nonzero_sums)
            print(f"\n    min_row_sum = {min_s}, max_row_sum = {max_s}")
            print(f"    ANSWER = {min_s} * {max_s} = {min_s * max_s}")

    print()
