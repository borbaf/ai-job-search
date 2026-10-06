---
name: ziprecruiter-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on ZipRecruiter (ziprecruiter.com),
  one of the largest job boards and matching networks in the US, UK, and internationally.
  Invoke for open positions, vacancies, and hiring on ZipRecruiter.
  Trigger phrases: ziprecruiter, zip recruiter, vaga ziprecruiter, buscar no ziprecruiter, ziprecruiter jobs.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/ziprecruiter-search/cli/src/cli.ts *)
---

# ZipRecruiter Search Skill

Search remote and international listings on **ZipRecruiter (ziprecruiter.com)**.

ZipRecruiter protects its web search endpoints with strict anti-bot and Cloudflare/PerimeterX protections that return HTTP 403 on automated requests. This CLI provides direct structured search URL generation, fallback querying, and structured results format compatible with the job-scraper agent workflow.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS), (3) Operations & Data Analytics.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Search URL: `https://www.ziprecruiter.com/jobs/search?q=<query>&l=<location>`
- Remote filter: `&l=Remote`
- Days filter: `&days=<days>` (e.g. `&days=7` or `&days=14`)
- Detail URL: `https://www.ziprecruiter.com/jobs/...`

## Commands

### Search job listings

```bash
bun run .agents/skills/ziprecruiter-search/cli/src/cli.ts search --query "<keyword>" [flags]
```

Key flags:
- `--query <text>` / `-q <text>` - search keywords across job titles and skills (e.g. `supply chain analyst`, `operations manager`, `product manager logistics`).
- `--location <text>` / `-l <text>` - target location (default: `Remote`).
- `--days <n>` - posted within the last N days (e.g. `14`, `7`).
- `--format json|table|plain` - output format (default: `json`).

### Generate Portal Search URLs

```bash
bun run .agents/skills/ziprecruiter-search/cli/src/cli.ts url --query "<keyword>" [--location Remote]
```

Returns the direct search URL for browser-based exploration or web search fallback.

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass query info to scraper pipeline |
| table | Quick human-readable scanning |
| plain | Reading job summaries in terminal |
