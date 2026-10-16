import json

with open('job_scraper/seen_jobs.json', 'r', encoding='utf-8') as f:
    seen = json.load(f)['seen']

discovered = [(k, v) for k, v in seen.items() if v.get('status') == 'discovered']

# Let's inspect all USD jobs and top BRL jobs
usd = [(k, v) for k, v in discovered if v.get('portal') in ['hirelatam', 'dynamitejobs', 'solvoglobal', 'himalayas', 'weworkremotely', 'getonbrd']]
brl_high = [(k, v) for k, v in discovered if v.get('fit') == 'high' and v.get('portal') in ['remotar', 'linkedin', 'catho', 'infojobs']]

print(f"USD candidates count: {len(usd)}")
for k, v in usd:
    print(f"[{v.get('portal')}] {v.get('title')} @ {v.get('company')} | {k}")
    print(f"  URL: {v.get('url')}")

print(f"\nBRL High candidates count: {len(brl_high)}")
for k, v in brl_high[:20]:
    print(f"[{v.get('portal')}] {v.get('title')} @ {v.get('company')} | {k}")
    print(f"  URL: {v.get('url')}")
