---
framework_version: 1.3.0
---

# Job Evaluation Framework

<!-- SETUP: Skill match areas and career goals are personalized by running /setup -->

## Eligibility Gate — run before scoring

If the candidate is not a citizen or permanent resident of the country they are applying in, run this first. It is a hard filter, not a scoring dimension, and it is separate from work-permit *timing*: timing asks "can they work the required hours yet?", eligibility asks "are they permitted to hold this job at all?". A candidate can pass timing and still be categorically excluded.

**Candidate citizenship status:** Brazilian citizen, located in Brazil. Holds **no US citizenship, Green Card, or US work authorization**.

Read the posting's eligibility / work rights / "who can apply" section **verbatim** and classify:

| Posting wording | Verdict |
|-----------------|---------|
| Names a **citizenship or permanent-residency requirement** ("must be a citizen of X", "permanent resident", "PR required", "must be legally authorized to work in the US without sponsorship", "US work authorization required") | **FAIL — hard stop.** Do not score, do not draft. Quote the exact wording back to the user (e.g., US roles that require domestic authorization). |
| Requires a **security clearance** at any level | **FAIL** in most countries, since clearance is normally gated on citizenship. Verify the specific scheme rather than assuming. |
| **Explicitly names** the candidate's permit class, or says "international applicants welcome", "visa holders considered", "we sponsor", or hires globally via EOR/Contractor (BairesDev, Scrambly, INDI) | **PASS** — verified acceptance. Worth noting as a positive in the application. |
| **Silent** on citizenship or residency | **PROCEED, but mark unverified.** Check the employer's own careers or international-applicant page before drafting. |

**Two rules that are easy to get wrong:**

1. **Silence is not permission.** Large corporate programs frequently gate eligibility on their own website rather than in the job ad. Highest-risk categories: professional-services firms, government and defence, banking, telecommunications, and anything touching critical infrastructure.
2. **A company-wide "we accept international applicants" statement is not role-level permission.** The common pattern is a general welcome followed by a *named list* of the specific programs or service lines it covers. Confirm the **specific posting or stream** appears on that list before drafting.

**Report an eligibility failure to the user with the quoted source** rather than silently dropping the role. They may know something about their own status that the profile does not record.

If the candidate's permit also constrains *hours* or *start date*, record that as a second gate under this section. Do not merge it with the eligibility question above — they fail for different reasons and need different answers.

A role that fails this gate is not scored and not drafted. Everything below applies only to roles that pass it.

## Language Gate — run before scoring

This gate checks a posting's language requirements against what the candidate actually speaks. It is not one of the five Scoring Dimensions below - it runs before them, structured the same way as the Eligibility Gate above: read the posting, classify against profile data, and treat a hard mismatch as FAIL before scoring. Its verdict is tracked downstream: `/rank` records the result as `language_gate` (PASS/FAIL/FLAG) with a supporting `language_note`, persists both into `seen_jobs.json`, and treats a FAIL as a shortlist veto; `/scrape` surfaces the flag in its results table and carries a language-override rule for postings whose ad language differs from the role's working language. `/apply`'s language detection (Step 1, which extracts a posting's required language generically) feeds this same check.

Read the posting's language requirements as stated for **the role itself** — not the language the ad happens to be written in. A posting written in a language you don't work in, for a role that only needs languages you do work in on the job, passes fine; only an explicit job-condition requirement ("fluent X required," "must communicate with the Y team in Z") triggers this check. For each language the posting requires as a job condition, compare it against your Languages table in CLAUDE.md / `01-candidate-profile.md`:

