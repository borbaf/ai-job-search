---
name: gupy-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Gupy
  (the dominant Brazilian ATS). Invoke for open positions, vacancies, and hiring on Gupy.
  Trigger phrases: gupy, vaga gupy, buscar no gupy, portal gupy.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/gupy-search/cli/src/cli.ts *)
---

# Gupy Search Skill

Search live job listings from **Gupy (portal.gupy.io)**, the leading Brazilian ATS used by large employers. Runs with bun; no API key.

> Access note: Gupy protects automated access (login + anti-bot). If the search fails or is blocked, fall back to pasting the job description into /apply.

## Candidate profile (search strategy)

Engineer/Consultant in Logistics Transformation, pivoting to Data & Product.
Priority: (1) Data/Analytics, (2) Product, (3) Supply Chain/Operations (data-flavored).
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Search: `https://portal.gupy.io/job-search/term=<termo>`
- Listing: `https://portal.gupy.io/jobs`
- Job page: `https://<empresa>.gupy.io/jobs/<id>`

## Commands

### Search job listings

    bun run .agents/skills/gupy-search/cli/src/cli.ts search --query "<termo>" [flags]

Key flags:
- --query <text> / -q <text> - keyword search (title, skill, role). Recommended.
- --location <text> / -l <text> - city/state (e.g. Remoto, Bombinhas, Fortaleza).
- --format json|table|plain - default json.

### Fetch full job detail

    bun run .agents/skills/gupy-search/cli/src/cli.ts detail <id|url> [--format json|plain]

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail |
| table | Quick human-readable scanning |
| plain | Reading a single job's full detail |

Errors go to stderr as { "error": "...", "code": "..." } with exit code 1.

## Notes

- Data from Gupy public job pages; may require login. Keep volume low.
