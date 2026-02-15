"""
Simulates the true (unobservable) asset price process.

We model the asset price as an Arithmetic Brownian Motion:

    dS_t = μ dt + σ dW_t

where:
    - S_t is the asset price at time t
    - μ is the drift (expected return per unit time)
    - σ is the volatility (standard deviation per unit time)
    - W_t is a standard Brownian motion

Arithmetic (vs. geometric) Brownian motion is standard in
market microstructure literature because the focus is on
short time horizons where the price can be well-approximated
as a random walk with normally distributed increments.

Reference:
    Avellaneda, M. & Stoikov, S. (2008).
    "High-frequency trading in a limit order book."
    Quantitative Finance, 8(3), 217-224.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class PriceProcess:
    """Configures and generates asset price paths.

    Attributes:
        s0:    Initial price.
        mu:    Drift per unit time (default 0 = no trend).
        sigma: Volatility per unit time.
    """

    s0: float = 100.0
    mu: float = 0.0
    sigma: float = 2.0

    def generate(self, T: float, n_steps: int, rng: np.random.Generator) -> np.ndarray:
        """Generate a price path via Arithmetic Brownian Motion.

        Args:
            T:       Total time horizon.
            n_steps: Number of discrete time steps.
            rng:     NumPy random generator (for reproducibility).

        Returns:
            Array of shape (n_steps + 1,) with the price at each time step.
        """
        dt = T / n_steps
        increments = self.mu * dt + self.sigma * np.sqrt(dt) * rng.standard_normal(n_steps)
        prices = np.empty(n_steps + 1)
        prices[0] = self.s0
        prices[1:] = self.s0 + np.cumsum(increments)
        return prices
