# Market Maker Simulator

A Python simulation framework for comparing market-making strategies under adverse selection and inventory risk. Implements three strategies of increasing sophistication — from a naive fixed-spread baseline to the **Avellaneda–Stoikov (2008)** optimal quoting model — and evaluates them via Monte Carlo analysis.

## Why Market Making?

A **market maker** continuously quotes bid (buy) and ask (sell) prices for an asset, profiting from the spread between them. But this comes with two fundamental risks:

| Risk | Description |
|------|-------------|
| **Inventory risk** | Accumulating a large position exposes the MM to adverse price moves. |
| **Adverse selection** | Informed traders exploit stale quotes, trading only when the MM is wrong. |

The optimal strategy must balance earning spread revenue from noise traders while protecting against informed flow and managing inventory exposure. This simulator lets you explore that tradeoff quantitatively.

## Strategies

### 1. Naive (Fixed Spread) — Baseline

Quotes a constant spread around the mid-price, ignoring all risk:

$$\text{bid} = m - \frac{\delta}{2}, \qquad \text{ask} = m + \frac{\delta}{2}$$

where $m$ is the mid-price estimate and $\delta$ is the fixed spread. Serves as a benchmark — it will accumulate large inventory positions and suffer from adverse selection.

### 2. Inventory-Based — Heuristic Risk Management

Skews quotes based on current inventory to mean-revert the position toward zero:

$$\text{bid} = m - \frac{\delta}{2} - \kappa q, \qquad \text{ask} = m + \frac{\delta}{2} - \kappa q$$

where $q$ is the current inventory and $\kappa$ controls skew intensity. When long ($q > 0$), both quotes shift down, making it cheaper for others to buy (reducing our position).

### 3. Avellaneda–Stoikov — Optimal Quoting

Derives optimal quotes from utility maximization under CARA (exponential) utility with inventory risk.

**Reservation price** (risk-adjusted fair value):

$$r = s - q \cdot \gamma \cdot \sigma^2 \cdot (T - t)$$

**Optimal spread**:

$$\delta^* = \gamma \cdot \sigma^2 \cdot (T - t) + \frac{2}{\gamma} \ln\left(1 + \frac{\gamma}{\kappa}\right)$$

**Quotes**:

$$\text{bid} = r - \frac{\delta^*}{2}, \qquad \text{ask} = r + \frac{\delta^*}{2}$$

| Parameter | Meaning |
|-----------|---------|
| $s$ | Mid-price estimate |
| $q$ | Current inventory |
| $\gamma$ | Risk aversion coefficient |
| $\sigma$ | Asset volatility |
| $T - t$ | Time remaining |
| $\kappa$ | Order arrival intensity |

**Key insight**: The reservation price *penalizes* large inventory — if you're long, your effective fair value drops, making you quote lower (eager to sell). The spread widens with volatility and time remaining, reflecting greater uncertainty.

> **Reference**: Avellaneda, M. & Stoikov, S. (2008). "High-frequency trading in a limit order book." *Quantitative Finance*, 8(3), 217–224.

## Simulation Model

The simulator runs in discrete time:

1. **True price** evolves via Arithmetic Brownian Motion: $dS_t = \mu \, dt + \sigma \, dW_t$
2. **Traders arrive** via a Poisson process with rate $\lambda$
   - With probability $\alpha$: **informed trader** (exploits mispricing)
   - With probability $1 - \alpha$: **noise trader** (buys/sells randomly)
3. **Market maker** quotes bid/ask, executes trades, updates inventory
4. **P&L** is marked to market: $\text{P\&L}_t = \text{Cash}_t + q_t \cdot S_t$

The MM cannot observe the true price — it maintains an estimate updated through trade flow signals and slow information leakage.

## Quick Start

```bash
# Clone and install
git clone https://github.com/YOUR_USERNAME/market-maker-sim.git
cd market-maker-sim
pip install -r requirements.txt

# Run the full simulation suite
python run_simulation.py

# Options
python run_simulation.py --n-sims 1000 --seed 123 --no-show
```

This generates comparison plots in `output/`.

## Project Structure

```
market-maker-sim/
├── market_maker/
│   ├── __init__.py           # Public API
│   ├── price_process.py      # Arithmetic Brownian Motion price model
│   ├── traders.py            # Informed + noise trader arrival model
│   ├── strategies.py         # MM strategies (Naive, Inventory, A-S)
│   ├── simulation.py         # Simulation engine + Monte Carlo
│   └── visualization.py      # Plotting utilities
├── notebooks/
│   └── walkthrough.ipynb     # Interactive exploration
├── run_simulation.py         # CLI entry point
├── requirements.txt
└── README.md
```

## Example Output

Running `python run_simulation.py` produces:

**Single-path strategy comparison** — same price path, three strategies:

Shows how the Avellaneda–Stoikov strategy actively manages inventory (staying close to zero) while the naive strategy lets inventory drift.

**Monte Carlo P&L distributions** — 500 independent simulations per strategy:

The Avellaneda–Stoikov strategy achieves higher expected P&L with lower variance (tighter distribution), demonstrating the value of optimal inventory management.

## Key Takeaways

| Metric | Naive | Inventory | Avellaneda–Stoikov |
|--------|-------|-----------|-------------------|
| E[P&L] | Low | Medium | **Highest** |
| P&L Variance | High | Medium | **Lowest** |
| Inventory Risk | Uncontrolled | Managed | **Optimally controlled** |
| Theoretical Basis | None | Heuristic | **Utility maximization** |

## Extending the Simulator

The modular design makes it easy to add:

- **New strategies**: Subclass `Strategy` and implement `compute_quotes()`
- **Different price models**: Modify `PriceProcess` (e.g., jump-diffusion, stochastic volatility)
- **Richer trader models**: Add momentum traders, market orders with varying sizes, etc.
- **Transaction costs**: Add fees to the P&L calculation in `simulation.py`

## License

MIT
