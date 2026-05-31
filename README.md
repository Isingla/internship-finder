# internship-finder

A command-line tool that aggregates SWE and ML internship listings from public, GitHub-maintained lists, filters them, and optionally AI-scores each one against a personal profile so the best-fit roles float to the top. Built for CS undergrads who'd rather run one command than click through five different repos. This is a personal learning project, not a polished product.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```powershell
git clone https://github.com/Isingla/internship-finder.git
cd internship-finder
uv sync
```

Scoring needs an Anthropic API key and a profile. Both have committed example files to copy:

1. **API key** — copy `.env.example` to `.env` and set your key:
   ```powershell
   copy .env.example .env
   # then edit .env and set ANTHROPIC_API_KEY=sk-ant-...
   ```
2. **Profile** — copy `profile.example.txt` to `profile.txt` and edit it to describe your year, skills, target roles, and locations. Claude scores listings against this text.
   ```powershell
   copy profile.example.txt profile.txt
   # then edit profile.txt
   ```
3. **Run:**
   ```powershell
   uv run internship-finder
   ```

The API key and profile are only needed when you pass `--score`. A plain run fetches and filters with no key required.

> **PowerShell gotcha:** don't create `.env` by redirecting (`echo ... > .env`). PowerShell 5.1's `>` writes UTF-16 with a BOM, which python-dotenv can't parse, and your key will silently fail to load. Open the file in an editor instead — e.g. `code .env`.

## What works today

- **Two live sources**, merged into one view: [vanshb03/Summer2027-Internships](https://github.com/vanshb03/Summer2027-Internships) (primary cycle) and [SimplifyJobs/Summer2026-Internships](https://github.com/SimplifyJobs/Summer2026-Internships) (off-season coverage). Listings hidden upstream (`is_visible: false`) are dropped.
- **Filters**, all optional and combinable: `--keyword`/`-k` (matches the title), `--location`/`-l` (matches any of a listing's locations), and `--company`/`-c` (matches the company name). All are case-insensitive substring matches.
- **Newest-first ordering**, capped by `--limit` (default 50). The cap is applied after filtering, so you get the newest *matching* listings, not the newest overall.
- **A rich terminal table** with Company, Title, Location, Posted date, Source, and a clickable Apply link.
- **AI relevance scoring** with `--score`: each listing is rated 0–100 with a one-line reason by Claude Haiku, and scored runs are re-sorted highest-first (adding Score and Reason columns to the table).
- **Score caching:** scores are cached to disk (`.cache/scores.json`) keyed on the listing plus your profile text, so re-runs are free but editing `profile.txt` re-scores everything.

## Usage

```powershell
# Basic run: fetch, merge, sort newest-first, show the top 50
uv run internship-finder

# Filtered run: backend roles in New York
uv run internship-finder --keyword backend --location "New York"

# Scored run: rank the listings against your profile.txt
uv run internship-finder --score

# Narrow, then score: 10 ML roles at Google, ranked by fit
uv run internship-finder -k "machine learning" -c Google --limit 10 --score
```

Narrowing with filters before `--score` is the cheap, fast path: you only spend API calls on listings you actually care about.

## Cost

Scoring uses Claude Haiku. A fresh full `--score` run is roughly **10–20 cents**. Because results are cached on disk, re-running the same scored query (without editing `profile.txt`) is **free** — no further API calls are made.

## Roadmap

Done:
- **Filters + rich table** (PR #5)
- **AI scoring + score caching** (PR #6)

Still planned:
- CI (lint + tests on every push).
- A Pydantic `Listing` model with basic deduplication.
- Markdown sources (speedyapply SWE/AI college-job lists).
- CSV / markdown export.

## Data sources

This tool aggregates publicly maintained internship lists. Credit and thanks to the maintainers — they do the hard work of keeping these current.

- [vanshb03/Summer2027-Internships](https://github.com/vanshb03/Summer2027-Internships) — live
- [SimplifyJobs/Summer2026-Internships](https://github.com/SimplifyJobs/Summer2026-Internships) — live
- [speedyapply/2026-SWE-College-Jobs](https://github.com/speedyapply/2026-SWE-College-Jobs) *(planned)*
- [speedyapply/2026-AI-College-Jobs](https://github.com/speedyapply/2026-AI-College-Jobs) *(planned)*
- [zapplyjobs/underclassmen-internships](https://github.com/zapplyjobs/underclassmen-internships) *(planned)*

## Tech stack

Python 3.12, [uv](https://docs.astral.sh/uv/) (packaging), [typer](https://typer.tiangolo.com/) (CLI), [httpx](https://www.python-httpx.org/) (fetching), [rich](https://rich.readthedocs.io/) (table output), the [Anthropic SDK](https://docs.anthropic.com/) (scoring), python-dotenv, and truststore. Dev: [pytest](https://docs.pytest.org/) and [ruff](https://docs.astral.sh/ruff/).

## License

MIT (TBD) — license file not yet added.
