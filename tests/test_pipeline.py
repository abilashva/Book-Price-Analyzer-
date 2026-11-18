from pathlib import Path

import pytest

from book_analyzer.analysis import price_by_rating, summary
from book_analyzer.cleaning import build_dataframe, parse_price
from book_analyzer.scraper import BASE_URL, parse_page

FIXTURE = Path(__file__).parent / "fixtures" / "sample_page.html"


@pytest.fixture
def books_and_next():
    return parse_page(FIXTURE.read_text(encoding="utf-8"), page_url=BASE_URL + "page-1.html")


def test_parse_page_extracts_books(books_and_next):
    books, _ = books_and_next
    assert [b.title for b in books] == ["A Light in the Attic", "Tipping the Velvet", "Soumission"]
    assert [b.rating for b in books] == [3, 1, 5]
    assert [b.in_stock for b in books] == [True, True, False]


def test_parse_page_finds_next_url(books_and_next):
    _, next_url = books_and_next
    assert next_url == BASE_URL + "page-2.html"


def test_parse_price_handles_encoding_noise():
    assert parse_price("Â£51.77") == 51.77
    assert parse_price("£12.00") == 12.0
    with pytest.raises(ValueError):
        parse_price("free")


def test_dataframe_and_summary(books_and_next):
    books, _ = books_and_next
    df = build_dataframe(b.to_dict() for b in books)
    assert "price_gbp" in df.columns and "price" not in df.columns
    s = summary(df)
    assert s["books"] == 3
    assert s["cheapest"] == "Soumission"
    assert s["most_expensive"] == "Tipping the Velvet"
    assert s["in_stock_pct"] == pytest.approx(66.7, abs=0.1)


def test_duplicates_removed(books_and_next):
    books, _ = books_and_next
    df = build_dataframe([b.to_dict() for b in books] * 2)
    assert len(df) == 3


def test_price_by_rating(books_and_next):
    books, _ = books_and_next
    df = build_dataframe(b.to_dict() for b in books)
    stats = price_by_rating(df)
    assert set(stats["rating"]) == {1, 3, 5}
