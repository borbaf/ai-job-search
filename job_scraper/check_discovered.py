import json

with open('job_scraper/seen_jobs.json', 'r', encoding='utf-8') as f:
    seen = json.load(f)['seen']

discovered = [(k, v) for k, v in seen.items() if v.get('status') == 'discovered']
print(f"Total discovered jobs in seen_jobs.json: {len(discovered)}")

high = [x for x in discovered if x[1].get('fit') == 'high']
med = [x for x in discovered if x[1].get('fit') == 'medium']

print(f"High fit: {len(high)}, Medium fit: {len(med)}")

print("\n--- SAMPLE HIGH FIT DISCOVERED ---")
for k, v in high[:15]:
    print(f"- [{v.get('portal')}] {v.get('title')} @ {v.get('company')}")
    print(f"  URL: {v.get('url')}")
