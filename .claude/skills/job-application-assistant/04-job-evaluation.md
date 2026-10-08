---
framework_version: 1.3.0
---

# Job Evaluation Framework

<!-- SETUP: Skill match areas and career goals are personalized by running /setup -->

## Gate 0: Employment & Compensation Model Gate — run first before scoring

This gate filters out non-compensating, high-risk equity, or unviable employment structures. Filippe requires guaranteed, predictable, regular monetary compensation (fixed salary, hourly contractor rate, fixed monthly retainer, CLT, or PJ).

Read the posting's compensation and engagement model **verbatim** and classify:

| Posting wording / Structure | Verdict |
|---|---|
| **Equity-only**, **Co-founder**, **Founding Team** (unfunded or revenue conditioned on future company traction/funding, e.g. Gabb) | **FAIL — hard stop.** Do not score, do not draft. Quote the wording (e.g., "Equity-only co-founder role", "Salary contingent on Series A"). |
| **Venture-building / Incubator / Fellowship / Stipend-only** (e.g., EWOR, Entrepreneur First, unpaid fellowships) | **FAIL — hard stop.** Do not score, do not draft. |
| **Commission-only, unpaid internship, or pure revenue-share** | **FAIL — hard stop.** |
| **Guaranteed regular compensation** (regular salary, fixed contractor rate, CLT, PJ, EOR via Deel/Remote) | **PASS.** Proceed to Gate 1. |
| **Silent on compensation model** but standard corporate hiring | **PROCEED, but verify during evaluation.** |

---

## Gate 1: Geographic Eligibility & In-Person Presence Gate — run before scoring

**CRITICAL DIRECTIVE: NEVER TRUST PLATFORM TAGS.**
Job board tags such as "Global Remote", "Anywhere in the World", "100% Remoto", or "Remote" (specifically on Wellfound, We Work Remotely, Himalayas, LinkedIn, ZipRecruiter) are frequently aspirational, company-wide defaults, or marketing labels. **The official Job Description (JD) body text is the ONLY valid source of truth.**

Candidate status: Brazilian citizen, located in Bombinhas, Santa Catarina, Brazil. Holds **no US citizenship, Green Card, or US work authorization**.

Read the full posting text / JD body **verbatim** and execute two checks:

### Check A: In-Person / On-site / Hybrid Presence in JD Text
Search the JD body text for physical presence indicators: `in-person`, `on-site`, `onsite`, `based in <city/country>`, `hybrid`, `X days a week in office`, `local candidates only`, `relocation required`.

- If the JD body requires regular physical presence outside Santa Catarina (within ~80km of Bombinhas) or Fortaleza/CE → **FAIL — hard stop.** (Eliminates roles like Bobyard in SF, Posh in NYC, Alpaca in NYC, C3 in Redwood City, Benchmark in South Bend, tennr in NYC, Loggi in SP, Renner in RS).
- Hybrid in SC within 80km (Florianópolis, Itajaí, BC, Navegantes) or Fortaleza/CE → **PASS**.
- Explicitly 100% remote without office attendance mandates → **PASS**.

### Check B: Country / Citizenship / Domestic Authorization in JD Text
Search the JD body text for geographic boundaries: `US only`, `Must be based in the US`, `Only candidates in the United States / Canada / UK / Europe`, `Authorized to work in the US without sponsorship`, `Security clearance required`.

- If the JD limits hiring to domestic US/foreign residents or forbids international contractors/sponsorship → **FAIL — hard stop.** (Eliminates roles like Squarespace, Chime, NetVendor, Smartsheet, Deep DSG in Ireland).
- If the JD explicitly supports hiring in Brazil, LATAM, or Worldwide via Contractor/EOR (e.g., Deel, Remote, BairesDev), or the employer is a Brazilian company (e.g., Remotar, Gupy) → **PASS**.
- If silent on domestic restrictions but the company is global remote → **PROCEED, but mark unverified**.

**Report any failure under Gate 0 or Gate 1 with the quoted text** rather than silently dropping or scoring the role. A role that fails either gate is not scored and not drafted.

---

## Gate 2: Language Gate — run before scoring

This gate checks a posting's language requirements against candidate capability.

