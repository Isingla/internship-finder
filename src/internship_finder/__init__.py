import truststore

# Use OS trust store so HTTPS works behind corporate / AV / VPN MITM proxies.
truststore.inject_into_ssl()

import typer  # noqa: E402

from internship_finder import filter as filter_module  # noqa: E402
from internship_finder import render  # noqa: E402
from internship_finder.sources import simplifyjobs, vansh_summer2027  # noqa: E402

app = typer.Typer(add_completion=False, no_args_is_help=False)


@app.command()
def run(
    keyword: str | None = typer.Option(None, "--keyword", "-k", help="Filter by keyword in title."),
    location: str | None = typer.Option(None, "--location", "-l", help="Filter by location."),
    company: str | None = typer.Option(None, "--company", "-c", help="Filter by company name."),
    limit: int = typer.Option(50, "--limit", help="Max listings to display."),
) -> None:
    """Fetch internships from configured sources, apply filters, render as a table."""
    simplify_listings = simplifyjobs.fetch_listings()
    for item in simplify_listings:
        item["_source"] = "simplifyjobs"

    vansh_listings = vansh_summer2027.fetch_listings()
    for item in vansh_listings:
        item["_source"] = "vansh_summer2027"

    merged = [
        item
        for item in (*simplify_listings, *vansh_listings)
        if item.get("is_visible") is not False
    ]

    filtered = filter_module.apply_filters(
        merged,
        keyword=keyword,
        location=location,
        company=company,
        limit=limit,
    )

    if not filtered:
        active = []
        if keyword is not None:
            active.append(f"keyword={keyword!r}")
        if location is not None:
            active.append(f"location={location!r}")
        if company is not None:
            active.append(f"company={company!r}")
        if active:
            print("No matches for " + " AND ".join(active))
        else:
            print("No listings available")
        return

    render.render_table(filtered)


def main() -> None:
    app()
