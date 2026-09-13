---
name: linkedin-search
version: 1.3.0
description: >
  Use this skill whenever the user wants to search for jobs in any location or
  market, find job listings, or look up a specific job posting — in any country,
  city, or remotely. Invoke for open positions, vacancies, and hiring across any
  sector or role (software, data, design, marketing, finance, legal, operations,
  etc.). The location is always supplied explicitly by the user. Trigger phrases:
  find a job, job search, search for jobs, job openings, vacancies, hiring,
  positions open, remote jobs, "are there any X jobs in <place>", look up this
  job posting.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/linkedin-search/cli/src/cli.ts *)
---

# LinkedIn Search Skill

Search live job listings from LinkedIn's public job board for **any country/region**
(and remote). No authentication, no API key, and **zero runtime dependencies** — it runs
with just `bun`. The location is always passed explicitly, so the same skill works for a
forker in any market out of the box.

> This is a country-agnostic worked example of the repo's job-portal-skill pattern.
> LinkedIn's `jobs-guest` endpoints are global and the HTML parsing is country-independent;
> only the `--location` you pass changes per market.

## ⚠️ Personal use only

This uses LinkedIn's public job pages; automated access is against LinkedIn's Terms of
Service, so **keep volume low and don't use it commercially or for bulk data collection.**
Run it on your own responsibility.

---

## 🎯 Candidate profile (context for search strategy)

The user of this fork is a **Logistics Transformation Engineer & Consultant** with 15+
years in supply-chain optimization and operations leadership, currently **pivoting their
career toward Data & Product**. Search priority order:

1. **Data / Analytics** (top priority): Data Engineering, Analytics Engineering, Data
   Analyst, Business Intelligence, Data Science
2. **Product** (high priority): Product Owner, Product Manager, Data Product Owner
3. **Supply Chain / Logistics / Operations** (secondary — core background, apply only
   when they add clear data/analytics/tech value)

- **Seniority:** Senior / Specialist / Product Owner / Manager / Lead
- **Tools & skills to match on:** SQL, Python, Power BI, Tableau, Databricks, WMS, TMS,
  ERP (SAP), data mining, product discovery, agile/Scrum, PMO
- **Preferred work setup:** Remote (anywhere) or hybrid in **Brazil** (Bombinhas/SC,
  open to relocation to Fortaleza/CE); also targets **Latam** for remote roles
- **Compensation preference:** USD-denominated remote roles prioritized when international;
  floor USD 2,000/mo, target USD 5,000/mo

Use this profile to choose `--query` terms and to prioritize results. When the user asks
to "find jobs for me", default to the recommended queries below unless they specify otherwise.

---

## Recommended search queries (by priority)

### A. Data / Analytics (top priority)
```bash
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "analytics engineer" -l "Remote" --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "business intelligence" -l "Remote" --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "data analyst" -l "Bombinhas, Santa Catarina, Brazil" --jobage 30 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "data analyst" -l "Fortaleza, Ceará, Brazil" --jobage 30 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "data analyst" -l "Latam" --jobage 30 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "product owner" -l "Remote" --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "product manager" -l "Remote" --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "data product owner" -l "Remote" --jobage 30 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "product owner" -l "Latam" --jobage 30 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "supply chain" -l "Remote" --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "logistics" -l "Remote" --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "operations manager" -l "Remote" --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "procurement" -l "Remote" --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "supply chain" -l "Latam" --jobage 30 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "supply chain" -l "Remote" --remote remote --jobage 7 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "operations" -l "Remote" --remote remote --jobage 7 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "data" -l "Remote" --remote remote --jobage 7 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "product" -l "Remote" --remote remote --jobage 7 --format table