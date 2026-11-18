"""Scrape book listings from books.toscrape.com (a site built for scraping practice)."""

from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from typing import Iterator
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/"
FIRST_PAGE = "page-1.html"
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
HEADERS = {"User-Agent": "book-price-analyzer/1.0 (learning project)"}


@dataclass
class Book:
    title: str
    price: str
    rating: int
    in_stock: bool
    url: str

    def to_dict(self) -> dict:
        return asdict(self)


def parse_page(html: str, page_url: str = BASE_URL) -> tuple[list[Book], str | None]:
    """Parse one listing page. Returns (books, absolute URL of next page or None)."""
    soup = BeautifulSoup(html, "html.parser")
    books: list[Book] = []

    for article in soup.select("article.product_pod"):
        link = article.select_one("h3 a")
        rating_tag = article.select_one("p.star-rating")
        rating_word = next(
            (c for c in (rating_tag.get("class", []) if rating_tag else []) if c in RATING_WORDS),
            None,
        )
        books.append(
            Book(
                title=link["title"],
                price=article.select_one("p.price_color").get_text(strip=True),
                rating=RATING_WORDS.get(rating_word, 0),
                in_stock="in stock" in article.select_one("p.availability").get_text().lower(),
                url=urljoin(page_url, link["href"]),
            )
        )

    next_link = soup.select_one("li.next a")
    next_url = urljoin(page_url, next_link["href"]) if next_link else None
    return books, next_url


def scrape(max_pages: int = 5, delay: float = 0.5) -> Iterator[Book]:
    """Yield books page by page, politely waiting `delay` seconds between requests."""
    url: str | None = urljoin(BASE_URL, FIRST_PAGE)
    pages = 0
    while url and pages < max_pages:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        response.encoding = "utf-8"
        books, url = parse_page(response.text, page_url=response.url)
        yield from books
        pages += 1
        if url:
            time.sleep(delay)
