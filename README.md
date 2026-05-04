# internship-finder

A command-line tool that aggregates SWE internship listings from public GitHub-maintained lists. Built for CS undergrads who want a single filtered view instead of clicking through five different repos. Phase 1 pulls structured JSON sources; later phases will add markdown-based lists and relevance scoring. This is a personal learning project, not a polished product.

## Status

Work in progress. Phase 1 is partially built.

What works today:
- Fetches the SimplifyJobs/Summer2026-Internships JSON feed.
- Prints summary counts: total listings, visible listings, and visible + active listings.

Not built yet:
- Filtering by location, term, or keyword.
- Rendering a terminal table of listings.
- Pulling from the second JSON source (vanshb03).
- Deduplication, pydantic models, CSV/markdown export.
- Markdown sources (speedyapply) and niche sources (zapplyjobs).

## Install

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```powershell
git clone https://github.com/Isingla/internship-finder.git
cd internship-finder
uv sync
```

## Usage

```powershell
uv run internship-finder
```

Today this fetches the SimplifyJobs listings JSON and prints three counts. That's it — no filtering, no table, no export yet.

## Roadmap

- **Phase 1**: fetch JSON sources, filter, render terminal table, optional CSV/markdown export.
- **Phase 1.5**: pydantic `Listing` model, basic deduplication.
- **Phase 2**: parse markdown-formatted sources (speedyapply lists).
- **Phase 3**: LLM relevance scoring (rank listings by fit to a resume blurb).
- **Phase 4**: scheduled runs + email/Slack digest.

## Data sources

This tool aggregates publicly maintained internship lists. Credit and thanks to the maintainers — they do the hard work of keeping these current.

- [SimplifyJobs/Summer2026-Internships](https://github.com/SimplifyJobs/Summer2026-Internships)
- [vanshb03/Summer2026-Internships](https://github.com/vanshb03/Summer2026-Internships) *(planned)*
- [speedyapply/2026-SWE-College-Jobs](https://github.com/speedyapply/2026-SWE-College-Jobs) *(planned)*
- [speedyapply/2026-AI-College-Jobs](https://github.com/speedyapply/2026-AI-College-Jobs) *(planned)*
- [zapplyjobs/underclassmen-internships](https://github.com/zapplyjobs/underclassmen-internships) *(planned)*

## Tech stack

**Installed today:** Python 3.12, uv, httpx, truststore.
**Planned:** typer (CLI), pydantic (models), pytest (tests), ruff (lint).

## License

MIT (TBD) — license file not yet added.
