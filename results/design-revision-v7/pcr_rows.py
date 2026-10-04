"""Design revision 7 scratch: the words-only projection of controls_real.json
(DESIGN 6.3, revision 7), transcribed from the rule and run on the clue file.
Revision 6's script (results/design-revision-v6/pcr_rows.py) plus the third
clause that the recheck of revision 6 asked for [r2v6 N10a].

Reads only data/prereg/controls_real.json (never a truth file).
Rule (DESIGN 6.3, "Two projections of the file"):
  AL (as licensed): every row at its primary option.
  WO (words only):  every row at its primary, except
    (1) a row whose narrative level marks it as computed from the author's
        tables ("computation")                         -> 'none'
    (2) a row that records the author's reduction of his own observation
        ("we computed" / "reduction of his own observation")
                                                         -> the widest licensed
                                                            option short of 'none'
    (3) revision 7: a row that quotes a record ("quoting the record" in its
        narrative level) whose primary is labelled the author's reading of
        that record ("reading of the record" in the primary's justification),
        and which offers an option labelled as what the record says
        ("the record says" in its justification)       -> that option
  Named exception (kept at its primary, reported): A-MONTH, the one primary
  that rests on a calendar reconstruction outside the texts [lcr flagged 1];
  the WO legs are also reported with A-MONTH at 'none' [r2v6 N10b].
Writes nothing; prints every row the WO projection changes, per set, so that
I13(f) can compare data/prereg/pcr_projection.json with it.
Run: py results/design-revision-v7/pcr_rows.py
"""
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
d = json.load(open("data/prereg/controls_real.json", encoding="utf-8"))


def width(o):
    op = o.get("operational") or {}
    for k in ("tol_h", "tol_deg", "tol_years", "tol_days"):
        if isinstance(op.get(k), (int, float)):
            return float(op[k])
    return 0.0


n_changed = 0
clause3 = []
for s in d["sets"]:
    changes = []
    for c in s["clues"]:
        opts = c.get("fork_options") or []
        if not opts:
            continue
        prim_o = next(o for o in opts if o.get("primary"))
        prim = prim_o["option"]
        nl = (c.get("narrative_level") or "").lower()
        wo = prim
        if "computation" in nl:
            wo = "none" if any(o["option"] == "none" for o in opts) else prim
        elif "we computed" in nl or "reduction of his own observation" in nl:
            cand = [o for o in opts if o["option"] != "none"]
            wo = max(cand, key=width)["option"]
        elif "quoting the record" in nl and "reading of the record" in (prim_o.get("justification") or "").lower():
            lit = [o for o in opts if "the record says" in (o.get("justification") or "").lower()]
            if len(lit) == 1:
                wo = lit[0]["option"]
                clause3.append(c["clue_id"])
        if wo != prim:
            changes.append(f"{c['clue_id']}: {prim} -> {wo}")
    n_changed += len(changes)
    print(f"{s['set_id']:13s} " + ("; ".join(changes) if changes else "(no change)"))
print(f"rows changed by the words-only projection: {n_changed}")
print(f"rows changed by clause (3), the record's own reading: {clause3}")
print("named exception kept at its primary: A-MONTH (reported with A-MONTH at 'none' as a sensitivity)")
