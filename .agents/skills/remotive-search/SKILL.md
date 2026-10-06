---
name: remotive-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Remotive (remotive.com),
  a premier global remote job board featuring tech, operations, data, product, and software roles.
  Invoke for open positions, vacancies, and hiring on Remotive.
  Trigger phrases: remotive, remotive.com, remote jobs remotive, vagas remotive, buscar no remotive.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/remotive-search/cli/src/cli.ts *)
---

# Remotive Search Skill

Search live remote job listings from **Remotive (remotive.com)**, a leading international remote job platform.

Runs with Bun; powered by Remotive's public live REST API (`remotive.com/api/remote-jobs`), zero external dependencies, with client-side keyword and recency filtering.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS), (3) Operations & Data Analytics.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Portal homepage: `https://remotive.com/`
- API endpoint: `https://remotive.com/api/remote-jobs`
- Posting detail: `https://remotive.com/remote-jobs/...`

## Commands

### Search job listings

```bash
bun run .agents/skills/remotive-search/cli/src/cli.ts search --query "<keyword>" [flags]
```

Key flags:
- `--query <text>` / `-q <text>` - search keywords across title, company, category, tags, candidate location, and description (e.g. `supply chain`, `operations`, `product manager`, `data`).
- `--category <slug>` / `-c <slug>` - filter by Remotive category slug (e.g. `data`, `product`, `operations`, `software-development`, `project-management`, `supply-chain`).
- `--limit <n>` / `-n <n>` - maximum number of results to display. Default 20.
- `--jobage <days>` - filter jobs posted within N days.
- `--format json|table|plain` - output format (default: `json`).

### Categories list

```bash
bun run .agents/skills/remotive-search/cli/src/cli.ts categories
```

Lists all official category slugs supported by Remotive.

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail or scraper pipeline |
| table | Quick human-readable scanning |
| plain | Reading job summaries in terminal |

Errors go to stderr as `{ "error": "...", "code": "..." }` with exit code 1.
