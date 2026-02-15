# Some Off Square - February 2024 (Solution)

**Puzzle:** [02_some_off_square.md](../../puzzles/2024/02_some_off_square.md)

## Official Solution

### Alternative Approach

Consider the situation where the circle's **center** and a point on the perimeter are chosen at random. One can show that there is a π/24 chance that the circle thus determined will be contained within the square.

### Key Insight

Imagine choosing circles by first selecting the point on the *perimeter* and then selecting the center. By doubling the vector from the perimeter point to the center, we get a vector which comprises the circle's diameter.

However, with probability 3/4, that endpoint is located outside the square! So the space of circles chosen by diameter is a uniform one-fourth of the circles chosen by radius.

Crucially, all circles entirely within the square can be selected by every diameter (by definition of them being entirely within the square), so the uniformity of the subspace is known for circles entirely contained within the square.

### Calculation

This means we have a π/6 chance of the circle being entirely within the square.

### Answer

**1 − π/6**

Note: The answer is NOT 5π/6 (a common error).
