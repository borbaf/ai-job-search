import json

with open('job_scraper/seen_jobs.json', 'r', encoding='utf-8') as f:
    seen = json.load(f)['seen']

discovered = [(k, v) for k, v in seen.items() if v.get('status') == 'discovered']

# Prioritize:
# 1. High fit international/remote USD (dynamitejobs, himalayas, getonbrd)
# 2. High fit remote/regional BRL (remotar, linkedin)
# 3. High fit catho / infojobs
def sort_key(item):
    k, v = item
    portal = v.get('portal', '')
    fit = v.get('fit', '')
    p_score = 0
    if portal in ['dynamitejobs', 'himalayas', 'hirelatam', 'solvoglobal']:
        p_score = 4
    elif portal in ['remotar', 'linkedin']:
        p_score = 3
    elif portal in ['getonbrd']:
        p_score = 2
    else:
        p_score = 1
    f_score = 2 if fit == 'high' else 1
    return (f_score, p_score)

discovered.sort(key=sort_key, reverse=True)

batch = discovered[:10]
print(f"Selected batch of {len(batch)} candidates for scoring:")
for i, (k, v) in enumerate(batch):
    print(f"{i+1}. [{v.get('portal')}] {v.get('title')} @ {v.get('company')} | Key: {k}")
    print(f"   URL: {v.get('url')}")
