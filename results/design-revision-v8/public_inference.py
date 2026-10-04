"""Design revision 8 scratch, added after the check of revision 8 [c8]
(results/design-check-v8/): does the public part of DESIGN.md describe
revision 7's P21 in words that rest on which counted *Almagest* sets keep their
truth, and what can a public-tier reader deduce from the public statements?

Neither part evaluates the sky or opens a truth file. The only numbers read are
the recheck's recorded design-stage narrowing (null side, through
narrowing_v8.py), and the only truth-side text read is Appendix T of DESIGN.md
itself, to check the model against R10's two named exceptions.

1. Phrase scan (characterisation_hits). Every match of PATTERNS is listed with
   its line and tier: 'public' above the Appendix T marker, 'AppT' below it.
   Lines are joined first, so that a phrase broken across a line wrap is still
   found; a match never crosses a table cell ('|').

2. Inference check (consistent_pairs). R10 has two exceptions, which only
   [AppT 6] names. A public-tier reader knows, from statements that predate
   revision 8 and that the check accepted:
     base  9 of the 11 counted sets keep their truth (2.6), and gate 3b's
           margin was nil (14.6 row 82), so exactly 2 of the 8 sets that can be
           narrowed lose it ("nil"; without it the pool is all 11 sets);
     S0x   gate 3b counts 6, and 5 when ALM-B cannot be narrowed (9.5), so
           ALM-B keeps its truth.
   The phrases of part 1 add, when they appear in the public part:
     P21v7 "ALM-B the knife-edge", "nearly determined", "open again", "no longer
           nearly fix it": revision 7's P21 had one knife-edge, ALM-B, so no
           other set that keeps its truth lay near the line under revision 7's
           projection;
     P21v8 "two knife-edges": exactly two sets that keep their truth lie near
           the line under revision 8's projection;
     R92   "the expected pass of gate 3b leaned on" A.2 and A.5: ALM-A keeps
           its truth.
   and, as a separate variant, because the design records it as inherent:
     T60   13 row 60's per-set tolerance hint, taken at its strongest: ALM-G
           loses its truth.
   "Near the line" is within 0.65 percentage points under the 5% line in
   every window of the recheck's recorded runs (narrowing_v8.py's list).
   For each set of constraints the script lists the pairs of sets that could
   be the two exceptions; a set that is an exception in every such pair is
   identified.

Run:
  py results/design-revision-v8/public_inference.py
  py results/design-revision-v8/public_inference.py --selftest   (synthetic text and sets only)
"""
import bisect
import io
import itertools
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

DESIGN = "C:/Projects/odybench/DESIGN.md"
BEFORE = os.path.join(HERE, "DESIGN-v8-before-c8.md")
MARKER = "<!-- APPENDIX-T"
LINE = 0.05
BAND = 0.0065          # 0.65 percentage points, as narrowing_v8.py's near-line list

COUNTED = ("ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H",
           "ALM-I", "ALM-J", "ALM-K", "ALM-L")
NARROWABLE = ("ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H", "ALM-L")

# up to 80 characters inside one table cell and one sentence: never across '|',
# nor across a full stop followed by a space (a dot inside "A.2" or "(2.7)" is crossed)
W = r"(?:(?!\.\s)[^|]){0,80}?"

# (name, regex over the joined text, the constraint the phrase lets a reader add)
PATTERNS = (
    ("ALM-B the knife-edge", r"ALM-B,?\s+(?:is\s+)?the\s+knife-edge", "P21v7"),
    ("nearly determined by known numbers", r"nearly\s+determined\s+by\s+known\s+numbers", "P21v7"),
    ("P21 beside 'nearly determined/fixed'",
     r"P21" + W + r"nearly\s+(?:determined|fix\w*|settled|decided)"
     r"|nearly\s+(?:determined|fix\w*|settled|decided)" + W + r"P21", "P21v7"),
    ("no longer nearly", r"no\s+longer\s+nearly", "P21v7"),
    ("open again", r"open\s+again", "P21v7"),
    ("two knife-edges", r"two\s+knife-edges", "P21v8"),
    ("expected pass ... leaned", r"expected\s+pass" + W + r"lean", "R92"),
)

# statements that predate revision 8 and that the check accepted as public
BASE = {"S0x": r"gate 3b 6 on every leg, and 5 under the other meaning",
        "nil": r"the gate's margin\s+was\s+nil"}


def flatten(text):
    """(flat, starts): the lines stripped and joined by single spaces, and the
    offset in flat at which each line starts (0-based list)"""
    starts, parts, pos = [], [], 0
    for l in text.split("\n"):
        t = l.strip()
        starts.append(pos)
        parts.append(t)
        pos += len(t) + 1
    return " ".join(parts), starts


def line_at(starts, k):
    """1-based line number holding offset k of the joined text"""
    return bisect.bisect_right(starts, k)


