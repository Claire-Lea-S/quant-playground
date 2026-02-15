#!/usr/bin/env python3
"""
Market Maker Simulator — Entry Point

Compare three market-making strategies through simulation:
  1. Naive (fixed spread)     — baseline, ignores risk
  2. Inventory-based          — heuristic inventory management
  3. Avellaneda–Stoikov       — optimal quoting under CARA utility

Outputs:
  - Single-path comparison plot
  - Monte Carlo P&L distribution comparison
  - Individual strategy deep-dive plots

All figures are saved to the output/ directory.
"""

import os
import argparse

from market_maker.price_process import PriceProcess
from market_maker.traders import TraderConfig
from market_maker.strategies import NaiveStrategy, InventoryStrategy, AvellanedaStoikov
from market_maker.simulation import SimulationConfig, run_simulation, monte_carlo
from market_maker.visualization import (
    plot_simulation,
    plot_strategy_comparison,
    plot_single_path_comparison,
)


def main(n_monte_carlo: int = 500, seed: int = 42, show: bool = True):
    """Run the full simulation suite."""
    import matplotlib.pyplot as plt

    os.makedirs("output", exist_ok=True)

    # --- Configuration ---
    price = PriceProcess(s0=100.0, mu=0.0, sigma=2.0)
    traders = TraderConfig(arrival_rate=100.0, informed_fraction=0.3, noise_tolerance=1.0)
    config = SimulationConfig(
        T=1.0,
        n_steps=10_000,
        price_process=price,
        trader_config=traders,
        trade_impact=0.05,
        info_leakage=0.005,
        seed=seed,
    )

    # --- Define strategies ---
    strategies = {
        "Naive (Fixed Spread)": NaiveStrategy(half_spread=0.5),
        "Inventory-Based": InventoryStrategy(half_spread=0.5, skew=0.1),
        "Avellaneda-Stoikov": AvellanedaStoikov(gamma=0.1, kappa=1.5),
    }

    # =========================================================
    # 1. Single-path comparison (same price path, all strategies)
    # =========================================================
    print("=" * 60)
    print("SINGLE-PATH COMPARISON")
    print("=" * 60)

    single_results = {}
    for name, strategy in strategies.items():
        result = run_simulation(strategy, config)
        single_results[name] = result
        print(
            f"  {name:30s}  P&L={result.final_pnl:+8.2f}  "
            f"Trades={result.n_trades:4d}  Max|Inv|={result.max_inventory:3d}"
        )

    fig1 = plot_single_path_comparison(single_results)
    fig1.savefig("output/single_path_comparison.png", dpi=150, bbox_inches="tight")
    print("\n  → Saved output/single_path_comparison.png")

    # =========================================================
    # 2. Monte Carlo comparison
    # =========================================================
    print(f"\n{'=' * 60}")
    print(f"MONTE CARLO ANALYSIS ({n_monte_carlo} simulations per strategy)")
    print("=" * 60)

    mc_results = {}
    for name, strategy in strategies.items():
        print(f"  Running: {name}...", end=" ", flush=True)
        mc_results[name] = monte_carlo(strategy, config, n_simulations=n_monte_carlo)
        pnls = [r.final_pnl for r in mc_results[name]]
        print(f"E[P&L]={sum(pnls)/len(pnls):+.2f}  σ={__import__('numpy').std(pnls):.2f}")

    fig2 = plot_strategy_comparison(mc_results)
    fig2.savefig("output/monte_carlo_comparison.png", dpi=150, bbox_inches="tight")
    print("\n  → Saved output/monte_carlo_comparison.png")

    # =========================================================
    # 3. Individual strategy deep-dives
    # =========================================================
    print(f"\n{'=' * 60}")
    print("INDIVIDUAL STRATEGY PLOTS")
    print("=" * 60)

    for name, strategy in strategies.items():
        result = run_simulation(strategy, config)
        fig = plot_simulation(result)
        safe_name = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        filename = f"output/{safe_name}.png"
        fig.savefig(filename, dpi=150, bbox_inches="tight")
        print(f"  → Saved {filename}")

    if show:
        plt.show()

    print("\nDone!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Market Maker Strategy Simulator")
    parser.add_argument(
        "-n", "--n-sims", type=int, default=500,
        help="Number of Monte Carlo simulations (default: 500)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=42,
        help="Random seed (default: 42)",
    )
    parser.add_argument(
        "--no-show", action="store_true",
        help="Don't display plots (just save to output/)",
    )
    args = parser.parse_args()
    main(n_monte_carlo=args.n_sims, seed=args.seed, show=not args.no_show)
