import subprocess
import json
import os
import sys

queries = [
    # Remotar
    ("remotar", 'bun run .agents/skills/remotar-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("remotar", 'bun run .agents/skills/remotar-search/cli/src/cli.ts search --query "Logistica" --format json'),
    ("remotar", 'bun run .agents/skills/remotar-search/cli/src/cli.ts search --query "Planejamento" --format json'),
    ("remotar", 'bun run .agents/skills/remotar-search/cli/src/cli.ts search --query "Operacoes" --format json'),
    
    # HireLATAM
    ("hirelatam", 'bun run .agents/skills/hirelatam-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("hirelatam", 'bun run .agents/skills/hirelatam-search/cli/src/cli.ts search --query "Logistics" --format json'),
    ("hirelatam", 'bun run .agents/skills/hirelatam-search/cli/src/cli.ts search --query "Operations" --format json'),
    
    # Get on Board
    ("getonbrd", 'bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("getonbrd", 'bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --query "Logistics" --format json'),
    ("getonbrd", 'bun run .agents/skills/getonbrd-search/cli/src/cli.ts search --query "Operations" --format json'),

    # Solvo Global
    ("solvoglobal", 'bun run .agents/skills/solvoglobal-search/cli/src/cli.ts search --query "Logistics" --format json'),
    ("solvoglobal", 'bun run .agents/skills/solvoglobal-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("solvoglobal", 'bun run .agents/skills/solvoglobal-search/cli/src/cli.ts search --query "Operations" --format json'),

    # Himalayas
    ("himalayas", 'bun run .agents/skills/himalayas-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("himalayas", 'bun run .agents/skills/himalayas-search/cli/src/cli.ts search --query "Logistics" --format json'),
    ("himalayas", 'bun run .agents/skills/himalayas-search/cli/src/cli.ts search --query "Operations Manager" --format json'),

    # Remotive
    ("remotive", 'bun run .agents/skills/remotive-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("remotive", 'bun run .agents/skills/remotive-search/cli/src/cli.ts search --query "Logistics" --format json'),
    ("remotive", 'bun run .agents/skills/remotive-search/cli/src/cli.ts search --query "Operations" --format json'),

    # Dynamite Jobs
    ("dynamitejobs", 'bun run .agents/skills/dynamitejobs-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("dynamitejobs", 'bun run .agents/skills/dynamitejobs-search/cli/src/cli.ts search --query "Logistics" --format json'),
    ("dynamitejobs", 'bun run .agents/skills/dynamitejobs-search/cli/src/cli.ts search --query "Operations" --format json'),

    # We Work Remotely
    ("weworkremotely", 'bun run .agents/skills/weworkremotely-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("weworkremotely", 'bun run .agents/skills/weworkremotely-search/cli/src/cli.ts search --query "Logistics" --format json'),
    ("weworkremotely", 'bun run .agents/skills/weworkremotely-search/cli/src/cli.ts search --query "Operations" --format json'),

    # Job na Gringa
    ("jobnagringa", 'bun run .agents/skills/jobnagringa-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("jobnagringa", 'bun run .agents/skills/jobnagringa-search/cli/src/cli.ts search --query "Logistics" --format json'),

    # LinkedIn Remote Brazil
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Supply Chain" -l "Brazil" --remote remote --format json'),
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Logistica" -l "Brazil" --remote remote --format json'),
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "S&OP" -l "Brazil" --remote remote --format json'),
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Gerente de Operacoes" -l "Brazil" --remote remote --format json'),
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Supply Chain Manager" -l "Brazil" --remote remote --format json'),
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Coordenador de Logistica" -l "Brazil" --remote remote --format json'),
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Torre de Controle" -l "Brazil" --remote remote --format json'),
    
    # LinkedIn Regional (Florianópolis / Santa Catarina / Fortaleza)
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Supply Chain" -l "Santa Catarina, Brazil" --format json'),
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Logistica" -l "Santa Catarina, Brazil" --format json'),
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Supply Chain" -l "Fortaleza, Ceara, Brazil" --format json'),
    ("linkedin", 'bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "Logistica" -l "Fortaleza, Ceara, Brazil" --format json'),

    # Catho (Desativado conforme diretriz)
    # ("catho", 'bun run .agents/skills/catho-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    # ("catho", 'bun run .agents/skills/catho-search/cli/src/cli.ts search --query "Gerente Logistica" --format json'),
    # ("catho", 'bun run .agents/skills/catho-search/cli/src/cli.ts search --query "Coordenador Logistica" --format json'),

    # InHire (nstech, Mottu, Wilson Sons, Deloitte, Autoglass, etc.)
    ("inhire", 'bun run .agents/skills/inhire-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("inhire", 'bun run .agents/skills/inhire-search/cli/src/cli.ts search --query "Logistica" --format json'),
    ("inhire", 'bun run .agents/skills/inhire-search/cli/src/cli.ts search --query "Operacoes" --format json'),
    ("inhire", 'bun run .agents/skills/inhire-search/cli/src/cli.ts search --query "Planejamento" --format json'),

    # Infojobs
    ("infojobs", 'bun run .agents/skills/infojobs-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ("infojobs", 'bun run .agents/skills/infojobs-search/cli/src/cli.ts search --query "Gerente Logistica" --format json'),
    ("infojobs", 'bun run .agents/skills/infojobs-search/cli/src/cli.ts search --query "Coordenador Logistica" --format json'),
]

all_raw_jobs = []

for portal, cmd in queries:
    print(f"Executing: [{portal}] {cmd}")
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace')
        if res.returncode != 0:
            print(f"  Error ({res.returncode}): {res.stderr[:200]}")
            continue
        try:
            parsed = json.loads(res.stdout)
            items = []
            if isinstance(parsed, list):
                items = parsed
            elif isinstance(parsed, dict):
                items = parsed.get("results", []) or parsed.get("data", []) or parsed.get("jobs", [])
            print(f"  Found {len(items)} items")
            for it in items:
                it["_portal_source"] = portal
                all_raw_jobs.append(it)
        except Exception as e:
            print(f"  Failed to parse JSON: {e}")
    except Exception as exc:
        print(f"  Subprocess error: {exc}")

print(f"\nTotal raw items collected across all queries: {len(all_raw_jobs)}")
with open("job_scraper/raw_sweep_results.json", "w", encoding="utf-8") as f:
    json.dump(all_raw_jobs, f, indent=2, ensure_ascii=False)
print("Saved raw sweep results to job_scraper/raw_sweep_results.json")
