# Run 3: Contradiction Debug Report

## Summary

The expression system as transcribed is **fundamentally unsolvable** -- no values
of (a, b, c) make all 37 expressions positive integers, even with no upper bound
on expression values. The root cause is **multiple expression misreadings from the
puzzle image**. At least 2-3 expressions must be wrong, because removing any single
expression or any pair still yields no solution.

## The Minimum Contradiction

### Two-expression incompatibility

The most compact contradiction involves just TWO expressions:

**Expression (5,10): `sqrt(a+2)/a`**
- For this to be a positive integer k: `sqrt(a+2) = k*a`, so `a+2 = k^2 * a^2`
- Solving: `a = (1 + sqrt(1 + 8k^2)) / (2k^2)`
- Only k=1 yields an integer: **a = 2**
- No other positive integer a works for any k

**Expression (2,7): `sqrt(30+a)/c`**
- With a=2: `sqrt(32)/c = 4*sqrt(2)/c`
- Since sqrt(2) is irrational, 4*sqrt(2)/c is NEVER a positive integer for any integer c
- **CONTRADICTION: (5,10) forces a=2, but (2,7) is impossible when a=2**

### Proof that these two alone are incompatible

For sqrt(a+2)/a to be a positive integer, we need a+2 to be a perfect square AND
sqrt(a+2)/a to be integer. Checked all a from 1 to 99: only a=2 works.

For sqrt(30+a)/c to be a positive integer, we need 30+a to be a perfect square.
a=34 gives sqrt(64)=8, but sqrt(36)/34 = 6/34 is not an integer.

**There is NO value of a that simultaneously satisfies both expressions.**

### The previously reported contradiction (a deeper consequence)

The contradiction reported in the task description was:
- (3,6): 8a-2b >= 1
- (6,6): 4a-5b >= 1
- (9,6): (b-1)^2 >= 1 => b >= 2
- (11,5): b^2 >= 1

This is a valid downstream contradiction that also exists (with a=2 forced, 4(2)-5b >= 1
requires b <= 1, but b >= 2). However, the (5,10)/(2,7) incompatibility is **more
fundamental** -- it doesn't even depend on b.

## Investigation Results

### 1. No N Cap (Investigation 1)
**Result: No solution exists even with no upper bound on expression values.**

Searched a in [1,49], b in [1,19], c in [2,49] (a != c). Zero solutions found.
This proves the issue is NOT the N <= 17 constraint.

### 2. Non-integer Variables (Investigation 3)
**Result: Variables must be integers; non-integer search also fails.**

- b MUST be integer: from `8-b` and `11-b` being positive integers
- a MUST be rational: from `8a-2b` integer with b integer, 8a is integer; from
  `4a-5b` integer, 4a is integer. But (5,10) constrains a to exactly 2.
- Searched a = n/4 for n in [1,79] and c = m/4 for m in [1,79]: no solutions
- Searched a = n/2 for n in [1,99] and c = m/2 for m in [1,99]: no solutions

### 3. Grid Size (Investigation 4)
**Result: Grid size is irrelevant to the contradiction.**

The contradiction is purely in the expression definitions, not in any grid-size
constraint (N cap, cell counts, etc.). The expressions are unsolvable regardless
of grid dimensions.

- constraints.md says 13x11 (inconsistent with grid_layout.json which says 13x13)
- Max column index in labeled cells is 11, at position (10,11)
- Whether grid is 13x11, 13x12, or 13x13 doesn't matter

### 4. Single Expression Removal (Investigation 7)
**Result: Removing ANY single expression still yields no solution.**

All 37 expressions tested individually. None, when removed alone, produces a
solvable system. This means at least TWO expressions are wrong.

### 5. Pair Removal (Investigation 8)
**Result: Removing ANY pair of expressions still yields no solution.**

All 666 pairs tested. None produces a solvable system. This means at least THREE
expressions are likely wrong.

### 6. Best Candidate Analysis (Investigation 6)
**Result: The best (a,b,c) satisfies only 21/37 expressions.**

Best candidate: **a=2, b=3, c=3** (21/37 valid, 16 failing)

