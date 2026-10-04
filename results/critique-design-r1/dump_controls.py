# Compact dump of a prereg clue file: one block per set, one line per clue option.
# Usage: py results/critique-design-r1/dump_controls.py <json> <out.txt>
# Written for the round-1 review of DESIGN.md revision 2 (read-only on data/prereg).
import json
import sys

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding="utf-8"))
lines = []
for s in d["sets"]:
    lines.append("=" * 100)
    head = {k: v for k, v in s.items() if k not in ("clues", "rows")}
    lines.append(json.dumps(head, ensure_ascii=False))
    for c in s.get("clues", s.get("rows", [])):
        meta = {k: v for k, v in c.items() if k not in ("fork_options", "options")}
        lines.append("  CLUE " + json.dumps(meta, ensure_ascii=False))
        for o in c.get("fork_options", c.get("options", [])):
            lines.append("     OPT " + json.dumps(o, ensure_ascii=False))
open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("wrote", out, len(lines), "lines")
