# Robot Javelin - December 2025 (Solution)

**Puzzle:** [12_robot_javelin.md](../../puzzles/2025/12_robot_javelin.md)

## Official Solution

### Phase 1: Nash Equilibrium (Fair Game)
"Each robot throws again if their first throw is less than (√5 - 1)/2 = φ ≈ 0.618034…, the golden ratio."

This threshold emerges from symmetry principles and indifference conditions.

### Phase 2: Spears Robot's Exploitation
Spears leverages information about whether Java-lin's first throw exceeded φ (the rethrow threshold):
- Below φ: Spears rethrows on scores under 0.5
- Above φ: Spears rethrows on scores below approximately 0.690983

### Phase 3: Java-lin's Counter-Exploitation
The critical insight involves exploiting Spears' predictable deviation. Java-lin adopts a threshold of 7/12, creating an interval [7/12, φ] where strategic advantage exists.

"Java-lin would normally choose to rethrow, but because Spears Robot will assume this, Java-lin can keep its best throws in this interval."

### Final Answer
**Winning Probability: (229 - 60√5)/192 ≈ 0.4939370904**

This represents Java-lin's victory chances using the counter-strategy, nearly equalizing odds from an initially disadvantaged position.