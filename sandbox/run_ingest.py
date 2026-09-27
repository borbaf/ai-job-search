"""Ingestão da sandbox: SOMA as vagas do scraped_jobs.json no seen_jobs.json da raiz.

Estrutura confirmada do seen_jobs.json:
  { "seen": { "<url da vaga>": { "title":..., "company":..., "url":..., "status":... } } }

- A CHAVE do dict é a URL completa da vaga (não um slug).
- Dedup por URL (vagas já presentes NÃO são duplicadas nem sobrescritas).
- Novas entram com status "new" (o que o /rank enxerga como candidato).
- Entradas existentes (ranked/skipped/applied) são preservadas intactas.

Uso:
  python sandbox/run_ingest.py
"""
import json, os, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
import config as C

# Caminho do estado da raiz (onde o /rank lê).
SEEN_JOBS = r"C:\dev\ai-job-search\job_scraper\seen_jobs.json"

# Chave de topo que contém o mapa de vagas (confirmada: "seen").
CONTAINER_KEY = "seen"

def main():
    scraped_path = os.path.join(C.STATE_DIR, "scraped_jobs.json")
    if not os.path.exists(scraped_path):
        print(f"ERRO: {scraped_path} não existe. Rode run_scrape.py primeiro.")
        sys.exit(1)
    with open(scraped_path, encoding="utf-8") as f:
        scraped = json.load(f)

    if not os.path.exists(SEEN_JOBS):
        print(f"ERRO: {SEEN_JOBS} não existe. Ajuste SEEN_JOBS no script.")
        sys.exit(1)
    with open(SEEN_JOBS, encoding="utf-8") as f:
        seen = json.load(f)

    if not isinstance(seen, dict) or CONTAINER_KEY not in seen:
        print(f"ERRO: estrutura inesperada. Esperava dict com chave '{CONTAINER_KEY}'.")
        print("Chaves encontradas:", list(seen.keys()) if isinstance(seen, dict) else type(seen).__name__)
        sys.exit(1)

    container = seen[CONTAINER_KEY]
    if not isinstance(container, dict):
        print(f"ERRO: '{CONTAINER_KEY}' não é dict (é {type(container).__name__}).")
        sys.exit(1)

    added = 0
    for j in scraped.get("jobs", []):
        # A chave do seen_jobs.json é a URL completa da vaga.
        key = j.get("url") or j.get("link") or j.get("key") or j.get("id")
        if not key or key in container:
            continue
        entry = {
            "title": j.get("title"),
            "company": j.get("company"),
            "url": j.get("url") or j.get("link"),
            "first_seen": datetime.now().strftime("%Y-%m-%d"),
            "posted_date": j.get("posted_date"),
            "deadline": j.get("deadline"),
            "fit": None,
            "status": "new",
            "portal": j.get("portal"),
            "ingested_at": datetime.now().isoformat(),
        }
        container[key] = entry
        added += 1

    with open(SEEN_JOBS, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)

    print(f"Adicionadas: {added} novas vagas (status 'new')")
    print(f"Total no seen_jobs.json: {len(container)}")

if __name__ == "__main__":
    main()