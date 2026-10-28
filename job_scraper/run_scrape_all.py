import subprocess
import json
import os
import sys
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.job_key import make_key

# Portais e comandos de busca de acordo com .claude/commands/scrape.md
portals_commands = [
    # Tier 1
    ("remotar", [
        'bun run .agents/skills/remotar-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/remotar-search/cli/src/cli.ts search --query "Logistica" --format json',
        'bun run .agents/skills/remotar-search/cli/src/cli.ts search --query "Operacoes" --format json',
        'bun run .agents/skills/remotar-search/cli/src/cli.ts search --query "Planejamento" --format json',
    ]),
    ("hirelatam", [
        'bun run .agents/skills/hirelatam-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/hirelatam-search/cli/src/cli.ts search --query "Logistics" --format json',
        'bun run .agents/skills/hirelatam-search/cli/src/cli.ts search --query "Operations" --format json',
    ]),
    ("solvoglobal", [
        'bun run .agents/skills/solvoglobal-search/cli/src/cli.ts search --query "Logistics" --format json',
        'bun run .agents/skills/solvoglobal-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/solvoglobal-search/cli/src/cli.ts search --query "Operations" --format json',
    ]),
    ("getonbrd", [
        'bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --query "Logistics" --format json',
        'bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --query "Operations" --format json',
    ]),

    # Tier 2
    ("dynamitejobs", [
        'bun run .agents/skills/dynamitejobs-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/dynamitejobs-search/cli/src/cli.ts search --query "Logistics" --format json',
        'bun run .agents/skills/dynamitejobs-search/cli/src/cli.ts search --query "Operations" --format json',
    ]),
    ("himalayas", [
        'bun run .agents/skills/himalayas-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/himalayas-search/cli/src/cli.ts search --query "Logistics" --format json',
        'bun run .agents/skills/himalayas-search/cli/src/cli.ts search --query "Operations Manager" --format json',
    ]),
    ("remotive", [
        'bun run .agents/skills/remotive-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/remotive-search/cli/src/cli.ts search --query "Logistics" --format json',
        'bun run .agents/skills/remotive-search/cli/src/cli.ts search --query "Operations" --format json',
    ]),
    ("weworkremotely", [
        'bun run .agents/skills/weworkremotely-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/weworkremotely-search/cli/src/cli.ts search --query "Logistics" --format json',
        'bun run .agents/skills/weworkremotely-search/cli/src/cli.ts search --query "Operations" --format json',
    ]),
    ("jobnagringa", [
        'bun run .agents/skills/jobnagringa-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/jobnagringa-search/cli/src/cli.ts search --query "Logistics" --format json',
    ]),
    ("ziprecruiter", [
        'bun run .agents/skills/ziprecruiter-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/ziprecruiter-search/cli/src/cli.ts search --query "Logistics Manager" --format json',
    ]),

    # Tier 3
    ("inhire", [
        'bun run .agents/skills/inhire-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/inhire-search/cli/src/cli.ts search --query "Logistica" --format json',
        'bun run .agents/skills/inhire-search/cli/src/cli.ts search --query "Operacoes" --format json',
        'bun run .agents/skills/inhire-search/cli/src/cli.ts search --query "Planejamento" --format json',
    ]),
    ("linkedin", [
        'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Supply Chain" -l "Brazil" --remote remote --format json',
        'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Logistica" -l "Brazil" --remote remote --format json',
        'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "S&OP" -l "Brazil" --remote remote --format json',
        'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Supply Chain Manager" -l "Brazil" --remote remote --format json',
        'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Supply Chain" -l "Santa Catarina, Brazil" --format json',
        'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Logistica" -l "Santa Catarina, Brazil" --format json',
        'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Supply Chain" -l "Fortaleza, Ceara, Brazil" --format json',
        'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Logistica" -l "Fortaleza, Ceara, Brazil" --format json',
    ]),
    ("freehire", [
        'bun run .agents/skills/freehire-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/freehire-search/cli/src/cli.ts search --query "Logistics" --format json',
    ]),
    ("infojobs", [
        'bun run .agents/skills/infojobs-search/cli/src/cli.ts search --query "Supply Chain" --format json',
        'bun run .agents/skills/infojobs-search/cli/src/cli.ts search --query "Gerente Logistica" --format json',
        'bun run .agents/skills/infojobs-search/cli/src/cli.ts search --query "Coordenador Logistica" --format json',
    ]),
]

