import json

with open('job_scraper/raw_sweep_results.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

for item in raw:
    title = item.get('title') or item.get('position') or ''
    portal = item.get('_portal_source', '')
    url = item.get('url') or item.get('link') or item.get('external_url') or ''
    comp = item.get('company') or item.get('company_name') or ''
    loc = item.get('location') or ''
    
    if portal in ['remotar', 'hirelatam', 'dynamitejobs', 'himalayas', 'weworkremotely']:
        t_low = title.lower()
        if any(w in t_low for w in ['supply chain', 'logist', 'operat', 's&op', 'procure', 'purchas']):
            print(f"[{portal}] {title} @ {comp} ({loc})")
            print(f"  URL: {url}")
            print(f"  Snippet: {(item.get('description_snippet') or item.get('description') or '')[:160]}")
            print("-" * 50)
