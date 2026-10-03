"""Sweep installed portal CLIs for Tiers 1-2 and general aggregators."""
import json
import subprocess
import os
import sys
from datetime import datetime

JOBS_SCRAPED = []

def run_cmd(cmd_list):
    try:
        p = subprocess.run(cmd_list, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if p.returncode == 0:
            return json.loads(p.stdout)
    except Exception as e:
        print(f"Error running {cmd_list[:4]}: {e}")
    return None

# 1. HireLATAM (Tier 1)
print("--> Sweeping HireLATAM (Tier 1)...")
hirelatam_queries = ["supply chain", "logistics", "operations", "data analyst", "analytics"]
hirelatam_seen = set()
for q in hirelatam_queries:
    data = run_cmd(["bun", "run", r".agents\skills\hirelatam-search\cli\src\cli.ts", "search", "--query", q, "--format", "json"])
    if data and "results" in data:
        for j in data["results"]:
            jid = j.get("id")
            if jid and jid not in hirelatam_seen:
                hirelatam_seen.add(jid)
                j["tier"] = "Tier 1: LATAM & Global"
                j["source_portal"] = "hirelatam"
                JOBS_SCRAPED.append(j)

print(f"    HireLATAM found: {len(hirelatam_seen)} jobs")

# 2. Dynamite Jobs (Tier 2)
print("--> Sweeping Dynamite Jobs (Tier 2)...")
dj_queries = ["supply chain", "logistics", "operations", "S&OP", "product manager"]
dj_seen = set()
for q in dj_queries:
    data = run_cmd(["bun", "run", r".agents\skills\dynamitejobs-search\cli\src\cli.ts", "search", "-q", q, "--format", "json"])
    if data and "results" in data:
        for j in data["results"]:
            jid = j.get("id")
            if jid and jid not in dj_seen:
                dj_seen.add(jid)
                j["tier"] = "Tier 2: Global Remote"
                j["source_portal"] = "dynamitejobs"
                JOBS_SCRAPED.append(j)

print(f"    Dynamite Jobs found: {len(dj_seen)} jobs")

# 3. FreeHire (Global Tech & Data Aggregator)
print("--> Sweeping FreeHire (Global Tech Aggregator)...")
freehire_queries = ["supply chain", "logistics", "S&OP"]
freehire_seen = set()
for q in freehire_queries:
    data = run_cmd(["bun", "run", r".agents\skills\freehire-search\cli\src\cli.ts", "search", "-q", q, "--remote", "--format", "json"])
    if data and "results" in data:
        for j in data["results"]:
            jid = j.get("id") or j.get("url")
            if jid and jid not in freehire_seen:
                freehire_seen.add(jid)
                j["tier"] = "Aggregator: Global Tech"
                j["source_portal"] = "freehire"
                JOBS_SCRAPED.append(j)

print(f"    FreeHire found: {len(freehire_seen)} jobs")

# 4. Gupy (Brazil Remote)
print("--> Sweeping Gupy (Brazil Remote)...")
gupy_queries = ["supply chain", "logistica", "S&OP", "torre de controle", "planejamento demanda", "product owner logistica"]
gupy_seen = set()
for q in gupy_queries:
    data = run_cmd(["bun", "run", r".agents\skills\gupy-search\cli\src\cli.ts", "search", "-q", q, "--remote", "--limit", "15", "--format", "json"])
    if data and "results" in data:
        for j in data["results"]:
            jid = j.get("id")
            if jid and jid not in gupy_seen:
                gupy_seen.add(jid)
                j["tier"] = "Aggregator: Brazil Remote (Gupy)"
                j["source_portal"] = "gupy"
                JOBS_SCRAPED.append(j)

print(f"    Gupy found: {len(gupy_seen)} jobs")

# 5. LinkedIn CLI (Remote)
print("--> Sweeping LinkedIn Remote...")
linkedin_queries = [
    ("Supply Chain Analyst", "Remote"),
    ("Logistics Data Analyst", "Remote"),
    ("S&OP Analyst", "Remote"),
    ("Supply Chain Manager", "Remote")
]
linkedin_seen = set()
for q, loc in linkedin_queries:
    data = run_cmd(["bun", "run", r".agents\skills\linkedin-search\cli\src\cli.ts", "search", "-q", q, "-l", loc, "--remote", "remote", "--jobage", "14", "--limit", "10", "--format", "json"])
    if data and "results" in data:
        for j in data["results"]:
            jid = j.get("id") or j.get("url")
            if jid and jid not in linkedin_seen:
                linkedin_seen.add(jid)
                j["tier"] = "Tier 1/2: LinkedIn Remote"
                j["source_portal"] = "linkedin"
                JOBS_SCRAPED.append(j)

print(f"    LinkedIn found: {len(linkedin_seen)} jobs")

out_file = r"sandbox\state\cli_sweep_results.json"
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({"timestamp": datetime.now().isoformat(), "total": len(JOBS_SCRAPED), "jobs": JOBS_SCRAPED}, f, ensure_ascii=False, indent=2)

print(f"\nTotal CLI sweep jobs collected: {len(JOBS_SCRAPED)}")
