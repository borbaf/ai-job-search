"""Scrape da sandbox: roda cada CLI de portal direto no shell.
Descobre as flags suportadas de cada CLI via --help e monta o comando
só com flags válidas. Nenhum LLM envolvido -> custo zero de conversa."""
import json, os, subprocess, sys, re
sys.path.insert(0, os.path.dirname(__file__))
import config as C

def get_help(cmd):
    try:
        out = subprocess.run(cmd + ["--help"], capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=30)
        return (out.stdout or "") + (out.stderr or "")
    except Exception:
        return ""

def has_flag(help_text, *aliases):
    # \b só no FIM da flag (após os caracteres). No início falha porque
    # flags começam com '-' (não-word), onde não existe word boundary.
    return any(re.search(rf"{re.escape(a)}\b", help_text) for a in aliases)

def run_portal(name, cmd, term, location, limit):
    help_text = get_help(cmd)
    print(f"\n== {name} ==")
    if not help_text:
        print("(não consegui ler o --help; pulando)"); return

    full = cmd[:]
    if has_flag(help_text, "-q", "--query"):
        full += ["-q", term]
    elif has_flag(help_text, "--search", "--keyword", "--text"):
        alias = next(a for a in ("--search", "--keyword", "--text") if has_flag(help_text, a))
        full += [alias, term]
    if has_flag(help_text, "-l", "--location"):
        if location:
            full += ["-l", location]
    if has_flag(help_text, "--limit", "-n"):
        full += ["--limit", str(limit)]
    if has_flag(help_text, "--format"):
        full += ["--format", "json"]

    try:
        out = subprocess.run(full, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=120)
        stdout = (out.stdout or "").strip()
        if stdout:
            try:
                data = json.loads(stdout)
                print(json.dumps(data, ensure_ascii=False)[:2500])
            except Exception:
                print(stdout[-2500:])
        else:
            print("(sem saída)")
        if out.returncode != 0:
            print(f"[{name}] falhou (código {out.returncode}): {(out.stderr or '')[-500:]}")
    except subprocess.TimeoutExpired:
        print(f"[{name}] timeout (120s)")
    except Exception as e:
        print(f"[{name}] erro inesperado: {e}")

def main():
    term = sys.argv[1] if len(sys.argv) > 1 else "data science"
    loc  = sys.argv[2] if len(sys.argv) > 2 else ""
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    for name, cmd in C.PORTALS.items():
        run_portal(name, cmd, term, loc, limit)

if __name__ == "__main__":
    main()