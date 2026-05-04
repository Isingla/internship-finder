import truststore

# Use OS trust store so HTTPS works behind corporate / AV / VPN MITM proxies.
truststore.inject_into_ssl()

from internship_finder.sources.simplify import fetch_listings  # noqa: E402


def main() -> None:
    """Entry point: fetch SimplifyJobs listings and print a summary count."""
    listings = fetch_listings()
    total = len(listings)
    visible = sum(1 for listing in listings if listing.get("is_visible"))
    visible_active = sum(
        1 for listing in listings if listing.get("is_visible") and listing.get("active")
    )
    print(f"Total listings: {total}")
    print(f"Visible: {visible}")
    print(f"Visible + active: {visible_active}")
