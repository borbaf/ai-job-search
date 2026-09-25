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

The user of this fork is a **Supply Chain & Logistics Leader** with 15+ years of operational
authority (terminal superintendent, fuel distribution coordinator, S&OP leader) currently
accelerating an applied career transition through **Data Analytics & BI (Python, SQL, Tableau, Power BI, GCP)**.

### Target Sweet Spots (Top Priority)
1. **Supply Chain Analytics, S&OP & BI:** Roles uniting operational leadership with data/automation
   (e.g., *Supply Chain Data Analyst*, *S&OP Analyst*, *Demand Planning Analyst - Data & Automation*, *BI Analyst*).
   Exemplified by roles like **INDI Staffing Services (BI Analyst - Remote, USD)** or **Drogaria Araujo / Loggi (Demand/S&OP with Python/SQL)**.
2. **Logistics Tech & Fleet Management Product:** Technical Product Owner in Fleet Management, TMS, WMS,
   or Supply Chain SaaS (exemplified by **Omron Automation**).

### Anti-patterns & Roles to Deprioritize
- **Pure Data Engineering:** Deep pipeline infrastructure (Spark/Kafka/Scala/Dataflow backend) with no business domain leverage.
- **Generic Product Owner:** Generalist PO in apparel, e-commerce, banking/fintech with no logistics/operations overlap.

### Constraints & Deal-breakers
- **Eligibility Filter:** Hard stop on US/foreign postings requiring domestic citizenship/green card/US work authorization without sponsorship (e.g. Core Health & Fitness). Must hire globally (EOR/Contractor/B2B) or sponsor.
- **Work Setup:**
  - **100% Remote:** Primary target (global/LATAM/Brazil; USD-denominated prioritized, floor USD 2,000/mo, target USD 5,000/mo).
  - **Hybrid in SC:** ONLY within ~80 km of Bombinhas-SC (Florianópolis, Itajaí, Balneário Camboriú, Navegantes). **Blumenau is NOT viable**.
  - **Hybrid in Fortaleza/CE:** Viable (open to relocation to Fortaleza).
  - **Excluded:** Hybrid or on-site in São Paulo (SP), Belo Horizonte (BH), Curitiba, Blumenau, etc.

---

## Recommended search queries (by priority)

### A. Supply Chain Analytics & S&OP (Top Sweet Spot)
```bash
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "supply chain analytics" -l "Remote" --remote remote --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "supply chain data analyst" -l "Remote" --remote remote --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "s&op analyst" -l "Remote" --remote remote --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "demand planning" -l "Remote" --remote remote --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "logistics analyst" -l "Remote" --remote remote --jobage 14 --format table
```

### B. Business Intelligence & Analytics (Operational Leverage)
```bash
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "business intelligence analyst" -l "Remote" --remote remote --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "data analyst" -l "Remote" --remote remote --jobage 14 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "analytics engineer" -l "Remote" --remote remote --jobage 14 --format table
```

### C. Logistics Tech & Fleet Product
```bash
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "fleet management product owner" -l "Remote" --jobage 30 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "logistics product owner" -l "Remote" --jobage 30 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "product owner" -l "Remote" --remote remote --jobage 14 --format table
```

### D. Local & Relocation Targets (SC 80km radius & Fortaleza/CE)
```bash
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "dados" -l "Florianópolis, Santa Catarina, Brazil" --jobage 30 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "logistica" -l "Itajaí, Santa Catarina, Brazil" --jobage 30 --format table
bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "dados" -l "Fortaleza, Ceará, Brazil" --jobage 30 --format table
```