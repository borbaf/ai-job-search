import json
import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.job_key import make_key

# Load evaluated jobs
with open('job_scraper/evaluated_sweep.json', 'r', encoding='utf-8') as f:
    evaluated = json.load(f)

# Load existing seen_jobs.json
with open('job_scraper/seen_jobs.json', 'r', encoding='utf-8') as f:
    seen_data = json.load(f)

seen_dict = seen_data.get('seen', {})

today_str = datetime.date.today().isoformat()

added_count = 0
all_evaluated_jobs = evaluated.get('high', []) + evaluated.get('medium', []) + evaluated.get('skipped', [])

for entry in all_evaluated_jobs:
    job = entry['job']
    fit = entry.get('fit', 'low')
    status = entry.get('status', 'skipped')
    veto = entry.get('veto_reason')
    
    title = job.get('title') or job.get('position') or ''
    company = job.get('company') or job.get('company_name') or 'Unknown'
    url = job.get('url') or job.get('link') or ''
    portal = job.get('_portal_source', 'portal')
    date_posted = job.get('date') or job.get('posted_date') or today_str
    
    if not title or not url:
        continue
        
    canonical_key = job.get('_canonical_key') or make_key(company, title, url)
    
    # Do not overwrite if already exists
    if canonical_key in seen_dict or url in seen_dict:
        continue
        
    seen_dict[canonical_key] = {
        'title': title,
        'company': company,
        'url': url,
        'first_seen': today_str,
        'posted_date': date_posted,
        'deadline': None,
        'fit': fit,
        'status': 'discovered' if status == 'active' else 'skipped',
        'portal': portal,
        'source': 'cli',
        'notes': veto if veto else ''
    }
    added_count += 1

seen_data['seen'] = seen_dict

with open('job_scraper/seen_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(seen_data, f, indent=2, ensure_ascii=False)

print(f"Successfully added {added_count} new entries to seen_jobs.json. Total entries now: {len(seen_dict)}")