def marker_line(text, marker=MARKER):
    """1-based line number of the Appendix T marker; ValueError unless it occurs once"""
    idx = [i for i, l in enumerate(text.split("\n"), 1) if l.startswith(marker)]
    if len(idx) != 1:
        raise ValueError(f"the marker occurs {len(idx)} times")
    return idx[0]


def characterisation_hits(text, patterns=PATTERNS, marker=MARKER):
    """[(line, tier, name, constraint, excerpt)] for every match, sorted by line;
    tier is 'public' above the marker line and 'AppT' below it"""
    ml = marker_line(text, marker)
    flat, starts = flatten(text)
    out = []
    for name, rx, con in patterns:
        for m in re.finditer(rx, flat):
            ln = line_at(starts, m.start())
            out.append((ln, "public" if ln < ml else "AppT", name, con,
                        flat[max(0, m.start() - 50):m.end() + 30]))
    out.sort(key=lambda h: (h[0], h[2]))
    return out


def public_flat(text, marker=MARKER):
    """the joined text of the public part (above the marker line)"""
    ml = marker_line(text, marker)
    return flatten("\n".join(text.split("\n")[:ml - 1]))[0]


def active_constraints(text, patterns=PATTERNS, base=BASE, marker=MARKER):
    """(active, nil): the constraints the public part supports, in the order
    S0x, P21v7, P21v8, R92; and whether the nil-margin statement is public"""
    pub = public_flat(text, marker)
    hits = characterisation_hits(text, patterns, marker)
    act = ["S0x"] if re.search(base["S0x"], pub) else []
    for c in ("P21v7", "P21v8", "R92"):
        if any(h[1] == "public" and h[3] == c for h in hits):
            act.append(c)
    return act, bool(re.search(base["nil"], pub))


def near_line(table, band=BAND, line=LINE):
    """sets whose share lies in [line - band, line] in every window of
    table = {window: {set: (frac, n_pass, n_cand)}}"""
    tags = list(table)
    sets = sorted(set.intersection(*(set(table[t]) for t in tags))) if tags else []
    return [s for s in sets if all(line - band <= table[t][s][0] <= line for t in tags)]


def recorded_near():
    """(near under revision 7's projection, near under revision 8's), from the
    recheck's recorded runs through narrowing_v8.py (no sky is evaluated)"""
    import narrowing_v8 as N
    rep = json.load(open(N.SRC, encoding="utf-8"))
    return near_line(N.assemble(rep, N.ROW_V7)), near_line(N.assemble(rep, N.ROW_V8))


def constraint_preds(near_v7, near_v8, knife="ALM-B", leaned="ALM-A", tol="ALM-G"):
    """{constraint: predicate on the frozenset of the two sets that lose their truth}"""
    return {
        "S0x": lambda L: knife not in L,
        "P21v7": lambda L: {s for s in near_v7 if s not in L} == {knife},
        "P21v8": lambda L: len([s for s in near_v8 if s not in L]) == 2,
        "R92": lambda L: leaned not in L,
        "T60": lambda L: tol in L,
    }


def consistent_pairs(pool, active, preds):
    """the pairs (sorted tuples) of sets in pool that satisfy every active constraint"""
    return [p for p in itertools.combinations(sorted(pool), 2)
            if all(preds[c](frozenset(p)) for c in active)]


def identified(pairs):
    """the sets that are an exception in every pair; empty when there is no pair"""
    if not pairs:
        return []
    common = set(pairs[0])
    for p in pairs[1:]:
        common &= set(p)
    return sorted(common)


def loser_counts(pairs, pool):
    """{set: the number of pairs in which it is an exception}"""
    return {s: sum(s in p for p in pairs) for s in sorted(pool)}


def named_exceptions(text, marker=MARKER):
    """R10's two exceptions as Appendix T names them, or None (truth-side text;
    used only to check that the model admits them)"""
    app = flatten(text[text.index(marker):])[0]
    m = re.search(r"whose truth is not in B under\s+regime SL are (ALM-[A-Z]) and (ALM-[A-Z])", app)
    return tuple(sorted(m.groups())) if m else None


def analyse(text, near_v7, near_v8, out):
    """print the scan and the inference for one copy of the file; return a dict of results"""
    hits = characterisation_hits(text)
    pub = [h for h in hits if h[1] == "public"]
    app = [h for h in hits if h[1] == "AppT"]
    out(f"  public hits: {len(pub)}")
    for h in pub:
        out(f"    l. {h[0]} [{h[2]}] -> {h[3]}: ...{h[4]}...")
    out(f"  Appendix T hits: {len(app)} (the explanation kept there: "
        f"{sorted(set(h[2] for h in app))})")
    act, nil = active_constraints(text)
    pool = NARROWABLE if nil else COUNTED
    preds = constraint_preds(near_v7, near_v8)
    named = named_exceptions(text)
    res = {"public_hits": len(pub), "appt_hits": len(app), "active": act, "nil": nil}
    for variant, extra in (("without 13 row 60", []), ("with 13 row 60's hint (T60)", ["T60"])):
        cons = act + extra
        pairs = consistent_pairs(pool, cons, preds)
        idf = identified(pairs)
        ok = named is not None and named in pairs
        out(f"  {variant}: constraints {['base' + ('+nil' if nil else '')] + cons}; "
            f"{len(pairs)} pairs could be R10's exceptions; identified: {idf if idf else 'none'}")
        cnt = loser_counts(pairs, pool)
        out("    times each set is an exception: " + ", ".join(f"{s[4:]} {n}" for s, n in cnt.items()))
        out(f"    the pair named in [AppT 6] is among them: {ok}")
        res[variant] = {"pairs": pairs, "identified": idf, "named_ok": ok}
    return res


