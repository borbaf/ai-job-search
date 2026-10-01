"""Configuracao central do sandbox framework. Edite apenas aqui.

Caminhos dos CLIs seguem o padrao .agents/skills/<portal>-search/cli/src/cli.ts.
Somente portais COM CLI instalado devem ficar ativos no PORTALS.
"""
PROJECT = "ai-job-search-borbaf"
REGION = "us"                  # multi-regiao (host .rep.)
MODEL = "gemini-3.8-flash"     # confirmado nos artefatos do CLI

# --- Arquivos lidos vivos a cada run (edicoes via agy valem no proximo run) ----
PROFILE_FILE = r"C:\dev\ai-job-search\.claude\skills\job-application-assistant\01-candidate-profile.md"
RUBRIC_FILE  = r"C:\dev\ai-job-search\.claude\skills\job-application-assistant\04-job-evaluation.md"
RANK_STATE   = r"C:\dev\ai-job-search\tools\rank_state.py"
STATE_DIR    = r"C:\dev\ai-job-search\sandbox\state"

# --- Controle de cota / lote ------------------------------------------------
BATCH_SIZE = 5                 # vagas por lote no rank (1 chamada Vertex por lote)
MAX_OUTPUT_TOKENS = 32768      # evita truncamento em lotes grandes

# --- Portais com CLI INSTALADO (confirmado via dir .agents\skills) -----------
# Ajuste apenas o caminho real se algum divergir.
PORTALS = {
    "linkedin":     ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\linkedin-search\cli\src\cli.ts", "search"],
    "gupy":         ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\gupy-search\cli\src\cli.ts", "search"],
    "catho":        ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\catho-search\cli\src\cli.ts", "search"],
    "infojobs":     ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\infojobs-search\cli\src\cli.ts", "search"],
    "freehire":     ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\freehire-search\cli\src\cli.ts", "search"],
    "dynamitejobs": ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\dynamitejobs-search\cli\src\cli.ts", "search"],
    "hirelatam":    ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\hirelatam-search\cli\src\cli.ts", "search"],

    # Instalados mas fora do escopo geografico atual (Dinamarca). Ative
    # descomentando se quiser alcance DK (o rank vetara por localizacao).
    "jobbank":      ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\jobbank-search\cli\src\cli.ts", "search"],
    "jobdanmark":   ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\jobdanmark-search\cli\src\cli.ts", "search"],
    "jobindex":     ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\jobindex-search\cli\src\cli.ts", "search"],
    "jobnet":       ["bun", "run", r"C:\dev\ai-job-search\.agents\skills\jobnet-search\cli\src\cli.ts", "search"],
}