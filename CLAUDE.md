# Internship-Finder CLI

A CLI tool for CS undergrads to aggregate SWE internships from public GitHub lists.

## Status

Phase 1 done. Both sources fetched and merged, filtered (keyword/location/company), rendered as a rich table, top 50 by date posted. First tests cover the filter module.

## Project Goals

- Ship a useful CLI that aggregates and filters internship listings.
- **Meta-goal**: the author is learning how to scaffold and ship a real Python project end-to-end (uv, packaging, git workflow, CI, tests, types). Prefer explanations and "the standard way pros do this" over shortcuts.

## Tech Stack & Conventions

- **Language**: Python 3.12+ (pinned via `.python-version`)
- **Package manager**: uv (never pip directly)
- **CLI**: typer
- **HTTP**: httpx, sync mode for Phase 1. Revisit async if source count grows or fetches become a bottleneck.
- **Validation/models**: pydantic. Defer until Phase 1.5 once we have a working fetch + filter pipeline.
- **Testing**: pytest
- **Lint/format**: ruff
- **Architecture**: Repository pattern for data sources, so adding Phase 2/3 sources doesn't churn the fetch/filter/render layers.

## Commands

```powershell
uv sync                         # install/lock deps into .venv
uv add <package>                # add a runtime dependency
uv add --dev <package>          # add a dev dependency
uv run internship-finder        # run the CLI entry point
uv run pytest                   # run tests
uv run ruff check               # lint
uv run ruff format              # format
```

## Git Workflow

- User creates feature branches for non-trivial work (e.g. `feat/fetch-simplify`, `feat/dedup-listings`). Claude Code commits to whatever branch is currently checked out and does not switch branches on its own.
- Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
- Each commit should leave the project in a working state.
- Do NOT add `Co-Authored-By: Claude` (or any AI co-author trailer) to commit messages. This project is the user's portfolio; AI tool use is acknowledged in CLAUDE.md and the README, but commits are attributed to the user only.

## Data Sources

### Phase 1: JSON sources (clean schema, identical format)

We're in May 2026 — Summer 2026 recruiting has effectively closed, and Summer 2027 is the next live cycle (applications open ~July 2026).

- **vanshb03/Summer2027-Internships** — primary cycle.
  - JSON: https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/dev/.github/scripts/listings.json
- **SimplifyJobs/Summer2026-Internships** — kept for off-season coverage (late Summer 2026 stragglers, Fall 2026 / Spring 2027 internships posted alongside summer ones).
  - JSON: https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/.github/scripts/listings.json

Both repos commit to `dev`, not `main`. The `main` branch is stale by design.

Schema fields per listing: `company_name`, `locations`, `title`, `date_posted` (unix ts), `terms`, `active`, `url`, `is_visible`, `source`, `company_url`, `date_updated`, `id`.

Filtering rules:
- `is_visible: false` -> drop entirely
- `active: false` -> keep, tag as `[CLOSED]`

Deduplication: match by `id`, fallback to `(company_name, title, url)`.

**Cycle-awareness (Phase 1.5)**: cycles roll over each year — by mid-2027 we'll want a Summer 2028 source, and Summer 2026 will be fully obsolete. The repository layer should make swapping/retiring sources cheap (no caller edits beyond registration), and listings will likely need a `cycle` tag once we're juggling 3+ overlapping cycles.

### Phase 2: Markdown sources (parsing required)

- speedyapply/2026-SWE-College-Jobs (FAANG+/Quant/Other tiering)
- speedyapply/2026-AI-College-Jobs (ML/AI specific, relevant for SHAKTI work)
- Files: INTERN_USA.md, INTERN_INTL.md, NEW_GRAD_USA.md, NEW_GRAD_INTL.md
- Needs a markdown table parser. Schema differs from Phase 1 sources.

### Phase 3: Niche sources

- zapplyjobs/underclassmen-internships: early-career programs (bootcamps, fellowships, "explorer days")

## Out of Scope

- Web UI / web app
- User accounts, auth, databases
- Scraping non-public sources (LinkedIn, Indeed, Handshake)
- Auto-applying to jobs

## Roadmap

- **Phase 1 (current)**: fetch JSON sources, filter, render terminal table, optional CSV/markdown export.
- **Phase 1.5**: pydantic `Listing` model, basic deduplication.
- **Phase 2**: markdown parsing for speedyapply lists; merged repository pattern.
- **Phase 3**: LLM relevance scoring (rank listings by fit to a resume blurb).
- **Phase 4**: scheduled runs + email/Slack digest.