"""
Market-making strategies.

Each strategy computes bid and ask quotes given the current market state.
Strategies differ in how they handle the two core risks of market making:

1. **Inventory risk** — holding a large position exposes the market maker
   to adverse price movements.
2. **Adverse selection** — informed traders pick off stale quotes.

Implemented strategies (increasing sophistication):
- NaiveStrategy:        Fixed spread, ignores all risk.
- InventoryStrategy:    Skews quotes to manage inventory.
- AvellanedaStoikov:    Optimal quotes under CARA utility with inventory risk.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np


@dataclass
class MarketState:
    """Snapshot of the current market state visible to the market maker.

    Attributes:
        t:         Current time.
        T:         Terminal time (end of trading session).
        mid_price: Market maker's current estimate of fair value.
        inventory: Current inventory (positive = long, negative = short).
        sigma:     Estimated asset volatility.
    """

    t: float
    T: float
    mid_price: float
    inventory: int
    sigma: float


class Strategy(ABC):
    """Abstract base class for market-making strategies."""

    @abstractmethod
    def compute_quotes(self, state: MarketState) -> tuple[float, float]:
        """Compute bid and ask prices.

        Args:
            state: Current market state.

        Returns:
            Tuple of (bid_price, ask_price).
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable strategy name."""
        pass


class NaiveStrategy(Strategy):
    """
    Fixed-spread market making (baseline).

    Quotes a constant spread around the mid-price, completely ignoring
    inventory position and time remaining.

        bid = mid − δ/2
        ask = mid + δ/2

    This is the simplest possible strategy and serves as a benchmark.
    It will accumulate large inventory positions and suffer from
    adverse selection without any mitigation.

    Args:
        half_spread: δ/2 — half the bid-ask spread.
    """

    def __init__(self, half_spread: float = 0.5):
        self.half_spread = half_spread

    @property
    def name(self) -> str:
        return "Naive (Fixed Spread)"

    def compute_quotes(self, state: MarketState) -> tuple[float, float]:
        bid = state.mid_price - self.half_spread
        ask = state.mid_price + self.half_spread
        return bid, ask


class InventoryStrategy(Strategy):
    """
    Inventory-based market making.

    Skews quotes based on current inventory to encourage mean-reversion
    of the position toward zero. When the market maker is long (positive
    inventory), both quotes are lowered to:
      - Make it more attractive for others to buy (lower ask)
      - Make it less attractive to sell to us (lower bid)

        bid = mid − δ/2 − κ · q
        ask = mid + δ/2 − κ · q

    where:
        q is the current inventory
        κ is the skew intensity parameter

    This is a common heuristic used in practice.

    Args:
        half_spread: δ/2 — half the base spread.
        skew:        κ — inventory skew intensity.
    """

    def __init__(self, half_spread: float = 0.5, skew: float = 0.1):
        self.half_spread = half_spread
        self.skew = skew

    @property
    def name(self) -> str:
        return "Inventory-Based"

    def compute_quotes(self, state: MarketState) -> tuple[float, float]:
        adjustment = self.skew * state.inventory
        bid = state.mid_price - self.half_spread - adjustment
        ask = state.mid_price + self.half_spread - adjustment
        return bid, ask


class AvellanedaStoikov(Strategy):
    """
    Avellaneda–Stoikov optimal market-making strategy.

    Derives optimal bid and ask quotes for a market maker with CARA
    (Constant Absolute Risk Aversion) utility who faces inventory risk.

    **Reservation price** (inventory-adjusted fair value):

        r = s − q · γ · σ² · (T − t)

    **Optimal spread**:

        δ* = γ · σ² · (T − t) + (2/γ) · ln(1 + γ/κ)

    **Quotes**:

        bid = r − δ*/2
        ask = r + δ*/2

    where:
        s = mid-price estimate
        q = current inventory
        γ = risk aversion coefficient
        σ = asset volatility
        T = terminal time
        t = current time
        κ = order arrival intensity parameter

    Key intuition:
    - The reservation price penalizes large inventory: if you're long,
      your "fair value" drops, making you quote lower (eager to sell).
    - The spread widens with volatility and time remaining (more risk).
    - Higher risk aversion (γ) → wider spread, more aggressive inventory control.

    Reference:
        Avellaneda, M. & Stoikov, S. (2008).
        "High-frequency trading in a limit order book."
        Quantitative Finance, 8(3), 217-224.

    Args:
        gamma: γ — risk aversion coefficient.
        kappa: κ — order arrival intensity parameter.
    """

    def __init__(self, gamma: float = 0.1, kappa: float = 1.5):
        self.gamma = gamma
        self.kappa = kappa

    @property
    def name(self) -> str:
        return "Avellaneda-Stoikov"

    def compute_quotes(self, state: MarketState) -> tuple[float, float]:
        tau = max(state.T - state.t, 1e-8)  # Time remaining (avoid zero)

        # Reservation price — penalize large inventory
        reservation = (
            state.mid_price
            - state.inventory * self.gamma * state.sigma**2 * tau
        )

        # Optimal spread
        spread = self.gamma * state.sigma**2 * tau + (2 / self.gamma) * np.log(
            1 + self.gamma / self.kappa
        )

        bid = reservation - spread / 2
        ask = reservation + spread / 2
        return bid, ask
