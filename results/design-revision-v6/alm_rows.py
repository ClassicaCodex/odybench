"""Design revision 6 scratch (revision 5's alm_rows.py with B.9 added to the coordinate-phase list, recheck N15f): the B&M-type projection and the held-out rows of
every Almagest set, under the rules written in DESIGN 6.4 (revision 5).

Reads only data/prereg/controls_almagest.json (never a truth file).
Rules transcribed from DESIGN 6.4:
  projection (regime SL):
    interval rows               -> structural (always in)
    moon-phase rows             -> 'phase_class' option, except A.10 and B.5,
                                   whose phase class rests on Ptolemy's stated
                                   longitudes -> 'none' in the projection
    planet rows                 -> the B&M kinds: ge_* (greatest elongation),
                                   ge_*_within_j / same_apparition, visible_only,
                                   visible_before_sunrise, bm_* ; for rows whose
                                   primary is ge_*_within_j the literal
                                   ge_*_same_apparition option is used
    season row                  -> its primary (equinox_tol)
    everything else             -> 'none'
  held-out rows (Q_H):
    star rows                   -> primary option (F.4's primary is 'none')
    planet rows whose primary is positional or an opposition (opp_*)
    moon-phase rows             -> their 'positional' option, or 'elongation_tol'
                                   (B.7, B.9: the measured Sun-Moon distance)
    the eclipse row (ALM-C only; ALM-C is not counted)
Run: py results/design-revision-v6/alm_rows.py
"""
import json
from collections import Counter

d = json.load(open("data/prereg/controls_almagest.json", encoding="utf-8"))
COUNTED = ["ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H",
           "ALM-I", "ALM-J", "ALM-K", "ALM-L"]
COORD_PHASE = {"ALM-A.10", "ALM-B.5", "ALM-B.9"}   # revision 6: B.9 read off the measured 92 deg
BM_PLANET = ("ge_", "visible_only", "visible_before_sunrise", "bm_")

print("rows by kind:", dict(Counter(c["kind"] for c in d["clues"])))
by_set = {}
for c in d["clues"]:
    by_set.setdefault(c["set"], []).append(c)

n_with = 0
for sid in sorted(by_set):
    proj, held = [], []
    for c in by_set[sid]:
        opts = c.get("fork_options") or []
        names = [o.get("name") or o.get("option") for o in opts]
        prim = next((o.get("name") or o.get("option") for o in opts if o.get("primary")), None)
        cid, kind = c["clue_id"], c["kind"]
        if kind == "interval":
            proj.append(f"{cid}:{prim or 'structural'}")
        elif kind == "moon-phase":
            proj.append(f"{cid}:{'none' if cid in COORD_PHASE else 'phase_class'}")
            if "positional" in names:
                held.append(f"{cid}:positional")
            elif "elongation_tol" in names:
                held.append(f"{cid}:elongation_tol")
        elif kind == "planet":
            if prim and prim.startswith(BM_PLANET):
                if prim.endswith("_within_j"):
                    lit = prim.replace("_within_j", "_same_apparition")
                    assert lit in names, (cid, lit)
                    proj.append(f"{cid}:{lit}")
                else:
                    proj.append(f"{cid}:{prim}")
            else:
                held.append(f"{cid}:{prim}")
        elif kind == "season":
            proj.append(f"{cid}:{prim}")
        elif kind == "star":
            if prim and prim != "none":
                held.append(f"{cid}:{prim}")
        elif kind == "eclipse-lunar":
            held.append(f"{cid}:{prim}")
    counted = sid in COUNTED
    if counted and held:
        n_with += 1
    print(f"{sid} {'counted' if counted else 'reported'}")
    print(f"   projection: {', '.join(proj)}")
    print(f"   held out  : {', '.join(held) if held else '(none)'}")
print(f"counted sets with at least one held-out row: {n_with} of {len(COUNTED)}")
