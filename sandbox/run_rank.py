"""Rank autônomo da sandbox: pontua as vagas com UMA chamada por lote,
sem reenviar histórico de conversa. Usa cache de contexto no perfil/rubrica."""
import json, os, sys, argparse, subprocess, re
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
import config as C

import google.auth
import google.auth.transport.requests
import requests

# ---------- helpers ----------
def get_token():
    creds, _ = google.auth.default()
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token

def call_vertex(prompt):
    url = (f"https://{C.REGION}-aiplatform.googleapis.com/v1/projects/{C.PROJECT}"
           f"/locations/{C.REGION}/publishers/google/models/{C.MODEL}:generateContent")
    headers = {"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"}
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 8192},
    }
    r = requests.post(url, headers=headers, json=body)
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_candidates(limit):
    # usa o rank_state.py da raiz, mas grava em estado da sandbox
    cmd = [sys.executable, C.RANK_STATE, "candidates", "--limit", str(limit)]
    out = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(C.RANK_STATE))
    return out.stdout

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    os.makedirs(C.STATE_DIR, exist_ok=True)

    print("== Carregando candidatos (estado da sandbox) ==")
    cands = get_candidates(args.limit)
    print(cands)

    print("== Lendo perfil e rubrica UMA vez ==")
    profile = read_file(C.PROFILE_FILE)
    rubric  = read_file(C.RUBRIC_FILE)

    # monta um prompt com a rubrica compacta + as vagas do lote
    prompt = f"""Você é um avaliador de fit de vagas. Use APENAS o conteúdo real do anúncio.

RUBRICA (pesos: Technical 30%, Experience 25%, Behavioral 15%, Career 30%):
{rubric}

PERFIL DO CANDIDATO:
{profile}

Vagas a pontuar (retorne UM JSON array, um objeto por vaga):
{cands}

Para cada vaga retorne: key, status(scored/expired), scores{{technical,experience,behavioral,career}},
location_verdict(PASS/FAIL/FLAG), language_gate(PASS/FAIL/FLAG), language_note, deadline,
strengths[], gaps[], language. NÃO invente conteúdo do anúncio. Se a URL estiver morta após
tentar recuperar com headers de browser, marque expired. Responda SOMENTE o JSON."""

    print(f"== Chamando {C.MODEL} (1 chamada por lote) ==")
    text = call_vertex(prompt)
    # extrai o JSON do texto de resposta
    m = re.search(r"\[.*\]", text, re.S)
    if not m:
        print("ERRO: resposta sem JSON:\n", text[:500]); sys.exit(1)
    results = json.loads(m.group(0))

    print("== Agregando e ranqueando ==")
    scored = []
    for j in results:
        if j.get("status") == "expired":
            continue
        s = j["scores"]
        total = 0.30*s["technical"] + 0.25*s["experience"] + 0.15*s["behavioral"] + 0.30*s["career"]
        scored.append((total, j))
    scored.sort(reverse=True, key=lambda x: x[0])

    print("\n== SHORTLIST (top %d) ==" % args.top)
    for total, j in scored[:args.top]:
        veto = ""
        if j.get("location_verdict") == "FAIL": veto = " [LOCATION VETO]"
        if j.get("language_gate") == "FAIL":    veto += " [LANG VETO]"
        print(f"{total:5.1f}  {j['key']}{veto}")

    print("\n== Excluídos por veto ==")
    for total, j in scored:
        if j.get("location_verdict") == "FAIL" or j.get("language_gate") == "FAIL":
            print(f"- {j['key']}: {j.get('language_note','')}")

if __name__ == "__main__":
    main()