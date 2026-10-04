"""Re-check of the amendment made to DESIGN.md revision 8 after the check of
revision 8 [c8] (truth tier). Evaluates no sky and opens no truth file. It reads
DESIGN.md and the byte copy of revision 8 as first written
(results/design-revision-v8/DESIGN-v8-before-c8.md); it reads Appendix T of
DESIGN.md only to check that the model admits R10's named pair.

1. Wording scan (scan). A broader set of phrases than public_inference.py
   uses, each listed with its line and tier ('public' above the Appendix T
   marker, 'AppT' below it), for review by hand. Lines are joined first, so a
   phrase broken by a line wrap is found; a match never crosses a table cell.

2. Statement detection (detect). Which public statements a reader can use
   about R10's two exceptions. Each statement is found by literal phrases in
   the public part; all of a statement's phrases must be present.

3. Pair model (consistent_pairs). For each combination of detected
   statements, the pairs of counted sets that could be R10's two exceptions,
   and the sets that are an exception in every such pair (identified).
   Statements beyond public_inference.py's model:
     row74   14.5 row 74: held_ALM's ceiling is below 8 "because a truth fails
             its own projection", so at least one exception has held-out rows;
             (S0x inherits S0's "held_ALM 7" and 9.5 marks it as contradicting
             nothing, but 9.4's known facts hold no held_ALM ceiling, so that
             says nothing about the truth-side ceiling and is not used;)
     notfix  "not fixed by known numbers" / "the known numbers do not settle"
             (P21, 2.10): at least two near-line sets keep their truth under
             revision 8's projection;
     favA    6.4's and row 92's "favoured 'the method can see'", at its
             strongest: ALM-A keeps its truth;
     T60     13 row 60's tolerance hint at its strongest: ALM-G loses it;
     cruxH   2.6 and 13 row 29: ALM-H.3 is a one-month crux whose emended
             interval Ptolemy's Sun confirms, run at its printed primary; a
             reader who knows Mercury's motion infers that ALM-H's truth
             probably fails. Inherent in the clue file.

Run:
  py results/build-recheck-c8/recheck_c8.py
  py results/build-recheck-c8/recheck_c8.py --selftest   (synthetic text and sets only)
"""
import bisect
import io
import itertools
import re
import sys

DESIGN = "C:/Projects/odybench/DESIGN.md"
BEFORE = "C:/Projects/odybench/results/design-revision-v8/DESIGN-v8-before-c8.md"
MARKER = "<!-- APPENDIX-T"

COUNTED = ("ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H",
           "ALM-I", "ALM-J", "ALM-K", "ALM-L")
NARROWABLE = ("ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H", "ALM-L")  # 2.6
HELDOUT = frozenset(("ALM-A", "ALM-B", "ALM-D", "ALM-H", "ALM-I", "ALM-J", "ALM-K", "ALM-L"))  # 6.4

# the design-stage shares (percent of a window's days) as the public part prints them
# (2.6 and 14.7 row 92); ALM-H's rows are not touched by revision 8
SHARES_V8 = {"ALM-A": (4.88, 4.89), "ALM-B": (4.40, 4.45), "ALM-H": (4.37, 4.59)}
SHARES_V7 = {"ALM-A": (0.54, 0.60), "ALM-B": (4.40, 4.45), "ALM-H": (4.37, 4.59)}
SHARE_TEXT = ("ALM-A 4.88–4.89%", "ALM-B 4.40–4.45%", "ALM-H 4.37–4.59%", "0.54–0.60% of days")

CELL = r"(?:(?!\.\s)[^|]){0,80}?"   # inside one table cell and one sentence

# phrases for review by hand: (name, regex over the joined text)
SCAN = (
    ("knife", r"knife"),
    ("nearly settled", r"nearly\s+(?:determined|fix\w*|settled|decided|certain)"),
    ("open again", r"open\s+again"),
    ("leaned / leans on", r"\blean(?:s|ed)?\b"),
    ("pivot / hinge", r"pivot\w*|hinge\w*"),
    ("only ALM-B", r"only\s+ALM-B|ALM-B\s+alone|single\s+knife|one\s+knife"),
    ("P21 beside 'regression expectation'",
     r"P21" + CELL + r"regression\s+expectation|regression\s+expectation" + CELL + r"P21"),
    ("set beside keep/lose truth",
     r"ALM-[A-L]" + CELL + r"\b(?:keeps?|loses?|retains?|lost|kept)\s+(?:its|their)\s+truth"),
    ("favoured 'can see'", r"favour\w*\s+\"the method can see\""),
)

