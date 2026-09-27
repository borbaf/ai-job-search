"""Rank autônomo da sandbox: pontua as vagas com UMA chamada Vertex por lote,
sem reenviar histórico. Lê PERFIL e RUBRICA ORIGINAIS a cada execução — edições
feitas via agy valem no próximo run automaticamente.

Uso:
  python sandbox/run_rank.py --limit 5 --top 3           # só imprime
  python sandbox/run_rank.py --limit 5 --top 3 --write   # persiste via rank_state.py apply
"""
import json, os, sys, argparse, subprocess, re, tempfile
from datetime import date, timedelta

# Console Windows: força UTF-8 para não quebrar em caracteres de substituição
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(__file__))
import config as C

import google.auth
import google.auth.transport.requests
import requests

WEIGHTS = {"technical": 0.30, "experience": 0.25, "behavioral": 0.15, "career": 0.30}
URGENT_DAYS = 7
# Saída grande (10 vagas x strengths/gaps) estoura 8192 — subimos e deixamos configurável
MAX_OUTPUT_TOKENS = getattr(C, "MAX_OUTPUT_TOKENS", 32768)

def get_token():
    creds, _ = google.auth.default()
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token

def call_vertex(prompt):
    url = (f"https://aiplatform.{C.REGION}.rep.googleapis.com/v1/projects/{C.PROJECT}"
           f"/locations/{C.REGION}/publishers/google/models/{C.MODEL}:generateContent")
    headers = {"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"}
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": MAX_OUTPUT_TOKENS},
    }
    r = requests.post(url, headers=headers, json=body, timeout=180)
    if r.status_code != 200:
        print("HTTP", r.status_code)
        print(r.text[:3000])
        r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

def get_candidates(limit):
    cmd = [sys.executable, C.RANK_STATE, "candidates", "--limit", str(limit)]
    out = subprocess.run(cmd, capture_output=True, text=True,
                         encoding="utf-8", errors="replace",
                         cwd=os.path.dirname(C.RANK_STATE))
    if out.returncode != 0:
        print("ERRO no rank_state:", (out.stderr or "")[-800:]); sys.exit(1)
    return out.stdout

def extract_json_array(text):
    """Extrai e valida o JSON array da resposta do modelo de forma robusta.
    Remove markdown fences, apara o array, tolera trailing commas e
    DETECTA truncamento (resposta cortada no limite de tokens)."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        print("ERRO: resposta sem array JSON:\n", text[:800]); sys.exit(1)
    chunk = text[start:end + 1]
    chunk = re.sub(r",\s*([}\]])", r"\1", chunk)
    try:
        return json.loads(chunk)
    except json.JSONDecodeError as e:
        tail = chunk[-120:]
        if not chunk.rstrip().endswith("]"):
            print("ERRO: JSON incompleto — resposta provavelmente TRUNCADA no "
                  f"limite de saída ({MAX_OUTPUT_TOKENS} tokens).\n"
                  f"Fim do trecho:\n{tail}\n"
                  "Sugestão: reduza --limit (ex.: 5) ou aumente MAX_OUTPUT_TOKENS no config.py.")
        else:
            print(f"ERRO: JSON inválido após limpeza ({e}).\nTrecho:\n{chunk[:1500]}")
        sys.exit(1)

def persist(results):
    fd, tmp = tempfile.mkstemp(suffix=".json", prefix="rank_results_", dir=C.STATE_DIR)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False)
    cmd = [sys.executable, C.RANK_STATE, "apply", "--results", tmp]
    out = subprocess.run(cmd, capture_output=True, text=True,
                         encoding="utf-8", errors="replace",
                         cwd=os.path.dirname(C.RANK_STATE))
    print(out.stdout[-2500:] if out.stdout else (out.stderr or "")[-800:])
    if os.path.exists(tmp):
        os.remove(tmp)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--write", action="store_true",
                    help="persiste via rank_state.py apply; padrão é só imprimir")
    args = ap.parse_args()

    os.makedirs(C.STATE_DIR, exist_ok=True)

    print("== Carregando candidatos (rank_state.py candidates) ==")
    cands = get_candidates(args.limit)
    print(cands[:1500])

    print("\n== Lendo PERFIL e RUBRICA ORIGINAIS (uma vez por run) ==")
    with open(C.PROFILE_FILE, encoding="utf-8") as f: profile = f.read()
    with open(C.RUBRIC_FILE, encoding="utf-8") as f:  rubric  = f.read()
    print(f"perfil : {C.PROFILE_FILE}\nrubrica: {C.RUBRIC_FILE}")

    prompt = f"""Você é um avaliador de fit de vagas (triage). Pontue cada vaga do lote contra o perfil e a rubrica abaixo.

