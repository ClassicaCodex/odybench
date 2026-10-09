"""
verdict.py -- the lean verdict (LEAN.md, "The rule, restricted"; DESIGN 9.2,
9.3).  Agent L2.

Gathers the rule's inputs from the run's result files, applies
odybench.lean.verdict.decide with the thresholds of
data/prereg/verdict_rule.json (unchanged), and writes results/VERDICT.md and
results/verdict.json.

Inputs (each optional; a quantity not found is printed "not evaluated"):
  results/attain/attain.json      null side: G_BM (or G_BM_lo) per slot v0..v5,
                                  p_H_min, Q_record, Q_exch (top level or under
                                  "heldout"/"null_side")
  results/t0/t0.json              T0_pass, T0, r_Ody
  results/heldout/heldout.json    p_H, Q_contra, p per pool, membership
  results/n6/n6.json              N6 (reported beside the rule, not an input)
  results/alm/alm.json            gate 3b: seen_ALM_SL (six legs), rec_ALM_BM,
                                  gate3b_run
  results/instrument/summary.json INSTR (else an "INSTR" key in the files above)
Each quantity is looked up by name (and listed aliases) in a fixed order of
files, and the file and key path it came from are printed beside it.

  py verdict.py                   # after the target stage
  py verdict.py --results DIR     # read another results tree (tests)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from odybench.lean import verdict as V  # noqa: E402

RULE = ROOT / "data" / "prereg" / "verdict_rule.json"
FILES = {
    "attain": "attain/attain.json",
    "t0": "t0/t0.json",
    "heldout": "heldout/heldout.json",
    "n6": "n6/n6.json",
    "alm": "alm/alm.json",
    "instrument": "instrument/summary.json",
}
# quantity -> (files in priority order, key names)
WHERE = {
    "INSTR": (("instrument", "attain", "t0", "heldout", "alm"), ("INSTR", "instr_pass", "all_pass")),
    "T0_pass": (("t0", "attain"), ("T0_pass",)),
    "T0": (("t0", "attain"), ("T0", "T0_class", "T0_verdict")),
    "r_Ody": (("t0", "attain", "heldout"), ("r_Ody", "reach_Ody", "r_ody")),
    "G_BM": (("attain",), ("G_BM",)),
    "G_BM_lo": (("attain",), ("G_BM_lo",)),
    "p_H_min": (("attain", "heldout"), ("p_H_min",)),
    "Q_record": (("attain", "heldout"), ("Q_record",)),
    "Q_exch": (("attain", "heldout"), ("Q_exch",)),
    "p_H": (("heldout",), ("p_H",)),
    "Q_contra": (("heldout",), ("Q_contra",)),
    "gate3b_run": (("alm",), ("gate3b_run", "gate_3b_run")),
    "seen_ALM_SL": (("alm",), ("seen_ALM_SL",)),
    "rec_ALM_BM": (("alm",), ("rec_ALM_BM",)),
}
EXPECT = [  # LEAN.md, "Already known, and so not a finding of the run"
    ("T0", "RE (18 Mar 1189 BC passes N, C, V and M as well)"),
    ("G_BM(v1)", "about 0.14; lower bounds 0.087-0.20 across the slot family; Q_tol and Q_slot expected"),
    ("p_H_min", "about 0.040; Q_record holds"),
    ("P(total at Ithaki, 16 Apr -1177), mixture", "about 0.30"),
    ("rec_ALM_BM", "<= 5 (Q_BM expected); seen_ALM_SL about 9 of 11"),
]


def _find(d, names, path=(), depth=0):
    """Depth-first search for the first key in `names` (the top level first)."""
    if not isinstance(d, dict) or depth > 4:
        return None
    for n in names:
        if n in d:
            return d[n], path + (n,)
    for k, v in d.items():
        if isinstance(v, dict) and k not in ("lattice", "Q_exch_tests", "reported", "weights", "eclipses"):
            r = _find(v, names, path + (k,), depth + 1)
            if r is not None:
                return r
    return None


def gather(results):
    docs, prov = {}, {}
    for k, rel in FILES.items():
        p = Path(results) / rel
        if p.exists():
            docs[k] = json.loads(p.read_text(encoding="utf-8"))
            prov[k] = dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    q, src = {}, {}
    for name, (files, keys) in WHERE.items():
        for f in files:
            if f in docs:
                r = _find(docs[f], keys)
                if r is not None:
                    q[name], src[name] = r[0], f"{FILES[f]}:{'.'.join(r[1])}"
                    break
    if isinstance(q.get("INSTR"), dict):
        q["INSTR"] = q["INSTR"].get("pass", q["INSTR"].get("all_pass"))
    if q.get("G_BM") is not None:
        g = {}
        for v, x in q["G_BM"].items():
            if isinstance(x, dict):
                g[v] = (x.get("G"), x.get("lo", x.get("G_lo")), x.get("hi", x.get("G_hi")))
            else:
                g[v] = tuple(x[:3])
        q["G_BM"] = g
    return q, src, docs, prov


def _v(x):
    if isinstance(x, float):
        return f"{x:.4g}"
    return "-" if x is None else str(x)


def write(results, out_md, out_json):
    rule = json.loads(RULE.read_text(encoding="utf-8"))
    thr = rule["thresholds"]
    q, src, docs, prov = gather(results)
    labels, quals, notes = V.decide(q, thr)
    head = V.headline(labels, quals)
    rows = V.numbers(q, thr)
    L = []
    p = L.append
    p("# odybench: the lean verdict")
    p("")
    p("LEAN.md (amendment 1 to DESIGN.md revision 8), \"The rule, restricted\"; thresholds of "
      "`data/prereg/verdict_rule.json`, unchanged.")
    p("")
    p("## Headline")
    p("")
    for h in head:
        p(f"- {h}")
    p("")
    p(f"**Labels:** {', '.join(labels)}  ")
    p(f"**Qualifiers:** {', '.join(quals) if quals else 'none'}  ")
    p("**Not tested in the lean run:** 3a, 4, label 2's pct_N4 leg" +
      ("" if any(r[0].startswith("seen_ALM_SL") and r[3] is not None for r in rows) else ", 3b (not run)"))
    p("")
    p("## Every number beside its threshold")
    p("")
    p("| quantity | value | condition | holds | source |")
    p("|---|---|---|---|---|")
    srcmap = {"G_BM,lo": "G_BM", "seen_ALM_SL (six legs)": "seen_ALM_SL", "p_H,min": "p_H_min",
              "T0 (reported)": "T0"}
    for name, val, cond, holds in rows:
        key = next((v for k, v in srcmap.items() if name.startswith(k)), name)
        p(f"| {name} | {_v(val)} | {cond} | {_v(holds) if holds is not None else 'not evaluated'} | "
          f"{src.get(key, src.get('G_BM_lo', '-') if key == 'G_BM' else '-')} |")
    p("")
    p("## Notes")
    p("")
    for n in notes:
        p(f"- {n}")
    hd = docs.get("heldout")
    if hd:
        p("")
        p("## Held-out test (DESIGN 7.2)")
        p("")
        p("| pool | member | n | p |")
        p("|---|---|---|---|")
        for P in ("P_BM", "P_MWRA", "P_BM_E", "P_MWRA_E"):
            p(f"| {P} | {_v(hd.get('member', {}).get(P))} | {_v(hd.get('n', {}).get(P))} | "
              f"{_v(hd.get('p', {}).get(P))} |")
        p(f"\np_H = {_v(hd.get('p_H'))}; disclosure table determined = {hd.get('determined')}; "
          f"Q_contra = {_v(hd.get('Q_contra'))}")
    n6 = docs.get("n6")
    if n6 and "summary" in n6:
        p("")
        p("## N6: the eclipse at Ithaca (reported, not a rule input)")
        p("")
        p("Each Delta-T model taken as a Gaussian with its stated sigma (an assumption, DESIGN 0).")
        p("")
        p("| site | eclipse | P(total) canon frame, mixture | own frames, mixture | P(smag >= 0.9) canon, mixture |")
        p("|---|---|---|---|---|")
        for sk, d in n6["summary"].items():
            for ek in ("1178BC", "1131BC"):
                if ek in d:
                    e = d[ek]
                    own = e.get("P_total_own") or {}
                    p(f"| {sk} | {ek} | {_v(e['P_total_canon'].get('mixture'))} | {_v(own.get('mixture'))} | "
                      f"{_v(e['P_mag09_canon'].get('mixture'))} |")
            if "joint" in d:
                p(f"| {sk} | joint (common offset) | {_v(d['joint'].get('canon', {}).get('mixture'))} | "
                  f"{_v(d['joint'].get('own', {}).get('mixture'))} | |")
    p("")
    p("## Expected on known facts (LEAN.md; not a prediction, never counted as a success)")
    p("")
    for k, v in EXPECT:
        p(f"- {k}: {v}")
    p("")
    p("## Provenance")
    p("")
    for k, d in prov.items():
        p(f"- `{d['path']}` sha256 `{d['sha256']}`")
    missing = [FILES[k] for k in FILES if k not in prov]
    if missing:
        p(f"- not present: {', '.join('`' + m + '`' for m in missing)}")
    md = "\n".join(L) + "\n"
    Path(out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(out_md).write_text(md, encoding="utf-8")
    js = dict(labels=labels, qualifiers=quals, notes=notes, headline=head, inputs=q, sources=src,
              provenance=prov, thresholds_file=str(RULE))
    Path(out_json).write_text(json.dumps(js, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return labels, quals, notes, md


def main(argv=None):
    ap = argparse.ArgumentParser(description="the lean verdict (LEAN.md; DESIGN 9.2)")
    ap.add_argument("--results", default=str(ROOT / "results"))
    ap.add_argument("--out", help="VERDICT.md path (default <results>/VERDICT.md)")
    a = ap.parse_args(argv)
    out_md = Path(a.out) if a.out else Path(a.results) / "VERDICT.md"
    labels, quals, notes, md = write(a.results, out_md, out_md.with_name("verdict.json"))
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
