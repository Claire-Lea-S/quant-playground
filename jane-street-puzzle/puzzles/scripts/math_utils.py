"""
Math Utilities for Jane Street Puzzles
======================================

A focused collection of mathematical functions useful for puzzle solving.
Import what you need - these are building blocks, not automatic solvers.

Usage:
    from scripts.math_utils import gcd, mod_inverse, binomial, prime_factorize
"""

import math
from typing import Dict, List, Tuple, Optional, Set, Callable, Any
from functools import lru_cache, reduce
from itertools import permutations, combinations, product
from collections import defaultdict
import random


# =============================================================================
# NUMBER THEORY
# =============================================================================

def gcd(a: int, b: int) -> int:
    """Greatest common divisor using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """Least common multiple."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean algorithm.
    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)
    """
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    Modular inverse of a mod m.
    Returns x such that a*x ≡ 1 (mod m), or None if no inverse.
    """
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m


def mod_pow(base: int, exp: int, mod: int) -> int:
    """Fast modular exponentiation: base^exp mod m."""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result


def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> Optional[int]:
    """
    Solve system of congruences: x ≡ r_i (mod m_i)
    Returns smallest positive x, or None if no solution.
    """
    if len(remainders) != len(moduli):
        return None
    
    current_r, current_m = remainders[0], moduli[0]
    
    for i in range(1, len(remainders)):
        r2, m2 = remainders[i], moduli[i]
        g = gcd(current_m, m2)
        diff = r2 - current_r
        
        if diff % g != 0:
            return None
        
        inv = mod_inverse(current_m // g, m2 // g)
        if inv is None:
            return None
        
        k = (inv * (diff // g)) % (m2 // g)
        current_r = current_r + current_m * k
        current_m = lcm(current_m, m2)
        current_r = current_r % current_m
    
    return current_r


def prime_factorize(n: int) -> Dict[int, int]:
    """
    Prime factorization as {prime: exponent}.
    Example: 12 → {2: 2, 3: 1}
    """
    if n <= 1:
        return {}
    
    factors = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
        i += 2
    
    if n > 1:
        factors[n] = 1
    
    return factors


def is_prime(n: int) -> bool:
    """Check if n is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def sieve_of_eratosthenes(n: int) -> List[int]:
    """Return all primes up to n."""
    if n < 2:
        return []
    is_prime_arr = [True] * (n + 1)
    is_prime_arr[0] = is_prime_arr[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime_arr[i]:
            for j in range(i*i, n + 1, i):
                is_prime_arr[j] = False
    return [i for i in range(n + 1) if is_prime_arr[i]]


def euler_phi(n: int) -> int:
    """Euler's totient function φ(n)."""
    result = n
    for p in prime_factorize(n):
        result -= result // p
    return result


# =============================================================================
# COMBINATORICS
# =============================================================================

def factorial(n: int) -> int:
    """Calculate n!"""
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def binomial(n: int, k: int) -> int:
    """Binomial coefficient C(n, k)."""
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


def multinomial(n: int, groups: List[int]) -> int:
    """Multinomial coefficient: n! / (k₁! * k₂! * ...)"""
    if sum(groups) != n:
        raise ValueError("Group sizes must sum to n")
    result = factorial(n)
    for k in groups:
        result //= factorial(k)
    return result


@lru_cache(maxsize=10000)
def partition_count(n: int, max_part: int = None) -> int:
    """Count integer partitions of n."""
    if max_part is None:
        max_part = n
    if n == 0:
        return 1
    if n < 0 or max_part <= 0:
        return 0
    return partition_count(n - max_part, max_part) + partition_count(n, max_part - 1)


def derangements(n: int) -> int:
    """Count derangements (permutations with no fixed points)."""
    if n == 0:
        return 1
    if n == 1:
        return 0
    prev2, prev1 = 1, 0
    for i in range(2, n + 1):
        current = (i - 1) * (prev1 + prev2)
        prev2, prev1 = prev1, current
    return prev1


def catalan(n: int) -> int:
    """Catalan number C_n."""
    return binomial(2 * n, n) // (n + 1)


def stirling_second(n: int, k: int) -> int:
    """Stirling number of the second kind S(n,k)."""
    @lru_cache(maxsize=10000)
    def S(n, k):
        if n == 0 and k == 0:
            return 1
        if n == 0 or k == 0 or k > n:
            return 0
        return k * S(n-1, k) + S(n-1, k-1)
    return S(n, k)


# =============================================================================
# GEOMETRY
# =============================================================================

def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def polygon_area(vertices: List[Tuple[float, float]]) -> float:
    """Area of polygon using shoelace formula."""
    n = len(vertices)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return abs(area) / 2


def circle_intersection_area(r1: float, r2: float, d: float) -> float:
    """Area of intersection of two circles with given radii and center distance."""
    if d >= r1 + r2:
        return 0.0
    if d <= abs(r1 - r2):
        return math.pi * min(r1, r2)**2
    
    part1 = r1**2 * math.acos((d**2 + r1**2 - r2**2) / (2 * d * r1))
    part2 = r2**2 * math.acos((d**2 + r2**2 - r1**2) / (2 * d * r2))
    part3 = 0.5 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
    return part1 + part2 - part3


# =============================================================================
# PROBABILITY & SIMULATION
# =============================================================================

def monte_carlo_probability(trial_func: Callable[[], bool], n_samples: int = 100000) -> Tuple[float, float]:
    """
    Estimate probability via Monte Carlo.
    Returns (probability, 95% CI half-width).
    """
    successes = sum(1 for _ in range(n_samples) if trial_func())
    p = successes / n_samples
    std_error = math.sqrt(p * (1 - p) / n_samples)
    return p, 1.96 * std_error


def monte_carlo_expected_value(sample_func: Callable[[], float], n_samples: int = 100000) -> Tuple[float, float]:
    """
    Estimate expected value via Monte Carlo.
    Returns (mean, standard_error).
    """
    samples = [sample_func() for _ in range(n_samples)]
    mean = sum(samples) / n_samples
    variance = sum((x - mean)**2 for x in samples) / (n_samples - 1)
    return mean, math.sqrt(variance / n_samples)


# =============================================================================
# EQUATION SOLVING
# =============================================================================

def solve_quadratic(a: float, b: float, c: float) -> List[float]:
    """Solve ax² + bx + c = 0. Returns real roots."""
    if a == 0:
        return [-c/b] if b != 0 else []
    disc = b**2 - 4*a*c
    if disc < 0:
        return []
    if disc == 0:
        return [-b / (2*a)]
    sqrt_disc = math.sqrt(disc)
    return [(-b - sqrt_disc) / (2*a), (-b + sqrt_disc) / (2*a)]


def bisection_solve(f: Callable[[float], float], a: float, b: float, tol: float = 1e-10) -> float:
    """Find root of f in [a, b] using bisection method."""
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    
    while b - a > tol:
        mid = (a + b) / 2
        fmid = f(mid)
        if fmid == 0:
            return mid
        if fa * fmid < 0:
            b, fb = mid, fmid
        else:
            a, fa = mid, fmid
    return (a + b) / 2


def newton_solve(f: Callable[[float], float], fprime: Callable[[float], float], 
                 x0: float, tol: float = 1e-10, max_iter: int = 100) -> float:
    """Find root using Newton-Raphson method."""
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        fp = fprime(x)
        if abs(fp) < 1e-15:
            raise ValueError("Derivative too small")
        x = x - fx / fp
    return x


# =============================================================================
# GAME THEORY
# =============================================================================

def nash_equilibrium_2x2(payoff_matrix: List[List[float]]) -> Tuple[float, float, float]:
    """
    Solve 2x2 zero-sum game for mixed strategy Nash equilibrium.
    Returns (p1_prob_row1, p2_prob_col1, game_value).
    """
    a, b = payoff_matrix[0]
    c, d = payoff_matrix[1]
    
    denom = a - c - b + d
    if abs(denom) < 1e-10:
        return (0.5, 0.5, (a + d) / 2)
    
    p = (d - c) / denom
    q = (d - b) / denom
    value = p * q * a + p * (1-q) * b + (1-p) * q * c + (1-p) * (1-q) * d
    
    return (max(0, min(1, p)), max(0, min(1, q)), value)


# =============================================================================
# BASE CONVERSION
# =============================================================================

def to_base(n: int, base: int) -> str:
    """Convert integer to string in given base (2-36)."""
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    negative = n < 0
    n = abs(n)
    result = []
    while n:
        result.append(digits[n % base])
        n //= base
    if negative:
        result.append('-')
    return ''.join(reversed(result))


def from_base(s: str, base: int) -> int:
    """Convert string in given base to integer."""
    return int(s, base)


def balanced_ternary_to_decimal(s: str) -> int:
    """Convert balanced ternary (T=-1, 0, 1) to decimal."""
    result = 0
    for i, c in enumerate(reversed(s)):
        digit = -1 if c in 'T-' else (0 if c == '0' else 1)
        result += digit * (3 ** i)
    return result


def decimal_to_balanced_ternary(n: int) -> str:
    """Convert decimal to balanced ternary."""
    if n == 0:
        return "0"
    negative = n < 0
    n = abs(n)
    result = []
    while n:
        r = n % 3
        if r == 0:
            result.append('0')
            n //= 3
        elif r == 1:
            result.append('1')
            n //= 3
        else:
            result.append('T')
            n = (n + 1) // 3
    s = ''.join(reversed(result))
    if negative:
        s = s.translate(str.maketrans('1T', 'T1'))
    return s


# =============================================================================
# GRID/CONSTRAINT HELPERS
# =============================================================================

def grid_neighbors(r: int, c: int, rows: int, cols: int, include_diagonal: bool = False) -> List[Tuple[int, int]]:
    """Get valid neighbors of cell (r, c) in a grid."""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if include_diagonal:
        directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors


def flood_fill(grid: List[List[Any]], start: Tuple[int, int], target: Any) -> Set[Tuple[int, int]]:
    """Find all connected cells with same value as target."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    stack = [start]
    
    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        if not (0 <= r < rows and 0 <= c < cols):
            continue
        if grid[r][c] != target:
            continue
        
        visited.add((r, c))
        for nr, nc in grid_neighbors(r, c, rows, cols):
            stack.append((nr, nc))
    
    return visited


# =============================================================================
# CONSTANTS
# =============================================================================

PHI = (1 + math.sqrt(5)) / 2  # Golden ratio ≈ 1.618
PHI_INV = (math.sqrt(5) - 1) / 2  # 1/φ ≈ 0.618


if __name__ == "__main__":
    print("Math Utilities - Quick Test")
    print("=" * 40)
    print(f"gcd(48, 18) = {gcd(48, 18)}")
    print(f"mod_inverse(3, 11) = {mod_inverse(3, 11)}")
    print(f"binomial(10, 3) = {binomial(10, 3)}")
    print(f"prime_factorize(360) = {prime_factorize(360)}")
    print(f"catalan(5) = {catalan(5)}")
    print(f"PHI = {PHI:.10f}")
