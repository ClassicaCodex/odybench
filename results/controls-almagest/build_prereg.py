"""
Build data/prereg/controls_almagest.json (clue sets, NO absolute dates) and
data/prereg/controls_almagest_truth.json (true dates, conversions) from
records.py and slack.json.

    cd C:\\Projects\\odybench && py results/controls-almagest/build_prereg.py

The set composition below was fixed from the TEXT ONLY (stated dates, body,
proximity in days, presence of a Venus/Mercury record and of a lunar record)
before slack.json was inspected; slack.json is read here only to copy the UT
instant of each record into the truth file.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(HERE))
import records as RC                    # noqa: E402
from odybench import ephem as E         # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
RC.resolve()
REC = {r["id"]: r for r in RC.R}
SLACK = {}
for o in json.loads((HERE / "slack.json").read_text(encoding="utf-8")):
    SLACK.setdefault(o["id"], {})[o["reading"]] = o
TEXT_FILE = "data/text/ptolemy-syntaxis-grc.tsv"
TEXT = RC.rows()
PRE = RC.PRE


def civil_day(r, month=None, day=None):
    return RC.nab_jd_noon(r["nab"], month or r["month"], day or r["day"]) + RC.civil_day_offset(r["part"])


def tod(r):
    p = r["part"]
    h = r.get("hours") or 0
    if p in ("evening", "morning", "noon"):
        return {"evening": "evening", "morning": "before dawn", "noon": "noon"}[p]
    return {
            "h_before_midnight": f"{h:g} equinoctial hours before midnight",
            "h_after_midnight": f"{h:g} equinoctial hours after midnight",
            "h_after_noon": f"{h:g} equinoctial hours after noon",
            "h_before_noon": f"{h:g} equinoctial hours before noon (after sunrise)", "noon": "noon"}[p]


GE_FORKS_COMMON = [
    {"option": "ge_true_k", "params": {"k_days": [1, 2, 3, 5, 7, 10, 16, 21]},
     "justification": "the words say the planet stood at (or about) its greatest distance from the Sun; read as: the day lies "
                      "within k days of the greatest elongation from the TRUE Sun on that side (k = 1 is B&M's own tolerance)"},
    {"option": "ge_mean_k", "params": {"k_days": [1, 2, 3, 5, 7, 10, 16, 21]},
     "justification": "Ptolemy defines the elongation from the MEAN Sun ('τῆς μέσης τοῦ ἡλίου παρόδου' / his reductions); same test "
                      "against the greatest distance from the mean Sun"},
    {"option": "visible_only", "params": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]},
     "justification": "minimal reading: only that the planet was seen on that side of the Sun (morning or evening) on that day"},
]
MWRA_FORK = {"option": "bm_mwra_k", "params": {"k_days": [1, 2, 3]},
             "justification": "B&M's own operational proxy for a Mercury 'turning point' (DESIGN T0b step 5: local maximum of "
                              "Mercury's rising azimuth). NOT what Ptolemy's words say; included only to measure how B&M's proxy "
                              "fares on an expert greatest-elongation record"}
BMV_FORK = {"option": "bm_venus_lead", "params": {"lead_min": [60, 90, 120]},
            "justification": "B&M's V vocabulary: Venus a morning object rising at least L minutes before the Sun (B&M use 90)"}


def planet_row(r, side_word):
    body = r["body"].capitalize()
    ph = r["phen"]
    star_side = {"E": "eastern (evening)", "W": "western (morning)"}[r["side"]]
    lic = r["phen_words"] + ((" … " + r["side_words"]) if r.get("side_words") else "")
    if r.get("extra_words"):
        lic += " … " + r["extra_words"]
    forks = []
    notes = []
    if ph in ("GE", "nearGE"):
        st = (f"{body} is {'an evening' if r['side'] == 'E' else 'a morning'} star at "
              f"{'about ' if ph == 'nearGE' else ''}its greatest {star_side} elongation on this day ({tod(r)}).")
        forks = [dict(f) for f in GE_FORKS_COMMON]
        if r["body"] == "mercury" and r["side"] == "W":
            forks.append(dict(MWRA_FORK))
        if r["body"] == "venus" and r["side"] == "W":
            forks.append(dict(BMV_FORK))
    elif ph == "GEold":
        st = (f"{body} is {'an evening' if r['side'] == 'E' else 'a morning'} star on this day ({tod(r)}); Ptolemy files the "
              f"record among observations made about the greatest elongations.")
        lic = r["phen_words"] + " … [" + r["ge_claim_ref"] + "] " + r["ge_claim_words"]
        forks = [{"option": "visible_only", "params": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]},
                  "justification": "the record's own words say only morning/evening star (ἑῷος / ἑσπέρας)"}] + \
                [dict(f) for f in GE_FORKS_COMMON[:2]]
        forks[1]["justification"] = ("Ptolemy's classification (words at " + r["ge_claim_ref"] + ") that the old records were "
                                     "made about greatest elongation; read as GE within k days")
        if r["body"] == "mercury" and r["side"] == "W":
            forks.append(dict(MWRA_FORK))
        notes.append("the greatest-elongation status is Ptolemy's classification, not the original record's words")
    elif ph == "beforeGE":
        w = r.get("before_words") or r["phen_words"]
        lic = r["phen_words"] + ((" … " + r["before_words"]) if r.get("before_words") else "")
        st = (f"{body} is {'an evening' if r['side'] == 'E' else 'a morning'} star on this day ({tod(r)}) and has NOT yet reached "
              f"its greatest {star_side} elongation.")
        forks = [{"option": "ge_after_within_j", "params": {"j_days": [7, 15, 30]},
                  "justification": "'not yet at greatest elongation': the next greatest elongation on that side falls 0..j days later"},
                 {"option": "visible_only", "params": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]},
                  "justification": "minimal reading: seen on that side of the Sun"}]
        if r["id"] == "IX.10.6a":
            notes.append("'not yet at greatest elongation' is Ptolemy's inference from the record four days later, not the record's words")
    elif ph == "afterGE":
        st = (f"{body} is {'an evening' if r['side'] == 'E' else 'a morning'} star on this day ({tod(r)}) and is already PAST its "
              f"greatest {star_side} elongation.")
        forks = [{"option": "ge_before_within_j", "params": {"j_days": [7, 15, 30, 60]},
                  "justification": "'after greatest elongation': the last greatest elongation on that side fell 0..j days earlier"},
                 {"option": "visible_only", "params": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]},
                  "justification": "minimal reading"}]
        if r["body"] == "venus" and r["side"] == "W":
            forks.append(dict(BMV_FORK))
    return st, lic, forks, notes


SETS = [
    dict(set="ALM-A", records=["IX.10.3", "X.8.2", "IX.9.4", "XI.2.2"],
         place=dict(value="Alexandria for IX.10.3 and XI.2.2 (stated); unstated for X.8.2 and IX.9.4",
                    words=["ἦν ὁ χρόνος ἐν Ἀλεξανδρείᾳ", "τὴν δʼ ἐν Ἀλεξανδρείᾳ φαινομένην"], refs=["9.10.3", "11.2.2"]),
         descr="Mercury evening star beside a young Moon (Day 0); Mars near opposition beside a near-full Moon; Mercury at "
               "greatest morning elongation; Moon beside Jupiter before sunrise. Four records over about 55 days."),
    dict(set="ALM-B", records=["X.4.3", "XI.6.2", "V.3.2", "VII.2.4"],
         place=dict(value="Alexandria (stated in all four rows)",
                    words=["ἐφαίνετο δʼ ἐν Ἀλεξανδρείᾳ", "ἡ δὲ ἐν Ἀλεξανδρείᾳ φαινομένη", "ἐν Ἀλεξανδρείᾳ", "μέλλοντος μὲν δύνειν ἐν Ἀλεξανδρείᾳ τοῦ ἡλίου"],
                    refs=["10.4.3", "11.6.2", "5.3.2", "7.2.4"]),
         descr="Venus morning star past greatest elongation beside a waning Moon (Day 0); Moon beside Saturn in the evening; "
               "two Sun-Moon elongation measurements (about last and first quarter). Four records over about 70 days."),
    dict(set="ALM-C", records=["IX.8.3", "IV.6.14"],
         place=dict(value="Alexandria for the eclipse (4.6.13 introduces the three eclipses as observed there); unstated for IX.8.3",
                    words=["ἐκ τῶν ἐπιμελέστατα ἡμῖν ἐν Ἀλεξανδρείᾳ τετηρημένων"], refs=["4.6.13"]),
         descr="Mercury morning star about greatest elongation (Day 0) and a partial lunar eclipse some 18 days later."),
    dict(set="ALM-D", records=["IX.7.4", "X.1.3"], place=dict(value="unstated", words=[], refs=[]),
         descr="Mercury at greatest evening elongation (Day 0) and Venus at greatest evening elongation about 35 days later."),
    dict(set="ALM-E", records=["X.3.2b", "III.1.10"], place=dict(value="unstated", words=[], refs=[]),
         descr="Venus at greatest evening elongation (Day 0) and a spring equinox about 33 days later."),
    dict(set="ALM-F", records=["X.2.4", "X.1.6"], place=dict(value="unstated", words=[], refs=[]),
         descr="Two records of Venus 'at greatest evening elongation' about 37 days apart (same apparition)."),
    dict(set="ALM-G", records=["X.3.2a", "IX.7.5"], place=dict(value="unstated", words=[], refs=[]),
         descr="LONG: Venus at greatest morning elongation (Day 0) and Mercury at greatest morning elongation about 106 days later."),
    dict(set="ALM-H", records=["IX.7.9", "IX.7.11", "IX.7.14"],
         place=dict(value="unstated (the calendar a record is dated in is not a place statement)", words=[], refs=[]),
         descr="LONG: three Mercury records relative to stars (morning, then two evenings), about 190 days; one interval is a textual fork."),
    dict(set="ALM-I", records=["IX.10.6a", "IX.10.6b"], place=dict(value="unstated", words=[], refs=[]),
         descr="Mercury morning star against the forehead of Scorpius, and again four days later (interval stated in words)."),
    dict(set="ALM-J", records=["X.9.2", "X.4.6a", "X.4.6b"], place=dict(value="unstated", words=[], refs=[]),
         descr="LONG: Mars occults beta Sco (Day 0); about 270 days later Venus overtakes a Virgo star, and its place 4 days later."),
    dict(set="ALM-K", records=["IX.7.16", "XI.3.2", "IX.7.15"],
         place=dict(value="unstated (the calendar a record is dated in is not a place statement; two of the three records may "
                          "come from a Mesopotamian archive - an inference, not a clue)", words=[], refs=[]),
         descr="LONG (about 8 years): Mercury morning star above beta Sco (Day 0); Jupiter occults delta Cnc; Mercury morning star above alpha Lib."),
    dict(set="ALM-L", records=["X.1.5", "X.2.3", "IX.9.3"], place=dict(value="unstated", words=[], refs=[]),
         descr="LONG (about 1.7 years): three records from one observer's set: Venus at greatest morning elongation twice, then "
               "Mercury at greatest evening elongation 3 5/6 deg east of Regulus."),
]
WINDOW_YEARS = 136   # B&M's own window width (1250-1115 BC); DESIGN.md / research-bm2008.md


def interval_row(sid, n, r, d, d_alt=None, alt_label=None, stated_words=None, stated_ref=None, day0=None):
    lic = ("[Egyptian civil dates at " + day0["ref"] + " and " + r["ref"] + " (regnal or era year, month, day): withheld from "
           "this file because, with any season clue, a wandering-calendar date fixes the absolute year; quoted in full in "
           "controls_almagest_truth.json]")
    if stated_words:
        lic = stated_words + "  " + lic
    forks = []
    if d_alt is not None:
        forks = [{"option": "as_printed", "day_offset": d,
                  "justification": "the Egyptian date as printed in the export"},
                 {"option": "mean_sun_emended", "day_offset": d_alt,
                  "justification": alt_label}]
    return dict(set=sid, clue_id=f"{sid}.{n}", kind="interval",
                statement=(f"Record {r['id']} falls on civil day {d:+d} relative to Day 0 (record {day0['id']}); civil days run "
                           f"midnight to midnight, so an evening observation and the following pre-dawn one belong to consecutive "
                           f"civil days."),
                licence_words=lic, ref=PRE + r["ref"], text_file=TEXT_FILE, fork_options=forks, narrative_level="narrator",
                notes="interval computed by exact Egyptian-calendar arithmetic (365-day year, 30-day months, 5 epagomenal days) "
                      "from the dates the text states; no modern date enters", day_offset=d, record=r["id"])


def star_rows(sid, n0, r, day):
    rows = []
    n = n0
    for s in r.get("stars", []):
        if s["kind"] == "note_only" and r["id"] not in ("X.4.3",):
            continue
        kind = "star"
        tol = {"offset": "the stated offsets in longitude/latitude", "line_east": "the stated distance from the line",
               "heads_line": "the stated position on the line", "conj": "the conjunction/occultation", "nearest": "the stated offset",
               "note_only": "the alignment"}[s["kind"]]
        forks = [{"option": "positional", "params": {"tolerance_deg": [0.25, 0.5, 1.0, 2.0]},
                  "justification": f"{tol} hold within the tolerance (unit conventions in notes)"},
                 {"option": "none", "justification": "B&M-vocabulary-only reading: positional relations to named stars are not used"}]
        notes = s["reading"]
        if s["kind"] == "nearest":
            notes += "; the star is not securely identified, so 'none' is the default"
        rows.append(dict(set=sid, clue_id=f"{sid}.{n}", kind=kind,
                         statement=f"{r['body'].capitalize()} relative to a named star on this day: {s['reading']}.",
                         licence_words=s.get("clue_words", s["words"]), ref=PRE + r["ref"], text_file=TEXT_FILE, fork_options=forks,
                         narrative_level="narrator", notes=notes, day_offset=day, record=r["id"]))
        n += 1
    return rows, n


MOON_TXT = {
    "IX.10.3": ("The Moon stands close to Mercury (Mercury 1 1/6 deg to the east of the Moon's centre) at 4 1/2 equinoctial hours "
                "before midnight, while Mercury is an evening star.",
                "Mercury is an evening star and never more than about 28 deg from the Sun, so a Moon beside it in the evening is a "
                "young crescent a few days after conjunction (my inference)", "young_crescent", "E"),
    "X.4.3": ("Before dawn (4 3/4 equinoctial hours after midnight) the Moon's apparent centre, Venus and beta Sco stand in one line, "
              "Venus just west of the Moon.",
              "Venus is a morning star past greatest elongation, so a Moon beside it before dawn is waning, roughly a crescent "
              "40-50 deg west of the Sun (my inference)", "waning_crescent", "W"),
    "X.8.2": ("At 3 equinoctial hours before midnight the Moon stands close to Mars (Mars 1 3/5 deg to the east of the Moon's centre), "
              "about three days after Mars' opposition.",
              "Mars is about three days from opposition, so a Moon beside it is near full (my inference)", "near_full", None),
    "XI.2.2": ("Before sunrise (about 5 equinoctial hours after midnight) the Moon's centre has the same longitude as Jupiter, the "
               "Moon lying further south.",
               "a Moon seen before sunrise is waning; with the longitudes Ptolemy states in the same sentence (Jupiter's, and the "
               "mean Sun's) it is about 30 deg west of the Sun, an old crescent (inference from the stated numbers)",
               "waning_crescent", "W"),
    "XI.6.2": ("At 4 equinoctial hours before midnight Saturn stands about 1/2 deg to the east of the Moon's centre (and as far "
               "from its northern horn).",
               "a Moon still up at that hour and seen with a 'northern horn' is a crescent; with the Moon's and the mean Sun's "
               "longitudes Ptolemy states in the same sentence it is about 40 deg east of the Sun, a waxing crescent (inference)",
               "waxing_crescent", "E"),
}


def moon_rows(sid, n, r, day):
    st, inf, phase, sgn = MOON_TXT[r["id"]]
    mo = r["moon"]
    forks = [{"option": "phase_class", "params": {"class": phase},
              "justification": inf},
             {"option": "positional", "params": {"tolerance_deg": [0.5, 1.0, 2.0]},
              "justification": "the stated body-Moon offset in longitude holds within the tolerance (topocentric)"},
             {"option": "none", "justification": "the Moon's phase is not stated in words; do not use it"}]
    return [dict(set=sid, clue_id=f"{sid}.{n}", kind="moon-phase", statement=st, licence_words=mo["words"],
                 ref=PRE + r["ref"], text_file=TEXT_FILE, fork_options=forks, narrative_level="narrator",
                 notes=mo["reading"], day_offset=day, record=r["id"])], n + 1


def build():
    import greek
    for S in SETS:                      # place words must be verbatim
        S["place"]["words"] = [greek.exact(TEXT[ref], w) for w, ref in zip(S["place"]["words"], S["place"]["refs"])]
        assert all(S["place"]["words"]), S["set"]
    clues, sets_out, truth_sets = [], [], []
    for S in SETS:
        sid = S["set"]
        recs = [REC[i] for i in S["records"]]
        d0 = recs[0]
        cd0 = civil_day(d0)
        n = 1
        offs = {}
        for r in recs:
            day = civil_day(r) - cd0
            offs[r["id"]] = day
            if r is not d0:
                d_alt = alt_label = None
                if r.get("emend"):
                    d_alt = civil_day(r, r["emend"]["month"], r["emend"]["day"]) - cd0
                    alt_label = ("day implied by the mean-Sun longitude Ptolemy states in the same sentence, under his own solar "
                                 "tables; the printed day numeral conflicts with it (textual crux, details in the truth file)")
                stated = None
                if r["id"] == "IX.10.6b":
                    stated = "μετὰ δ ἡμέρας"
                if r["id"] == "X.4.6b":
                    stated = "μετὰ γὰρ δ ἡμέρας τῆς προκειμένης τηρήσεως"
                clues.append(interval_row(sid, n, r, day, d_alt, alt_label, stated, r["ref"], d0)); n += 1
            b = r["body"]
            if b in ("mercury", "venus") and r["phen"] in ("GE", "nearGE", "GEold", "beforeGE", "afterGE"):
                st, lic, forks, notes = planet_row(r, None)
                clues.append(dict(set=sid, clue_id=f"{sid}.{n}", kind="planet", statement=st, licence_words=lic,
                                  ref=PRE + r["ref"], text_file=TEXT_FILE, fork_options=forks, narrative_level="narrator",
                                  notes="; ".join(notes + ["the text also gives a zodiacal longitude and an elongation in degrees; "
                                                           "they are NOT used (B&M's clue grammar has no coordinates)"]),
                                  day_offset=day, record=r["id"])); n += 1
            elif r["phen"] == "pos" and b in ("mercury", "venus"):
                pass                       # positional only (IX.10.6b, X.4.6b): handled by star rows / below
            if r["id"] == "X.4.6a":
                import greek
                hour = greek.exact(TEXT[r["ref"]], "ὥρᾳ ιβ΄")
                assert hour
                clues.append(dict(set=sid, clue_id=f"{sid}.{n}", kind="planet",
                                  statement="Venus is seen as a morning star at the twelfth (last) hour of the night; Ptolemy adds "
                                            "that it had already passed its greatest morning elongation.",
                                  licence_words=hour + " … ὁ τῆς Ἀφροδίτης ἐφαίνετο … " + r["after_words"],
                                  ref=PRE + r["ref"], text_file=TEXT_FILE,
                                  fork_options=[{"option": "ge_before_within_j", "params": {"j_days": [15, 30, 60]},
                                                 "justification": "Ptolemy's 'παρεληλύθει ... τὴν μεγίστην ἑῴαν ἀπόστασιν' (his inference "
                                                                  "from the record four days later, not the observer's words)"},
                                                {"option": "visible_only", "params": {"min_minutes_between_body_and_sun_horizon_crossings": [30, 60]},
                                                 "justification": "the observer's own words: Venus seen at the last hour of the night"},
                                                dict(BMV_FORK)],
                                  narrative_level="narrator", notes="the 'past greatest elongation' status is Ptolemy's inference",
                                  day_offset=day, record=r["id"])); n += 1
            if r["id"] == "X.8.2":
                clues.append(dict(set=sid, clue_id=f"{sid}.{n}", kind="planet",
                                  statement="Mars was at opposition (to the mean Sun, Ptolemy's 'ἀκρώνυκτος') about three days before this day.",
                                  licence_words=r["phen_words"], ref=PRE + r["ref"], text_file=TEXT_FILE,
                                  fork_options=[{"option": "opp_true_k", "params": {"k_days": [1, 2, 3]},
                                                 "justification": "opposition to the true Sun 3 +- k days earlier"},
                                                {"option": "opp_mean_k", "params": {"k_days": [1, 2, 3]},
                                                 "justification": "opposition to the mean Sun (Ptolemy's definition, 10.7.2) 3 +- k days earlier"},
                                                {"option": "none", "justification": "outer-planet oppositions are not a B&M clue type"}],
                                  narrative_level="narrator", notes="'ἔγγιστα' (about): the three days are approximate in the words",
                                  day_offset=day, record=r["id"])); n += 1
            if r["id"] == "XI.2.2":
                clues.append(dict(set=sid, clue_id=f"{sid}.{n}", kind="planet",
                                  statement="Jupiter is visible before sunrise (a morning object).",
                                  licence_words=r["phen_words"], ref=PRE + r["ref"], text_file=TEXT_FILE,
                                  fork_options=[{"option": "visible_before_sunrise", "params": {"min_altitude_deg": [5]},
                                                 "justification": "the observation was made before sunrise"},
                                                {"option": "none", "justification": "outer planets are not a B&M clue type"}],
                                  narrative_level="narrator", notes="", day_offset=day, record=r["id"])); n += 1
            if r["id"] in ("X.9.2", "XI.3.2"):
                clues.append(dict(set=sid, clue_id=f"{sid}.{n}", kind="planet",
                                  statement=f"{b.capitalize()} is a morning object (ἑῷος) on this day.",
                                  licence_words=r["phen_words"], ref=PRE + r["ref"], text_file=TEXT_FILE,
                                  fork_options=[{"option": "visible_before_sunrise", "params": {"min_altitude_deg": [5]},
                                                 "justification": "'ἑῷος': seen in the morning"}],
                                  narrative_level="narrator", notes="", day_offset=day, record=r["id"])); n += 1
            if r["id"] == "X.4.6b":
                clues.append(dict(set=sid, clue_id=f"{sid}.{n}", kind="planet",
                                  statement="Venus, four days after its conjunction with the star (previous row), stands about 4 2/3 deg "
                                            "further east (difference of the two longitudes Ptolemy gives for the two reports).",
                                  licence_words=r["phen_words"], ref=PRE + r["ref"], text_file=TEXT_FILE,
                                  fork_options=[{"option": "positional", "params": {"tolerance_deg": [0.5, 1.0, 2.0]},
                                                 "justification": "Venus' longitude gain over the four days as Ptolemy converts it"},
                                                {"option": "none", "justification": "Ptolemy's conversion of the observer's report, not the observer's words"}],
                                  narrative_level="narrator", notes="the longitudes are Ptolemy's; only their difference is used",
                                  day_offset=day, record=r["id"])); n += 1
            if r.get("moon"):
                rows, n = moon_rows(sid, n, r, day)
                clues += rows
            if r.get("moonsun"):
                ms = r["moonsun"]
                qual = "last quarter (Moon west of the Sun, seen after sunrise)" if ms["stated"] < 0 else "first quarter (Moon east of the Sun at sunset)"
                st_deg = ((ms["stated"] + 180) % 360) - 180
                clues.append(dict(set=sid, clue_id=f"{sid}.{n}", kind="moon-phase",
                                  statement=f"The apparent Moon is about {abs(st_deg):.0f} deg {'west' if st_deg < 0 else 'east'} of the Sun "
                                            f"({tod(r)}): {qual}.",
                                  licence_words=ms["words"] + (" … " + r["phen_words"] if r["id"] == "V.3.2" else ""),
                                  ref=PRE + r["ref"], text_file=TEXT_FILE,
                                  fork_options=[{"option": "elongation_tol", "params": {"tolerance_deg": [3, 6, 12]},
                                                 "justification": "the measured Sun-Moon distance holds within the tolerance"},
                                                {"option": "phase_class", "params": {"class": "last_quarter" if st_deg < 0 else "first_quarter",
                                                                                     "tolerance_days": [1, 2]},
                                                 "justification": "quarter Moon within the tolerance in days"}],
                                  narrative_level="narrator",
                                  notes=("the licence words also give the Sun's zodiacal longitude, a season statement that is NOT "
                                         "used here (no coordinates in the B&M grammar)"),
                                  day_offset=day, record=r["id"])); n += 1
            if r["phen"] == "ecl":
                clues.append(dict(set=sid, clue_id=f"{sid}.{n}", kind="eclipse-lunar",
                                  statement="A partial lunar eclipse in the night of this day: 1/2 + 1/3 of the diameter eclipsed, "
                                            "from the north; mid-eclipse 1 equinoctial hour before midnight (Ptolemy's computed time).",
                                  licence_words=r["phen_words"] + " … τὸν δὲ μέσον χρόνον ἐπελογισάμεθα γεγονέναι πρὸ α ὥρας ἰσημερινῆς τοῦ μεσονυκτίου",
                                  ref=PRE + r["ref"], text_file=TEXT_FILE,
                                  fork_options=[{"option": "any_visible", "justification": "a lunar eclipse visible that night"},
                                                {"option": "magnitude", "params": {"umbral_mag_range": [[0.7, 0.95], [0.6, 1.0]]},
                                                 "justification": "5/6 of the diameter, from the north"},
                                                {"option": "magnitude_and_time", "params": {"time_tol_h": [1, 2]},
                                                 "justification": "plus the stated mid-eclipse time"}],
                                  narrative_level="narrator", notes="the mid-time is Ptolemy's reduction ('ἐπελογισάμεθα'), not a direct reading",
                                  day_offset=day, record=r["id"])); n += 1
            if r["phen"] == "equinox":
                clues.append(dict(set=sid, clue_id=f"{sid}.{n}", kind="season",
                                  statement="The spring equinox occurred on this day, about 1 equinoctial hour after noon.",
                                  licence_words=r["phen_words"] + " … μετὰ μίαν ὥραν ἔγγιστα τῆς μεσημβρίας",
                                  ref=PRE + r["ref"], text_file=TEXT_FILE,
                                  fork_options=[{"option": "equinox_tol", "params": {"tolerance_days": [0.5, 1, 2]},
                                                 "justification": "true equinox within the tolerance of the stated instant"},
                                                {"option": "spring_broad", "params": {"tolerance_days": [10]},
                                                 "justification": "B&M-like coarse season reading"}],
                                  narrative_level="narrator", notes="observed equinox (3.1.10, 'εὑρίσκομεν')", day_offset=day,
                                  record=r["id"])); n += 1
            srows, n = star_rows(sid, n, r, day)
            clues += srows
        span = max(offs.values())
        sets_out.append(dict(set=sid, description=S["descr"], records=S["records"], day0_record=d0["id"],
                             n_records=len(recs), span_days=span, tight=span <= 75,
                             observer_place=S["place"], window_width_years=WINDOW_YEARS,
                             window_note="width only; the bench places the window without reading the truth file "
                                         "(B&M's own width, so the control is searched at the same look-elsewhere scale)"))
        # ---------- truth
        trs = []
        for r in recs:
            cd = civil_day(r)
            y, m, d, _ = E.julian_from_jd(cd)
            sl = SLACK[r["id"]]["printed"]
            t = dict(record=r["id"], ref=r["ref"], body=r["body"], observer=r["observer"], era=r["era"],
                     date_words=r["date_words"], date_words_nab=r.get("date_words_nab"), time_words=r.get("time_words"),
                     nab_year=r["nab"], egyptian_month=RC.MONTHS[r["month"] - 1], egyptian_day=r["day"], part=r["part"],
                     jd_noon_of_egyptian_day=RC.nab_jd_noon(r["nab"], r["month"], r["day"]),
                     conversion=f"1448638 + 365*({r['nab']}-1) + 30*({r['month']}-1) + ({r['day']}-1) = "
                                f"{RC.nab_jd_noon(r['nab'], r['month'], r['day'])} (noon of the Egyptian day); "
                                f"+{RC.civil_day_offset(r['part'])} for a pre-dawn/after-midnight time",
                     civil_jd_noon=cd, civil_date_julian=f"{y:+05d}-{m:02d}-{d:02d}",
                     civil_date_text=f"{d} {'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[m-1]} "
                                     f"{(str(1 - y) + ' BC') if y <= 0 else ('AD ' + str(y))} (astronomical year {y}), proleptic Julian",
                     day_offset=offs[r["id"]], instant_ut=sl["date"], instant_jd_ut=sl["jd_ut"],
                     instant_note="UT instant of the observation as I reconstruct it (evening/dawn = Sun 8 deg below the horizon; "
                                  "stated hours = local apparent time at the site) - computed by me with slack.py")
            for k in ("nab_note", "date_note"):
                if r.get(k):
                    t[k] = r[k]
            if r.get("emend"):
                em = r["emend"]
                cde = civil_day(r, em["month"], em["day"])
                ye, me, de, _ = E.julian_from_jd(cde)
                t["emended"] = dict(label=em["label"], why=em["why"], civil_jd_noon=cde,
                                    civil_date_julian=f"{ye:+05d}-{me:02d}-{de:02d}", day_offset=cde - cd0,
                                    instant_ut=SLACK[r["id"]]["emended: " + em["label"]]["date"])
            ms, _ = RC.ptolemy_mean_sun(r)
            t["ptolemy_mean_sun_check"] = dict(stated=r.get("ptol_mean_sun"), from_his_tables=round(ms, 3))
            trs.append(t)
        y0, m0, dd0, _ = E.julian_from_jd(cd0)
        truth_sets.append(dict(set=sid, day0_record=d0["id"], day0_civil_jd_noon=cd0,
                               day0_civil_date_julian=f"{y0:+05d}-{m0:02d}-{dd0:02d}",
                               day0_text=f"{dd0} {'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[m0-1]} "
                                         f"{(str(1 - y0) + ' BC') if y0 <= 0 else ('AD ' + str(y0))} (astronomical {y0}), proleptic Julian",
                               records=trs))
    return clues, sets_out, truth_sets


ERA_CHAIN = [
    dict(claim="Nabonassar epoch: Nab 1 Thoth 1 noon = JD 1448638 = 26 Feb 747 BC (astronomical -746), proleptic Julian",
         source="task brief; docs/research-controls.md 4.19; checked: ephem.jd_from_julian(-746, 2, 26) + 0.5 = 1448638.0 (computed by me)"),
    dict(claim="Philip (years from Alexander's death) n = Nab 424 + n", source="3.7.4 'ἀπὸ ... Ναβονασάρου βασιλείας μέχρι τῆς Ἀλεξάνδρου τελευτῆς ἔτη ... υκδ'; 10.9.2 Philip 52 = Nab 476"),
    dict(claim="Hadrian n = Nab 863 + n", source="3.7.4: Alexander's death to Augustus 294 years (numeral damaged 'σ??δ'), Augustus 1 Thoth 1 noon to Hadrian 17 Athyr 7 = 161 years 66 days, so Hadrian 17 = Nab 424+294+1+161 = 880; also docs/research-controls.md 4.19 (three Hadrianic eclipses match NASA rows)"),
    dict(claim="Antoninus n = Nab 884 + n", source="9.10.3 'τῷ βʹ ἔτει Ἀντωνίνου, ὅ ἦν κατὰ τὸ ωπϚʹ ἔτος ἀπὸ Ναβονασσάρου'; 10.4.6 'μέχρι τῆς Ἀντωνίνου βασιλείας ωπδ΄'; 3.1.9 Antoninus 3 = Philip 463 = Nab 887"),
    dict(claim="Philadelphus 13 = Nab 476", source="10.4.6 'τὸ μὲν τῆς τηρήσεως ἔτος υος΄ ἐστὶν ἀπὸ Ναβονασσάρου'"),
    dict(claim="Dionysian and Chaldean dates: Ptolemy's own Egyptian equivalents are used (quoted per record as date_words_nab)", source="9.7.9-16, 9.10.6, 10.9.2, 11.3.2, 11.7.2"),
    dict(claim="Check: Ptolemy's stated mean Sun for each record is reproduced by his own solar tables (epoch Pisces 0;45 at Nab 1 Thoth 1 noon, 3.7.4; daily motion 0;59,8,17,13,12,31) to <= 0.12 deg for 28 of 30 statements; the two failures are textual cruxes (IX.7.11, IX.9.4) and both readings are carried",
         source="computed by me with results/controls-almagest/records.py"),
]


PRIMARY = ["as_printed", "ge_true_k", "ge_after_within_j", "ge_before_within_j", "phase_class", "elongation_tol",
           "positional", "magnitude", "equinox_tol", "opp_mean_k", "visible_before_sunrise", "visible_only"]
PRIMARY_GEOLD = "visible_only"      # an old record's own words say only morning/evening star


def finish(clues, sets_out):
    """Schema alignment with controls_real.json: 'operational' parameters and exactly one 'primary' option per fork list."""
    for c in clues:
        fo = c["fork_options"]
        for o in fo:
            if "params" in o:
                o["operational"] = o.pop("params")
            if "day_offset" in o:
                o["operational"] = {"day_offset": o.pop("day_offset")}
        if not fo:
            continue
        names = [o["option"] for o in fo]
        rec = REC[c["record"]]
        if c["kind"] == "planet" and rec["phen"] == "GEold":
            pick = PRIMARY_GEOLD
        else:
            pick = next((p for p in PRIMARY if p in names), names[0])
        for o in fo:
            o["primary"] = (o["option"] == pick)
    for s in sets_out:
        p = s["observer_place"]
        if p["value"].startswith("Alexandria"):
            p["search_coordinates"] = {"lat": RC.ALEXANDRIA[0], "lon": RC.ALEXANDRIA[1]}
            p["coordinates_source"] = "modern approximate placement written by the drafter; the text gives only the name"
        else:
            p["search_coordinates"] = None
            p["coordinates_source"] = ("no site in the words: horizon-dependent options (visible_only, bm_venus_lead, bm_mwra_k, "
                                       "visible_before_sunrise) need one; the harness uses its default site and reports it")
        s["anchor_record"] = s.pop("day0_record")
        s["window_note"] = ("width only. The harness, not the searcher, places the window so that the anchor record's accepted "
                            "date falls at a uniformly random position inside it (as controls_real.json and DESIGN 4.2 step 3); "
                            "136 years is B&M's own width")


def main():
    clues, sets_out, truth_sets = build()
    finish(clues, sets_out)
    out = ROOT / "data" / "prereg"
    out.mkdir(parents=True, exist_ok=True)
    clue_doc = dict(
        file="controls_almagest.json",
        purpose=("Positive control of B&M's own clue types (critique-design.md issue 3): real, independently dated Almagest "
                 "records of Mercury/Venus elongation status, planet-star relations, lunar phase, a lunar eclipse and an "
                 "equinox, grouped into sets with the day intervals the text's own dates give. Searcher input. Contains NO "
                 "absolute dates, regnal/era years, Egyptian months/days or observer names."),
        written="2026-10-04, by the controls-almagest task (results/controls-almagest/build_prereg.py)",
        conventions=dict(
            day_offset="integer civil days (local midnight to midnight) after Day 0 (the set's anchor record). An evening observation "
                       "and the next pre-dawn observation are consecutive civil days. A row's day_offset is the as-printed value; "
                       "where the record's interval row carries a fork (a textual crux), that fork governs all rows of the record.",
            fork_fields="each option has 'operational' (machine-readable parameters; list values are enumerated) and 'primary' "
                        "(exactly one per row: the drafter's preferred reading)",
            time_of_day="as the words give it; 'equinoctial hours' are on Ptolemy's local apparent clock",
            units="1 'moon' (σελήνη) is read as 0.5 deg; a full-moon diameter (σελήνη διχόμηνος) 0.5 deg; a Pleiad length "
                  "1.5 deg (Ptolemy's own value, 10.1.3); a finger (δάκτυλος) 1/12 deg; a cubit (πῆχυς) about 2 deg (my glosses)",
            forks="every row's fork_options must be enumerated by the searcher; 'none' drops the row",
            licence_words="exact substrings of the row at `ref` in text_file ('…' marks an omission); interval rows withhold the "
                          "date words (see each row)"),
        rules_applied=["no feature the words do not state is a clue: phases inferred from proximity are forks with a 'none' option",
                       "zodiacal longitudes and elongation magnitudes stated by Ptolemy are not used (B&M grammar has no coordinates)",
                       "intervals come only from the dates the text states (Egyptian calendar arithmetic) or from interval words "
                       "('μετὰ δ ἡμέρας')",
                       "no similes or lying tales occur in these passages; all rows are narrator (Ptolemy reporting observations)",
                       "set composition fixed from the text (dates, bodies, proximity) before the DE441 comparison was looked at"],
        sets=sets_out, clues=clues)
    (out / "controls_almagest.json").write_text(json.dumps(clue_doc, ensure_ascii=False, indent=1), encoding="utf-8")
    truth = dict(
        file="controls_almagest_truth.json",
        warning="TRUTH FILE: the searcher must never read this file.",
        written="2026-10-04, by the controls-almagest task (results/controls-almagest/build_prereg.py)",
        calendar="Egyptian civil (wandering) calendar: 12 x 30 days + 5 epagomenal, no leap day. Civil dates below are proleptic "
                 "Julian with astronomical years. No Python datetime was used: JD arithmetic via odybench.ephem.julian_from_jd.",
        era_chain=ERA_CHAIN, sets=truth_sets)
    (out / "controls_almagest_truth.json").write_text(json.dumps(truth, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(sets_out)} sets, {len(clues)} clue rows")
    for s, t in zip(sets_out, truth_sets):
        print(s["set"], s["records"], "span", s["span_days"], "| Day0", t["day0_text"],
              "| offsets", [(x["record"], x["day_offset"], x.get("emended", {}).get("day_offset")) for x in t["records"]])
    # leak check: no era names / months / years in the clue file
    txt = (out / "controls_almagest.json").read_text(encoding="utf-8")
    bad = [w for w in ("Ἀδριαν", "Ἀντωνίν", "Ναβονασ", "Διονύσ", "Χαλδαί", "Φιλαδέλφ", "Ἀλεξάνδρου τελευτ", "Θέων", "Τιμόχαρ",
                       "Τμόχαρ", "Ἵππαρχ", "Thoth", "Phaophi", "Athyr", "Choiak", "Tybi", "Mecheir", "Phamenoth", "Pharmouthi",
                       "Pachon", "Payni", "Epiphi", "Mesore", " BC", "AD 1", "Hadrian", "Antoninus",
                       "Θὼθ", "Φαωφ", "Ἀθὺρ", "Χοι", "Τυβ", "Μεχ", "Φαμεν", "Φαρμουθ", "Παχ", "Παϋν", "Ἐπιφ", "Μεσορ",
                       "Theon", "Timocharis", "Hipparchus", "Nab ", "Dionysian", "Chaldean", "Philip",
                       "Ὑδρῶν", "Ταυρῶν", "Διδυμῶν", "Λεοντῶν", "Σκορπιῶν", "Αἴγων", "Παρθενῶν", "Δίου", "Ἀπελλαί", "Ξανθικ",
                       "κατʼ Αἰγυπτίους") if w in txt]
    print("leak check (strings that must not occur in the clue file):", bad or "none")


if __name__ == "__main__":
    main()
