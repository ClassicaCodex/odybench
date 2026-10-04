"""Unit tests for check_v8.py, one or more per function, on hand-built cases.
Run from C:/Projects/odybench:  py results/design-check-v8/test_check_v8.py
"""
import io
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_v8 as K  # noqa: E402


def t_Phi_phi():
    assert abs(K.Phi(0.0) - 0.5) < 1e-15
    assert abs(K.Phi(1.959964) - 0.975) < 1e-6
    assert abs(K.phi(0.0) - 1 / math.sqrt(2 * math.pi)) < 1e-15
    assert abs(K.phi(1.0) - math.exp(-0.5) / math.sqrt(2 * math.pi)) < 1e-15


def t_p_window():
    assert abs(K.p_window(10.0, 2.0, 10.0 - 1.959964 * 2, 10.0 + 1.959964 * 2) - 0.95) < 1e-6
    assert K.p_window(0.0, 1.0, 2.0, 1.0) == 0.0
    assert abs(K.p_window(0.0, 1.0, 0.0, 50.0) - 0.5) < 1e-12


def t_joint_common_offset():
    # overlap of offsets [-1, 0] for d ~ N(0, 1)
    j = K.joint_common_offset(5.0, 1.0, (4.0, 6.0), 7.0, (5.0, 7.0))
    assert abs(j - (K.Phi(0.0) - K.Phi(-1.0))) < 1e-12
    assert K.joint_common_offset(0.0, 1.0, (0.0, 1.0), 0.0, (2.0, 3.0)) == 0.0


def t_ndot_shift():
    assert abs(K.ndot_shift(1955.0)) < 1e-12
    # 0.91072 * 0.038 * 31.3168^2 = 33.94 s at -1176.68 (2.3: +34 s)
    assert abs(K.ndot_shift(-1176.68) - 0.91072 * 0.038 * ((-1176.68 - 1955) / 100) ** 2) < 1e-9
    assert abs(K.ndot_shift(-1176.68) - 33.94) < 0.01
    assert K.ndot_shift(100.0, -25.82, -25.82) == 0.0


def t_models_at():
    dt = lambda y, m: {"smh2020": 1.0, "smh2020_parabola": 2.0, "smh2016_parabola": 3.0,
                       "em2006_canon": 4.0}[m]
    sg = lambda y, m: 7.0
    ms = K.models_at(-1176.68, dt, sg)
    shift = K.ndot_shift(-1176.68)
    assert [m for m, _mu, _s in ms] == list(K.MODELS)
    assert abs(ms[0][1] - (1.0 + shift)) < 1e-12 and abs(ms[3][1] - 4.0) < 1e-12
    assert all(s == 7.0 for _m, _mu, s in ms)


def t_table():
    ms = [("a", 0.0, 1.0), ("b", 1.0, 1.0)]
    t = K.table(ms, ms, (-1.0, 1.0), (-1.0, 1.0))
    pa = K.Phi(1.0) - K.Phi(-1.0)
    pb = K.Phi(0.0) - K.Phi(-2.0)
    assert abs(t["a"][0] - pa) < 1e-12 and abs(t["b"][1] - pb) < 1e-12
    assert abs(t["mixture"][0] - (pa + pb) / 2) < 1e-12
    assert abs(t["a"][2] - pa) < 1e-12        # same window and model: joint = P


def t_bisect_bound_and_max_boundaries():
    assert abs(K.bisect_bound(0.1, 540.6) - 0.1 / (540.6 * math.sqrt(2 * math.pi))) < 1e-15
    assert K.max_boundaries(0.1, 540.6) == 1
    assert K.max_boundaries(0.01, 540.6) == 13
    assert K.max_boundaries(0.01, 60.0) == 1


def t_positive_or_inf():
    assert K.positive_or_inf(0.0) == float("inf")
    assert K.positive_or_inf(1e-9) == 1e-9


def t_widen_change():
    c = K.widen_change(0.0, 1.0, (-1.0, 1.0), 0.5)
    assert abs(c - ((K.Phi(1.5) - K.Phi(-1.5)) - (K.Phi(1.0) - K.Phi(-1.0)))) < 1e-12
    assert K.widen_change(0.0, 1.0, (-1.0, 1.0), 0.0) == 0.0


def t_shifted_joints():
    m78 = [("a", 0.0, 1.0)]
    m31 = [("a", 0.0, 1.0)]
    j0 = K.shifted_joints(m78, m31, (-1.0, 1.0), (-1.0, 1.0), 0.0)["a"]
    j1 = K.shifted_joints(m78, m31, (-1.0, 1.0), (-1.0, 1.0), 1.0)["a"]
    assert abs(j0 - (K.Phi(1.0) - K.Phi(-1.0))) < 1e-12
    assert abs(j1 - (K.Phi(2.0) - K.Phi(0.0))) < 1e-12


