import json

from internship_finder import score


def test_cache_key_stable_for_same_input():
    """Same listing + profile → same cache key on repeated calls."""
    listing = {"id": "abc123", "title": "ML Intern", "company_name": "Stripe"}
    profile = "I like ML."

    assert score._cache_key(listing, profile) == score._cache_key(listing, profile)


def test_cache_key_changes_when_profile_changes():
    """Editing the profile invalidates the cache so listings get re-scored."""
    listing = {"id": "abc123", "title": "ML Intern", "company_name": "Stripe"}

    a = score._cache_key(listing, "I like ML.")
    b = score._cache_key(listing, "I like distributed systems.")
    assert a != b


def test_cache_key_falls_back_to_title_company_when_id_missing():
    """Listings without an id still get a stable key from (title, company)."""
    no_id = {"title": "ML Intern", "company_name": "Stripe"}
    other = {"title": "Backend Intern", "company_name": "Stripe"}

    assert score._cache_key(no_id, "p") == score._cache_key(no_id, "p")
    assert score._cache_key(no_id, "p") != score._cache_key(other, "p")


def test_build_prompt_includes_profile_title_company():
    """The prompt must surface the candidate profile and key listing fields."""
    listing = {"title": "ML Intern", "company_name": "Stripe", "locations": ["NYC", "Remote"]}
    profile = "MAGIC_PROFILE_MARKER undergrad."

    prompt = score._build_prompt(listing, profile)
    assert "MAGIC_PROFILE_MARKER" in prompt
    assert "ML Intern" in prompt
    assert "Stripe" in prompt
    assert "NYC" in prompt


def test_call_anthropic_returns_zero_on_parse_failure():
    """Malformed JSON from the API must not crash; listing gets score=0."""

    class FakeContent:
        text = "not json at all"

    class FakeResponse:
        content = [FakeContent()]

    class FakeClient:
        class messages:
            @staticmethod
            def create(**_kwargs):
                return FakeResponse()

    result = score._call_anthropic(FakeClient(), {"title": "x", "company_name": "y"}, "p")
    assert result == {"score": 0, "reason": "scoring failed"}


def test_call_anthropic_clamps_score_to_0_100():
    """A model returning an out-of-range score gets clamped, not propagated raw."""

    class FakeContent:
        text = '"score": 250, "reason": "great"}'  # SDK prefill "{" is prepended in _call_anthropic

    class FakeResponse:
        content = [FakeContent()]

    class FakeClient:
        class messages:
            @staticmethod
            def create(**_kwargs):
                return FakeResponse()

    result = score._call_anthropic(FakeClient(), {"title": "x", "company_name": "y"}, "p")
    assert result["score"] == 100
    assert result["reason"] == "great"


def test_score_listings_uses_cache_and_skips_api(monkeypatch, tmp_path):
    """A fully cached run reads scores from disk and never constructs the API client."""
    cache_file = tmp_path / "scores.json"
    monkeypatch.setattr(score, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(score, "CACHE_FILE", cache_file)

    listing = {"id": "L1", "title": "ML Intern", "company_name": "Stripe"}
    profile = "Test profile."
    key = score._cache_key(listing, profile)
    cache_file.write_text(
        json.dumps({key: {"score": 87, "reason": "good fit"}}), encoding="utf-8"
    )

    def boom(*_args, **_kwargs):
        raise AssertionError("anthropic client must not be constructed on a full cache hit")

    monkeypatch.setattr(score.anthropic, "Anthropic", boom)

    result = score.score_listings([listing], profile)
    assert result[0]["_score"] == 87
    assert result[0]["_score_reason"] == "good fit"
