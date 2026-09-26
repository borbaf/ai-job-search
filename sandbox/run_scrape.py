"""Scrape da sandbox: roda cada CLI de portal direto no shell.
Nenhum LLM envolvido -> custo zero de conversa."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C

def run_portal(name, cmd, term, location, limit):
    # monta: bun run <cli.ts> search -q "<term>" [-l "<loc>"] --limit N --format json
    full = cmd + ["-q", term]
    if location:
        full += ["-l", location]
    full += ["--limit", str(limit), "--format", "json"]
    print(f"\n== {name} ==")
    try:
        out = subprocess.run(full, capture_output=True, text=True, timeout=120)
        if out.stdout.strip():
            # tenta exibir como JSON compacto; se não parsear, mostra texto cru
            try:
                data = json.loads(out.stdout)
                print(json.dumps(data, ensure_ascii=False)[:2000])
            except Exception:
                print(out.stdout[-2000:])
        else:
            print("(sem saída)")
        if out.returncode != 0:
            print(f"[{name}] falhou (código {out.returncode}): {out.stderr[-500:]}")
    except subprocess.TimeoutExpired:
        print(f"[{name}] timeout (120s)")

def main():
    term = sys.argv[1] if len(sys.argv) > 1 else "data science"
    loc  = sys.argv[2] if len(sys.argv) > 2 else ""
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    for name, cmd in C.PORTALS.items():
        run_portal(name, cmd, term, loc, limit)

if __name__ == "__main__":
    main()