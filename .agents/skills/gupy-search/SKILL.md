---
name: gupy-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on Gupy
  (the dominant Brazilian ATS). Invoke for open positions, vacancies, and hiring on Gupy.
  Trigger phrases: gupy, vaga gupy, buscar no gupy, portal gupy.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/gupy-search/cli/src/cli.ts *)
---

# Gupy Search Skill

Search live job listings from **Gupy (portal.gupy.io)**, the leading Brazilian ATS used by large employers. Runs with bun; no API key.

> Access note: Gupy protects automated access (login + anti-bot). If the search fails or is blocked, fall back to pasting the job description into /apply.

## Candidate profile (search strategy)

Engineer/Consultant in Logistics Transformation, pivoting to Data & Product.
Priority: (1) Data/Analytics, (2) Product, (3) Supply Chain/Operations (data-flavored).
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

- Search: `https://portal.gupy.io/job-search/term=<termo>`
- Listing: `https://portal.gupy.io/jobs`
- Job page: `https://<empresa>.gupy.io/jobs/<id>`

## Commands

### Search job listings

    bun run .agents/skills/gupy-search/cli/src/cli.ts search --query "<termo>" [flags]

Key flags:
- --query <text> / -q <text> - keyword search (title, skill, role). Recommended.
- --location <text> / -l <text> - city/state (e.g. Remoto, Bombinhas, Fortaleza).
- --format json|table|plain - default json.

### Fetch full job detail

    bun run .agents/skills/gupy-search/cli/src/cli.ts detail <id|url> [--format json|plain]

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail |
| table | Quick human-readable scanning |
| plain | Reading a single job's full detail |

Errors go to stderr as { "error": "...", "code": "..." } with exit code 1.

## Notes

- Data from Gupy public job pages; may require login. Keep volume low.


## Gupy Application Constraints & Workflow (/apply Integration)

**CRITICAL GUPY ATS SPECIFICS:**
1. **No Per-Application PDF CV Upload:** Gupy relies exclusively on the candidate's unified master profile already registered on the platform. You cannot attach a new role-specific PDF CV during a standard Gupy application.
2. **No PDF Cover Letter Attachment:** Gupy has no field or option to upload a cover letter file.
3. **1500-Character Application Pitch:** Gupy features an open-ended mandatory/key response field:
   *"The company wants to know more about you! Tell us about yourself and your professional journey, explaining how you can help the company with the challenge described in the job posting."*
   - This field has a **strict 1500-character limit** (including spaces).
   - The `/apply` workflow for Gupy jobs MUST prioritize drafting this 1500-character tailored pitch instead of generating an unattachable cover letter PDF.
   - Text must be verified with `len(text) <= 1500` characters before outputting to the user.
4. **Top 3 Skills Selection:** Gupy prompts the applicant to pick their **top 3 matching skills** for the vacancy. The `/apply` output must explicitly recommend the exact 3 skills to select.
5. **Screening Questions Guidance:** Pre-populate recommended values for typical mandatory questions (e.g., current compensation, salary expectation).