| Posting requirement vs. your Languages table | Verdict |
|---|---|
| Requires a language **not on your table at all** (e.g. "fluent Polish required," "must communicate with the Warsaw team in Russian", and you list no Polish/Russian row) | **FAIL — hard stop.** Do not score, do not draft. Quote the exact requirement line. |
| Requires a language you **do** list, but the posting's stated bar (as written — "fluent," "native," "C1+," "business-level") reads as plausibly **higher** than your declared level | **FLAG, then proceed.** Not a fail. Score and draft normally, but surface the gap explicitly in your report to the user (quote both the posting's requirement and your declared level) so they can judge it themselves. Never silently drop the posting and never silently treat it as a clean pass. |
| Requires a language you list, at or below your declared level (or the posting doesn't specify a level at all — just names the language) | **PASS.** No note needed. |

**CRITICAL RULE FOR ENGLISH:**
Candidate's declared level is **Advanced** (held professional engineering role delivered in English in Ireland; conducts international GLG consultations; recent formal recruitment test scored B2; medium-term target is C1).
- Any job posting requiring **"fluent"**, **"native"**, or **"C1+"** English must be **FLAGGED** (never treated as a silent PASS).
- Explicitly surface the gap in the report (`language_gate: FLAG`, `language_note: "Posting requires C1/Fluent English vs. declared Advanced (recent test: B2, target: C1)"`).
- Postings with unspecified English or conversational/working English pass cleanly.

## Hiring Model Assessment — run for every posting

Classify and report the hiring model for every evaluated role:
1. **Direct Hire (Client):** Hired directly by the company operating the core business.
2. **Staff Augmentation (Staffing / Outstaffing / Agency):** Hired through a third party (e.g., HireLATAM, Solvo Global, Revelo, BairesDev, staffing agencies) to provide talent to an end-client.
   - *Key Rule for Staff Augmentation:* The application and CV will be reviewed by the end-client. Therefore, **keywords, industry domain terminology, and specific tools of the end-client count just as heavily as the raw job description requirements**.
   - *Reporting:* The hiring model must be explicitly stated in the evaluation summary.

## Scoring Dimensions

Evaluate each job posting against these five dimensions:

### 1. Technical Skills Match (0-100)
How well do the required/preferred skills align with the candidate's capabilities?

| Score | Meaning |
|-------|---------|
| 80-100 | Core requirements are primary skills |
| 60-79 | Most requirements match, 1-2 gaps that are learnable |
| 40-59 | Partial match, significant upskilling needed |
| 0-39 | Fundamental mismatch |

**Strong match areas:** Python (NumPy, Pandas, web scraping, APIs), SQL (PostgreSQL, MongoDB), BigQuery, Power BI, Tableau, EDA and statistical analysis, supply chain analytics, logistics control towers, supply and materials planning, S&OP, Lean/VSM/5S/TPM, SAP (PM & MM), WMS/TMS, advanced Excel, procurement and MRO materials management, GIS (GSI, Dekart, Kepler.gl), Google Cloud Platform (certified 2026, limited production hours), Git/GitHub, dashboard and data-model design at scale, forecasting and demand planning, SCADA and industrial automation, PMO and project management.

**Moderate match areas:** C and Assembly (historical/embedded background), Bash scripting, Docker fundamentals.

**Weak match areas / Out of Scope:** Machine learning and MLOps in production, pure backend SQL development / data warehouse engineering (5-7+ years dev), Microsoft Fabric, Azure Synapse / Databricks, data engineering (Airflow, dbt, Spark, streaming), cloud infrastructure and DevOps, software engineering (web/backend development), R, Snowflake, deep statistical modeling and experimentation design.

### 2. Experience Match (0-100)
Does work history align with what they're looking for? Match on the function and nature of the work performed, not the literal job title.

| Score | Meaning |
|-------|---------|
| 80-100 | Direct experience in the same domain and role type |
| 60-79 | Related experience, transferable skills clear |
| 40-59 | Adjacent experience, would need to make the case |
| 0-39 | Unrelated experience |

**Strong:** Supply chain and logistics operations (13 years at Vibra Energia / BR Distribuidora, rising from MRO Operator to Superintendent), fuel and liquid-bulk terminal management, distribution and freight, supply chain consulting (Moby, 2023-2025), large-team leadership (50+ direct organization), industrial maintenance and MRO, end-to-end international delivery (AIS Ireland).

**Moderate:** Supply chain analytics and BI delivery (~2 years applied, inside consulting engagements), business/data analysis for enterprise clients, control-tower implementation, industrial automation engineering, expert-network advisory (GLG).

**Entry-level / Mismatch:** Generic Data Analyst / Data Scientist / BI Developer roles with no domain context, backend data engineering, product analytics in non-logistics spaces, any role requiring a portfolio of shipped ML models.

**Positioning Framing (use on every analytics application):** The honest claim is a **Supply Chain & Operations Leader with an Analytical Layer** and a **decisive problem solver (resolutor)** who has delivered applied analytics — not a junior analyst and not a career beginner. Roles that reward domain knowledge *plus* SQL/Python/BI (supply chain analyst, logistics data analyst, WMS/TMS business analyst, analytics consultant, demand planner) score materially higher on this dimension than generic data-analyst postings, and should be prioritized in `/rank`.

### 3. Behavioral/Culture Fit (0-100)
Does the role and company culture match the behavioral profile?

| Score | Meaning |
|-------|---------|
| 80-100 | Culture strongly matches behavioral preferences |
| 60-79 | Mixed signals but mostly compatible |
| 40-59 | Some friction areas |
| 0-39 | Significant culture mismatch |

**Positive signals:** Ownership, cross-functional bridge, high autonomy, outcome orientation, continuous learning, problem solving.
**Red flags:** Department disorganization, micromanagement, presence-based evaluation, lack of decision ownership, maintenance-only scope without growth.

### 4. Location & Logistics (Pass/Fail + Notes)

Base: Bombinhas, Santa Catarina, Brazil. Target: **fully remote roles paid in USD**. Relocation is viable for Fortaleza/CE or abroad with sponsorship.

- **Fully remote (global, LATAM, or Brazil):** **PASS** — the primary target (prioritize USD-denominated roles).
- **Hybrid or on-site in Santa Catarina within ~80 km of Bombinhas** (Florianópolis, Itajaí, Balneário Camboriú, Navegantes, Tijucas): **PASS**.
- **Hybrid or on-site in Fortaleza, Ceará:** **PASS** — candidate is explicitly open to relocating to Fortaleza.
- **Hybrid or on-site in Blumenau, SC:** **FAIL / HARD STOP** — explicitly not viable for daily/regular presence.
- **Hybrid or on-site in São Paulo (SP), Belo Horizonte (BH), Curitiba, or other distant Brazilian cities:** **FAIL / HARD STOP** — deal-breaker; do not score or draft.
- **On-site abroad with visa sponsorship:** **FLAG** — viable and of genuine interest; check sponsorship explicitly and run the Eligibility Gate above.
- **On-site abroad *without* sponsorship or work rights:** **FAIL** (see Eligibility Gate).
- **Timezone:** no hard constraint, but flag anything requiring sustained work outside roughly UTC-3 ± 6 hours.

### 5. Career Alignment & Motivation (0-100)
Does this role advance career goals and contain tasks that energize?

| Score | Meaning |
|-------|---------|
| 80-100 | Strongly aligned with career direction, clear growth path |
| 60-79 | Good role but only partially aligned with long-term goals |
| 40-59 | Decent job but doesn't build toward career goals |
| 0-39 | Dead end or backwards step |

**Target Sweet Spots (Score 85-100):**
1. **Supply Chain Analytics, S&OP & BI:** S&OP Analyst, Demand Planning (Data & Automation), Supply Chain Data Analyst, Business Intelligence Analyst. Capitalizes on 15+ years of operational leadership and executive presence, powered by Python, SQL, Tableau, Power BI, GCP, and GIS.
2. **Logistics Tech / Fleet Management Product:** Technical Product Owner / Product Manager in Fleet Management, TMS, WMS, Logistics Cloud, or Supply Chain SaaS (e.g., Omron model).

**Anti-Patterns / Deprioritized (Score 0-45 / Veto):**
- **Junior Data Analyst Roles (STRICT VETO):** Excluded. The candidate is seen as overqualified with high churn risk. Never steer the framework toward junior data roles.
- **Pure Data Engineering & Database Development:** Roles demanding 5-7+ years of pure SQL programming, data warehouse engineering, or data pipeline plumbing with no business/domain connection (e.g., Wesco).
- **Microsoft Fabric Core:** Roles where Microsoft Fabric, Azure Synapse, or Azure Databricks are mandatory prerequisites.
- **Generic Product Owner:** Generalist PO in apparel, e-commerce, banking, or non-supply-chain apps.
- **Ambiguous Work Models:** Roles based in SP, BH, etc., with consulting or hybrid risk without guaranteed 100% remote contract.
- **PhD / Academic Requirements:** Roles requiring PhD or academic publications.

**Motivation filter:**
- **Tasks that energize:** building analyses and control towers that change operational decisions; owning a problem end-to-end; working directly with domain stakeholders; control tower, S&OP, and demand planning challenges; high operational scale and consequence.
- **Tasks that drain:** execution-only mandates with no decision authority; maintenance-only scope with no development path; pure theoretical research; environments where decisions stall for lack of an owner.

**Compensation filter:**
- **Floor:** USD 1,600 / month (hard stop if posted range top is below).
- **Target:** USD 4,000 - 7,000 / month.

### 6. Salary Benchmark (Optional)
If configured (`salary_data.json` exists), run:
```bash
python salary_lookup.py "<Company Name>" --json
```

## Output Format

Present the evaluation as:

```
## Job Fit Evaluation: [Role] at [Company]

| Dimension | Score / Status | Notes |
|-----------|----------------|-------|
| Hiring Model | Direct Hire / Staff Augmentation | [e.g. Direct / Agency (Client: X)] |
| Language Gate | PASS / FLAG / FAIL | [e.g. FLAG: Requires C1 vs. declared B2] |
| Technical Skills | XX/100 | [brief note] |
| Experience Match | XX/100 | [brief note] |
| Behavioral Fit | XX/100 | [brief note] |
| Location | PASS/FAIL | [brief note] |
| Career Alignment | XX/100 | [brief note] |

**Overall Score: XX/100** (weighted average of scored dimensions)

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

## Weighting
- Technical Skills: 30%
- Experience Match: 25%
- Behavioral Fit: 15%
- Career Alignment: 30%
(Location is pass/fail, not weighted)

## Thresholds
- **Strong Fit** (75+): Definitely apply, tailor everything
- **Good Fit** (60-74): Apply, address gaps in cover letter
- **Moderate Fit** (45-59): Consider carefully, discuss with user
- **Weak Fit** (30-44): Probably skip unless strategic reasons
- **Poor Fit** (<30): Skip

## Pre-Application: Call the Employer (Best Practice)
Only call if there are substantive questions regarding role challenges, day-to-day balance, or critical success metrics.
