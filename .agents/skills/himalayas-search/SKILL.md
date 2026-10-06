---
name: himalayas-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Himalayas (himalayas.app),
  a premier global remote job board featuring transparent salaries, company insights, and global tech & operations roles.
  Invoke for open positions, vacancies, and hiring on Himalayas.
  Trigger phrases: himalayas, himalayas.app, remote jobs himalayas, vagas himalayas, buscar no himalayas.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/himalayas-search/cli/src/cli.ts *)
---

# Himalayas Search Skill

Search live remote job listings from **Himalayas (himalayas.app)**, the modern remote job platform with transparent salaries.

Runs with Bun; powered by Himalayas' public live REST API (`himalayas.app/jobs/api`) with cursor-based pagination, zero runtime dependencies, and no API key required.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS), (3) Operations & Data Analytics.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Portal homepage: `https://himalayas.app/`
- API endpoint: `https://himalayas.app/jobs/api`
- Posting detail: `https://himalayas.app/companies/<company>/jobs/<slug>`

## Commands

### Search job listings

```bash
bun run .agents/skills/himalayas-search/cli/src/cli.ts search --query "<keyword>" [flags]
```

Key flags:
- `--query <text>` / `-q <text>` - search keywords across title, company, categories, and description (e.g. `supply chain`, `operations`, `product manager`, `data`).
- `--category <text>` / `-c <text>` - filter by category name.
- `--limit <n>` / `-n <n>` - maximum number of results to display. Default 20.
- `--format json|table|plain` - output format (default: `json`).

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail or scraper pipeline |
| table | Quick human-readable scanning |
| plain | Reading job summaries in terminal |

Errors go to stderr as `{ "error": "...", "code": "..." }` with exit code 1.
