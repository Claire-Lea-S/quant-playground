"""
Models trader arrivals and behavior.

Two types of traders interact with the market maker:

1. **Noise traders** — trade for exogenous reasons (hedging, rebalancing).
   They arrive and buy or sell with equal probability, provided the
   spread is within their tolerance.

2. **Informed traders** — possess private information about the true
   asset value. They exploit mispriced quotes:
   - Buy if ask < true_value  (asset is cheap)
   - Sell if bid > true_value (asset is expensive)

Adverse selection arises because informed traders systematically trade
against the market maker when quotes are stale, creating a fundamental
tension: wider spreads protect against informed flow but reduce volume
from (profitable) noise traders.

Trader arrivals follow a Poisson process with rate λ.
"""

import numpy as np
from dataclasses import dataclass
from enum import Enum


class TradeDirection(Enum):
    """Direction of an incoming trade."""

    BUY = 1
    SELL = -1
    NONE = 0


@dataclass
class TraderConfig:
    """Parameters governing trader behavior.

    Attributes:
        arrival_rate:      λ — expected trader arrivals per unit time.
        informed_fraction: α — probability that an arriving trader is informed.
        noise_tolerance:   Maximum half-spread a noise trader will accept.
    """

    arrival_rate: float = 100.0
    informed_fraction: float = 0.3
    noise_tolerance: float = 1.0


class TraderSimulator:
    """Simulates stochastic trader arrivals and trade decisions."""

    def __init__(self, config: TraderConfig, rng: np.random.Generator):
        self.config = config
        self.rng = rng

    def step(
        self, dt: float, bid: float, ask: float, true_price: float
    ) -> TradeDirection:
        """Simulate one timestep of trader arrival.

        Args:
            dt:         Length of the time step.
            bid:        Market maker's current bid price.
            ask:        Market maker's current ask price.
            true_price: The (unobservable) true asset value.

        Returns:
            TradeDirection indicating whether a trade occurred and its direction.
        """
        # Poisson arrival: P(arrival in dt) ≈ λ * dt  (for small dt)
        if self.rng.random() > self.config.arrival_rate * dt:
            return TradeDirection.NONE

        # Determine trader type
        if self.rng.random() < self.config.informed_fraction:
            return self._informed_trade(bid, ask, true_price)
        else:
            return self._noise_trade(bid, ask)

    def _informed_trade(
        self, bid: float, ask: float, true_price: float
    ) -> TradeDirection:
        """Informed trader exploits mispriced quotes."""
        if ask < true_price:
            return TradeDirection.BUY  # Asset is underpriced → buy from MM
        elif bid > true_price:
            return TradeDirection.SELL  # Asset is overpriced → sell to MM
        return TradeDirection.NONE  # Quotes are fair → no edge

    def _noise_trade(self, bid: float, ask: float) -> TradeDirection:
        """Noise trader buys or sells randomly if spread is acceptable."""
        half_spread = (ask - bid) / 2
        if half_spread > self.config.noise_tolerance:
            return TradeDirection.NONE  # Spread too wide
        if self.rng.random() < 0.5:
            return TradeDirection.BUY
        else:
            return TradeDirection.SELL
