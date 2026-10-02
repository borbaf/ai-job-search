# ============================================================
# setup-portais.ps1 (v2 - robusto)
# Rodar em POWERSHELL (nao python):
#   cd C:\dev\ai-job-search
#   .\setup-portais.ps1
# ============================================================
$ErrorActionPreference = 'Stop'
$Base   = 'C:\dev\ai-job-search'
$Skills = Join-Path $Base '.agents\skills'

# ---------- 1/4 Pastas -------------------------------------
$slugs = @('gupy','catho','infojobs','dynamitejobs','hirelatam')
foreach ($s in $slugs) {
    New-Item -ItemType Directory -Force -Path (Join-Path $Skills "$s-search\cli\src") | Out-Null
}
Write-Host "[1/4] Pastas criadas: $($slugs.Count)"

# ---------- 2/4 CLAUDE.md ----------------------------------
$claudeMd = @'
# Candidate Profile - Filippe Rezende Borba

## Identity
- Location: Bombinhas, Santa Catarina, Brazil (remote-first; open to relocation to Fortaleza/CE)
- Contact: +55 11 97143 1108 | borbaf@gmail.com
- LinkedIn: linkedin.com/in/borbaf | GitHub: github.com/borbaf
- Languages: PT native | EN advanced | ES elementary
- CV: English (primary) + Portuguese variant
- Status: Independent consultant (GLG Network Member), actively searching

## Positioning
"Supply Chain & Logistics Leader | Data Analytics (Python, SQL, Power BI) | Google Cloud Certified Data Analyst"
"I am not a beginner in data - I am a Supply Chain professional who finally has the right tool."

## Career pivot priority
1. Data / Analytics (top): Data Analyst, Analytics Engineer, Data Engineer, BI
2. Product (high): Product Owner, Product Manager, Data Product Owner
3. Supply Chain / Operations (secondary, data-flavored only)

## Education
- Postgraduate in Data Science & Big Data (in progress) - UNIALPHAVILLE
- Data Science & Analytics coursework (2024-2025) - SENAI SC, Coursera, DSA
- MBA Supply Chain Management (2018-2019) - FGV
- MBA Economics & Management (2014-2015) - FGV
- BSc Electrical/Electronic Engineering (2006-2011) - PUC Goias

