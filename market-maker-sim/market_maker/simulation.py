"""
Core simulation engine.

Runs a discrete-time market-making simulation:

    1. The true asset price evolves via Arithmetic Brownian Motion (unobservable).
    2. The market maker quotes bid/ask prices based on their strategy.
    3. Traders arrive stochastically (Poisson process) and trade against quotes.
    4. The market maker's inventory, cash, and P&L are tracked throughout.

The market maker cannot observe the true price directly. Instead, they
maintain a mid-price estimate updated via:
    - Trade flow signals (buys push estimate up, sells push it down).
    - Slow information leakage from the broader market.

This creates realistic adverse selection: the MM's estimate lags the
true price, and informed traders exploit this lag.
"""

import numpy as np
from dataclasses import dataclass, field

from .price_process import PriceProcess
from .traders import TraderConfig, TraderSimulator, TradeDirection
from .strategies import Strategy, MarketState


@dataclass
class SimulationConfig:
    """Configuration for a single simulation run.

    Attributes:
        T:             Trading horizon (e.g. 1.0 = one trading session).
        n_steps:       Number of discrete time steps.
        price_process: Asset price dynamics configuration.
        trader_config: Trader behavior configuration.
        trade_impact:  How much each trade moves the MM's mid-price estimate.
        info_leakage:  Rate at which the MM's estimate drifts toward true price.
        seed:          Random seed for reproducibility.
    """

    T: float = 1.0
    n_steps: int = 10_000
    price_process: PriceProcess = field(default_factory=PriceProcess)
    trader_config: TraderConfig = field(default_factory=TraderConfig)
    trade_impact: float = 0.05
    info_leakage: float = 0.005
    seed: int | None = None


@dataclass
class SimulationResult:
    """Full history and summary statistics of a simulation run."""

    times: np.ndarray
    true_prices: np.ndarray
    bids: np.ndarray
    asks: np.ndarray
    inventory: np.ndarray
    cash: np.ndarray
    pnl: np.ndarray
    trades: np.ndarray  # +1 = someone bought from MM, -1 = someone sold to MM, 0 = no trade
    strategy_name: str

    @property
    def n_trades(self) -> int:
        """Total number of executed trades."""
        return int(np.sum(self.trades != 0))

    @property
    def n_buys(self) -> int:
        """Number of buy trades (others buying from MM)."""
        return int(np.sum(self.trades == 1))

    @property
    def n_sells(self) -> int:
        """Number of sell trades (others selling to MM)."""
        return int(np.sum(self.trades == -1))

    @property
    def final_pnl(self) -> float:
        """Terminal mark-to-market P&L."""
        return float(self.pnl[-1])

    @property
    def max_inventory(self) -> int:
        """Maximum absolute inventory reached."""
        return int(np.max(np.abs(self.inventory)))

    @property
    def pnl_sharpe(self) -> float:
        """Sharpe-like ratio computed from P&L increments."""
        pnl_changes = np.diff(self.pnl)
        std = np.std(pnl_changes)
        if std == 0:
            return 0.0
        return float(np.mean(pnl_changes) / std * np.sqrt(len(pnl_changes)))


def run_simulation(strategy: Strategy, config: SimulationConfig) -> SimulationResult:
    """Run a single market-making simulation.

    Args:
        strategy: The market-making strategy to use.
        config:   Simulation parameters.

    Returns:
        SimulationResult with full time-series history.
    """
    # Derive independent RNGs for price and trader processes
    master_rng = np.random.default_rng(config.seed)
    price_rng = np.random.default_rng(master_rng.integers(0, 2**31))
    trader_rng = np.random.default_rng(master_rng.integers(0, 2**31))

    n = config.n_steps
    dt = config.T / n

    # Generate true price path
    true_prices = config.price_process.generate(config.T, n, rng=price_rng)

    # Initialize state arrays
    times = np.linspace(0, config.T, n + 1)
    bids = np.zeros(n + 1)
    asks = np.zeros(n + 1)
    inventory = np.zeros(n + 1, dtype=int)
    cash = np.zeros(n + 1)
    pnl = np.zeros(n + 1)
    trades = np.zeros(n + 1, dtype=int)

    # Trader arrival simulator
    trader_sim = TraderSimulator(config.trader_config, trader_rng)

    # Market maker's mid-price estimate (starts at known initial price)
    mid_estimate = config.price_process.s0

    for i in range(n):
        # 1. Compute quotes
        state = MarketState(
            t=times[i],
            T=config.T,
            mid_price=mid_estimate,
            inventory=int(inventory[i]),
            sigma=config.price_process.sigma,
        )
        bid, ask = strategy.compute_quotes(state)
        bids[i] = bid
        asks[i] = ask

        # 2. Simulate trader arrival and potential trade
        direction = trader_sim.step(dt, bid, ask, true_prices[i])

        if direction == TradeDirection.BUY:
            # Someone buys from MM at ask → MM sells, inventory decreases
            inventory[i + 1] = inventory[i] - 1
            cash[i + 1] = cash[i] + ask
            trades[i] = 1
            # Trade flow signal: a buy suggests upward pressure
            mid_estimate += config.trade_impact

        elif direction == TradeDirection.SELL:
            # Someone sells to MM at bid → MM buys, inventory increases
            inventory[i + 1] = inventory[i] + 1
            cash[i + 1] = cash[i] - bid
            trades[i] = -1
            # Trade flow signal: a sell suggests downward pressure
            mid_estimate -= config.trade_impact

        else:
            inventory[i + 1] = inventory[i]
            cash[i + 1] = cash[i]
            trades[i] = 0

        # Slow information leakage — MM gradually learns from the market
        mid_estimate += config.info_leakage * (true_prices[i] - mid_estimate)

        # Mark-to-market P&L = cash + inventory valued at true price
        pnl[i + 1] = cash[i + 1] + inventory[i + 1] * true_prices[i + 1]

    # Fill final-step quotes (for plotting)
    bids[-1] = bids[-2] if n > 0 else 0
    asks[-1] = asks[-2] if n > 0 else 0

    return SimulationResult(
        times=times,
        true_prices=true_prices,
        bids=bids,
        asks=asks,
        inventory=inventory,
        cash=cash,
        pnl=pnl,
        trades=trades,
        strategy_name=strategy.name,
    )


def monte_carlo(
    strategy: Strategy,
    config: SimulationConfig,
    n_simulations: int = 500,
) -> list[SimulationResult]:
    """Run Monte Carlo simulations for statistical analysis.

    Each simulation uses a different random seed to generate
    independent price paths and trader arrivals.

    Args:
        strategy:       The market-making strategy to evaluate.
        config:         Base simulation configuration.
        n_simulations:  Number of independent runs.

    Returns:
        List of SimulationResult objects.
    """
    results = []
    base_seed = config.seed if config.seed is not None else 0

    for i in range(n_simulations):
        sim_config = SimulationConfig(
            T=config.T,
            n_steps=config.n_steps,
            price_process=config.price_process,
            trader_config=config.trader_config,
            trade_impact=config.trade_impact,
            info_leakage=config.info_leakage,
            seed=base_seed + i,
        )
        results.append(run_simulation(strategy, sim_config))

    return results
