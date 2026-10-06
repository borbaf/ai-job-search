---
name: weworkremotely-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on We Work Remotely
  (weworkremotely.com), the premier international remote job board.
  Invoke for open positions, vacancies, and hiring on We Work Remotely.
  Trigger phrases: weworkremotely, we work remotely, wwr, vagas remotas internacionais, remote jobs wwr.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/weworkremotely-search/cli/src/cli.ts *)
---

# We Work Remotely Search Skill

Search live job listings from **We Work Remotely (weworkremotely.com)**, the largest remote work community in the world.

Runs with Bun; powered by We Work Remotely's public live RSS syndication feeds across major job categories with zero runtime dependencies and no API key required.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS), (3) Operations & Data Analytics.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Portal homepage: `https://weworkremotely.com/`
- RSS feeds: `https://weworkremotely.com/remote-jobs.rss`, `https://weworkremotely.com/categories/remote-management-and-finance-jobs.rss`, `https://weworkremotely.com/categories/remote-product-jobs.rss`
- Posting detail: `https://weworkremotely.com/remote-jobs/<slug>`

## Commands

### Search job listings

```bash
bun run .agents/skills/weworkremotely-search/cli/src/cli.ts search --query "<keyword>" [flags]
```

Key flags:
- `--query <text>` / `-q <text>` - search keywords across title, company, category, and description.
- `--category <text>` / `-c <text>` - filter by category (Product, Management, etc.).
- `--limit <n>` / `-n <n>` - maximum number of results to display. Default 20.
- `--format json|table|plain` - output format (default: `json`).

### Fetch full job detail

```bash
bun run .agents/skills/weworkremotely-search/cli/src/cli.ts detail <id|url> [--format json|plain]
```

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail or scraper pipeline |
| table | Quick human-readable scanning |
| plain | Reading a single job's full detail in terminal |

Errors go to stderr as `{ "error": "...", "code": "..." }` with exit code 1.
