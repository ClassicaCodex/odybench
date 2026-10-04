"""Unit tests for the functions of revision 8's scratch scripts, on hand-built
and synthetic cases (no sky is evaluated, no truth file is read).

Covers: i2c_table.py, outcome4_bound.py, verdict_trace.py, alm_rows.py,
narrowing_v8.py, replace_region.py, and the two helper functions of
scan_public.py (extracted with ast, so the scan itself does not run).
Run: py results/design-revision-v8/test_scratch.py
"""
import ast
import json
import math
import os
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "C:/Projects/odybench")

import i2c_table as T          # noqa: E402
import outcome4_bound as O     # noqa: E402
import verdict_trace as V      # noqa: E402
import alm_rows as A           # noqa: E402
import narrowing_v8 as N       # noqa: E402
import replace_region as R     # noqa: E402
from scipy.stats import chi2, gamma  # noqa: E402

TESTS = []


def test(f):
    TESTS.append(f)
    return f


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


# ---------------------------------------------------------------- i2c_table
@test
def t_phi_and_window():
    assert close(T.Phi(0.0), 0.5)
    assert close(T.p_window(0.0, 1.0, -1.0, 1.0), 0.6826894921, 1e-9)
    assert close(T.p_window(100.0, 10.0, 100.0, 1e9), 0.5, 1e-12)
    assert T.p_window(0.0, 1.0, 1.0, -1.0) < 0          # reversed bounds give a negative mass


@test
def t_joint_common_offset():
    # identical windows relative to identical means: joint = single-window mass
    j = T.joint_common_offset(0.0, 1.0, (-1.0, 1.0), 5.0, (4.0, 6.0))
    assert close(j, T.p_window(0.0, 1.0, -1.0, 1.0))
    # disjoint offset ranges: zero
    assert T.joint_common_offset(0.0, 1.0, (0.0, 1.0), 0.0, (2.0, 3.0)) == 0.0
    # partial overlap of offsets [0.5, 1]
    j2 = T.joint_common_offset(0.0, 2.0, (0.0, 1.0), 10.0, (10.5, 11.5))
    assert close(j2, T.Phi(1.0 / 2.0) - T.Phi(0.5 / 2.0))


@test
def t_ndot_and_density():
    assert close(T.ndot_conv(1955.0), 0.0)
    assert T.ndot_conv(-1176.676) > 0                    # SMH -> canon adds seconds in antiquity
    assert close(T.ndot_conv(-1176.676), 34.0, 0.6)      # about 34 s at -1177 (DESIGN section 0)
    assert close(T.max_density(1.0), 1.0 / math.sqrt(2 * math.pi))
    assert close(0.1 * T.max_density(540.6), 7.38e-5, 1e-7)


@test
def t_read_windows():
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("x\ncontinuous totality window (canon frame): 100.25 - 200.50 s; more\n"
                "1131 BC continuous totality window: 10.00 - 20.00 s; more\n")
        p = f.name
    try:
        w78, w31 = T.read_windows(p)
        assert w78 == (100.25, 200.5) and w31 == (10.0, 20.0)
    finally:
        os.remove(p)


@test
def t_table_with_synthetic_models():
    saved = T.models_at
    try:
        T.models_at = lambda y: [(m, 1000.0 + 10 * i, 100.0) for i, m in enumerate(T.MODELS)]
        rows = T.table((900.0, 1100.0), (950.0, 1050.0), 0.0, 0.0)
        for i, m in enumerate(T.MODELS):
            mu = 1000.0 + 10 * i
            assert close(rows[m][0], T.p_window(mu, 100.0, 900.0, 1100.0))
            assert close(rows[m][1], T.p_window(mu, 100.0, 950.0, 1050.0))
        for k in range(3):
            assert close(rows["mixture"][k], sum(rows[m][k] for m in T.MODELS) / 4)
    finally:
        T.models_at = saved


