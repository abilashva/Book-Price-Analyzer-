"""Command-line entry point: scrape -> clean -> analyse -> save outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import plot_price_by_rating, plot_price_distribution, price_by_rating, summary
from .cleaning import build_dataframe
from .scraper import scrape


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scrape books and analyse their prices.")
    parser.add_argument("--pages", type=int, default=5, help="listing pages to scrape (20 books each)")
    parser.add_argument("--delay", type=float, default=0.5, help="seconds between requests")
    parser.add_argument("--out", type=Path, default=Path("outputs"), help="output directory")
    args = parser.parse_args(argv)

    args.out.mkdir(parents=True, exist_ok=True)

    print(f"Scraping up to {args.pages} pages...")
    df = build_dataframe(b.to_dict() for b in scrape(args.pages, args.delay))
    if df.empty:
        print("No books found.")
        return 1

    csv_path = args.out / "books.csv"
    df.to_csv(csv_path, index=False)
    plot_price_distribution(df, args.out / "price_distribution.png")
    plot_price_by_rating(df, args.out / "price_by_rating.png")

    print(f"\nSaved {len(df)} books to {csv_path}\n")
    for key, value in summary(df).items():
        print(f"{key:>15}: {value}")
    print("\nAverage price by rating:")
    print(price_by_rating(df).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
