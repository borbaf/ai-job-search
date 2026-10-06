# Search Queries & Channel Strategy for Job Scraper

<!-- Generated and updated per career consulting guidance for Filippe Borba. -->

## Channel & Portal Strategy (5 Tiers)

The framework structures job searching across five distinct tiers, prioritizing high-conversion channels for remote USD/global opportunities:

### Tier 1: LATAM & Global Talent Platforms (Short-term Priority)
Primary channel for immediate focus. Connects LATAM professionals to US/global companies with structured, objective processes:
- **HireLATAM** (`hirelatam.com` / `hirelatam-search` CLI) — US companies hiring top-tier LATAM talent for remote operations and analytics.
- **Solvo Global** (`solvoglobal.com`) — Remote recruiting with objective, structured workflows for operational and analytical roles.
- **Revelo** (`revelo.com`) — Strong in technology, analytics, and agile placement with rapid candidate-to-offer velocity.
- **Get on Board** (`getonbrd.com`) — Tech and operations roles in high-growth startups across LATAM and globally.

### Tier 2: Global Remote Job Boards
Established global aggregators with high-signal remote opportunities:
- **FlexJobs** (`flexjobs.com`) — Curated and verified remote job listings with minimal spam (subscription board).
- **We Work Remotely** (`weworkremotely.com`) — Premier global 100% remote job community.
- **Remotive** (`remotive.com` / `remotive-search` CLI) — Leading international remote job board for software, data, operations, and product.
- **Wellfound** (formerly AngelList Talent, `wellfound.com`) — Startup ecosystem, venture-backed scale-ups, and early tech teams.

### Tier 3: Worthwhile Niche & Community Job Boards
High-value specialized boards for international and remote roles:
- **Remotar** (`remotar.com.br`) — Curated remote listings for Brazilian and international talent.
- **Himalayas** (`himalayas.app`) — Fast-growing global remote tech job database with comprehensive company insights.
- **ZipRecruiter** (`ziprecruiter.com` / `ziprecruiter-search` CLI) — Algorithmic matching, heavily adopted in the US, UK, and Ireland.
- **Snaphunt** (`snaphunt.com`) — Global talent matching platform strong in Europe and Asia.
- **Sprout** (`sprout.ph` / global boards) — Remote business operations and technology roles.
- **Job na Gringa** (`jobnagringa.com.br`) — Specialized community supporting Brazilian talent landing remote roles abroad, featuring unlisted opportunities, English coaching, and recruiter networking.

### Tier 4: Startups & Developer Communities
Engineering and high-tempo startup environments:
- **Y Combinator Jobs** (`workatastartup.com`) — Exclusive job board for Y Combinator portfolio startups.
- **Hacker News** (`news.ycombinator.com`) — Monthly "Who is hiring?" threads (1st of each month).
- **DEV Community** (`dev.to/jobs`) — Tech-first and engineering-adjacent operational openings.

### Tier 5: Executive Search & Venture Boutiques
High-touch executive and leadership placement:
- **Venture People** (`venturepeople.com.br`) — Executive search boutique specializing in leadership, operations, and tech for venture-backed startups and scale-ups across LATAM and the USA.

---

## Installed Portal CLIs & WebSearch Integration

`/scrape` automatically discovers and runs installed portal skills under `.agents/skills/*/SKILL.md`:
- **Active CLIs:** `linkedin-search`, `freehire-search`, `hirelatam-search`, `solvoglobal-search`, `getonbrd-search`, `weworkremotely-search`, `remotar-search`, `himalayas-search`, `remotive-search`, `ziprecruiter-search`, `gupy-search`, `catho-search`, `infojobs-search`, `dynamitejobs-search`.
- For boards without a dedicated CLI, `/scrape` executes Google WebSearch fallback queries below.

**Language scope:** Queries are generated in **English and Portuguese** (languages spoken professionally). Spanish is excluded from query generation (elementary level).

---

## Query Categories (Aligned with Sweet Spots)

### Priority 1: Supply Chain Analytics, S&OP & BI (Top Sweet Spot)
Capitalizes on 15+ years of operational authority paired with data execution (Python, SQL, BigQuery, Power BI, Tableau).