# statements a reader can use: (name, [regexes that must all match the public part])
STATEMENTS = (
    ("nil", [r"the gate's margin\s+was\s+nil"]),
    ("S0x", [r"gate 3b 6 on every leg, and 5 under the other meaning"]),
    ("row74", [r"because a truth fails its own projection"]),
    ("notfix", [r"not fixed by known numbers|known numbers do not settle"]),
    ("favA", [r"favoured\s+\"the method can see\""]),
    ("T60", [r"a set whose tolerance differs holds the outlier record, and its truth may fail"]),
    ("cruxH", [r"IX\.7\.11, one Egyptian month \(ALM-H\.3\)", r"confirms both emended\s+intervals"]),
    ("P21v7", [r"ALM-B,?\s+(?:is\s+)?the\s+knife-edge|nearly\s+determined\s+by\s+known\s+numbers"]),
    ("R92", [r"expected\s+pass" + CELL + r"lean"]),
)

# the words Appendix T says revision 8 first printed above the marker
REMOVED = ("ALM-B the knife-edge", "nearly determined by known numbers", "open again",
           "no longer nearly fix", "expected pass of gate 3b leaned")


def flatten(text):
    """(flat, starts): the lines stripped and joined by single spaces, and the
    offset in flat at which each line starts"""
    starts, parts, pos = [], [], 0
    for line in text.split("\n"):
        t = line.strip()
        starts.append(pos)
        parts.append(t)
        pos += len(t) + 1
    return " ".join(parts), starts


def line_at(starts, k):
    """1-based line number holding offset k of the joined text"""
    return bisect.bisect_right(starts, k)


def marker_line(text, marker=MARKER):
    """1-based line of the Appendix T marker; ValueError unless it occurs exactly once"""
    idx = [i for i, l in enumerate(text.split("\n"), 1) if l.startswith(marker)]
    if len(idx) != 1:
        raise ValueError(f"the marker occurs {len(idx)} times")
    return idx[0]


def public_text(text, marker=MARKER):
    """the lines above the marker line, as one string"""
    return "\n".join(text.split("\n")[:marker_line(text, marker) - 1])


def scan(text, patterns=SCAN, marker=MARKER):
    """[(line, tier, name, excerpt)] for every match, sorted by line and name"""
    ml = marker_line(text, marker)
    flat, starts = flatten(text)
    hits = []
    for name, rx in patterns:
        for m in re.finditer(rx, flat):
            ln = line_at(starts, m.start())
            hits.append((ln, "public" if ln < ml else "AppT", name,
                         flat[max(0, m.start() - 60):m.end() + 40]))
    hits.sort(key=lambda h: (h[0], h[2]))
    return hits


def detect(text, statements=STATEMENTS, marker=MARKER):
    """the names of the statements whose every regex matches the joined public part"""
    flat = flatten(public_text(text, marker))[0]
    return [name for name, rxs in statements if all(re.search(rx, flat) for rx in rxs)]


def near_line(shares, line=5.0, band=0.65):
    """sets whose printed share range lies inside [line - band, line]"""
    return frozenset(s for s, (lo, hi) in shares.items() if line - band <= lo and hi <= line)


def predicates(near_v7, near_v8, heldout=HELDOUT):
    """{statement: predicate on L, the frozenset of the two sets that lose their truth}"""
    return {
        "S0x": lambda L: "ALM-B" not in L,
        "row74": lambda L: len(L & heldout) >= 1,
        "notfix": lambda L: len(near_v8 - L) >= 2,
        "favA": lambda L: "ALM-A" not in L,
        "T60": lambda L: "ALM-G" in L,
        "cruxH": lambda L: "ALM-H" in L,
        "P21v7": lambda L: near_v7 - L == {"ALM-B"},
        "R92": lambda L: "ALM-A" not in L,
    }


def consistent_pairs(pool, active, preds):
    """the pairs (sorted tuples) of sets in pool that satisfy every active predicate"""
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


def named_pair(text, marker=MARKER):
    """R10's two exceptions as Appendix T names them, or None"""
    app = flatten(text[text.index(marker):])[0]
    m = re.search(r"whose truth is not in B under\s+regime SL are (ALM-[A-Z]) and (ALM-[A-Z])", app)
    return tuple(sorted(m.groups())) if m else None


VARIANTS = (
    ("c8 model (S0x, P21v7, R92)", ("S0x", "P21v7", "R92")),
    ("+ row74, notfix", ("S0x", "P21v7", "R92", "row74", "notfix")),
    ("+ favA at its strongest", ("S0x", "P21v7", "R92", "row74", "notfix", "favA")),
    ("+ T60", ("S0x", "P21v7", "R92", "row74", "notfix", "favA", "T60")),
    ("design statements + cruxH (inherent)", ("S0x", "P21v7", "R92", "row74", "notfix", "cruxH")),
    ("everything + T60 + cruxH", ("S0x", "P21v7", "R92", "row74", "notfix", "favA", "T60", "cruxH")),
)