RUBRICA (pesos: Technical 30%, Experience 25%, Behavioral 15%, Career 30%):
{rubric}

PERFIL DO CANDIDATO:
{profile}

Vagas do lote (JSON):
{cands}

Regras:
- Use APENAS as informações fornecidas acima (título, empresa, local). Não invente conteúdo do anúncio.
- Retorne UM ÚNICO JSON array, um objeto por vaga, no formato exato:
  {{"key": "<key>", "status": "scored"|"expired", "scores": {{"technical": 0-100, "experience": 0-100, "behavioral": 0-100, "career": 0-100}}, "location_verdict": "PASS"|"FAIL"|"FLAG", "location_note": "<motivo>", "language_gate": "PASS"|"FAIL"|"FLAG", "language_note": "<só se FLAG/FAIL>", "deadline": "YYYY-MM-DD"|null, "strengths": ["1-2 bullets curtos"], "gaps": ["1-2 bullets curtos"], "language": "<idioma do anúncio>"}}
- SEJA CONCISO: strengths/gaps com NO MÁXIMO 2 bullets curtos cada. Não repita o perfil.
- location_verdict: FAIL = fora das localizações aceitas (SP, BH, Curitiba, Blumenau NÃO são viáveis); FLAG = presencial no exterior com sponsorship; PASS = remoto / SC até ~80km de Bombinhas / Fortaleza.
- language_gate: FAIL = exige idioma não declarado no perfil (ex.: espanhol como requisito de trabalho); FLAG = nível declarado abaixo do exigido; PASS = ok.
- "expired" apenas se a URL estiver morta; caso contrário, "scored".
Responda SOMENTE o JSON, SEM texto antes ou depois, e SEMPRE fechando o array com ]."""

    print(f"\n== Chamando {C.MODEL} (UMA chamada por lote; maxOutputTokens={MAX_OUTPUT_TOKENS}) ==")
    text = call_vertex(prompt)

    results = extract_json_array(text)

    ranked, vetoed, expired = [], [], []
    for j in results:
        if j.get("status") == "expired":
            expired.append(j); continue
        s = j.get("scores") or {}
        total = (0.30 * s.get("technical", 0) + 0.25 * s.get("experience", 0)
               + 0.15 * s.get("behavioral", 0) + 0.30 * s.get("career", 0))
        if j.get("location_verdict") == "FAIL" or j.get("language_gate") == "FAIL":
            vetoed.append((total, j))
        else:
            ranked.append((total, j))
    ranked.sort(key=lambda x: x[0], reverse=True)

    today = date.today()
    def markers(j):
        f = ""
        if j.get("location_verdict") == "FLAG" or j.get("language_gate") == "FLAG":
            f += " ⚠"
        dl = j.get("deadline")
        if dl:
            try:
                d = date.fromisoformat(dl)
                if today <= d <= today + timedelta(days=URGENT_DAYS):
                    f += " 🔥"
            except ValueError:
                pass
        return f

    print(f"\n== SHORTLIST (top {args.top}; vetos EXCLUÍDOS antes do top) ==")
    if not ranked:
        print("(nenhuma vaga passou nos vetos de localização/idioma neste lote)")
    else:
        for total, j in ranked[:args.top]:
            print(f"{total:5.1f}  {j['key']}{markers(j)}")

    print(f"\n== VETADOS ({len(vetoed)}) ==")
    for total, j in sorted(vetoed, key=lambda x: x[0], reverse=True):
        motivos = []
        if j.get("location_verdict") == "FAIL":
            motivos.append(f"LOCALIZAÇÃO: {j.get('location_note') or '<sem motivo>'}")
        if j.get("language_gate") == "FAIL":
            motivos.append(f"IDIOMA: {j.get('language_note') or '<sem motivo>'}")
        print(f"{total:5.1f}  {j['key']} — {'; '.join(motivos)}")

    if expired:
        print(f"\n== EXPIRADAS ({len(expired)}) ==")
        for j in expired:
            print(f"- {j['key']}")

    if args.write:
        print("\n== Persistindo via rank_state.py apply ==")
        persist([j for _, j in ranked] + [j for _, j in vetoed] + expired)
    else:
        print("\n(dica: rode com --write quando quiser persistir no seen_jobs.json da raiz)")

if __name__ == "__main__":
    main()