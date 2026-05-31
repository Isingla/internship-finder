"""The Listing model — the shared shape passed between sources, filter, dedup, render, and score.

Every upstream field we read is Optional with a default so partial or missing data (and the
partial fixtures our tests build) never raises. Upstream keys we don't use (season, sponsorship,
source, company_url, date_updated) are silently dropped via extra="ignore".
"""

from pydantic import BaseModel, ConfigDict, Field


class Listing(BaseModel):
    model_config = ConfigDict(extra="ignore")

    # Upstream fields we actually consume.
    id: str | None = None
    company_name: str | None = None
    title: str | None = None
    locations: list[str] = Field(default_factory=list)
    date_posted: int | None = None
    is_visible: bool | None = None  # tri-state preserved; the merge keeps `is not False`
    active: bool | None = None  # modeled for fidelity / future [CLOSED] tag; currently unread
    url: str | None = None

    # Our own annotations. Pydantic treats leading-underscore names as private attributes,
    # so the dict keys _source/_score/_score_reason become these regular optional fields.
    source_repo: str | None = None  # which configured source produced this, e.g. "vansh_summer2027"
    score: int | None = None  # set by score.score_listings()
    score_reason: str | None = None  # one-line rationale from the model
