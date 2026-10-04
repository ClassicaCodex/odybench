"""Scratch (A0, truth tier): drafts data/prereg/heldout_disclosure.json (DESIGN 7.1,
10.2, 12.1 item 9) from the scan of tools/disclosure_scan.py and the published
sources, and checks that its sealed facts cover every scan hit of a sealed
class (sealed_list(...)["uncovered"] must be empty).

Run from C:\\Projects\\odybench after the scan:
    py tools/disclosure_scan.py --json results/build-A0/disclosure_scan.json
    py results/build-A0/draft_disclosure.py
No value of the target's sky is read or written here: the facts are described
in words, and every number below is a line number, a date of record or a value
DESIGN section 2 already prints (D2, D4).
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import disclosure_scan as D  # noqa: E402

SCAN = ROOT / "results" / "build-A0" / "disclosure_scan.json"
OUT = ROOT / "data" / "prereg" / "heldout_disclosure.json"

R = "results/"
PDFS = ["data/bm2008-a/baikouzis-magnasco-2008-pnas.pdf", "data/refs/baikouzis-magnasco-2008.pdf",
        "data/sources/bm2008-b/baikouzis-magnasco-2008-pnas.pdf"]
D5_FILES = [f"data/ephem/horizons/venus_mercury_m1177_{w}_{b}.txt"
            for w in ("03_14_dusk", "04_10_dawn") for b in ("199", "299")]
D5_OUTPUTS = ["results/validate_ephem.txt", "results/data-acquisition/validate_ephem.after.txt",
              "results/data-acquisition/validate_ephem.after1.txt",
              "results/data-acquisition/validate_ephem.before.txt"]

FACTS = [
    {"id": "D1",
     "fact": "Mars was not visible in March-April 1178 BC except during the eclipse",
     "source": "B&M 2008, section Historical Plausibility (published 2008); docs/research-bm2008.md l. 64",
     "on_record_since": "2008 (publication)",
     "bears_on": ["H4", "H5"], "status": "settles",
     "reasoning": "With D2, settles H4: fails. An invisible Mars stood within about 20 deg of the Sun, and "
                  "a Venus that rises 1 h 43 min before the Sun stands far west of it, so the two cannot "
                  "lie within 5 deg of each other on Days -10 to -4 (DESIGN 7.1).",
     "scan_classes": ["D1"],
     "locators": [{"path": "docs/research-bm2008.md", "lines": [64], "found_by": "design"},
                  {"path": "docs/research-bm2008-b.md", "lines": [413], "found_by": "review",
                   "note": "the same remark in the second extraction"}]},
    {"id": "D2",
     "fact": "Venus a morning star far west of the Sun around Day -5: lead 1:42:56 on Ti-5; greatest "
             "morning elongation in mid-March",
     "source": "On record: B&M 2008, section Intersecting (the lead); MacDonald 1967 p. 327 ('17 March', "
               "under a year that is a slip for 1178) [unread 2.5]. Corroboration written after the "
               "freeze, not record [r2v6 N7]: rev V10 (103.6 min, written 3 Oct at 21:02) and unread 2.5 "
               "(44.3 deg west on 11 Apr, written 4 Oct)",
     "on_record_since": "2008 (B&M); 1967 (MacDonald)",
     "bears_on": ["H4"], "status": "settles",
     "reasoning": "With D1, settles H4: fails (see D1). Its values are printed in DESIGN 2.2, 2.5 and 2.10.",
     "scan_classes": ["D2", "H4-other"], "locators": []},
    {"id": "D3",
     "fact": "At the eclipse, all five naked-eye planets within 90 deg of the ecliptic, with each one's "
             "magnitude",
     "source": "B&M 2008, Fig. 1; docs/research-bm2008.md l. 596; docs/research-bm2008-b.md l. 410. The "
               "scan also finds it in docs/research-bm2008-a.md l. 315 (the third extraction note), in "
               "the paper's own text (data/bm2008-a/bm2008-pmc-fulltext.txt ll. 57-58, data/refs/bm2008.txt "
               "l. 42) and on page 1 of the three PDF copies of the paper",
     "on_record_since": "2008 (publication)",
     "bears_on": ["H3", "H4", "H5"], "status": "constrains",
     "reasoning": "Mercury's brightness on Day 0 bears on its phase, and so on how far it stood from a "
                  "conjunction; its position bears on its visibility on Day 0. Whether that fixes H3 "
                  "cannot be decided without evaluating H3 at the target (DESIGN 7.1). Sealed.",
     "scan_classes": ["D3"],
     "locators": [{"path": "docs/research-bm2008.md", "lines": [596], "found_by": "design"},
                  {"path": "docs/research-bm2008-b.md", "lines": [410], "found_by": "design"},
                  {"path": "docs/research-bm2008-a.md", "lines": [315], "found_by": "scan"},
                  {"path": "data/bm2008-a/bm2008-pmc-fulltext.txt", "lines": [57, 58], "found_by": "review"},
                  {"path": "data/refs/bm2008.txt", "lines": [42], "found_by": "scan"},
                  {"path": "docs/research-chronology.md", "lines": [64], "found_by": "review",
                   "note": "conservative: names B&M's figure, the eclipse, Mercury and Venus with an "
                           "elongation code; not read, so sealed"}]
                 + [{"path": p, "file": True, "found_by": "review", "note": "Fig. 1 caption on page 1"}
                    for p in PDFS]},
    {"id": "D4",
     "fact": "Mercury's spring events of -1177: a morning station on 5 Mar, the greatest western "
             "elongation on 19 Mar, and the rise-azimuth maximum about 12.3 Mar",
     "source": "vis 2.3 (2026-10-03); rev #12; DESIGN 2.9",
     "on_record_since": "2026-10-03 (research-visibility)",
     "bears_on": ["H3"], "status": "constrains",
     "reasoning": "Mercury's superior conjunction follows its greatest western elongation by roughly five "
                  "weeks. Public by design (DESIGN 7.1, R3-9): these are the reproduction of B&M's own "
                  "fitted clue M, printed in DESIGN 2.2 and 2.9, so they are not sealed.",
     "scan_classes": ["D4"], "locators": []},
    {"id": "D5",
     "fact": "Horizons tables of Mercury and Venus at Ithaki, at dusk on 14 Mar -1177 (Day -33) and at "
             "dawn on 10 Apr -1177 (Day -6): quantities 1, 2, 4, 20, 23 (elongation) and 30",
     "source": "data/ephem/horizons/venus_mercury_m1177_{03_14_dusk,04_10_dawn}_{199,299}.txt, fetched "
               "2026-10-03 19:40 local, 45 minutes before revision 1 froze H3 and H4. Printed by "
               "results/validate_ephem.txt and results/data-acquisition/validate_ephem.*.txt, and, as the "
               "scan finds, by docs/research-ephemeris.md in its sections 7 and 10",
     "on_record_since": "2026-10-03 19:40 local",
     "bears_on": ["H3"], "status": "constrains",
     "reasoning": "Mercury's elongation six days before Day 0 bounds where it could stand on Days 0 and +1. "
                  "Its values are not read before the second freeze. Sealed.",
     "scan_classes": ["D5", "D5-output", "H3-other"],
     "locators": ([{"path": p, "file": True, "found_by": "design"} for p in D5_FILES]
                  + [{"path": p, "file": True, "found_by": "design"} for p in D5_OUTPUTS]
                  + [{"glob": "results/instrument/i1/*", "found_by": "design",
                      "note": "I1's rerun (tools/run_i1.py, A6) writes its full output here"}]
                  + [{"path": "docs/research-ephemeris.md", "lines": [552, 553, 570, 571, 572, 573]
                      + list(range(950, 962)), "found_by": "scan",
                      "note": "rows of the Horizons comparison at the D5 instants; 571-573 conservative"},
                     {"path": "docs/critique-design-r1.md", "lines": [286, 701], "found_by": "scan",
                      "note": "conservative: Mercury at Day -6 with numbers, in the recheck of revision 5"},
                     {"path": "results/design-revision-v6/critique-design-r1.recheck-of-rev5.md",
                      "lines": [286, 701], "found_by": "scan", "note": "byte copy of the line above"}])},
    {"id": "D6",
     "fact": "The Sun and the Moon at the eclipse, and the eclipse's local circumstances",
     "source": "data/ephem/horizons/sun_moon_m1177_04_16_eclipse_{10,301}.txt; DESIGN 2.3; NASA's canon "
               "and site catalogues (data/jsex/sites/, data/refs/nasa/); the Horizons cache of the "
               "controls research (results/controls/hzcache/); many dossier notes",
     "on_record_since": "1926 (Schoch); 2006 (NASA canon); 2026-10-03",
     "bears_on": [], "status": "none",
     "reasoning": "Neither held-out predicate involves the Sun's or the Moon's position or the eclipse.",
     "scan_classes": ["D6", "ECL"], "locators": []},
    {"id": "D7",
     "fact": "Every morning of 1250-1115 BC, including Days -40 to +2 of -1177: for Venus, Mercury, "
             "Jupiter and Mars, the rise lead, the Sun's altitude at the body's rising, the signed "
             "elongation, the magnitude, and the body's altitude with the Sun at -6, -9 and -12 deg",
     "source": "results/research-visibility-mornings.npz, written 2026-10-03 19:51 local by "
               "docs/research_visibility_calc.py (arrays V_*, M_*, J_*, A_*, A being Mars)",
     "on_record_since": "2026-10-03 19:51 local (34 minutes before revision 1 froze H3 and H4)",
     "bears_on": ["H3", "H4", "H5"], "status": "constrains",
     "reasoning": "Found by the disclosure scan; revision 8's table did not list it. Mercury's morning "
                  "circumstances on Days 0 and +1 bear on H3's visibility clause, and its signed "
                  "elongation through the days around Day 0 bears on when it passed the Sun, H3's "
                  "conjunction clause; Venus' and Mars' elongations on Days -10 to -4 bear on H4, which "
                  "D1-D2 already settle. The archive may settle H3; whether it does cannot be decided "
                  "without evaluating H3 at the target, which the bench forbids before the second freeze, "
                  "so H3 stays null. With H4 = fail no pass pattern reaches 0.05 either way (Q_record). "
                  "Sealed as a file.",
     "scan_classes": [],
     "locators": [{"path": "results/research-visibility-mornings.npz", "file": True, "found_by": "scan"}]},
    {"id": "D8",
     "fact": "Mercury's events of the spring of -1177 (greatest western and eastern elongations, the "
             "inferior conjunction, the stations, the rise-azimuth extrema, the morning-visibility runs "
             "at three arcus visionis values) and a daily table for 1 Mar to 20 Apr -1177 (elongation, "
             "rise lead, Sun altitude at Mercury's rising, magnitude, altitude at civil dawn, rise "
             "azimuths); with the 1178 BC case values of B&M's criteria",
     "source": "results/research-visibility.json, written 2026-10-03 19:56 local by "
               "docs/research_visibility_calc.py (keys mercury_events.window_1178BC and "
               "bm_rates.case_16Apr1178BC)",
     "on_record_since": "2026-10-03 19:56 local (29 minutes before revision 1 froze H3 and H4)",
     "bears_on": ["H3", "H4", "H5"], "status": "constrains",
     "reasoning": "Found by the disclosure scan; revision 8's table did not list it. The daily table "
                  "runs through Days 0 to +4 and the event list bounds Mercury's apparitions around Day 0, "
                  "so it bears on both clauses of H3. Its D4 subset (station, western elongation, "
                  "rise-azimuth maximum) is public by design; the rest is sealed with the file. It may "
                  "settle H3; H3 stays null for the reason given under D7.",
     "scan_classes": [],
     "locators": [{"path": "results/research-visibility.json", "file": True, "found_by": "scan"}]},
    {"id": "D9",
     "fact": "The Moon's circumstances on the night after Day -5 of 1178 BC (its rising time)",
     "source": "docs/research-textclues.md 5.2 (l. 99, l. 261), 2026-10-03",
     "on_record_since": "2026-10-03 (research-textclues)",
     "bears_on": ["H2"], "status": "none",
     "reasoning": "Bears only on H2, which is not counted because its value at 1178 BC was known before "
                  "its threshold was frozen (DESIGN 7.1).",
     "scan_classes": ["H2"], "locators": []},
    {"id": "D10",
     "fact": "The target's season, star, equinox and conjunction values and B&M's criteria at 1178 BC "
             "(the reproduction values of DESIGN 2.2 and 2.4)",
     "source": "B&M 2008 and Table S2; the dossier notes; DESIGN section 2",
     "on_record_since": "2008; 2026-10-03",
     "bears_on": [], "status": "none",
     "reasoning": "They bear on N, C, V, M and E, which B&M fitted, and on H1 (night length), none of "
                  "which is a counted held-out predicate.",
     "scan_classes": ["OTHER"], "locators": []},
]

REVIEWED = [
    {"path": "docs/research-bm2008.md", "lines": [59],
     "reason": "B&M's abstract: the four references on Days -33, -29, -5 and 0 (D2, D4, D10), no Day-0 "
               "Mercury quantity (structure probe: under the Abstract heading at l. 57)"},
    {"path": "docs/research-bm2008-a.md", "lines": [29],
     "reason": "the same abstract in the first extraction (heading at l. 28)"},
    {"path": "docs/DESIGN-v6.md", "lines": [3383], "reason": "revision 6's D5 row: a description (files, "
                                                              "dates, quantity codes), no value"},
    {"path": "docs/DESIGN-v7.md", "lines": [3694], "reason": "revision 7's D5 row, a description"},
    {"path": "results/design-revision-v8/DESIGN-v8-before-c8.md", "lines": [3868],
     "reason": "revision 8's D5 row before [c8], a description"},
    {"path": "results/design-revision-v6/parts/7_heldout.md", "lines": [56],
     "reason": "revision 6's D5 row as spliced, a description"},
    {"path": "results/design-revision-v6/preserved_sha256.txt", "lines": [24, 25],
     "reason": "hash lines naming D5's files: names, no value"},
]


def planet_list_generic(report):
    """The D3-class hits that are generic predicate text (herald fork, instrument
    rows, the ephem API), reviewed by structure: they sit in design copies or in
    a module-API section and name no target instant."""
    out = []
    for f in report["files"]:
        lines = [h["line"] for h in f["hits"]
                 if D.classify(f["path"], h) == "D3" and h["match"] == "planet-list"]
        if not lines:
            continue
        p = f["path"]
        if p.startswith(("docs/DESIGN-v", "results/design-revision")) or p == "docs/research-ephemeris.md":
            out.append({"path": p, "lines": lines,
                        "reason": "generic predicate or API text naming several planets (the herald fork "
                                  "'Venus, Jupiter, Sirius, or Mars at magnitude -1 or brighter', the "
                                  "instrument rows I6/I15, or ephem's API in research-ephemeris 9); no "
                                  "target value"})
    return out


def scan_summary(report):
    files = []
    for f in report["files"]:
        dates = sorted({d for h in f["hits"] for d in h["dates"]})
        codes = sorted({c for h in f["hits"] for c in h["codes"]})
        cls = Counter(D.classify(f["path"], h) for h in f["hits"])
        files.append({"path": f["path"], "kind": f["kind"], "hits": len(f["hits"]),
                      "lines": [h["line"] for h in f["hits"]],
                      "dates": [dates[0], dates[-1]] if dates else [],
                      "codes": codes, "classes": dict(sorted(cls.items()))})
    return files


def main():
    report = json.loads(SCAN.read_text(encoding="utf-8"))
    reviewed = REVIEWED + planet_list_generic(report)
    sl = D.sealed_list(report, FACTS, public_by_design=("D4",), reviewed=reviewed)
    table = {
        "schema": "odybench heldout_disclosure v1 (DESIGN 7.1, 10.2)",
        "status": "DRAFT by A0 (truth tier), 2026-10-04; to be checked by A9 (DESIGN 7.1, 12.1 item 9)",
        "predicates_frozen": "2026-10-03T20:25-05:00 (revision 1)",
        "target": "16 Apr -1177 (1178 BC), Day 0; the scanned span is 7 Mar to 18 Apr -1177 (Day -40 to Dawn +2)",
        "scan": {
            "tool": "tools/disclosure_scan.py",
            "run": "py tools/disclosure_scan.py --json results/build-A0/disclosure_scan.json",
            "scan_json_sha256": hashlib.sha256(SCAN.read_bytes()).hexdigest(),
            "what_it_prints": "file names, line numbers (or JSON key paths, NPZ array names, PDF pages), "
                              "civil dates and quantity codes; never a value",
            "n_files": len(report["files"]), "n_hits": sum(len(f["hits"]) for f in report["files"]),
            "unscanned": report["unscanned"], "errors": report["errors"],
            "excluded": "ephemeris kernels (*.bsp)",
            "files": scan_summary(report)},
        "facts": FACTS,
        "public_by_design": ["D4"],
        "reviewed_not_sealed": reviewed,
        "sealed_outputs": [],
        "sealed": {k: sl[k] for k in ("files", "lines", "globs", "facts")},
        "determined": {"H3": None, "H4": "fail"},
        "notes": [
            "Q_record and Q_contra read only 'determined' (DESIGN 7.1, 7.2).",
            "D7 and D8 are new in this draft: the scan found them; revision 8's table (D1-D6) did not list "
            "them. Both were on record before the predicates were frozen. They are sealed with D3 and D5.",
            "D3's locators add four places the design's sealed list did not name: research-bm2008-a.md "
            "l. 315 (on the public whitelist, so the export must mask it), the paper's text in "
            "data/bm2008-a/ and data/refs/, and the PDF copies; research-chronology.md l. 64 is sealed "
            "conservatively.",
            "D5's locators add lines of docs/research-ephemeris.md (on the public whitelist), which prints "
            "the Horizons comparison at the D5 instants in its sections 7 and 10; the export must mask them.",
            "docs/research_visibility_calc.py (public whitelist) recomputes D7 and D8 when run as a script "
            "(sections planets, mercury_events, bm_rates, herald). Its functions may be imported, but it "
            "must not be run as a script before prereg-2 (access.json, rules)."],
        "uncovered_check": {"uncovered": sl["uncovered"], "complete": not sl["uncovered"]},
    }
    OUT.write_text(json.dumps(table, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(FACTS)} facts; sealed {len(sl['files'])} files, "
          f"{sum(len(x['lines']) for x in sl['lines'])} lines in {len(sl['lines'])} files, "
          f"{len(sl['globs'])} globs; uncovered {len(sl['uncovered'])}")
    for u in sl["uncovered"]:
        print("  UNCOVERED", u)


if __name__ == "__main__":
    main()
