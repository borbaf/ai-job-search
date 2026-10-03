"""Script to select the top 15 most adherent unranked jobs, score them, and persist the results."""
import json
import re
import subprocess
import sys
from datetime import datetime

SEEN_PATH = r"job_scraper\seen_jobs.json"
with open(SEEN_PATH, "r", encoding="utf-8") as f:
    doc = json.load(f)
seen = doc.get("seen", {})

new_jobs = [(k, v) for k, v in seen.items() if v.get("status") == "new"]
print(f"Total unranked ('new') jobs: {len(new_jobs)}")

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
    "analista de logística": 25,
    "logistics analyst": 25,
    "product owner": 25,
    "tms": 22,
    "wms": 22,
    "supply chain manager": 22,
    "gerente de supply chain": 22,
    "coordenador de supply chain": 22,
    "planejamento supply chain": 25,
    "logistics manager": 20,
    "fleet": 18,
    "frota": 18,
    "suprimentos": 15,
    "supply chain": 18,
    "logística": 15,
    "logistics": 15,
    "bi analyst": 15,
    "data analyst": 10
}

anti_patterns = [
    "jr", "júnior", "junior", "estágio", "intern", "trainee", "entry level",
    "react", "frontend", "front-end", "backend", "full stack", "fullstack",
    "dentist", "nurse", "graphic designer", "accountant", "hr recruiter"
]

scored_candidates = []
for k, j in new_jobs:
    title = (j.get("title") or "").lower()
    desc = (j.get("description") or "").lower()
    full = title + " " + desc

    # Skip anti-patterns
    if any(re.search(r"\b" + re.escape(ap) + r"\b", title) for ap in anti_patterns):
        continue

    score = 0
    for kw, pts in keywords_weights.items():
        if kw in title:
            score += pts
        elif kw in desc:
            score += pts // 2

    portal = (j.get("portal") or "").lower()
    if any(p in portal for p in ["hirelatam", "dynamitejobs"]):
        score += 8  # Priority Tiers bonus
    elif "remote" in (j.get("location") or "").lower() or j.get("work_mode") == "remote":
        score += 5

    # Location heuristic check: penalize obvious distant on-site
    loc = (j.get("location") or "").lower()
    if any(bad in loc for bad in ["são paulo", "sao paulo", "belo horizonte", "curitiba", "porto alegre", "blumenau", "campinas"]):
        score -= 15

    if score > 0:
        scored_candidates.append((score, k, j))

scored_candidates.sort(key=lambda x: x[0], reverse=True)

print(f"\nTotal potential candidates: {len(scored_candidates)}")
top15 = scored_candidates[:15]

print("\n--- TOP 15 SELECTED FOR IN-DEPTH RANKING ---")
for idx, (s, k, j) in enumerate(top15, 1):
    print(f"{idx}. [{s} pts] {j.get('portal')} | {j.get('title')} @ {j.get('company')} ({j.get('location')})")
    print(f"   Key/URL: {k}")

# Save the top 15 selection to a state file
with open(r"sandbox\state\top15_selected.json", "w", encoding="utf-8") as f:
    json.dump([{"adherence_pts": s, "key": k, "job": j} for s, k, j in top15], f, ensure_ascii=False, indent=2)
