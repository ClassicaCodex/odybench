"""Design revision 8 scratch (revision 6's alm_rows.py, with A.2, A.5 and B.2
added to the rows the projection sets to "none" [r3v7 R3-1]): the B&M-type
projection and the held-out rows of every Almagest set, under the rules
written in DESIGN 6.4 (revision 8).

Reads only data/prereg/controls_almagest.json (never a truth file).
Rules transcribed from DESIGN 6.4:
  projection (regime SL):
    interval rows               -> structural (always in)
    moon-phase rows             -> 'phase_class' option only where the words
                                   state the phase. 'none' for every row whose
                                   own 'none' option says the Moon's phase is
                                   not stated in words (A.2, A.5, A.10, B.2,
                                   B.5: inferred from proximity, an opposition
                                   or stated longitudes), and for B.9, whose
                                   class is read off the measured 92 deg.
                                   B.7 ('about a quadrant') alone stays.
    planet rows                 -> the B&M kinds: ge_* (greatest elongation),
                                   ge_*_within_j / same_apparition, visible_only,
                                   visible_before_sunrise, bm_* ; for rows whose
                                   primary is ge_*_within_j the literal
                                   ge_*_same_apparition option is used
    season row                  -> its primary (equinox_tol)
    everything else             -> 'none'
  held-out rows (Q_H), unchanged from revision 6:
    star rows                   -> primary option (F.4's primary is 'none')
    planet rows whose primary is positional or an opposition (opp_*)
    moon-phase rows             -> their 'positional' option, or 'elongation_tol'
                                   (B.7, B.9: the measured Sun-Moon distance)
    the eclipse row (ALM-C only; ALM-C is not counted)
Run: py results/design-revision-v8/alm_rows.py
"""
import json
from collections import Counter

CLUES = "C:/Projects/odybench/data/prereg/controls_almagest.json"
REV6_OUT = "C:/Projects/odybench/results/design-revision-v6/alm_rows.out.txt"
COUNTED = ["ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H",
           "ALM-I", "ALM-J", "ALM-K", "ALM-L"]
MEASURED_PHASE = {"ALM-B.9"}        # class read off the measured 92 deg (revision 6, r1v5 N15f)
NOT_IN_WORDS = "not stated in words"
BM_PLANET = ("ge_", "visible_only", "visible_before_sunrise", "bm_")


def opt_name(o):
    return o.get("name") or o.get("option")


def unstated_phase_rows(clues):
    """moon-phase rows whose own 'none' option says the phase is not stated in words."""
    out = set()
    for c in clues:
        if c["kind"] != "moon-phase":
            continue
        for o in c.get("fork_options") or []:
            if opt_name(o) == "none" and NOT_IN_WORDS in (o.get("justification") or ""):
                out.add(c["clue_id"])
    return out


def project(clues, none_phase):
    """{set: (projection list, held-out list)} under the rules above."""
    by_set = {}
    for c in clues:
        by_set.setdefault(c["set"], []).append(c)
    out = {}
    for sid in sorted(by_set):
        proj, held = [], []
        for c in by_set[sid]:
            opts = c.get("fork_options") or []
            names = [opt_name(o) for o in opts]
            prim = next((opt_name(o) for o in opts if o.get("primary")), None)
            cid, kind = c["clue_id"], c["kind"]
            if kind == "interval":
                proj.append(f"{cid}:{prim or 'structural'}")
            elif kind == "moon-phase":
                proj.append(f"{cid}:{'none' if cid in none_phase else 'phase_class'}")
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
        out[sid] = (proj, held)
    return out


def parse_rev6(path=REV6_OUT):
    """{set: (projection list, held-out list)} from revision 6's printed output."""
    out, sid = {}, None
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if s.startswith("ALM-") and (" counted" in s or " reported" in s):
            sid = s.split()[0]
            out[sid] = ([], [])
        elif s.startswith("projection:") and sid:
            out[sid][0].extend(x.strip() for x in s.split(":", 1)[1].split(","))
        elif s.startswith("held out") and sid:
            body = s.split(":", 1)[1].strip()
            if body != "(none)":
                out[sid][1].extend(x.strip() for x in body.split(","))
    return out


def main():
    d = json.load(open(CLUES, encoding="utf-8"))
    clues = d["clues"]
    print("rows by kind:", dict(Counter(c["kind"] for c in clues)))
    unstated = unstated_phase_rows(clues)
    none_phase = unstated | MEASURED_PHASE
    phase_rows = sorted(c["clue_id"] for c in clues if c["kind"] == "moon-phase")
    print("moon-phase rows:", ", ".join(phase_rows))
    print("  whose 'none' option says the phase is not stated in words:", ", ".join(sorted(unstated)))
    print("  read off a measured coordinate:", ", ".join(sorted(MEASURED_PHASE)))
    print("  kept at their phase class:", ", ".join(sorted(set(phase_rows) - none_phase)))
    assert none_phase == {"ALM-A.2", "ALM-A.5", "ALM-A.10", "ALM-B.2", "ALM-B.5", "ALM-B.9"}, none_phase
    res = project(clues, none_phase)
    n_with = 0
    for sid, (proj, held) in res.items():
        counted = sid in COUNTED
        if counted and held:
            n_with += 1
        print(f"{sid} {'counted' if counted else 'reported'}")
        print(f"   projection: {', '.join(proj)}")
        print(f"   held out  : {', '.join(held) if held else '(none)'}")
    print(f"counted sets with at least one held-out row: {n_with} of {len(COUNTED)}")

    print("\nChanges from revision 6's lists (results/design-revision-v6/alm_rows.out.txt):")
    try:
        old = parse_rev6()
    except OSError:
        # not in the public export (10.1); the lists above do not depend on it
        print("  revision 6's output is not available here; comparison skipped")
        return
    for sid in res:
        po, ho = old[sid]
        pn, hn = res[sid]
        if po != pn:
            print(f"  {sid} projection: " + "; ".join(f"{a} -> {b}" for a, b in zip(po, pn) if a != b))
        if ho != hn:
            print(f"  {sid} held out changed: {ho} -> {hn}")
    same_held = all(old[s][1] == res[s][1] for s in res)
    print(f"  held-out rows unchanged in every set: {same_held}")


if __name__ == "__main__":
    main()
