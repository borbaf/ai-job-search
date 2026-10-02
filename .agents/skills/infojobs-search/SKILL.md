---
name: infojobs-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Infojobs
  (a major Brazilian job board). Invoke for open positions, vacancies, and hiring on Infojobs.
  Trigger phrases: infojobs, vaga infojobs, buscar no infojobs.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/infojobs-search/cli/src/cli.ts *)
---

# Infojobs Search Skill

Search live job listings from **Infojobs (infojobs.com.br)**, a major Brazilian job board. Runs with bun; no API key.

> Access note: Infojobs requires login for full listings and protects automated access. If blocked, fall back to pasting the description into /apply.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS). Anti-pattern: Junior Data Analyst.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Search: `https://www.infojobs.com.br`
- Company: `https://www.infojobs.com.br/<empresa>/vagas`
- Mobile: `https://m.infojobs.com.br`

## Commands

### Search job listings

    bun run .agents/skills/infojobs-search/cli/src/cli.ts search --query "<termo>" [flags]

Key flags:
- --query <text> / -q <text> - keyword search (title, skill, role). Recommended.
- --location <text> / -l <text> - city/state (e.g. Remoto, Bombinhas, Fortaleza).
- --format json|table|plain - default json.

### Fetch full job detail

    bun run .agents/skills/infojobs-search/cli/src/cli.ts detail <id|url> [--format json|plain]

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail |
| table | Quick human-readable scanning |
| plain | Reading a single job's full detail |

Errors go to stderr as { "error": "...", "code": "..." } with exit code 1.

## Notes

- Data from Infojobs public job pages; may require login. Keep volume low.
