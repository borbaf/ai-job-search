---
name: sprout-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Sprout (sprout.ph / usesprout.com),
  covering remote business operations, technology, HR SaaS, and global tech roles.
  Invoke for open positions, vacancies, and hiring on Sprout.
  Trigger phrases: sprout, sprout.ph, usesprout, vaga sprout, buscar no sprout.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/sprout-search/cli/src/cli.ts *)
---

# Sprout Search Skill

Search jobs and opportunities associated with **Sprout (sprout.ph / usesprout.com)**.

Sprout operates as an HR technology platform and AI-assisted job application ecosystem. Because listings are distributed across applicant tracking systems and platform portals, this CLI generates verified search endpoints, performs structured queries, and integrates with the `/scrape` pipeline.

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS), (3) Operations & Data Analytics.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Homepage: `https://sprout.ph/`
- AI Jobs Platform: `https://usesprout.com/`
- Careers: `https://sprout.ph/` (Careers & Talent Portal)

## Commands

### Search job listings

```bash
bun run .agents/skills/sprout-search/cli/src/cli.ts search --query "<keyword>" [flags]
```

Key flags:
- `--query <text>` / `-q <text>` - search keywords across job titles, operations, data, or product (e.g. `operations`, `data analyst`, `product manager`).
- `--location <text>` / `-l <text>` - target location (default: `Remote`).
- `--format json|table|plain` - output format (default: `json`).

### Generate Portal Search URLs

```bash
bun run .agents/skills/sprout-search/cli/src/cli.ts url --query "<keyword>"
```

Returns direct structured URLs for exploration.

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass query info to scraper pipeline |
| table | Quick human-readable scanning |
| plain | Reading job summaries in terminal |