@test
def t_models_at_is_the_ephem_models():
    # the four models at the 1178 BC epoch agree with the 2.3 table's printed values
    got = {m: (mu, s) for m, mu, s in T.models_at(-1176.676)}
    assert close(got["smh2020"][0] - T.ndot_conv(-1176.676), 28543, 1.0)
    assert close(got["smh2020"][1], 720, 1.0)
    assert close(got["em2006_canon"][0], 28589, 1.0)
    assert close(got["smh2016_parabola"][1], 541, 1.0)


# ----------------------------------------------------------- outcome4_bound
@test
def t_g_hi_poisson_cases():
    n = 10690
    assert close(O.g_hi([], n), chi2.ppf(0.975, 2) / (2 * n), 1e-15)
    assert close(O.g_hi([], n) * n, 3.689, 1e-3)
    for k in range(1, 7):
        assert close(O.g_hi([1.0] * k, n), gamma.ppf(0.975, k + 1) / n, 1e-12)


@test
def t_g_hi_monotone_and_max_targets():
    n = 1000
    assert O.g_hi([0.5] * 4, n) < O.g_hi([1.0] * 4, n)
    assert O.max_targets(1.0) == 4                        # at the design-stage bound 0.00107
    assert O.max_targets(0.5) >= O.max_targets(1.0)
    assert O.max_targets(1.0, bound=O.G_BM_U) == 9
    # a bound below U0 admits nothing
    assert O.max_targets(1.0, bound=1e-9) == 0


@test
def t_max_units_shaped():
    assert close(O.max_units_shaped([1.0]), 4.0)
    u = O.max_units_shaped([1.0, 0.41])
    assert 4.0 <= u <= 8.5


# ------------------------------------------------------------ verdict_trace
def _set(name):
    return V.SETS[name][0]


@test
def t_lattice_and_record():
    pp, ph = V.p_H_of(V.NULL["pools"], "both")
    assert close(ph, 2 / 50, 1e-12)                       # P_BM,E: (1 + 1)/(1 + 49)
    pp, ph = V.p_H_of(V.NULL["pools"], "h4")
    assert close(ph, 2 / 29, 1e-12)                       # P_MWRA,E: 0.0690
    assert close(V.p_min(V.NULL["pools"]["P_BM"]), 2 / 77)
    assert V.p_pool(V.NULL["pools"]["P_BM"], "both", member=False) == 1.0
    assert V.q_record(V.NULL["pools"], {"H4": False}) is True
    assert V.q_record(V.NULL["pools"], {}) is False


@test
def t_q_score_split():
    L, Q, _ = V.decide(_set("S0x"))
    assert L == {"3a"} and {"Q_score3a", "Q_score3b"} <= Q
    L, Q, _ = V.decide(_set("S0y"))
    assert L == {"3a", "3b"} and "Q_score3a" in Q and "Q_score3b" not in Q
    L7, Q7, _ = V.decide_v7(_set("S0x"))
    assert "Q_score" in Q7


@test
def t_q_attain_gates_only_beside_firing_gate():
    L, Q, _ = V.decide(_set("S20"))
    assert "3a" not in L and "3b" not in L
    assert "Q_attain3a" not in Q and "Q_attain3b" not in Q
    L7, Q7, _ = V.decide_v7(_set("S20"))
    assert {"Q_attain3a", "Q_attain3b"} <= Q7
    L, Q, _ = V.decide(_set("S16"))
    assert "3a" in L and "Q_attain3a" in Q
    L, Q, _ = V.decide(_set("S17"))
    assert "3b" in L and "Q_attain3b" in Q


@test
def t_q_attain4_windows_and_guard():
    L, Q, _ = V.decide(_set("S14c"))
    assert "Q_attain4" in Q                                # E_j 2 but no hit in the two windows
    L7, Q7, _ = V.decide_v7(_set("S14c"))
    assert "Q_attain4" not in Q7                           # revision 7 read E_j
    L, Q, _ = V.decide(_set("S4c"))
    assert "4" in L and "Q_attain4" not in Q               # the guard
    L, Q, _ = V.decide(_set("S4c"), guard=False)
    assert "4" in L and "Q_attain4" in Q
    L, Q, _ = V.decide(_set("S4"))
    assert L == {"4"} and "Q_attain4" not in Q
    L, Q, _ = V.decide(_set("S14"))
    assert "Q_attain4" in Q                                # G condition fails
    L, Q, _ = V.decide(_set("S4b"))
    assert "4" not in L and "Q_attain4" not in Q


