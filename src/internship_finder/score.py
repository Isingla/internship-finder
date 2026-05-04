"""AI-powered relevance scoring with Claude Haiku 4.5.

Scores 0-100 with a one-sentence reason, cached to disk.
"""

import hashlib
import json
from pathlib import Path

import anthropic
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)

MODEL = "claude-haiku-4-5-20251001"
CACHE_DIR = Path(".cache")
CACHE_FILE = CACHE_DIR / "scores.json"
PROFILE_PATH = Path("profile.txt")


def load_profile() -> str:
    """Read profile.txt. Raise FileNotFoundError with a clear message if missing."""
    if not PROFILE_PATH.exists():
        raise FileNotFoundError(
            f"{PROFILE_PATH} not found. Copy profile.example.txt to profile.txt and edit it."
        )
    return PROFILE_PATH.read_text(encoding="utf-8").strip()


def score_listings(listings: list[dict], profile: str) -> list[dict]:
    """Add _score (int 0-100) and _score_reason (str) to each listing.

    Reads cache, makes API calls only on cache miss, writes cache once at the end.
    Shows a rich progress bar. Mutates listings in place AND returns them.
    """
    cache = _load_cache()
    client = None  # built lazily on first cache miss so fully-cached runs need no API key

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:
        task = progress.add_task(f"Scoring {len(listings)} listings...", total=len(listings))
        for listing in listings:
            key = _cache_key(listing, profile)
            if key in cache:
                cached = cache[key]
                listing["_score"] = cached["score"]
                listing["_score_reason"] = cached["reason"]
            else:
                if client is None:
                    client = anthropic.Anthropic()
                result = _call_anthropic(client, listing, profile)
                listing["_score"] = result["score"]
                listing["_score_reason"] = result["reason"]
                cache[key] = result
            progress.advance(task)

    _save_cache(cache)
    return listings


def _cache_key(listing: dict, profile: str) -> str:
    """SHA-256 hex of (id || title+company fallback, title, company_name, profile)."""
    listing_id = listing.get("id")
    title = listing.get("title") or ""
    company = listing.get("company_name") or ""
    identity = str(listing_id) if listing_id is not None else f"{title}|{company}"
    payload = "\x1f".join([identity, title, company, profile])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _load_cache() -> dict[str, dict]:
    """Load cache JSON, return {} if file missing or unreadable."""
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_cache(cache: dict[str, dict]) -> None:
    """Write cache, creating .cache/ if needed."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def _build_prompt(listing: dict, profile: str) -> str:
    """Build the user prompt string for one listing."""
    company = listing.get("company_name") or "unspecified"
    title = listing.get("title") or "unspecified"
    locations = listing.get("locations") or []
    locations_str = ", ".join(locations) or "unspecified"
    return f"""You are scoring an internship listing for a candidate.

Candidate profile:
{profile}

Listing:
- Company: {company}
- Title: {title}
- Locations: {locations_str}

Rate this listing 0-100 for fit (100 = perfect match for the candidate's skills and interests).
Respond with valid JSON only, no markdown, no preamble:
{{"score": <int 0-100>, "reason": "<one short sentence>"}}
"""


def _call_anthropic(client, listing: dict, profile: str) -> dict:
    """One API call. Returns {"score": int, "reason": str}.

    On parse failure or any exception: return {"score": 0, "reason": "scoring failed"}.
    Never raises — failures must not crash the whole batch.
    """
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=200,
            system="You output only valid JSON. No markdown, no preamble.",
            messages=[
                {"role": "user", "content": _build_prompt(listing, profile)},
                {"role": "assistant", "content": "{"},
            ],
        )
        text = "{" + response.content[0].text
        parsed = json.loads(text)
        score = max(0, min(100, int(parsed.get("score", 0))))
        reason = parsed.get("reason")
        if not isinstance(reason, str):
            reason = "no reason given"
        return {"score": score, "reason": reason}
    except Exception:
        return {"score": 0, "reason": "scoring failed"}
