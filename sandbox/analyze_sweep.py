"""Process, filter, evaluate and ingest scraped jobs from the Tier 1-5 sweep."""
import json
import os
import re
from datetime import datetime

SEEN_PATH = r"job_scraper\seen_jobs.json"
SWEEP_PATH = r"sandbox\state\cli_sweep_results.json"

with open(SEEN_PATH, "r", encoding="utf-8") as f:
    seen_data = json.load(f)
seen_dict = seen_data.get("seen", {})

with open(SWEEP_PATH, "r", encoding="utf-8") as f:
    sweep_data = json.load(f)
raw_jobs = sweep_data.get("jobs", [])

print(f"Total raw jobs collected: {len(raw_jobs)}")
print(f"Total existing in seen_jobs.json: {len(seen_dict)}")

# Filter criteria aligned with the updated rubrics
RELEVANT_KEYWORDS = [
    "supply chain", "logistics", "logística", "s&op", "sop", "demand plan",
    "operations", "operações", "transport", "freight", "wms", "tms",
    "fleet", "frota", "procurement", "compras", "inventory", "estoque",
    "materials", "suprimentos", "control tower", "torre de controle",
    "warehouse", "distribution", "distribuição", "business intelligence",
    "bi analyst", "data analyst"
]

EXCLUDE_TITLES = [
    "junior data analyst", "analista de dados júnior", "junior data scientist",
    "react", "frontend", "front-end", "backend", "back-end", "full stack", "fullstack",
    "ios", "android", "flutter", "devops", "qa engineer", "scrum master",
    "accountant", "accounting", "dentist", "nurse", "sales executive",
    "content writer", "copywriter", "graphic designer", "clinical", "security guard",
    "penetration tester", "legal counsel", "hr recruiter", "recruitment", "talent acquisition"
]

def is_relevant(title, desc=""):
    t = (title or "").lower()
    d = (desc or "").lower()
    full = t + " " + d

    # Strict anti-pattern check
    for exc in EXCLUDE_TITLES:
        if exc in t:
            return False

    # Positive match check
    for kw in RELEVANT_KEYWORDS:
        if kw in full:
            return True
    return False

def classify_sweet_spot(title, desc=""):
    t = (title or "").lower()
    if any(k in t for k in ["s&op", "demand plan", "supply chain analyst", "logistics analyst", "bi ", "business intelligence", "supply chain data"]):
        return "Sweet Spot 1: Supply Chain Analytics, S&OP & BI"
    if any(k in t for k in ["product owner", "product manager", "tms", "wms", "fleet"]):
        return "Sweet Spot 2: Logistics Tech & Fleet Management"
    if any(k in t for k in ["manager", "gerente", "coordenador", "director", "head", "lead"]):
        return "Sweet Spot 3: Supply Chain & Operations Leadership"
    return "Operations & Analytics Adjacent"

def classify_hiring_model(portal, company=""):
    p = (portal or "").lower()
    c = (company or "").lower()
    if "hirelatam" in p or "hirelatam" in c:
        return "Staff Augmentation (HireLATAM -> US Client)"
    if any(k in c for k in ["staffing", "recruitment", "talents", "bairesdev", "turing", "solvo"]):
        return "Staff Augmentation (Agency/Staffing)"
    return "Direct Hire (Client)"

filtered_jobs = []
new_jobs = []
already_seen_jobs = []

for j in raw_jobs:
    title = j.get("title", "")
    desc = j.get("description", "") or ""
    url = j.get("url") or j.get("link") or j.get("id")
    portal = j.get("source_portal", "")

    if not is_relevant(title, desc):
        continue

    category = classify_sweet_spot(title, desc)
    hiring_model = classify_hiring_model(portal, j.get("company", ""))

    job_record = {
        "title": title,
        "company": j.get("company", "Unknown"),
        "location": j.get("location", "Remote"),
        "url": url,
        "portal": portal,
        "tier": j.get("tier", "Unclassified"),
        "category": category,
        "hiring_model": hiring_model,
        "date": j.get("date"),
        "description": desc[:300] if desc else None
    }

    filtered_jobs.append(job_record)

    if url in seen_dict:
        already_seen_jobs.append(job_record)
    else:
        new_jobs.append(job_record)

print(f"\nFiltered relevant jobs: {len(filtered_jobs)}")
print(f"Already seen: {len(already_seen_jobs)}")
print(f"Brand new: {len(new_jobs)}")

# Ingest new jobs into seen_jobs.json
for nj in new_jobs:
    url = nj["url"]
    if not url:
        continue
    seen_dict[url] = {
        "title": nj["title"],
        "company": nj["company"],
        "url": url,
        "first_seen": datetime.now().strftime("%Y-%m-%d"),
        "posted_date": nj.get("date"),
        "deadline": None,
        "fit": None,
        "status": "new",
        "portal": nj["portal"],
        "tier": nj["tier"],
        "category": nj["category"],
        "hiring_model": nj["hiring_model"],
        "ingested_at": datetime.now().isoformat()
    }

with open(SEEN_PATH, "w", encoding="utf-8") as f:
    json.dump(seen_data, f, ensure_ascii=False, indent=2)

print(f"Updated seen_jobs.json - Total jobs now: {len(seen_dict)}")

# Save report data
report_path = r"sandbox\state\sweep_report.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "total_filtered": len(filtered_jobs),
        "total_new": len(new_jobs),
        "total_seen": len(already_seen_jobs),
        "new_jobs": new_jobs,
        "already_seen": already_seen_jobs
    }, f, ensure_ascii=False, indent=2)

print(f"Saved analysis report to {report_path}")
