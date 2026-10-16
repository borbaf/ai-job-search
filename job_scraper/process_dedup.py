import json
import re
import unicodedata
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.job_key import make_key

with open('job_scraper/raw_sweep_results.json', 'r', encoding='utf-8') as f:
    raw_jobs = json.load(f)

with open('job_scraper/seen_jobs.json', 'r', encoding='utf-8') as f:
    seen_data = json.load(f)

seen_dict = seen_data.get('seen', {})
seen_urls = set()
seen_keys = set(seen_dict.keys())

for k, v in seen_dict.items():
    if isinstance(v, dict) and v.get('url'):
        seen_urls.add(v['url'])
    # also key might be url in legacy records
    if k.startswith('http'):
        seen_urls.add(k)

print(f"Total raw scraped: {len(raw_jobs)}")
print(f"Existing seen keys: {len(seen_keys)}, unique URLs: {len(seen_urls)}")

# Deduplicate raw items among themselves and against seen_jobs
new_jobs = []
dedup_keys_this_run = set()

def normalize_url(u):
    if not u:
        return ""
    return u.split('?')[0].rstrip('/')

for item in raw_jobs:
    title = item.get('title') or item.get('position') or item.get('name') or ''
    company = item.get('company') or item.get('company_name') or item.get('employer') or 'Unknown'
    url = item.get('url') or item.get('link') or item.get('external_url') or ''
    portal = item.get('_portal_source', 'portal')
    location = item.get('location') or item.get('city') or ''
    
    if not title or not url:
        continue
        
    norm_url = normalize_url(url)
    if norm_url in seen_urls:
        continue
    if any(norm_url == normalize_url(su) for su in seen_urls):
        continue
        
    key = make_key(company, title, url)
    if key in seen_keys or key in dedup_keys_this_run:
        continue
        
    dedup_keys_this_run.add(key)
    item['_canonical_key'] = key
    item['_norm_url'] = norm_url
    new_jobs.append(item)

print(f"New candidate jobs after deduplication: {len(new_jobs)}")

with open('job_scraper/deduped_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(new_jobs, f, indent=2, ensure_ascii=False)