## Experience
- Supply Chain Expert (2025-present) - GLG Network (remote)
- Senior Supply Chain Consultant (2023-2025) - Moby Consulting (Bracell, Suzano, Unilever, Vibra, Ipiranga, COMGAS, TotalEnergies)
- Superintendent / Senior Manager (2021-2022) - Vibra Energia, Port of Tubarao (50+ professionals; 60% of ES fuel supply)
- Logistics Coordinator (2017-2019) - Vibra Energia (30% of Brazil's bulk fuel)
- Manager / MRO Operator (2009-2017) - BR Distribuidora (SAP PM & MM)
- Project Engineer (2022-2023) - AIS Ltd, Dublin, Ireland

## Skills
- Data: Python (NumPy, Pandas, Matplotlib, Seaborn, scraping, APIs), SQL (PostgreSQL), NoSQL (MongoDB), Power BI, Tableau, EDA, statistics
- Cloud: GCP, BigQuery (Google Cloud Data Analyst certified, 2026)
- AI/automation: LLM APIs, agentic workflows (Claude Code, Gemini CLI), process automation
- Domain: supply chain analytics, control towers, fuel distribution, liquid bulk terminals, WMS/TMS/ERP (SAP PM&MM), PMO, procurement, Lean/VSM/5S/TPM

## Certifications
- Google Cloud Data Analytics - Professional Certificate (2026)
- Global Champion - Deel & Nomad
- Industrial Instrumentation & Automation - Universidade Petrobras

## Compensation
- Floor: USD 2,000/mo (reject below) | Target: USD 5,000/mo

## Deal-breakers
- Below USD 2,000/mo

## Writing & tooling rules
- When mentioning agentic coding or AI tooling, explicitly reference Claude Code by name.
- CV/letters must be repositioned toward Data & Product / Automation, not pure supply chain.
'@
Set-Content -LiteralPath (Join-Path $Base 'CLAUDE.md') -Value $claudeMd -Encoding utf8
Write-Host "[2/4] OK: CLAUDE.md"

# ---------- 3/4 SKILL.md dos portais (template + loop) -----
$tpl = @'
---
name: {{SLUG}}-search
version: 1.0.0
description: >
  Use this skill whenever the user wants to search for jobs on {{NOME}}
  ({{DESC}}). Invoke for open positions, vacancies, and hiring on {{NOME}}.
  Trigger phrases: {{TRIGGERS}}.
context: fork
enabled: true  # set to false to keep this portal installed but have /scrape skip it
allowed-tools: Bash(bun run .agents/skills/{{SLUG}}-search/cli/src/cli.ts *)
---

# {{NOME}} Search Skill

{{SOBRE}}

> Access note: {{ACESSO}}

## Candidate profile (search strategy)

Supply Chain & Operations Leader with Analytical Layer. Problem solver bridging physical operations and data intelligence.
Sweet Spots: (1) Supply Chain Analytics, S&OP & BI, (2) Logistics Tech & Fleet Management (PO/PM in TMS/WMS/SaaS). Anti-pattern: Junior Data Analyst.
Base: Bombinhas/SC (open to relocation to Fortaleza/CE). Remote-first; USD roles prioritized.

## URL patterns

{{URLS}}

## Commands

### Search job listings

    bun run .agents/skills/{{SLUG}}-search/cli/src/cli.ts search --query "<termo>" [flags]

Key flags:
- --query <text> / -q <text> - keyword search (title, skill, role). Recommended.
- --location <text> / -l <text> - city/state (e.g. Remoto, Bombinhas, Fortaleza).
- --format json|table|plain - default json.

### Fetch full job detail

    bun run .agents/skills/{{SLUG}}-search/cli/src/cli.ts detail <id|url> [--format json|plain]

## Output formats

| Format | Best for |
|--------|----------|
| json | Programmatic use - pass IDs to detail |
| table | Quick human-readable scanning |
| plain | Reading a single job's full detail |

Errors go to stderr as { "error": "...", "code": "..." } with exit code 1.

## Notes

- {{NOTAS}}
'@

$portais = @(
  @{
    slug='gupy'; nome='Gupy'; desc='the dominant Brazilian ATS'
    triggers='gupy, vaga gupy, buscar no gupy, portal gupy'
    sobre='Search live job listings from **Gupy (portal.gupy.io)**, the leading Brazilian ATS used by large employers. Runs with bun; no API key.'
    acesso='Gupy protects automated access (login + anti-bot). If the search fails or is blocked, fall back to pasting the job description into /apply.'
    urls='- Search: `https://portal.gupy.io/job-search/term=<termo>`|- Listing: `https://portal.gupy.io/jobs`|- Job page: `https://<empresa>.gupy.io/jobs/<id>`'
    notas='Data from Gupy public job pages; may require login. Keep volume low.'
  },
  @{
    slug='catho'; nome='Catho'; desc='a major Brazilian job board'
    triggers='catho, vaga catho, buscar no catho'
    sobre='Search live job listings from **Catho (catho.com.br)**, a major Brazilian job board. Runs with bun; no API key.'
    acesso='Catho requires login for full listings and protects automated access. If blocked, fall back to pasting the description into /apply.'
    urls='- Search: `https://www.catho.com.br/vagas`'
    notas='Data from Catho public job pages; may require login. Keep volume low.'
  },
  @{
    slug='infojobs'; nome='Infojobs'; desc='a major Brazilian job board'
    triggers='infojobs, vaga infojobs, buscar no infojobs'
    sobre='Search live job listings from **Infojobs (infojobs.com.br)**, a major Brazilian job board. Runs with bun; no API key.'
    acesso='Infojobs requires login for full listings and protects automated access. If blocked, fall back to pasting the description into /apply.'
    urls='- Search: `https://www.infojobs.com.br`|- Company: `https://www.infojobs.com.br/<empresa>/vagas`|- Mobile: `https://m.infojobs.com.br`'
    notas='Data from Infojobs public job pages; may require login. Keep volume low.'
  },
  @{
    slug='dynamitejobs'; nome='Dynamite Jobs'; desc='an international remote-first job board'
    triggers='dynamite jobs, remote jobs, vaga remota'
    sobre='Search live job listings from **Dynamite Jobs (dynamitejobs.com)**, an international remote-first job board. No login, no API key.'
    acesso='Public search works without login. The Company API (/developers) is for hiring companies - ignore it.'
    urls='- Search: `https://dynamitejobs.com/remote-jobs?text=<termo>&page=<n>`|- By country: `https://dynamitejobs.com/country/remote-jobs-in-<pais>`|- By skill: `https://dynamitejobs.com/skill/remote-<skill>-jobs`'
    notas='Data from Dynamite Jobs public pages; no login required.'
  },
  @{
    slug='hirelatam'; nome='HireLATAM'; desc='a platform connecting LATAM talent to US/global remote roles'
    triggers='hirelatam, vaga hirelatam'
    sobre='Search live job listings from **HireLATAM (hirelatam.com)**, connecting LATAM talent to US/global remote roles. Runs with bun; no API key.'
    acesso='HireLATAM focuses on the hiring company (flat-fee model); /jobs may require login or be institutional only. If blocked, fall back to pasting the description into /apply.'
    urls='- Search: `https://hirelatam.com/jobs`'
    notas='Data from HireLATAM public pages; may require login. Keep volume low.'
  }
)

foreach ($p in $portais) {
    $c = $tpl
    foreach ($k in $p.Keys) {
        $val = $p[$k].Replace('|', "`n")
        $c = $c.Replace('{{' + $k.ToUpper() + '}}', $val)
    }
    Set-Content -LiteralPath (Join-Path $Skills "$($p.slug)-search\SKILL.md") -Value $c -Encoding utf8
    Write-Host "OK: $($p.slug)-search/SKILL.md"
}
Write-Host "[3/4] OK: SKILL.md dos 5 portais"

# ---------- 4/4 Ajuste de localizacao no linkedin ----------
$li = Join-Path $Skills 'linkedin-search\SKILL.md'
if (Test-Path -LiteralPath $li) {
    $t = Get-Content -LiteralPath $li -Raw -Encoding UTF8
    $novo = $t -replace 'Curitiba, Paran.*Brazil', 'Bombinhas, Santa Catarina, Brazil'
    if ($novo -ne $t) {
        Set-Content -LiteralPath $li -Value $novo -Encoding UTF8
        Write-Host "[4/4] OK: linkedin SKILL.md atualizado para Bombinhas/SC"
    } else {
        Write-Host "[4/4] linkedin SKILL.md: nada a alterar"
    }
} else {
    Write-Host "[4/4] linkedin SKILL.md nao encontrado - pulando"
}

Write-Host ""
Write-Host "Concluido. Estrutura em .agents\skills:"
Get-ChildItem $Skills -Directory | Select-Object -ExpandProperty Name