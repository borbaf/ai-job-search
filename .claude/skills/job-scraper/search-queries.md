# Search Queries & Channel Strategy for Job Scraper

<!-- Calibrated per empirical triage analysis and strategic goals for Filippe Borba. -->

## Channel & Portal Strategy (Calibrated by Real Conversion)

Verified scraping results showed that platform tags like "Global Remote" or "100% Remoto" have high divergence (up to 100% false positives on Wellfound and 80%+ on We Work Remotely due to hidden US-only domestic authorization or in-person requirements in the JD body). The portal hierarchy is now calibrated strictly by verified viability and strategic fit:

### Tier 1: High Conversion & Strategic Realism (Top Priority)
High-conversion channels connecting LATAM talent with realistic hiring pipelines:
- **Remotar** (`remotar.com.br` / `remotar-search` CLI) — **100% verified viability in live audit.** Premier Brazilian board for remote roles. Primary source for Track 1 BRL roles (R$ 10k-25k+/mo) in logistics, supply chain, and operations.
- **HireLATAM** (`hirelatam.com` / `hirelatam-search` CLI) — Connects top-tier LATAM talent to US companies paying in USD ($1,600 - $7,000/mo) for remote operations, analytics, and project coordination.
- **Solvo Global** (`solvoglobal.com` / `solvoglobal-search` CLI) — Nearshore talent platform with structured remote hiring for US/global operations and analytics.
- **Get on Board** (`getonbrd.com` / `getonbrd-search` CLI) — Tech and operations roles in high-growth companies across LATAM and global remote with transparent remote policies.

### Tier 2: Global Remote Job Boards (Mandatory JD-Text Gating)
High-volume global boards where postings **must be strictly gated against the JD body text** (never trusting platform tags):
- **Dynamite Jobs** (`dynamitejobs.com` / `dynamitejobs-search` CLI) — Remote-first job board. Must verify worldwide eligibility.
- **Himalayas** (`himalayas.app` / `himalayas-search` CLI) — Global remote tech and operations database. Must verify salary (filter out venture-building/co-founder equity-only like EWOR) and country eligibility.
- **Remotive** (`remotive.com` / `remotive-search` CLI) — International remote board for operations, product, and data.
- **We Work Remotely** (`weworkremotely.com` / `weworkremotely-search` CLI) — High volume, but heavily infested with US-domestic-only roles masquerading as remote. Hard gate on JD body text required.
- **Wellfound** (`wellfound.com`) — Startup ecosystem. Highest divergence: platform tags "Global Remote" on in-person NYC/SF or unfunded co-founder roles. Hard gate on JD body text required.

### Tier 3: Brazilian National Platforms & Curated Communities
- **Gupy** (`portal.gupy.io` / `gupy-search` CLI) — Dominant Brazilian ATS. High volume for domestic S&OP, logistics management, and supply chain control tower roles.
- **Job na Gringa** (`jobnagringa.com.br` / `jobnagringa-search` CLI) — Curated community for Brazilian talent landing remote USD/EUR contracts.
- **Catho / Infojobs** (`catho.com.br`, `infojobs.com.br`) — Secondary Brazilian job boards for industrial and logistical management.

### Deprioritized Channels (Low Yield for Candidate Profile)
- **Revelo** (`revelo.com`) — Tested 0% viability: overwhelmingly tailored for software engineering/devs, with minimal signal for supply chain or operations leadership.

### Disabled / Out of Scope
- **Danish Portals** (`jobindex`, `jobnet`, `jobdanmark`, `jobbank`) — Disabled. Zero relevance for Brazil-based candidate without EU right to work or Danish fluency.

---

## Installed Portal CLIs & WebSearch Integration

`/scrape` automatically discovers and runs installed portal skills under `.agents/skills/*/SKILL.md`:
- **Active Operational CLIs:** `remotar-search`, `hirelatam-search`, `solvoglobal-search`, `getonbrd-search`, `himalayas-search`, `remotive-search`, `dynamitejobs-search`, `weworkremotely-search`, `jobnagringa-search`, `gupy-search`, `linkedin-search`, `freehire-search`, `ziprecruiter-search`, `catho-search`, `infojobs-search`.

**Language scope:** Queries are generated in **English and Portuguese** (professional languages). Spanish is excluded from query generation.

---

## Query Strategy by Strategic Track

Every query must incorporate negative keywords to eliminate noise:
- **Global Negatives (EN):** `-junior -intern -internship -trainee -"co-founder" -unpaid -"equity only"`
- **Global Negatives (PT):** `-junior -júnior -jr -estagio -estágio -estagiário -trainee -aprendiz -blumenau`

### Track 1: Supply Chain & Physical Operations (Core Strengths)
Capitalizes on 15+ years of operational line leadership (50+ reports, terminal operations, fuel distribution, S&OP, control tower, procurement).

