"""Pure-function filters for internship listings. No I/O, no side effects — easily testable."""


def apply_filters(
    listings: list[dict],
    keyword: str | None = None,
    location: str | None = None,
    company: str | None = None,
    limit: int | None = None,
) -> list[dict]:
    """Apply optional keyword/location/company filters, sort newest first, then cap at limit.

    Order: keyword → location → company → sort → limit. Limit runs last so callers asking
    for "the 5 newest matching" don't get "the 5 newest overall, then filtered".
    """
    result = listings

    if keyword is not None:
        needle = keyword.lower()
        result = [item for item in result if needle in (item.get("title") or "").lower()]

    if location is not None:
        needle = location.lower()
        result = [
            item
            for item in result
            if any(needle in loc.lower() for loc in (item.get("locations") or []))
        ]

    if company is not None:
        needle = company.lower()
        result = [
            item
            for item in result
            if item.get("company_name") and needle in item["company_name"].lower()
        ]

    # Sort newest first; missing/zero date_posted sorts last.
    result = sorted(result, key=lambda item: item.get("date_posted") or 0, reverse=True)

    if limit is not None:
        result = result[:limit]

    return result
