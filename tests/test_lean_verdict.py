"""
Tests of odybench/lean/verdict.py (agent L2): the lean rule of LEAN.md
("The rule, restricted"), on synthetic input sets adapted from DESIGN 9.5.

    cd C:\\Projects\\odybench && py tests/test_lean_verdict.py

The null side of every set is the design-stage estimate of 2.6/2.9 (as 9.5's
S0), and p_H, p_H,min and Q_record are computed from the pools' counts by
odybench.lean.heldout, as 9.5 says ("each pool's p from the target's pass
pattern and the pool's counts").

Sets of 9.5 kept (with the lean outcome; differences from 9.2 in brackets):
  S0, S0x [3a not tested, so {inconclusive}], S0y [{3b}], S1, S1b, S2nm, S3b,
  S5, S7, S8, S10, S11 [no Q_H], S12, S13, S15 [{1, 3b}: label 4 is not tested;
  as in 9.2, 3b does not veto label 1 (LEAN.md as corrected 2026-10-09)], S18.
Sets dropped because they need deferred inputs:
  S2 and S6 (pct_N4: N4 deferred; S6 is replaced by S6g, label 1 with label 2
  by its G leg), S3a, S9, S16 and S20 (gate 3a, Q_attain3a), S4, S4b, S4c,
  S6b, S14, S14b, S14c (the negatives, label 4, Q_attain4), S17 (Q_attain3b),
  S19 (Q_H) -- the last three qualifiers are outside the lean rule's list.
Lean-only sets: L3b_notrun (gate 3b not built: label 1 still provisional),
  L0_notrun, Lmissing (inputs not supplied), Linstr_none (no instrument record).

Reachable in the lean rule: labels 1, 2 (no match), 2 (ordinary), 3b,
inconclusive and BLOCKED; qualifiers Q_attain, Q_record, Q_contra, Q_exch,
Q_tol, Q_slot and Q_BM.  On the design-stage null side, label 2 (ordinary) is
reachable only by a branch test (S10, S6g): with the pct_N4 leg deferred it
needs G_BM,lo >= 0.20 under all six slot variants, and the design-stage lower
bounds are 0.087-0.203.  Q_attain is likewise a branch test (S5, S13).

A second check runs results/design-revision-v8/verdict_trace.py's
transcription of 9.2 on every one of its 31 sets and requires the lean rule
to give 9.2's output restricted as LEAN.md says.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np  # noqa: E402
from odybench.lean import heldout as H  # noqa: E402
from odybench.lean import verdict as V  # noqa: E402

THR = json.loads((ROOT / "data" / "prereg" / "verdict_rule.json").read_text(encoding="utf-8"))["thresholds"]
DET = {"H3": None, "H4": "fail"}
G_BM = {"v0": (0.224, 0.139, 0.344), "v1": (0.140, 0.087, 0.215), "v2": (0.211, 0.131, 0.324),
        "v3": (0.278, 0.172, 0.427), "v4": (0.182, 0.112, 0.279), "v5": (0.327, 0.203, 0.504)}
POOLS = {"P_BM": dict(n=76, h3=14, h4=1, both=1), "P_MWRA": dict(n=43, h3=8, h4=1, both=0),
         "P_BM_E": dict(n=49, h3=9, h4=1, both=1), "P_MWRA_E": dict(n=28, h3=6, h4=1, both=0)}
LEGS = V.LEGS3B


def _arrays(c):
    n, a3, a4, ab = c["n"], c["h3"], c["h4"], c["both"]
    h3 = np.array([True] * ab + [True] * a3 + [False] * a4 + [False] * (n - ab - a3 - a4))
    h4 = np.array([True] * ab + [False] * a3 + [True] * a4 + [False] * (n - ab - a3 - a4))
    return h3, h4


def build(pattern="h3", member=None, pools=None, determined=DET, **kw):
    """A lean input set: the null side from pool counts, the target side from
    the pattern (both, h4, h3, none) and membership."""
    pools = copy.deepcopy(pools or POOLS)
    member = member or {P: True for P in H.POOLS}
    t3, t4 = pattern in ("both", "h3"), pattern in ("both", "h4")
    arr = {P: _arrays(pools[P]) for P in H.POOLS}
    p = {P: H.p_pool(*arr[P], t3, t4, member[P])["p"] for P in H.POOLS}
    lat = {pat: dict(p_H=max(H.p_pool(*arr[P], pat in ("both", "h3"), pat in ("both", "h4"))["p"]
                             for P in H.POOLS)) for pat in H.PATTERNS}
    qrec, _ = H.q_record(lat, determined)
    qcon, _ = H.q_contra({"H3": t3, "H4": t4}, determined)
    q = dict(INSTR=True, T0_pass=True, T0="RE", r_Ody=0.0815, G_BM=copy.deepcopy(G_BM),
             p_H_min=max((1 + pools[P]["both"]) / (1 + pools[P]["n"]) for P in H.POOLS),
             Q_record=qrec, Q_exch=False, p_H=max(p.values()), Q_contra=qcon,
             gate3b_run=True, seen_ALM_SL={leg: 7 for leg in LEGS}, rec_ALM_BM=3)
    q.update(kw)
    return q


def legs(k):
    return {leg: k for leg in LEGS}


BASEQ = ["Q_BM", "Q_tol", "Q_slot", "Q_record"]
SETS = {
    # name: (input set, labels, qualifiers, mark)
    "S0": (build(), ["inconclusive"], BASEQ, "realisable"),
    "S0x": (build(seen_ALM_SL=legs(6)), ["inconclusive"], BASEQ, "realisable"),
    "S0y": (build(seen_ALM_SL=legs(5)), ["3b"], BASEQ, "realisable"),
    "S1": (build("both"), ["1"], ["Q_contra"] + BASEQ, "realisable"),
    "S1b": (build("h4"), ["inconclusive"], ["Q_contra"] + BASEQ, "realisable"),
    "S2nm": (build(r_Ody=0.0), ["2 (no match)"], BASEQ, "realisable"),
    "S3b": (build(seen_ALM_SL=legs(3)), ["3b"], BASEQ, "realisable"),
    "S5": (build("both", pools=dict(POOLS, P_BM=dict(n=76, h3=11, h4=1, both=4))), ["inconclusive"],
           ["Q_contra", "Q_BM", "Q_tol", "Q_slot", "Q_attain", "Q_record"], "branch"),
    "S6g": (build("both", G_BM={v: (0.327, 0.203, 0.504) for v in V.SLOTS}), ["1", "2 (ordinary)"],
            ["Q_contra", "Q_BM", "Q_tol", "Q_record"], "branch"),
    "S7": (build(INSTR=False), ["BLOCKED"], [], "realisable"),
    "S8": (build("both", T0_pass=False, T0="NR"), ["inconclusive"], ["Q_contra"] + BASEQ, "realisable"),
    "S10": (build(G_BM={v: (0.327, 0.203, 0.504) for v in V.SLOTS}), ["2 (ordinary)"],
            ["Q_BM", "Q_tol", "Q_record"], "branch"),
    "S11": (build("both", rec_ALM_BM=7), ["1"], ["Q_contra", "Q_tol", "Q_slot", "Q_record"], "realisable"),
    "S12": (build("both", member={"P_BM": True, "P_MWRA": False, "P_BM_E": True, "P_MWRA_E": False}),
            ["inconclusive"], ["Q_contra"] + BASEQ, "realisable"),
    "S13": (build("both", pools=dict(POOLS, P_MWRA_E=dict(n=28, h3=4, h4=1, both=2))), ["inconclusive"],
            ["Q_contra", "Q_BM", "Q_tol", "Q_slot", "Q_attain", "Q_record"], "branch"),
    "S15": (build("both", seen_ALM_SL=legs(3)), ["1", "3b"], ["Q_contra"] + BASEQ, "realisable"),
    "S18": (build("both", Q_exch=True), ["1"], ["Q_contra", "Q_exch"] + BASEQ, "branch"),
    "L3b_notrun": (build("both", gate3b_run=False, seen_ALM_SL=None, rec_ALM_BM=None), ["1"],
                   ["Q_contra", "Q_tol", "Q_slot", "Q_record"], "lean"),
    "L0_notrun": (build(gate3b_run=False, seen_ALM_SL=None), ["inconclusive"], BASEQ, "lean"),
    "Lmissing": (build(r_Ody=None, p_H=None, Q_exch=None, G_BM=None), ["inconclusive"],
                 ["Q_BM", "Q_record"], "lean"),
    "Linstr_none": (build(INSTR=None), ["BLOCKED"], [], "lean"),
}


def test_sets():
    for name, (q, labels, quals, mark) in SETS.items():
        L, Q, notes = V.decide(q, THR)
        assert L == labels, (name, L, labels)
        assert Q == quals, (name, Q, quals)
        if "1" in L:
            assert any(V.PROVISIONAL in n for n in notes), (name, notes)
        if L != ["BLOCKED"]:
            assert any(n.startswith("3a: not tested") for n in notes)
            assert any(n.startswith("4: not tested") for n in notes)
        if name == "Lmissing":
            for k in ("label 1: not evaluated", "Q_exch: not evaluated", "Q_tol, Q_slot",
                      "label 2's no-match leg: not evaluated"):
                assert any(n.startswith(k) for n in notes), (k, notes)
        if name == "L3b_notrun":
            assert any("3b: not run" in n for n in notes) and any("3b not run" in n for n in notes)


def test_every_lean_outcome_reached():
    seen_l, seen_q = set(), set()
    for q, *_ in SETS.values():
        L, Q, _ = V.decide(q, THR)
        seen_l |= set(L)
        seen_q |= set(Q)
    assert seen_l == {"1", "2 (no match)", "2 (ordinary)", "3b", "inconclusive", "BLOCKED"}, seen_l
    assert seen_q == set(V.LEAN_QUALIFIERS), seen_q
    # realisable on the design-stage null side: every label except 2 (ordinary); every qualifier except Q_attain
    real_l, real_q = set(), set()
    for q, _, _, mark in SETS.values():
        if mark == "realisable":
            L, Q, _ = V.decide(q, THR)
            real_l |= set(L)
            real_q |= set(Q)
    assert real_l == {"1", "2 (no match)", "3b", "inconclusive", "BLOCKED"}, real_l
    assert real_q == set(V.LEAN_QUALIFIERS) - {"Q_attain", "Q_exch"}, real_q


def test_design_stage_numbers():
    q = SETS["S0"][0]
    assert abs(q["p_H_min"] - 0.0400) < 1e-4 and abs(q["p_H"] - 0.2759) < 1e-4
    assert abs(SETS["S1"][0]["p_H"] - 0.0400) < 1e-4 and abs(SETS["S1b"][0]["p_H"] - 0.0690) < 1e-4
    assert abs(SETS["S5"][0]["p_H_min"] - 5 / 77) < 1e-12
    assert abs(SETS["S13"][0]["p_H_min"] - 3 / 29) < 1e-12
    assert SETS["S12"][0]["p_H"] == 1.0


def test_headline_and_numbers():
    L, Q, _ = V.decide(SETS["S18"][0], THR)
    h = V.headline(L, Q)
    assert h[0].startswith("Q_contra") and h[1].startswith("Label 1") and "Q_exch" in h[1]
    L, Q, _ = V.decide(SETS["S6g"][0], THR)
    assert any("B&M's own match is not what shows it" in x for x in V.headline(L, Q))
    rows = V.numbers(SETS["S0"][0], THR)
    names = [r[0] for r in rows]
    assert "p_H" in names and "G_BM,lo(v5)" in names and "seen_ALM_SL (six legs)" in names
    assert V.headline(["BLOCKED"], []) == ["BLOCKED: no verdict is read"]


def _verdict_trace():
    p = ROOT / "results" / "design-revision-v8" / "verdict_trace.py"
    spec = importlib.util.spec_from_file_location("verdict_trace_v8", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_against_design_9_2_restricted():
    """verdict_trace.py's 9.2 on its own 31 sets, restricted as LEAN.md says,
    equals the lean rule on the same inputs."""
    vt = _verdict_trace()
    for name, (q9, _mark) in vt.SETS.items():
        L9, Q9, extra = vt.decide(q9)
        det = {k: ("pass" if v else "fail") for k, v in q9["determined"].items()}
        t = {"H3": q9["pattern"] in ("both", "h3"), "H4": q9["pattern"] in ("both", "h4")}
        lean_q = dict(
            INSTR=q9["INSTR"], T0_pass=q9["T0_pass"], T0=q9["T0"], r_Ody=q9["r_Ody"],
            G_BM={v: x[:3] for v, x in q9["G_BM"].items()},
            p_H_min=max(vt.p_min(q9["pools"][P]) for P in vt.POOLS),
            Q_record=vt.q_record(q9["pools"], q9["determined"]), Q_exch=q9["Q_exch"],
            p_H=vt.p_H_of(q9["pools"], q9["pattern"], q9["member"])[1],
            Q_contra=H.q_contra(t, det)[0],
            gate3b_run=True, seen_ALM_SL=[q9["gate3b"][f"{a}_{s}"] for a in ("bf", "st")
                                          for s in ("fine", "mid", "coarse")],
            rec_ALM_BM=q9["rec_ALM_BM"])
        L, Q, _ = V.decide(lean_q, THR)
        if L9 == "BLOCKED":
            assert L == ["BLOCKED"], name
            continue
        g2_all = all(q9["G_BM"][v][1] >= 0.20 for v in vt.SLOTS)
        fire3b = min(q9["gate3b"].values()) < 6
        exp = set(L9) - {"3a", "4"}
        if "2 (ordinary)" in exp and not g2_all:
            exp.discard("2 (ordinary)")             # it came from the pct_N4 leg, deferred
        exp = exp or {"inconclusive"}
        assert set(L) == exp, (name, L, L9)
        assert set(Q) == set(Q9) & set(V.LEAN_QUALIFIERS), (name, Q, Q9)



def _write_tree(td, alm=True, instr=True):
    """A synthetic results tree with S0's numbers, in the shapes verdict.py reads."""
    q = SETS["S0"][0]
    (td / "attain").mkdir()
    (td / "t0").mkdir()
    (td / "heldout").mkdir()
    att = {"G_BM": {v: {"G": g, "lo": lo, "hi": hi} for v, (g, lo, hi) in G_BM.items()},
           "heldout": {"null_side": {"p_H_min": q["p_H_min"], "Q_record": q["Q_record"], "Q_exch": False}}}
    (td / "attain" / "attain.json").write_text(json.dumps(att), encoding="utf-8")
    (td / "t0" / "t0.json").write_text(json.dumps({"T0_pass": True, "T0": "RE", "r_Ody": 0.0815}),
                                       encoding="utf-8")
    hd = {"p_H": q["p_H"], "Q_contra": False, "p": {P: 0.25 for P in H.POOLS}, "member": {P: True for P in H.POOLS},
          "n": {"P_BM": 76, "P_MWRA": 43, "P_BM_E": 49, "P_MWRA_E": 28}, "determined": DET,
          "null_side": {"Q_record": True, "Q_exch": False, "p_H_min": q["p_H_min"]}}
    (td / "heldout" / "heldout.json").write_text(json.dumps(hd), encoding="utf-8")
    if alm:
        (td / "alm").mkdir()
        (td / "alm" / "alm.json").write_text(json.dumps({"gate3b_run": True, "seen_ALM_SL": {l: 9 for l in LEGS},
                                                         "rec_ALM_BM": 4}), encoding="utf-8")
    if instr:
        (td / "instrument").mkdir()
        (td / "instrument" / "summary.json").write_text(json.dumps({"INSTR": True}), encoding="utf-8")
    n6 = ROOT / "results" / "build-L2" / "n6" / "n6.json"
    if n6.exists():
        (td / "n6").mkdir()
        (td / "n6" / "n6.json").write_text(n6.read_text(encoding="utf-8"), encoding="utf-8")


