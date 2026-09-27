"""Scrape autônomo da sandbox: coleta vagas via CLIs de busca (bun) SEM custo de LLM.

Otimizações desta versão:
- Localização ajustada POR PORTAL — resolve a ambiguidade de "SC": nos portais
  internacionais vira South Carolina/EUA; nos brasileiros, Santa Catarina.
- Tratamento de erro por portal (um portal que falha não derruba o run).
- Encoding UTF-8 explícito (evita "S�o Paulo" no console).
- Persiste o resultado em sandbox/state/scraped_jobs.json.

Uso:
  python sandbox/run_scrape.py "supply chain" "SC" 5
  python sandbox/run_scrape.py "supply chain" "remoto" 5
"""
import json, os, sys, argparse, subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
import config as C

# ---------------------------------------------------------------------------
# Localização por portal.
# O argumento posicional <location> é o fallback; este mapa sobrescreve por portal.
# Ajuste conforme sua política (BR vs internacional/remoto).
# ---------------------------------------------------------------------------
LOCATION_BY_PORTAL = {
    # Brasileiros: estado BR ou "remoto"
    "gupy":         "Santa Catarina",
    "catho":        "Santa Catarina",
    "infojobs":     "Santa Catarina",
    # Internacionais / remoto
    "linkedin":     "Brazil",
    "freehire":     "remote",
    "dynamitejobs": "remote",
    "hirelatam":    "remote",
}

# Flag de localização por portal. A maioria usa "-l"; se algum CLI divergir,
# rode '<cli> search --help' e ajuste aqui (ex.: "--location").
LOCATION_FLAG = {
    "linkedin":     "-l",
    "gupy":         "-l",
    "catho":        "-l",
    "infojobs":     "-l",
    "freehire":     "-l",
    "dynamitejobs": "-l",
    "hirelatam":    "-l",
}

def run_portal(name, cmd, query, location):
    """Executa um portal e retorna (ok, jobs, error)."""
    loc = LOCATION_BY_PORTAL.get(name, location)
    flag = LOCATION_FLAG.get(name, "-l")
    full = cmd + [query, flag, loc]
    try:
        out = subprocess.run(full, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=120)
    except Exception as e:
        return False, [], f"falha ao executar: {e}"
    if out.returncode != 0:
        return False, [], (out.stderr or out.stdout or "")[-500:]
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError as e:
        return False, [], f"saída não é JSON: {e}"
    jobs = data.get("results", []) if isinstance(data, dict) else []
    return True, jobs, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="termo de busca (ex.: 'supply chain')")
    ap.add_argument("location", nargs="?", default="SC", help="localização fallback")
    ap.add_argument("limit", nargs="?", type=int, default=5, help="vagas por portal")
    args = ap.parse_args()

    os.makedirs(C.STATE_DIR, exist_ok=True)
    all_jobs = []
    summary = []

    for name, cmd in C.PORTALS.items():
        print(f"\n== {name} ==")
        ok, jobs, err = run_portal(name, cmd, args.query, args.location)
        if not ok:
            print(f"  [ERRO] {err}")
            summary.append((name, "erro", 0))
            continue
        jobs = jobs[:args.limit]
        for j in jobs:
            j["portal"] = name
            j["scraped_at"] = datetime.now().isoformat()
        all_jobs.extend(jobs)
        print(f"  {len(jobs)} vagas")
        summary.append((name, "ok", len(jobs)))

    out_path = os.path.join(C.STATE_DIR, "scraped_jobs.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"scraped_at": datetime.now().isoformat(),
                   "query": args.query,
                   "location": args.location,
                   "jobs": all_jobs}, f, ensure_ascii=False, indent=2)

    print("\n== Resumo ==")
    for name, status, n in summary:
        print(f"  {name:12} {status:6} {n}")
    print(f"\nTotal: {len(all_jobs)} vagas salvas em {out_path}")

if __name__ == "__main__":
    main()