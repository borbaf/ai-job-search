---
name: catho-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Catho
  (a major Brazilian job board). Invoke for open positions, vacancies, and hiring on Catho.
  Trigger phrases: catho, vaga catho, buscar no catho.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/catho-search/cli/src/cli.ts *)
---

# Catho Search Skill

Search live job listings from **Catho (catho.com.br)**, a major Brazilian job board. Runs with bun; no API key.

> Access note: Catho requires login for full listings and protects automated access. If blocked, fall back to pasting the description into /apply.

## Candidate profile (search strategy)

Engineer/Consultant in Logistics Transformation, pivoting to Data & Product.
Priority: (1) Data/Analytics, (2) Product, (3) Supply Chain/Operations (data-flavored).
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Search: `https://www.catho.com.br/vagas`

## Commands

### Search job listings

    bun run .agents/skills/catho-search/cli/src/cli.ts search --query "<termo>" [flags]

Key flags:
- --query <text> / -q <text> - keyword search (title, skill, role). Recommended.
- --location <text> / -l <text> - city/state (e.g. Remoto, Bombinhas, Fortaleza).
- --format json|table|plain - default json.

### Fetch full job detail

    bun run .agents/skills/catho-search/cli/src/cli.ts detail <id|url> [--format json|plain]

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail |
| table | Quick human-readable scanning |
| plain | Reading a single job's full detail |

Errors go to stderr as { "error": "...", "code": "..." } with exit code 1.

## Notes

- Data from Catho public job pages; may require login. Keep volume low.
