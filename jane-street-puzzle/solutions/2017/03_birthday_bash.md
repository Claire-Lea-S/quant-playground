# Birthday Bash - March 2017 (Solution)

**Puzzle:** [03_birthday_bash.md](../../puzzles/2017/03_birthday_bash.md)

## Official Solution

**Answer: 2287** people are needed in order to make the probability that each birthday is covered greater than 50%.

This number isn't necessarily easy to compute, but there are some approximations we can make which show us the answer should be on that order.

**Upper bound:** If we had asked for the average number of people needed (instead of the median), that would've been equivalent to the "coupon collector problem". The average number of people needed would've been 365 × (1/365 + 1/364 + 1/363 + …+ 1) ≈ 2365. Given that the average case incorporates what should be a long tail on the right side of the distribution, the average should be greater than the median, and thus 2365 would be an upper bound.

**Lower bound:** For a given day D, the probability of at least 1 out of N people having their birthday on that day would be [1 – (364/365)^N]. Given that at least 1 person has their birthday on D, it makes it slightly less likely that the other days are covered. But if we ignore this effect and assume independence, we could ask how large N would need to be in order for the product of all 365 days' individual probabilities to exceed 0.5. The expression [1 – (364/365)^N]^365 becomes greater than 0.5 when N reaches 2285, so 2285 would be a lower bound.
