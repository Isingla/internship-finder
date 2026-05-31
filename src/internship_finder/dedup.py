"""Collapse duplicate listings that appear across (or within) sources."""

from internship_finder.models import Listing


def dedup(listings: list[Listing]) -> list[Listing]:
    """Drop duplicates sharing a case-insensitive (company_name, title); keep the newest.

    Two listings collide when their lowercased (company_name, title) match. On a clash we
    keep the one with the higher date_posted (missing dates count as 0). First-seen order
    is preserved so the output stays stable for the caller's later sort.
    """
    best: dict[tuple[str, str], Listing] = {}
    order: list[tuple[str, str]] = []
    for item in listings:
        key = ((item.company_name or "").lower(), (item.title or "").lower())
        existing = best.get(key)
        if existing is None:
            best[key] = item
            order.append(key)
        elif (item.date_posted or 0) > (existing.date_posted or 0):
            best[key] = item
    return [best[key] for key in order]
