"""
Tests of odybench/lean/almagest.py and tools/build_regimes.py (gate 3b and
Q_BM of the lean run; agent L3; LEAN.md, DESIGN 6.4, 6.3.2, 10.3).

    cd C:\\Projects\\odybench && py tests/test_lean_almagest.py

(no pytest on this machine; also collectable by pytest).  Nothing here runs a
control search on the real sky (LEAN.md stage 1): the searches are on
synthetic sets, and the real-sky checks compare this module's sky code with
brute-force ephem scans at dates before -800, where no control truth lies.
"""
import builtins
import importlib.util
import json
import math
import re
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import calendar as C  # noqa: E402
from odybench.lean import almagest as A  # noqa: E402

REG = ROOT / "data" / "prereg" / "almagest_regimes.json"
CLUES = ROOT / "data" / "prereg" / "controls_almagest.json"
ALM_ROWS_OUT = ROOT / "results" / "design-revision-v8" / "alm_rows.out.txt"
SRC = ROOT / "odybench" / "lean" / "almagest.py"


def _build_regimes():
    spec = importlib.util.spec_from_file_location("build_regimes", ROOT / "tools" / "build_regimes.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _reg():
    return json.loads(REG.read_text(encoding="utf-8"))


# ------------------------------------------------------------ the regime file

def test_build_regimes_selftest():
    assert _build_regimes().selftest(verbose=False)


def test_projection_equals_alm_rows():
    """I13(f): the builder's projection and held-out lists equal alm_rows.out.txt (revision 8)."""
    br = _build_regimes()
    clues = json.loads(CLUES.read_text(encoding="utf-8"))["clues"]
    p = br.project(clues)
    doc = {"sets": {sid: {"projection": dict(v["projection"]), "held_out": dict(v["held_out"])} for sid, v in p.items()}}
    assert br.compare_alm_rows(doc, ALM_ROWS_OUT) == []


def test_regime_file_lists_options_and_predicates():
    br = _build_regimes()
    reg = _reg()
    clues_doc = json.loads(CLUES.read_text(encoding="utf-8"))
    assert reg["clue_file_sha256"] == A._sha256(CLUES)
    assert br.compare_alm_rows(reg, ALM_ROWS_OUT) == []
    assert br.check_named_options(reg, clues_doc) == []
    assert reg["counted_sets"] == ["ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H", "ALM-I", "ALM-J",
                                   "ALM-K", "ALM-L"]
    ops = A.operational_view(clues_doc)
    for sid, s in reg["sets"].items():
        for regime, step in [("SL", st) for st in A.STEPS] + [("BM", None)]:
            for cid, opt, params in A.run_rows(ops[sid], s, regime, step):
                pred = s["row_predicates"][cid]
                A.instant_key(pred["instant"])
                if opt not in ("phase_class", "equinox_tol"):
                    assert pred["side"] in ("morning", "evening"), cid


def test_regime_values_follow_6_4():
    """Spot checks of 6.4's table on the written file."""
    reg = _reg()
    b, h, a = reg["sets"]["ALM-B"], reg["sets"]["ALM-H"], reg["sets"]["ALM-A"]
    assert b["regimes"]["BM"]["ALM-B.1"] == {"option": "bm_venus_lead", "params": {"lead_min": 90.0}}
    assert b["regimes"]["SL"]["coarse"]["ALM-B.1"]["option"] == "ge_before_same_apparition"
    assert b["regimes"]["SL"]["coarse"]["ALM-B.7"]["params"]["tolerance_days"] == 2
    assert b["regimes"]["BM"]["ALM-B.7"]["params"]["tolerance_days"] == 1
    assert h["regimes"]["BM"]["ALM-H.1"] == {"option": "bm_mwra_k", "params": {"k_days": 1.5}}
    assert h["regimes"]["BM"]["ALM-H.4"] == {"option": "ge_true_k", "params": {"k_days": 1.5}}
    assert h["regimes"]["SL"]["fine"]["ALM-H.1"]["params"]["min_minutes_between_body_and_sun_horizon_crossings"] == 30
    assert a["regimes"]["SL"]["coarse"]["ALM-A.7"]["params"]["k_days"] == a["tolerances"][
        "greatest_elongation_days"]["mercury"]["coarse"]
    for sid, s in reg["sets"].items():
        ge = s["tolerances"]["greatest_elongation_days"]
        for body, v in ge.items():
            assert v["fine"] <= v["mid"] <= v["coarse"]
            assert v["coarse"] == math.ceil(v["coarse"])
    # A.2, A.5, A.10, B.2, B.5 and B.9 at none; B.7 kept (revision 8)
    for cid in ("ALM-A.2", "ALM-A.5", "ALM-A.10"):
        assert a["projection"][cid] == "none"
    for cid in ("ALM-B.2", "ALM-B.5", "ALM-B.9"):
        assert b["projection"][cid] == "none"
    assert b["projection"]["ALM-B.7"] == "phase_class"


def test_row_predicates_by_rule():
    rp = {cid: p for s in _reg()["sets"].values() for cid, p in s["row_predicates"].items()}
    assert rp["ALM-A.1"] == {"body": "mercury", "side": "evening", "instant": {"kind": "lat", "hours": 19.5},
                             "words": ["Mercury", "evening star", "4.5 equinoctial hours before midnight"]}
    assert rp["ALM-A.9"]["instant"] == {"kind": "lat", "hours": 5.0} and rp["ALM-A.9"]["body"] == "jupiter"
    assert rp["ALM-B.7"]["instant"] == {"kind": "lat", "hours": 6.75}
    assert rp["ALM-E.3"]["instant"] == {"kind": "lat", "hours": 13.0}
    assert rp["ALM-J.4"]["instant"] == {"kind": "night_hour", "hour": 12, "point": "middle"}
    for cid in ("ALM-D.3", "ALM-L.6", "ALM-H.4"):
        assert rp[cid]["instant"] == {"kind": "sun_alt", "deg": -8.0, "part": "evening"}, cid
    for cid in ("ALM-G.1", "ALM-L.1", "ALM-J.1", "ALM-K.4", "ALM-I.1"):
        assert rp[cid]["instant"] == {"kind": "sun_alt", "deg": -8.0, "part": "morning"}, cid


# ------------------------------------------------------------ blinding

def test_operational_view_has_no_prose():
    ops = A.operational_view(json.loads(CLUES.read_text(encoding="utf-8")))
    assert sorted(ops) == [f"ALM-{c}" for c in "ABCDEFGHIJKL"]
    assert sum(len(s["rows"]) for s in ops.values()) == 72
    for s in ops.values():
        for r in s["rows"]:
            assert set(r) <= set(A.ROW_KEYS)
            for o in r["fork_options"]:
                assert set(o) <= set(A.OPTION_KEYS)


def test_search_code_reads_no_truth():
    """Static: the truth file is named once and opened by _Harness only; no
    search code reads a statement, licence, ref or note; the Nabonassar epoch
    (JD 1448638) appears nowhere (I13)."""
    src = SRC.read_text(encoding="utf-8")
    assert src.count('PREREG / "controls_almagest_truth.json"') == 1
    # one path to a truth-side JSON in code (the slack table's slack.json is named without "truth")
    assert len(re.findall(r"/ \"[^\"]*truth[^\"]*\.json\"", src)) == 1
    assert "1448638" not in src
    # the truth values (_day0) live in _Harness and the scoring-side _truth_rows only
    h0, h1 = src.index("class _Harness"), src.index("def _clusters")
    t0, t1 = src.index("def _truth_rows"), src.index("def aggregate")
    for m in re.finditer(r"_day0", src):
        assert h0 < m.start() < h1 or t0 < m.start() < t1, src[m.start() - 80: m.start() + 20]
    for key in ("statement", "licence_words", "license_check", "notes", "text_file"):
        assert f'["{key}"]' not in src and f"get(\"{key}\")" not in src, key
    # TRUTH is used as the harness default only
    uses = [m.start() for m in re.finditer(r"\bTRUTH\b", src)]
    harness = src.index("class _Harness")
    run_def = src.index("def run(")
    for u in uses:
        line = src[src.rfind("\n", 0, u) + 1: src.find("\n", u)]
        assert line.startswith("TRUTH =") or (harness < u < src.index("def gate_window", harness)) \
            or (run_def < u < src.index('"""', run_def)), line


def test_search_runs_without_the_truth_file():
    """Runtime: f_array on a synthetic sky never opens a truth file."""
    real_open = builtins.open
    real_read = Path.read_text

    def guard_open(file, *a, **k):
        assert "truth" not in str(file), file
        return real_open(file, *a, **k)

    def guard_read(self, *a, **k):
        assert "truth" not in str(self), self
        return real_read(self, *a, **k)
    builtins.open, Path.read_text = guard_open, guard_read
    try:
        tab = A._synthetic_table()
        ops = {"set": "SYN", "rows": [
            {"clue_id": "S.1", "set": "SYN", "kind": "planet", "record": "R1", "day_offset": 0,
             "fork_options": [{"option": "ge_true_k", "primary": True, "operational": {"k_days": [1, 2]}}]},
            {"clue_id": "S.2", "set": "SYN", "kind": "season", "record": "R2", "day_offset": 30,
             "fork_options": [{"option": "equinox_tol", "primary": True, "operational": {"tolerance_days": [1, 2]}}]}]}
        reg_set = {"regimes": {"BM": {"S.1": {"option": "ge_true_k", "params": {"k_days": 1.5}},
                                      "S.2": {"option": "equinox_tol", "params": {"tolerance_days": 1}}}},
                   "row_predicates": {"S.1": {"body": "mercury", "side": "evening",
                                              "instant": {"kind": "sun_alt", "deg": -8.0, "part": "evening"}},
                                      "S.2": {"body": "sun", "side": None, "instant": {"kind": "lat", "hours": 13.0}}}}
        f, cov, detail = A.f_array(tab, ops, reg_set, A.run_rows(ops, reg_set, "BM"))
        assert cov.sum() > 3000 and (f[A.P_PASS][cov] == 0).sum() >= 0
    finally:
        builtins.open, Path.read_text = real_open, real_read


def test_no_datetime_in_l3_files():
    # the numpy type's name is assembled, so that test_calendar's own ban scan does not flag this file
    pat = re.compile(r"^\s*(import\s+datetime|from\s+datetime\s+import)|" + "datetime" + "64", re.M)
    for p in (SRC, ROOT / "almagest.py", ROOT / "tools" / "build_regimes.py"):
        assert not pat.search(p.read_text(encoding="utf-8")), p


# ------------------------------------------------------------ windows, scoring, Delta-T

def test_selftest_synthetic():
    assert A.selftest(verbose=False, real_sky=False)


def test_harness_windows_with_a_synthetic_truth():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "fake_truth.json"
        p.write_text(json.dumps({"sets": [{"set": "ALM-A", "day0_civil_jd_noon": 1700000},
                                          {"set": "ALM-K", "day0_civil_jd_noon": 1650000}]}), encoding="utf-8")
        h = A._Harness(p)
        for sid, t in (("ALM-A", 1700000), ("ALM-K", 1650000)):
            a = h.gate_window(sid)
            days = A.window_jdns(a)
            assert t in days and len(days) == 49674
            u = A._rng("control_window", sid).random()
            assert abs(a - (t - u * A.W_DAYS)) < 1e-9
            sw = h.sensitivity_windows(sid)
            assert len(sw) == 20 and all(t in A.window_jdns(x) for x in sw)
        f = np.ones(200000, dtype=np.int16)
        f[1700000 - 1600000] = 0
        sc = h.score("ALM-A", f, np.ones(200000, dtype=bool), 1600000, h.gate_window("ALM-A"))
        assert sc["S0"] == 1 and sc["seen_st"] and sc["seen_bf"] and sc["unique_B"]


def test_null_windows_every_counted_set():
    ops = A.operational_view(json.loads(CLUES.read_text(encoding="utf-8")))
    w = json.loads((ROOT / "data" / "prereg" / "windows.json").read_text(encoding="utf-8"))["spans"]
    lo = C.jd_from_julian(w["null_window_range"]["years"][0], 1, 1)
    hi = C.jd_from_julian(w["null_window_range"]["years"][1] + 1, 1, 1) + 0.5
    for sid in _reg()["counted_sets"]:
        mn, mx = A._offset_range(ops[sid])
        nw = A.null_windows(sid, mn, mx)
        assert len(nw) == 21 and nw == A.null_windows(sid, mn, mx)
        assert all(lo <= a and a + A.W_DAYS <= hi for a in nw)
        assert all(a + A.W_DAYS + mx <= hi for a in nw)


def test_p_mix_exact_against_quadrature():
    y = np.array([-300.0])
    mu, sg = A.dt_models(y)
    lo, hi = A.dt_ref(y) - 500.0, A.dt_ref(y) + 200.0
    x = np.linspace(float(lo[0]), float(hi[0]), 200001)
    pdf = np.mean([np.exp(-0.5 * ((x - mu[i, 0]) / sg[i, 0]) ** 2) / (sg[i, 0] * math.sqrt(2 * math.pi))
                   for i in range(4)], axis=0)
    quad = float(np.sum((pdf[1:] + pdf[:-1]) * 0.5 * np.diff(x)))
    assert abs(float(A.p_mix_interval(y, lo, hi)[0]) - quad) < 1e-9
    assert np.all(A.dt_band(np.array([-1000.0, 0.0, 241.0])) > 0)


def test_record_offsets_and_cruxes():
    ops = A.operational_view(json.loads(CLUES.read_text(encoding="utf-8")))
    a_pr, a_em = A.record_offsets(ops["ALM-A"]["rows"]), A.record_offsets(ops["ALM-A"]["rows"], "mean_sun_emended")
    assert a_pr["IX.9.4"] == 52 and a_em["IX.9.4"] == 49 and a_pr["XI.2.2"] == a_em["XI.2.2"] == 55
    h_pr, h_em = A.record_offsets(ops["ALM-H"]["rows"]), A.record_offsets(ops["ALM-H"]["rows"], "mean_sun_emended")
    assert h_pr["IX.7.11"] == 102 and h_em["IX.7.11"] == 72 and h_pr["IX.7.14"] == 192
    assert A.record_offsets(ops["ALM-K"]["rows"])["IX.7.15"] == 2902


def test_run_rows_regimes():
    reg, ops = _reg(), A.operational_view(json.loads(CLUES.read_text(encoding="utf-8")))
    bm = A.run_rows(ops["ALM-B"], reg["sets"]["ALM-B"], "BM")
    assert [(c, o) for c, o, _ in bm] == [("ALM-B.1", "bm_venus_lead"), ("ALM-B.7", "phase_class")]
    sl = A.run_rows(ops["ALM-E"], reg["sets"]["ALM-E"], "SL", "fine")
    assert [(c, o, p) for c, o, p in sl] == [("ALM-E.1", "ge_true_k", {"k_days": 20.6}),
                                             ("ALM-E.3", "equinox_tol", {"tolerance_days": 2})]
    names = [r[0] for r in A._runs_for_set(ops["ALM-A"], reg["sets"]["ALM-A"])]
    assert "SL:coarse" in names and "SL_side:fine" in names and "BM" in names
    assert "sens:projection_rev7:SL:coarse" in names and "sens:cruxes_emended:BM" in names


def test_needs_cover_every_row():
    needs = A.needs_from_regimes(_reg())
    assert set(needs["lat_hours"]) >= {19.5, 4.75, 5.0, 6.75, 13.0}
    assert ("jupiter", "lat:5") in [tuple(x) for x in needs["alts"]]
    assert ("mars", "sun-8:morning") in [tuple(x) for x in needs["alts"]]
    assert "lat:6.75" in needs["moon_keys"]


# ------------------------------------------------------------ the real sky, far from any control

def test_real_sky_synthetic_set_and_brute_force():
    fails = []

    def chk(c, msg):
        if not c:
            fails.append(msg)
    A._selftest_real_sky(chk, False)
    assert not fails, fails


def test_slack_row_on_a_synthetic_record():
    """slack_row's greatest-elongation offset and set lag for a made-up evening
    record of Mercury at -850 (not a control record)."""
    lat, lon = A.site("alexandria")
    j0 = int(C.jdn_from_julian(-850, 6, 1))
    t = A._time_tt(np.array([float(j0)]))
    ge = None
    grid = j0 + np.arange(0.0, 130.0, 1.0)
    se = A._signed_elong_dlon("mercury", grid)[0]
    i = int(np.argmax(se))
    ge = float(A._refine_max(lambda x: A._signed_elong_dlon("mercury", x)[0], np.array([grid[i]]))[0])
    dtv = float(A.dt_ref(A._epoch_of_jd(ge)))
    rec = {"id": "SYN", "reading": "printed", "body": "mercury", "rs_kind": "set lag",
           "jd_ut": ge - dtv / 86400.0 + 2.0}
    r = A.slack_row(rec, lat, lon)
    assert abs(r["off_ge_true_d"] - 2.0) < 0.01, r
    assert r["rs_kind"] == "set lag" and np.isfinite(r["rs_min"])
    assert r["elong_true"] > 0 and r["ge_true_val"] >= r["elong_true"]
    assert "az_max_off_d" in r and "az_min_off_d" in r
    del t


def test_slack_table_on_synthetic_records():
    """slack_table end to end on three made-up Mercury records at -850 (a fake
    slack.json, note Summary and clue file): the |record - GE| summary and the
    leave-one-set-out ceilings it implies."""
    j0 = int(C.jdn_from_julian(-850, 6, 1))
    grid = j0 + np.arange(0.0, 400.0, 1.0)
    se = A._signed_elong_dlon("mercury", grid)[0]
    i = np.nonzero((se[1:-1] > se[:-2]) & (se[1:-1] >= se[2:]) & (se[1:-1] > 0))[0] + 1
    ges = A._refine_max(lambda x: A._signed_elong_dlon("mercury", x)[0], grid[i[:3]])
    offs = (0.45, -2.0, 3.25)
    recs = []
    for k, (g, o) in enumerate(zip(ges, offs)):
        dtv = float(A.dt_ref(A._epoch_of_jd(g))) / 86400.0
        recs.append({"id": f"R{k + 1}", "reading": "printed", "body": "mercury", "rs_kind": "set lag",
                     "site": "Alexandria", "jd_ut": float(g) - dtv + o})
    note = ("x\n**Summary: |record - true greatest elongation| for records the text puts at or about greatest "
            "elongation**\n\n- mercury (n = 3; none as printed): true Sun <= 1 d: 1/3\n  - mean Sun: <= 1 d: 1/3\n"
            "  - sorted: R1 0.5, R2 2.0, R3 3.3\n\n")
    saved = (A.SLACK_TRUTH, A.SLACK_NOTE, A.CLUES)
    try:
        with tempfile.TemporaryDirectory() as d:
            A.SLACK_TRUTH, A.SLACK_NOTE, A.CLUES = Path(d) / "s.json", Path(d) / "n.md", Path(d) / "c.json"
            A.SLACK_TRUTH.write_text(json.dumps(recs), encoding="utf-8")
            A.SLACK_NOTE.write_text(note, encoding="utf-8")
            A.CLUES.write_text(json.dumps({"sets": [{"set": "SYN-X", "records": ["R1"]},
                                                    {"set": "SYN-Y", "records": ["R2", "R3"]}]}), encoding="utf-8")
            reg = {"sets": {"SYN-X": {"tolerances": {"greatest_elongation_days": {
                "mercury": {"fine": 3.3, "mid": 3.5, "coarse": 4.0}}}},
                "SYN-Y": {"tolerances": {"greatest_elongation_days": {
                    "mercury": {"fine": 0.5, "mid": 0.5, "coarse": 1.0}}}}}}
            st = A.slack_table(reg)
    finally:
        A.SLACK_TRUTH, A.SLACK_NOTE, A.CLUES = saved
    got = st["ge_summary_abs_days"]["mercury"]
    assert all(abs(got[f"R{k + 1}"] - abs(o)) < 0.01 for k, o in enumerate(offs)), got
    assert st["ceilings_agree_with_regime_file"], st["ceilings"]


def _synthetic_inputs(d, j0):
    """A synthetic clue file, regime file and truth file whose sets are built
    from the real sky around -850: their truths pass every row by construction."""
    lat, lon = A.site("alexandria")
    needs = {"lat_hours": [4.75, 13.0], "horizon_bodies": ["mercury", "venus"], "rise_az_bodies": ["mercury"],
             "alts": [], "moon_keys": []}
    tab = A.build_table("alexandria", j0, j0 + 1500, needs, workers=1, cache=False, chunk=500)
    dtv = lambda t: float(A.dt_ref(A._epoch_of_jd(t))) / 86400.0
    civil = lambda t_tt: int(math.floor(t_tt - dtv(t_tt) + 0.5 + lon / 360.0))
    ge = tab.events["ge:mercury:east"]
    ga = civil(ge[(ge > j0 + 500) & (ge < j0 + 1000)][0])
    ia = ga - tab.jdn0
    off = int(np.nonzero(tab.cols["venus:lead"][ia + 5:] >= 60.0)[0][0]) + 5
    gw = tab.events["ge:venus:west"]
    gw = gw[(gw > j0 + 300) & (gw < j0 + 1200)][0]
    iw = civil(gw) - tab.jdn0
    ib = iw + 10 + int(np.nonzero(tab.cols["venus:lead"][iw + 10:] >= 100.0)[0][0])
    eq = tab.events["equinox"]
    gc = civil(eq[(eq > j0 + 400) & (eq < j0 + 1100)][0])
    sets = [{"set": "SYN-A", "records": ["RA1", "RA2"]}, {"set": "SYN-B", "records": ["RB1"]},
            {"set": "SYN-C", "records": ["RC1"]}]
    clues = [
        {"clue_id": "SYN-A.1", "set": "SYN-A", "kind": "planet", "record": "RA1", "day_offset": 0,
         "statement": "Mercury is an evening star at its greatest eastern elongation (evening).",
         "fork_options": [{"option": "ge_true_k", "primary": True, "operational": {"k_days": [1, 2, 3]}},
                          {"option": "visible_only", "primary": False,
                           "operational": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]}}]},
        {"clue_id": "SYN-A.2", "set": "SYN-A", "kind": "interval", "record": "RA2", "day_offset": off,
         "fork_options": []},
        {"clue_id": "SYN-A.3", "set": "SYN-A", "kind": "planet", "record": "RA2", "day_offset": off,
         "statement": "Venus is a morning star (before dawn).",
         "fork_options": [{"option": "visible_only", "primary": True,
                           "operational": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]}}]},
        {"clue_id": "SYN-B.1", "set": "SYN-B", "kind": "planet", "record": "RB1", "day_offset": 0,
         "statement": "Venus is a morning star (4.75 equinoctial hours after midnight), past its greatest elongation.",
         "fork_options": [{"option": "ge_before_within_j", "primary": True, "operational": {"j_days": [15, 30, 60]}},
                          {"option": "ge_before_same_apparition", "primary": False,
                           "operational": {"bound": "same_apparition"}},
                          {"option": "visible_only", "primary": False,
                           "operational": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]}},
                          {"option": "bm_venus_lead", "primary": False, "operational": {"lead_min": [60, 90, 120]}}]},
        {"clue_id": "SYN-C.1", "set": "SYN-C", "kind": "season", "record": "RC1", "day_offset": 0,
         "statement": "The spring equinox, about one hour after noon.",
         "fork_options": [{"option": "equinox_tol", "primary": True, "operational": {"tolerance_days": [0.5, 1, 2]}}]},
    ]
    clue_doc = {"sets": sets, "clues": clues}
    cp = Path(d) / "syn_clues.json"
    cp.write_text(json.dumps(clue_doc), encoding="utf-8")
    br = _build_regimes()
    ka = {"fine": 5.5, "mid": 5.5, "coarse": 6.0}
    reg = {"clue_file_sha256": A._sha256(cp), "counted_sets": ["SYN-A", "SYN-B"], "reported_sets": ["SYN-C"],
           "sets": {}}
    for s in sets:
        sid = s["set"]
        rows = [c for c in clues if c["set"] == sid]
        proj = {c["clue_id"]: (c["fork_options"][0]["option"] if c["fork_options"] else "structural") for c in rows}
        if sid == "SYN-B":
            proj["SYN-B.1"] = "ge_before_same_apparition"
        sl = {st: {cid: br.sl_entry(next(c for c in rows if c["clue_id"] == cid), o,
                                    {"mercury": ka, "venus": ka}, None, st) for cid, o in proj.items()}
              for st in A.STEPS}
        bm = {cid: br.bm_entry(next(c for c in rows if c["clue_id"] == cid),
                               br.bm_option(next(c for c in rows if c["clue_id"] == cid), o)) for cid, o in proj.items()}
        preds = {c["clue_id"]: br.row_predicate(c) for c in rows if c["kind"] != "interval"}
        reg["sets"][sid] = {"counted": sid != "SYN-C", "projection": proj, "regimes": {"SL": sl, "BM": bm},
                            "row_predicates": preds, "sensitivities": {}, "tolerances": {}}
    rp = Path(d) / "syn_regimes.json"
    rp.write_text(json.dumps(reg), encoding="utf-8")
    tp = Path(d) / "syn_truth.json"
    tp.write_text(json.dumps({"sets": [{"set": "SYN-A", "day0_civil_jd_noon": ga},
                                       {"set": "SYN-B", "day0_civil_jd_noon": tab.jdn0 + ib},
                                       {"set": "SYN-C", "day0_civil_jd_noon": gc}]}), encoding="utf-8")
    return cp, rp, tp


