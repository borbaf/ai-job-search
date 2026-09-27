"""Teste integrado da sandbox: executa o pipeline completo scrape -> ingest -> rank
e valida cada etapa antes de seguir. Se qualquer etapa falhar, para no ponto exato.

Uso:
  python sandbox/run_all.py                     # usa dados de scrape existentes
  python sandbox/run_all.py --scrape            # roda o scrape antes (coleta nova)
  python sandbox/run_all.py --scrape --limit 10 --top 5
"""
import os, sys, subprocess, json, argparse

sys.path.insert(0, os.path.dirname(__file__))
import config as C

SEEN_JOBS = r"C:\dev\ai-job-search\job_scraper\seen_jobs.json"

def run(step, cmd):
    print(f"\n{'='*64}\n== {step}\n{'='*64}")
    out = subprocess.run(cmd, capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    print(out.stdout)
    if out.returncode != 0:
        print(f"[FALHOU] {step}\n{(out.stderr or '')[-800:]}")
        sys.exit(1)
    return out.stdout

def validate_scrape():
    p = os.path.join(C.STATE_DIR, "scraped_jobs.json")
    if not os.path.exists(p):
        print("[VALIDACAO] scraped_jobs.json ausente"); return False
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    n = len(d.get("jobs", []))
    print(f"[VALIDACAO] scrape: {n} vagas")
    return n > 0

def validate_ingest():
    if not os.path.exists(SEEN_JOBS):
        print("[VALIDACAO] seen_jobs.json ausente"); return False
    with open(SEEN_JOBS, encoding="utf-8") as f:
        d = json.load(f)
    n = len(d.get("seen", {}))
    print(f"[VALIDACAO] ingest: {n} vagas no seen_jobs.json")
    return n > 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scrape", action="store_true",
                    help="roda o scrape antes (sem ele, usa dados existentes)")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    py = sys.executable

    # 1) SCRAPE (opcional)
    if args.scrape:
        run("SCRAPE", [py, os.path.join(base, "run_scrape.py"), "supply chain", "SC", "5"])
    if not validate_scrape():
        print("\nSem dados de scrape. Rode com --scrape para coletar primeiro.")
        sys.exit(1)

    # 2) INGEST (soma no seen_jobs.json)
    run("INGEST", [py, os.path.join(base, "run_ingest.py")])
    validate_ingest()

    # 3) RANK (1 chamada por lote)
    run("RANK", [py, os.path.join(base, "run_rank.py"),
                 "--limit", str(args.limit), "--top", str(args.top)])

    print(f"\n{'='*64}\nTESTE INTEGRADO CONCLUÍDO: scrape -> ingest -> rank OK\n{'='*64}")

if __name__ == "__main__":
    main()