"""Design revision 8 scratch [r3v7 R3-1, R3-4, R3-5, R3-11]: the design-stage
estimate of how far each counted Almagest set's B&M-type projection narrows a
136-year window, under revision 8's projection (6.4: A.2, A.5 and B.2 at
"none"; `same_apparition` at its frozen meaning).

NO NEW SKY COMPUTATION. This script does not search the sky. It reads the
recheck's recorded output, results/critique-design-r3/narrowing_inferred_phase.json
([r2v6]'s narrowing_3b.py machinery, rerun by the recheck on three null windows
starting at -1500, -1100 and -700, which hold no control date), and picks, for
each counted set, the row that matches revision 8's projection:
  ALM-A  "ALM-A [frozen, inferred phases none]"   (A.9 with the Sun at -8 deg)
  ALM-B  "ALM-B [frozen, inferred phases none]"
  ALM-I  "ALM-I (same_app & visible)"
  ALM-J  "ALM-J (same_app & visible)"
  others the plain row: their projections hold no phase row and no
         `same_apparition` option, so revision 8 leaves them as they were.
The bench's own frozen code recomputes narrowability at the null-side stage;
none of these numbers enters a rule.
Run: py results/design-revision-v8/narrowing_v8.py
"""
import json

SRC = "C:/Projects/odybench/results/critique-design-r3/narrowing_inferred_phase.json"
COUNTED = ["ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H",
           "ALM-I", "ALM-J", "ALM-K", "ALM-L"]
ROW_V8 = {"ALM-A": "ALM-A [frozen, inferred phases none]",
          "ALM-B": "ALM-B [frozen, inferred phases none]",
          "ALM-I": "ALM-I (same_app & visible)",
          "ALM-J": "ALM-J (same_app & visible)"}
ROW_V7 = {"ALM-A": "ALM-A (same_app & visible)", "ALM-B": "ALM-B (same_app & visible)",
          "ALM-I": "ALM-I (same_app & visible)", "ALM-J": "ALM-J (same_app & visible)"}
LINE = 0.05


def pick(window, sid, rowmap):
    return window["sets"][rowmap.get(sid, sid)]


def assemble(report, rowmap=ROW_V8):
    """{window tag: {set: (frac, n_pass, n_cand)}} for the counted sets."""
    out = {}
    for tag, w in report.items():
        out[tag] = {}
        for sid in COUNTED:
            r = pick(w, sid, rowmap)
            out[tag][sid] = (r["frac"], r["n_pass"], r["n_cand"])
    return out


def narrowable_sets(table_w):
    return sorted(s for s, (f, n, N) in table_w.items() if n <= LINE * N)


def main():
    rep = json.load(open(SRC, encoding="utf-8"))
    v8 = assemble(rep)
    v7 = assemble(rep, ROW_V7)
    tags = list(rep)
    print("windows:", ", ".join(f"{t} from {rep[t]['start_year']} (N_cand {rep[t]['n_cand']}, "
                                 f"5% = {LINE * rep[t]['n_cand']:.0f} days)" for t in tags))
    print("\nshare of a window's days passing each counted set's projection (revision 8), and margin to the line:")
    for sid in COUNTED:
        fr = [v8[t][sid][0] for t in tags]
        nd = [v8[t][sid][1] for t in tags]
        lo, hi = min(fr), max(fr)
        note = ""
        if sid in ("ALM-A", "ALM-B"):
            f7 = [v7[t][sid][0] for t in tags]
            note = f"   (revision 7's projection: {min(f7) * 100:.2f}-{max(f7) * 100:.2f}%)"
        print(f"  {sid}: {lo * 100:5.2f}-{hi * 100:5.2f}%  days {min(nd)}-{max(nd)}  "
              f"{'narrows' if hi <= LINE else ('does not narrow' if lo > LINE else 'MIXED')}"
              f"  margin {(LINE - hi) * 100:+.2f} to {(LINE - lo) * 100:+.2f} points{note}")
    for t in tags:
        ns = narrowable_sets(v8[t])
        print(f"  {t}: {len(ns)} sets narrow: {', '.join(ns)}")
    near = [s for s in COUNTED if all(LINE - 0.0065 <= v8[t][s][0] <= LINE for t in tags)]
    print("sets within 0.65 percentage points under the line in every window:", ", ".join(near))

    print("\nvariants of ALM-A (the recheck's rows; reported, not revision 8's projection):")
    for name in ("ALM-A (A.2 only none) [frozen, inferred phases none]",
                 "ALM-A (A.5 only none) [frozen, inferred phases none]",
                 "ALM-A (civil dawn for A.9) [frozen, inferred phases none]"):
        fr = [rep[t]["sets"][name]["frac"] for t in tags]
        print(f"  {name}: {min(fr) * 100:.2f}-{max(fr) * 100:.2f}%")
    print("  ALM-A with A.9 at its stated hour (about 5 equinoctial hours after midnight, LAT), the "
          "instant revision 8 freezes (6.4, 10.3): NOT ESTIMATED (no new sky search before the freeze)")
    print("\nthe other meaning of same_apparition (side of the Sun only), as recorded:")
    for sid in ("ALM-A", "ALM-B", "ALM-I", "ALM-J"):
        fr = [rep[t]["sets"][sid]["frac"] for t in tags]
        print(f"  {sid}, with its phase rows at their class: {min(fr) * 100:.2f}-{max(fr) * 100:.2f}%")
    print("  (B.2 at none under the side-only meaning was not estimated; under the frozen meaning B.7 "
          "implies B.2's class, so B.2 changes nothing there [r3v7 C7])")
    same_b = all(rep[t]["sets"]["ALM-B [frozen, inferred phases none]"]["n_pass"] ==
                 rep[t]["sets"]["ALM-B (same_app & visible)"]["n_pass"] for t in tags)
    print(f"  ALM-B, frozen meaning: identical day counts with and without B.2: {same_b}")


if __name__ == "__main__":
    main()
