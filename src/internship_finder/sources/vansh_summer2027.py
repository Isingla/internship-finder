"""vanshb03/Summer2027-Internships data source — primary cycle (applications open ~July 2026)."""

import httpx

LISTINGS_URL = "https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/dev/.github/scripts/listings.json"


def fetch_listings() -> list[dict]:
    """Fetch the vanshb03 Summer 2027 internships JSON and return it as a list of dicts."""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(LISTINGS_URL)
        response.raise_for_status()
        return response.json()
