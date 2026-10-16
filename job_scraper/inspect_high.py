import json

with open('job_scraper/evaluated_sweep.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

high = data['high']
print(f"Total High matches: {len(high)}")
for i, item in enumerate(high):
    j = item['job']
    portal = j.get('_portal_source', '')
    title = j.get('title', '')
    company = j.get('company', '')
    loc = j.get('location', '')
    url = j.get('url', '')
    print(f"{i+1}. [{portal}] {title} @ {company} | Loc: {loc}")
    print(f"   URL: {url}")
