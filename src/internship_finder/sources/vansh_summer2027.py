"""vanshb03/Summer2027-Internships data source.

Primary cycle (applications open ~July 2026).
"""

import httpx

from internship_finder.models import Listing

LISTINGS_URL = "https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/dev/.github/scripts/listings.json"


def fetch_listings() -> list[Listing]:
    """Fetch the vanshb03 Summer 2027 internships JSON and return it as a list of Listings."""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(LISTINGS_URL)
        response.raise_for_status()
        return [Listing(**row, source_repo="vansh_summer2027") for row in response.json()]
