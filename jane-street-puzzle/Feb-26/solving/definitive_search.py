"""
Definitive search for (a, b, c) using ORIGINAL expressions only.
No variants — user confirmed expressions are correct.

Key question: which (a,b,c) makes the most expressions evaluate to positive integers?
"""
import math
from collections import Counter, defaultdict

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

def safe(f, a, b, c):
    try:
        v = f(a, b, c)
        if v is None or isinstance(v, complex): return None
        if math.isnan(v) or math.isinf(v): return None
        return v
    except:
        return None

def is_pos_int(v, max_n=None):
    """Check if v is a positive integer (optionally ≤ max_n)"""
    if v is None: return False
    if v <= 1e-9: return False
    if abs(v - round(v)) > 1e-9: return False
    iv = int(round(v))
    if max_n and iv > max_n: return False
    return True

# ALL 37 ORIGINAL expressions — no variants
EXPR = {
    (0,4):   ("6c-4b",              lambda a,b,c: 6*c - 4*b),
    (1,6):   ("8-b",                lambda a,b,c: 8 - b),
    (2,1):   ("(a^b-4)/(6c+1)",     lambda a,b,c: (a**b - 4)/(6*c + 1)),
    (2,3):   ("(b+c)/(c-1)",        lambda a,b,c: (b + c)/(c - 1) if c != 1 else None),
    (2,5):   ("b²-b/c",             lambda a,b,c: b**2 - b/c if c else None),
    (2,7):   ("√(30+a)/c",          lambda a,b,c: ssqrt(30 + a)/c if c else None),
    (2,9):   ("(a+b)/(c-3a)",       lambda a,b,c: (a + b)/(c - 3*a) if c != 3*a else None),
    (3,4):   ("(b-3a)/(a-c)",       lambda a,b,c: (b - 3*a)/(a - c) if a != c else None),
    (3,6):   ("8a-2b",              lambda a,b,c: 8*a - 2*b),
    (3,8):   ("b/(a-c)",            lambda a,b,c: b/(a - c) if a != c else None),
    (3,10):  ("(b+9)/√(c-a)",       lambda a,b,c: (b + 9)/ssqrt(c - a) if c > a else None),
    (4,1):   ("18/(ac+1)",          lambda a,b,c: 18/(a*c + 1)),
    (4,5):   ("c^b",                lambda a,b,c: c**b),
    (4,9):   ("(3+b²)/√(3+2c)",     lambda a,b,c: (3 + b**2)/ssqrt(3 + 2*c)),
    (5,3):   ("b/(a²-c²)",          lambda a,b,c: b/(a**2 - c**2) if a**2 != c**2 else None),
    (5,10):  ("√(a+2)/a",           lambda a,b,c: ssqrt(a + 2)/a if a else None),
    (6,2):   ("a^b-12/a",           lambda a,b,c: a**b - 12/a if a else None),
    (6,4):   ("2c+c/a",             lambda a,b,c: 2*c + c/a if a else None),
    (6,6):   ("4a-5b",              lambda a,b,c: 4*a - 5*b),
    (6,8):   ("c+2a",               lambda a,b,c: c + 2*a),
    (6,10):  ("b/(9a-5c)",          lambda a,b,c: b/(9*a - 5*c) if 9*a != 5*c else None),
    (7,0):   ("(b³+2c)/(b+2c)",     lambda a,b,c: (b**3 + 2*c)/(b + 2*c) if b + 2*c else None),
    (7,8):   ("b/(a-1)",            lambda a,b,c: b/(a - 1) if a != 1 else None),
    (8,2):   ("(c-b)/(2a)",         lambda a,b,c: (c - b)/(2*a) if a else None),
    (8,6):   ("b/(a-c)",            lambda a,b,c: b/(a - c) if a != c else None),
    (8,10):  ("(b+c)/(a-c)",        lambda a,b,c: (b + c)/(a - c) if a != c else None),
    (9,2):   ("log_c(a)",           lambda a,b,c: slog(c, a)),
    (9,4):   ("(c²-b)/a",           lambda a,b,c: (c**2 - b)/a if a else None),
    (9,6):   ("(b-1)²",             lambda a,b,c: (b - 1)**2),
    (9,8):   ("∛(43-ac)/a",         lambda a,b,c: scbrt(43 - a*c)/a if a else None),
    (10,3):  ("(b-a)/(a-c)",        lambda a,b,c: (b - a)/(a - c) if a != c else None),
    (10,5):  ("11-b",               lambda a,b,c: 11 - b),
    (10,7):  ("(b-2a)/(a-c)",       lambda a,b,c: (b - 2*a)/(a - c) if a != c else None),
    (10,9):  ("(c+3)/a",            lambda a,b,c: (c + 3)/a if a else None),
    (10,11): ("8c-b/c",             lambda a,b,c: 8*c - b/c if c else None),
    (11,5):  ("b²",                 lambda a,b,c: b**2),
    (12,8):  ("(2^b+1)/(ac)",       lambda a,b,c: (2**b + 1)/(a*c) if a*c else None),
}

