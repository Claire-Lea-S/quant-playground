# Lesses More - January 2023 (Solution)

**Puzzle:** [01_lesses_more.md](../../puzzles/2023/01_lesses_more.md)

## Official Solution

### Mathematical Analysis

Generalize the active square's corner numbers from integers to reals, considering the four numbers as an element of **R**⁴. The function representing a step is:

f((a, b, c, d)) = (|a-b|, |b-c|, |c-d|, |d-a|)

Without loss of generality, consider input (a, b, c, d) to have a largest and b > d. By case checking, the only arrangement that doesn't lead to (0,0,0,0) in fewer than 10 steps has a > b > c > d.

### Normalization

"Normalize" input by subtracting d from everything, then dividing by a-d, to get a general input of the form (1, x, y, 0) for 1 > x > y > 0.

### Finding the Fixed Point

To find arbitrarily long sequences, search for a real input to f that never reaches (0,0,0,0). This requires the normalized output to match the input:

x = (1-x-y)/(1-y) AND y = (x-2y)/(1-y)

The first set of equations resolves to:

**x³ - 4x² + 6x - 2 = 0**

This has a zero at approximately x ≈ 0.456311… with corresponding y ≈ 0.160713….

### Finding the Integer Solution

Search over all c values between 1 and 10,000,000, choosing a and b that are near to c/y and cx/y respectively.

### Answer

**8646064;3945294;1389537;0**

This has f value of **44**.

### Connection

These special input integers have overlaps with the Tribonacci sequence (OEIS A000073)!
