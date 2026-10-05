---
name: getonbrd-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Get on Board (getonbrd.com),
  a leading tech job board across Latin America and global remote roles.
  Invoke for open positions, vacancies, and hiring on Get on Board.
  Trigger phrases: getonbrd, get on board, vaga getonbrd, vagas getonbrd, buscar no getonbrd, getonboard.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/getonbrd-search/cli/src/cli.ts *)
---

# Get on Board Search Skill

Search live job listings from **Get on Board (getonbrd.com)**, the leading tech job platform connecting tech, data, operations, product, and engineering talent across Latin America (Brazil, Chile, Colombia, Mexico, Argentina, Peru, etc.) and global remote roles.

Runs with Bun; powered by Get on Board's official public REST API (`/api/v0/search/jobs`) with zero runtime dependencies and no API key required.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS), (3) Operations & Data Analytics.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD/BRL roles prioritized.

## URL patterns

- Portal homepage: `https://www.getonbrd.com/`
- Search API endpoint: `https://www.getonbrd.com/api/v0/search/jobs?query=<text>&expand[]=company`
- Detail URL pattern: `https://www.getonbrd.com/jobs/<slug>`

## Commands

### Search job listings

```bash
bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --query "<keyword>" [flags]
```

Key flags:
- `--query <text>` / `-q <text>` - search keywords (title, skill, role).
- `--remote` - filter for remote positions only.
- `--country <text>` / `-c <text>` - filter by country (e.g. Brazil, Chile, Colombia, Mexico, Remote).
- `--page <n>` - 1-indexed page number. Default 1.
- `--limit <n>` / `-n <n>` - maximum number of results to display. Default 20.
- `--format json|table|plain` - output format (default: `json`).

### Fetch full job detail

```bash
bun run .agents/skills/getonbrd-search/cli/src/cli.ts detail <id|url> [--format json|plain]
```

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail or scraper pipeline |
| table | Quick human-readable scanning |
| plain | Reading a single job's full detail in terminal |