def t_ff_upper_and_poisson_upper():
    n = 10690
    assert abs(K.ff_upper([], n) * n - 3.689) < 1e-3          # U0 = 3.69/n
    for k in range(0, 7):                                        # all reach 1: exact Poisson
        assert abs(K.ff_upper([1.0] * k, n) - K.poisson_upper(k, n)) < 1e-15
    assert abs(K.poisson_upper(4, n) * n - 10.2416) < 1e-3
    assert abs(K.poisson_upper(5, n) * n - 11.6683) < 1e-3
    # thinner reach at the same total gives a smaller bound
    assert K.ff_upper([0.5] * 8, n) < K.ff_upper([1.0] * 4, n)


def t_max_reached():
    n = 10690
    b = K.poisson_upper(4, n) + 1e-12
    assert K.max_reached(1.0, b, n) == 4
    assert K.max_reached(1.0, K.ff_upper([], n) - 1e-9, n) == -1
    assert K.max_reached(1.0, K.ff_upper([], n) + 1e-12, n) == 0


def t_max_units_shaped():
    n = 1000
    assert K.max_units_shaped([1.0], K.poisson_upper(3, n) + 1e-12, n) == 3.0
    assert K.max_units_shaped([1.0, 0.5], K.ff_upper([1.0, 0.5, 1.0], n) + 1e-12, n) == 2.5


def t_thin_limit_units():
    n = 10690
    b = 0.087 * 131 / n
    u = K.thin_limit_units(b, n)
    # the supremum lies above any finite thin spread and below the bound's own units
    assert K.max_reached(0.01, b, n) * 0.01 <= u + 1e-9 < b * n
    assert K.thin_limit_units(K.ff_upper([], n) * 0.5, n) == 0.0


def t_frac_range_and_line_days():
    runs = {"a": {"start_year": 0, "n_cand": 1000, "sets": {"S": {"n_pass": 40, "n_cand": 1000}}},
            "b": {"start_year": 1, "n_cand": 1000, "sets": {"S": {"n_pass": 60, "n_cand": 1000}}}}
    assert K.frac_range(runs, "S") == ((0.04, 0.06), (40, 60))
    assert K.line_days(runs) == [50]


def t_phase_rows_and_words_only_none():
    clues = [
        {"clue_id": "X.1", "kind": "moon-phase", "fork_options": [
            {"option": "phase_class", "primary": True, "justification": "Mars near opposition (my inference)"},
            {"option": "positional", "primary": False},
            {"option": "none", "primary": False, "justification": "the Moon's phase is not stated in words; do not use it"}]},
        {"clue_id": "X.2", "kind": "moon-phase", "fork_options": [
            {"option": "phase_class", "primary": True, "justification": "quarter Moon"},
            {"option": "elongation_tol", "primary": False}]},
        {"clue_id": "X.3", "kind": "star", "fork_options": [{"option": "none", "primary": True}]}]
    r = K.phase_rows(clues)
    assert set(r) == {"X.1", "X.2"}
    assert r["X.1"][0] == "phase_class" and "inference" in r["X.1"][1]
    assert r["X.2"][2] is None and r["X.2"][3] == {"phase_class", "elongation_tol"}
    assert K.words_only_none(r) == ["X.1"]


def t_phrase_lines():
    doc = "\n".join(["intro", "B the knife-edge here", K.MARKER + " truth below -->",
                     "B the knife-edge again", "nothing"])
    got = K.phrase_lines(doc, ("B the knife-edge", "absent phrase"))
    assert got == [(2, "public", "B the knife-edge"), (4, "AppT", "B the knife-edge")]
    assert K.phrase_lines("no marker, no phrase", ("x y z",)) == []


def t_selftest():
    buf = io.StringIO()
    assert K.selftest(out=lambda s: buf.write(s + "\n")) is True
    assert "pass" in buf.getvalue()


def t_check_runs_and_prints_key_lines():
    buf = io.StringIO()
    K.check(out=lambda s: buf.write(s + "\n"))
    text = buf.getvalue()
    assert "cells differing from the printed table: revision 7 0, revision 8 0" in text
    assert "reach 1: at most 4 targets" in text
    assert "ALM-A: 4.88-4.89%" in text
    assert "ALM-B day counts with and without B.2 identical: True" in text
    assert "['ALM-A.10', 'ALM-A.2', 'ALM-A.5', 'ALM-B.2', 'ALM-B.5']" in text
    assert "New-blocker scan" in text


if __name__ == "__main__":
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("t_") and callable(v)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print("PASS", name)
        except Exception as e:  # report every failure honestly
            failed += 1
            print("FAIL", name, type(e).__name__, e)
    print(f"{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
