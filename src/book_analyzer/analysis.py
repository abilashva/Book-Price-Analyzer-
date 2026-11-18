"""Summary statistics and charts."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt
import pandas as pd


def summary(df: pd.DataFrame) -> dict:
    return {
        "books": int(len(df)),
        "avg_price": round(float(df["price_gbp"].mean()), 2),
        "median_price": round(float(df["price_gbp"].median()), 2),
        "cheapest": df.loc[df["price_gbp"].idxmin(), "title"],
        "most_expensive": df.loc[df["price_gbp"].idxmax(), "title"],
        "in_stock_pct": round(float(df["in_stock"].mean() * 100), 1),
        "avg_rating": round(float(df["rating"].mean()), 2),
    }


def price_by_rating(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("rating")["price_gbp"]
        .agg(count="count", mean_price="mean")
        .round(2)
        .reset_index()
    )


def plot_price_distribution(df: pd.DataFrame, out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["price_gbp"], bins=15, color="#3b6fb6", edgecolor="white")
    ax.set_title("Book price distribution")
    ax.set_xlabel("Price (£)")
    ax.set_ylabel("Number of books")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_price_by_rating(df: pd.DataFrame, out: Path) -> Path:
    stats = price_by_rating(df)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(stats["rating"].astype(str), stats["mean_price"], color="#3b6fb6")
    ax.set_title("Average price by star rating")
    ax.set_xlabel("Star rating")
    ax.set_ylabel("Average price (£)")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out
