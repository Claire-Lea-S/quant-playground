"""
market-maker-sim: A Market-Making Strategy Simulator

Simulate and compare market-making strategies across stochastic
price environments. Implements three strategies of increasing
sophistication — from a naive fixed-spread baseline to the
Avellaneda–Stoikov optimal quoting model.

Usage:
    from market_maker import (
        NaiveStrategy, InventoryStrategy, AvellanedaStoikov,
        PriceProcess, TraderConfig, SimulationConfig,
        run_simulation, monte_carlo,
    )

    config = SimulationConfig(seed=42)
    result = run_simulation(AvellanedaStoikov(), config)
    print(f"Final P&L: {result.final_pnl:.2f}")
"""

from .strategies import NaiveStrategy, InventoryStrategy, AvellanedaStoikov
from .simulation import run_simulation, monte_carlo, SimulationConfig, SimulationResult
from .price_process import PriceProcess
from .traders import TraderConfig

__all__ = [
    "NaiveStrategy",
    "InventoryStrategy",
    "AvellanedaStoikov",
    "run_simulation",
    "monte_carlo",
    "SimulationConfig",
    "SimulationResult",
    "PriceProcess",
    "TraderConfig",
]