def test_script_on_synthetic_trees():
    import tempfile
    spec = importlib.util.spec_from_file_location("verdict_script", ROOT / "verdict.py")
    vs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vs)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        _write_tree(td)
        L, Q, notes, md = vs.write(td, td / "VERDICT.md", td / "verdict.json")
        assert L == ["inconclusive"] and Q == ["Q_BM", "Q_tol", "Q_slot", "Q_record"], (L, Q)
        assert (td / "VERDICT.md").exists() and "## Every number beside its threshold" in md
        js = json.loads((td / "verdict.json").read_text(encoding="utf-8"))
        assert js["sources"]["p_H"] == "heldout/heldout.json:p_H"
        assert js["sources"]["Q_record"].startswith("attain/attain.json:heldout.null_side")
        assert js["sources"]["seen_ALM_SL"] == "alm/alm.json:seen_ALM_SL"
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        _write_tree(td, alm=False)
        L, Q, notes, md = vs.write(td, td / "VERDICT.md", td / "verdict.json")
        assert L == ["inconclusive"] and "Q_BM" not in Q
        assert any(n.startswith("3b: not run") for n in notes) and "3b (not run)" in md
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        _write_tree(td, instr=False)
        L, Q, notes, md = vs.write(td, td / "VERDICT.md", td / "verdict.json")
        assert L == ["BLOCKED"]


if __name__ == "__main__":
    import time
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            t0 = time.time()
            try:
                fn()
                print(f"PASS {name} ({time.time() - t0:.1f} s)")
            except Exception as exc:          # noqa: BLE001
                fails += 1
                import traceback
                traceback.print_exc()
                print(f"FAIL {name}: {exc!r}")
    print("all passed" if not fails else f"{fails} failed")
    sys.exit(1 if fails else 0)
