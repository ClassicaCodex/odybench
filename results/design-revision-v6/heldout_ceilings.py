"""Design revision 6 scratch (TRUTH-SIDE: reads results/controls-almagest/slack.json,
which holds measurements at the true dates; never give this script or its output
to a public-tier agent).

Recheck of revision 5, issue N12: the held-out rows of the Almagest calibration
(Q_H, DESIGN 6.4) took "the most lenient listed value" of the drafter's
tolerance lists, the rule regime SL abandoned for R2-9's reason.  Revision 6
sets them by the same leave-one-set-out ceiling rule as regime SL:

  tolerance(row of class K in set S) = the largest measured |computed - stated|
  among the records of class K that are NOT in S (records in no set included),
  rounded UP to the next 0.1 deg (degrees) or the next whole day (days).

Measured offsets (from slack.json, the drafter's DE441 comparison, alm Tables 3-5):
  planet-star  : for each stated component (dlon_s, dlat_s, dist_s, beyond_pollux_s),
                 |computed - stated|; a conjunction / occultation ('conj') stated as
                 coincidence contributes its separation at the record instant;
                 an inequality that holds contributes 0 (IX.7.11's 'more than 3 moons
                 south'; X.1.5's 'a Pleiad-length or less' in longitude);
                 a record whose star the drafter marks as not securely identified
                 (X.1.6) contributes nothing;
  planet-Moon  : |dlon_c - dlon_s|; a record whose stated offset is not in its words
                 (X.4.3: the 1/4 deg came from Ptolemy's computed lunar longitude,
                 [lca2 item 3]) contributes nothing;
  Sun-Moon     : |computed - stated| (V.3.2, VII.2.4);
  opposition   : |record - mean-Sun opposition| in days (off_opp_mean_d).
Cruxes enter at the reading the slack summary uses (IX.7.11 emended, IX.9.4 printed),
as regime SL's ceilings do.
A class with no record outside the set falls back to the pooled lunar classes
(planet-Moon and Sun-Moon) outside the set.
Run: py results/design-revision-v6/heldout_ceilings.py
"""
import json
import math

SLACK = "results/controls-almagest/slack.json"
SETS = {
    "ALM-A": ["IX.10.3", "X.8.2", "IX.9.4", "XI.2.2"],
    "ALM-B": ["X.4.3", "XI.6.2", "V.3.2", "VII.2.4"],
    "ALM-C": ["IX.8.3", "IV.6.14"],
    "ALM-D": ["IX.7.4", "X.1.3"],
    "ALM-E": ["X.3.2b", "III.1.10"],
    "ALM-F": ["X.2.4", "X.1.6"],
    "ALM-G": ["X.3.2a", "IX.7.5"],
    "ALM-H": ["IX.7.9", "IX.7.11", "IX.7.14"],
    "ALM-I": ["IX.10.6a", "IX.10.6b"],
    "ALM-J": ["X.9.2", "X.4.6a", "X.4.6b"],
    "ALM-K": ["IX.7.16", "XI.3.2", "IX.7.15"],
    "ALM-L": ["X.1.5", "X.2.3", "IX.9.3"],
}
COUNTED = ["ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H",
           "ALM-I", "ALM-J", "ALM-K", "ALM-L"]
INSECURE_STAR = {"X.1.6"}
MOON_NOT_IN_WORDS = {"X.4.3"}
INEQUALITY_HOLDS = {("IX.7.11", "dlat"), ("X.1.5", "dlon")}
CRUX_READING = {"IX.7.11": "emended", "IX.9.4": "printed"}


def rows():
    out = {}
    for r in json.load(open(SLACK, encoding="utf-8")):
        rid = r["id"]
        want = CRUX_READING.get(rid)
        if want and not r["reading"].startswith(want):
            continue
        out[rid] = r
    return out


def star_offset(rid, s):
    if rid in INSECURE_STAR or s.get("kind") in ("note_only", "nearest"):
        return None
    if s["kind"] == "conj":
        return s["sep"]
    vals = []
    for comp in ("dlon", "dlat"):
        st = s.get(f"{comp}_s")
        if st is None:
            continue
        if (rid, comp) in INEQUALITY_HOLDS:
            vals.append(0.0)
            continue
        vals.append(abs(s[f"{comp}_c"] - st))
    if "dist_s" in s:
        vals.append(abs(s["dist_c"] - s["dist_s"]))
    if "beyond_pollux_s" in s:
        vals.append(abs(s["beyond_pollux_c"] - s["beyond_pollux_s"]))
        vals.append(abs(s.get("perp_c", 0.0)))
    return max(vals) if vals else None


def measured():
    m = {"star": {}, "moon": {}, "sunmoon": {}, "opp": {}}
    for rid, r in rows().items():
        offs = [o for o in (star_offset(rid, s) for s in (r.get("stars") or [])) if o is not None]
        if offs:
            m["star"][rid] = max(offs)
        mo = r.get("moon")
        if mo and "dlon_s" in mo and rid not in MOON_NOT_IN_WORDS:
            m["moon"][rid] = abs(mo["dlon_c"] - mo["dlon_s"])
        ms = r.get("moonsun")
        if ms:
            m["sunmoon"][rid] = abs(ms["computed"] - ms["stated"])
        if "off_opp_mean_d" in r:
            m["opp"][rid] = abs(r["off_opp_mean_d"])
    return m


def ceil_to(x, step):
    return math.ceil(round(x / step, 9)) * step


def main():
    m = measured()
    for k, d in m.items():
        print(f"{k:8s} " + ", ".join(f"{rid} {v:.2f}" for rid, v in sorted(d.items(), key=lambda t: -t[1])))
    print()
    result = {}
    for S in COUNTED:
        inset = set(SETS[S])
        row = {}
        for k, step, unit in (("star", 0.1, "deg"), ("moon", 0.1, "deg"),
                              ("sunmoon", 0.1, "deg"), ("opp", 1.0, "d")):
            out = {rid: v for rid, v in m[k].items() if rid not in inset}
            if not out and k in ("moon", "sunmoon"):
                out = {rid: v for kk in ("moon", "sunmoon") for rid, v in m[kk].items() if rid not in inset}
                src = "pooled lunar classes"
            else:
                src = "own class"
            if not out:
                continue
            rid_max = max(out, key=out.get)
            row[k] = dict(max=round(out[rid_max], 3), record=rid_max,
                          tolerance=round(ceil_to(out[rid_max], step), 3), unit=unit, source=src)
        result[S] = row
        print(S, "  ".join(f"{k}: {v['tolerance']} {v['unit']} (max {v['max']} at {v['record']}; {v['source']})"
                           for k, v in row.items()))
    json.dump(result, open("results/design-revision-v6/heldout_ceilings.json", "w"), indent=1)


if __name__ == "__main__":
    main()
