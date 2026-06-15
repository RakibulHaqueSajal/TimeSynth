"""Benchmark AutoARIMA training time on many synthetic series."""

from __future__ import annotations

import argparse
from time import perf_counter

import numpy as np
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
from statsforecast.utils import AirPassengersDF


def build_dataset(n_series: int, noise_std: float, seed: int) -> pd.DataFrame:
    """Replicate AirPassengers into many unique series with a bit of noise."""
    base = AirPassengersDF[["ds", "y"]].copy()
    periods = len(base)
    rng = np.random.default_rng(seed)

    ds = np.tile(base["ds"].to_numpy(), n_series)
    y = np.tile(base["y"].to_numpy(), n_series)
    y = y + rng.normal(scale=noise_std, size=y.size)

    series_ids = np.array([f"series_{i}" for i in range(n_series)], dtype=object)
    unique_ids = np.repeat(series_ids, periods)

    return pd.DataFrame({"unique_id": unique_ids, "ds": ds, "y": y})


def run_benchmark(n_series: int, horizon: int, noise_std: float, seed: int) -> None:
    df = build_dataset(n_series=n_series, noise_std=noise_std, seed=seed)

    sf = StatsForecast(models=[AutoARIMA(season_length=12)], freq="ME")

    start = perf_counter()
    sf.fit(df)
    fit_time = perf_counter() - start

    start = perf_counter()
    forecast = sf.predict(h=horizon, level=[95])
    infer_time = perf_counter() - start

    print(f"Trained AutoARIMA on {n_series:,} series in {fit_time:.2f}s.")
    print(f"Inference ({horizon} steps) took {infer_time:.2f}s.")
    print("Per-series averages:")
    print(f"  train: {fit_time / n_series:.6f}s | infer: {infer_time / n_series:.6f}s")
    print("\nForecast head:\n", forecast.head())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark StatsForecast AutoARIMA across many time series."
    )
    parser.add_argument("--n-series", type=int, default=50_000, help="Number of series.")
    parser.add_argument(
        "--horizon", type=int, default=12, help="Prediction horizon per series."
    )
    parser.add_argument(
        "--noise-std",
        type=float,
        default=3.0,
        help="Std-dev of gaussian noise added to cloned series.",
    )
    parser.add_argument("--seed", type=int, default=0, help="Random seed.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_benchmark(
        n_series=args.n_series,
        horizon=args.horizon,
        noise_std=args.noise_std,
        seed=args.seed,
    )
