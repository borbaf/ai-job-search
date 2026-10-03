import json

d = json.load(open('job_scraper/seen_jobs.json', encoding='utf-8'))
seen = d.get('seen', {})
new_jobs = [(k, v) for k, v in seen.items() if v.get('status') == 'new']

terms = ['s&op', 'sop', 'control tower', 'torre de controle', 'demand', 'demanda', 
         'supply chain', 'suprimentos', 'logistica', 'logistics', 'fleet', 'frota', 'tms', 'wms', 'planning']

matches = []
for k, v in new_jobs:
    t = (v.get('title') or '').lower()
    p = v.get('portal') or ''
    loc = v.get('location') or ''
    company = v.get('company') or ''
    if any(term in t for term in terms):
        matches.append((p, v.get('title'), company, loc, k))

print(f"Total keyword matching new jobs: {len(matches)}")
for idx, (p, title, company, loc, k) in enumerate(matches[:40], 1):
    print(f"{idx:2d}. [{p}] {title} @ {company} ({loc})")