def test_run_end_to_end_on_synthetic_sets():
    """run(), aggregate() and report() on three synthetic sets from the real sky
    at -850, with 2-year windows (W_DAYS patched) and null windows placed by the
    test.  The truths pass every row by construction, so strict recall must hold
    in both regimes; the aggregates must agree with the per-set flags."""
    saved = (A.W_DAYS, A.null_windows, A.SEEDS)
    j0 = int(C.jdn_from_julian(-852, 1, 1))
    try:
        with tempfile.TemporaryDirectory() as d:
            cp, rp, tp = _synthetic_inputs(d, j0)
            seeds = json.loads(A.SEEDS.read_text(encoding="utf-8"))
            for purpose in ("control_window", "control_window_sensitivity", "null_windows_I16a"):
                for i, sid in enumerate(("SYN-A", "SYN-B", "SYN-C")):
                    seeds["purposes"][purpose]["seeds"][sid] = 1000 + 17 * i + len(purpose)
            sp = Path(d) / "syn_seeds.json"
            sp.write_text(json.dumps(seeds), encoding="utf-8")
            A.SEEDS = sp
            A.W_DAYS = 365.25 * 2
            A.null_windows = lambda sid, mn, mx, n=A.N_NULL: [float(j0 + 300 + 7 * k) for k in range(n)]
            res = A.run(workers=1, null_side=True, sensitivity=True, babylon=False, slack=False, cache=False,
                        progress=None, clues_path=cp, regimes_path=rp, truth_path=tp, canonical_table=False)
            sys.path.insert(0, str(ROOT))
            spec = importlib.util.spec_from_file_location("almagest_script", ROOT / "almagest.py")
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            txt = m.report(res)
            json.dumps(m._jsonable(res))
    finally:
        A.W_DAYS, A.null_windows, A.SEEDS = saved
    for sid in ("SYN-A", "SYN-B", "SYN-C"):
        runs = res["per_set"][sid]["runs"]
        for name in ("SL:fine", "SL:mid", "SL:coarse", "SL_side:coarse", "BM"):
            assert runs[name]["strict_recall"], (sid, name, runs[name])
            assert runs[name]["truth_covered"] and runs[name]["n_uncovered"] == 0, (sid, name)
    for leg in A.LEGS:
        sc, st = leg.split(":")
        assert res["seen_ALM_SL"][leg] == sum(int(res["per_set"][s]["runs"][f"SL:{st}"][f"seen_{sc}"])
                                             for s in ("SYN-A", "SYN-B"))
        assert res["seen_ALM_SL_side"][leg] >= res["seen_ALM_SL"][leg]
    assert res["rec_ALM_BM"] == sum(int(res["per_set"][s]["runs"]["BM"]["narrow_st"]) for s in ("SYN-A", "SYN-B"))
    assert res["Q_BM"] is True and res["gate_3b"]["fires"] is True          # 2 sets can never reach 6
    assert set(res["N_narrow_3b"]) == set(A.LEGS)
    assert "Gate 3b" in txt and "SYN-A" in txt


def test_script_refuses_before_freeze():
    spec = importlib.util.spec_from_file_location("almagest_script", ROOT / "almagest.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if m.freeze_tag_exists():
        return                                    # after Freeze 1 the run is allowed
    out = sys.stdout
    try:
        assert m.main([]) == 2
    finally:
        sys.stdout = out


if __name__ == "__main__":
    import time
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            t0 = time.time()
            try:
                fn()
                print(f"PASS {name} ({time.time() - t0:.2f} s)")
            except Exception as exc:          # noqa: BLE001
                fails += 1
                print(f"FAIL {name}: {exc!r}")
    print("all passed" if not fails else f"{fails} failed")
    sys.exit(1 if fails else 0)