@test
def t_blocked_and_label1():
    assert V.decide(_set("S7"))[0] == "BLOCKED"
    L, Q, _ = V.decide(_set("S1"))
    assert L == {"1"} and "Q_contra" in Q and "Q_record" in Q
    L, Q, _ = V.decide(_set("S8"))
    assert "1" not in L


@test
def t_check_constraints():
    assert V.check(_set("S0")) == []
    assert V.check(_set("S4c")) == []                      # hit without hit_j(m_hat) is admissible
    q = V.var(negatives=[(False, 0.0004, 0.0009, 0, True)] * 12)
    assert "C4 hit_j(m_hat)" in V.check(q)                 # a hit at m_hat needs E_j >= 1
    q = V.var(negatives=[(True, 0.0, 0.0009, 2, True)] * 12)
    assert "C4 hit_j" in V.check(q)
    q = V.var(negatives=[(False, 0.0004, 0.0009, 1.5, False)] * 12)
    assert "C5 E_j" in V.check(q)
    q = V.var(gate3a=V.gate3a(2, 3, 3, 3))
    assert "C10 3a" in V.check(q)
    assert any(b.startswith("C7") for b in V.check(_set("S20")))


@test
def t_helpers():
    assert V.legs(1, 2, 3, 4) == {"AL_bf": 1, "AL_st": 2, "WO_bf": 3, "WO_st": 4}
    g = V.gate3a(4, 2, 3, 3, redraft=(4, 4, 4, 4))
    assert g["main"]["AL_bf"] == 4 and g["redraft"]["AL_st"] == 4 and g["noncirc"]["AL_st"] == 2
    b = V.gate3b(6, 5)
    assert b["bf_fine"] == 6 and b["st_coarse"] == 5 and len(b) == 6
    assert V.held(5) == {"fine": 5, "mid": 5, "coarse": 5}
    assert V.held(5, 7, 7)["mid"] == 7
    q = V.var(pool_override={"P_BM": dict(both=4)})
    assert q["pools"]["P_BM"]["both"] == 4 and V.S0["pools"]["P_BM"]["both"] == 1
    assert V.tag_of("realisable", []) == "realisable"
    assert V.tag_of("branch", []).startswith("MARKED BRANCH TEST")
    assert "C7" in V.tag_of("branch", ["C7 x"])
    assert V.cp_lo(0, 10) == 0.0 and 0 < V.cp_lo(5, 10) < 0.5


@test
def t_every_set_matches_its_mark():
    for name, (q, mark) in V.SETS.items():
        bad = V.check(q)
        if mark == "realisable":
            assert not bad, (name, bad)
        if mark == "branch":
            assert bad, name


# ------------------------------------------------------------------ alm_rows
def _clue(cid, kind, opts, s=None):
    return {"set": s or cid.split(".")[0], "clue_id": cid, "kind": kind, "fork_options": opts}


