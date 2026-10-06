---
name: remotar-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Remotar (remotar.com.br),
  a premier Brazilian job board specializing in 100% remote and flexible tech, operations,
  product, and data roles across Brazil and Latin America.
  Invoke for open positions, vacancies, and hiring on Remotar.
  Trigger phrases: remotar, vaga remotar, vagas remotar, buscar no remotar, portal remotar.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/remotar-search/cli/src/cli.ts *)
---

# Remotar Search Skill

Search live remote job listings from **Remotar (remotar.com.br)**, a leading remote-first job platform in Brazil and LATAM.

Runs with Bun; powered by Remotar's public REST API (`api.remotar.com.br/jobs`) with zero runtime dependencies and no API key required.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS), (3) Operations & Data Analytics.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD or BRL roles.

## URL patterns

- Portal homepage: `https://remotar.com.br/`
- Search page: `https://remotar.com.br/search/jobs`
- API endpoint: `https://api.remotar.com.br/jobs`
- Posting detail: `https://remotar.com.br/job/<id>`

## Commands

### Search job listings

```bash
bun run .agents/skills/remotar-search/cli/src/cli.ts search --query "<keyword>" [flags]
```

Key flags:
- `--query <text>` / `-q <text>` - search keywords across title, company, category, and requirements (e.g. `supply chain`, `logistica`, `dados`, `operacoes`).
- `--category <text>` / `-c <text>` - filter by category name.
- `--limit <n>` / `-n <n>` - maximum number of results to display. Default 20.
- `--format json|table|plain` - output format (default: `json`).

### Fetch full job detail

```bash
bun run .agents/skills/remotar-search/cli/src/cli.ts detail <id|url> [--format json|plain]
```

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail or scraper pipeline |
| table | Quick human-readable scanning |
| plain | Reading a single job's full detail in terminal |

Errors go to stderr as `{ "error": "...", "code": "..." }` with exit code 1.
