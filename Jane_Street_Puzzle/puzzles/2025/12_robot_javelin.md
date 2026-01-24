# Robot Javelin - December 2025

**Category:** Game Theory / Probability
**Difficulty:** Hard
**URL:** https://www.janestreet.com/puzzles/robot-javelin-index/

## Problem Statement

The game is a head-to-head competition between two robots with these mechanics:

### Rules

1. **First throw**: Each robot's initial throw distance is uniformly drawn from [0, 1]
2. **Decision point**: Without knowing the opponent's result, each robot chooses to either keep their distance or discard it
3. **Second throw option**: If discarded, they receive a new distance (also uniform from [0, 1]) which they must keep
4. **Winner**: The robot with the larger final distance wins

### Scenario

Your robot (Java-lin) normally plays the Nash equilibrium strategy. However, the opposing "Spears Robot" has discovered a protocol exploit: they receive one bit of information revealing whether your first throw was above or below a threshold *d* of their choosing—before making their own decision.

Spears has optimized *d* to maximize their winning probability, assuming you remain at equilibrium.

### Challenge

Determine Java-lin's winning probability if you adapt your strategy optimally while Spears still expects you to play the standard Nash equilibrium.

**Answer format**: Exact terms or decimal to 10 places.

## Key Concepts to Apply

- Nash equilibrium analysis
- Threshold strategies
- Counter-exploitation when opponent expects equilibrium play
- Golden ratio (φ ≈ 0.618) often appears in symmetric game theory problems

## Hints for Solving

1. First establish the baseline Nash equilibrium for the fair game
2. Analyze how Spears exploits the information advantage
3. Find how Java-lin can counter-exploit Spears' predictable deviation
4. Look for intervals where keeping a throw that you'd normally discard is advantageous

## My Attempt

[Write your solution approach here]

---

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

## Lessons Learned

1. In game theory, information asymmetry can be partially countered by deviating from expected behavior
2. The golden ratio appears naturally in symmetric rethrow problems
3. Counter-exploitation requires understanding what the opponent expects you to do