@test
def t_alm_rows_rules():
    none_unstated = {"option": "none", "justification": "the Moon's phase is not stated in words; do not use it"}
    clues = [
        _clue("ALM-X.1", "moon-phase", [{"option": "phase_class", "primary": True},
                                        {"option": "positional"}, none_unstated]),
        _clue("ALM-X.2", "moon-phase", [{"option": "phase_class", "primary": True},
                                        {"option": "elongation_tol"}]),
        _clue("ALM-X.3", "planet", [{"option": "ge_after_within_j", "primary": True},
                                    {"option": "ge_after_same_apparition"}]),
        _clue("ALM-X.4", "planet", [{"option": "positional", "primary": True}]),
        _clue("ALM-X.5", "star", [{"option": "none", "primary": True}]),
        _clue("ALM-X.6", "star", [{"option": "positional", "primary": True}]),
        _clue("ALM-X.7", "interval", [{"option": "as_printed", "primary": True}]),
        _clue("ALM-X.8", "season", [{"option": "equinox_tol", "primary": True}]),
    ]
    assert A.unstated_phase_rows(clues) == {"ALM-X.1"}
    res = A.project(clues, A.unstated_phase_rows(clues))
    proj, held = res["ALM-X"]
    assert proj == ["ALM-X.1:none", "ALM-X.2:phase_class", "ALM-X.3:ge_after_same_apparition",
                    "ALM-X.7:as_printed", "ALM-X.8:equinox_tol"]
    assert held == ["ALM-X.1:positional", "ALM-X.2:elongation_tol", "ALM-X.4:positional",
                    "ALM-X.6:positional"]
    assert A.opt_name({"name": "a"}) == "a" and A.opt_name({"option": "b"}) == "b"


@test
def t_alm_rows_parse_rev6():
    txt = ("rows by kind: {}\nALM-Q counted\n   projection: ALM-Q.1:none, ALM-Q.2:ge_true_k\n"
           "   held out  : (none)\nALM-R reported\n   projection: ALM-R.1:x\n   held out  : ALM-R.2:y, ALM-R.3:z\n")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(txt)
        p = f.name
    try:
        got = A.parse_rev6(p)
        assert got["ALM-Q"] == (["ALM-Q.1:none", "ALM-Q.2:ge_true_k"], [])
        assert got["ALM-R"] == (["ALM-R.1:x"], ["ALM-R.2:y", "ALM-R.3:z"])
    finally:
        os.remove(p)


@test
def t_alm_rows_on_the_real_file():
    d = json.load(open(A.CLUES, encoding="utf-8"))
    un = A.unstated_phase_rows(d["clues"])
    assert un == {"ALM-A.2", "ALM-A.5", "ALM-A.10", "ALM-B.2", "ALM-B.5"}
    res = A.project(d["clues"], un | A.MEASURED_PHASE)
    assert "ALM-B.7:phase_class" in res["ALM-B"][0]
    assert all(not x.endswith("phase_class") for s in res for x in res[s][0] if not x.startswith("ALM-B.7"))
    old = A.parse_rev6()
    assert all(old[s][1] == res[s][1] for s in res)       # held-out rows unchanged


@test
def t_alm_rows_main_without_rev6():
    import contextlib
    import io

    def missing(path=None):
        raise FileNotFoundError("not exported")
    saved = A.parse_rev6
    buf = io.StringIO()
    try:
        A.parse_rev6 = missing
        with contextlib.redirect_stdout(buf):
            A.main()
    finally:
        A.parse_rev6 = saved
    out = buf.getvalue()
    assert "comparison skipped" in out and "ALM-B.7:phase_class" in out


# -------------------------------------------------------------- narrowing_v8
@test
def t_narrowing_assemble():
    rep = {"w": {"start_year": 0, "n_cand": 1000, "sets": {}}}
    for sid in N.COUNTED:
        rep["w"]["sets"][sid] = {"frac": 0.5, "n_pass": 500, "n_cand": 1000}
    rep["w"]["sets"]["ALM-A [frozen, inferred phases none]"] = {"frac": 0.049, "n_pass": 49, "n_cand": 1000}
    rep["w"]["sets"]["ALM-B [frozen, inferred phases none]"] = {"frac": 0.051, "n_pass": 51, "n_cand": 1000}
    rep["w"]["sets"]["ALM-I (same_app & visible)"] = {"frac": 0.01, "n_pass": 10, "n_cand": 1000}
    rep["w"]["sets"]["ALM-J (same_app & visible)"] = {"frac": 0.05, "n_pass": 50, "n_cand": 1000}
    tab = N.assemble(rep)
    assert tab["w"]["ALM-A"] == (0.049, 49, 1000) and tab["w"]["ALM-D"] == (0.5, 500, 1000)
    assert N.narrowable_sets(tab["w"]) == ["ALM-A", "ALM-I", "ALM-J"]   # 50 of 1000 is on the line
    assert N.pick(rep["w"], "ALM-B", N.ROW_V8)["n_pass"] == 51


