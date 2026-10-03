import json
import subprocess
import sys

jobs_to_eval = [
    # 1. Hyundai Glovis - Logistics Data Analyst
    {"key": "https://www.linkedin.com/jobs/view/4461189128", "title": "Analista de Dados - Pleno", "company": "Hyundai Glovis Brasil Logistica", "portal": "linkedin-search"},
    # 2. Bosch Brasil - Demand & Supply Analyst
    {"key": "https://www.linkedin.com/jobs/view/4461666995", "title": "Analista de Demanda e Suprimentos PL - 35302", "company": "Bosch Brasil", "portal": "linkedin-search"},
    # 3. Ting - Supply Chain Manager (Dynamite Jobs)
    {"key": "https://dynamitejobs.com/company/ting/remote-job/supply-chain-manager", "title": "Supply Chain Manager", "company": "Ting", "portal": "dynamitejobs-search"},
    # 4. Jiga - Logistics Manager (Dynamite Jobs)
    {"key": "https://dynamitejobs.com/company/jiga/remote-job/logistics-manager-remote-anywhere", "title": "Logistics Manager - Remote/Anywhere", "company": "Jiga", "portal": "dynamitejobs-search"},
    # 5. Gruns - Director of Supply Chain (Dynamite Jobs)
    {"key": "https://dynamitejobs.com/company/gruns/remote-job/director-of-supply-chain", "title": "Director of Supply Chain", "company": "Gruns", "portal": "dynamitejobs-search"},
    # 6. Fresh Prints - Supply Chain Support Manager
    {"key": "https://job-boards.greenhouse.io/freshprints/jobs/6209508004?utm_source=freehire.me", "title": "Supply Chain Support Manager (Full Time, Remote)", "company": "Fresh Prints", "portal": "freehire-search"},
    # 7. Magic - Supply Chain Coordinator / Procurement
    {"key": "https://magic.pinpointhq.com/en/postings/d75c9e42-6335-492f-966e-d0be0a99dfa9?utm_source=freehire.me", "title": "Supply Chain Coordinator/Procurement Assistant - Freelance, Remote", "company": "Magic", "portal": "freehire-search"},
    # 8. Loggi - Analista S&OP Senior
    {"key": "https://br.linkedin.com/jobs/view/analista-s-op-s%C3%AAnior-planejamento-s%C3%A3o-paulo-sp-at-loggi-4460520582", "title": "Analista S&OP Sênior | Planejamento", "company": "Loggi", "portal": "linkedin-search"},
    # 9. Arthrex LATAM - Analista de Planejamento de Demanda Senior
    {"key": "https://br.linkedin.com/jobs/view/analista-de-planejamento-de-demanda-s%C3%AAnior-at-arthrex-latam-4466512948", "title": "Analista de Planejamento de Demanda Sênior", "company": "Arthrex LATAM", "portal": "linkedin-search"},
    # 10. GOL Linhas Aereas - Analista de Dados II
    {"key": "https://www.linkedin.com/jobs/view/4458415296", "title": "Analista de Dados II", "company": "GOL Linhas Aereas", "portal": "linkedin-search"},
    # 11. AB InBev - RTM Specialist
    {"key": "https://www.linkedin.com/jobs/view/4422748128", "title": "RTM Specialist", "company": "AB InBev", "portal": "linkedin-search"},
    # 12. Mondelez International - o9 Global Data Science
    {"key": "https://www.linkedin.com/jobs/view/4434776462", "title": "o9 Global Data Science", "company": "Mondelez International", "portal": "linkedin-search"},
    # 13. Grupo Farmax - Banco de Talentos Supply Chain
    {"key": "grupo-farmax_banco-de-talentos-supply-chain-suprimentos-e-logistica", "title": "Banco de Talentos - Supply Chain, Suprimentos e Logística", "company": "Grupo Farmax", "portal": "gupy-search"},
    # 14. EWOR GmbH - Supply Chain Chief of Staff (100% remote)
    {"key": "https://eworgmbh.teamtailor.com/jobs/8454019-supply-chain-chief-of-staff-100-remote-m-f-d?utm_source=freehire.me", "title": "Supply Chain Chief of Staff (100 % remote) (m/f/d)", "company": "EWOR GmbH", "portal": "freehire-search"},
    # 15. B. Braun - Demand Planner & Supply Chain Analyst
    {"key": "https://freehire.me/jobs/demand-planner-supply-chain-analyst-b-braun-biie2r2n", "title": "Demand Planner & Supply Chain Analyst", "company": "B. Braun", "portal": "freehire-search"}
]

print(f"Preparing batch scoring for {len(jobs_to_eval)} prioritized positions...")
