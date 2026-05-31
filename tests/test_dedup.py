from internship_finder.dedup import dedup
from internship_finder.models import Listing


def test_no_duplicates_returns_all():
    """Distinct (company, title) pairs all survive, first-seen order preserved."""
    listings = [
        Listing(company_name="Google", title="SWE Intern", date_posted=100),
        Listing(company_name="Stripe", title="Backend Intern", date_posted=200),
    ]
    result = dedup(listings)
    assert [(item.company_name, item.title) for item in result] == [
        ("Google", "SWE Intern"),
        ("Stripe", "Backend Intern"),
    ]


def test_exact_duplicate_collapses_to_one():
    """Two identical (company, title) entries collapse to a single listing."""
    listings = [
        Listing(company_name="TMEIC", title="Software Engineer Intern", date_posted=100),
        Listing(company_name="TMEIC", title="Software Engineer Intern", date_posted=100),
    ]
    assert len(dedup(listings)) == 1


def test_near_duplicate_keeps_newer_date():
    """Same (company, title), different date_posted -> the newer one wins, regardless of order."""
    older = Listing(company_name="TMEIC", title="SWE Intern", date_posted=100, url="old")
    newer = Listing(company_name="TMEIC", title="SWE Intern", date_posted=500, url="new")
    assert dedup([older, newer])[0].url == "new"
    assert dedup([newer, older])[0].url == "new"
    assert len(dedup([older, newer])) == 1


def test_duplicate_across_merged_sources_collapses():
    """A listing present in two source lists (merged) dedupes to one, keeping the newer."""
    source_a = [Listing(company_name="Rippling", title="Frontend Intern", date_posted=100, url="a")]
    source_b = [Listing(company_name="Rippling", title="Frontend Intern", date_posted=300, url="b")]
    result = dedup([*source_a, *source_b])
    assert len(result) == 1
    assert result[0].url == "b"


def test_dedup_is_case_insensitive():
    """Company/title casing differences still count as the same listing; newer kept."""
    listings = [
        Listing(company_name="TMEIC", title="Software Engineer Intern", date_posted=100),
        Listing(company_name="tmeic", title="software engineer intern", date_posted=200),
    ]
    result = dedup(listings)
    assert len(result) == 1
    assert result[0].date_posted == 200
