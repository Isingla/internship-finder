import truststore

# Use OS trust store so HTTPS works behind corporate / AV / VPN MITM proxies.
truststore.inject_into_ssl()

from internship_finder.sources import simplifyjobs, vansh_summer2027  # noqa: E402


def main() -> None:
    """Entry point: fetch both data sources and print per-source + combined counts."""
    simplify_listings = simplifyjobs.fetch_listings()
    simplify_total = len(simplify_listings)
    simplify_visible = sum(1 for listing in simplify_listings if listing.get("is_visible"))
    simplify_visible_active = sum(
        1 for listing in simplify_listings if listing.get("is_visible") and listing.get("active")
    )

    vansh_listings = vansh_summer2027.fetch_listings()
    vansh_total = len(vansh_listings)
    vansh_visible = sum(1 for listing in vansh_listings if listing.get("is_visible"))
    vansh_visible_active = sum(
        1 for listing in vansh_listings if listing.get("is_visible") and listing.get("active")
    )

    print("SimplifyJobs (Summer 2026 + off-season):")
    print(f"  Total: {simplify_total}")
    print(f"  Visible: {simplify_visible}")
    print(f"  Visible + active: {simplify_visible_active}")
    print()
    print("vanshb03 (Summer 2027):")
    print(f"  Total: {vansh_total}")
    print(f"  Visible: {vansh_visible}")
    print(f"  Visible + active: {vansh_visible_active}")
    print()
    print(f"Combined visible + active: {simplify_visible_active + vansh_visible_active}")
