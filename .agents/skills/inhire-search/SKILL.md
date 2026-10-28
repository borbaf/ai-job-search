---
name: inhire-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on InHire (inhire.app),
  a prominent Brazilian Applicant Tracking System (ATS) hosting careers pages for top tech,
  logistics, and high-growth companies (including nstech, Mottu, Wilson Sons, Deloitte, Autoglass, etc.).
  Invoke for open positions, vacancies, and hiring on InHire.
  Trigger phrases: inhire, vaga inhire, vagas inhire, buscar no inhire, portal inhire.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/inhire-search/cli/src/cli.ts *)
---

# InHire Search Skill

Search live job listings across 130+ active company career portals hosted on **InHire (`inhire.app`)**, including major logistics tech players like **nstech** (Frete Rápido, OpenTech, Buonny, BRK, GBM), **Mottu**, **Wilson Sons Offshore**, **Autoglass**, **Deloitte**, **Share People Hub**, etc.

Runs with Bun; queries InHire's public career APIs (`api.inhire.app/job-posts/public/pages`) with high throughput across active enterprise tenants, requiring zero browser simulation.

## Candidate Profile & Search Strategy

Target: Supply Chain & Operations Leader with Analytical Layer (S&OP, Logistics Control Tower, Physical Operations, Logistics Tech / PO / PM).
Language scope: Portuguese & English.

## Commands

### Search job listings

```bash
bun run .agents/skills/inhire-search/cli/src/cli.ts search --query "<keyword>" [flags]
```

Key flags:
- `--query <text>` / `-q <text>` - search keywords across title, company, and location (e.g. `supply chain`, `logistica`, `operacoes`, `planejamento`).
- `--tenant <name>` / `-t <name>` - restrict search to a specific company tenant (e.g. `-t nstech`, `-t mottu`, `-t deloitte`, `-t wilsonsonsoffshore`).
- `--remote` - filter only remote positions.
- `--limit <n>` / `-n <n>` - maximum number of results to display (default: 30).
- `--format json|table|plain` - output format (default: `json`).

### Fetch full job detail

```bash
bun run .agents/skills/inhire-search/cli/src/cli.ts detail <tenant:jobId|url> [--format json|plain]
```

Examples:
```bash
bun run .agents/skills/inhire-search/cli/src/cli.ts detail "nstech:335f2e58-86af-4d5e-9f4d-ec6a62aca5fc"
bun run .agents/skills/inhire-search/cli/src/cli.ts detail "https://nstech.inhire.app/vagas/335f2e58-86af-4d5e-9f4d-ec6a62aca5fc"
```
