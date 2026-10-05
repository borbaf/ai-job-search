---
name: solvoglobal-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Solvo Global (careers.solvoglobal.com),
  a nearshore talent and staffing platform offering remote and on-site roles for US and global companies across LATAM.
  Invoke for open positions, vacancies, and hiring on Solvo Global.
  Trigger phrases: solvo, solvoglobal, solvo global, vaga solvo, vagas solvo global, buscar no solvo.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/solvoglobal-search/cli/src/cli.ts *)
---

# Solvo Global Search Skill

Search live job listings from **Solvo Global (careers.solvoglobal.com)**, connecting bilingual and specialized talent in Latin America (Colombia, Mexico, Argentina, etc.) to US and global companies across operations, logistics/supply chain, customer support, IT/development, finance, and back-office roles.

Runs with Bun; no external dependencies or API keys required.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS). Anti-pattern: Junior Data Analyst.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Search / Listing page: `https://careers.solvoglobal.com/job-listing/`
- AJAX endpoint: `https://careers.solvoglobal.com/wp-admin/admin-ajax.php` (action: `fetch_jobs`)

## Commands

### Search job listings

```bash
bun run .agents/skills/solvoglobal-search/cli/src/cli.ts search --query "<keyword>" [flags]
```

Key flags:
- `--query <text>` / `-q <text>` - search keywords (title, skill, role).
- `--country <text>` / `-c <text>` - filter by country (e.g. Colombia, Mexico, Argentina).
- `--location <text>` / `-l <text>` - alias for `--country` or city/location filtering.
- `--page <n>` - 1-indexed page number. Default 1.
- `--limit <n>` / `-n <n>` - maximum number of results to display. Default 20.
- `--format json|table|plain` - output format (default: `json`).

### Fetch full job detail

```bash
bun run .agents/skills/solvoglobal-search/cli/src/cli.ts detail <id|url> [--format json|plain]
```

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail |
| table | Quick human-readable scanning |
| plain | Reading a single job's full detail |

Errors are written to **stderr** as `{ "error": "...", "code": "..." }` with exit code `1`.

## Notes

- Data is fetched directly from Solvo Global's public job listing AJAX endpoint (`fetch_jobs`).
- Jobs are categorized by country, city, remote eligibility (`Yes` / `No` / hybrid), and department/vertical.
