# Compact dump of controls_almagest.json (sets, then clues with options).
# Read-only on data/prereg. Round-1 review of DESIGN.md revision 2.
import json
import sys

d = json.load(open("data/prereg/controls_almagest.json", encoding="utf-8"))
out = []
out.append("CONVENTIONS " + json.dumps(d["conventions"], ensure_ascii=False))
out.append("RULES " + json.dumps(d["rules_applied"], ensure_ascii=False))
out.append("LICENSE " + json.dumps(d["license_check"], ensure_ascii=False))
for s in d["sets"]:
    out.append("=" * 80)
    out.append(json.dumps(s, ensure_ascii=False))
for c in d["clues"]:
    out.append("-" * 80)
    meta = {k: v for k, v in c.items() if k not in ("options", "fork_options")}
    out.append("CLUE " + json.dumps(meta, ensure_ascii=False))
    for o in c.get("options", c.get("fork_options", [])):
        out.append("   OPT " + json.dumps(o, ensure_ascii=False))
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out))
