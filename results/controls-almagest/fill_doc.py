"""Assemble docs/controls-almagest.md from doc_template.md, doc_tables.md and the prereg files."""
import json, collections, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
tpl = (HERE / "doc_template.md").read_text(encoding="utf-8")
tab = (HERE / "doc_tables.md").read_text(encoding="utf-8")
i2 = tab.index("### Table 2.")
t1, t2 = tab[:i2].strip(), tab[i2:].strip()
d = json.loads((ROOT / "data/prereg/controls_almagest.json").read_text(encoding="utf-8"))
t = json.loads((ROOT / "data/prereg/controls_almagest_truth.json").read_text(encoding="utf-8"))
rows = []
for s, ts in zip(d["sets"], t["sets"]):
    kinds = collections.Counter(c["kind"] for c in d["clues"] if c["set"] == s["set"])
    others = ", ".join(f"{x['record']} ({x['day_offset']:+d}" + (f"; emended {x['emended']['day_offset']:+d}" if "emended" in x else "") + ")"
                       for x in ts["records"][1:])
    place = s["observer_place"]["value"]
    rows.append(f"| {s['set']} | {ts['day0_record']} | {others} | {s['span_days']} | "
                f"{', '.join(f'{k} {v}' for k, v in sorted(kinds.items()))} | {place} | {ts['day0_text']} |")
out = tpl.replace("<<TABLES_1>>", t1.replace("### ", "**").replace("\n\n|", "**\n\n|", 2) if False else t1) \
         .replace("<<TABLES_2>>", t2).replace("<<SETROWS>>", "\n".join(rows))
# demote generated '### Table' headings to bold captions so the doc's own section headings stay the outline
out = "\n".join(("**" + ln[4:].strip() + "**") if ln.startswith("### Table") or ln.startswith("### Summary") else ln
                for ln in out.splitlines()) + "\n"
assert "<<" not in out
(ROOT / "docs" / "controls-almagest.md").write_text(out, encoding="utf-8")
print("wrote docs/controls-almagest.md", len(out), "chars")
