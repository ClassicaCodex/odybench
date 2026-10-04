"""Design revision 6 scratch: the words-only projection of controls_real.json
(DESIGN 6.3, revision 6), transcribed from the rule and run on the clue file.

Reads only data/prereg/controls_real.json (never a truth file).
Rule (DESIGN 6.3, "Two projections of the file"):
  AL (as licensed): every row at its primary option.
  WO (words only):  every row at its primary, except
    - a row whose narrative level marks it as computed from the author's
      tables ("computation")                     -> 'none'
    - a row that records the author's reduction of his own observation
      ("we computed" / "reduction of his own observation")
                                                   -> the widest licensed
                                                      option short of 'none'
Writes nothing; prints every row the WO projection changes, per set, so that
I13(f) can compare data/prereg/pcr_projection.json with it.
Run: py results/design-revision-v6/pcr_rows.py
"""
import json

d = json.load(open("data/prereg/controls_real.json", encoding="utf-8"))


def width(o):
    op = o.get("operational") or {}
    for k in ("tol_h", "tol_deg", "tol_years", "tol_days"):
        if isinstance(op.get(k), (int, float)):
            return float(op[k])
    return 0.0


n_changed = 0
for s in d["sets"]:
    changes = []
    for c in s["clues"]:
        opts = c.get("fork_options") or []
        if not opts:
            continue
        prim = next(o["option"] for o in opts if o.get("primary"))
        nl = (c.get("narrative_level") or "").lower()
        if "computation" in nl:
            wo = "none" if any(o["option"] == "none" for o in opts) else prim
        elif "we computed" in nl or "reduction of his own observation" in nl:
            cand = [o for o in opts if o["option"] != "none"]
            wo = max(cand, key=width)["option"]
        else:
            wo = prim
        if wo != prim:
            changes.append(f"{c['clue_id']}: {prim} -> {wo}")
    n_changed += len(changes)
    print(f"{s['set_id']:13s} " + ("; ".join(changes) if changes else "(no change)"))
print(f"rows changed by the words-only projection: {n_changed}")
