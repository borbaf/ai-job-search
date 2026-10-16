import json

with open('job_scraper/seen_jobs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

seen = data['seen']

# We want to identify URLs that exist both under a legacy key (like url as key) and a new canonical key
# and retain the best metadata while removing the duplicate entry.
url_to_keys = {}
for k, v in seen.items():
    u = v.get('url') if isinstance(v, dict) else None
    if u:
        url_to_keys.setdefault(u, []).append(k)

fixed_seen = dict(seen)
removed = 0
for u, keys in url_to_keys.items():
    if len(keys) > 1:
        # Keep the canonical key (the one not starting with http), remove http key
        http_keys = [k for k in keys if k.startswith('http')]
        canon_keys = [k for k in keys if not k.startswith('http')]
        if http_keys and canon_keys:
            for hk in http_keys:
                del fixed_seen[hk]
                removed += 1

print(f"Removed {removed} duplicate URL keys from seen_jobs.json.")
data['seen'] = fixed_seen

with open('job_scraper/seen_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
