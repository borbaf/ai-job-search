"""Scrape autônomo da sandbox: coleta vagas via CLIs de busca (bun) SEM custo de LLM.

Otimizações desta versão:
- Localização ajustada POR PORTAL — resolve a ambiguidade de "SC" (Santa Catarina
  nos BR vs remote/Brazil nos internacionais) e respeita as flags de CADA CLI.
- PORTAL_SPEC: cada portal define a flag de query e os argumentos de localização
  que o próprio CLI aceita (ex.: freehire usa -q + --remote, não -l).
- Tratamento de erro por portal (um portal que falha não derruba o run).
- Encoding UTF-8 explícito (evita "S�o Paulo" no console).
- Persiste o resultado em sandbox/state/scraped_jobs.json.

Uso:
  python sandbox/run_scrape.py "supply chain" "SC" 5
"""
import json, os, sys, argparse, subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
import config as C

# ---------------------------------------------------------------------------
# Especificação de chamada POR PORTAL.
#   query_flag : flag de keywords. None = query posicional (padrão dos CLIs).
#   location_args : lista de argumentos de localização que o CLI aceita.
# Ajuste conforme o 'search --help' de cada CLI.
# ---------------------------------------------------------------------------
PORTAL_SPEC = {
    # Brasileiros: query posicional + "-l" com estado BR
    "gupy":         {"query_flag": None, "location_args": ["-l", "Santa Catarina"]},
    "catho":        {"query_flag": None, "location_args": ["-l", "Santa Catarina"]},
    "infojobs":     {"query_flag": None, "location_args": ["-l", "Santa Catarina"]},

    # Internacional / remoto
    "linkedin":     {"query_flag": None, "location_args": ["-l", "Brazil"]},
    "dynamitejobs": {"query_flag": None, "location_args": ["-l", "remote"]},
    "hirelatam":    {"query_flag": None, "location_args": ["-l", "remote"]},

    # Dinamarca (se ativar no PORTALS): local provavel, descubra com --help
    # "jobbank":     {"query_flag": None, "location_args": ["-l", "denmark"]},
    # "jobdanmark":  {"query_flag": None, "location_args": ["-l", "denmark"]},
    # "jobindex":    {"query_flag": None, "location_args": ["-l", "denmark"]},
    # "jobnet":      {"query_flag": None, "location_args": ["-l", "denmark"]},

    # freehire NAO usa "-l": usa "-q" p/ keywords e facet flags p/ localizacao
    "freehire":     {"query_flag": "-q", "location_args": ["--remote", "remote"]},
}

def build_cmd(name, cmd, query, fallback_loc):
    """Monta a lista de argumentos da busca conforme o PORTAL_SPEC do portal."""
    spec = PORTAL_SPEC.get(name)
    if spec is None:
        # portal sem spec: usa fallback genérico (query posicional + -l)
        return cmd + [query, "-l", fallback_loc]
    loc_args = spec["location_args"] or ["-l", fallback_loc]
    if spec["query_flag"]:
        return cmd + [spec["query_flag"], query] + loc_args
    return cmd + [query] + loc_args

def run_portal(name, cmd, query, fallback_loc):
    """Executa um portal e retorna (ok, jobs, error)."""
    full = build_cmd(name, cmd, query, fallback_loc)
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