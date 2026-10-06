---
name: jobnagringa-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Job na Gringa (jobnagringa.com.br),
  a specialized Brazilian community and curated platform for remote international USD/EUR jobs.
  Invoke for open positions, vacancies, and hiring on Job na Gringa.
  Trigger phrases: job na gringa, jobnagringa, vaga job na gringa, vagas gringa, buscar no job na gringa.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/jobnagringa-search/cli/src/cli.ts *)
---

# Job na Gringa Search Skill

Search remote international job listings curated for Brazilian professionals from **Job na Gringa (jobnagringa.com.br)**.

Runs with Bun; provides query parsing, structured search URL generation, portal guidance, and integration with the `/scrape` pipeline.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS), (3) Operations & Data Analytics.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Portal homepage: `https://jobnagringa.com.br/`
- Community & Curated Board: `https://jobnagringa.com.br/`
- Discord & Member Hub: Community login required for member-exclusive unlisted postings.

## Commands

### Search job listings

```bash
bun run .agents/skills/jobnagringa-search/cli/src/cli.ts search --query "<keyword>" [flags]
```

Key flags:
- `--query <text>` / `-q <text>` - search keywords across title, domain, operations, or technology (e.g. `supply chain`, `operations`, `data analyst`, `product manager`).
- `--format json|table|plain` - output format (default: `json`).

### Generate Portal Search URLs

```bash
bun run .agents/skills/jobnagringa-search/cli/src/cli.ts url --query "<keyword>"
```

Returns direct search URLs and guidance for members.

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass query info to scraper pipeline |
| table | Quick human-readable scanning |
| plain | Reading job summaries in terminal |
