"""Rich-based terminal output for filtered listings."""

from datetime import UTC, datetime

from rich.console import Console
from rich.table import Table


def render_table(listings: list[dict], show_scores: bool = False) -> None:
    """Print a rich table of listings. Caller must guard against empty input.

    When show_scores is True, insert Score and Reason columns between Posted and Source.
    """
    table = Table(title=f"Internships ({len(listings)} matched)")
    table.add_column("Company", style="bold")
    table.add_column("Title")
    table.add_column("Location")
    table.add_column("Posted")
    if show_scores:
        table.add_column("Score")
        table.add_column("Reason", overflow="fold")
    table.add_column("Source")
    table.add_column("Apply")

    for item in listings:
        company = item.get("company_name") or "—"
        title = item.get("title") or "—"
        location = _format_locations(item.get("locations") or [])
        posted_ts = item.get("date_posted") or 0
        posted = (
            datetime.fromtimestamp(posted_ts, tz=UTC).strftime("%Y-%m-%d") if posted_ts else "—"
        )
        source = item.get("_source") or "—"
        url = item.get("url") or ""
        apply_cell = f"[link={url}]Apply[/link]" if url else "—"
        if show_scores:
            score_cell = f"[bold]{item.get('_score', 0)}[/bold]"
            reason_cell = item.get("_score_reason") or "—"
            table.add_row(
                company, title, location, posted, score_cell, reason_cell, source, apply_cell
            )
        else:
            table.add_row(company, title, location, posted, source, apply_cell)

    Console().print(table)


def _format_locations(locations: list[str]) -> str:
    """Format a list of locations: 'X, Y' if 1-2 entries; 'X + N more' if 3+."""
    if not locations:
        return "—"
    if len(locations) <= 2:
        return ", ".join(locations)
    return f"{locations[0]} + {len(locations) - 1} more"
