from internship_finder.filter import apply_filters
from internship_finder.models import Listing


def test_keyword_filter_matches_title_case_insensitive():
    """Keyword matches title as a case-insensitive substring."""
    listings = [
        Listing(title="ML Engineer Intern"),
        Listing(title="Backend SWE"),
        Listing(title="Software Engineer"),
    ]

    assert [item.title for item in apply_filters(listings, keyword="ml")] == ["ML Engineer Intern"]
    # "Backend SWE" doesn't contain "engineer"; the other two do.
    engineer_titles = sorted(item.title for item in apply_filters(listings, keyword="ENGINEER"))
    assert engineer_titles == ["ML Engineer Intern", "Software Engineer"]


def test_location_filter_matches_any_location_in_list():
    """Substring match against any location; missing/empty locations is skipped, not crashed on."""
    listings = [
        Listing(title="A", locations=["San Francisco, CA", "Remote"]),
        Listing(title="B", locations=["New York, NY"]),
        Listing(title="C", locations=[]),
        Listing(title="D"),  # no locations -> model defaults to empty list
    ]

    result = apply_filters(listings, location="remote")
    assert [item.title for item in result] == ["A"]


def test_company_filter_matches_company_name_case_insensitive():
    """Company matches as case-insensitive substring; missing/None company_name is excluded."""
    listings = [
        Listing(title="A", company_name="Google"),
        Listing(title="B", company_name="Stripe"),
        Listing(title="C", company_name="google deepmind"),
        Listing(title="D", company_name=None),
        Listing(title="E"),  # no company_name -> defaults to None, excluded
    ]

    google_titles = sorted(item.title for item in apply_filters(listings, company="google"))
    assert google_titles == ["A", "C"]

    stripe_titles = [item.title for item in apply_filters(listings, company="STRIPE")]
    assert stripe_titles == ["B"]


def test_filters_combine_with_and():
    """When multiple filters are set, only listings matching ALL of them survive."""
    listings = [
        # Matches keyword only.
        Listing(title="ML Engineer", company_name="Stripe", locations=["NYC"]),
        # Matches location only.
        Listing(title="Backend SWE", company_name="Stripe", locations=["Remote"]),
        # Matches company only.
        Listing(title="Backend SWE", company_name="Google", locations=["NYC"]),
        # Matches all three.
        Listing(title="ML Engineer", company_name="Google", locations=["Remote"]),
    ]

    result = apply_filters(listings, keyword="ml", location="remote", company="google")
    assert len(result) == 1
    assert result[0].company_name == "Google"
    assert result[0].locations == ["Remote"]
    assert result[0].title == "ML Engineer"


def test_limit_applies_after_sort():
    """Limit returns the N newest matches; missing date_posted sorts last."""
    listings = [
        Listing(title="old", date_posted=1000),
        Listing(title="newest", date_posted=5000),
        Listing(title="middle", date_posted=3000),
        Listing(title="no_date"),  # no date_posted -> sorts last
        Listing(title="second_newest", date_posted=4000),
    ]

    result = apply_filters(listings, limit=2)
    assert [item.title for item in result] == ["newest", "second_newest"]

    full = apply_filters(listings)
    assert [item.title for item in full] == [
        "newest",
        "second_newest",
        "middle",
        "old",
        "no_date",
    ]
