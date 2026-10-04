"""Unit tests for recheck_c8.py: every function on hand-built cases, then the
script on the real files. Run: py results/build-recheck-c8/test_recheck_c8.py"""
import io
import os
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recheck_c8 as R  # noqa: E402

M = R.MARKER + " cut -->"


def t_flatten_and_line_at():
    flat, starts = R.flatten("ab\n  cd \nef")
    assert flat == "ab cd ef" and starts == [0, 3, 6]
    assert [R.line_at(starts, k) for k in (0, 2, 3, 5, 6, 7)] == [1, 1, 2, 2, 3, 3]


def t_marker_line_and_public_text():
    doc = "a\nb\n" + M + "\nc\n"
    assert R.marker_line(doc) == 3
    assert R.public_text(doc) == "a\nb"
    for bad in ("a\nb\n", M + "\n" + M + "\n"):
        try:
            R.marker_line(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("marker count not enforced")


def t_scan_tiers_wrap_and_cells():
    doc = ("x | ALM-H | keeps its truth\nALM-D loses its\ntruth here\nP21 was a regression\nexpectation.\n"
           + M + "\nALM-B is the knife-edge\n")
    hits = R.scan(doc)
    got = [(h[0], h[1], h[2]) for h in hits]
    assert (2, "public", "set beside keep/lose truth") in got           # across a wrap
    assert not any(h[0] == 1 for h in hits)                             # not across a cell
    assert (4, "public", "P21 beside 'regression expectation'") in got
    assert (7, "AppT", "knife") in got and (7, "AppT", "only ALM-B") not in got
    assert got == sorted(got, key=lambda g: (g[0], g[2]))


def t_scan_patterns_each():
    cases = {"knife": "a knife-edge", "nearly settled": "nearly fixed", "open again": "open  again",
             "leaned / leans on": "it leaned on", "pivot / hinge": "pivotal set",
             "only ALM-B": "ALM-B alone", "favoured 'can see'": 'favoured "the method can see"'}
    for name, text in cases.items():
        hits = R.scan(text + "\n" + M + "\n")
        assert any(h[2] == name and h[1] == "public" for h in hits), name
    assert R.scan("a leaning tower\n" + M + "\n") == []          # word boundary after lean/leans/leaned


def t_detect_requires_every_phrase():
    stm = (("one", [r"alpha"]), ("both", [r"beta", r"gamma"]))
    assert R.detect("alpha beta\n" + M + "\ngamma\n", stm) == ["one"]       # gamma only below the marker
    assert R.detect("alpha beta\ngamma\n" + M + "\n", stm) == ["one", "both"]


def t_detect_real_statement_regexes():
    pub = ("the gate's margin\nwas nil. gate 3b 6 on every leg, and 5 under the other meaning; "
           "lower than 8 because a truth fails its own projection; P21 is open, and not fixed by known numbers; "
           "so they favoured \"the method can see\"; a set whose tolerance differs holds the outlier record, "
           "and its truth may fail; \"as printed\": IX.7.11, one Egyptian month (ALM-H.3); Ptolemy's Sun "
           "confirms both emended\nintervals; (gate 3b does not fire; ALM-B the knife-edge); the expected pass "
           "of gate 3b leaned on rows\n")
    assert R.detect(pub + M + "\n") == [s for s, _ in R.STATEMENTS]
    assert R.detect("nothing\n" + M + "\n" + pub) == []


def t_near_line():
    assert R.near_line(R.SHARES_V8) == {"ALM-A", "ALM-B", "ALM-H"}
    assert R.near_line(R.SHARES_V7) == {"ALM-B", "ALM-H"}
    assert R.near_line({"X": (4.35, 5.0)}) == {"X"} and R.near_line({"X": (4.34, 4.9)}) == frozenset()


def t_predicates():
    p = R.predicates(frozenset({"ALM-B", "ALM-H"}), frozenset({"ALM-A", "ALM-B", "ALM-H"}))
    f = frozenset
    assert p["S0x"](f({"ALM-A", "ALM-G"})) and not p["S0x"](f({"ALM-B", "ALM-G"}))
    assert p["row74"](f({"ALM-A", "ALM-G"})) and not p["row74"](f({"ALM-E", "ALM-G"}))
    assert p["row74"](f({"ALM-A", "ALM-H"})) and "held7" not in p
    assert p["notfix"](f({"ALM-G", "ALM-H"})) and not p["notfix"](f({"ALM-A", "ALM-H"}))
    assert p["favA"](f({"ALM-G", "ALM-H"})) and not p["favA"](f({"ALM-A", "ALM-G"}))
    assert p["T60"](f({"ALM-G", "ALM-D"})) and not p["T60"](f({"ALM-A", "ALM-D"}))
    assert p["cruxH"](f({"ALM-G", "ALM-H"})) and not p["cruxH"](f({"ALM-A", "ALM-G"}))
    assert p["P21v7"](f({"ALM-H", "ALM-D"})) and not p["P21v7"](f({"ALM-D", "ALM-G"}))
    assert p["R92"](f({"ALM-H", "ALM-D"})) and not p["R92"](f({"ALM-A", "ALM-D"}))


def t_consistent_pairs_and_identified():
    preds = {"noA": lambda L: "A" not in L, "hasB": lambda L: "B" in L}
    assert R.consistent_pairs(("C", "B", "A"), [], preds) == [("A", "B"), ("A", "C"), ("B", "C")]
    assert R.consistent_pairs(("A", "B", "C"), ["noA"], preds) == [("B", "C")]
    assert R.consistent_pairs(("A", "B", "C"), ["noA", "hasB"], preds) == [("B", "C")]
    assert R.identified([("B", "C")]) == ["B", "C"] and R.identified([]) == []
    assert R.identified([("B", "C"), ("B", "D")]) == ["B"] and R.identified([("A", "B"), ("C", "D")]) == []


def t_named_pair():
    assert R.named_pair("x\n" + M + "\nwhose truth is not in B under\nregime SL are ALM-X and ALM-C (T2)") == ("ALM-C", "ALM-X")
    assert R.named_pair("x\n" + M + "\nnothing\n") is None


def t_analyse_on_synthetic_text():
    pub = "the gate's margin was nil. gate 3b 6 on every leg, and 5 under the other meaning.\n"
    app = "whose truth is not in B under regime SL are ALM-D and ALM-E.\n"
    lines = []
    res = R.analyse(pub + M + "\n" + app, out=lines.append)
    n, idf, ok = res["c8 model (S0x, P21v7, R92)"]
    assert n == 21 and idf == [] and ok
    assert any("statements found" in l for l in lines)


def t_run_on_temp_files():
    pub_before = ("the gate's margin was nil. gate 3b 6 on every leg, and 5 under the other meaning. "
                  "v7 P21 (ALM-B the knife-edge)\n")
    pub_now = "the gate's margin was nil. gate 3b 6 on every leg, and 5 under the other meaning.\n"
    app = "whose truth is not in B under regime SL are ALM-G and ALM-H.\n"
    with tempfile.TemporaryDirectory() as d:
        b, n = os.path.join(d, "b.md"), os.path.join(d, "n.md")
        open(b, "w", encoding="utf-8").write(pub_before + M + "\n" + app)
        open(n, "w", encoding="utf-8").write(pub_now + M + "\n" + app)
        lines = []
        res = R.run(design=n, before=b, out=lines.append)
    before = res["revision 8 as first written"][0]["c8 model (S0x, P21v7, R92)"]
    now = res["DESIGN.md now"][0]["c8 model (S0x, P21v7, R92)"]
    assert before[1] == ["ALM-H"] and before[0] == 6 and before[2]
    assert now[1] == [] and now[0] == 21 and now[2]
    assert res["revision 8 as first written"][1] == ["ALM-B the knife-edge"] and res["DESIGN.md now"][1] == []


def t_selftest_passes():
    lines = []
    assert R.selftest(out=lines.append) == 0, lines


def t_main_modes():
    old = sys.stdout
    try:
        sys.stdout = io.StringIO()
        assert R.main(["--selftest"]) == 0
        assert "selftest: passed" in sys.stdout.getvalue()
    finally:
        sys.stdout = old


def t_real_files():
    lines = []
    res = R.run(out=lines.append)
    before, now = res["revision 8 as first written"], res["DESIGN.md now"]
    # the c8 model reproduces the check's finding on the copy as first written ...
    assert before[0]["c8 model (S0x, P21v7, R92)"][1] == ["ALM-H"]
    # ... and finds nothing identified from the design's own statements now
    for label in ("c8 model (S0x, P21v7, R92)", "+ row74, notfix", "+ favA at its strongest"):
        assert now[0][label][1] == [], label
    assert now[0]["c8 model (S0x, P21v7, R92)"][0] == 21          # the amendment's own count
    assert now[0]["+ T60"][1] == ["ALM-G"]
    assert now[0]["design statements + cruxH (inherent)"][1] == ["ALM-H"]
    assert now[1] == []                                   # no removed word is public
    # every variant admits the pair Appendix T names (the model is not contradicted)
    for label, (n, idf, ok) in list(now[0].items()) + list(before[0].items()):
        assert ok and n >= 1, label
    shares = [l for l in lines if l.startswith("  shares printed")]
    assert len(shares) == 2 and all("False" not in l for l in shares), shares


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("t_") and callable(v)]

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
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
    sys.exit(1 if failed else 0)
