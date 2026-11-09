import json
import os
import subprocess
import sys
from datetime import datetime, timedelta

def run_cmd(cmd, timeout=30):
    try:
        p = subprocess.run(cmd, capture_output=True, encoding='utf-8', errors='replace', timeout=timeout)
        if p.returncode != 0:
            return None, p.stderr.strip()
        return p.stdout.strip(), None
    except Exception as e:
        return None, str(e)

def parse_json(raw):
    if not raw:
        return []
    try:
        d = json.loads(raw)
        if isinstance(d, list):
            return d
        if isinstance(d, dict):
            return d.get('results', d.get('jobs', []))
    except Exception:
        pass
    return []

def main():
    print("=== STARTING FULL PORTAL SCRAPE ===")
    seen_path = 'job_scraper/seen_jobs.json'
    with open(seen_path, 'r', encoding='utf-8') as f:
        seen_data = json.load(f)
    seen_dict = seen_data.get('seen', {})
    seen_urls = {v.get('url'): k for k, v in seen_dict.items() if v.get('url')}
    seen_comp_title = {(v.get('company', '').lower().strip(), v.get('title', '').lower().strip()): k for k, v in seen_dict.items()}

    # Tasks configuration
    # Portal -> queries
    searches = [
        # Tier 1 (LATAM & Brazil Priority)
        ('remotar-search', ['bun', 'run', '.agents/skills/remotar-search/cli/src/cli.ts', 'search', '-q', 'supply chain', '-n', '20']),
        ('remotar-search', ['bun', 'run', '.agents/skills/remotar-search/cli/src/cli.ts', 'search', '-q', 'logistica', '-n', '20']),
        ('remotar-search', ['bun', 'run', '.agents/skills/remotar-search/cli/src/cli.ts', 'search', '-q', 'operacoes', '-n', '20']),
        ('remotar-search', ['bun', 'run', '.agents/skills/remotar-search/cli/src/cli.ts', 'search', '-q', 'planejamento', '-n', '20']),

        ('hirelatam-search', ['bun', 'run', '.agents/skills/hirelatam-search/cli/src/cli.ts', 'search', '-q', 'supply chain']),
        ('hirelatam-search', ['bun', 'run', '.agents/skills/hirelatam-search/cli/src/cli.ts', 'search', '-q', 'logistics']),
        ('hirelatam-search', ['bun', 'run', '.agents/skills/hirelatam-search/cli/src/cli.ts', 'search', '-q', 'operations']),

        ('solvoglobal-search', ['bun', 'run', '.agents/skills/solvoglobal-search/cli/src/cli.ts', 'search', '-q', 'logistics']),
        ('solvoglobal-search', ['bun', 'run', '.agents/skills/solvoglobal-search/cli/src/cli.ts', 'search', '-q', 'supply chain']),
        ('solvoglobal-search', ['bun', 'run', '.agents/skills/solvoglobal-search/cli/src/cli.ts', 'search', '-q', 'operations']),

        ('getonbrd-search', ['bun', 'run', '.agents/skills/getonbrd-search/cli/src/cli.ts', 'search', '-q', 'supply chain', '-n', '20']),
        ('getonbrd-search', ['bun', 'run', '.agents/skills/getonbrd-search/cli/src/cli.ts', 'search', '-q', 'logistics', '-n', '20']),
        ('getonbrd-search', ['bun', 'run', '.agents/skills/getonbrd-search/cli/src/cli.ts', 'search', '-q', 'operations', '-n', '20']),

        # Tier 2 (Global Remote)
        ('dynamitejobs-search', ['bun', 'run', '.agents/skills/dynamitejobs-search/cli/src/cli.ts', 'search', '-q', 'supply chain']),
        ('dynamitejobs-search', ['bun', 'run', '.agents/skills/dynamitejobs-search/cli/src/cli.ts', 'search', '-q', 'operations']),
        ('dynamitejobs-search', ['bun', 'run', '.agents/skills/dynamitejobs-search/cli/src/cli.ts', 'search', '-q', 'logistics']),

        ('himalayas-search', ['bun', 'run', '.agents/skills/himalayas-search/cli/src/cli.ts', 'search', '-q', 'supply chain', '-n', '20']),
        ('himalayas-search', ['bun', 'run', '.agents/skills/himalayas-search/cli/src/cli.ts', 'search', '-q', 'logistics', '-n', '20']),
        ('himalayas-search', ['bun', 'run', '.agents/skills/himalayas-search/cli/src/cli.ts', 'search', '-q', 'operations manager', '-n', '20']),

        ('remotive-search', ['bun', 'run', '.agents/skills/remotive-search/cli/src/cli.ts', 'search', '-q', 'supply chain', '-n', '20']),
        ('remotive-search', ['bun', 'run', '.agents/skills/remotive-search/cli/src/cli.ts', 'search', '-q', 'logistics', '-n', '20']),
        ('remotive-search', ['bun', 'run', '.agents/skills/remotive-search/cli/src/cli.ts', 'search', '-q', 'operations', '-n', '20']),

        ('weworkremotely-search', ['bun', 'run', '.agents/skills/weworkremotely-search/cli/src/cli.ts', 'search', '-q', 'supply chain', '-n', '20']),
        ('weworkremotely-search', ['bun', 'run', '.agents/skills/weworkremotely-search/cli/src/cli.ts', 'search', '-q', 'logistics', '-n', '20']),
        ('weworkremotely-search', ['bun', 'run', '.agents/skills/weworkremotely-search/cli/src/cli.ts', 'search', '-q', 'operations manager', '-n', '20']),

        # Tier 3 (Brazilian & Curated)
        ('inhire-search', ['bun', 'run', '.agents/skills/inhire-search/cli/src/cli.ts', 'search', '--query', 'supply chain', '--limit', '20']),
        ('inhire-search', ['bun', 'run', '.agents/skills/inhire-search/cli/src/cli.ts', 'search', '--query', 'logistica', '--limit', '20']),
        ('inhire-search', ['bun', 'run', '.agents/skills/inhire-search/cli/src/cli.ts', 'search', '--query', 'operacoes', '--limit', '20']),

        ('jobnagringa-search', ['bun', 'run', '.agents/skills/jobnagringa-search/cli/src/cli.ts', 'search', '-q', 'supply chain', '-n', '20']),
        ('jobnagringa-search', ['bun', 'run', '.agents/skills/jobnagringa-search/cli/src/cli.ts', 'search', '-q', 'operations', '-n', '20']),

        ('infojobs-search', ['bun', 'run', '.agents/skills/infojobs-search/cli/src/cli.ts', 'search', '-q', 'supply chain']),
        ('infojobs-search', ['bun', 'run', '.agents/skills/infojobs-search/cli/src/cli.ts', 'search', '-q', 'gerente de operacoes']),

        # Additional Active Aggregators
        ('freehire-search', ['bun', 'run', '.agents/skills/freehire-search/cli/src/cli.ts', 'search', '-q', 'supply chain', '--format', 'json']),
        ('freehire-search', ['bun', 'run', '.agents/skills/freehire-search/cli/src/cli.ts', 'search', '-q', 'logistics', '--format', 'json']),

        ('ziprecruiter-search', ['bun', 'run', '.agents/skills/ziprecruiter-search/cli/src/cli.ts', 'search', '-q', 'supply chain remote']),
        ('sprout-search', ['bun', 'run', '.agents/skills/sprout-search/cli/src/cli.ts', 'search', '-q', 'operations', '-n', '20']),

        # LinkedIn Search (Remote & Brazil)
        ('linkedin-search', ['bun', 'run', '.agents/skills/linkedin-search/cli/src/cli.ts', 'search', '-q', 'supply chain manager', '-l', 'Remote', '--remote', 'remote', '--jobage', '14', '--format', 'json']),
        ('linkedin-search', ['bun', 'run', '.agents/skills/linkedin-search/cli/src/cli.ts', 'search', '-q', 'gerente de operacoes', '-l', 'Brazil', '--remote', 'remote', '--jobage', '14', '--format', 'json']),
        ('linkedin-search', ['bun', 'run', '.agents/skills/linkedin-search/cli/src/cli.ts', 'search', '-q', 'S&OP', '-l', 'Brazil', '--remote', 'remote', '--jobage', '14', '--format', 'json']),
    ]

    total_fetched = 0
    raw_candidates = []
    portal_stats = {}

    for portal, cmd in searches:
        query_label = " ".join(cmd[cmd.index('search')+1:])
        print(f"[{portal}] Running {query_label} ...")
        out, err = run_cmd(cmd, timeout=40)
        if err:
            print(f"  -> Warn/Err: {err[:120]}")
            portal_stats[portal] = portal_stats.get(portal, 0)
            continue
        items = parse_json(out)
        print(f"  -> Found {len(items)} items")
        portal_stats[portal] = portal_stats.get(portal, 0) + len(items)
        total_fetched += len(items)
        for it in items:
            raw_candidates.append((portal, it))

    print(f"\nTotal raw jobs fetched across all portals: {total_fetched}")

    # Process and deduplicate
    new_jobs = []
    fourteen_days_ago = datetime.now() - timedelta(days=14)

    for portal, it in raw_candidates:
        title = (it.get('title') or it.get('name') or '').strip()
        company = (it.get('company') or it.get('employer') or '').strip()
        url = (it.get('url') or it.get('link') or it.get('apply_url') or '').strip()
        location = (it.get('location') or it.get('city') or it.get('region') or 'Remote').strip()
        posted_date = it.get('date') or it.get('posted_date') or it.get('published_at') or None
        description = (it.get('description') or it.get('description_snippet') or it.get('snippet') or '').strip()

        if not title or not url:
            continue

        # Check against seen
        if url in seen_urls:
            continue
        if (company.lower().strip(), title.lower().strip()) in seen_comp_title:
            continue

        # Check recency if date present
        if posted_date:
            try:
                dt_str = str(posted_date)[:10]
                dt = datetime.strptime(dt_str, '%Y-%m-%d')
                if dt < fourteen_days_ago:
                    continue
            except Exception:
                pass

        # Check negative filters
        t_low = title.lower()
        if any(neg in t_low for neg in ['junior', 'júnior', 'estagio', 'estágio', 'estagiário', 'trainee', 'aprendiz', 'intern ']):
            continue
        if 'blumenau' in location.lower():
            continue

        # Get canonical key
        key_cmd = ['python', 'tools/job_key.py', '--company', company, '--title', title, '--url', url]
        k_out, _ = run_cmd(key_cmd, timeout=5)
        key = k_out.strip() if k_out else f"{company.lower()}-{title.lower()}"

        if key in seen_dict:
            continue

        # Quick fit evaluation
        fit = "medium"
        t_clean = t_low.replace('ç', 'c').replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('ó', 'o')
        
        # High match criteria
        if any(core in t_clean for core in [
            'supply chain', 'logistica', 'logistics', 's&op', 'demand plan', 'demand planner',
            'torre de controle', 'control tower', 'operacoes', 'operations manager',
            'diretor de operacoes', 'gerente de operacoes', 'coordenador de operacoes',
            'coordenador de logistica', 'gerente de logistica', 'head of supply chain',
            'head de operacoes', 'head de logistica', 'procurement', 'suprimentos',
            'product manager logistics', 'product owner logistics', 'product owner tms', 'product owner wms'
        ]):
            fit = "high"
        elif any(adj in t_clean for adj in [
            'operations', 'operacao', 'operational', 'planejamento', 'planning',
            'consultant', 'continuous improvement', 'melhoria continua', 'process manager',
            'project manager', 'program manager', 'business analyst operations'
        ]):
            fit = "medium"
        else:
            fit = "low"

        # Language or remote vetoes in title/desc
        desc_low = description.lower()
        if 'us only' in desc_low or 'must reside in the us' in desc_low or 'us citizen' in desc_low:
            continue # Hard veto Gate 1

        new_entry = {
            'key': key,
            'title': title,
            'company': company,
            'url': url,
            'location': location,
            'first_seen': datetime.now().strftime('%Y-%m-%d'),
            'posted_date': posted_date,
            'deadline': it.get('deadline') or it.get('expires_at') or None,
            'fit': fit,
            'status': 'new',
            'portal': portal,
            'source': 'cli',
            'description': description[:300]
        }
        new_jobs.append(new_entry)
        seen_urls[url] = key
        seen_comp_title[(company.lower().strip(), title.lower().strip())] = key
        seen_dict[key] = {
            'title': title,
            'company': company,
            'url': url,
            'first_seen': new_entry['first_seen'],
            'posted_date': posted_date,
            'deadline': new_entry['deadline'],
            'fit': fit,
            'status': 'new',
            'portal': portal,
            'source': 'cli'
        }

    # Save updated seen_jobs.json
    seen_data['seen'] = seen_dict
    with open(seen_path, 'w', encoding='utf-8') as f:
        json.dump(seen_data, f, indent=2, ensure_ascii=False)

    # Save new jobs output to scratch for presentation
    with open('job_scraper/latest_scrape_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'portal_stats': portal_stats,
            'total_fetched': total_fetched,
            'new_jobs': new_jobs
        }, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(new_jobs)} NEW jobs to seen_jobs.json and job_scraper/latest_scrape_results.json")

if __name__ == '__main__':
    main()
