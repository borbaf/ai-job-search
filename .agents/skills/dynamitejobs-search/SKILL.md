---
name: dynamitejobs-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Dynamite Jobs
  (an international remote-first job board). Invoke for open positions, vacancies, and hiring on Dynamite Jobs.
  Trigger phrases: dynamite jobs, remote jobs, vaga remota.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/dynamitejobs-search/cli/src/cli.ts *)
---

# Dynamite Jobs Search Skill

Search live job listings from **Dynamite Jobs (dynamitejobs.com)**, an international remote-first job board. No login, no API key.

> Access note: Public search works without login. The Company API (/developers) is for hiring companies - ignore it.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS). Anti-pattern: Junior Data Analyst.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Search: `https://dynamitejobs.com/remote-jobs?text=<termo>&page=<n>`
- By country: `https://dynamitejobs.com/country/remote-jobs-in-<pais>`
- By skill: `https://dynamitejobs.com/skill/remote-<skill>-jobs`

## Commands

### Search job listings

    bun run .agents/skills/dynamitejobs-search/cli/src/cli.ts search --query "<termo>" [flags]

Key flags:
- --query <text> / -q <text> - keyword search (title, skill, role). Recommended.
- --location <text> / -l <text> - city/state (e.g. Remoto, Bombinhas, Fortaleza).
- --format json|table|plain - default json.

### Fetch full job detail

    bun run .agents/skills/dynamitejobs-search/cli/src/cli.ts detail <id|url> [--format json|plain]

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail |
| table | Quick human-readable scanning |
| plain | Reading a single job's full detail |

Errors go to stderr as { "error": "...", "code": "..." } with exit code 1.

## Notes

- Data from Dynamite Jobs public pages; no login required.
