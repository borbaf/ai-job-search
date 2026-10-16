import subprocess
import json
import os
import sys

skills = [
    ('himalayas', 'bun run .agents/skills/himalayas-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ('remotive', 'bun run .agents/skills/remotive-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ('dynamitejobs', 'bun run .agents/skills/dynamitejobs-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ('weworkremotely', 'bun run .agents/skills/weworkremotely-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ('jobnagringa', 'bun run .agents/skills/jobnagringa-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ('catho', 'bun run .agents/skills/catho-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ('infojobs', 'bun run .agents/skills/infojobs-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ('freehire', 'bun run .agents/skills/freehire-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ('ziprecruiter', 'bun run .agents/skills/ziprecruiter-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
    ('sprout', 'bun run .agents/skills/sprout-search/cli/src/cli.ts search --query "Supply Chain" --format json'),
]

for name, cmd in skills:
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=35, encoding='utf-8', errors='replace')
        out = res.stdout.strip()
        print(f"=== {name} === (exit {res.returncode}) len: {len(out)}")
        if len(out) < 200:
            print(out)
        else:
            print(out[:150] + " ... " + out[-100:])
    except Exception as e:
        print(f"=== {name} === ERROR: {e}")