# ======================================================================
# Phase 1: Wide search (no N limit)
# ======================================================================
print("=" * 70)
print("PHASE 1: Find (a,b,c) maximizing # of positive-integer expressions")
print("  a,b,c ∈ [1,30], NO upper bound on N")
print("=" * 70)

results = []
for a in range(1, 31):
    for b in range(1, 31):
        for c in range(1, 31):
            score = 0
            vals = {}
            max_val = 0
            for pos, (name, func) in EXPR.items():
                v = safe(func, a, b, c)
                if is_pos_int(v):
                    iv = int(round(v))
                    score += 1
                    vals[pos] = iv
                    max_val = max(max_val, iv)
            if score >= 25:  # only track high scores
                results.append((score, a, b, c, max_val, vals))

results.sort(reverse=True)
print(f"\nTotal candidates with score >= 25: {len(results)}")
print(f"\nTop 30:")
for score, a, b, c, max_val, vals in results[:30]:
    print(f"  a={a:2d}, b={b:2d}, c={c:2d}: {score}/37, max_val={max_val}")

# ======================================================================
# Phase 2: Detailed analysis of top candidates
# ======================================================================
print("\n" + "=" * 70)
print("PHASE 2: Detailed analysis of top candidates")
print("=" * 70)

for score, a, b, c, max_val, vals in results[:5]:
    print(f"\n{'─' * 70}")
    print(f"  a={a}, b={b}, c={c}: {score}/37, max_val={max_val}")
    print(f"{'─' * 70}")

    for pos in sorted(EXPR.keys()):
        name, func = EXPR[pos]
        v = safe(func, a, b, c)
        ok = is_pos_int(v)
        if ok:
            iv = int(round(v))
            print(f"  ✓ {str(pos):10s} {name:25s} = {iv}")
        else:
            v_str = f"{v:.6f}" if v is not None else "UNDEF"
            print(f"  ✗ {str(pos):10s} {name:25s} = {v_str}")

    # Count constraint check
    cnts = Counter(vals.values())
    violations = {k: cnt for k, cnt in cnts.items() if cnt > k}
    if violations:
        print(f"  COUNT VIOLATIONS: {violations}")
    else:
        print(f"  COUNT CONSTRAINT: OK")
    print(f"  Value distribution: {dict(sorted(cnts.items()))}")

# ======================================================================
# Phase 3: Focus on b=2 candidates with N=17 limit
# ======================================================================
print("\n" + "=" * 70)
print("PHASE 3: b=2 forced, c∈{2,3,4}, wider a search, N≤17")
print("=" * 70)

for a in range(1, 31):
    for c in [2, 3, 4]:
        b = 2
        if a == c:
            continue
        score = 0
        vals = {}
        for pos, (name, func) in EXPR.items():
            v = safe(func, a, b, c)
            if is_pos_int(v, max_n=17):
                iv = int(round(v))
                score += 1
                vals[pos] = iv
        if score >= 15:
            cnts = Counter(vals.values())
            violations = {k: cnt for k, cnt in cnts.items() if cnt > k}
            cv = "OK" if not violations else f"VIOL: {violations}"
            print(f"  a={a:2d}, b=2, c={c}: {score}/37, {cv}")