| Posting requirement vs. Candidate Languages | Verdict |
|---|---|
| Requires a language not listed in profile (e.g. Polish, Russian, German) | **FAIL — hard stop.** |
| Requires working-level Spanish (candidate has Elementary only) | **FAIL — hard stop.** |
| Requires **"Fluent"**, **"Native"**, or **"C1+"** English | **FLAG, then proceed.** (Candidate has Advanced, tested B2, target C1; flag explicitly in report). |
| Unspecified English or Professional/Working English | **PASS.** |

---

## Currency & Strategic Track Classification — classify every posting

Every evaluated job must be explicitly tagged with its **Strategic Track** and **Currency Track**:

### 1. Strategic Track
- **Track 1: Supply Chain & Physical Operations Leadership / S&OP** (Physical domain: bulk liquids, fuel terminals, multi-modal transport, manufacturing, procurement, S&OP, demand planning). Highest conversion and proven viability (Remotar, Gupy, HireLATAM, Solvo).
- **Track 2: Logistics Tech & Data Products** (TMS, WMS, logistics telemetry, fleet management, and supply chain SaaS). Selective layer; requires rigorous geographic & compensation verification.

### 2. Currency Track & Compensation Floor
- **Track USD (International / Remote Global / LATAM):**
  - Floor: **USD 1,600 / month** (deal-breaker if posted top of range is below).
  - Target: **USD 4,000 - 7,000 / month**.
- **Track BRL (National / Remote Brazil / Hybrid SC or Fortaleza):**
  - Floor: **R$ 10,000 / month CLT** or **R$ 14,000 / month PJ** (deal-breaker if top of range is below).
  - Target: **R$ 15,000 - 25,000+ / month**.

---

## Hiring Model Assessment — run for every posting

1. **Direct Hire (Client):** Hired directly by the operating business.
2. **Staff Augmentation (Staffing / Outstaffing / Agency):** Hired through a third party (HireLATAM, Solvo Global, Revelo, BairesDev, etc.). End-client domain keywords and tooling count just as heavily as raw agency requirements.

---

## Scoring Dimensions

Evaluate each job posting against these four dimensions:

### 1. Technical Skills Match (0-100)
How well do the required/preferred skills align with the candidate's capabilities?

| Score | Meaning |
|-------|---------|
| 80-100 | Core requirements are primary skills (Python, SQL, BigQuery, Power BI, Tableau, GIS, S&OP, VSM/Lean) |
| 60-79 | Most requirements match, 1-2 learnable gaps |
| 40-59 | Partial match, significant upskilling needed |
| 0-39 | Fundamental mismatch |

**Strong match areas:** Python (Pandas, NumPy, scraping, APIs), SQL (PostgreSQL, BigQuery), Power BI, Tableau, GIS (Dekart, Kepler.gl, GSI), S&OP / Demand Planning, Lean/VSM/5S, SAP (PM & MM), WMS/TMS, logistics telemetry, Google Cloud Platform (certified 2026).
**Weak / Out of Scope:** Pure backend SQL development / DW plumbing (5-7+ years dev), Microsoft Fabric, Azure Synapse / Databricks, machine learning engineering in production, data engineering pipelines (Airflow, dbt, Spark streaming).

### 2. Experience Match & Physical Domain Weight (0-100)
Does work history align with what they're looking for? **HEAVILY WEIGHT PHYSICAL SUPPLY CHAIN & OPERATIONS DOMAIN.**

| Score | Meaning |
|-------|---------|
| 85-100 | **High Domain Match:** Direct experience in physical supply chain, logistics operations, terminal management, distribution, multi-modal transport, manufacturing, procurement, S&OP, or Logistics Tech (TMS/WMS/Fleet Tech). |
| 60-84 | Related operational experience, clear transferable domain skills. |
| 30-59 | **Domain Penalty:** Generic SaaS, ad-tech, retail apparel, consumer fintech, marketing tech (e.g., Koast, Bobyard, C3, Vercel). Filippe's competitive moat is physical operations + data; generic digital SaaS receives severe domain downgrades. |
| 0-29 | Unrelated experience or entry-level mismatch.