**English:**
```
site:linkedin.com/jobs "Supply Chain Analyst" remote
site:linkedin.com/jobs "Supply Chain Data Analyst" remote
site:linkedin.com/jobs "S&OP Analyst" remote
site:linkedin.com/jobs "Demand Planner" data remote
site:linkedin.com/jobs "Business Intelligence Analyst" supply chain remote
site:weworkremotely.com "supply chain" analyst
site:himalayas.app "supply chain" analyst
site:wellfound.com "supply chain" analyst
site:flexjobs.com/jobs "Supply Chain Analyst" remote
"Logistics Control Tower" analyst remote job
```

**Portuguese:**
```
site:linkedin.com/jobs "Analista de Supply Chain" remoto
site:linkedin.com/jobs "Analista de S&OP" remoto
site:linkedin.com/jobs "Analista de Planejamento" demanda dados remoto
site:linkedin.com/jobs "Analista de BI" logística remoto
site:portal.gupy.io "Supply Chain" analista remoto
site:portal.gupy.io "Torre de Controle" logística
```

### Priority 2: Logistics Tech & Fleet Management (Product Owner / Product Manager)
Technical PO/PM roles in TMS, WMS, logistics cloud, fleet management, or supply chain SaaS.

**English:**
```
site:linkedin.com/jobs "Product Owner" TMS OR WMS remote
site:linkedin.com/jobs "Technical Product Manager" logistics remote
site:linkedin.com/jobs "Product Manager" "fleet management" remote
site:wellfound.com "Product Manager" logistics
site:workatastartup.com "Product" supply chain
site:flexjobs.com/jobs "Product Manager" remote
```

**Portuguese:**
```
site:linkedin.com/jobs "Product Owner" logística remoto
site:linkedin.com/jobs "Product Manager" supply chain remoto
site:portal.gupy.io "Product Owner" logística
```

### Priority 3: Supply Chain Leadership with Analytical Depth
Operational leadership (Manager/Coordinator) where large-scale line experience (50+ teams, 60% of state fuel supply) is the primary requirement and data analytics provides the competitive edge.

**English:**
```
site:linkedin.com/jobs "Supply Chain Manager" remote
site:linkedin.com/jobs "Logistics Operations Manager" remote LATAM
site:linkedin.com/jobs "S&OP Manager" remote
site:wellfound.com "Operations Manager" remote
site:flexjobs.com/jobs "Supply Chain Manager" remote
```

**Portuguese:**
```
site:linkedin.com/jobs "Gerente de Supply Chain" remoto
site:linkedin.com/jobs "Coordenador de Logística" dados remoto
site:portal.gupy.io "Gerente de Logística" remoto
```

### STRICT ANTI-PATTERN: Junior Data Analyst Roles
**NEVER generate queries for or target Junior Data Analyst positions.** The candidate is overqualified with 15+ years of operational leadership and terminal management, creating immediate churn risk and recruiter disqualification.

---

## Candidate Filters & Gate Rules

### Location Filter
- Base: **Bombinhas, Santa Catarina, Brazil** (UTC-3). Target: **fully remote roles paid in USD**.
- **Remote:** Fully remote (global, LATAM, Brazil) = **PASS**.
- **Santa Catarina Hybrid:** Within ~80 km of Bombinhas (Florianópolis, Itajaí, Balneário Camboriú, Navegantes) = **PASS**.
- **Fortaleza / CE:** Hybrid or on-site in Fortaleza = **PASS** (open to relocation).
- **Blumenau, SC:** Hybrid or on-site = **FAIL / HARD STOP** (not viable).
- **SP, BH, Curitiba, etc.:** Hybrid or on-site = **FAIL / HARD STOP** (deal-breaker).
- **International on-site:** Requires visa sponsorship (**FLAG**); without sponsorship = **FAIL**.

### Compensation Filter
- **Floor:** USD 1,600 / month (strict deal-breaker if top of range is below).
- **Target:** USD 4,000 - 7,000 / month.

### Language Filter (Strict Rule)
- Candidate declared level is **Advanced** English (recent testing returned B2; medium-term goal is C1).
- **"Fluent", "Native", or "C1+" English required** → **FLAG** (never a silent PASS). Explicitly display the requirement alongside the candidate's declared level in triage reports.
- **Unspecified or Working/Professional English** → **PASS**.
- **Spanish required** → **FLAG** (elementary level; let candidate judge).

### Hiring Model Reporting
In all scraping and rank summaries, distinguish whether the posting is direct hire or through a staff augmentation agency.
