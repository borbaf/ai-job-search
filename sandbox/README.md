# ai-job-search — Sandbox Framework

Pipeline autônomo de triagem de vagas de emprego com **custo de LLM mínimo**:
coleta via CLIs de busca (grátis), ranking com **1 chamada de modelo por lote**
e estado isolado na sandbox.

> **Filosofia:** scrape grátis (CLIs `bun`) + rank barato (1 chamada por lote)
> + leitura viva dos arquivos de perfil/rubrica. Nada de reenviar histórico
> de conversa a cada vaga.

---

## 1. Arquitetura / Fluxo

1. **`run_scrape.py`** coleta vagas via CLIs de busca (`bun run ... cli.ts search`),
   com localização ajustada por portal. Sem custo de LLM.
2. **`run_ingest.py`** soma as vagas novas no `seen_jobs.json` da raiz, marcando-as
   como `new` (visíveis ao rank). Dedup por URL — não duplica nem sobrescreve.
3. **`run_rank.py`** pontua as vagas contra o perfil e a rubrica com **1 chamada
   de modelo por lote**, agrega com pesos e apresenta shortlist limpo de vetos.

---

## 2. Estrutura de arquivos


Arquivos de contexto (lidos vivos a cada run, editáveis via agy):
- `.claude/skills/job-application-assistant/01-candidate-profile.md` — perfil
- `.claude/skills/job-application-assistant/04-job-evaluation.md` — rubrica
- `tools/rank_state.py` — estado do backlog (`candidates` / `apply` / `sweep`)
- `job_scraper/seen_jobs.json` — backlog real (estrutura `{"seen": {url: objeto}}`)

---

## 3. Pré-requisitos

- **Python 3.12+** com `requests`, `google-auth`
- **Bun** (para os CLIs de busca dos portais)
- **Credenciais GCP** com Application Default Credentials:
  ```powershell
  gcloud auth application-default login

PROJECT = "ai-job-search-borbaf"
REGION = "us"                  # multi-região (host .rep.)
MODEL = "gemini-3.8-flash"     # confirmado nos artefatos do CLI

PROFILE_FILE = r"C:\dev\ai-job-search\.claude\skills\job-application-assistant\01-candidate-profile.md"
RUBRIC_FILE  = r"C:\dev\ai-job-search\.claude\skills\job-application-assistant\04-job-evaluation.md"
RANK_STATE   = r"C:\dev\ai-job-search\tools\rank_state.py"
STATE_DIR    = r"C:\dev\ai-job-search\sandbox\state"
BATCH_SIZE   = 5

PORTALS = {
    "linkedin":     ["bun", "run", r"...\linkedin-search\cli\src\cli.ts", "search"],
    "gupy":         ["bun", "run", r"...\gupy-search\cli\src\cli.ts", "search"],
    "catho":        ["bun", "run", r"...\catho-search\cli\src\cli.ts", "search"],
    "infojobs":     ["bun", "run", r"...\infojobs-search\cli\src\cli.ts", "search"],
    "freehire":     ["bun", "run", r"...\freehire-search\cli\src\cli.ts", "search"],
    "dynamitejobs": ["bun", "run", r"...\dynamitejobs-search\cli\src\cli.ts", "search"],
    "hirelatam":    ["bun", "run", r"...\hirelatam-search\cli\src\cli.ts", "search"],
}

python sandbox\run_scrape.py "supply chain" "SC" 5

query — termo de busca
location — localização fallback (o mapa por portal sobrescreve)
limit — vagas por portal (padrão 5)
Localização por portal (em PORTAL_SPEC do run_scrape.py):

BR (gupy/catho/infojobs) → Santa Catarina
Internacionais (linkedin/dynamitejobs/hirelatam) → remote / Brazil
freehire → usa -q para keywords e --remote remote (não aceita -l)
Saída: sandbox/state/scraped_jobs.json + resumo por portal (ok/erro).

Soma as vagas novas no job_scraper/seen_jobs.json (estrutura {"seen": {url: objeto}}), marcando como new. Dedup por URL — preserva entradas existentes.

5.3 Rankear (1 chamada por lote)

python sandbox\run_rank.py --limit 10 --top 5        # só imprime
python sandbox\run_rank.py --limit 10 --top 5 --write # persiste via rank_state.py apply

--limit — vagas a pontuar (padrão 10)
--top — tamanho do shortlist (padrão 5)
--write — persiste o ranking no seen_jobs.json (padrão: só imprime)
Saída:

SHORTLIST — top-N com vetos excluídos antes; marcadores ⚠ (FLAG) e 🔥 (deadline ≤ 7 dias)
VETADOS — motivo correto por veto (LOCALIZAÇÃO / IDIOMA)
EXPIRADAS — URLs mortas / deadline passado

Custo / Controle de cota
Scrape: zero custo de LLM (CLIs bun).
Rank: 1 chamada de modelo por lote (não por vaga). BATCH_SIZE = 5 amortiza o custo; maxOutputTokens configurável via C.MAX_OUTPUT_TOKENS (padrão 32768 — evita truncamento em lotes grandes).
Para economizar cota, reduza --limit (ex.: 5) em vez de encolher o lote.

8. Notas
Perfil e rubrica são lidos vivos a cada run — edições via agy valem no próximo run, sem cópia local.
Vetos de localização/idioma seguem 04-job-evaluation.md: FAIL exclui do shortlist; FLAG mantém com marcador ⚠.
O rank é triagem (título/empresa/local), não avaliação final — o /apply continua sendo a fonte autoritativa com pesquisa de empresa.