**English (USD Remote):**
```
site:linkedin.com/jobs ("Supply Chain Manager" OR "Logistics Operations Manager" OR "S&OP Manager") remote LATAM -junior -intern
site:linkedin.com/jobs ("Supply Chain Analyst" OR "S&OP Analyst" OR "Demand Planner") remote -junior -intern
site:hirelatam.com ("Supply Chain" OR "Logistics" OR "Operations")
site:weworkremotely.com ("supply chain" OR "logistics" OR "operations manager") -junior
site:himalayas.app ("supply chain" OR "logistics" OR "inventory planner") -junior
"Logistics Control Tower" analyst remote job -junior
```

**Portuguese (BRL Remote / SC Hybrid / Fortaleza):**
```
site:remotar.com.br "supply chain" OR "logistica" OR "planejamento" -junior
site:portal.gupy.io ("Gerente de Logística" OR "Gerente de Supply Chain" OR "Coordenador de Logística") remoto -junior -estagio
site:portal.gupy.io ("Analista de Supply Chain" OR "Analista de S&OP" OR "Torre de Controle") remoto -junior -estagio
site:linkedin.com/jobs ("Gerente de Operações" OR "Coordenador de Supply Chain") (remoto OR "Santa Catarina" OR Fortaleza) -junior -blumenau
site:linkedin.com/jobs ("Analista de S&OP" OR "Analista de Planejamento de Demanda") remoto -junior -estagio
```

### Track 2: Logistics Tech & Data Products (Product Owner / PM / Telemetry)
Technical PO/PM roles in TMS, WMS, fleet telematics, routing algorithms, or supply chain SaaS. Must have real operational anchor (not generic SaaS/ad-tech/retail apparel).

**English (USD Remote):**
```
site:linkedin.com/jobs ("Product Owner" OR "Product Manager") (TMS OR WMS OR "fleet management" OR "supply chain") remote -junior
site:himalayas.app "Product Manager" (logistics OR supply chain OR freight) -junior
site:weworkremotely.com ("Product Manager" OR "Product Owner") logistics remote -junior
```

**Portuguese (BRL Remote):**
```
site:linkedin.com/jobs ("Product Owner" OR "Product Manager") (logística OR supply chain OR TMS OR WMS) remoto -junior
site:portal.gupy.io ("Product Owner" OR "Gerente de Produto") (logística OR supply chain) remoto -junior
```

---

## Anti-Patterns & Query Sanity Rules

1. **NEVER use bare "Analista de Dados" or "Data Analyst":**
   - Disastrous false positive generator. Yields entry-level BI roles with 22-year-old cohorts, ignoring 15+ years of leadership.
   - Always anchor data roles to domain: `"Supply Chain Data Analyst"`, `"Analista de Dados Logística"`, `"S&OP Data Analyst"`.
2. **NEVER target Junior / Trainee / Intern roles:**
   - Explicit churn risk and immediate recruiter rejection.
3. **NEVER target generic Ad-tech / Marketing / Consumer SaaS:**
   - Filippe's competitive edge is heavy physical operations, bulk fuels, terminals, and asset-intensive supply chains. Roles in pure web advertising, fashion e-commerce, or crypto have low domain fit.

---

## Candidate Filters & Hard Gates

### Gate 0: Employment & Compensation Model Gate (Hard Gate)
- **Guaranteed Cash Income Required:** Must offer predictable salary (CLT/PJ or USD contractor rate).
- **Hard Disqualification (FAIL):**
  - Equity-only roles (0 base salary, options/shares only).
  - Unfunded co-founder / venture-building tracks (e.g. EWOR, Gabb, accelerator cohorts without fixed salary).
  - Commission-only or unpaid roles.

### Gate 1: Geographic Eligibility & Presence Gate (Hard Gate)
- **Base:** Bombinhas, SC, Brazil (UTC-3).
- **Mandatory JD Body Text Check:** Do NOT trust platform tags ("Global Remote", "Anywhere in the world", "100% Remoto"). Check text for:
  - `in-person`, `onsite`, `based in [City]`, `hybrid` outside SC/Fortaleza → **FAIL**.
  - Domestic US work authorization required ("US Citizens / Green Card holders only", "Must reside in the US/UK/Ireland") → **FAIL**.
- **Approved Locations:**
  - Fully remote (Worldwide, LATAM, Brazil) = **PASS**.
  - SC Hybrid (within ~80 km: Florianópolis, Itajaí, Balneário Camboriú, Navegantes) = **PASS**.
  - Fortaleza / CE (Hybrid or On-site) = **PASS** (open to relocation).
  - Blumenau, SC (Hybrid or On-site) = **FAIL** (commute not viable).
  - SP, BH, Curitiba, etc. (Hybrid or On-site) = **FAIL** (requires relocation).

### Gate 2: Currency & Compensation Floors
- **USD Track:** Floor: **USD 1,600 / month** (strict veto if below); Target: **USD 4,000 - 7,000 / month**.
- **BRL Track:** Floor: **R$ 10,000 / month CLT** or **R$ 14,000 / month PJ**; Target: **R$ 15,000 - 25,000+ / month**.

### Gate 3: Language Gate
- Candidate level: **Advanced English** (tested B2; working toward C1). Native Portuguese.
- "Native" or "C1+ required" → **FLAG** (visible ⚠ warning, candidate decides).
- "Professional / Working English" → **PASS**.
- "Spanish required" → **FLAG** (elementary level).