# Load existing seen_jobs.json
seen_file = ROOT / "job_scraper" / "seen_jobs.json"
with open(seen_file, "r", encoding="utf-8") as f:
    seen_state = json.load(f)

seen_dict = seen_state.setdefault("seen", {})
seen_urls = {entry.get("url") for entry in seen_dict.values() if entry.get("url")}
seen_keys = set(seen_dict.keys())

today_str = datetime.date.today().isoformat()
sweep_summary = {}

print(f"=== Starting full scrape across {len(portals_commands)} configured portals ===")

for portal, cmd_list in portals_commands:
    portal_raw_items = []
    portal_failed = False
    fail_err = ""

    for cmd in cmd_list:
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=40, encoding="utf-8", errors="replace")
            if res.returncode != 0:
                print(f"[{portal}] Warning: command returned {res.returncode}")
                continue
            output = res.stdout.strip()
            if not output:
                continue
            data = json.loads(output)
            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = data.get("results", []) or data.get("data", []) or data.get("jobs", [])
            portal_raw_items.extend(items)
        except Exception as e:
            portal_failed = True
            fail_err = str(e)
            print(f"[{portal}] Error during execution: {e}")

    # Deduplicate within this portal run and against seen_jobs
    portal_new_jobs = []
    seen_in_this_run = set()

    for item in portal_raw_items:
        title = (item.get("title") or item.get("displayName") or item.get("position") or "").strip()
        company = (item.get("company") or item.get("company_name") or item.get("companyDisplayName") or item.get("tenantName") or "Unknown").strip()
        url = (item.get("url") or item.get("link") or item.get("external_url") or "").strip()
        location = item.get("location") or item.get("workplace_type") or "Not specified"

        if not title or not url:
            continue

        job_key = make_key(company, title, url)
        if job_key in seen_keys or url in seen_urls or job_key in seen_in_this_run or url in seen_in_this_run:
            continue

        seen_in_this_run.add(job_key)
        seen_in_this_run.add(url)
        seen_keys.add(job_key)
        seen_urls.add(url)

        # Register in seen_jobs.json with status "new"
        job_record = {
            "title": title,
            "company": company,
            "url": url,
            "location": location,
            "date_found": today_str,
            "date_posted": item.get("date") or item.get("posted_date") or today_str,
            "portal": portal,
            "status": "new",
            "score": None,
            "raw": item
        }
        seen_dict[job_key] = job_record
        portal_new_jobs.append(job_record)

    sweep_summary[portal] = {
        "collected_raw": len(portal_raw_items),
        "new_registered": len(portal_new_jobs),
        "failed": portal_failed and len(portal_raw_items) == 0,
        "error": fail_err if portal_failed and len(portal_raw_items) == 0 else None,
        "sample": portal_new_jobs[:5]
    }
    print(f"[{portal}] Total raw: {len(portal_raw_items)} | New registered: {len(portal_new_jobs)}")

# Save updated seen_jobs.json
with open(seen_file, "w", encoding="utf-8") as f:
    json.dump(seen_state, f, indent=2, ensure_ascii=False)

# Save sweep report
report_path = ROOT / "job_scraper" / "latest_scrape_summary.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(sweep_summary, f, indent=2, ensure_ascii=False)

print("\n=== Scrape Complete ===")
total_new = sum(s["new_registered"] for s in sweep_summary.values())
print(f"Total new jobs collected: {total_new}")
