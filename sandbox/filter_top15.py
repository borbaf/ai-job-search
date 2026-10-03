import json
import re

SEEN_PATH = r"job_scraper\seen_jobs.json"
with open(SEEN_PATH, "r", encoding="utf-8") as f:
    doc = json.load(f)
seen = doc.get("seen", {})

new_jobs = [(k, v) for k, v in seen.items() if v.get("status") == "new"]

keywords_weights = {
    "s&op": 30,
    "sop": 25,
    "demand plan": 30,
    "planejamento de demanda": 30,
    "torre de controle": 30,
    "control tower": 30,
    "supply chain analyst": 28,
    "supply chain analytics": 28,
    "supply chain data": 28,
    "analista de supply chain": 26,
    "analista de logistica": 25,
    "logistics analyst": 25,
    "product owner": 25,
    "tms": 22,
    "wms": 22,
    "supply chain manager": 22,
    "gerente de supply chain": 22,
    "coordenador de supply chain": 22,
    "logistics manager": 20,
    "fleet": 18,
    "frota": 18,
    "suprimentos": 15,
    "supply chain": 18,
    "logistica": 15,
    "logistics": 15,
    "bi analyst": 15,
    "data analyst": 10
}

anti_patterns = ["jr", "junior", "estagio", "intern", "trainee", "react", "frontend", "dentist", "nurse"]

def is_remote_or_sc(j):
    loc = (j.get("location") or "").lower()
    title = (j.get("title") or "").lower()
    desc = (j.get("description") or "").lower()
    work_mode = (j.get("work_mode") or "").lower()
    portal = (j.get("portal") or "").lower()
    
    if work_mode == "remote":
        return True
    if any(r in loc for r in ["remote", "remoto", "teletrabalho", "anywhere", "latin america", "latam"]):
        return True
    if any(r in title for r in ["remote", "remoto"]):
        return True
    if "hirelatam" in portal or "dynamitejobs" in portal:
        return True
    if any(sc in loc for sc in ["santa catarina", "florianopolis", "florianópolis", "itajai", "itajaí", "joinville", "navegantes"]):
        return True
    return False

eligible = []
for k, j in new_jobs:
    title = (j.get("title") or "").lower()
    # Check anti-patterns
    if any(re.search(r"\b" + re.escape(ap) + r"\b", title) for ap in anti_patterns):
        continue
    if not is_remote_or_sc(j):
        continue
    score = 0
    full = title + " " + (j.get("description") or "").lower()
    for kw, pts in keywords_weights.items():
        if kw in title:
            score += pts
        elif kw in full:
            score += pts // 2
    if score > 0:
        eligible.append((score, k, j))

eligible.sort(key=lambda x: x[0], reverse=True)

with open(r"sandbox\state\top15_filtered.json", "w", encoding="utf-8") as f:
    json.dump([{"score": s, "key": k, "job": j} for s, k, j in eligible[:15]], f, ensure_ascii=False, indent=2)

print(f"Total eligible remote/SC jobs found: {len(eligible)}")
for idx, (s, k, j) in enumerate(eligible[:15], 1):
    print(f"{idx}. [{s} pts] {j.get('portal')} | {j.get('title')} @ {j.get('company')} ({j.get('location')})")
    print(f"   URL: {j.get('url') or k}")
