"""Ingestão da sandbox: SOMA as vagas do scraped_jobs.json no seen_jobs.json da raiz.

- Dedup por key (vagas já presentes NÃO são duplicadas nem sobrescritas).
- Novas entram com status "new" (o que o /rank enxerga como candidato).
- Entradas existentes (ranked/skipped/applied) são preservadas intactas.
- Estrutura suportada: {"seen": [ ... ]} (confirmada no seu seen_jobs.json).

Uso:
  python sandbox/run_ingest.py
"""
import json, os, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
import config as C

# Caminho do estado da raiz (onde o /rank lê).
SEEN_JOBS = r"C:\dev\ai-job-search\job_scraper\seen_jobs.json"

# Chave de topo que contém a lista de vagas no seen_jobs.json (confirmada: "seen").
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

    # Estrutura: dict com a lista sob CONTAINER_KEY. Preserva os demais metadados.
    if not isinstance(seen, dict) or CONTAINER_KEY not in seen:
        print(f"ERRO: estrutura inesperada. Esperava dict com chave '{CONTAINER_KEY}'.")
        print("Chaves encontradas:", list(seen.keys()) if isinstance(seen, dict) else type(seen).__name__)
        sys.exit(1)

    jobs_container = seen[CONTAINER_KEY]
    meta = {k: v for k, v in seen.items() if k != CONTAINER_KEY}

    existing = {j.get("key") for j in jobs_container if j.get("key")}
    added = 0
    for j in scraped.get("jobs", []):
        key = j.get("key") or j.get("id") or j.get("slug")
        if not key or key in existing:
            continue
        entry = {
            "key": key,
            "title": j.get("title"),
            "company": j.get("company"),
            "url": j.get("url") or j.get("link"),
            "portal": j.get("portal"),
            "deadline": j.get("deadline"),
            "posted_date": j.get("posted_date"),
            "status": "new",
            "ingested_at": datetime.now().isoformat(),
        }
        jobs_container.append(entry)
        existing.add(key)
        added += 1

    seen[CONTAINER_KEY] = jobs_container
    seen.update(meta)

    with open(SEEN_JOBS, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)

    print(f"Adicionadas: {added} novas vagas (status 'new')")
    print(f"Total no seen_jobs.json: {len(jobs_container)}")

if __name__ == "__main__":
    main()