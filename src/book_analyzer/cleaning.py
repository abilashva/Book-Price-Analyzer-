"""Turn raw scraped records into a clean pandas DataFrame."""

from __future__ import annotations

import re
from typing import Iterable

import pandas as pd

_PRICE_RE = re.compile(r"(\d+(?:\.\d+)?)")


def parse_price(raw: str) -> float:
    """Extract a number from strings like '£51.77' (handles stray encoding characters)."""
    match = _PRICE_RE.search(raw)
    if not match:
        raise ValueError(f"No price found in {raw!r}")
    return float(match.group(1))


def build_dataframe(records: Iterable[dict]) -> pd.DataFrame:
    df = pd.DataFrame(list(records))
    if df.empty:
        return df
    df["price_gbp"] = df["price"].map(parse_price)
    df = df.drop(columns=["price"]).drop_duplicates(subset="url").reset_index(drop=True)
    df["price_band"] = pd.cut(
        df["price_gbp"],
        bins=[0, 20, 40, 60, float("inf")],
        labels=["<£20", "£20-40", "£40-60", "£60+"],
        right=False,
    )
    return df