The 16 failing expressions at a=2, b=3, c=3:
| Position | Expression | Value | Issue |
|----------|-----------|-------|-------|
| (2,1)  | (a^b-4)/(6c+1)     | 0.21  | Not integer    |
| (2,7)  | sqrt(30+a)/c        | 1.89  | Not integer    |
| (2,9)  | (a+b)/(c-3a)        | -1.67 | Negative       |
| (3,8)  | b/(a-c)             | -3.00 | Negative       |
| (4,1)  | 18/(ac+1)           | 2.57  | Not integer    |
| (5,3)  | b/(a^2-c^2)         | -0.60 | Negative       |
| (6,4)  | 2c+c/a              | 7.50  | Not integer    |
| (6,6)  | 4a-5b               | -7.00 | Negative       |
| (7,0)  | (b^3+2c)/(b+2c)     | 3.67  | Not integer    |
| (8,2)  | (c-b)/(2a)          | 0.00  | Zero (not pos) |
| (8,6)  | b/(a-c)             | -3.00 | Negative       |
| (8,10) | (b+c)/(a-c)         | -6.00 | Negative       |
| (9,2)  | log_c(a)            | 0.63  | Not integer    |
| (9,8)  | cbrt(43-ac)/a       | 1.67  | Not integer    |
| (10,3) | (b-a)/(a-c)         | -1.00 | Negative       |
| (12,8) | (2^b+1)/(ac)        | 1.50  | Not integer    |

**Key patterns in failing expressions:**
- Many expressions with `(a-c)` in denominator evaluate to negative values
  (because a=2, c=3 gives a-c=-1). These expressions REQUIRE a > c.
- But (3,10): `(b+9)/sqrt(c-a)` REQUIRES c > a (to avoid imaginary sqrt)
- This means expressions simultaneously demand a > c AND c > a -- another
  sub-contradiction suggesting sign/variable errors in the transcription.

### 7. Expression Variant Testing (Investigation 5)
**Result: No single-expression plausible variant fixes the system.**

Tested 12 plausible misreadings of individual expressions (changing variables,
signs, operations). None produced a solution. This further confirms multiple
expressions need correction.

### 8. Joint sqrt Variant Testing
**Result: No combination of (5,10) and (2,7) variants fixes the system.**

Tested 100 combinations of 10 variants each for both sqrt expressions. None
produced a full solution (though some improve the score).

### 9. The a=34 Analysis
**Result: a=34 is the only value making both sqrt arguments perfect squares.**

- sqrt(34+2) = sqrt(36) = 6
- sqrt(30+34) = sqrt(64) = 8

With a=34, the best score (using original expressions) is only 14/37.
The expression values like 8a-2b = 268 are far too large for [1,17].

## Root Cause Assessment

**The expression transcription from the puzzle image contains multiple errors.**

Evidence:
1. No solution exists even with infinite range (no N cap)
2. No single-expression removal helps (implies >= 2 errors)
3. No pair removal helps (implies >= 3 errors)
4. Best score is only 21/37 (57%) -- 16 expressions fail simultaneously
5. Sub-contradictions exist: some expressions require a > c, others require c > a
6. The two sqrt expressions are provably incompatible with each other

**Most likely misread expressions** (based on failure analysis and image ambiguity):
- Expressions involving `a-c` vs `c-a` in denominators (sign confusion)
- The sqrt expressions (5,10) and (2,7) (argument or divisor confusion)
- Expressions where a, b, c could be confused (visually similar in handwriting)
- Coefficient confusion (e.g., 5b vs 5c, 8a vs 8c)

## Recommended Next Steps

1. **Re-examine the puzzle image cell by cell** with extreme care, especially:
   - (5,10): Is it really `sqrt(a+2)/a`? Could be `sqrt(a+2)`, `sqrt(c+2)/a`, etc.
   - (2,7): Is it really `sqrt(30+a)/c`? Could be `sqrt(3c+a)/c`, etc.
   - All expressions with `(a-c)` denominator: verify signs and variable choices
   - (6,6): Is it really `4a-5b`? Could be `4c-5b`, `4a+5b`, etc.

2. **Get a higher-resolution image** if possible

3. **Try an automated approach**: For each expression, generate ALL plausible
   misreadings, then search for (a,b,c) that satisfies at least one variant of
   each expression simultaneously (combinatorial but tractable with pruning)

4. **Check the Jane Street website directly** for a clearer version of the puzzle

## Files Created
- `/solving/debug_contradiction.py` - Main investigation script (7 investigations)
- `/solving/debug_contradiction2.py` - Pair removal + deep constraint analysis
- `/solving/debug_contradiction3.py` - Extended search + sqrt variant analysis