**Positioning Framing:** The honest claim is a **Supply Chain & Operations Leader with an Analytical Layer** and a **decisive problem solver (resolutor)** who has delivered applied analytics — not a generic or junior analyst, and not a digital ad-tech PO.

### 3. Behavioral/Culture Fit (0-100)
Does the role match the behavioral profile?
- **Positive signals (80-100):** Ownership, end-to-end accountability, cross-functional bridge, high autonomy, outcome orientation, continuous learning.
- **Red flags (0-40):** Micromanagement, presence-based evaluation, slow consensus cycles, maintenance-only scope without optimization.

### 4. Career Alignment & Strategic Track Fit (0-100)
Does this role advance career goals and energize?
- **Track 1 & Track 2 Sweet Spots (85-100):** S&OP Analyst/Manager, Supply Chain Analytics Specialist, Demand Planning Lead, Logistics Operations Manager, Technical PO/PM in TMS/WMS/Fleet Tech.
- **USD / High BRL Sweet Spot:** Roles in the USD $4k-$7k range or BRL R$ 15k-25k+ range score 90-100 on alignment.
- **Anti-patterns / Deprioritized (0-40):** Generic PO in fintech/apparel, Junior Data Analyst, pure DB development, ambiguous hybrid models.

---

## Weighting
- Technical Skills: 25%
- Experience Match (Domain Authority & Physical SC Weight): 30%
- Behavioral Fit: 15%
- Career Alignment & Strategic Track: 30%
(Gates 0, 1, 2 are hard pass/fail filters run before scoring)

## Thresholds
- **Strong Fit** (75+): Top priority for application.
- **Good Fit** (60-74): Solid fit; address gaps in cover letter.
- **Moderate Fit** (45-59): Review carefully; proceed only if strategic.
- **Weak Fit** (30-44): Deprioritized / skip.
- **Poor Fit** (<30): Skip.

## Output Format

Present the evaluation as:

```
## Job Fit Evaluation: [Role] at [Company]

| Dimension | Score / Status | Notes |
|-----------|----------------|-------|
| Strategic Track | Track 1 (Physical SC) / Track 2 (Logistics Tech) | [e.g. Track 1: S&OP & Operations Leadership] |
| Currency Track | USD Track / BRL Track | [e.g. USD Track: Target $4k-$7k] |
| Employment Model | PASS / FAIL | [e.g. PASS: Guaranteed monthly contractor rate] |
| Geographic Reality | PASS / FAIL / FLAG | [e.g. PASS: Verified 100% remote for LATAM in JD text] |
| Language Gate | PASS / FLAG / FAIL | [e.g. FLAG: Requires C1 vs. declared B2] |
| Hiring Model | Direct Hire / Staff Augmentation | [e.g. Direct / Agency (Client: X)] |
| Technical Skills (25%) | XX/100 | [brief note] |
| Experience & Domain (30%)| XX/100 | [note: physical domain vs digital SaaS] |
| Behavioral Fit (15%) | XX/100 | [brief note] |
| Career Alignment (30%) | XX/100 | [brief note] |

**Overall Score: XX/100** (weighted average: Technical 25%, Experience 30%, Behavioral 15%, Career Alignment 30%)

### Verdict: [Strong Fit / Good Fit / Moderate Fit / Weak Fit / Poor Fit]

### Key Strengths for This Role
- [bullet points]

### Gaps to Address
- [bullet points]

### Recommendation
[1-2 sentences: apply/skip/apply with caveats]

### Company Research Checklist
- [ ] Checked company website (mission, values, recent news)
- [ ] Checked review sites (Glassdoor, Jobindex, etc.)
- [ ] Checked LinkedIn for team size, recent hires, connections
- [ ] Checked media for restructuring, growth, or workplace issues
- [ ] Identified network contacts who may know the team/manager
```

## Company Research Cache

The Company Research Checklist above is executed independently by `/apply` Step 3's reviewer agent and by `/interview` Step 2.
**File:** `company_research/<normalized-company-name>.json`, one file per company (lowercase, trim, spaces to hyphens).
**TTL:** 30 days from `fetched_date`.

## Pre-Application: Call the Employer (Best Practice)
Only call if there are substantive questions regarding role challenges, day-to-day balance, or critical success metrics.
