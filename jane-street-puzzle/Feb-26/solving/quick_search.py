"""
Quick expanded search: what if (4,5) is NOT c^b?
If (4,5) = c*b, then b=3 becomes possible → test a=2, b=3, c=3.
"""
import math

MAX_N = 17

def safe(func, a, b, c):
    try:
        v = func(a, b, c)
        if v is None or isinstance(v, complex):
            return None
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except:
        return None

def is_ok(v):
    if v is None:
        return False
    return v > 1e-9 and abs(v - round(v)) < 1e-9 and round(v) <= MAX_N

# All 37 expressions with ORIGINAL transcription
EXPR = {
    (0,4):   lambda a,b,c: 6*c - 4*b,
    (1,6):   lambda a,b,c: 8 - b,
    (2,1):   lambda a,b,c: (a**b - 4) / (6*c + 1),
    (2,3):   lambda a,b,c: (b + c) / (c - 1),
    (2,5):   lambda a,b,c: b**2 - b / c,
    (2,7):   lambda a,b,c: math.sqrt(30 + a) / c,
    (2,9):   lambda a,b,c: (a + b) / (c - 3*a),
    (3,4):   lambda a,b,c: (b - 3*a) / (a - c),
    (3,6):   lambda a,b,c: 8*a - 2*b,
    (3,8):   lambda a,b,c: b / (a - c),
    (3,10):  lambda a,b,c: (b + 9) / math.sqrt(c - a) if c > a else None,
    (4,1):   lambda a,b,c: 18 / (a*c + 1),
    (4,5):   lambda a,b,c: c**b,
    (4,9):   lambda a,b,c: (3 + b**2) / math.sqrt(3 + 2*c),
    (5,3):   lambda a,b,c: b / (a**2 - c**2) if a**2 != c**2 else None,
    (5,10):  lambda a,b,c: math.sqrt(a + 2) / a,
    (6,2):   lambda a,b,c: a**b - 12 / a,
    (6,4):   lambda a,b,c: 2*c + c / a,
    (6,6):   lambda a,b,c: 4*a - 5*b,
    (6,8):   lambda a,b,c: c + 2*a,
    (6,10):  lambda a,b,c: b / (9*a - 5*c) if 9*a != 5*c else None,
    (7,0):   lambda a,b,c: (b**3 + 2*c) / (b + 2*c),
    (7,8):   lambda a,b,c: b / (a - 1) if a != 1 else None,
    (8,2):   lambda a,b,c: (c - b) / (2*a),
    (8,6):   lambda a,b,c: b / (a - c) if a != c else None,
    (8,10):  lambda a,b,c: (b + c) / (a - c) if a != c else None,
    (9,2):   lambda a,b,c: math.log(a) / math.log(c) if c > 0 and c != 1 and a > 0 else None,
    (9,4):   lambda a,b,c: (c**2 - b) / a,
    (9,6):   lambda a,b,c: (b - 1)**2,
    (9,8):   lambda a,b,c: (abs(43 - a*c)**(1/3) * (1 if 43 >= a*c else -1)) / a,
    (10,3):  lambda a,b,c: (b - a) / (a - c) if a != c else None,
    (10,5):  lambda a,b,c: 11 - b,
    (10,7):  lambda a,b,c: (b - 2*a) / (a - c) if a != c else None,
    (10,9):  lambda a,b,c: (c + 3) / a,
    (10,11): lambda a,b,c: 8*c - b / c,
    (11,5):  lambda a,b,c: b**2,
    (12,8):  lambda a,b,c: (2**b + 1) / (a*c),
}

NAMES = {
    (0,4): "6c-4b", (1,6): "8-b", (2,1): "(a^b-4)/(6c+1)", (2,3): "(b+c)/(c-1)",
    (2,5): "b²-b/c", (2,7): "√(30+a)/c", (2,9): "(a+b)/(c-3a)",
    (3,4): "(b-3a)/(a-c)", (3,6): "8a-2b", (3,8): "b/(a-c)", (3,10): "(b+9)/√(c-a)",
    (4,1): "18/(ac+1)", (4,5): "c^b", (4,9): "(3+b²)/√(3+2c)",
    (5,3): "b/(a²-c²)", (5,10): "√(a+2)/a", (6,2): "a^b-12/a", (6,4): "2c+c/a",
    (6,6): "4a-5b", (6,8): "c+2a", (6,10): "b/(9a-5c)",
    (7,0): "(b³+2c)/(b+2c)", (7,8): "b/(a-1)", (8,2): "(c-b)/(2a)",
    (8,6): "b/(a-c)", (8,10): "(b+c)/(a-c)", (9,2): "log_c(a)",
    (9,4): "(c²-b)/a", (9,6): "(b-1)²", (9,8): "∛(43-ac)/a",
    (10,3): "(b-a)/(a-c)", (10,5): "11-b", (10,7): "(b-2a)/(a-c)",
    (10,9): "(c+3)/a", (10,11): "8c-b/c", (11,5): "b²", (12,8): "(2^b+1)/(ac)",
}


print("=" * 70)
print("WIDE SEARCH: a in [1,20], b in {2,3,4}, c in [1,20], a≠c")
print("Testing all original expressions (no variants)")
print("=" * 70)

best_score = 0
best_list = []

for a in range(1, 21):
    for b in [2, 3, 4]:
        for c in range(1, 21):
            if a == c:
                continue

            score = 0
            vals = {}
            for pos, func in EXPR.items():
                v = safe(func, a, b, c)
                if is_ok(v):
                    score += 1
                    vals[pos] = int(round(v))

            if score >= best_score - 2:
                if score > best_score:
                    best_score = score
                    best_list = [(score, a, b, c, vals)]
                elif score == best_score:
                    best_list.append((score, a, b, c, vals))

print(f"\nBest score: {best_score}/37")
print(f"\nAll candidates with score >= {best_score}:")
for score, a, b, c, vals in sorted(best_list, reverse=True)[:20]:
    # Check count constraint
    from collections import Counter
    cnts = Counter(vals.values())
    count_ok = all(cnt <= k for k, cnt in cnts.items())
    max_v = max(vals.values()) if vals else 0
    print(f"  a={a:2d}, b={b}, c={c:2d}: {score}/37, max_val={max_v}, count_ok={count_ok}")

# Show details for top 3
for score, a, b, c, vals in sorted(best_list, reverse=True)[:3]:
    print(f"\n{'─'*70}")
    print(f"  Detail: a={a}, b={b}, c={c} ({score}/37)")
    print(f"{'─'*70}")
    for pos in sorted(EXPR.keys()):
        v = safe(EXPR[pos], a, b, c)
        ok = is_ok(v)
        if ok:
            print(f"  ✓ {str(pos):10s} {NAMES[pos]:25s} = {int(round(v)):3d}")
        else:
            v_str = f"{v:.4f}" if v is not None else "UNDEF"
            print(f"  ✗ {str(pos):10s} {NAMES[pos]:25s} = {v_str:>10s}")
