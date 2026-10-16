import json
import re

with open('job_scraper/deduped_candidates.json', 'r', encoding='utf-8') as f:
    candidates = json.load(f)

print(f"Total candidates to evaluate: {len(candidates)}")

# Gates criteria:
# Anti-patterns (FAIL immediately):
# - Junior, estágio, estagiário, assistente, trainee, aprendiz
# - Non-target domains (adtech, medical doctor, nurse, legal counsel, developer/full-stack engineer unless TMS/WMS PM)
# Location Gates:
# - If remote / 100% remoto: PASS (unless hidden US-only authorization requirement)
# - If hybrid/onsite in SC near Bombinhas (Itajaí, Balneário Camboriú, Navegantes, Brusque, Florianópolis, São José) or Fortaleza/CE: PASS
# - If hybrid/onsite in SP/RJ/MG/etc without remote option: FAIL location

JUNIOR_RE = re.compile(r'\b(junior|júnior|jr|estagio|estágio|estagiario|estagiário|assistente|trainee|aprendiz|auxiliar)\b', re.IGNORECASE)
IRRELEVANT_TITLES = re.compile(r'\b(enfermeir|médic|medico|professor|motorista|vendedor|balconista|atendente|telemarketing|cozinheiro|operador de empilhadeira|pedreiro|fiscal de caixa)\b', re.IGNORECASE)

HIGH_SC_CITIES = ['bombinhas', 'itajai', 'itajaí', 'navegantes', 'balneario camboriu', 'balneário camboriú', 'florianopolis', 'florianópolis', 'sao jose', 'são josé', 'brusque', 'porto belo', 'itapema']
FORTALEZA_CITIES = ['fortaleza', 'maracanau', 'maracanaú', 'caucaia', 'eusebio', 'eusébio']

results = []

for job in candidates:
    title = job.get('title') or job.get('position') or ''
    company = job.get('company') or job.get('company_name') or 'Unknown'
    location = job.get('location') or job.get('city') or ''
    url = job.get('url') or job.get('link') or ''
    portal = job.get('_portal_source', 'portal')
    key = job.get('_canonical_key', '')
    desc = job.get('description') or job.get('description_snippet') or ''
    tags = str(job.get('tags') or '')

    # Check title vetoes
    if JUNIOR_RE.search(title):
        results.append({
            'job': job,
            'status': 'skipped',
            'fit': 'low',
            'veto_reason': 'Junior/Entry level title'
        })
        continue

    if IRRELEVANT_TITLES.search(title):
        results.append({
            'job': job,
            'status': 'skipped',
            'fit': 'low',
            'veto_reason': 'Out-of-domain role'
        })
        continue

    loc_lower = location.lower()
    is_remote = False
    if 'remot' in loc_lower or 'remot' in tags.lower() or job.get('work_mode') == 'remote' or job.get('type') == 'remote':
        is_remote = True

    is_sc_hub = any(c in loc_lower for c in HIGH_SC_CITIES)
    is_fortaleza = any(c in loc_lower for c in FORTALEZA_CITIES)

    # If portal is Solvo or HireLATAM, almost all are USD remote
    if portal in ['hirelatam', 'solvoglobal', 'himalayas', 'dynamitejobs', 'weworkremotely']:
        is_remote = True

    # If linkedin or catho or infojobs and location is SP, RJ, etc. and not remote:
    location_pass = is_remote or is_sc_hub or is_fortaleza
    if not location_pass and ('são paulo' in loc_lower or 'sao paulo' in loc_lower or 'rio de janeiro' in loc_lower or 'curitiba' in loc_lower or 'belo horizonte' in loc_lower or 'rs' in loc_lower or 'pr' in loc_lower or 'sp' in loc_lower or 'rj' in loc_lower):
        results.append({
            'job': job,
            'status': 'skipped',
            'fit': 'low',
            'veto_reason': f'On-site/Hybrid outside target region ({location})'
        })
        continue

    # Evaluate fit
    # High fit: Supply Chain Manager/Coordinator/Specialist/Lead/Sr Analyst, Logistica Gerente/Coordenador/Especialista/Sr, S&OP, Torre de Controle, Demand Planning, Procure-to-Pay / SAP MM
    text_to_eval = f"{title} {desc}".lower()
    fit = 'medium'
    
    high_keywords = ['supply chain', 's&op', 'demanda', 'torre de controle', 'planejamento logístico', 'planejamento logistico', 'logistics operations', 'procurement', 'compras', 'sap mm', 'sap s/4', 'tms', 'wms', 'operations manager', 'gerente de logística', 'gerente de operac', 'coordenador de logística', 'coordenador de operac', 'head of supply chain']
    if any(k in title.lower() for k in high_keywords):
        fit = 'high'
    elif any(k in text_to_eval for k in ['supply chain', 's&op', 'logistica', 'logística', 'operations manager']):
        fit = 'medium'
    else:
        fit = 'low'

    results.append({
        'job': job,
        'status': 'active' if fit in ['high', 'medium'] else 'skipped',
        'fit': fit,
        'veto_reason': None if fit in ['high', 'medium'] else 'Low relevance to target tracks'
    })

high_matches = [r for r in results if r['fit'] == 'high']
med_matches = [r for r in results if r['fit'] == 'medium']
skipped = [r for r in results if r['status'] == 'skipped']

print(f"Evaluated: High={len(high_matches)}, Medium={len(med_matches)}, Skipped={len(skipped)}")

with open('job_scraper/evaluated_sweep.json', 'w', encoding='utf-8') as f:
    json.dump({
        'high': high_matches,
        'medium': med_matches,
        'skipped': skipped
    }, f, indent=2, ensure_ascii=False)
