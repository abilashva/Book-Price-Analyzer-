# Book Price Analyzer

A Python project that scrapes book listings from [books.toscrape.com](https://books.toscrape.com) (a site built for scraping practice), cleans the data with pandas, and produces summary statistics and charts.

## Features

- Polite scraper (custom User-Agent, delay between requests, pagination handling) using `requests` + `BeautifulSoup`
- Data cleaning: price parsing, de-duplication, price bands
- Analysis: average/median price, stock percentage, price by star rating
- Charts saved as PNG (price distribution, average price by rating)
- Offline unit tests using a saved HTML fixture, so tests never hit the network

## Project structure

```
book-price-analyzer/
├── src/book_analyzer/
│   ├── scraper.py      # fetch + parse listing pages
│   ├── cleaning.py     # raw records -> clean DataFrame
│   ├── analysis.py     # statistics and matplotlib charts
│   └── cli.py          # command-line entry point
├── tests/
│   ├── fixtures/sample_page.html
│   └── test_pipeline.py
├── outputs/            # generated CSV and charts
├── requirements.txt
└── pytest.ini
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
cd src
python -m book_analyzer --pages 5
```

Options: `--pages N` (20 books per page), `--delay SECONDS`, `--out DIR`.

Results are written to `outputs/books.csv`, `outputs/price_distribution.png` and `outputs/price_by_rating.png`.

## Run tests

```bash
pytest
```

## Ideas for extending it

- Scrape each book's detail page for category and description
- Store results in SQLite and track price changes over time
- Add a Streamlit dashboard
- Add GitHub Actions to run the tests on every push

## Note

This site exists for practice. If you adapt the scraper to another site, check its `robots.txt` and terms of service first.
