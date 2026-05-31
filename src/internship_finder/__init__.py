import truststore

# Use OS trust store so HTTPS works behind corporate / AV / VPN MITM proxies.
truststore.inject_into_ssl()

import typer  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

from internship_finder import filter as filter_module  # noqa: E402
from internship_finder import render, score  # noqa: E402
from internship_finder.sources import vansh_summer2027  # noqa: E402

app = typer.Typer(add_completion=False, no_args_is_help=False)


@app.command()
def run(
    keyword: str | None = typer.Option(None, "--keyword", "-k", help="Filter by keyword in title."),
    location: str | None = typer.Option(None, "--location", "-l", help="Filter by location."),
    company: str | None = typer.Option(None, "--company", "-c", help="Filter by company name."),
    limit: int = typer.Option(50, "--limit", help="Max listings to display."),
    score_listings: bool = typer.Option(
        False, "--score", help="Score listings against profile.txt with Claude Haiku."
    ),
) -> None:
    """Fetch internships from configured sources, apply filters, render as a table."""
    vansh_listings = vansh_summer2027.fetch_listings()
    for item in vansh_listings:
        item["_source"] = "vansh_summer2027"

    # SimplifyJobs is paused: their org only has Summer2026 (closing cycle) — no
    # Summer2027 repo exists yet. Re-add simplifyjobs to the merge when it launches.
    merged = [item for item in vansh_listings if item.get("is_visible") is not False]

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

    if score_listings:
        profile = score.load_profile()
        score.score_listings(filtered, profile)
        filtered.sort(key=lambda item: item.get("_score") or 0, reverse=True)

    render.render_table(filtered, show_scores=score_listings)


def main() -> None:
    # Load .env so ANTHROPIC_API_KEY is picked up by the anthropic SDK.
    load_dotenv()
    app()
