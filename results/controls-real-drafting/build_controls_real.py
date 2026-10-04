"""Build data/prereg/controls_real.json (the real-record positive controls
and the Livy hard case) from the local ancient texts only.

Every licence-word string below is looked up in the named row of the named
data/text/*.tsv file; the build fails if it is not there. The lookup maps a
few look-alike characters (apostrophes, numeral signs) one-for-one before
searching and then copies the exact substring out of the file, so the JSON
always carries the file's own characters.

This script must not read, and does not read, any truth file.

    cd C:\\Projects\\odybench && py results/controls-real-drafting/build_controls_real.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT = ROOT / "data" / "text"
OUT = ROOT / "data" / "prereg" / "controls_real.json"

# ---------------------------------------------------------------- text access
_rows = {}


def _cit(ref):
    m = re.match(r"urn:cts:[^:]+:[^.]+\.[^.]+\.[^.]+\.(.*)$", ref)
    return m.group(1) if m else ref


def rows(stem):
    if stem not in _rows:
        d = {}
        for line in (TEXT / (stem + ".tsv")).read_text(encoding="utf-8").splitlines():
            ref, _, text = line.partition("\t")
            d[_cit(ref)] = (ref, text)
        _rows[stem] = d
    return _rows[stem]


_FOLD = str.maketrans({"\u02bc": "'", "\u2019": "'", "\u1fbd": "'", "\u0027": "'",
                       "\u02b9": "'", "\u0384": "'", "\u0374": "'", "\u00b4": "'",
                       "\u03c2": "\u03c3"})


def lic(stem, cit, *words):
    """Return (text_file, full_ref, [exact substrings]) after checking them."""
    ref, text = rows(stem)[cit]
    folded = text.translate(_FOLD)
    out = []
    for w in words:
        i = folded.find(w.translate(_FOLD))
        if i < 0:
            raise SystemExit(f"licence words not found in {stem} {cit}: {w!r}")
        out.append(text[i:i + len(w)])
    return ("data/text/" + stem + ".tsv", ref, out)


# ------------------------------------------------------------------ builders
def fork(option, reading, justification, operational=None, primary=False):
    d = {"option": option, "reading": reading, "justification": justification}
    if operational is not None:
        d["operational"] = operational
    d["primary"] = primary
    return d


def clue(set_id, clue_id, event, kind, feature, statement, sources, level,
         forks=(), notes=""):
    files, refs, words = [], [], []
    for (f, r, ws) in sources:
        for w in ws:
            files.append(f)
            refs.append(r)
            words.append(w)
    prim = [f["option"] for f in forks if f["primary"]]
    if forks and len(prim) != 1:
        raise SystemExit(f"{clue_id}: forks need exactly one primary option, got {prim}")
    return {"set": set_id, "clue_id": clue_id, "event": event, "kind": kind,
            "feature": feature, "statement": statement,
            "licence_words": words, "ref": refs, "text_file": files,
            "fork_options": list(forks), "narrative_level": level, "notes": notes}


def place(events, name, sources, coords, coord_note):
    files, refs, words = [], [], []
    for (f, r, ws) in sources:
        for w in ws:
            files.append(f); refs.append(r); words.append(w)
    return {"events": events, "place": name, "licence_words": words, "ref": refs,
            "text_file": files, "search_coordinates": coords,
            "coordinates_source": coord_note}


def unstated(events, note):
    return {"events": events, "place": "unstated", "licence_words": [], "ref": [],
            "text_file": [], "search_coordinates": None, "coordinates_source": note}


COORD_NOTE = ("modern approximate placement written by the drafter from general "
              "geographic knowledge; the text gives only the name")

# generic option sets reused below -------------------------------------------
ATHENS = {"lat": 37.97, "lon": 23.72}
SYRACUSE = {"lat": 37.07, "lon": 15.29}
AEGEAN_BOX = {"lat": [35.0, 41.5], "lon": [19.5, 28.5]}
ITALY_BOX = {"lat": [36.6, 44.0], "lon": [8.0, 18.6]}
SICILY_BOX = {"lat": [36.6, 38.3], "lon": [12.4, 15.7]}


def season_none(just="the passage gives no season in its own words", primary=False):
    return fork("none", "no season constraint", just, {"season": None}, primary)


def site_forks(primary_point_name, point, point_just, box, box_just, primary="box"):
    return [
        fork("point", f"observer at {primary_point_name}", point_just,
             {"site": point}, primary == "point"),
        fork("box", "observer anywhere inside the box; the clue holds if it holds at "
             "some site in the box", box_just, {"site_box": box}, primary == "box"),
        fork("none", "no site: the eclipse need only satisfy the other clues somewhere "
             "on Earth", "the text names no observing place", {"site": None},
             primary == "none"),
    ]


sets = []

# =========================================================================== #
# R-PTOL-BAB : Almagest IV.6, the three Babylonian lunar eclipses            #
# =========================================================================== #
S = "R-PTOL-BAB"
P = "ptolemy-syntaxis-grc"
c = []
src_place = lic(P, "4.6.3", "ἐκ τῶν ἐν Βαβυλῶνι τετηρημένων")
EG_NOTE = ("Egyptian civil calendar: 12 months of 30 days (Thoth=1, Phaophi=2, Athyr=3, "
           "Choiak=4, Tybi=5, Mechir=6, Phamenoth=7, Pharmouthi=8, Pachon=9, Payni=10, "
           "Epiphi=11, Mesore=12) plus 5 epagomenal days, no leap day. "
           "'D into D+1' (D εἰς τὴν D+1) is the night between civil days D and D+1. "
           "night_index = 365*(Y-1) + 30*(M-1) + D. JD of local midnight of that night = "
           "J_free + night_index, J_free an unknown integer: the epoch of the regnal "
           "count in Julian terms is NOT in the text, and the 365-day year wanders "
           "against the seasons, so the dates fix intervals only.")
c.append(clue(S, "PB-CAL", ["E1", "E2", "E3"], "other", "calendar-date",
    "Mid-eclipse nights in Ptolemy's Egyptian reckoning by regnal years of "
    "Mardokempados: E1 = year 1 Thoth 29 into 30; E2 = year 2 Thoth 18 into 19; "
    "E3 = year 2 Phamenoth 15 into 16. night_index: E1 = 29, E2 = 383, E3 = 560. "
    "One free integer J_free (shared by E1-E3) maps night_index to Julian Day; it is "
    "not constrained by anything in the text.",
    [lic(P, "4.6.3", "τῷ πρώτῳ ἔτει Μαρδοκεμπάδου κατʼ Αἰγυπτίους Θὼθ κθʹ εἰς τὴν λ΄"),
     lic(P, "4.6.4", "τῷ δευτέρῳ ἔτει τοῦ αὐτοῦ Μαρδοκεμπάδου κατʼ Αἰγυπτίους Θὼθ ιη΄ εἰς τὴν ιθ΄"),
     lic(P, "4.6.5", "τῷ αὐτῷ δευτέρῳ ἔτει τοῦ Μαρδοκεμπάδου κατʼ Αἰγυπτίους Φαμενὼθ ιεʹ εἰς τὴν ιϛ΄")],
    "narrator (Ptolemy, dating the Babylonian records in his own calendar)",
    [], EG_NOTE + " The night differences E2-E1 = 354 and E3-E2 = 177 are what Ptolemy "
    "himself states in IV.6.6 (clues PB-INT-12, PB-INT-23); this row and those rows "
    "carry the same information and a searcher uses one or the other, not both."))
c.append(clue(S, "PB-INT-12", ["E1", "E2"], "interval", "day-interval",
    "From E1 to E2: 354 days and 2 1/2 equinoctial hours (apparent), 2 1/2 + 1/15 h in "
    "mean days, mid-eclipse to mid-eclipse.",
    [lic(P, "4.6.6", "ἡμέρας περιέχει τνδ καὶ ὥρας ἰσημερινὰς ἁπλῶς μὲν οὕτως θεωροῦσιν δύο ἥμισυ")],
    "narrator (Ptolemy)",
    [fork("calendar-exact", "E2 falls on the night exactly 354 civil nights after E1's "
          "night (whole-night count)", "the day count is calendar arithmetic on two "
          "dates the record gives; it does not depend on Ptolemy's hour reductions",
          {"delta_nights": 354}, True),
     fork("ptolemy-hours", "mid-eclipse E2 - mid-eclipse E1 = 354 d 2.5 h +/- 1 h",
          "uses Ptolemy's reduced hours as well (see PB-E1-TIME, PB-E2-TIME)",
          {"delta_days": 354.104, "tol_hours": 1.0}),
     fork("none", "E1 and E2 treated as unlinked", "sensitivity: drops the interval",
          {"delta_nights": None})],
    "Redundant with PB-CAL."))
c.append(clue(S, "PB-INT-23", ["E2", "E3"], "interval", "day-interval",
    "From E2 to E3: 176 days and 20 1/2 equinoctial hours (apparent), 20 1/5 h in mean "
    "days; equivalently the night of E3 is 177 civil nights after the night of E2.",
    [lic(P, "4.6.6", "ἡμέρας ρος καὶ ὥρας ἰσημερινὰς ἀπλῶς μὲν πάλιν κ U+2220΄")],
    "narrator (Ptolemy)",
    [fork("calendar-exact", "E3 falls on the night exactly 177 civil nights after E2's night",
          "calendar arithmetic on the recorded dates", {"delta_nights": 177}, True),
     fork("ptolemy-hours", "mid-eclipse E3 - mid-eclipse E2 = 176 d 20.5 h +/- 1 h",
          "uses Ptolemy's reduced hours", {"delta_days": 176.854, "tol_hours": 1.0}),
     fork("none", "E2 and E3 treated as unlinked", "sensitivity", {"delta_nights": None})],
    "Redundant with PB-CAL. The local text prints the half-sign of Heiberg's edition as the "
    "literal string 'U+2220' (an export artefact); κ U+2220΄ is 20 1/2."))
# E1
c.append(clue(S, "PB-E1-MAG", "E1", "eclipse-lunar", "magnitude",
    "E1 is a lunar eclipse seen from Babylon and was total: umbral magnitude >= 1.0.",
    [lic(P, "4.6.3", "καὶ ἐξέλειπεν ὅλη")],
    "narrator (Ptolemy quoting the Babylonian record: φησίν)", [],
    "Ptolemy also says 'ἐπειδήπερ τελεία ἦν ἡ ἔκλειψις' in the same row."))
c.append(clue(S, "PB-E1-TIME", "E1", "time-of-day", "eclipse-timing",
    "Timing of E1 at Babylon. The record: it began to be eclipsed after the rising, "
    "a full hour having passed. Ptolemy's reduction: night of 12 equinoctial hours, "
    "first contact 4 1/2 h and mid-eclipse 2 1/2 h before local midnight at Babylon "
    "(3 1/3 h before midnight at Alexandria, using his 5/6 h longitude difference).",
    [lic(P, "4.6.3", "ἤρξατο δέ, φησίν, ἐκλείπειν μετὰ τὴν ἀνατολὴν μιᾶς ὥρας ἱκανῶς παρελθούσης",
         "ὁ δὲ μέσος χρόνος, ἐπειδήπερ τελεία ἦν ἡ ἔκλειψις, πρὸ β U+2220΄ ὡρῶν")],
    "record: narrator quoting the Babylonian report; reduction: narrator (Ptolemy's inference)",
    [fork("record", "first umbral contact between 1.0 and 2.0 equinoctial hours after "
          "moonrise at Babylon", "'μιᾶς ὥρας ἱκανῶς παρελθούσης' = one hour well "
          "passed; the upper bound of 2 h is the drafter's reading of ἱκανῶς; "
          "ἀνατολή read as the Moon's rising, as Ptolemy reads it",
          {"first_contact_after_moonrise_h": [1.0, 2.0], "site": "Babylon"}, True),
     fork("reduction", "mid-eclipse 2.5 equinoctial hours before local apparent "
          "midnight (LAT) at Babylon, +/- 1 h", "Ptolemy's own reduction in the "
          "text; the 1 h tolerance is the drafter's allowance for his assumed 12 h night",
          {"mid_minus_midnight_LAT_h": -2.5, "tol_h": 1.0, "site": "Babylon"}),
     fork("none", "no timing constraint beyond the Moon being above the horizon "
          "during totality at Babylon", "sensitivity", {"timing": None})]))
c.append(clue(S, "PB-E1-SUN", "E1", "season", "solar-longitude",
    "Ptolemy computes the Sun at mid-eclipse E1 at Pisces 24 1/2 deg, i.e. tropical "
    "longitude 354.5 deg ('about the end of Pisces'; night of about 12 equinoctial hours).",
    [lic(P, "4.6.3", "ὁ ἥλιος περὶ τὰ ἔσχατα τῶν Ἰχθύων ἦν",
         "ἐπεῖχεν ἀκριβῶς τῶν Ἰχθύων μοίρας κδ U+2220΄ ἔγγιστα")],
    "narrator (Ptolemy's computation from his own solar tables: κατὰ τοὺς ἐκτεθειμένους ἡμῖν ἐπιλογισμούς)",
    [fork("pm5", "tropical solar longitude 354.5 +/- 5 deg at mid-eclipse",
          "the value is computed from Ptolemy's solar theory, not observed; the drafter "
          "allows 5 deg for the drift of a tables-derived longitude carried back about "
          "nine centuries (general knowledge that Ptolemy's year is a few minutes too "
          "long; not a figure taken from any control answer)",
          {"sun_lon_deg": 354.5, "tol_deg": 5.0}, True),
     fork("pm15", "354.5 +/- 15 deg (season only: late winter)",
          "looser: uses only 'about the end of Pisces'", {"sun_lon_deg": 354.5, "tol_deg": 15.0}),
     fork("none", "solar longitude not used", "the value is a derived quantity",
          {"sun_lon_deg": None})],
    "Ptolemy also gives the night as about 12 equinoctial hours ('ἡ νὺξ ὡρῶν ἰσημερινῶν "
    "ιβ ἔγγιστα'), which follows from the same computed longitude and adds nothing; "
    "the Babylonian record quoted in the row gives no season of its own."))
# E2
c.append(clue(S, "PB-E2-MAG", "E2", "eclipse-lunar", "magnitude",
    "E2 is a partial lunar eclipse of 3 digits (1 digit = 1/12 of the lunar diameter): "
    "umbral magnitude about 0.25.",
    [lic(P, "4.6.4", "ἐξέλειπε δέ, φησίν, ἀπὸ νότου δακτύλους γ")],
    "narrator quoting the Babylonian record (φησίν)",
    [fork("pm0.10", "umbral magnitude 0.25 +/- 0.10", "3 digits as stated, with a "
          "tolerance of about one digit", {"umag": [0.15, 0.35]}, True),
     fork("pm0.20", "umbral magnitude 0.25 +/- 0.20", "looser", {"umag": [0.05, 0.45]}),
     fork("partial", "any partial umbral eclipse, 0 < umag < 1", "uses 'partial' only",
          {"umag": [0.0, 1.0]})],
    "The digit as 1/12 of the diameter is the drafter's convention (general "
    "knowledge of Greek and Babylonian eclipse reports), not stated in this row."))
c.append(clue(S, "PB-E2-DIR", "E2", "eclipse-lunar", "direction",
    "E2 was eclipsed 'from the south': the southern part of the disk was darkened, so "
    "the Moon passed north of the shadow axis (ecliptic latitude of the Moon > 0 at "
    "mid-eclipse).",
    [lic(P, "4.6.4", "ἀπὸ νότου")], "narrator quoting the record",
    [fork("north-of-axis", "Moon's ecliptic latitude > 0 at mid-eclipse",
          "the darkened limb faces the shadow centre, which lies on the ecliptic",
          {"moon_lat_sign": 1}, True),
     fork("none", "direction not used", "the direction words could describe where "
          "the darkening began rather than which side was covered", {"moon_lat_sign": None})]))
c.append(clue(S, "PB-E2-TIME", "E2", "time-of-day", "eclipse-timing",
    "The record: 3 digits eclipsed at midnight itself. Ptolemy: mid-eclipse at local "
    "midnight at Babylon (5/6 h before midnight at Alexandria).",
    [lic(P, "4.6.4", "αὐτοῦ τοῦ μεσονυκτίου",
         "ἐπεὶ οὖν ὁ μέσος χρόνος ἐν Βαβυλῶνι φαίνεται γεγονὼς κατʼ αὐτὸ τὸ μεσονύκτιον")],
    "narrator quoting the record; reduction by Ptolemy",
    [fork("mid-at-midnight", "mid-eclipse within +/- 1 h of local apparent midnight "
          "(LAT) at Babylon", "Ptolemy's reading of the record",
          {"mid_minus_midnight_LAT_h": 0.0, "tol_h": 1.0, "site": "Babylon"}, True),
     fork("in-progress", "the umbral eclipse is in progress at local apparent "
          "midnight at Babylon", "the record says only that it was eclipsed at midnight",
          {"umbral_phase_contains_LAT_h": 0.0, "site": "Babylon"}),
     fork("none", "no timing constraint beyond visibility from Babylon", "sensitivity",
          {"timing": None})]))
c.append(clue(S, "PB-E2-SUN", "E2", "season", "solar-longitude",
    "Ptolemy computes the Sun at Pisces 13 3/4 deg: tropical longitude 343.75 deg.",
    [lic(P, "4.6.4", "τῶν Ἰχθύων μοίρας ιγ U+2220΄ δ΄")],
    "narrator (Ptolemy's computation)",
    [fork("pm5", "343.75 +/- 5 deg", "as PB-E1-SUN", {"sun_lon_deg": 343.75, "tol_deg": 5.0}, True),
     fork("pm15", "343.75 +/- 15 deg", "as PB-E1-SUN", {"sun_lon_deg": 343.75, "tol_deg": 15.0}),
     fork("none", "not used", "derived quantity", {"sun_lon_deg": None})],
    "ιγ U+2220΄ δ΄ = 13 + 1/2 + 1/4."))
# E3
c.append(clue(S, "PB-E3-MAG", "E3", "eclipse-lunar", "magnitude",
    "E3: more than half the diameter eclipsed, from the north; not said to be total.",
    [lic(P, "4.6.5", "ἐξέλειπεν ἀπʼ ἄρκτων πλεῖον τοῦ ἡμίσους")],
    "narrator quoting the Babylonian record (φησίν)",
    [fork("partial-gt-half", "0.5 < umbral magnitude < 1.0", "'more than half' and not "
          "'whole' as for E1 in the same record", {"umag": [0.5, 1.0]}, True),
     fork("gt-half", "umbral magnitude > 0.5 (totality allowed)", "reads 'more than half' "
          "as a lower bound only", {"umag": [0.5, None]}),
     fork("loose", "umbral magnitude > 0.4", "allows a rounded report", {"umag": [0.4, None]})]))
c.append(clue(S, "PB-E3-DIR", "E3", "eclipse-lunar", "direction",
    "E3 eclipsed 'from the north': Moon south of the shadow axis (ecliptic latitude < 0).",
    [lic(P, "4.6.5", "ἀπʼ ἄρκτων")], "narrator quoting the record",
    [fork("south-of-axis", "Moon's ecliptic latitude < 0 at mid-eclipse", "as PB-E2-DIR",
          {"moon_lat_sign": -1}, True),
     fork("none", "direction not used", "as PB-E2-DIR", {"moon_lat_sign": None})]))
c.append(clue(S, "PB-E3-TIME", "E3", "time-of-day", "eclipse-timing",
    "The record: it began to be eclipsed after the rising. Ptolemy: night of 11 "
    "equinoctial hours, first contact about 5 h and mid-eclipse 3 1/2 h before local "
    "midnight at Babylon, assuming a 3-hour eclipse.",
    [lic(P, "4.6.5", "ἤρξατο δέ, φησίν, ἐκλείπειν μετὰ τὴν ἀνατολὴν",
         "ὁ δὲ μέσος χρόνος πρὸ γ U+2220΄ ὡρῶν")],
    "record: narrator quoting the report; reduction: Ptolemy's inference",
    [fork("record", "first umbral contact after moonrise at Babylon, Moon above the "
          "horizon at first contact", "'μετὰ τὴν ἀνατολήν' gives a lower bound only",
          {"first_contact_after_moonrise_h": [0.0, None], "site": "Babylon"}, True),
     fork("record-soon", "first umbral contact within 0 to 1 h after moonrise at Babylon",
          "reads 'after the rising' as 'soon after', as Ptolemy's 1/2 h does",
          {"first_contact_after_moonrise_h": [0.0, 1.0], "site": "Babylon"}),
     fork("reduction", "mid-eclipse 3.5 h before local apparent midnight at Babylon +/- 1 h",
          "Ptolemy's reduction (assumes a 3 h duration)",
          {"mid_minus_midnight_LAT_h": -3.5, "tol_h": 1.0, "site": "Babylon"}),
     fork("none", "no timing constraint beyond visibility", "sensitivity", {"timing": None})]))
c.append(clue(S, "PB-E3-SUN", "E3", "season", "solar-longitude",
    "Ptolemy computes the Sun at Virgo 3 1/4 deg ('about the beginning of Virgo'): "
    "tropical longitude 153.25 deg.",
    [lic(P, "4.6.5", "ὁ ἥλιος περὶ τὴν ἀρχὴν ἦν τῆς Παρθένου", "τῆς Παρθένου μοίρας γ δ΄ ἔγγιστα")],
    "narrator (Ptolemy's computation)",
    [fork("pm5", "153.25 +/- 5 deg", "as PB-E1-SUN", {"sun_lon_deg": 153.25, "tol_deg": 5.0}, True),
     fork("pm15", "153.25 +/- 15 deg", "as PB-E1-SUN", {"sun_lon_deg": 153.25, "tol_deg": 15.0}),
     fork("none", "not used", "derived quantity", {"sun_lon_deg": None})],
    "Ptolemy's night of about 11 hours at Babylon ('τὸ μὲν τῆς νυκτὸς μέγεθος ἐν "
    "Βαβυλῶνι ια ἔγγιστα') follows from the same computed longitude."))
sets.append({
    "set_id": S, "role": "positive control (pass/fail)",
    "texts": [{"text_file": "data/text/ptolemy-syntaxis-grc.tsv",
               "local_keys": ["4.6.3", "4.6.4", "4.6.5", "4.6.6"],
               "citation": "Ptolemy, Almagest (Syntaxis) IV.6, Heiberg's text"}],
    "events": [{"event_id": "E1", "kind": "eclipse-lunar", "ref": "4.6.3"},
               {"event_id": "E2", "kind": "eclipse-lunar", "ref": "4.6.4"},
               {"event_id": "E3", "kind": "eclipse-lunar", "ref": "4.6.5"}],
    "observer_place": [place(["E1", "E2", "E3"], "Babylon", [src_place],
                             {"lat": 32.54, "lon": 44.42}, COORD_NOTE)],
    "window_years": 136, "anchor_event": "E1",
    "clues": c})

# =========================================================================== #
# R-PTOL-ALEX : Almagest IV.6, Ptolemy's three Alexandrian eclipses          #
# =========================================================================== #
S = "R-PTOL-ALEX"
c = []
src_alex = lic(P, "4.6.13", "ἐκ τῶν ἐπιμελέστατα ἡμῖν ἐν Ἀλεξανδρείᾳ τετηρημένων")
c.append(clue(S, "PA-CAL", ["H1", "H2", "H3"], "other", "calendar-date",
    "Mid-eclipse nights in the Egyptian calendar by regnal years of Hadrian: H1 = year 17 "
    "Payni 20 into 21; H2 = year 19 Choiak 2 into 3; H3 = year 20 Pharmouthi 19 into 20. "
    "night_index: H1 = 6130, H2 = 6662, H3 = 7164 (formula in notes). One free integer "
    "J_free (shared by H1-H3) maps to Julian Day.",
    [lic(P, "4.6.13", "τῷ ιζʹ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Παϋνὶ κʹ εἰς τὴν καʹ"),
     lic(P, "4.6.14", "τῷ ιθʹ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Χοϊὰκ βʹ εἰς τὴν γʹ"),
     lic(P, "4.6.15", "τῷ κʹ ἔτει Αδριανοῦ κατʼ Αἰγυπτίους Φαρμουθὶ ιθʹ εἰς τὴν κʹ")],
    "narrator (Ptolemy, his own observations)", [],
    EG_NOTE + " Differences: H2-H1 = 532 nights, H3-H2 = 502 nights, matching IV.6.16 "
    "(1 Egyptian year + 166 d 23 3/4 h; 1 Egyptian year + 137 d 5 h)."))
c.append(clue(S, "PA-INT", ["H1", "H2", "H3"], "interval", "day-interval",
    "H1 to H2: 1 Egyptian year, 166 days, 23 3/4 equinoctial hours (apparent; 23 5/8 h "
    "mean). H2 to H3: 1 Egyptian year, 137 days, 5 h (apparent; 5 1/2 h mean).",
    [lic(P, "4.6.16", "ἐνιαυτοῦ Αἰγυπτιακοῦ ἑνὸς καὶ ἡμερῶν ρξς",
         "ἐνιαυτοῦ πάλιν Αἰγυπτιακοῦ ἑνὸς καὶ ἡμερῶν ρλζ καὶ ὡρῶν ἰσημερινῶν ἁπλῶς μὲν ε")],
    "narrator (Ptolemy)",
    [fork("calendar-exact", "H2 is 532 civil nights after H1; H3 is 502 after H2",
          "calendar arithmetic", {"delta_nights": {"H1->H2": 532, "H2->H3": 502}}, True),
     fork("none", "unlinked", "sensitivity", {"delta_nights": None})],
    "Redundant with PA-CAL."))
for ev, cit, magw, mag_stmt, mag_forks, timew, tstmt, toff, sunw, sunlon, sunnote in [
    ("H1", "4.6.13", "καὶ ἐξέλειπεν ὅλη", "H1 total: umbral magnitude >= 1.0.", [],
     "πρὸ ἡμίσους καὶ τετάρτου μιᾶς ὥρας ἰσημερινῆς τοῦ μεσονυκτίου",
     "Ptolemy computed mid-eclipse 3/4 equinoctial hour before midnight (Alexandria).", -0.75,
     "τοῦ Ταύρου μοίρας ιγ δʹ ἔγγιστα", 43.25, "Taurus 13 1/4 deg"),
    ("H2", "4.6.14", "ἐξέλειπεν ἀπʼ ἄρκτων τὸ U+2220ʹ καὶ γʹ τῆς διαμέτρου",
     "H2 partial, 1/2 + 1/3 = 5/6 of the diameter (10 digits) from the north: umag about 0.83.",
     [fork("pm0.10", "umbral magnitude 0.83 +/- 0.10", "as stated, about one digit of slack",
           {"umag": [0.73, 0.93]}, True),
      fork("pm0.20", "0.83 +/- 0.20", "looser", {"umag": [0.63, 1.0]}),
      fork("partial", "any partial umbral eclipse", "partial only", {"umag": [0.0, 1.0]})],
     "πρὸ α ὥρας ἰσημερινῆς τοῦ μεσονυκτίου",
     "Ptolemy computed mid-eclipse 1 equinoctial hour before midnight (Alexandria).", -1.0,
     "τῶν Χηλῶν μοίρας κε ςʹ ἔγγιστα", 205.17, "Chelae (Libra) 25 1/6 deg"),
    ("H3", "4.6.15", "ἐξέλειπε τὸ ἥμισυ τῆς διαμέτρου ἀπʼ ἄρκτων",
     "H3 partial, half the diameter from the north: umag about 0.5.",
     [fork("pm0.10", "umbral magnitude 0.50 +/- 0.10", "as stated", {"umag": [0.40, 0.60]}, True),
      fork("pm0.20", "0.50 +/- 0.20", "looser", {"umag": [0.30, 0.70]}),
      fork("partial", "any partial umbral eclipse", "partial only", {"umag": [0.0, 1.0]})],
     "μετὰ δ ὥρας ἰσημερινὰς τοῦ μεσονυκτίου",
     "Ptolemy computed mid-eclipse 4 equinoctial hours after midnight (Alexandria).", 4.0,
     "τῶν Ἰχθύων μοίρας ιδ ιβ΄ ἔγγιστα", 344.08, "Pisces 14 1/12 deg"),
]:
    c.append(clue(S, f"PA-{ev}-MAG", ev, "eclipse-lunar", "magnitude", mag_stmt,
                  [lic(P, cit, magw)], "narrator (Ptolemy's own observation)", mag_forks))
    if ev != "H1":
        c.append(clue(S, f"PA-{ev}-DIR", ev, "eclipse-lunar", "direction",
            f"{ev} eclipsed from the north: Moon south of the shadow axis (latitude < 0).",
            [lic(P, cit, "ἀπʼ ἄρκτων")], "narrator (Ptolemy)",
            [fork("south-of-axis", "Moon's ecliptic latitude < 0 at mid-eclipse",
                  "as PB-E2-DIR", {"moon_lat_sign": -1}, True),
             fork("none", "not used", "as PB-E2-DIR", {"moon_lat_sign": None})]))
    c.append(clue(S, f"PA-{ev}-TIME", ev, "time-of-day", "eclipse-timing", tstmt,
        [lic(P, cit, timew, "ἐπελογισάμεθα")],
        "narrator (Ptolemy: 'we computed', a reduction of his own observation)",
        [fork("pm0.5", f"mid-eclipse at {toff:+.2f} h from local apparent midnight (LAT) "
              "at Alexandria, +/- 0.5 h", "stated to a quarter hour",
              {"mid_minus_midnight_LAT_h": toff, "tol_h": 0.5, "site": "Alexandria"}, True),
         fork("pm1", "same, +/- 1 h", "looser", {"mid_minus_midnight_LAT_h": toff,
              "tol_h": 1.0, "site": "Alexandria"}),
         fork("none", "visibility from Alexandria only", "sensitivity", {"timing": None})]))
    c.append(clue(S, f"PA-{ev}-SUN", ev, "season", "solar-longitude",
        f"Ptolemy computes the Sun at {sunnote}: tropical longitude {sunlon} deg.",
        [lic(P, cit, sunw)], "narrator (Ptolemy's computation)",
        [fork("pm3", f"{sunlon} +/- 3 deg", "computed from tables in Ptolemy's own era; "
              "3 deg allows a tables error of a few days", {"sun_lon_deg": sunlon, "tol_deg": 3.0}, True),
         fork("pm15", f"{sunlon} +/- 15 deg", "season only", {"sun_lon_deg": sunlon, "tol_deg": 15.0}),
         fork("none", "not used", "derived quantity", {"sun_lon_deg": None})]))
sets.append({
    "set_id": S, "role": "positive control (pass/fail)",
    "texts": [{"text_file": "data/text/ptolemy-syntaxis-grc.tsv",
               "local_keys": ["4.6.13", "4.6.14", "4.6.15", "4.6.16"],
               "citation": "Ptolemy, Almagest (Syntaxis) IV.6, Heiberg's text"}],
    "events": [{"event_id": "H1", "kind": "eclipse-lunar", "ref": "4.6.13"},
               {"event_id": "H2", "kind": "eclipse-lunar", "ref": "4.6.14"},
               {"event_id": "H3", "kind": "eclipse-lunar", "ref": "4.6.15"}],
    "observer_place": [place(["H1", "H2", "H3"], "Alexandria", [src_alex],
                             {"lat": 31.20, "lon": 29.92}, COORD_NOTE)],
    "window_years": 136, "anchor_event": "H1",
    "clues": c})

# =========================================================================== #
# R-PTOL-CHAIN : the two triples joined by Ptolemy's own interval (IV.7)      #
# =========================================================================== #
S = "R-PTOL-CHAIN"
c = [clue(S, "PC-LINK", ["E2", "H2"], "interval", "day-interval",
    "From E2 (Mardokempados year 2, Thoth 18 into 19, 5/6 h before midnight at "
    "Alexandria) to H2 (Hadrian year 19, Choiak 2 into 3, 1 h before midnight): 854 "
    "Egyptian years, 73 days and 23 1/2 + 1/3 equinoctial hours (apparent; 23 1/3 h in "
    "mean days); in all 311,783 days and 23 1/3 h. Equivalently the night of H2 is "
    "311,784 civil nights after the night of E2.",
    [lic(P, "4.7.1", "περιέχει Αἰγυπτιακὰ ἔτη ωνδ καὶ ἡμέρας ογ", "πάσας δὲ ἡμέρας M λα καὶ αψπγ")],
    "narrator (Ptolemy)",
    [fork("calendar-exact", "night(H2) - night(E2) = 311,784 civil nights", "calendar "
          "arithmetic on dates given in the text (854*365 + 74)", {"delta_nights": 311784}, True),
     fork("none", "the two triples unlinked (equivalent to running R-PTOL-BAB and "
          "R-PTOL-ALEX separately)", "sensitivity", {"delta_nights": None})],
    "With this link one J_free serves both triples. The link is stated in IV.7.1, the "
    "chapter after the one named in the task; it is used because the rule admits day "
    "intervals that the text itself gives.")]
sets.append({
    "set_id": S, "role": "positive control (pass/fail); the strongest of the Ptolemy sets",
    "includes_sets": ["R-PTOL-BAB", "R-PTOL-ALEX"],
    "texts": [{"text_file": "data/text/ptolemy-syntaxis-grc.tsv", "local_keys": ["4.7.1"],
               "citation": "Ptolemy, Almagest IV.7"}],
    "events": [{"event_id": e, "kind": "eclipse-lunar"} for e in ["E1", "E2", "E3", "H1", "H2", "H3"]],
    "observer_place": [place(["E1", "E2", "E3"], "Babylon", [src_place], {"lat": 32.54, "lon": 44.42}, COORD_NOTE),
                       place(["H1", "H2", "H3"], "Alexandria", [src_alex], {"lat": 31.20, "lon": 29.92}, COORD_NOTE)],
    "window_years": 136, "anchor_event": "E1",
    "window_note": "The window bounds E1 only; H1-H3 fall about 854 years later, where the link puts them.",
    "clues": c})

# =========================================================================== #
# R-THUC : Thucydides 2.28, 4.52, 7.50                                        #
# =========================================================================== #
S = "R-THUC"
T = "thucydides-grc"
c = []
SUMMER_FORKS = lambda prim: [
    fork("half-year", "Sun's tropical longitude in [0, 180] deg (between the equinoxes)",
         "Thucydides counts by summers and winters, each half the year (5.20.3 "
         "'ἐξ ἡμισείας ἑκατέρου τοῦ ἐνιαυτοῦ'); the drafter centres the summer half on "
         "the summer solstice", {"sun_lon_deg": [0.0, 180.0]}, prim == "half-year"),
    fork("campaign", "Sun's tropical longitude in [330, 225] deg (wrapping through 0)",
         "the summer begins 'ἅμα ἦρι ἀρχομένῳ' (2.2.1) and runs to the onset of winter; "
         "this allows a summer longer than half the year (drafter's inference)",
         {"sun_lon_deg": [330.0, 225.0]}, prim == "campaign"),
    season_none("sensitivity: drop the season"),
]
c.append(clue(S, "T1-ECL", "T1", "eclipse-solar", "occurrence",
    "T1: a solar eclipse that ended in view ('filled out again'): last contact before "
    "sunset at the observer, Sun above the horizon during the eclipse.",
    [lic(T, "2.28.1.1", "ὁ ἥλιος ἐξέλιπε", "καὶ πάλιν ἀνεπληρώθη")], "narrator",
    [fork("end-seen", "Sun above the horizon at last contact", "'πάλιν ἀνεπληρώθη': "
          "the refilling was seen", {"last_contact_sun_up": True}, True),
     fork("none", "only some phase visible", "sensitivity", {"last_contact_sun_up": None})]))
c.append(clue(S, "T1-PHASE", "T1", "moon-phase", "new-moon",
    "T1 on the new-moon day by the Moon ('νουμηνίᾳ κατὰ σελήνην'); Thucydides adds that "
    "this is the only time an eclipse seems possible.",
    [lic(T, "2.28.1.1", "νουμηνίᾳ κατὰ σελήνην, ὥσπερ καὶ μόνον δοκεῖ εἶναι γίγνεσθαι δυνατόν")],
    "narrator", [], "Automatically true of any solar eclipse; recorded for completeness, "
    "adds no constraint."))
c.append(clue(S, "T1-TIME", "T1", "time-of-day", "eclipse-timing",
    "T1 'after midday'.", [lic(T, "2.28.1.1", "μετὰ μεσημβρίαν")], "narrator",
    [fork("max-pm", "maximum eclipse after local apparent noon (LAT > 12 h) at the observer",
          "the eclipse as a whole is placed after midday", {"max_LAT_h": [12.0, None]}, True),
     fork("start-pm", "first contact after local apparent noon", "stricter: the whole "
          "eclipse after midday", {"first_contact_LAT_h": [12.0, None]}),
     fork("none", "no timing", "sensitivity", {"timing": None})]))
c.append(clue(S, "T1-SHAPE", "T1", "eclipse-solar", "magnitude",
    "T1 'became crescent-shaped'.", [lic(T, "2.28.1.1", "γενόμενος μηνοειδὴς")], "narrator",
    [fork("crescent-max", "the greatest phase was a crescent: 0.5 <= magnitude < 1.0 at the "
          "observer (magnitude = fraction of the solar diameter covered)", "a crescent "
          "needs more than half the diameter covered (drafter's geometry); a total "
          "eclipse would have been described as such", {"smag": [0.5, 1.0]}, True),
     fork("crescent-passed", "magnitude >= 0.5; totality not excluded", "a crescent is "
          "also passed through on the way to totality", {"smag": [0.5, None]}),
     fork("none", "magnitude unconstrained", "sensitivity", {"smag": None})]))
c.append(clue(S, "T1-DARK", "T1", "darkness", "stars-visible",
    "'some stars having appeared'.", [lic(T, "2.28.1.1", "ἀστέρων τινῶν ἐκφανέντων")], "narrator",
    [fork("X4", "magnitude >= 0.60 at the observer", "the design's darkness-wording "
          "threshold (DESIGN 3.1 class X4, set from Hdt. 9.10 and Plut. Pel. 31)",
          {"smag": [0.60, None]}, True),
     fork("X3", "magnitude >= 0.95", "the design's near-total class (DESIGN 3.1 X3)",
          {"smag": [0.95, None]}),
     fork("none", "not used", "sensitivity", {"smag": None})],
    "Only 'some' stars, so the drafter takes the weaker threshold as primary."))
c.append(clue(S, "T1-SEASON", "T1", "season", "half-year",
    "T1 in the same summer as the events of 2.19-2.27 (the first summer of the war).",
    [lic(T, "2.28.1.1", "τοῦ δ’ αὐτοῦ θέρους")], "narrator", SUMMER_FORKS("half-year"),
    "Narrative order (after the invasion of 2.19, which came about 80 days after the "
    "attack on Plataea at the start of spring) is not used; it would be an inference "
    "from order, not a statement about the eclipse."))
c.append(clue(S, "T2-ECL", "T2", "eclipse-solar", "magnitude",
    "T2: 'some eclipse of the Sun', about the new moon; partial.",
    [lic(T, "4.52.1.1", "τοῦ τε ἡλίου ἐκλιπές τι ἐγένετο περὶ νουμηνίαν")], "narrator",
    [fork("partial", "0 < magnitude < 1.0 at the observer", "'ἐκλιπές τι', some "
          "eclipsing: not described as total or dark", {"smag": [0.0, 1.0]}, True),
     fork("any", "any magnitude > 0", "'τι' read as indefinite, not as 'small'",
          {"smag": [0.0, None]})],
    "'περὶ νουμηνίαν' is automatically true of a solar eclipse. The earthquake 'τοῦ αὐτοῦ "
    "μηνὸς ἱσταμένου' is not an astronomical clue and is not used."))
c.append(clue(S, "T2-SEASON", "T2", "season", "early-summer",
    "T2 'right at the start of the following summer'.",
    [lic(T, "4.52.1.1", "τοῦ δ’ ἐπιγιγνομένου θέρους εὐθὺς")], "narrator",
    [fork("early", "Sun's tropical longitude in [330, 60] deg (wrapping): the first two "
          "months or so of a summer that begins with spring", "'εὐθύς' at the head of "
          "the summer; summer begins 'ἅμα ἦρι' (2.2.1); the two-month width is the "
          "drafter's", {"sun_lon_deg": [330.0, 60.0]}, True)] + SUMMER_FORKS(None)[:2] +
    [season_none("sensitivity")]))
c.append(clue(S, "T3-ECL", "T3", "eclipse-lunar", "occurrence",
    "T3: a lunar eclipse at full moon, seen by the Athenians at Syracuse as they were "
    "about to sail; magnitude not stated.",
    [lic(T, "7.50.4.1", "ἡ σελήνη ἐκλείπει· ἐτύγχανε γὰρ πασσέληνος οὖσα")], "narrator",
    [fork("umbral", "umbral eclipse (umag > 0) with the Moon above the horizon at the "
          "observer during some part of the umbral phase", "an eclipse noticed by an army",
          {"umag": [0.0, None], "moon_up_during_umbral": True}, True),
     fork("penumbral-deep", "umbral, or penumbral with penumbral magnitude >= 0.7, Moon up",
          "a deep penumbral eclipse can be noticed by eye (drafter's rough threshold, "
          "general knowledge)", {"umag": None, "pmag": [0.7, None], "moon_up": True})],
    "'πασσέληνος' (full moon) is automatically true of a lunar eclipse. Nicias' "
    "'τρὶς ἐννέα ἡμέρας' is a waiting period, not a date clue, and is not used. "
    "Totality is not stated anywhere in 7.50."))
c.append(clue(S, "T3-SEASON", "T3", "season", "half-year",
    "T3 falls in the summer of the 19th war-year: that summer opens at 7.19.1 ('τοῦ δ’ "
    "ἐπιγιγνομένου ἦρος εὐθὺς ἀρχομένου') and ends at 8.1.4 ('καὶ τὸ θέρος ἐτελεύτα'); "
    "no winter is named between.",
    [lic(T, "7.19.1.1", "τοῦ δ’ ἐπιγιγνομένου ἦρος εὐθὺς ἀρχομένου"),
     lic(T, "8.1.4.1", "καὶ τὸ θέρος ἐτελεύτα")], "narrator", SUMMER_FORKS("half-year"),
    "The season is not stated at 7.50 itself; it follows from Thucydides' explicit "
    "summer/winter frame, which the text gives at both ends."))
c.append(clue(S, "T-INT-12", ["T1", "T2"], "interval", "war-years",
    "T1 lies in war-year 1 (year 1 ends at 2.47.1, after 2.28); T2 in war-year 8 (year 7 "
    "ends at 4.51.1, immediately before 4.52). T2 is 7 war-years after T1. A war-year "
    "is one natural year (5.20.3) beginning with spring (2.2.1).",
    [lic(T, "2.47.1.1", "πρῶτον ἔτος τοῦ πολέμου τοῦδε ἐτελεύτα"),
     lic(T, "4.51.1.1", "καὶ ἕβδομον ἔτος τῷ πολέμῳ ἐτελεύτα")], "narrator",
    [fork("pm0.5", "t(T2) - t(T1) = 7 years +/- 0.5 year", "both events lie in summer "
          "halves of their war-years, so the difference is 7 years give or take less "
          "than half a year", {"delta_years": 7, "tol_years": 0.5}, True),
     fork("pm1", "7 +/- 1 year", "allows uncertainty in where the war-year boundary falls",
          {"delta_years": 7, "tol_years": 1.0}),
     fork("none", "unlinked", "sensitivity", {"delta_years": None})],
    "Intermediate year-ends, all in the text: 2.70.4 (2nd), 2.103.2 (3rd), 3.25.2 (4th), "
    "3.88.4 (5th), 3.116.3 (6th)."))
c.append(clue(S, "T-INT-13", ["T1", "T3"], "interval", "war-years",
    "T3 lies in war-year 19 (year 18 ends at 7.18.4; year 19 ends at 8.6.5): 18 war-years "
    "after T1.",
    [lic(T, "7.18.4.1", "καὶ ὄγδοον καὶ δέκατον ἔτος τῷ πολέμῳ ἐτελεύτα"),
     lic(T, "8.6.5.1", "καὶ ἑνὸς δέον εἰκοστὸν ἔτος τῷ πολέμῳ ἐτελεύτα")], "narrator",
    [fork("pm0.5", "t(T3) - t(T1) = 18 years +/- 0.5 year", "as T-INT-12",
          {"delta_years": 18, "tol_years": 0.5}, True),
     fork("pm1", "18 +/- 1 year", "as T-INT-12", {"delta_years": 18, "tol_years": 1.0}),
     fork("none", "unlinked", "sensitivity", {"delta_years": None})],
    "T2 to T3 (11 war-years) follows from T-INT-12 and T-INT-13 and is not a separate clue."))
c.append(clue(S, "T1-SITE", "T1", "site", "observer",
    "Where T1 was seen: unstated.", [lic(T, "1.1.1.1", "Θουκυδίδης Ἀθηναῖος")],
    "narrator (self-identification)",
    site_forks("Athens", ATHENS, "inference: the narrator is an Athenian (1.1.1) and the "
               "neighbouring narrative (2.27) concerns Athens and Aegina", AEGEAN_BOX,
               "the Greek mainland and Aegean, where the war was being fought"),
    "The licence words identify the narrator only; they do not place the eclipse."))
c.append(clue(S, "T2-SITE", "T2", "site", "observer", "Where T2 was seen: unstated.",
    [lic(T, "1.1.1.1", "Θουκυδίδης Ἀθηναῖος")], "narrator (self-identification)",
    site_forks("Athens", ATHENS, "inference from the narrator, as T1-SITE", AEGEAN_BOX,
               "as T1-SITE; the next sentence (4.52.2) is set in the Troad, inside the box")))
sets.append({
    "set_id": S, "role": "positive control (pass/fail)",
    "texts": [{"text_file": "data/text/thucydides-grc.tsv",
               "local_keys": ["2.28.1.1", "4.52.1.1", "7.50.4.1", "2.47.1.1", "4.51.1.1", "7.18.4.1",
                        "7.19.1.1", "8.1.4.1", "8.6.5.1", "5.20.3.1", "2.2.1.1"],
               "citation": "Thucydides 2.28, 4.52, 7.50 and the war-year statements"}],
    "events": [{"event_id": "T1", "kind": "eclipse-solar", "ref": "2.28.1.1"},
               {"event_id": "T2", "kind": "eclipse-solar", "ref": "4.52.1.1"},
               {"event_id": "T3", "kind": "eclipse-lunar", "ref": "7.50.4.1"}],
    "observer_place": [
        unstated(["T1"], "unstated; site forks in clue T1-SITE"),
        unstated(["T2"], "unstated; site forks in clue T2-SITE"),
        place(["T3"], "the Athenian camp at Syracuse",
              [lic(T, "7.50.1.1", "ἐς τὰς Συρακούσας"), lic(T, "7.50.3.1", "ἐκ τοῦ στρατοπέδου")],
              SYRACUSE, COORD_NOTE)],
    "window_years": 136, "anchor_event": "T1",
    "clues": c})

# =========================================================================== #
# R-XEN : Xenophon, Hellenica 1.6.1, 2.3.4, 4.3.10                            #
# =========================================================================== #
S = "R-XEN"
X = "xenophon-hellenica-grc"
c = []
GLOSS_NOTE = ("The chronological notices of Hellenica 1-2 (ephors, archons, Olympiads, "
              "war-year counts, Sicilian notices) are widely held to be later "
              "interpolations [critique-design issue 2 cites ctl §4.4 for this; the drafter "
              "did not open that note]. The local text prints them without brackets, and "
              "the drafter could not check from it whether the eclipse clause belongs to "
              "the gloss.")
c.append(clue(S, "X1-ECL", "X1", "eclipse-lunar", "occurrence",
    "X1: the Moon was eclipsed in the evening, in the same year as the burning of the old "
    "temple of Athena at Athens.",
    [lic(X, "1.6.1.1", "ἥ τε σελήνη ἐξέλιπεν ἑσπέρας")],
    "narrator (inside a year heading that may be an interpolated gloss)",
    [fork("use", "umbral lunar eclipse (umag > 0), Moon above the horizon at the observer "
          "during part of the umbral phase", "as written", {"umag": [0.0, None]}, True),
     fork("exclude", "drop X1 (heading treated as a gloss)", GLOSS_NOTE, {"exclude": True})]))
c.append(clue(S, "X1-TIME", "X1", "time-of-day", "evening",
    "X1 'in the evening'.", [lic(X, "1.6.1.1", "ἑσπέρας")], "narrator (year heading)",
    [fork("early-night", "some umbral phase visible between sunset and sunset + 3 h at "
          "the observer", "ἑσπέρα = evening; 3 h is the drafter's width",
          {"umbral_visible_between_h_after_sunset": [0.0, 3.0]}, True),
     fork("before-midnight", "some umbral phase visible before local apparent midnight",
          "looser reading of 'evening'", {"umbral_visible_before_LAT_h": 24.0}),
     fork("none", "no timing", "sensitivity", {"timing": None})]))
c.append(clue(S, "X1-SITE", "X1", "site", "observer",
    "Where X1 was seen: unstated. The same clause names Athens for the temple fire only.",
    [lic(X, "1.6.1.1", "ὁ παλαιὸς τῆς Ἀθηνᾶς νεὼς ἐν Ἀθήναις ἐνεπρήσθη")], "narrator (year heading)",
    site_forks("Athens", ATHENS, "inference: the clause pairs the eclipse with an "
               "Athenian event", AEGEAN_BOX, "the theatre of the narrative (Aegean war)",
               primary="box")))
c.append(clue(S, "X2-ECL", "X2", "eclipse-solar", "occurrence",
    "X2: 'about the time of an eclipse of the Sun'; no magnitude, no hour.",
    [lic(X, "2.3.4.1", "κατὰ δὲ τοῦτον τὸν καιρὸν περὶ ἡλίου ἔκλειψιν")], "narrator",
    [fork("any", "a solar eclipse with magnitude > 0 at the observer, Sun up",
          "the text says only that there was a solar eclipse", {"smag": [0.0, None]}, True),
     fork("noticed", "magnitude >= 0.5 at the observer", "an eclipse noticed without "
          "being sought; 0.5 is the drafter's rough threshold", {"smag": [0.5, None]})]))
c.append(clue(S, "X2-SITE", "X2", "site", "observer",
    "Where X2 was seen: unstated. The clause dates a battle in Thessaly fought by Lycophron "
    "of Pherae against the Larisaeans.",
    [lic(X, "2.3.4.1", "Λυκόφρων ὁ Φεραῖος", "Λαρισαίους")], "narrator",
    [fork("box", "anywhere in the Aegean box", "no place is given for the eclipse itself",
          {"site_box": AEGEAN_BOX}, True),
     fork("thessaly", "Thessaly (Pherae-Larisa, 39.5N 22.6E)", "inference: the eclipse "
          "dates a Thessalian event", {"site": {"lat": 39.5, "lon": 22.6}}),
     fork("athens", "Athens", "inference: the surrounding narrative (2.3.1-3) is Athenian",
          {"site": ATHENS}),
     fork("none", "anywhere on Earth", "sensitivity", {"site": None})]))
c.append(clue(S, "X-INT-12", ["X1", "X2"], "interval", "year-headings",
    "X1 is in the year opened at 1.6.1 ('τῷ δ’ ἐπιόντι ἔτει'); the next year opens at "
    "2.1.10 and ends at 2.2.24 ('καὶ ὁ ἐνιαυτὸς ἔληγεν'); the year after opens at 2.3.1, and "
    "X2 falls 'at this time' within it. X2 is two Xenophontic years after X1.",
    [lic(X, "1.6.1.1", "τῷ δʼ ἐπιόντι ἔτει"), lic(X, "2.1.10.1", "τῷ δʼ ἐπιόντι ἔτει"),
     lic(X, "2.2.24.1", "καὶ ὁ ἐνιαυτὸς ἔληγεν"), lic(X, "2.3.1.1", "τῷ δʼ ἐπιόντι ἔτει")],
    "narrator (year headings, possibly interpolated)",
    [fork("1to3", "1 year < t(X2) - t(X1) < 3 years", "two year-boundaries apart; the "
          "position of each event within its year is unknown", {"delta_years": [1.0, 3.0]}, True),
     fork("none", "unlinked", GLOSS_NOTE, {"delta_years": None})],
    "The war-year counts in the same headings (1.6.1 'τεττάρων καὶ εἴκοσιν ἐτῶν', 2.1.7 "
    "'πέντε καὶ εἴκοσι') agree with consecutive years but are not used, being the "
    "most suspect part of the headings."))
c.append(clue(S, "X2-SEASON", "X2", "season", "narrative-order",
    "Not stated. 2.3.9 has Lysander back at Sparta 'τελευτῶντος τοῦ θέρους' after the "
    "events of 2.3.3-4.",
    [lic(X, "2.3.9.1", "τελευτῶντος τοῦ θέρους")], "narrator",
    [season_none("the eclipse's own sentence gives no season", True),
     fork("before-autumn", "Sun's tropical longitude in [330, 210] deg", "inference from "
          "narrative order: X2 precedes an end of summer in the same year",
          {"sun_lon_deg": [330.0, 210.0]})]))
c.append(clue(S, "X3-ECL", "X3", "eclipse-solar", "magnitude",
    "X3: 'the Sun seemed to appear crescent-shaped' while Agesilaus was at the entry "
    "into Boeotia.",
    [lic(X, "4.3.10.1", "ὁ ἥλιος μηνοειδὴς ἔδοξε φανῆναι")], "narrator",
    [fork("crescent", "0.5 <= magnitude < 1.0 at the observer", "a visible crescent needs "
          "more than half the diameter covered (drafter's geometry); not described as "
          "total or dark", {"smag": [0.5, 1.0]}, True),
     fork("any", "any magnitude > 0", "'ἔδοξε' (seemed): a weak impression",
          {"smag": [0.0, None]})]))
c.append(clue(S, "X3-SEASON", "X3", "season", "narrative-order",
    "Not stated. 4.1.41 says spring was just showing when Agesilaus left Pharnabazus' "
    "country; the recall (4.2.1-3), the march (4.2.8-4.3.9) and X3 follow.",
    [lic(X, "4.1.41.1", "σχεδὸν δὲ καὶ ἔαρ ἤδη ὑπέφαινεν")], "narrator",
    [season_none("the eclipse's own sentence gives no season", True),
     fork("after-spring", "Sun's tropical longitude in [330, 225] deg", "inference from "
          "narrative order: after the start of spring, within one campaigning season",
          {"sun_lon_deg": [330.0, 225.0]})]))
sets.append({
    "set_id": S, "role": "positive control (pass/fail)",
    "texts": [{"text_file": "data/text/xenophon-hellenica-grc.tsv",
               "local_keys": ["1.6.1.1", "2.1.10.1", "2.2.24.1", "2.3.1.1", "2.3.4.1", "2.3.9.1",
                        "4.1.41.1", "4.3.9.1", "4.3.10.1"],
               "citation": "Xenophon, Hellenica 1.6.1, 2.3.4, 4.3.10"}],
    "events": [{"event_id": "X1", "kind": "eclipse-lunar", "ref": "1.6.1.1"},
               {"event_id": "X2", "kind": "eclipse-solar", "ref": "2.3.4.1"},
               {"event_id": "X3", "kind": "eclipse-solar", "ref": "4.3.10.1", "linked": False}],
    "observer_place": [
        unstated(["X1"], "unstated; forks in X1-SITE"),
        unstated(["X2"], "unstated; forks in X2-SITE"),
        place(["X3"], "Agesilaus' army at the entry into Boeotia, coming from Phthiotis",
              [lic(X, "4.3.10.1", "ὄντος δʼ αὐτοῦ ἐπὶ τῇ ἐμβολῇ"),
               lic(X, "4.3.9.1", "μέχρι πρὸς τὰ Βοιωτῶν ὅρια")],
              {"lat": 38.5, "lon": 22.85}, COORD_NOTE + "; the Boeotian frontier towards "
              "Phocis, near Chaeronea and Coronea (4.3.15)")],
    "window_years": 136, "anchor_event": "X1",
    "window_note": "X3 has no textual link to X1/X2 and is searched in its own 136-year window.",
    "clues": c})

# =========================================================================== #
# R-ARBELA : the lunar eclipse before Gaugamela                                #
# =========================================================================== #
S = "R-ARBELA"
PA_ = "plutarch-alexander-grc"
AR = "arrian-anabasis-grc"
CU = "curtius-lat"
PL = "pliny-nh-lat"
c = []
c.append(clue(S, "A-ECL", "A1", "eclipse-lunar", "occurrence",
    "A1: a lunar eclipse seen by Alexander's army in the days before the great battle "
    "with Darius (four sources, one event).",
    [lic(PA_, "31.4.1", "ἡ μὲν οὖν σελήνη τοῦ Βοηδρομιῶνος ἐξέλιπε"),
     lic(AR, "3.7.5.1", "καὶ τῆς σελήνης τὸ πολὺ ἐκλιπὲς ἐγένετο"),
     lic(CU, "4.10.2.1", "luna deficiens"),
     lic(PL, "2.70.3", "luna defecisse")],
    "narrator (all four)", [],
    "Arrian's eclipse sentence is 3.7.6 in the standard numbering; the local row key is "
    "3.7.5.1. Pliny NH 2.180 is local key 2.70.3."))
c.append(clue(S, "A-MAG", "A1", "eclipse-lunar", "magnitude",
    "Arrian: the greater part of the Moon was eclipsed. Curtius: the Moon first hid its "
    "brightness, then, suffused with a blood colour, fouled all its light.",
    [lic(AR, "3.7.5.1", "τῆς σελήνης τὸ πολὺ ἐκλιπὲς"),
     lic(CU, "4.10.2.1", "deinde sanguinis colore suffuso lumen omne foedavit")],
    "narrator",
    [fork("gt-half", "umbral magnitude > 0.5", "the weakest reading compatible with both "
          "sources (total satisfies 'the greater part')", {"umag": [0.5, None]}, True),
     fork("total", "umbral magnitude >= 1.0", "Curtius: blood colour, all light fouled",
          {"umag": [1.0, None]}),
     fork("partial-gt-half", "0.5 < umag < 1.0", "Arrian alone, 'τὸ πολύ' read as 'most, "
          "not all'", {"umag": [0.5, 1.0]}),
     fork("none", "magnitude unconstrained", "sensitivity", {"umag": None})]))
c.append(clue(S, "A-TIME-PLINY", "A1", "time-of-day", "eclipse-timing",
    "Pliny: at Arbela the Moon was reported eclipsed in the second hour of the night.",
    [lic(PL, "2.70.3", "apud Arbilam Magni Alexandri victoria luna defecisse noctis secunda hora est prodita")],
    "narrator (Pliny, reporting a tradition: 'est prodita')",
    [fork("in-progress", "umbral phase in progress at some time during the 2nd seasonal "
          "hour of the night at Arbela (night = sunset to sunrise in 12 equal hours)",
          "the hour is given for the eclipse, not for a contact", {"seasonal_night_hour": 2,
          "site": "Arbela", "relation": "umbral phase overlaps hour"}, True),
     fork("onset", "first umbral contact within the 2nd seasonal hour of the night",
          "'defecisse' read as the start", {"seasonal_night_hour": 2, "site": "Arbela",
          "relation": "first contact in hour"}),
     fork("none", "not used", "sensitivity", {"timing": None})]))
c.append(clue(S, "A-TIME-CURTIUS", "A1", "time-of-day", "eclipse-timing",
    "Curtius: about the first watch, two days after crossing the Tigris.",
    [lic(CU, "4.10.2.1", "Sed prima fere vigilia"),
     lic(CU, "4.10.1.1", "Biduo ibi stafiva rex habuit")], "narrator",
    [fork("first-watch", "umbral phase in progress at some time during the first watch "
          "(the first quarter of the night, sunset to sunset + night/4) at the camp, "
          "+/- 1 h for 'fere'", "Roman watches are quarters of the night",
          {"night_quarter": 1, "tol_h": 1.0, "site": "Tigris camp"}, True),
     fork("none", "not used", "sensitivity", {"timing": None})],
    "The local text has the OCR slip 'stafiva' for 'stativa'."))
c.append(clue(S, "A-SICILY", "A1", "other", "moonrise-elsewhere",
    "Pliny: the same eclipse was seen in Sicily as the Moon was rising.",
    [lic(PL, "2.70.3", "eademque in Sicilia exoriens")], "narrator (Pliny)",
    [fork("sicily-box", "the Moon rises at some site in Sicily while the umbral eclipse is "
          "in progress", "as written; Sicily is named as a whole",
          {"moonrise_during_umbral": True, "site_box": SICILY_BOX}, True),
     fork("syracuse", "the Moon rises at Syracuse while the umbral eclipse is in progress",
          "a single Sicilian city", {"moonrise_during_umbral": True, "site": SYRACUSE}),
     fork("none", "not used", "Pliny's sentence illustrates longitude and may be a "
          "computed illustration rather than a report", {"moonrise_during_umbral": None})]))
c.append(clue(S, "A-MONTH", "A1", "other", "calendar-date",
    "Plutarch: the eclipse was in Boedromion, about the beginning of the Mysteries at "
    "Athens. Arrian: the battle was in Pyanepsion, in the same month in which the Moon "
    "was seen eclipsed.",
    [lic(PA_, "31.4.1", "τοῦ Βοηδρομιῶνος", "περὶ τὴν τῶν μυστηρίων τῶν Ἀθήνησιν ἀρχήν"),
     lic(AR, "3.15.7.1", "μηνὸς Πυανεψιῶνος", "ἐν τῷ αὐτῷ μηνί, ἐν ὅτῳ ἡ σελήνη ἐκλιπὴς ἐφάνη")],
    "narrator",
    [fork("either", "the full moon of Attic month 3 or 4, with a free offset of -1, 0 or "
          "+1 lunation", "the two sources disagree; the union is the weakest reading",
          {"attic_month": [3, 4], "lunation_offset": [-1, 0, 1]}, True),
     fork("boedromion", "Attic month 3, offset -1..+1", "Plutarch",
          {"attic_month": [3], "lunation_offset": [-1, 0, 1]}),
     fork("pyanepsion", "Attic month 4, offset -1..+1", "Arrian",
          {"attic_month": [4], "lunation_offset": [-1, 0, 1]}),
     fork("none", "month not used", "the Attic calendar's alignment is not given in "
          "these texts", {"attic_month": None})],
    "Operational Attic month: month 1 (Hekatombaion) begins at the first new moon after "
    "the summer solstice; month m is the m-th lunation from there. This rule is a "
    "modern reconstruction of the Athenian calendar [secondary: standard handbooks, e.g. "
    "Samuel, Greek and Roman Chronology, 1972], not in these texts; the free offset "
    "absorbs intercalation. Arrian's archon name ('ἐπὶ ἄρχοντος Ἀθηναίοις "
    "Ἀριστοφάνους') would need a modern archon list and is not used. Plutarch's "
    "'eleventh night after the eclipse' dates the battle, not the sky, and is not used."))
sets.append({
    "set_id": S, "role": "positive control (pass/fail)",
    "texts": [{"text_file": "data/text/plutarch-alexander-grc.tsv", "local_keys": ["31.4.1"],
               "citation": "Plutarch, Alexander 31.4"},
              {"text_file": "data/text/arrian-anabasis-grc.tsv", "local_keys": ["3.7.5.1", "3.15.7.1"],
               "citation": "Arrian, Anabasis 3.7.6 (local 3.7.5.1) and 3.15.7"},
              {"text_file": "data/text/curtius-lat.tsv", "local_keys": ["4.10.1.1", "4.10.2.1"],
               "citation": "Curtius 4.10.1-2"},
              {"text_file": "data/text/pliny-nh-lat.tsv", "local_keys": ["2.70.3"],
               "citation": "Pliny, NH 2.180 (local 2.70.3)"}],
    "events": [{"event_id": "A1", "kind": "eclipse-lunar"}],
    "observer_place": [
        place(["A1"], "Arbela (Pliny's report)", [lic(PL, "2.70.3", "apud Arbilam")],
              {"lat": 36.19, "lon": 44.01}, COORD_NOTE),
        place(["A1"], "the Macedonian camp just across the Tigris (Arrian, Curtius)",
              [lic(AR, "3.7.5.1", "διαβαίνει τὸν πόρον", "ἐνταῦθα ἀναπαύει τὸν στρατόν")],
              {"lat": 36.5, "lon": 43.0}, COORD_NOTE + "; the crossing point is not known "
              "and this placement is rough (+/- 0.5 deg)"),
        place(["A1"], "Sicily (Pliny: Moon rising)", [lic(PL, "2.70.3", "in Sicilia")],
              SICILY_BOX, COORD_NOTE)],
    "window_years": 136, "anchor_event": "A1",
    "clues": c})

# =========================================================================== #
# R-PYDNA : Livy 44.36-37, Plutarch Aemilius 16-17                             #
# =========================================================================== #
S = "R-PYDNA"
LV = "livy-lat"
AE = "plutarch-aemilius-grc"
c = []
c.append(clue(S, "P-ECL", "P1", "eclipse-lunar", "occurrence",
    "P1: a lunar eclipse on the night before the battle, foretold by C. Sulpicius Gallus "
    "and seen from both camps; the Moon was full and high.",
    [lic(LV, "4.44.37.8.1", "edita hora luna cum defecisset"),
     lic(AE, "17.7.1", "ἡ σελήνη πλήρης οὖσα καὶ μετέωρος ἐμελαίνετο")],
    "narrator (Livy reports Gallus' forecast, a character's speech in indirect form, then "
    "confirms it in narrative; Plutarch narrator)", []))
c.append(clue(S, "P-MAG", "P1", "eclipse-lunar", "magnitude",
    "Plutarch: with its light gone, after changing all sorts of colours, the Moon "
    "vanished. Livy gives no magnitude.",
    [lic(AE, "17.7.1", "τοῦ φωτὸς ἀπολιπόντος αὐτὴν χρόας ἀμείψασα παντοδαπὰς ἠφανίσθη")],
    "narrator (Plutarch)",
    [fork("total", "umbral magnitude >= 1.0", "Plutarch's 'vanished' after colour changes; "
          "Livy is silent, not contrary", {"umag": [1.0, None]}, True),
     fork("deep", "umbral magnitude >= 0.8", "allows a deep partial eclipse to be "
          "described as vanishing", {"umag": [0.8, None]}),
     fork("umbral", "any umbral eclipse", "Livy alone", {"umag": [0.0, None]})]))
c.append(clue(S, "P-TIME", "P1", "time-of-day", "eclipse-timing",
    "Gallus foretold the eclipse from the second to the fourth hour of the night, and it "
    "happened at the hour announced. Plutarch: after nightfall and dinner, as they turned "
    "to sleep.",
    [lic(LV, "4.44.37.5.1", "ab hora secunda usque ad quartam horam noctis lunam defecturam esse"),
     lic(LV, "4.44.37.8.1", "edita hora"),
     lic(AE, "17.7.1", "ἐπεὶ δὲ νὺξ γεγόνει καὶ μετὰ δεῖπνον ἐτράποντο πρὸς ὕπνον")],
    "Livy: character's forecast (indirect speech) confirmed by the narrator; Plutarch: narrator",
    [fork("overlap", "the umbral phase overlaps the 2nd-4th seasonal hours of the night "
          "(night = sunset to sunrise in 12 equal hours) at the camp",
          "'edita hora': the eclipse came at the announced hours", {"seasonal_night_hours":
          [2, 4], "relation": "umbral phase overlaps", "site": "Pydna"}, True),
     fork("within", "first umbral contact in hour 2 or later and last umbral contact by "
          "the end of hour 4", "'ab ... usque ad' read as the whole eclipse",
          {"seasonal_night_hours": [2, 4], "relation": "umbral phase within", "site": "Pydna"}),
     fork("none", "not used", "sensitivity", {"timing": None})],
    "The hours are seasonal: Gallus speaks to soldiers, not astronomers (drafter's choice)."))
c.append(clue(S, "P-ALT", "P1", "other", "moon-altitude",
    "Plutarch: the Moon was full and high ('μετέωρος') when it darkened.",
    [lic(AE, "17.7.1", "πλήρης οὖσα καὶ μετέωρος")], "narrator (Plutarch)",
    [fork("aloft", "Moon's altitude >= 10 deg at the onset of the umbral phase",
          "'μετέωρος' = aloft, off the horizon; 10 deg is the drafter's threshold",
          {"moon_alt_deg_at_first_umbral_contact": [10.0, None]}, True),
     fork("up", "Moon above the horizon at first umbral contact", "weaker",
          {"moon_alt_deg_at_first_umbral_contact": [0.0, None]}),
     fork("none", "not used", "sensitivity", {"moon_alt": None})]))
c.append(clue(S, "P-END", "P1", "eclipse-lunar", "emergence-seen",
    "Both sources say the emergence was seen: the Macedonian uproar lasted until the "
    "Moon came out into its light (Livy); Aemilius sacrificed when he first saw the Moon "
    "clearing (Plutarch).",
    [lic(LV, "4.44.37.9.1", "donec luna in suam lucem emersit"),
     lic(AE, "17.10.1", "ὡς εἶδε πρῶτον τὴν σελήνην ἀποκαθαιρομένην")], "narrator",
    [fork("emergence", "Moon above the horizon at the end of the umbral phase",
          "both sources", {"moon_up_at_last_umbral_contact": True}, True),
     fork("none", "not used", "sensitivity", {"moon_up_at_last_umbral_contact": None})]))
c.append(clue(S, "P-SEASON", "P1", "season", "after-solstice",
    "Livy (that day): the time of year was after the solstice had come round, the Sun "
    "growing hot. Plutarch: it was the season of waning summer, the rivers low.",
    [lic(LV, "4.44.36.1.1", "Tempus anni post circumactum solstitium erat"),
     lic(AE, "16.9.1", "θέρους γὰρ ἦν ὥρα φθίνοντος")], "narrator",
    [fork("summer-after-solstice", "Sun's tropical longitude in [90, 180] deg",
          "the union of Livy (after the summer solstice) and Plutarch (waning summer)",
          {"sun_lon_deg": [90.0, 180.0]}, True),
     fork("livy-just-after", "Sun's tropical longitude in [90, 120] deg", "Livy alone, "
          "'circumactum' read as 'just turned'; the 30-deg width is the drafter's",
          {"sun_lon_deg": [90.0, 120.0]}),
     fork("plutarch", "Sun's tropical longitude in [120, 180] deg", "Plutarch alone",
          {"sun_lon_deg": [120.0, 180.0]}),
     season_none("sensitivity")],
    "'solstitium' alone is the summer solstice in Latin (the winter one is 'bruma'); the "
    "heat words in 44.36.1-2 agree. Note for the record: critique-design issue 2 says "
    "the earlier draft's 'summer' for this set had no textual source; it has one, in "
    "44.36.1, one chapter before the eclipse sentence."))
c.append(clue(S, "P-DATE", "P1", "other", "calendar-date",
    "Livy: the eclipse was in the night followed by the day 'pridie Nonas Septembres' "
    "(Roman 4 September), i.e. the evening of Roman 3 September.",
    [lic(LV, "4.44.37.8.1", "nocte, quam pridie nonas Septembres insecuta est dies")],
    "narrator (Livy)",
    [fork("free", "JD = JD(proleptic Julian 3/4 Sep of year y, night) + delta, delta an "
          "unknown integer number of days, unbounded", "the Roman calendar before 45 BC "
          "had an unknown, varying offset from the Julian; the rule for this bench is a "
          "free offset", {"roman_date": "a.d. III Non. Sept. (night before pridie Non. Sept.)",
          "offset_days": None}, True),
     fork("bounded90", "same with |delta| <= 90 days", "assumes the calendar was within "
          "a season of the Sun (drafter's assumption, not in the text)",
          {"roman_date": "a.d. III Non. Sept.", "offset_days": [-90, 90]}),
     fork("naive", "delta = 0 (Roman date read as Julian)", "sensitivity only; not a "
          "licensed reading", {"roman_date": "a.d. III Non. Sept.", "offset_days": [0, 0]})],
    "With the primary (free) offset this row constrains nothing; it is entered so that "
    "the bench can report what the date would have added under each bound."))
sets.append({
    "set_id": S, "role": "positive control (pass/fail)",
    "texts": [{"text_file": "data/text/livy-lat.tsv",
               "local_keys": ["4.44.36.1.1", "4.44.37.5.1", "4.44.37.8.1", "4.44.37.9.1", "4.44.42.7.1"],
               "citation": "Livy 44.36.1, 44.37.5-9"},
              {"text_file": "data/text/plutarch-aemilius-grc.tsv",
               "local_keys": ["16.5.1", "16.9.1", "17.7.1", "17.10.1"],
               "citation": "Plutarch, Aemilius Paullus 16-17"}],
    "events": [{"event_id": "P1", "kind": "eclipse-lunar"}],
    "observer_place": [place(["P1"], "the Roman and Macedonian camps before Pydna",
        [lic(AE, "16.5.1", "πρὸ τῆς Πύδνης"),
         lic(LV, "4.44.42.7.1", "qui Pydnam ex acie perfugerant")],
        {"lat": 40.37, "lon": 22.60}, COORD_NOTE)],
    "window_years": 136, "anchor_event": "P1",
    "clues": c})

# =========================================================================== #
# R-DIOD : Diodorus 20.5.5, Agathocles                                         #
# =========================================================================== #
S = "R-DIOD"
DI = "diodorus-bk18-20-grc"
c = []
c.append(clue(S, "D-ECL", "D1", "eclipse-solar", "magnitude",
    "D1: on the day after Agathocles' fleet escaped from Syracuse (at nightfall), an "
    "eclipse of the Sun so great that it seemed fully night, with stars seen everywhere.",
    [lic(DI, "20.5.5.1", "τῇ δʼ ὑστεραίᾳ τηλικαύτην ἔκλειψιν ἡλίου συνέβη γενέσθαι ὥστε ὁλοσχερῶς φανῆναι νύκτα, θεωρουμένων τῶν ἀστέρων πανταχοῦ")],
    "narrator",
    [fork("X3", "magnitude >= 0.95 at the observer", "darkness 'like full night' with "
          "stars everywhere: the design's near-total class (DESIGN 3.1 X3); ancient "
          "accounts do not separate total from near-total", {"smag": [0.95, None]}, True),
     fork("total", "magnitude >= 1.0 at the observer", "'ὁλοσχερῶς ... νύκτα' read as totality",
          {"smag": [1.0, None]}),
     fork("X4", "magnitude >= 0.60", "the design's darkness-wording class (X4)",
          {"smag": [0.60, None]})],
    "No hour and no season are in the text; none is entered. 'τῇ δʼ ὑστεραίᾳ' ties the "
    "eclipse to the escape (20.5.4 'ἐπιλαβούσης τῆς νυκτὸς'), which is not dated."))
c.append(clue(S, "D-SITE", "D1", "site", "observer",
    "The observers are Agathocles' men at sea, one day out of Syracuse, bound for Libya "
    "(six days and nights of sailing, 20.6.1).",
    [lic(DI, "20.5.2.1", "ἐξέπλευσεν"), lic(DI, "20.5.5.1", "οἱ περὶ τὸν Ἀγαθοκλέα"),
     lic(DI, "20.6.1.1", "ἓξ δʼ ἡμέρας καὶ τὰς ἴσας νύκτας αὐτῶν πλευσάντων")], "narrator",
    [fork("day-out", "any point at sea within 150 km of Syracuse", "one day's rowing from "
          "the harbour (drafter's distance); the direction of the first day's course is "
          "not given", {"site_disc": {"lat": 37.07, "lon": 15.29, "radius_km": 150}}, True),
     fork("syracuse", "Syracuse itself", "the departure point", {"site": SYRACUSE}),
     fork("route-box", "anywhere in 35.5-38.5N, 10.0-16.0E (Sicily to the African coast)",
          "the whole crossing", {"site_box": {"lat": [35.5, 38.5], "lon": [10.0, 16.0]}})]))
sets.append({
    "set_id": S, "role": "positive control (pass/fail)",
    "texts": [{"text_file": "data/text/diodorus-bk18-20-grc.tsv",
               "local_keys": ["20.5.2.1", "20.5.4.1", "20.5.5.1", "20.6.1.1"],
               "citation": "Diodorus 20.5-6"}],
    "events": [{"event_id": "D1", "kind": "eclipse-solar"}],
    "observer_place": [place(["D1"], "Agathocles' fleet at sea, the day after leaving Syracuse",
        [lic(DI, "20.5.2.1", "ὡς ἴδεν τὸ στόμα τοῦ λιμένος ἔρημον τῶν ἐφορμούντων, ἐξέπλευσεν")],
        {"lat": 37.07, "lon": 15.29, "radius_km": 150}, COORD_NOTE + "; centre Syracuse")],
    "window_years": 136, "anchor_event": "D1",
    "clues": c})

# =========================================================================== #
# H-LIVY : the prodigy notices (hard case)                                     #
# =========================================================================== #
S = "H-LIVY"
c = []
ROMAN_FREE = lambda rd: [
    fork("free", "JD = JD(proleptic Julian date of the same name in year y) + delta, delta "
         "an unknown integer, unbounded", "Roman calendar of the Republic: unknown offset",
         {"roman_date": rd, "offset_days": None}, True),
    fork("bounded90", "same with |delta| <= 90 days", "drafter's assumption, not in the text",
         {"roman_date": rd, "offset_days": [-90, 90]}),
    fork("naive", "delta = 0", "sensitivity only; not a licensed reading",
         {"roman_date": rd, "offset_days": [0, 0]})]
# L1
c.append(clue(S, "L1-ECL", "L1", "eclipse-solar", "magnitude",
    "L1: among prodigies reported from several places at once, 'the Sun's disk seemed to "
    "be diminished'.", [lic(LV, "2.22.1.9.1", "solis orbem minui visum")],
    "narrator (reported prodigy)",
    [fork("any", "magnitude > 0 at the observer, Sun up", "'minui visum': a diminished "
          "disk, no darkness", {"smag": [0.0, None]}, True),
     fork("noticed", "magnitude >= 0.5", "an unsought eclipse noticed by eye (drafter's "
          "rough threshold)", {"smag": [0.5, None]})]))
c.append(clue(S, "L1-SITE", "L1", "site", "observer",
    "Not stated for this item. The list opens 'in Sicilia ...', then 'in Sardinia autem "
    "...', and runs on in accusative-infinitive items until 'Praeneste' names a new place.",
    [lic(LV, "2.22.1.8.1", "prodigia ex pluribus simul locis nuntiata", "in Sicilia",
         "in Sardinia autem"), lic(LV, "2.22.1.9.1", "et Praeneste")],
    "narrator (reported prodigy)",
    [fork("italy-box", "anywhere in Italy, Sicily and Sardinia (36.6-44.0N, 8.0-18.6E)",
          "the list covers several places; the item's own place is not named",
          {"site_box": ITALY_BOX}, True),
     fork("sardinia", "Sardinia (38.9-41.3N, 8.1-9.9E)", "grammatical reading: 'in Sardinia "
          "autem' governs the run of items up to 'Praeneste'",
          {"site_box": {"lat": [38.9, 41.3], "lon": [8.1, 9.9]}}),
     fork("rome", "Rome", "the place where the prodigies were reported, not seen",
          {"site": {"lat": 41.89, "lon": 12.49}}),
     fork("none", "anywhere", "sensitivity", {"site": None})]))
c.append(clue(S, "L1-DATE", "L1", "season", "report-time",
    "The prodigies were reported when the consul entered office at Rome on the Ides of "
    "March, as spring was approaching; the eclipse came before the report, by an "
    "unstated time.",
    [lic(LV, "2.22.1.1.1", "iam ver adpetebat"),
     lic(LV, "2.22.1.4.1", "Cn. Servilius consul Romae idibus Martiis magistratum iniit")],
    "narrator",
    [season_none("the text dates the report, not the eclipse", True),
     fork("within-12mo", "the eclipse lies within the 12 months before a time when the "
          "Sun's tropical longitude is in [315, 15] deg (late winter to early spring)",
          "inference: prodigies were reported in the year they occurred; 'iam ver "
          "adpetebat' is a natural season, so no calendar offset is needed",
          {"before_report_months": [0, 12], "report_sun_lon_deg": [315.0, 15.0]})]))
c.append(clue(S, "L1b-ARPI", "L1b", "other", "possible-eclipse",
    "Same list: at Arpi shields were seen in the sky and 'the Sun fighting with the Moon'.",
    [lic(LV, "2.22.1.9.1", "Arpis parmas in caelo visas pugnantemque cum luna solem")],
    "narrator (reported prodigy)",
    [fork("not-eclipse", "not used as an eclipse report", "the words do not say the Sun "
          "was darkened", {"exclude": True}, True),
     fork("eclipse-arpi", "a solar eclipse visible at Arpi (41.50N, 15.56E), magnitude > 0",
          "the Sun 'fighting with the Moon' may describe an eclipse",
          {"smag": [0.0, None], "site": {"lat": 41.50, "lon": 15.56}})]))
# L2
c.append(clue(S, "L2-ECL", "L2", "eclipse-solar", "magnitude",
    "L2: at Cumae the Sun's disk seemed to be diminished.",
    [lic(LV, "2.30.38.8.1", "Cumis solis orbis minui visus")], "narrator (reported prodigy)",
    [fork("any", "magnitude > 0 at Cumae, Sun up", "as L1-ECL", {"smag": [0.0, None]}, True),
     fork("noticed", "magnitude >= 0.5 at Cumae", "as L1-ECL", {"smag": [0.5, None]})]))
c.append(clue(S, "L2-DATE", "L2", "other", "narrative-order",
    "The prodigies were reported just as news of the Carthaginian breach came; the text "
    "goes on to the Ludi Apollinares of the same year (flooded circus).",
    [lic(LV, "2.30.38.8.1", "prodigia quoque nuntiata sub ipsam famam rebellionis"),
     lic(LV, "2.30.38.10.1", "ludi Apollinares")], "narrator",
    [season_none("no date for the prodigy is given", True),
     fork("before-ludi", "the eclipse precedes the Ludi Apollinares (Roman Quinctilis; "
          "Livy 37.4.4 puts the games at a.d. V Id. Quint.) of the same year, with the "
          "Roman offset free", "inference from narrative order",
          {"before_roman_date": "a.d. V Id. Quint.", "offset_days": None})]))
# L3
c.append(clue(S, "L3-ECL", "L3", "eclipse-solar", "magnitude",
    "L3: during the Ludi Apollinares, on a.d. V Id. Quint., in a clear sky, the daylight "
    "was darkened in daytime because the Moon had passed under the Sun's disk.",
    [lic(LV, "3.37.4.4.1", "caelo sereno interdiu obscurata lux est, cum luna sub orbem solis subisset")],
    "narrator",
    [fork("X4", "magnitude >= 0.60 at the observer, Sun up", "darkened daylight: the "
          "design's darkness-wording class X4", {"smag": [0.60, None]}, True),
     fork("any", "magnitude > 0", "Livy explains the cause, so it was an eclipse; the "
          "darkness may be overstated", {"smag": [0.0, None]}),
     fork("X3", "magnitude >= 0.95", "strong reading of 'obscurata lux'",
          {"smag": [0.95, None]})]))
c.append(clue(S, "L3-DATE", "L3", "other", "calendar-date",
    "Roman date a.d. V Id. Quint. (Roman 11 Quinctilis), during the Ludi Apollinares, "
    "when the consul set out for the war.",
    [lic(LV, "3.37.4.4.1", "ludis Apollinaribus, a. d. quintum idus Quinctiles")],
    "narrator", ROMAN_FREE("a.d. V Id. Quint. (11 Quinctilis)")))
c.append(clue(S, "L3-SITE", "L3", "site", "observer",
    "Not stated as such; the games and the consul's departure ('ab urbe est profectus', "
    "37.4.2) put the narrative at Rome.",
    [lic(LV, "3.37.4.2.1", "ab urbe est profectus"), lic(LV, "3.37.4.4.1", "ludis Apollinaribus")],
    "narrator",
    [fork("rome", "Rome (41.89N, 12.49E)", "the Ludi Apollinares were Roman games",
          {"site": {"lat": 41.89, "lon": 12.49}}, True),
     fork("italy-box", "anywhere in the Italy box", "the site is not named",
          {"site_box": ITALY_BOX}),
     fork("none", "anywhere", "sensitivity", {"site": None})]))
# L4
c.append(clue(S, "L4-DARK", "L4", "darkness", "daytime-darkness",
    "L4: a three-day supplication was decreed because darkness had come on in daylight "
    "between about the third and fourth hour. The text does not say eclipse.",
    [lic(LV, "3.38.36.4.1", "quod luce inter horam tertiam ferme et quartam tenebrae obortae fuerant")],
    "narrator (reported prodigy)",
    [fork("eclipse-hours", "a solar eclipse of magnitude >= 0.60 whose maximum falls in "
          "the 3rd-4th seasonal hour of the day (day = sunrise to sunset in 12 equal "
          "hours), +/- 1 h for 'ferme'", "darkness by day read as an eclipse; X4 for "
          "darkness wording", {"smag": [0.60, None], "seasonal_day_hours": [3, 4],
          "tol_h": 1.0, "relation": "maximum in window"}, True),
     fork("eclipse-any-hour", "a solar eclipse of magnitude >= 0.60, any hour", "keeps the "
          "eclipse reading, drops the hour", {"smag": [0.60, None]}),
     fork("not-eclipse", "not an eclipse (weather, smoke or dust); L4 undatable",
          "the text names no cause", {"exclude": True})]))
c.append(clue(S, "L4-SITE", "L4", "site", "observer",
    "Not stated. The expiation was at all the crossroads (of Rome) and the other prodigy "
    "in the same sentence is on the Aventine.",
    [lic(LV, "3.38.36.4.1", "in omnibus compitis", "in Aventino")], "narrator",
    [fork("rome", "Rome", "the expiation and the companion prodigy are Roman",
          {"site": {"lat": 41.89, "lon": 12.49}}, True),
     fork("italy-box", "anywhere in the Italy box", "the site is not named",
          {"site_box": ITALY_BOX}),
     fork("none", "anywhere", "sensitivity", {"site": None})]))
c.append(clue(S, "L4-DATE", "L4", "other", "report-time",
    "The supplication was decreed before the new magistrates left for their provinces; "
    "the consuls had entered office on the Ides of March (38.35.7).",
    [lic(LV, "3.38.36.4.1", "priusquam in provincias novi magistratus proficiscerentur"),
     lic(LV, "3.38.35.7.1", "consulatum idibus Martiis cum inissent")], "narrator",
    [season_none("the text dates the expiation, not the darkness", True),
     fork("near-ides-march", "the darkness lies within 120 days before the Roman Ides of "
          "March of the consular year, Roman offset free", "inference: the expiation "
          "followed the prodigy within months", {"before_roman_date": "Id. Mart.",
          "within_days": 120, "offset_days": None})]))
sets.append({
    "set_id": S, "role": "HARD CASE (reported, not pass/fail)",
    "texts": [{"text_file": "data/text/livy-lat.tsv",
               "local_keys": ["2.22.1.1.1", "2.22.1.4.1", "2.22.1.8.1", "2.22.1.9.1", "2.30.38.8.1",
                        "2.30.38.10.1", "3.37.4.2.1", "3.37.4.4.1", "3.38.35.7.1", "3.38.36.4.1"],
               "citation": "Livy 22.1.8-9, 30.38.8-10, 37.4.4, 38.36.4"}],
    "events": [{"event_id": "L1", "kind": "eclipse-solar", "ref": "22.1.9", "linked": False},
               {"event_id": "L1b", "kind": "other", "ref": "22.1.9", "linked": False},
               {"event_id": "L2", "kind": "eclipse-solar", "ref": "30.38.8", "linked": False},
               {"event_id": "L3", "kind": "eclipse-solar", "ref": "37.4.4", "linked": False},
               {"event_id": "L4", "kind": "darkness", "ref": "38.36.4", "linked": False}],
    "observer_place": [
        unstated(["L1", "L1b"], "unstated for the item; forks in L1-SITE (Arpi for L1b)"),
        place(["L2"], "Cumae", [lic(LV, "2.30.38.8.1", "Cumis")], {"lat": 40.85, "lon": 14.05}, COORD_NOTE),
        unstated(["L3"], "Rome by inference only; forks in L3-SITE"),
        unstated(["L4"], "Rome by inference only; forks in L4-SITE")],
    "window_years": 136, "anchor_event": None,
    "window_note": "The four notices are not linked by any interval the text states at "
                   "these passages; each is searched alone in its own 136-year window.",
    "clues": c})

# ------------------------------------------------------------------- write out
doc = {
    "schema": "odybench controls_real v1",
    "drafted": "2026-10-04",
    "status": "drafted blind from the local texts; to be frozen with data/prereg",
    "truth": "not in this file; see controls_real_truth.json, which the searcher must not read",
    "drafting_record": "docs/controls-real-drafting.md (explains every set and fork, and what the drafter had seen before drafting)",
    "conventions": {
        "years": "historical BC with astronomical year; proleptic Julian calendar; JD arithmetic only",
        "solar_magnitude": "smag = fraction of the Sun's diameter covered at the site, at maximum (NASA/Besselian convention)",
        "lunar_magnitude": "umag = umbral magnitude at greatest eclipse (fraction of the Moon's diameter inside the umbra); pmag = penumbral magnitude",
        "digit": "1 digit = 1/12 of the lunar diameter",
        "LAT": "local apparent solar time at the named site; 'midnight' in Ptolemy is apparent midnight",
        "seasonal_hours": "Greek and Roman hours of the day (night) are twelfths of the interval sunrise-sunset (sunset-sunrise); hour n runs from (n-1)/12 to n/12 of it",
        "watch": "a Roman vigilia is a quarter of the night (sunset to sunrise)",
        "sun_lon_deg": "apparent tropical ecliptic longitude of the Sun, of date; ranges [a, b] with a > b wrap through 0",
        "site_box": "the clue passes if it holds at some site inside the box (lat, lon ranges, degrees, east positive)",
        "attic_month": "month 1 begins at the first new moon after the summer solstice (secondary reconstruction); lunation_offset absorbs intercalation",
        "egyptian_calendar": "365-day wandering year, 12x30 + 5; night_index = 365*(Y-1) + 30*(M-1) + D for the night 'D into D+1'; JD(local midnight) = J_free + night_index",
        "roman_calendar": "a Roman date before 45 BC carries a free integer offset delta from the proleptic Julian date of the same name",
    },
    "policies": [
        "A feature the words do not state is not a clue; an implied feature is a fork whose options include 'none'.",
        "Primary option: the reading closest to the words, with no inference from narrative order or outside knowledge; where two sources for one event disagree, the primary option is the weakest reading compatible with both and each source alone is an alternative.",
        "Thresholds for darkness wording are the design's own eclipse classes (DESIGN 3.1: X3 >= 0.95, X4 >= 0.60); 0.5 for a crescent is geometry. No threshold was chosen to fit any known answer.",
        "Similes and lying tales are excluded as date carriers (none occurs in these passages).",
        "Year and day intervals enter only when the text states them (Ptolemy's Egyptian dates and day counts, Thucydides' war-years, Xenophon's year headings); no modern date enters.",
        "Coordinates are the drafter's modern placements of the places the text names; they are search inputs, not clues.",
    ],
    "window_semantics": "window_years is a width only. The harness, not the searcher, places the window so that the anchor event's accepted date falls at a uniformly random position inside it (as PC-S, DESIGN 4.2 step 3). Events marked linked: false are each searched in their own window.",
    "field_notes": "texts[].local_keys are row citations in the local file (the part of the row key after the edition id). licence_words, ref and text_file are parallel lists (one entry per quoted string). ref is the full row key in text_file. fork_options: exactly one option has primary: true; operational holds machine-readable parameters. Strings are copied from the local files by results/controls-real-drafting/build_controls_real.py, which checks each one.",
    "sets": sets,
}
for st in sets:
    for t in st["texts"]:
        stem = t["text_file"].split("/")[-1][:-4]
        for k in t["local_keys"]:
            if k not in rows(stem):
                raise SystemExit(f"{st['set_id']}: local key {k} not in {stem}")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
n = sum(len(s["clues"]) for s in sets)
print(f"wrote {OUT} : {len(sets)} sets, {n} clue rows")