def run(design=DESIGN, before=BEFORE, out=print):
    near_v7, near_v8 = recorded_near()
    out("near the line (within 0.65 points under 5% in every window of the recheck's recorded runs):")
    out(f"  revision 7's projection: {near_v7}")
    out(f"  revision 8's projection: {near_v8}")
    results = {}
    for label, path in (("revision 8 as first written (DESIGN-v8-before-c8.md)", before),
                        ("DESIGN.md now", design)):
        out(f"\n{label}:")
        text = open(path, encoding="utf-8").read()
        results[label] = analyse(text, near_v7, near_v8, out)
    now = results["DESIGN.md now"]
    first = results["revision 8 as first written (DESIGN-v8-before-c8.md)"]
    out("\nverdict:")
    out(f"  as first written, the public part identified a withheld exception: "
        f"{bool(first['without 13 row 60']['identified'])}")
    out(f"  now: no public characterisation: {now['public_hits'] == 0}")
    out(f"  now: Appendix T still states the explanation: {now['appt_hits'] > 0}")
    out(f"  now: no set identified from the public statements alone: "
        f"{not now['without 13 row 60']['identified']}")
    out(f"  now: with 13 row 60's inherent hint, only that hint's set is identified: "
        f"{now['with 13 row 60' + chr(39) + 's hint (T60)']['identified'] == ['ALM-G']}")
    return results


def selftest(out=print):
    """the functions on synthetic text and synthetic sets only; returns the number of failures"""
    fails = 0

    def check(cond, msg):
        nonlocal fails
        out(("ok   " if cond else "FAIL ") + msg)
        fails += 0 if cond else 1

    doc = ("# toy\n| v7 P21 (x; ALM-B the knife-edge) | **nearly determined by known numbers** |\n"
           "P21 is open\nagain here.\nP8 was nearly fixed by a calibration.\n"
           "S0x: gate 3b 6 on every leg, and 5 under the other meaning; the gate's margin\nwas nil.\n"
           + MARKER + " cut -->\nthat is why P21 nearly determined.\n"
           "whose truth is not in B under regime SL are ALM-Q and ALM-P (T2).\n")
    hits = characterisation_hits(doc)
    check([(h[0], h[1], h[2]) for h in hits] == [
        (2, "public", "ALM-B the knife-edge"), (2, "public", "nearly determined by known numbers"),
        (3, "public", "open again"), (9, "AppT", "P21 beside 'nearly determined/fixed'")],
        "phrase scan: tiers, line numbers, a phrase across a wrap, and no hit for P8")
    act, nil = active_constraints(doc)
    check(act == ["S0x", "P21v7"] and nil, "active constraints from the synthetic public part")
    check(named_exceptions(doc) == ("ALM-P", "ALM-Q"), "named exceptions parsed from the synthetic Appendix T")
    pool = ("ALM-A", "ALM-B", "ALM-P", "ALM-Q", "ALM-R")
    preds = constraint_preds(["ALM-B", "ALM-Q"], ["ALM-A", "ALM-B", "ALM-Q"], tol="ALM-P")
    pairs = consistent_pairs(pool, ["S0x"], preds)
    check(len(pairs) == 6 and identified(pairs) == [], "S0x alone leaves C(4,2) = 6 pairs, none identified")
    pairs = consistent_pairs(pool, ["S0x", "P21v7"], preds)
    check(identified(pairs) == ["ALM-Q"] and len(pairs) == 3, "one knife-edge under revision 7 identifies ALM-Q")
    pairs = consistent_pairs(pool, ["S0x", "P21v7", "T60"], preds)
    check(pairs == [("ALM-P", "ALM-Q")], "with the tolerance hint both are identified")
    table = {"w1": {"X": (0.049, 1, 1), "Y": (0.02, 1, 1)}, "w2": {"X": (0.0436, 1, 1), "Y": (0.049, 1, 1)}}
    check(near_line(table) == ["X"], "near_line needs every window inside the band")
    return fails


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        f = selftest()
        print(f"selftest: {'passed' if not f else f'{f} failed'}")
        return 1 if f else 0
    run()
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.exit(main())