def analyse(text, out=print):
    """print and return {variant: (n_pairs, identified, named_ok)} for one copy of the file"""
    found = detect(text)
    pool = NARROWABLE if "nil" in found else COUNTED
    preds = predicates(near_line(SHARES_V7), near_line(SHARES_V8))
    named = named_pair(text)
    out(f"  statements found in the public part: {found}")
    res = {}
    for label, wanted in VARIANTS:
        active = [c for c in wanted if c in found]
        pairs = consistent_pairs(pool, active, preds)
        idf = identified(pairs)
        ok = named is not None and named in pairs
        res[label] = (len(pairs), idf, ok)
        out(f"  {label}: active {active}; {len(pairs)} pairs; identified: {idf if idf else 'none'}; "
            f"named pair admitted: {ok}")
    return res


def run(design=DESIGN, before=BEFORE, out=print):
    out(f"near the line: revision 7 {sorted(near_line(SHARES_V7))}, revision 8 {sorted(near_line(SHARES_V8))}")
    results = {}
    for label, path in (("revision 8 as first written", before), ("DESIGN.md now", design)):
        text = open(path, encoding="utf-8").read()
        flat_pub = flatten(public_text(text))[0]
        out(f"\n{label} ({path}):")
        out("  shares printed in the public part: "
            + ", ".join(f"{s!r} {s in flat_pub}" for s in SHARE_TEXT))
        hits = scan(text)
        pub = [h for h in hits if h[1] == "public"]
        out(f"  wording scan: {len(pub)} public hits, {len(hits) - len(pub)} Appendix T hits")
        for h in pub:
            out(f"    l. {h[0]} [{h[2]}] ...{h[3]}...")
        removed = [w for w in REMOVED if w in flat_pub]
        out(f"  words Appendix T lists as removed, still public: {removed if removed else 'none'}")
        results[label] = (analyse(text, out), removed, pub)
    return results


def selftest(out=print):
    """the functions on synthetic text and sets only; returns the number of failures"""
    fails = 0

    def check(cond, msg):
        nonlocal fails
        out(("ok   " if cond else "FAIL ") + msg)
        fails += 0 if cond else 1

    doc = ("# toy\n| x | P21 is open\nagain | y |\nthe gate's margin was nil; gate 3b 6 on every leg,"
           " and 5 under the other meaning.\nso they favoured \"the method can see\".\n"
           + MARKER + " -->\nP21 nearly determined.\nwhose truth is not in B under regime SL are ALM-Q and ALM-P.\n")
    hits = scan(doc)
    check([(h[0], h[1], h[2]) for h in hits] == [
        (2, "public", "open again"), (5, "public", "favoured 'can see'"), (7, "AppT", "nearly settled")],
        "scan: a phrase across a wrap, the tiers, and the line numbers")
    check(detect(doc) == ["nil", "S0x", "favA"], "detect: statements with every phrase present")
    check(named_pair(doc) == ("ALM-P", "ALM-Q"), "named_pair parses the synthetic Appendix T")
    check(near_line({"X": (4.4, 4.5), "Y": (4.2, 4.9), "Z": (4.9, 5.1)}) == {"X"},
          "near_line: whole range inside the band")
    preds = predicates(frozenset({"ALM-B", "ALM-H"}), frozenset({"ALM-A", "ALM-B", "ALM-H"}))
    pool = ("ALM-A", "ALM-B", "ALM-D", "ALM-G", "ALM-H")
    check(len(consistent_pairs(pool, ["S0x"], preds)) == 6, "S0x alone: C(4,2) pairs")
    pairs = consistent_pairs(pool, ["S0x", "P21v7"], preds)
    check(identified(pairs) == ["ALM-H"], "a single revision-7 knife-edge identifies the other near set")
    check(consistent_pairs(pool, ["S0x", "notfix"], preds)
          == [p for p in consistent_pairs(pool, ["S0x"], preds) if p != ("ALM-A", "ALM-H")],
          "notfix removes only the pair that leaves one revision-8 knife-edge")
    check(consistent_pairs(pool, ["S0x", "row74"], preds)
          == [p for p in consistent_pairs(pool, ["S0x"], preds) if p != ("ALM-E", "ALM-G")]
          and consistent_pairs(("ALM-A", "ALM-E", "ALM-G"), ["row74"], preds)
          == [("ALM-A", "ALM-E"), ("ALM-A", "ALM-G")],
          "row74: at least one exception with held-out rows (ALM-E and ALM-G have none)")
    check(identified([]) == [] and identified([("a", "b"), ("a", "c")]) == ["a"], "identified")
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
