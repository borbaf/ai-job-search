"""Scrape da sandbox: roda cada CLI de portal direto no shell.
Nenhum LLM envolvido -> custo zero de conversa."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import config as C

def run_portal(name, cmd, term):
    full = cmd + [term]
    print(f"\n== {name} ==")
    try:
        out = subprocess.run(full, capture_output=True, text=True, timeout=120)
        print(out.stdout[-2000:] if out.stdout else "(sem saída)")
        if out.returncode != 0:
            print(f"[{name}] falhou (código {out.returncode}): {out.stderr[-500:]}")
    except subprocess.TimeoutExpired:
        print(f"[{name}] timeout (120s)")

def main():
    term = sys.argv[1] if len(sys.argv) > 1 else "data science"
    for name, cmd in C.PORTALS.items():
        run_portal(name, cmd, term)

if __name__ == "__main__":
    main()