@test
def t_narrowing_on_the_recorded_runs():
    rep = json.load(open(N.SRC, encoding="utf-8"))
    tab = N.assemble(rep)
    for t in tab:
        assert N.narrowable_sets(tab[t]) == ["ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G",
                                             "ALM-H", "ALM-L"]
        assert 0.0485 <= tab[t]["ALM-A"][0] <= 0.0490


# ------------------------------------------------------------ replace_region
@test
def t_replace_region():
    assert R.replace_region("aXbYc", "X", "Y", "Z") == "aZc"
    assert R.replace_region("aXbYc", "X", "Y", "Z", keep_end=True) == "aZYc"
    assert R.replace_region("aXbYcY", "X", "Y", "") == "acY"
    for bad in (("aXbXc", "X", "c"), ("abc", "X", "c"), ("aXb", "X", "Y")):
        try:
            R.replace_region(bad[0], bad[1], bad[2], "Z")
        except ValueError:
            pass
        else:
            raise AssertionError(f"no error for {bad}")


@test
def t_replace_region_main_on_temp_files():
    from pathlib import Path
    tmp = Path(tempfile.mkdtemp())
    (tmp / "parts").mkdir()
    (tmp / "parts" / "p.md").write_text("NEW", encoding="utf-8")
    (tmp / "D.md").write_text("head START old END tail", encoding="utf-8")
    saved = (R.DESIGN, R.LOG, R.PARTS, sys.argv)
    try:
        R.DESIGN, R.LOG, R.PARTS = tmp / "D.md", tmp / "log.txt", tmp / "parts"
        sys.argv = ["replace_region.py", "START", "END", "p.md", "--keep-end"]
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()):
            R.main()
        assert (tmp / "D.md").read_text(encoding="utf-8") == "head NEWEND tail"
        assert "p.md" in (tmp / "log.txt").read_text(encoding="utf-8")
    finally:
        R.DESIGN, R.LOG, R.PARTS, sys.argv = saved


def _run_main(mod):
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod.main()
    return buf.getvalue()


@test
def t_mains_print_their_key_lines():
    out = _run_main(T)
    assert "0.5030 (0.503)" in out and "0.3076 (0.308)" in out and "within 0.0017 of the table" in out
    out = _run_main(O)
    assert "reach 1.00: at most    4 targets" in out and "would have been 9" in out
    out = _run_main(N)
    assert "ALM-A:  4.88- 4.89%" in out and "w3: 8 sets narrow" in out
    out = _run_main(V)
    assert "31 synthetic sets" in out and "S20: revision 7's rule" in out and "\n  S4c\n" in out


# --------------------------------------------- scan_public helper functions
def _scan_helpers():
    src = open(os.path.join(HERE, "scan_public.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    keep = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ("norm", "forms")]
    ns = {}
    exec("import re\nimport sys\nsys.path.insert(0, 'C:/Projects/odybench')\n"
         "from odybench import calendar as cal\n"
         "MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\n"
         "MONFULL = ['January','February','March','April','May','June','July','August',"
         "'September','October','November','December']\n", ns)
    exec(compile(ast.Module(body=keep, type_ignores=[]), "scan_public_helpers", "exec"), ns)
    return ns


@test
def t_scan_helpers():
    ns = _scan_helpers()
    assert ns["norm"]("\u2212700\u2013690") == "-700-690"
    f = ns["forms"](-699, 3, 5)                           # a synthetic date, far from any control
    assert "-0699-03-05" in f and "5 Mar 700 BC" in f and "March 5, 700 BC" in f
    jdn = ns["cal"].jdn_from_julian(-699, 3, 5)
    assert str(jdn) in f
    g = ns["forms"](150, 7, 1)
    assert "+0150-07-01" in g and "1 Jul AD 150" in g


def main():
    failed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {t.__name__}")
            traceback.print_exc(file=sys.stdout)
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    return failed


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
