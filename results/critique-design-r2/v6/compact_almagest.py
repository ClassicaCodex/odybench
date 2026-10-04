# Compact row-by-row view of controls_almagest.json (clue file only; no truth file),
# for the licence/leak review of revision 6. Output: compact_almagest.txt (UTF-8).
import json, pathlib
ROOT = pathlib.Path(r"C:\Projects\odybench")
OUT = pathlib.Path(__file__).parent
d = json.load(open(ROOT / "data/prereg/controls_almagest.json", encoding="utf-8"))
L = []
for s in d["sets"]:
    L.append("=" * 90)
    L.append(f"SET {s['set']}: records {s['records']} span {s.get('span_days')} d; tight {s.get('tight')}; anchor {s.get('anchor_record')}")
    L.append(f"  description: {s['description']}")
    op = s.get("observer_place")
    L.append(f"  observer: {json.dumps(op, ensure_ascii=False)[:400]}")
    for c in [c for c in d["clues"] if c["set"] == s["set"]]:
        L.append("-" * 70)
        L.append(f"{c['clue_id']} [{c['kind']}] day {c.get('day_offset')} rec {c.get('record')} level: {c.get('narrative_level')}")
        L.append(f"  STATEMENT: {c['statement']}")
        L.append(f"  LICENCE: {c['licence_words']}")
        for o in c.get("fork_options") or []:
            mark = "*" if o.get("primary") else " "
            L.append(f"   {mark} {o.get('option')}: {json.dumps(o.get('operational'), ensure_ascii=False)}")
            if o.get("primary"):
                L.append(f"       just: {o.get('justification','')[:400]}")
        if c.get("notes"):
            L.append(f"  NOTES: {c['notes'][:500]}")
(OUT / "compact_almagest.txt").write_text("\n".join(L), encoding="utf-8")
print("rows", len(d["clues"]), "lines", len(L))
