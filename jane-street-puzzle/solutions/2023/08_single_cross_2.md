# Single-Cross 2 - August 2023 (Solution)

**Puzzle:** [08_single_cross_2.md](../../puzzles/2023/08_single_cross_2.md)

## Official Solution

This is a 3D throwback to the original "Single Cross" puzzle from 2020.

### Calculation

For lengths D ≤ 1, the probability of a single cross is a spherical coordinate double integral that miraculously simplifies to:

**(1/(4π)) × D × (-16D + 3D² + 6π)**

### Optimal Value

This function has a local maximum at:

**D = (16 - √(256 - 54π))/9 ≈ 0.7452572091**

With maximal probability ≈ **0.5095346021**

### Answer

**0.7452572091,0.5095346021**
