"""
Plotting utilities for market-making simulations.

Produces publication-quality figures for:
- Single simulation run (price, inventory, P&L panels)
- Side-by-side strategy comparison on the same price path
- Monte Carlo P&L distribution comparison
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from .simulation import SimulationResult

# --- Color palette ---
STRATEGY_COLORS = {
    "Naive (Fixed Spread)": "#e74c3c",
    "Inventory-Based": "#3498db",
    "Avellaneda-Stoikov": "#2ecc71",
}
COLORS = {
    "true_price": "#2c3e50",
    "bid": "#3498db",
    "ask": "#e74c3c",
    "inventory": "#8e44ad",
    "pnl": "#27ae60",
}


def _setup_style():
    """Apply a clean plot style."""
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "#fafafa",
            "axes.grid": True,
            "grid.alpha": 0.3,
            "grid.linestyle": "--",
            "font.family": "sans-serif",
            "font.size": 10,
        }
    )


def plot_simulation(result: SimulationResult, figsize: tuple = (14, 10)) -> plt.Figure:
    """Plot a single simulation run with three panels: price, inventory, P&L.

    Args:
        result:  Output of run_simulation().
        figsize: Figure dimensions.

    Returns:
        Matplotlib Figure object.
    """
    _setup_style()
    fig = plt.figure(figsize=figsize)
    gs = gridspec.GridSpec(3, 1, height_ratios=[2, 1, 1], hspace=0.35)

    # --- Panel 1: Price + Quotes ---
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(
        result.times,
        result.true_prices,
        color=COLORS["true_price"],
        linewidth=1.5,
        label="True Price",
        alpha=0.9,
    )
    ax1.plot(
        result.times, result.bids, color=COLORS["bid"],
        linewidth=0.6, alpha=0.5, label="Bid",
    )
    ax1.plot(
        result.times, result.asks, color=COLORS["ask"],
        linewidth=0.6, alpha=0.5, label="Ask",
    )
    ax1.fill_between(
        result.times, result.bids, result.asks,
        alpha=0.08, color="gray", label="Spread",
    )

    # Mark trades
    buy_mask = result.trades == 1
    sell_mask = result.trades == -1
    if np.any(buy_mask):
        ax1.scatter(
            result.times[buy_mask], result.asks[buy_mask],
            marker="^", color=COLORS["ask"], s=12, alpha=0.4, label="Buy",
        )
    if np.any(sell_mask):
        ax1.scatter(
            result.times[sell_mask], result.bids[sell_mask],
            marker="v", color=COLORS["bid"], s=12, alpha=0.4, label="Sell",
        )

    ax1.set_title(
        f"Market Making Simulation — {result.strategy_name}",
        fontsize=14, fontweight="bold",
    )
    ax1.set_ylabel("Price")
    ax1.legend(loc="upper left", fontsize=8, ncol=3)

    # --- Panel 2: Inventory ---
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.fill_between(result.times, result.inventory, 0, alpha=0.25, color=COLORS["inventory"])
    ax2.plot(result.times, result.inventory, color=COLORS["inventory"], linewidth=1)
    ax2.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
    ax2.set_ylabel("Inventory (units)")
    ax2.set_title("Inventory Over Time", fontsize=11)

    # --- Panel 3: P&L ---
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    ax3.plot(result.times, result.pnl, color=COLORS["pnl"], linewidth=1.5)
    ax3.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
    ax3.fill_between(
        result.times, result.pnl, 0,
        where=result.pnl >= 0, alpha=0.15, color="green",
    )
    ax3.fill_between(
        result.times, result.pnl, 0,
        where=result.pnl < 0, alpha=0.15, color="red",
    )
    ax3.set_ylabel("P&L")
    ax3.set_xlabel("Time")
    ax3.set_title(
        f"Mark-to-Market P&L  (Final: {result.final_pnl:+.2f}  |  "
        f"Trades: {result.n_trades}  |  Max |Inv|: {result.max_inventory})",
        fontsize=11,
    )

    plt.tight_layout()
    return fig


def plot_strategy_comparison(
    results: dict[str, list[SimulationResult]],
    figsize: tuple = (16, 6),
) -> plt.Figure:
    """Compare P&L distributions and risk metrics across strategies.

    Args:
        results:  Dict mapping strategy name → list of SimulationResults (from Monte Carlo).
        figsize:  Figure dimensions.

    Returns:
        Matplotlib Figure object.
    """
    _setup_style()
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    strategy_names = list(results.keys())

    # --- Panel 1: P&L Distribution ---
    ax1 = axes[0]
    for name in strategy_names:
        final_pnls = [r.final_pnl for r in results[name]]
        color = STRATEGY_COLORS.get(name, "#95a5a6")
        ax1.hist(final_pnls, bins=40, alpha=0.45, label=name, color=color, density=True)
        mean_pnl = np.mean(final_pnls)
        ax1.axvline(mean_pnl, color=color, linestyle="--", linewidth=2, alpha=0.8)
    ax1.set_xlabel("Final P&L")
    ax1.set_ylabel("Density")
    ax1.set_title("P&L Distribution", fontweight="bold")
    ax1.legend(fontsize=8)

    # --- Panel 2: Max Inventory Distribution ---
    ax2 = axes[1]
    for name in strategy_names:
        max_invs = [r.max_inventory for r in results[name]]
        color = STRATEGY_COLORS.get(name, "#95a5a6")
        ax2.hist(max_invs, bins=30, alpha=0.45, label=name, color=color, density=True)
    ax2.set_xlabel("Max |Inventory|")
    ax2.set_ylabel("Density")
    ax2.set_title("Inventory Risk Exposure", fontweight="bold")
    ax2.legend(fontsize=8)

    # --- Panel 3: Summary Statistics Table ---
    ax3 = axes[2]
    ax3.axis("off")

    table_data = []
    for name in strategy_names:
        pnls = [r.final_pnl for r in results[name]]
        sharpes = [r.pnl_sharpe for r in results[name]]
        max_invs = [r.max_inventory for r in results[name]]
        n_trades_avg = np.mean([r.n_trades for r in results[name]])
        table_data.append(
            [
                name.replace(" (Fixed Spread)", "\n(Fixed)"),
                f"{np.mean(pnls):+.1f}",
                f"{np.std(pnls):.1f}",
                f"{np.mean(sharpes):.2f}",
                f"{np.mean(max_invs):.0f}",
                f"{n_trades_avg:.0f}",
            ]
        )

    table = ax3.table(
        cellText=table_data,
        colLabels=["Strategy", "E[P&L]", "σ[P&L]", "Sharpe", "E[Max|Inv|]", "E[Trades]"],
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.8)
    ax3.set_title("Summary Statistics", fontweight="bold", pad=20)

    fig.suptitle(
        "Strategy Comparison — Monte Carlo Analysis",
        fontsize=14, fontweight="bold",
    )
    fig.subplots_adjust(top=0.88)
    return fig


def plot_single_path_comparison(
    results: dict[str, SimulationResult],
    figsize: tuple = (14, 10),
) -> plt.Figure:
    """Compare strategies side-by-side on the same price path.

    Args:
        results:  Dict mapping strategy name → SimulationResult.
        figsize:  Figure dimensions.

    Returns:
        Matplotlib Figure object.
    """
    _setup_style()
    fig, axes = plt.subplots(3, 1, figsize=figsize, height_ratios=[2, 1, 1])

    first_result = list(results.values())[0]

    # --- Panel 1: Price with spread overlays ---
    ax1 = axes[0]
    ax1.plot(
        first_result.times, first_result.true_prices,
        color=COLORS["true_price"], linewidth=1.5, label="True Price", zorder=10,
    )
    for name, result in results.items():
        color = STRATEGY_COLORS.get(name, "#95a5a6")
        ax1.fill_between(
            result.times, result.bids, result.asks,
            alpha=0.12, color=color, label=f"{name} spread",
        )
    ax1.set_title("Quote Comparison on Same Price Path", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Price")
    ax1.legend(fontsize=8)

    # --- Panel 2: Inventory comparison ---
    ax2 = axes[1]
    for name, result in results.items():
        color = STRATEGY_COLORS.get(name, "#95a5a6")
        ax2.plot(result.times, result.inventory, color=color, label=name, linewidth=1.2)
    ax2.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
    ax2.set_ylabel("Inventory")
    ax2.set_title("Inventory Over Time", fontsize=11)
    ax2.legend(fontsize=8)

    # --- Panel 3: P&L comparison ---
    ax3 = axes[2]
    for name, result in results.items():
        color = STRATEGY_COLORS.get(name, "#95a5a6")
        ax3.plot(result.times, result.pnl, color=color, label=name, linewidth=1.5)
    ax3.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
    ax3.set_ylabel("P&L")
    ax3.set_xlabel("Time")
    ax3.set_title("P&L Comparison", fontsize=11)
    ax3.legend(fontsize=8)

    plt.tight_layout()
    return fig
