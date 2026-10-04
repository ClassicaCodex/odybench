"""Unit tests for public_inference.py (added after the check of revision 8 [c8]),
on hand-built text and hand-built sets, and end-to-end runs of the scripts it
extends (check_design.py, scan_public.py) and of its own main on the real file.

No sky is evaluated. The only data read are DESIGN.md, its byte copy
DESIGN-v8-before-c8.md, and the recheck's recorded design-stage narrowing
(through narrowing_v8.py). scan_public.py, run end to end, reads the two truth
files only to build its list of accepted dates, as it always has.
Run: py results/design-revision-v8/test_public_inference.py
"""
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import public_inference as P  # noqa: E402

TESTS = []


def test(f):
    TESTS.append(f)
    return f


M = P.MARKER + " cut here -->"


def _out():
    lines = []
    return lines, lines.append


# ------------------------------------------------------------ text helpers
@test
def t_flatten_and_line_at():
    flat, starts = P.flatten("a\n  b c\n\nd")
    assert flat == "a b c  d"
    assert starts == [0, 2, 6, 7]
    assert [P.line_at(starts, k) for k in (0, 1, 2, 4, 5, 6, 7)] == [1, 1, 2, 2, 2, 3, 4]


@test
def t_marker_line():
    assert P.marker_line("x\ny\n" + M + "\nz") == 3
    for bad in ("x\ny", M + "\n" + M):
        try:
            P.marker_line(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("a missing or doubled marker must raise")


@test
def t_public_flat():
    doc = "top\n  two\n" + M + "\nbelow\n"
    assert P.public_flat(doc) == "top two"


@test
def t_characterisation_hits_each_pattern_and_tier():
    doc = "\n".join([
        "| v7 P21 (x; ALM-B the knife-edge) | **nearly determined by known numbers** |",   # 1
        "ALM-B is the knife-edge here.",                                                    # 2
        "P21 rested on A.2 and was nearly determined.",                                     # 3: a dot in A.2 is crossed
        "so known numbers no longer nearly fix it (2.7).",                                  # 4
        "P21 is open",                                                                      # 5: wrapped phrase
        "again. P8 was nearly fixed by a calibration.",                                     # 6: sentence end blocks P21
        "| P21 | nearly fixed |",                                                           # 7: a cell boundary blocks
        "the expected pass of gate 3b leaned on rows.",                                     # 8
        "two knife-edges",                                                                  # 9
        M,                                                                                  # 10
        "that is why the recheck found P21 nearly determined.",                             # 11
    ])
    got = [(h[0], h[1], h[2], h[3]) for h in P.characterisation_hits(doc)]
    assert got == [
        (1, "public", "ALM-B the knife-edge", "P21v7"),
        (1, "public", "nearly determined by known numbers", "P21v7"),
        (2, "public", "ALM-B the knife-edge", "P21v7"),
        (3, "public", "P21 beside 'nearly determined/fixed'", "P21v7"),
        (4, "public", "no longer nearly", "P21v7"),
        (5, "public", "open again", "P21v7"),
        (8, "public", "expected pass ... leaned", "R92"),
        (9, "public", "two knife-edges", "P21v8"),
        (11, "AppT", "P21 beside 'nearly determined/fixed'", "P21v7"),
    ], got
    # every hit carries an excerpt that holds the match
    assert all("knife" in h[4] or "nearly" in h[4] or "open" in h[4] or "lean" in h[4]
               for h in P.characterisation_hits(doc))


@test
def t_characterisation_hits_ignores_neutral_wording():
    doc = ("P21 is restated [R3-4].\nWhether it passes is P21, which the known numbers do not settle.\n"
           "P8's second clause, nearly fixed by that calibration, is R23.\n"
           "The first two are knife-edges.\n" + M + "\n")
    assert P.characterisation_hits(doc) == []


# ------------------------------------------------------------ constraints
@test
def t_active_constraints():
    base = ("gate 3b 6 on every leg, and 5 under the other meaning\nso the gate's margin\nwas nil\n")
    act, nil = P.active_constraints(base + "the expected pass of gate 3b leaned on them\n" + M + "\nopen again\n")
    assert act == ["S0x", "R92"] and nil is True          # 'open again' below the marker adds nothing
    act, nil = P.active_constraints("two knife-edges; P21 is open again\n" + M + "\n")
    assert act == ["P21v7", "P21v8"] and nil is False
    act, nil = P.active_constraints("nothing\n" + M + "\n")
    assert act == [] and nil is False


@test
def t_constraint_preds():
    pr = P.constraint_preds(["ALM-B", "ALM-H"], ["ALM-A", "ALM-B", "ALM-H"])
    f = frozenset
    assert pr["S0x"](f({"ALM-G", "ALM-H"})) and not pr["S0x"](f({"ALM-B", "ALM-H"}))
    assert pr["P21v7"](f({"ALM-G", "ALM-H"}))              # ALM-B the only near set kept
    assert not pr["P21v7"](f({"ALM-G", "ALM-D"}))          # ALM-H kept too: two near sets
    assert not pr["P21v7"](f({"ALM-B", "ALM-H"}))          # the knife-edge itself lost
    assert pr["P21v8"](f({"ALM-H", "ALM-D"})) and not pr["P21v8"](f({"ALM-D", "ALM-E"}))
    assert pr["R92"](f({"ALM-G", "ALM-H"})) and not pr["R92"](f({"ALM-A", "ALM-H"}))
    assert pr["T60"](f({"ALM-G", "ALM-D"})) and not pr["T60"](f({"ALM-D", "ALM-E"}))
    pr2 = P.constraint_preds(["X"], ["X", "Y"], knife="X", leaned="Y", tol="Z")
    assert pr2["S0x"](f({"Y", "Z"})) and not pr2["R92"](f({"Y", "Z"})) and pr2["T60"](f({"Y", "Z"}))


@test
def t_consistent_pairs_identified_loser_counts():
    pool = ("ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H", "ALM-L")
    pr = P.constraint_preds(["ALM-B", "ALM-H"], ["ALM-A", "ALM-B", "ALM-H"])
    allp = P.consistent_pairs(pool, [], pr)
    assert len(allp) == 28 and allp[0] == ("ALM-A", "ALM-B")
    s0x = P.consistent_pairs(pool, ["S0x"], pr)
    assert len(s0x) == 21 and P.identified(s0x) == []
    v7 = P.consistent_pairs(pool, ["S0x", "P21v7"], pr)
    assert len(v7) == 6 and P.identified(v7) == ["ALM-H"]
    v7r = P.consistent_pairs(pool, ["S0x", "P21v7", "R92"], pr)
    assert len(v7r) == 5 and P.identified(v7r) == ["ALM-H"]
    both = P.consistent_pairs(pool, ["S0x", "P21v7", "R92", "T60"], pr)
    assert both == [("ALM-G", "ALM-H")] and P.identified(both) == ["ALM-G", "ALM-H"]
    cnt = P.loser_counts(s0x, pool)
    assert cnt["ALM-B"] == 0 and all(cnt[s] == 6 for s in pool if s != "ALM-B")
    assert P.identified([]) == [] and P.loser_counts([], ("X",)) == {"X": 0}


@test
def t_near_line():
    t = {"w1": {"X": (0.0436, 1, 1), "Y": (0.0501, 1, 1), "Z": (0.04, 1, 1), "Q": (0.049, 1, 1)},
         "w2": {"X": (0.05, 1, 1), "Y": (0.049, 1, 1), "Z": (0.049, 1, 1)}}
    assert P.near_line(t) == ["X"]                         # Y over the line once, Z too far once, Q missing in w2
    assert P.near_line(t, band=0.011) == ["X", "Z"]
    assert P.near_line({}) == []


@test
def t_recorded_near():
    v7, v8 = P.recorded_near()
    assert v7 == ["ALM-B", "ALM-H"], v7
    assert v8 == ["ALM-A", "ALM-B", "ALM-H"], v8


@test
def t_named_exceptions():
    doc = "x\n" + M + "\n- R10: the two sets whose truth is not in B under\n  regime SL are ALM-Q and ALM-C (T2).\n"
    assert P.named_exceptions(doc) == ("ALM-C", "ALM-Q")
    assert P.named_exceptions("x\n" + M + "\nnothing here\n") is None


# ------------------------------------------------------------ analyse / run / main
SYN_BEFORE = ("gate 3b 6 on every leg, and 5 under the other meaning; the gate's margin was nil.\n"
              "| v7 P21 (a; ALM-B the knife-edge) | x |\n" + M + "\n"
              "whose truth is not in B under regime SL are ALM-G and ALM-H (T2).\n"
              "that is why the recheck found P21 nearly determined.\n")
SYN_AFTER = SYN_BEFORE.replace("ALM-B the knife-edge", "restated")


@test
def t_analyse():
    lines, out = _out()
    r = P.analyse(SYN_BEFORE, ["ALM-B", "ALM-H"], ["ALM-A", "ALM-B", "ALM-H"], out)
    assert r["public_hits"] == 1 and r["appt_hits"] == 1 and r["active"] == ["S0x", "P21v7"] and r["nil"]
    assert r["without 13 row 60"]["identified"] == ["ALM-H"] and r["without 13 row 60"]["named_ok"]
    assert r["with 13 row 60's hint (T60)"]["identified"] == ["ALM-G", "ALM-H"]
    assert any("public hits: 1" in l for l in lines)
    r2 = P.analyse(SYN_AFTER, ["ALM-B", "ALM-H"], ["ALM-A", "ALM-B", "ALM-H"], out)
    assert r2["public_hits"] == 0 and r2["without 13 row 60"]["identified"] == []
    assert len(r2["without 13 row 60"]["pairs"]) == 21


@test
def t_run_on_temp_files():
    with tempfile.TemporaryDirectory() as d:
        b, a = os.path.join(d, "before.md"), os.path.join(d, "after.md")
        open(b, "w", encoding="utf-8").write(SYN_BEFORE)
        open(a, "w", encoding="utf-8").write(SYN_AFTER)
        lines, out = _out()
        res = P.run(design=a, before=b, out=out)
    text = "\n".join(lines)
    assert "as first written, the public part identified a withheld exception: True" in text
    assert "now: no public characterisation: True" in text
    assert "now: Appendix T still states the explanation: True" in text
    assert "now: no set identified from the public statements alone: True" in text
    assert "now: with 13 row 60's inherent hint, only that hint's set is identified: True" in text
    assert set(res) == {"revision 8 as first written (DESIGN-v8-before-c8.md)", "DESIGN.md now"}


@test
def t_selftest_passes():
    lines, out = _out()
    assert P.selftest(out) == 0
    assert all(l.startswith("ok") for l in lines) and len(lines) == 7


@test
def t_main_selftest_and_real_file():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        assert P.main(["--selftest"]) == 0
    assert "selftest: passed" in buf.getvalue()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        assert P.main([]) == 0
    out = buf.getvalue()
    for line in ("as first written, the public part identified a withheld exception: True",
                 "now: no public characterisation: True",
                 "now: Appendix T still states the explanation: True",
                 "now: no set identified from the public statements alone: True",
                 "now: with 13 row 60's inherent hint, only that hint's set is identified: True"):
        assert line in out, line


# ------------------------------------------------------------ the scripts it extends, end to end
def _py(script):
    r = subprocess.run(["py", os.path.join(HERE, script)], capture_output=True, text=True,
                       encoding="utf-8", cwd="C:/Projects/odybench")
    return r.returncode, r.stdout, r.stderr


@test
def t_check_design_runs_clean():
    rc, out, err = _py("check_design.py")
    assert rc == 0, err
    assert out.count("no problems found") == 4, out
    assert "check-of-revision-8 checks" in out and "every label and qualifier agrees" in out


@test
def t_scan_public_finds_no_date_and_none_of_the_wording():
    rc, out, err = _py("scan_public.py")
    assert rc == 0, err
    assert "total date hits 0" in out
    for p in ("[nearly determined by known numbers]", "[ALM-B,? (is )?the knife-edge]", "[open again]",
              "[no longer nearly]", "[expected pass]", "[P21[^|]{0,80}nearly]",
              "[nearly (determined|fix\\w*)[^|]{0,80}P21]"):
        assert p not in out, p


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
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.exit(1 if main() else 0)
