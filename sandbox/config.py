# ===== CONFIG DA SANDBOX =====
# Edite apenas esta seção. Tudo aqui é isolado do framework principal.

PROJECT = "ai-job-search-borbaf"
REGION = "us-east5"          # mesma região do seu billing
MODEL = "gemini-3.8-flash"   # mantém o 3.8 (mesmo preço dos outros Flash)

# Caminhos ABSOLUTOS dos arquivos de perfil e rubrica (leia uma vez só)
PROFILE_FILE = r"C:\dev\ai-job-search\.claude\skills\job-application-assistant\01-candidate-profile.md"
RUBRIC_FILE  = r"C:\dev\ai-job-search\.claude\skills\job-application-assistant\04-job-evaluation.md"

# Estado ISOLADO da sandbox (não é o da raiz)
STATE_DIR = r"C:\dev\ai-job-search\sandbox\state"

# Tamanho do lote por chamada (mantenha ~5 para amortizar o custo)
BATCH_SIZE = 5

# Portais -> comando bun de busca. AJUSTE o caminho real de cada cli.ts.
# Portais -> comando bun de busca. Caminhos reais confirmados (com sufixo -search).
PORTALS = {
    "linkedin":     ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\linkedin-search\cli\src\cli.ts", "search"],
    "gupy":         ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\gupy-search\cli\src\cli.ts", "search"],
    "catho":        ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\catho-search\cli\src\cli.ts", "search"],
    "infojobs":     ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\infojobs-search\cli\src\cli.ts", "search"],
    "freehire":     ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\freehire-search\cli\src\cli.ts", "search"],
    "dynamitejobs": ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\dynamitejobs-search\cli\src\cli.ts", "search"],
    "hirelatam":    ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\hirelatam-search\cli\src\cli.ts", "search"],
    "jobindex":     ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\jobindex-search\cli\src\cli.ts", "search"],
    "jobnet":       ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\jobnet-search\cli\src\cli.ts", "search"],
    "jobdanmark":   ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\jobdanmark-search\cli\src\cli.ts", "search"],
    "jobbank":      ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\jobbank-search\cli\src\cli.ts", "search"],
}
# =============================