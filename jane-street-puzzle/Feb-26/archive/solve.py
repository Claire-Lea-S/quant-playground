import math
from itertools import product

# Primes to try (bounded by expressions like c^b <= 17)
# Including 1 as an option since user said ">= 1"
primes = [2, 3, 5, 7, 11, 13, 17]
candidates = [1] + primes  # try with and without 1

def is_integer(x, tol=1e-9):
    """Check if a float is close to an integer."""
    if x is None or math.isnan(x) or math.isinf(x):
        return False
    return abs(x - round(x)) < tol

def evaluate_all(a, b, c):
    """Evaluate all expressions. Returns (results_dict, valid) where valid means
    all expressions are positive integers between 1 and 17."""
    results = {}
    try:
        exprs = {
            "(0,4)  6c - 4b":              6*c - 4*b,
            "(1,6)  8 - b":                 8 - b,
            "(2,1)  (a^b-4)/(6c+1)":       (a**b - 4) / (6*c + 1),
            "(2,3)  (b+c)/(c-1)":           (b + c) / (c - 1),
            "(2,5)  b^2 - b/c":             b**2 - b/c,
            "(2,7)  sqrt(30+a)/c":          math.sqrt(30 + a) / c,
            "(2,9)  (a+b)/(c-3a)":          (a + b) / (c - 3*a),
            "(3,4)  (b-3a)/(a-c)":          (b - 3*a) / (a - c),
            "(3,6)  8a - 2b":               8*a - 2*b,
            "(3,8)  b/(a-c)":               b / (a - c),
            "(3,10) (b+9)/sqrt(c-a)":       (b + 9) / math.sqrt(c - a) if c > a else None,
            "(4,1)  18/(ac+1)":             18 / (a*c + 1),
            "(4,5)  c^b":                   c**b,
            "(4,9)  (3+b^2)/sqrt(3+2c)":   (3 + b**2) / math.sqrt(3 + 2*c),
            "(5,3)  b/(a^2-c^2)":           b / (a**2 - c**2),
            "(5,10) sqrt(a+2)/a":           math.sqrt(a + 2) / a,
            "(6,2)  a^b - 12/a":            a**b - 12/a,
            "(6,4)  2c + c/a":              2*c + c/a,
            "(6,6)  4a - 5b":               4*a - 5*b,
            "(6,8)  c + 2a":                c + 2*a,
            "(6,10) b/(9a-5c)":             b / (9*a - 5*c) if (9*a - 5*c) != 0 else None,
            "(7,0)  (b^3+2c)/(b+2c)":       (b**3 + 2*c) / (b + 2*c),
            "(7,8)  b/(a-1)":               b / (a - 1),
            "(8,2)  (c-b)/(2a)":            (c - b) / (2*a),
            "(8,6)  b/(a-c)":               b / (a - c),
            "(8,10) (b+c)/(a-c)":           (b + c) / (a - c),
            "(9,2)  log_c(a)":              math.log(a) / math.log(c),
            "(9,4)  (c^2-b)/a":             (c**2 - b) / a,
            "(9,6)  (b-1)^2":               (b - 1)**2,
            "(9,8)  cbrt(43-ac)/a":         (43 - a*c)**(1/3) / a if (43 - a*c) >= 0 else None,
            "(10,3) (b-a)/(a-c)":           (b - a) / (a - c),
            "(10,5) 11 - b":                11 - b,
            "(10,7) (b-2a)/(a-c)":          (b - 2*a) / (a - c),
            "(10,9) (c+3)/a":               (c + 3) / a,
            "(10,11) 8c - b/c":             8*c - b/c,
            "(11,5) b^2":                   b**2,
            "(12,8) (2^b+1)/(ac)":          (2**b + 1) / (a*c),
        }
    except (ZeroDivisionError, ValueError):
        return {}, False

    for name, val in exprs.items():
        if val is None:
            return results, False
        if not is_integer(val):
            return results, False
        val_int = round(val)
        if val_int < 1 or val_int > 17:
            return results, False
        results[name] = val_int

    return results, True


print("Searching for solutions where a, b, c are primes >= 2,")
print("and all expressions evaluate to integers in [1, 17]...\n")

solutions = []
for a, b, c in product(primes, repeat=3):
    results, valid = evaluate_all(a, b, c)
    if valid:
        solutions.append((a, b, c, results))

print(f"Found {len(solutions)} solution(s):\n")
for a, b, c, results in solutions:
    print(f"{'='*60}")
    print(f"  a = {a},  b = {b},  c = {c}")
    print(f"{'='*60}")
    for name, val in sorted(results.items()):
        print(f"  {name} = {val}")
    print()
