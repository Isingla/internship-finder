"""SimplifyJobs/Summer2026-Internships data source.

Covers Summer 2026 (closing) plus Fall 2026 / Spring 2027 off-season listings.

Paused: not currently wired into run() — SimplifyJobs has no Summer 2027 repo yet.
Re-add to the merge in internship_finder/__init__.py when their 2027 repo launches.
"""

import httpx

from internship_finder.models import Listing

LISTINGS_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/.github/scripts/listings.json"


def fetch_listings() -> list[Listing]:
    """Fetch the SimplifyJobs Summer 2026 internships JSON and return it as a list of Listings."""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(LISTINGS_URL)
        response.raise_for_status()
        return [Listing(**row, source_repo="simplifyjobs") for row in response.json()]
