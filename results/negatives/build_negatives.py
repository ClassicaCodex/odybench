"""Build data/prereg/negatives.json: clean negative-control clue sets (and the
Iliad same-tradition comparison) for odybench.

Written 2026-10-04 for the negatives drafting task (docs/negatives-drafting.md).

Every licence-words fragment is located in the local text rows it cites
(data/text/*.tsv), and the exact original characters are copied into the JSON,
so no Greek or Latin is retyped. The script fails if a fragment is missing, if a
ref does not exist, if a pinned reading names an option that does not exist, or
if the output contains a calendar date or a BC/AD year (the clue file must hold
no positions). There is no truth file: these texts have no true date.

Run:  py results/negatives/build_negatives.py
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT = ROOT / "data" / "text"
OUT = ROOT / "data" / "prereg" / "negatives.json"

AEN = "virgil-aeneid-lat.tsv"
ARG = "apollonius-argonautica-grc.tsv"
QS = "quintus-smyrnaeus-grc.tsv"
VF = "valerius-flaccus-argonautica-lat.tsv"
IL = "iliad-grc.tsv"

# ---------------------------------------------------------------- text access
_cache = {}


def short(ref):
    m = re.match(r"urn:cts:[^:]+:(.*)", ref)
    if not m:
        return ref
    parts = m.group(1).split(".")
    for i, p in enumerate(parts):
        if "perseus" in p or "-grc" in p or "-lat" in p:
            return ".".join(parts[i + 1:])
    return m.group(1)


def rows(name):
    if name not in _cache:
        lst = []
        with open(TEXT / name, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if "\t" not in line:
                    continue
                k, t = line.split("\t", 1)
                lst.append((k, short(k), t))
        _cache[name] = lst
    return _cache[name]


def expand(name, spec):
    """'2.254-2.256' or '2.254' -> list of (fullkey, text)."""
    lst = rows(name)
    a, b = (spec.split("-") + [None])[:2] if "-" in spec else (spec, spec)
    if b is None:
        b = a
    idx = {s: i for i, (_, s, _) in enumerate(lst)}
    if a not in idx or b not in idx:
        raise SystemExit(f"ref not found: {name} {spec}")
    i, j = idx[a], idx[b]
    if j < i:
        raise SystemExit(f"bad range: {name} {spec}")
    return [(lst[k][0], lst[k][2]) for k in range(i, j + 1)]


APOS = set("'ʼ’᾽ʹ`´᾿")


def norm_map(s):
    out, idx = [], []
    for j, c in enumerate(s):
        for d in unicodedata.normalize("NFD", c):
            if unicodedata.category(d) == "Mn":
                continue
            d = d.lower()
            if d == "ς":
                d = "σ"
            if d in APOS:
                d = "'"
            if d.isspace():
                d = " "
                if out and out[-1] == " ":
                    continue
            out.append(d)
            idx.append(j)
    return "".join(out), idx


def norm(s):
    return norm_map(s)[0].strip()


def locate(text, pat):
    n, idx = norm_map(text)
    p = norm(pat)
    k = n.find(p)
    if k < 0:
        return None
    a = idx[k]
    b = idx[k + len(p) - 1] + 1
    while b < len(text) and unicodedata.category(text[b]) == "Mn":
        b += 1
    return text[a:b]


def licence(name, specs, frags):
    keys, texts = [], []
    for sp in specs:
        for k, t in expand(name, sp):
            keys.append(k)
            texts.append(t)
    joined = " ".join(texts)
    got = []
    for fr in frags:
        ex = locate(joined, fr)
        if ex is None:
            raise SystemExit(f"licence words not found in {name} {specs}: {fr!r}")
        got.append(ex)
    return keys, " … ".join(got)


# ---------------------------------------------------------------- fork menus
def F4(day):
    """Morning-star menu, DESIGN 3.4 F4."""
    return [
        dict(option="lead60", operational=f"Venus rises at least 60 min before the Sun on {day} (rise lead; Sun h0 -0.8333 deg, Venus h0 -0.5667 deg, as in T0b)",
             justification="the morning star taken as Venus; lowest lead threshold of the Odyssey's F4 menu [DESIGN 3.4 F4]"),
        dict(option="lead90", operational=f"Venus rises at least 90 min before the Sun on {day}",
             justification="B&M's own threshold for Od. 13.93-95 [DESIGN 1.1, criterion V]"),
        dict(option="lead120", operational=f"Venus rises at least 120 min before the Sun on {day}",
             justification="strict end of the F4 menu [DESIGN 3.4 F4]"),
        dict(option="vis7", operational=f"Venus visible as a morning object on {day} (arcus visionis 7 deg)",
             justification="the words name a morning star, not a lead; visibility is the least-inference reading [vis 1.2]"),
        dict(option="herald", operational=f"some bright dawn herald visible before sunrise on {day}: Venus, Jupiter, Sirius, or Mars at magnitude -1 or brighter (arcus visionis per body as in DESIGN 3.5)",
             justification="the text does not say which star; the Odyssey's F4 menu allows any bright herald [DESIGN 3.4 F4]"),
        dict(option="none", operational="clue dropped",
             justification="the dawn star is a traditional time-marker for the last hour of night (Od. 13.93-95 and Il. 23.226-228 use the same device) [txt 5.7]"),
    ]


def F4eve(day):
    """Evening-star menu: the mirror of F4."""
    return [
        dict(option="lag60", operational=f"Venus sets at least 60 min after the Sun on {day}",
             justification="the evening star taken as Venus; mirror of the F4 lead thresholds"),
        dict(option="lag90", operational=f"Venus sets at least 90 min after the Sun on {day}",
             justification="mirror of B&M's 90-min threshold"),
        dict(option="lag120", operational=f"Venus sets at least 120 min after the Sun on {day}",
             justification="strict end of the mirrored menu"),
        dict(option="vis7", operational=f"Venus visible as an evening object on {day} (arcus visionis 7 deg)",
             justification="the words name an evening star; visibility is the least-inference reading"),
        dict(option="herald", operational=f"some bright evening object visible in the evening twilight of {day}: Venus, Jupiter, Sirius, or Mars at magnitude -1 or brighter",
             justification="the text does not say which star"),
        dict(option="none", operational="clue dropped",
             justification="the evening star is a stock marker of nightfall (the star of the fold / of evening)"),
    ]


def F5(day):
    """Hermes = Mercury menu, DESIGN 3.4 F5 (5 events x 3 tolerances x 2 visibility rules + none = 31)."""
    tail = "; t in {1, 2, 3} days; with or without Mercury visible that morning (arcus visionis 10 deg)"
    j = "B&M's rule (Hermes' journey = the motion of Mercury) applied unchanged to this Hermes passage [DESIGN 1.1, criterion M; B&M call it conjectural]"
    return [
        dict(option="mwra", operational=f"Mercury's maximum western rise azimuth within +-t days of {day}" + tail, justification=j + "; B&M's own event"),
        dict(option="gwe", operational=f"Mercury's greatest western elongation within +-t days of {day}" + tail, justification=j + "; one of the three events B&M name [DESIGN 3.4 F5]"),
        dict(option="station", operational=f"a Mercury station that ends retrograde motion (morning station) within +-t days of {day}" + tail, justification=j + "; one of the three events B&M name"),
        dict(option="any3", operational=f"any of the three events above within +-t days of {day}" + tail, justification=j),
        dict(option="firstvis", operational=f"Mercury's first morning visibility (arcus visionis 10 deg) within +-t days of {day}; t in {{1, 2, 3}} days",
             justification=j + "; B&M also speak of Mercury's heliacal rising [txt 2.1]"),
        dict(option="none", operational="clue dropped",
             justification="the passage has no light, star, rising or turning vocabulary; Hermes is the messenger god [txt 5.9 for the Odyssey's version]"),
    ]


NONE = lambda why: dict(option="none", operational="clue dropped", justification=why)


def O(opt, op, why):
    return dict(option=opt, operational=op, justification=why)


SITE_NOTE = "coordinates are the drafter's identification of the named place (Wikipedia coordinates fetched 2026-10-04, results/negatives/coords*.out.json), not text"

# ---------------------------------------------------------------- sets
WIN = [136, 251]
DAYCONV = ("Day n is the local civil date (LMT at the set's site) of the daylight of that day; Night n runs from sunset of Day n to "
           "sunrise of Day n+1; Dawn n+1 is the morning twilight that ends Night n. Offsets count days, not 24-hour periods.")


def place(name, file, spec, frags, lat, lon, src=SITE_NOTE):
    keys, words = licence(file, [spec], frags)
    return dict(place=name, words=words, ref=keys, text_file=file, lat=lat, lon=lon, coord_source=src)


SETS = []
CLUES = []
EXCLUDED = []


def clue(set_, cid, kind, statement, file, specs, frags, level, forks=(), notes=""):
    keys, words = licence(file, specs, frags)
    CLUES.append(dict(set=set_, clue_id=cid, kind=kind, statement=statement, licence_words=words,
                      ref=keys, text_file=file, fork_options=list(forks), narrative_level=level, notes=notes))


def excl(file, spec, level, reason):
    keys = [k for k, _ in expand(file, spec)]
    EXCLUDED.append(dict(ref=keys, text_file=file, narrative_level=level, reason=reason))


# ============================================================ AEN-TROY
SETS.append(dict(
    set="AEN-TROY", role="negative", searchable=True,
    text="Virgil, Aeneid 2 (Latin; Aeneas narrates the last night of Troy to Dido)", text_file=AEN, edition_id=1827,
    day0="Day 0 is the Trojans' festal day at whose end the Greek fleet sails back from Tenedos; Night 0 is the night of the sack; Dawn +1 is Lucifer's rising.",
    day_convention=DAYCONV,
    observer_places=[
        place("Troy (Ilium), the city and the mound of ancient Ceres outside it", AEN, "2.742-2.743", ["tumulum antiquae Cereris sedemque sacratam venimus"], 39.9575, 26.2389),
        place("Tenedos (the Greek fleet's departure point)", AEN, "2.255", ["a Tenedo"], 39.8219, 26.0289),
        place("Mount Ida (the ridge over which Lucifer rises, as seen from Troy)", AEN, "2.801", ["iugis summae", "Idae"], 39.7, 26.8333),
    ],
    window_width_years=WIN,
    pinned_readings={
        "R-i (moon up)": {"AEN-TROY-02": "i-b", "AEN-TROY-04": "a", "AEN-TROY-05": "none", "AEN-TROY-07": "vis7"},
        "R-ii (silent moon = conjunction; 2.340 read figuratively)": {"AEN-TROY-02": "ii-a", "AEN-TROY-04": "none", "AEN-TROY-05": "none", "AEN-TROY-07": "vis7"},
        "R-ii-literal (conjunction, and 2.340 kept: contradictory)": {"AEN-TROY-02": "ii-a", "AEN-TROY-04": "a", "AEN-TROY-05": "none", "AEN-TROY-07": "vis7"},
        "BM-analogue": {"AEN-TROY-02": "ii-a", "AEN-TROY-04": "none", "AEN-TROY-05": "conj", "AEN-TROY-07": "lead90"},
    },
    odyssey_slots={
        "day0_phase": dict(status="fork", clue_ids=["AEN-TROY-02"], note="only reading ii of 2.255 (silens luna = conjunction) gives the Odyssey's Day-0 conjunction; reading i puts a lit moon in the sky instead"),
        "season_stars": dict(status="empty", clue_ids=[], note="no star or season statement in the night of the sack"),
        "morning_star": dict(status="text", clue_ids=["AEN-TROY-07"], note="Lucifer at Dawn +1, after the anchor (the Odyssey's is five days before it)"),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note="no Hermes/Mercury in book 2"),
        "darkness_eclipse": dict(status="empty", clue_ids=[], note="'nox atra' (2.360) and 'caecam noctem' (2.397) describe the night, not a darkening; no eclipse-compatible darkness statement"),
        "other": dict(status="fork", clue_ids=["AEN-TROY-05"], note="Day 0 is a day of public celebration, like Apollo's feast on the Odyssey's Day 0 (Od. 20.156)"),
    },
    notes="Both readings of 2.255 are pinned, as critique-design issue 15 requires. Under reading ii the moonlight of 2.340 contradicts the conjunction; R-ii drops 2.340, R-ii-literal keeps it.",
))

clue("AEN-TROY", "AEN-TROY-01", "time-of-day",
     "Nightfall ends Day 0; the Trojans fall asleep on the walls. Night 0 begins.",
     AEN, ["2.250-2.253"], ["Vertitur interea caelum et ruit oceano nox", "fusi per moenia Teucri conticuere, sopor fessos complectitur artus"],
     "character speech", notes="Aeneas' narrative to Dido (true within the fiction; the Odyssey's level E). Fixes the sailing of row 02 in Night 0.")

clue("AEN-TROY", "AEN-TROY-02", "moon-phase",
     "In the first part of Night 0 the Greek fleet sails from Tenedos 'through the friendly silences of the silent moon'.",
     AEN, ["2.254-2.256"], ["et iam Argiva phalanx instructis navibus ibat", "a Tenedo tacitae per amica silentia lunae"],
     "character speech",
     forks=[
         O("i-a", "the Moon is above the horizon at some instant between the end of evening nautical twilight and local midnight of Night 0, with illuminated fraction >= 0.5",
           "reading i: 'amica' lunar light guides the fleet; the >= 0.5 threshold is DESIGN NC2's addition, not in the words"),
         O("i-b", "the Moon is above the horizon at some instant between the end of evening nautical twilight and local midnight of Night 0 (any phase)",
           "reading i without the phase threshold the words do not give"),
         O("ii-a", "Day 0 is the date of conjunction (LMT at Troy)",
           "reading ii: 'silens luna' is the Moon at conjunction; Pliny NH 16.190 says the day of coitus is called by some interlunium, by others the day of the silent moon [pliny-nh-lat.tsv 16.39.2]; Pliny contrasts 'silente luna' with 'plena' [local key 18.31.3] and pairs it with eclipses [local key 28.7.3]"),
         O("ii-b", "conjunction falls within +-1.5 days of local midnight of Night 0 (the Moon invisible: interlunium)",
           "reading ii taken as the days of invisibility round conjunction rather than one date"),
         NONE("'silentia' read as the stillness of night and the Moon as an attribute; the line states no phase"),
     ],
     notes="The fork that decides whether this negative has the Odyssey's Day-0 anchor. The ancient commentary on the line (Servius) is not in the library and was not read.")

clue("AEN-TROY", "AEN-TROY-03", "time-of-day",
     "The royal ship raises the fire signal and the men in the horse come out; Hector's ghost appears to Aeneas at the hour of first sleep. The sack fills the rest of Night 0.",
     AEN, ["2.256-2.257", "2.268-2.270"], ["flammas cum regia puppis extulerat", "Tempus erat, quo prima quies mortalibus aegris incipit"],
     "character speech", notes="Time-of-night only; orders rows 02 and 04 within Night 0.")

clue("AEN-TROY", "AEN-TROY-04", "moon-phase",
     "During the fighting of Night 0 Rhipeus, Epytus, Hypanis and Dymas join Aeneas, 'met by the moon'.",
     AEN, ["2.339-2.340"], ["Addunt se socios Rhipeus et maximus armis", "Epytus oblati per lunam"],
     "character speech",
     forks=[
         O("a", "the Moon is above the horizon at some instant between the end of evening nautical twilight and the start of morning nautical twilight of Night 0",
           "'per lunam': they appear by moonlight"),
         O("b", "as a, with illuminated fraction >= 0.5 at that instant",
           "they are recognised by the light, which a thin crescent would not give; the threshold is the drafter's"),
         NONE("'per lunam' read as 'by night'; the same night is 'nox atra' (2.360) and 'caeca' (2.397)"),
     ],
     notes="Incompatible with reading ii of row 02 (a Moon at conjunction is not up at night). See pinned readings.")

clue("AEN-TROY", "AEN-TROY-05", "other",
     "Day 0, the last day of Troy, is a day of public celebration: the Trojans deck the shrines with festal foliage.",
     AEN, ["2.248-2.249"], ["quibus ultimus esset ille dies, festa velamus fronde per urbem"],
     "character speech",
     forks=[
         O("conj", "Day 0 is a conjunction date (LMT at Troy)",
           "analogy only: B&M read Apollo's feast on the Odyssey's Day 0 as a new-moon feast through a scholion citing Philochorus [txt 5.3]; no source ties this celebration to the Moon"),
         NONE("the text gives the celebration a cause (the Greeks' apparent departure), not a calendar date"),
     ])

clue("AEN-TROY", "AEN-TROY-06", "interval",
     "Lucifer's rising (row 07) comes at the end of Night 0, after the night is spent: it is Dawn +1.",
     AEN, ["2.795", "2.801"], ["Sic demum socios consumpta nocte reviso", "Iamque"],
     "character speech")

clue("AEN-TROY", "AEN-TROY-07", "planet",
     "At Dawn +1 Lucifer was rising over the ridges of highest Ida and leading in the day, seen by Aeneas at the mound of Ceres outside Troy.",
     AEN, ["2.801-2.802"], ["Iamque iugis summae surgebat Lucifer Idae ducebatque diem"],
     "character speech",
     forks=F4("Dawn +1") + [
         O("ida", "Venus's rising azimuth on Dawn +1, seen from Troy, lies within +-15 deg (variant +-30 deg) of the bearing of the Ida summit, 119 deg [me: great-circle bearing from the coordinates in observer_places]",
           "'iugis ... Idae' puts the rising over Ida; the bearing and its tolerance are the drafter's geography, not the text. At 40 deg N an azimuth of 119 deg needs a declination near -22 deg"),
     ],
     notes="'ida' is a rider that can be combined with any non-none F4 option. Latin Lucifer is the planet Venus as morning star, so 'vis7' is the least-inference reading.")

excl(AEN, "2.8-2.9", "character speech", "frame time at Carthage (setting stars at Dido's banquet), not the night of Troy; 2.9's second half repeats 4.81")
excl(AEN, "2.108-2.113", "lying tale", "Sinon's lying tale (winter storms kept the Greeks from sailing)")
excl(AEN, "2.135", "lying tale", "Sinon's lying tale (hid in a marsh through the night)")
excl(AEN, "2.355-2.358", "simile", "simile (wolves in a black mist)")
excl(AEN, "2.692-2.698", "character speech", "a falling star with a trail (portent): not computable")

# ============================================================ AEN-CRETE
SETS.append(dict(
    set="AEN-CRETE", role="negative", searchable=True,
    text="Virgil, Aeneid 3.121-3.152 (the settlement on Crete; Aeneas narrating)", text_file=AEN, edition_id=1827,
    day0="Night 0 is the night of the Penates' vision by full moonlight; the Sirius season precedes it by an unstated interval.",
    day_convention=DAYCONV,
    observer_places=[place("Crete, the town Aeneas founds and calls Pergamea (its location is not given)", AEN, "3.131-3.133",
                           ["antiquis Curetum adlabimur oris", "Pergameamque voco"], 35.21, 24.91,
                           "central Crete chosen by the drafter as a representative point; the text names the island and the town only")],
    window_width_years=WIN,
    pinned_readings={"literal": {"AEN-CRETE-01": "a60", "AEN-CRETE-02": "a"}, "BM-analogue": {"AEN-CRETE-01": "a60", "AEN-CRETE-02": "a"}},
    odyssey_slots={
        "day0_phase": dict(status="text", clue_ids=["AEN-CRETE-02"], note="full moon on Night 0: the opposite phase to the Odyssey's anchor"),
        "season_stars": dict(status="text", clue_ids=["AEN-CRETE-01"], note="Sirius' scorching season, interval to Night 0 unstated"),
        "morning_star": dict(status="empty", clue_ids=[], note=""),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note=""),
        "darkness_eclipse": dict(status="empty", clue_ids=[], note=""),
    },
    notes="Two clues only; a season plus a phase. Expected to have many survivors.",
))

clue("AEN-CRETE", "AEN-CRETE-01", "season",
     "Some time before Night 0 (interval unstated) a plague year strikes the new settlement: Sirius scorches the barren fields and the grass dries up.",
     AEN, ["3.137-3.142"], ["letifer annus", "tum sterilis exurere Sirius agros", "arebant herbae"],
     "character speech",
     forks=[
         O("a60", "Night 0 lies between Sirius' heliacal rising (first morning visibility at the site) and 60 days after it",
           "'Sirius exurere agros' names the dog-star season; the interval to the vision night is unstated ('tum' ... 'Nox erat'), so the window width is the drafter's"),
         O("a30", "as a60 with 30 days", "narrower variant of the same reading"),
         NONE("the plague-year topos; no stated interval ties it to Night 0"),
     ])

clue("AEN-CRETE", "AEN-CRETE-02", "moon-phase",
     "On Night 0 the Penates appear to the sleeping Aeneas, clear in the light the full moon pours through the windows.",
     AEN, ["3.147", "3.150-3.152"], ["Nox erat", "visi ante oculos adstare iacentis in somnis, multo manifesti lumine, qua se plena per insertas fundebat luna fenestras"],
     "character speech",
     forks=[
         O("a", "opposition falls within +-1 day of local midnight of Night 0 and the Moon is above the horizon at some instant of Night 0",
           "'plena luna'"),
         O("b", "illuminated fraction >= 0.9 at local midnight of Night 0 and the Moon above the horizon at some instant of Night 0",
           "a looser 'full' that does not require opposition to the day"),
         NONE("the light belongs to the dream ('in somnis'), not to the night's sky"),
     ])

# ============================================================ AEN-ITALY
SETS.append(dict(
    set="AEN-ITALY", role="negative", searchable=True,
    text="Virgil, Aeneid 3.506-3.524 (Palinurus reads the stars before the crossing to Italy)", text_file=AEN, edition_id=1827,
    day0="Day 0 is the day the fleet beaches near the Ceraunian mountains; Night 0 is Palinurus' night; Dawn +1 shows Italy.",
    day_convention=DAYCONV,
    observer_places=[place("the shore by the Ceraunian mountains (Epirus)", AEN, "3.506-3.509", ["vicina Ceraunia iuxta", "sternimur optatae gremio telluris ad undam"],
                           40.1986, 19.5917, "Llogara Pass (Wikipedia, fetched 2026-10-04) taken by the drafter as a point on the Ceraunian range")],
    window_width_years=WIN,
    pinned_readings={"literal": {"AEN-ITALY-02": "a5"}, "BM-analogue": {"AEN-ITALY-02": "a2"}},
    odyssey_slots={
        "day0_phase": dict(status="empty", clue_ids=[], note=""),
        "season_stars": dict(status="text", clue_ids=["AEN-ITALY-02"], note="the closest analogue of Od. 5.270-275: a steersman's star list, itself a repeated formula (3.516 = 1.744, as Od. 5.273-275 = Il. 18.487-489)"),
        "morning_star": dict(status="empty", clue_ids=[], note="3.521 is dawn with the stars put to flight; no morning star"),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note=""),
        "darkness_eclipse": dict(status="empty", clue_ids=[], note=""),
    },
    notes="A season-only set: it can date a season, not a year.",
))

clue("AEN-ITALY", "AEN-ITALY-01", "time-of-day",
     "The Sun sets at the end of Day 0 as the fleet beaches; the crews sleep.",
     AEN, ["3.508-3.511"], ["Sol ruit interea et montes umbrantur opaci", "fessos sopor inrigat artus"], "character speech")

clue("AEN-ITALY", "AEN-ITALY-02", "star",
     "Before local midnight of Night 0 Palinurus rises and notes all the gliding stars: Arcturus, the rainy Hyades, the twin Triones and Orion armed with gold; the sky is clear.",
     AEN, ["3.512-3.518"], ["Necdum orbem medium Nox horis acta subibat", "sidera cuncta notat tacito labentia caelo, Arcturum pluviasque Hyadas geminosque Triones, armatumque auro circumspicit Oriona", "caelo constare sereno"],
     "character speech",
     forks=[
         O("a5", "each of Arcturus, Aldebaran (Hyades), Betelgeuse and Rigel (Orion) is >= 5 deg above the horizon at some instant between the end of evening nautical twilight and local midnight of Night 0 (the Triones, the Bears, are circumpolar)",
           "'necdum orbem medium' sets the before-midnight window; 'notat ... circumspicit' means he sees each star"),
         O("a2", "as a5 with >= 2 deg", "the Odyssey's F3 altitude [DESIGN 3.4 F3]"),
         O("b5", "all four >= 5 deg at one and the same instant in that window", "one survey of the sky"),
         NONE("3.516 repeats 1.744 word for word (Iopas' song of the sky at Carthage): a formula, not a night's observation"),
     ])

clue("AEN-ITALY", "AEN-ITALY-03", "time-of-day",
     "At Dawn +1, as the stars flee, they sight the low hills of Italy.",
     AEN, ["3.521-3.523"], ["Iamque rubescebat stellis Aurora fugatis", "humilemque videmus Italiam"], "character speech")

# ============================================================ AEN-ETNA
SETS.append(dict(
    set="AEN-ETNA", role="negative", searchable=True,
    text="Virgil, Aeneid 3.568-3.654 (the night under Etna and Achaemenides)", text_file=AEN, edition_id=1827,
    day0="Day 0 is the day the fleet reaches the Cyclopes' shore at sunset; Night 0 is the cloudy night; Dawn +1 rises 'with the first Eous'; Achaemenides speaks on Day +1.",
    day_convention=DAYCONV,
    observer_places=[place("the Cyclopes' harbour under Etna (Sicily)", AEN, "3.569-3.571", ["Cyclopum adlabimur oris", "iuxta tonat Aetna"],
                           37.5636, 15.1614, "Aci Trezza (Wikipedia, fetched 2026-10-04), the drafter's point on the Etna coast")],
    window_width_years=WIN,
    pinned_readings={"literal": {"AEN-ETNA-02": "a", "AEN-ETNA-03": "vis7", "AEN-ETNA-04": "a"},
                     "BM-analogue": {"AEN-ETNA-02": "a", "AEN-ETNA-03": "lead90", "AEN-ETNA-04": "a"}},
    odyssey_slots={
        "day0_phase": dict(status="text", clue_ids=["AEN-ETNA-02", "AEN-ETNA-04"], note="a Moon up at midnight and waxing on Day +1: a phase constraint, not a conjunction"),
        "season_stars": dict(status="empty", clue_ids=[], note=""),
        "morning_star": dict(status="fork", clue_ids=["AEN-ETNA-03"], note="'primo Eoo' at Dawn +1, if Eous is the morning star"),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note=""),
        "darkness_eclipse": dict(status="empty", clue_ids=[], note="Night 0 is starless, but the text gives cloud as the cause"),
    },
    notes="The richest Odyssey-shaped Aeneid set: a night with a lunar statement, a morning star next dawn and a phase statement the next day.",
))

clue("AEN-ETNA", "AEN-ETNA-01", "time-of-day",
     "The wind drops with the Sun at the end of Day 0 and the fleet drifts onto the Cyclopes' shore.",
     AEN, ["3.568-3.569"], ["Interea fessos ventus cum sole reliquit", "Cyclopum adlabimur oris"], "character speech")

clue("AEN-ETNA", "AEN-ETNA-02", "moon-phase",
     "On Night 0 no stars were visible and cloud covered the sky; 'the dead of night held the Moon in a cloud'.",
     AEN, ["3.583", "3.585-3.587"], ["Noctem illam", "neque erant astrorum ignes", "obscuro sed nubila caelo, et lunam in nimbo nox intempesta tenebat"],
     "character speech",
     forks=[
         O("a", "the Moon is above the horizon at local midnight of Night 0", "'nox intempesta' is the dead of night; the Moon is there, behind cloud"),
         O("b", "the Moon is above the horizon at some instant of Night 0", "looser timing"),
         NONE("the passage describes a lightless night; the Moon is named only as hidden"),
     ])

clue("AEN-ETNA", "AEN-ETNA-03", "planet",
     "Dawn +1 was rising 'with the first Eous', and Aurora had driven the damp shadow from the sky.",
     AEN, ["3.588-3.589"], ["Postera iamque dies primo surgebat Eoo", "umentemque Aurora polo dimoverat umbram"],
     "character speech",
     forks=F4("Dawn +1")[:-1] + [NONE("'Eous' read as the dawn or the east; 3.589 repeats 4.7, a dawn formula")],
     notes="Eous can name the morning star or the dawn; the fork carries both.")

clue("AEN-ETNA", "AEN-ETNA-04", "moon-phase",
     "On Day +1 Achaemenides, a Greek left behind, says that the horns of the third moon are now filling with light since he began living in the woods.",
     AEN, ["3.645-3.647"], ["Tertia iam lunae se cornua lumine complent, cum vitam in silvis inter deserta ferarum lustra domosque traho"],
     "character speech",
     forks=[
         O("a", "the Moon is waxing on Day +1 (between conjunction and opposition)", "'se cornua lumine complent' in the present: the horns are filling now"),
         O("b", "opposition falls within +-2 days of Day +1", "'filling the horns with light' read as the disc closing to full"),
         O("c", "no phase constraint on Day +1 (the line counts about three lunations since an event in another story)", "'tertia' counts months; the start event is not in this set"),
         NONE("dropped"),
     ],
     notes="Achaemenides' speech within Aeneas' narrative. He is a Greek suppliant like Sinon, but the poem presents his account as true.")

excl(AEN, "3.195-3.204", "character speech", "darkness of three days and three starless nights at sea, from storm cloud ('involvere diem nimbi', 'caeca caligine'); weather, kept out of the darkness slot")
excl(AEN, "3.284-3.285", "character speech", "the year comes round and winter roughens the sea at Actium; season only, no stated interval to any other sky clue")
excl(AEN, "3.8-3.9", "character speech", "the departure 'as summer had scarcely begun'; no stated interval to the night of Troy, so it constrains nothing")

# ============================================================ AEN-CARTHAGE (beyond the named books)
SETS.append(dict(
    set="AEN-CARTHAGE", role="negative", searchable=True,
    text="Virgil, Aeneid 4 (Mercury's descent and Aeneas' night departure from Carthage), with the year count of 1.755-1.756", text_file=AEN, edition_id=1827,
    day0="Night 0 is the night Mercury appears to Aeneas in sleep and the fleet leaves; Dawn +1 shows Dido the empty harbour. Day M1, Mercury's descent, lies an unstated number of days before Day 0.",
    day_convention=DAYCONV,
    observer_places=[place("Carthage", AEN, "4.265", ["Tu nunc Karthaginis altae"], 36.8528, 10.3233)],
    window_width_years=WIN,
    pinned_readings={"literal": {"AEN-CARTHAGE-01": "none", "AEN-CARTHAGE-02": "free30", "AEN-CARTHAGE-03": "a", "AEN-CARTHAGE-05": "none", "AEN-CARTHAGE-07": "a"},
                     "BM-analogue": {"AEN-CARTHAGE-01": "mwra", "AEN-CARTHAGE-02": "free30", "AEN-CARTHAGE-03": "a", "AEN-CARTHAGE-05": "none", "AEN-CARTHAGE-07": "a"}},
    odyssey_slots={
        "day0_phase": dict(status="empty", clue_ids=[], note=""),
        "season_stars": dict(status="text", clue_ids=["AEN-CARTHAGE-03"], note="'hiberno sidere': a season named by a star, without the star's name"),
        "morning_star": dict(status="empty", clue_ids=[], note=""),
        "mercury_turning_point": dict(status="text", clue_ids=["AEN-CARTHAGE-01", "AEN-CARTHAGE-05"], note="Virgil's rewriting of Od. 5.43-54 (sandals, wand, a seabird skimming the waves); the only clean negative with a Hermes slot. Its interval to Day 0 is unstated"),
        "darkness_eclipse": dict(status="empty", clue_ids=[], note=""),
    },
    notes="Outside the books the task named (2-3). Added because it is the one clean negative where B&M's Hermes = Mercury rule can be applied to a Hermes journey written in imitation of the Odyssey's. Row 07 links it to AEN-TROY by a year count the text states.",
))

clue("AEN-CARTHAGE", "AEN-CARTHAGE-01", "planet",
     "On Day M1 Mercury binds on his golden sandals, takes his wand, flies past Atlas and drops to the sea like a bird skimming low over the water, to Carthage.",
     AEN, ["4.239-4.242", "4.252-4.255"], ["pedibus talaria nectit aurea", "tum virgam capit", "Hic primum paribus nitens Cyllenius alis constitit", "misit, avi similis, quae circum litora, circum piscosos scopulos humilis volat aequora iuxta"],
     "narrator", forks=F5("Day M1"),
     notes="The model is Od. 5.43-54 (Hermes ties on his sandals, takes his wand, skims the waves like a gull).")

clue("AEN-CARTHAGE", "AEN-CARTHAGE-02", "interval",
     "Between Day M1 and Night 0 Aeneas has the fleet readied in secret, Dido confronts him, the Trojans work on the ships and Dido prepares her rites: the number of days is not stated.",
     AEN, ["4.288-4.291", "4.397-4.398"], ["Mnesthea Sergestumque vocat", "classem aptent taciti", "Tum vero Teucri incumbunt, et litore celsas deducunt toto naves"],
     "narrator",
     forks=[O("free30", "Day M1 lies 1 to 30 days before Day 0 (the upper bound is the drafter's)", "the text gives no count; the events need at least a day"),
            NONE("no interval: row 01 is unlinked")])

clue("AEN-CARTHAGE", "AEN-CARTHAGE-03", "season",
     "Between Day M1 and Night 0 Dido says Aeneas is readying his fleet under the wintry star, hurrying to sea in the midst of the north winds.",
     AEN, ["4.309-4.310"], ["Quin etiam hiberno moliris sidere classem, et mediis properas aquilonibus ire per altum"],
     "character speech",
     forks=[O("a", "Night 0 falls when the Sun's ecliptic longitude is between 225 and 315 deg (winter solstice +-45 days)", "'hiberno sidere': winter; the width is the drafter's"),
            O("b", "Night 0 falls between the autumn equinox and the vernal equinox", "the whole closed sailing season"),
            NONE("Dido's reproach; 'hiberno sidere' as rhetoric")])

clue("AEN-CARTHAGE", "AEN-CARTHAGE-04", "time-of-day",
     "Night 0: midnight, the stars in mid-course; all creatures sleep except Dido.",
     AEN, ["4.522-4.524"], ["Nox erat", "cum medio volvuntur sidera lapsu"], "narrator")

clue("AEN-CARTHAGE", "AEN-CARTHAGE-05", "planet",
     "Later in Night 0 Mercury appears again to the sleeping Aeneas on his ship, urges him to flee before dawn, and vanishes into the black night.",
     AEN, ["4.554-4.558", "4.570"], ["Aeneas celsa in puppi", "carpebat somnos", "Huic se forma dei voltu redeuntis eodem obtulit in somnis", "omnia Mercurio similis", "nocti se immiscuit atrae"],
     "narrator", forks=F5("Night 0 (the date of Day 0)")[:-1] + [NONE("a dream apparition, not a journey")])

clue("AEN-CARTHAGE", "AEN-CARTHAGE-06", "time-of-day",
     "The fleet leaves at once; at Dawn +1 Dido sees the harbour empty.",
     AEN, ["4.584-4.587"], ["Et iam prima novo spargebat lumine terras Tithoni croceum linquens Aurora cubile", "classem procedere velis"], "narrator")

clue("AEN-CARTHAGE", "AEN-CARTHAGE-07", "interval",
     "When Aeneas reaches Carthage (in the summer before Night 0), Dido says the seventh summer is carrying him in his wandering since Troy.",
     AEN, ["1.755-1.756"], ["nam te iam septima portat omnibus errantem terris et fluctibus aestas"],
     "character speech",
     forks=[O("a", "Night 0 of AEN-CARTHAGE falls 6 to 8 years after Night 0 of AEN-TROY", "'septima aestas' gives the count; +-1 year covers inclusive or exclusive counting and the half-year from that summer to the winter departure"),
            NONE("a round number; Iris, disguised, repeats 'the seventh summer' a year later (5.626), so the poem's count is not exact")],
     notes="The only stated year interval between two Aeneid sets. It allows AEN-TROY and AEN-CARTHAGE to be run as one linked set.")

excl(AEN, "4.52", "character speech", "Anna: 'while winter and watery Orion rage at sea'; season on a day with no stated interval to Day M1 or Day 0")
excl(AEN, "4.80-4.81", "narrator", "habitual nights (iterative), not one night; 4.81's second half repeats 2.9")
excl(AEN, "4.193", "lying tale", "Fama's report, true and false mixed (4.190)")
excl(AEN, "5.626", "lying tale", "Iris disguised as Beroe")

# ============================================================ ARG-CIUS
SETS.append(dict(
    set="ARG-CIUS", role="negative", searchable=True,
    text="Apollonius, Argonautica 1.1012-1.1283 (from the night battle at Cyzicus to the loss of Hylas and Heracles at Cius)", text_file=ARG, edition_id=1,
    day0="Day 0 is the day the Argo reaches Cius at supper-time; Night 0 is the full-moon night of Hylas; Dawn +1 is the morning star and the departure.",
    day_convention=DAYCONV,
    observer_places=[
        place("Cius, by Mount Arganthonios and the mouth of the Cius river", ARG, "1.1177-1.1178", ["Κιανίδος ἤθεα γαίης", "Ἀργανθώνειον ὄρος προχοάς τε Κίοιο"], 40.4325, 29.1564),
        place("Cyzicus, land of the Doliones (Night -17)", ARG, "1.1018", ["ἐυξείνοισι Δολίοσιν"], 40.3878, 27.8706),
    ],
    window_width_years=WIN,
    pinned_readings={"literal": {"ARG-CIUS-02": "a", "ARG-CIUS-03": "vis7", "ARG-CIUS-05": "none", "ARG-CIUS-06": "n17", "ARG-CIUS-07": "none"},
                     "BM-analogue": {"ARG-CIUS-02": "a", "ARG-CIUS-03": "lead90", "ARG-CIUS-05": "a", "ARG-CIUS-06": "n17", "ARG-CIUS-07": "b"}},
    odyssey_slots={
        "day0_phase": dict(status="text", clue_ids=["ARG-CIUS-02"], note="full moon on Night 0: the opposite phase to the Odyssey's anchor"),
        "season_stars": dict(status="fork", clue_ids=["ARG-CIUS-07"], note="only through the halcyon (a bird, not a star) on Night -2"),
        "morning_star": dict(status="text", clue_ids=["ARG-CIUS-03"], note="Dawn +1; the verb echoes Od. 13.93 (ὑπερέσχε)"),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note=""),
        "darkness_eclipse": dict(status="fork", clue_ids=["ARG-CIUS-05"], note="a dark night at Cyzicus on Night -17, if non-recognition is read as moonlessness"),
    },
    notes="DESIGN's NC3 season clue (1.1202, Orion's wintry setting) is inside a simile and is excluded here.",
))

clue("ARG-CIUS", "ARG-CIUS-01", "time-of-day",
     "The Argo reaches Cius at the hour when a digger or ploughman goes home hungry for supper, at the end of Day 0.",
     ARG, ["1.1172-1.1177"], ["ἦμος δʼ ἀγρόθεν εἶσι φυτοσκάφος ἤ τις ἀροτρεὺς", "δόρποιο χατίζων", "τῆμος ἄρʼ οἵγʼ ἀφίκοντο Κιανίδος ἤθεα γαίης"],
     "narrator", notes="An ἦμος/τῆμος time-marker, not a simile (no ὡς).")

clue("ARG-CIUS", "ARG-CIUS-02", "moon-phase",
     "Early in Night 0, while Hylas draws water for supper, the full (mid-month) moon shines on him from the sky and the nymph of the spring sees him.",
     ARG, ["1.1209", "1.1229-1.1232"], ["ποτιδόρπιον", "τὸν δὲ σχεδὸν εἰσενόησεν", "πρὸς γάρ οἱ διχόμηνις ἀπʼ αἰθέρος αὐγάζουσα βάλλε σεληναίη"],
     "narrator",
     forks=[O("a", "opposition falls within +-1 day of local midnight of Night 0 and the Moon is above the horizon at some instant in the 3 hours after sunset of Day 0",
              "διχόμηνις is the month-halving (full) moon; water 'for supper' puts the scene early in the night"),
            O("b", "opposition within +-2 days of local midnight of Night 0 and the Moon above the horizon at some instant of Night 0", "looser"),
            NONE("διχόμηνις as an ornamental epithet of the bright moon")])

clue("ARG-CIUS", "ARG-CIUS-03", "planet",
     "At Dawn +1 the dawn star rose over the highest peaks and the breezes came down; Tiphys urges them aboard and they sail, leaving Heracles.",
     ARG, ["1.1273-1.1275"], ["αὐτίκα δʼ ἀκροτάτας ὑπερέσχεθεν ἄκριας ἀστὴρ ἠῷος, πνοιαὶ δὲ κατήλυθον"],
     "narrator", forks=F4("Dawn +1"),
     notes="The peaks are not named, so no azimuth rider. Dawn proper follows at 1.1280-1.1283.")

clue("ARG-CIUS", "ARG-CIUS-04", "time-of-day",
     "Dawn +1 breaks after the sailing; only then do they see they have left Heracles behind.",
     ARG, ["1.1280-1.1283"], ["ἦμος δʼ οὐρανόθεν χαροπὴ ὑπολάμπεται ἠὼς", "τῆμος τούσγʼ ἐνόησαν ἀιδρείῃσι λιπόντες"], "narrator")

clue("ARG-CIUS", "ARG-CIUS-05", "darkness",
     "On Night -17 (row 06) the Argo, after a full day's sail, is driven back to Cyzicus in the night; in the night the Doliones do not recognise the returning heroes and the two sides fight.",
     ARG, ["1.1015-1.1023"], ["ἡ δʼ ἔθεεν λαίφεσσι πανήμερος", "αὐτονυχί", "οὐδʼ ὑπὸ νυκτὶ Δολίονες ἂψ ἀνιόντας ἥρωας νημερτὲς ἐπήισαν"],
     "narrator",
     forks=[O("a", "the Moon is below the horizon for at least 75% of the dark hours of that night", "non-recognition read as a moonless night; the predicate is DESIGN H2's, used for the Odyssey's σκοτομήνιος"),
            O("b", "the Moon is below the horizon at local midnight of that night", "a weaker form"),
            NONE("the text says only that it was night; it does not blame the Moon")])

clue("ARG-CIUS", "ARG-CIUS-06", "interval",
     "From the battle night to Night 0: three whole days of mourning; from then on storms for twelve days and nights; the halcyon on the following night (row 07); next day the sacrifice on Dindymon and a night feast; at dawn they leave and reach Cius that evening.",
     ARG, ["1.1057", "1.1078-1.1080", "1.1092-1.1093", "1.1150-1.1152"],
     ["ἤματα δὲ τρία πάντα γόων", "ἐκ δὲ τόθεν τρηχεῖαι ἀνηέρθησαν ἄελλαι ἤμαθʼ ὁμοῦ νύκτας τε δυώδεκα", "ἐπιπλομένῃ δʼ ἐνὶ νυκτὶ", "Δινδύμου", "αὐτὰρ ἐς ἠὼ ληξάντων ἀνέμων νῆσον λίπον εἰρεσίῃσιν"],
     "narrator",
     forks=[O("n17", "the battle night is Night -17 and the halcyon night is Night -2", "mourning Days -16 to -14, storms Days -13 to -2, halcyon on the following night (Night -2), sacrifice Day -1, departure and Cius Day 0 [me: count]"),
            O("n18", "battle night Night -18; halcyon Night -2", "the funeral takes a fourth day before the storms start"),
            O("n16", "battle night Night -16; halcyon Night -2", "the halcyon night counted as the twelfth night of storm")])

clue("ARG-CIUS", "ARG-CIUS-07", "season",
     "On Night -2 a halcyon flies over the sleeping Jason, prophesying the end of the winds.",
     ARG, ["1.1084-1.1087"], ["πωτᾶτʼ ἀλκυονὶς λιγυρῇ ὀπὶ θεσπίζουσα λῆξιν ὀρινομένων ἀνέμων"],
     "narrator",
     forks=[O("a", "Night -2 within +-7 days of the winter solstice", "the halcyon days: halcyons breed at midwinter, seven days before and seven after, with calm seas [pliny-nh-lat.tsv 10.32.1; also 18.26.1]"),
            O("b", "Night -2 within +-15 days of the Pleiades' morning setting or of either solstice", "Pliny says the halcyon is seen only at the setting of the Vergiliae and about the solstices [pliny-nh-lat.tsv 10.32.1]"),
            NONE("a bird-omen of calm; the text names no season")],
     notes="Not a star clue: the season enters only through ancient bird lore, as the Odyssey's new moon enters Apollo's feast only through a scholion.")

excl(ARG, "1.1201-1.1204", "simile", "simile: a squall strikes a mast at Orion's wintry setting (DESIGN NC3 took its season from here; critique-design issue 15)")
excl(ARG, "1.1265-1.1269", "simile", "simile (gadfly-stung bull)")

# ============================================================ ARG-COLCHIS
SETS.append(dict(
    set="ARG-COLCHIS", role="negative", searchable=True,
    text="Apollonius, Argonautica 2.1097-4.183 (from the storm at the Island of Ares to the flight with the fleece)", text_file=ARG, edition_id=1,
    day0="Day 0 is the day of Jason's ordeal; Night 0 is Medea's flight with the Moon rising; Dawn +1 is the flight with the fleece.",
    day_convention=DAYCONV,
    observer_places=[
        place("Colchis: the Phasis and Aia", ARG, "2.1260-2.1261", ["ἐννύχιοι", "ἵκοντο Φᾶσίν τʼ εὐρὺ ῥέοντα"], 42.15, 41.6667),
        place("the Island of Ares (Night -7)", ARG, "2.1230", ["νῆσον ἀποπροέλειπον Ἄρηος"], 40.9289, 38.4361,
              "Giresun Island (Wikipedia, fetched 2026-10-04); the identification with the Island of Ares is modern, not the text's"),
    ],
    window_width_years=WIN,
    pinned_readings={"literal": {"ARG-COLCHIS-01": "none", "ARG-COLCHIS-02": "a3", "ARG-COLCHIS-04": "b", "ARG-COLCHIS-05": "none", "ARG-COLCHIS-06": "a"},
                     "BM-analogue": {"ARG-COLCHIS-01": "a", "ARG-COLCHIS-02": "a3", "ARG-COLCHIS-04": "a", "ARG-COLCHIS-05": "a", "ARG-COLCHIS-06": "a"}},
    odyssey_slots={
        "day0_phase": dict(status="text", clue_ids=["ARG-COLCHIS-06"], note="moonrise in the dark hours of Night 0: a waning Moon, not a conjunction"),
        "season_stars": dict(status="text", clue_ids=["ARG-COLCHIS-01", "ARG-COLCHIS-04"], note="Arcturus' rainy season on Night -7 (phase unnamed); Orion seen by sailors on Night -3 (fork)"),
        "morning_star": dict(status="empty", clue_ids=[], note=""),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note=""),
        "darkness_eclipse": dict(status="empty", clue_ids=[], note="the starless night of 2.1103-1105 is storm cloud by the text's own words"),
    },
    notes="",
))

clue("ARG-COLCHIS", "ARG-COLCHIS-01", "season",
     "On Night -7, the day the sons of Phrixus near the Island of Ares, Zeus stirs the north wind, 'marking with rain the wet path of Arcturus'; by night a storm wrecks their ship.",
     ARG, ["2.1097-2.1099"], ["καὶ δὴ ἔσαν νήσοιο μάλα σχεδὸν ἤματι κείνῳ", "ὕδατι σημαίνων διερὴν ὁδὸν Ἀρκτούροιο"],
     "narrator",
     forks=[O("a", "Night -7 within +-15 days of Arcturus' morning setting (setting at dawn)", "the wet season of Arcturus read as its setting; the text does not name the phase"),
            O("b", "Night -7 within +-15 days of Arcturus' heliacal rising (first morning visibility)", "Arcturus' rising was also a stormy sign; same caveat"),
            O("c", "Night -7 within +-15 days of Arcturus' evening setting (last evening visibility)", "same caveat"),
            NONE("a learned periphrasis for rain; no phase is named")],
     notes="The storm itself is cloud: 'κελαινὴ δʼ οὐρανὸν ἀχλὺς ἄμπεχεν ... ἐκ νεφέων' (2.1103-1105); it is not entered as darkness.")

clue("ARG-COLCHIS", "ARG-COLCHIS-02", "interval",
     "From Night -7: the rain stops at sunrise (Day -6); they sleep that night; early next morning (Day -5) they leave the island; on the following night they pass Philyra; they sail on past the peoples of the coast, see Prometheus' eagle at evening and reach the Phasis by night (Night -4); dawn comes soon after (Day -3).",
     ARG, ["2.1120-2.1121", "2.1227-2.1228", "2.1231", "2.1244", "2.1251", "2.1260", "2.1285"],
     ["τὸ δὲ μυρίον ἐκ Διὸς ὕδωρ λῆξεν ἅμʼ ἠελίῳ", "κατέδαρθεν", "ἦρι δʼ ἀνεγρομένοισιν", "νυκτὶ δʼ ἐπιπλομένῃ Φιλυρηίδα νῆσον ἄμειβον", "ἐπιπρὸ γὰρ αἰὲν ἔτεμνον", "ἴδον ἕσπερον", "ἐννύχιοι", "ἠὼς δʼ οὐ μετὰ δηρὸν ἐελδομένοις ἐφαάνθη"],
     "narrator",
     forks=[O("a3", "arrival at the Phasis on Night -4, so the Ares storm is Night -7", "one day's sail between the Philyra night and the arrival night [me: count]"),
            O("a4", "arrival on Night -4 but the Ares storm on Night -8", "more than one day passes along the coast ('ἐπιπρὸ γὰρ αἰὲν ἔτεμνον' gives no count)")])

clue("ARG-COLCHIS", "ARG-COLCHIS-03", "interval",
     "In Colchis: Day -3 Jason visits Aeetes; Night -3 Medea lies sleepless; Day -2 she meets Jason at Hecate's temple; at dawn of Day -1 the heroes ask Aeetes for the teeth; Night -1 Jason sacrifices; Day 0 is the ordeal, ending at sunset.",
     ARG, ["3.823-3.824", "3.1171-3.1172", "3.1191", "3.1223-3.1224", "3.1407"],
     ["φέγγος Ἠριγενής", "αὐτὰρ ἅμʼ ἠοῖ", "Ἠέλιος μὲν ἄπωθεν ἐρεμνὴν δύετο γαῖαν", "ἠριγενὴς Ἠὼς βάλεν ἀντέλλουσα", "ἦμαρ ἔδυ, καὶ τῷ τετελεσμένος ἦεν ἄεθλος"],
     "narrator")

clue("ARG-COLCHIS", "ARG-COLCHIS-04", "star",
     "At nightfall of Night -3, 'sailors at sea looked to Helice and the stars of Orion from their ships' (part of a nocturne of the whole sleeping world).",
     ARG, ["3.744-3.746"], ["νὺξ μὲν ἔπειτʼ ἐπὶ γαῖαν ἄγεν κνέφας", "οἱ δʼ ἐνὶ πόντῳ ναῦται εἰς Ἑλίκην τε καὶ ἀστέρας Ὠρίωνος ἔδρακον ἐκ νηῶν"],
     "narrator",
     forks=[O("a", "Betelgeuse and Rigel >= 5 deg above the horizon at the end of evening nautical twilight of Night -3", "the nocturne is set at nightfall ('νὺξ ... ἄγεν κνέφας')"),
            O("b", "Betelgeuse and Rigel >= 5 deg at some instant of the dark hours of Night -3", "sailors watch through the night"),
            NONE("a generic nocturne: the sailors are not the Argonauts and Helice (the Bear) is circumpolar")])

clue("ARG-COLCHIS", "ARG-COLCHIS-05", "time-of-day",
     "Night -1: after sunset, once the stars of Helice the Bear had leaned over and the air was still, Jason goes to his midnight sacrifice, as Medea told him to wait for the night halved in two.",
     ARG, ["3.1029", "3.1195-3.1197"], ["μέσσην νύκτα διαμμοιρηδὰ φυλάξας", "αὐτίκʼ ἐπεί ῥʼ Ἑλίκης εὐφεγγέος ἀστέρες Ἄρκτου ἔκλιθεν"],
     "narrator",
     forks=[O("a", "Dubhe (alpha UMa) is past its upper culmination (west of the meridian) at local midnight of Night -1", "the leaning Bear read as a midnight star-clock, which depends on the season"),
            NONE("a time-of-night marker only (after midnight, as instructed)")],
     notes="3.1029 is Medea's speech (character speech); 3.1195-1197 is narrator.")

clue("ARG-COLCHIS", "ARG-COLCHIS-06", "moon-phase",
     "In Night 0, as Medea runs from the palace, the Titan goddess Moon, newly rising from the horizon, sees her and exults.",
     ARG, ["4.54-4.55"], ["τὴν δὲ νέον Τιτηνὶς ἀνερχομένη περάτηθεν φοιταλέην ἐσιδοῦσα θεὰ ἐπεχήρατο Μήνη"],
     "narrator",
     forks=[O("a", "moonrise falls in the dark hours of Night 0 (between the end of evening nautical twilight and the start of morning nautical twilight)", "'νέον ... ἀνερχομένη περάτηθεν': the Moon is just rising during the flight"),
            O("b", "moonrise falls between local midnight and 2 hours before the start of morning nautical twilight", "the drafter's inference that the flight is late: the rowing to the grove, the hunters' pre-dawn hour (4.109-113) and the taking of the fleece all follow before dawn"),
            O("c", "the Moon is above the horizon at some instant of Night 0", "Selene only sees her"),
            NONE("Selene as a speaking goddess-witness (4.57-65)")])

clue("ARG-COLCHIS", "ARG-COLCHIS-07", "time-of-day",
     "Before dawn, at the hour hunters wake to beat the daylight, Jason and Medea go for the fleece; Dawn +1 spreads as they return to the ship.",
     ARG, ["4.109-4.114", "4.183"], ["ἦμος δʼ ἀνέρες ὕπνον ἀπʼ ὀφθαλμῶν ἐβάλοντο ἀγρόται", "τῆμος ἄρʼ Αἰσονίδης κούρη τʼ ἀπὸ νηὸς ἔβησαν", "Ἠὼς μέν ῥʼ ἐπὶ γαῖαν ἐκίδνατο"],
     "narrator")

excl(ARG, "3.756-3.759", "simile", "simile (a sunbeam dancing off water)")
excl(ARG, "3.957", "simile", "simile (Jason like Sirius)")
excl(ARG, "3.1359-3.1362", "simile", "simile (stars after a winter storm)")
excl(ARG, "3.1377", "simile", "simile (a fiery star or meteor)")
excl(ARG, "4.167-4.170", "simile", "simile (a girl catching the full moon's light on her dress)")
excl(ARG, "3.226-3.227", "narrator", "ekphrasis of Aeetes' springs (warm at the Pleiades' setting): a permanent property, not a date")

# ============================================================ ARG-RETURN
SETS.append(dict(
    set="ARG-RETURN", role="negative", searchable=True,
    text="Apollonius, Argonautica 4.1620-4.1718 (from Triton's harbour by Carpathos and Crete to Anaphe)", text_file=ARG, edition_id=1,
    day0="Day 0 is the day the Argo leaves Crete; Night 0 is the 'pall' night with neither stars nor moon; Dawn +1 shows Anaphe. The evening star is on Day E = Day -(3 + x).",
    day_convention=DAYCONV,
    observer_places=[
        place("the Cretan sea beyond Cape Salmonis (Night 0)", ARG, "4.1693-4.1694", ["ὑπὲρ Σαλμωνίδος ἄκρης", "Κρηταῖον ὑπὲρ μέγα λαῖτμα"], 35.3128, 26.3076,
              "Cape Sideros (Wikipedia, fetched 2026-10-04); identifying Salmonis with Sideros is modern, not the text's"),
        place("Anaphe (Dawn +1)", ARG, "4.1717", ["Ἀνάφην δέ τε λισσάδα νῆσον"], 36.3719, 25.7953),
        place("at sea off the Libyan desert coast, east of Triton's harbour (Day E); no place named", ARG, "4.1623-4.1624", ["αὐτὴν ἐπὶ δεξίʼ ἔχοντες γαῖαν ἐρημαίην"], 32.8225, 21.8625,
              "Cyrene (Wikipedia) chosen by the drafter as a representative point; the text names no place"),
    ],
    window_width_years=WIN,
    pinned_readings={"literal": {"ARG-RETURN-01": "vis7", "ARG-RETURN-03": "x0", "ARG-RETURN-04": "a"},
                     "BM-analogue": {"ARG-RETURN-01": "lag90", "ARG-RETURN-03": "x0", "ARG-RETURN-04": "b"}},
    odyssey_slots={
        "day0_phase": dict(status="text", clue_ids=["ARG-RETURN-04"], note="a moonless night on Night 0, the analogue of the Odyssey's σκοτομήνιος (14.457) rather than of its Day-0 conjunction; option b turns it into a conjunction anchor"),
        "season_stars": dict(status="empty", clue_ids=[], note=""),
        "morning_star": dict(status="empty", clue_ids=[], note="an evening star instead, on Day E"),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note=""),
        "darkness_eclipse": dict(status="fork", clue_ids=["ARG-RETURN-04"], note="a night darkness; eclipse-compatible only as a lunar eclipse (option c)"),
    },
    notes="",
))

clue("ARG-RETURN", "ARG-RETURN-01", "planet",
     "On Day E, when the Sun set, the 'star of the fold' that brings rest to weary ploughmen came up; the wind then dropped in the black night.",
     ARG, ["4.1629-4.1631"], ["ἦμος δʼ ἠέλιος μὲν ἔδυ, ἀνὰ δʼ ἤλυθεν ἀστὴρ αὔλιος, ὅς τʼ ἀνέπαυσεν ὀιζυροὺς ἀροτῆρας", "κελαινῇ νυκτὶ"],
     "narrator", forks=F4eve("Day E"),
     notes="A literal 'rising at sunset' of an unnamed bright star constrains nothing (some bright star always rises near sunset) and is folded into 'none'.")

clue("ARG-RETURN", "ARG-RETURN-02", "interval",
     "From the evening of Day E they row all night, the next day and the following night; Carpathos receives them on Day E+2.",
     ARG, ["4.1633-4.1636"], ["παννύχιοι καὶ ἐπʼ ἦμαρ, ἐπʼ ἤματι δʼ αὖτις ἰοῦσαν νύχθʼ ἑτέρην", "ὑπέδεκτο δʼ ἀπόπροθι παιπαλόεσσα Κάρπαθος"],
     "narrator")

clue("ARG-RETURN", "ARG-RETURN-03", "interval",
     "From Carpathos they cross to Crete (no day count), where Talos bars them; they spend Night -1 on Crete and at the new dawn of Day 0 found a shrine, take water and embark.",
     ARG, ["4.1636-4.1637", "4.1689-4.1692"], ["ἔνθεν δʼ οἵγε περαιώσεσθαι ἔμελλον Κρήτην", "κεῖνο μὲν οὖν Κρήτῃ ἐνὶ δὴ κνέφας ηὐλίζοντο ἥρωες", "νέον φαέθουσαν ἐς ἠῶ"],
     "narrator",
     forks=[O("x0", "the crossing to Crete is on Day E+2, so Day E = Day -3", "the shortest reading the text allows"),
            O("xfree", "the crossing takes x = 0 to 10 further days, so Day E is between Day -13 and Day -3 (the upper bound is the drafter's)", "no count is given for Carpathos and the crossing")])

clue("ARG-RETURN", "ARG-RETURN-04", "darkness",
     "On Night 0, as they run over the Cretan sea, the night they call 'the pall' terrifies them: neither stars nor moonbeams pierce it; black chaos from heaven, or darkness risen from the depths.",
     ARG, ["4.1694-4.1698"], ["νὺξ ἐφόβει, τήνπερ τε κατουλάδα κικλήσκουσιν", "νύκτʼ ὀλοὴν οὐκ ἄστρα διίσχανεν, οὐκ ἀμαρυγαὶ μήνης", "οὐρανόθεν δὲ μέλαν χάος"],
     "narrator",
     forks=[O("a", "the Moon is below the horizon for at least 75% of the dark hours of Night 0", "'no moonbeams'; the predicate is DESIGN H2's for the Odyssey's σκοτομήνιος"),
            O("b", "conjunction falls within +-2 days of local midnight of Night 0", "the moonless night read as the dark of the moon"),
            O("c", "an umbral lunar eclipse is in progress while the Moon is above the horizon during Night 0", "the darkness slot read as an eclipse; the drafter's inference, not the text"),
            NONE("a supernatural darkness: the stars are hidden too, so the Moon's absence is not the cause the text gives")])

clue("ARG-RETURN", "ARG-RETURN-05", "time-of-day",
     "After Apollo's bow flashes, an islet appears; they anchor, and Dawn +1 rises at once: they name the island Anaphe.",
     ARG, ["4.1713-4.1714", "4.1717"], ["αὐτίκα δʼ Ἠὼς φέγγεν ἀνερχομένη", "Ἀνάφην"], "narrator")

excl(ARG, "4.1280-4.1287", "simile", "simile that describes an eclipse (the Sun brings night at midday and the stars shine): excluded as a simile, though it is the poem's only eclipse")
excl(ARG, "4.1479-4.1480", "simile", "simile (seeing the new moon through mist)")
excl(ARG, "4.1616", "simile", "comparison (Triton's fins like the horns of the moon)")
excl(ARG, "4.961", "narrator", "a measure of duration ('as long as a spring day lengthens'), not the season of the day")

# ============================================================ QS-SACK
SETS.append(dict(
    set="QS-SACK", role="negative", searchable=True,
    text="Quintus Smyrnaeus, Posthomerica 12.340-14.470 (the horse brought in, the sack, the departure and Athena's storm)", text_file=QS, edition_id=1600,
    day0="Day 0 is the day the Trojans find the horse; Night 0 is the night of the portents and the sack; Dawn +1 is 14.1.",
    day_convention=DAYCONV,
    observer_places=[
        place("Troy, the god-built city", QS, "12.514", ["θεοδμήτοιο πόληος"], 39.9575, 26.2389),
        place("Tenedos (the fleet)", QS, "12.345", ["πρὸς ἠιόνας Τενέδοιο"], 39.8219, 26.0289),
        place("Cape Caphereus, Euboea (the storm)", QS, "14.469", ["Καφηρέος"], 38.1167, 24.5667),
    ],
    window_width_years=WIN,
    pinned_readings={"literal": {"QS-SACK-02": "none", "QS-SACK-03": "none", "QS-SACK-06": "none"},
                     "BM-analogue": {"QS-SACK-02": "c", "QS-SACK-03": "b", "QS-SACK-06": "none"}},
    odyssey_slots={
        "day0_phase": dict(status="empty", clue_ids=[], note="no lunar statement in books 12-14"),
        "season_stars": dict(status="fork", clue_ids=["QS-SACK-03"], note="only through the lost-Pleiad aetiology"),
        "morning_star": dict(status="empty", clue_ids=[], note=""),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note=""),
        "darkness_eclipse": dict(status="fork", clue_ids=["QS-SACK-02", "QS-SACK-06"], note="stars hidden under a cloudless sky on Night 0 (a prodigy); storm darkness at sea later"),
    },
    notes="The thinnest set: Quintus has no Moon, morning star or Hermes in the sack. Expected to have many survivors under every reading.",
))

clue("QS-SACK", "QS-SACK-01", "time-of-day",
     "The fleet waits at Tenedos through Night -1 for the torch; Dawn of Day 0 comes; the Trojans see smoke over the Hellespont shore and the horse.",
     QS, ["12.345", "12.349", "12.352-12.353"], ["πρὸς ἠιόνας Τενέδοιο", "ὁππότε πυρσὸς ἐελδομένοισι φανείη", "ἐπήλυθεν Ἠριγένεια", "Τρῶες εἰσενόησαν ἐπʼ ᾐόσιν Ἑλλησπόντου"],
     "narrator")

clue("QS-SACK", "QS-SACK-02", "darkness",
     "Among the portents at the Trojans' sacrifices in the evening of Night 0, night-birds cry and a mist covers all the stars above the city, although the shining sky is cloudless.",
     QS, ["12.512-12.516"], ["ἐπεστενάχοντο δὲ λυγρὸν ἐννύχιοι ὄρνιθες", "ἄστρα δὲ πάντʼ ἐφύπερθε θεοδμήτοιο πόληος ἀχλὺς ἀμφεκάλυψε καὶ ἀννεφέλου περ ἐόντος οὐρανοῦ αἰγλήεντος"],
     "narrator",
     forks=[O("a", "an umbral lunar eclipse is in progress while the Moon is above the horizon at Troy in the evening of Night 0 (before local midnight)", "the darkness slot read as an eclipse; the drafter's inference"),
            O("b", "the Moon is above the horizon with illuminated fraction >= 0.9 at the end of evening nautical twilight of Night 0", "a 'gleaming' cloudless sky that hides the stars read as bright moonlight; a weak reading"),
            O("c", "Day 0 is a conjunction date (LMT at Troy)", "a starless, moonless-seeming night read as the dark of the moon; eclipse-compatible anchor; the drafter's inference"),
            NONE("a prodigy among others (bleeding altars, weeping statues, self-opening gates); the text rules out cloud and names no Moon")])

clue("QS-SACK", "QS-SACK-03", "star",
     "During the sack (Night 0) they say Electra, mother of Dardanus, wrapped herself in mist and cloud and left the dance of her sister Pleiades; the others rise in a crowd, she alone is hidden for ever.",
     QS, ["13.551-13.557"], ["Ἠλέκτρην βαθύπεπλον ἑὸν δέμας ἀμφικαλύψαι ἀχλύϊ καὶ νεφέεσσιν ἀποιχομένην χοροῦ ἄλλων πληιάδων", "ἡ δʼ ἄρα μούνη κεύθεται αἰὲν ἄϊστος"],
     "narrator",
     forks=[O("a", "the Pleiades (Alcyone) are above the horizon at some instant of the dark hours of Night 0", "the withdrawal read as an event seen that night"),
            O("b", "Alcyone >= 5 deg above the horizon at the end of evening nautical twilight of Night 0", "seen at nightfall"),
            NONE("an aetiology of the lost Pleiad told as hearsay ('φασι', 13.551) and made permanent ('αἰέν'); schol. Il. 18.486 tells the same story and assigns it to the Cyclic poets [scholia-iliad-grc.tsv key 2.18.198.1]")])

clue("QS-SACK", "QS-SACK-04", "time-of-day",
     "When sleep holds the drunken city, Sinon raises the torch and the fleet sails from Tenedos: the sack is in Night 0.",
     QS, ["13.21-13.23", "13.29"], ["εὖτε γὰρ ὕπνος ἔρυκεν ἀνὰ πτόλιν", "Σίνων ἀνὰ πυρσὸν ἄειρε", "ἐκ Τενέδου νήεσσιν ἐπὶ πλόον ἐντύνοντο"],
     "narrator")

clue("QS-SACK", "QS-SACK-05", "time-of-day",
     "Dawn +1 rises from Ocean; the victors feast until midnight of Night +1; Dawn +2 scatters the night and the Greeks prepare to sail home.",
     QS, ["14.1-14.2", "14.143", "14.228-14.229"], ["καὶ τότʼ ἀπʼ Ὠκεανοῖο θεὰ χρυσόθρονος Ἠὼς οὐρανὸν εἰσανόρουσε", "μέσον περιτέλλετο νυκτός", "ἀνήιεν Ἠριγένεια νύκτα διασκεδάσασα"],
     "narrator")

clue("QS-SACK", "QS-SACK-06", "darkness",
     "On the voyage home (day not stated, at least Day +2), near Euboea, Athena gathers clouds: night pours round the earth and the sea darkens.",
     QS, ["14.422", "14.461-14.462"], ["ὁπότʼ Εὐβοίης σχεδὸν ἤλυθον", "σὺν δʼ ἔχεεν νεφέλας τε καὶ ἠέρα πᾶσαν ὕπερθε· νὺξ δʼ ἐχύθη περὶ γαῖαν"],
     "narrator",
     forks=[O("a", "a solar eclipse of class X1-X4 (DESIGN 3.1) visible near Cape Caphereus, Sun above the horizon, on some day from Day +2 to Day +12 (the bound is the drafter's)", "the darkness slot read as an eclipse; the day is unstated"),
            NONE("storm darkness: the text names the clouds that make it")])

excl(QS, "12.104-12.105", "narrator", "starry night of Athena's dream to Epeius; separated from Day 0 by the three days of building (12.147) and an unstated gap; time of night only")
excl(QS, "13.68-13.69", "simile", "simile (sheep on an autumn night)")
excl(QS, "13.480-13.486", "simile", "simile (gales when the Altar rises opposite Arcturus)")

# ============================================================ VF-LEMNOS
SETS.append(dict(
    set="VF-LEMNOS", role="negative", searchable=True,
    text="Valerius Flaccus, Argonautica 1.309-2.79 and 2.350-2.372 (the first night at sea, landfall at Lemnos, the delay there)", text_file=VF, edition_id=2081,
    day0="Day 0 is the first day of the voyage; Night 0 is the first night at sea (Tiphys' speech); Dawn +1 brings Lemnos in sight. Day L, the storm at Lemnos, is an unstated number of days later.",
    day_convention=DAYCONV,
    observer_places=[
        place("at sea between Pallene, Athos and Lemnos (Night 0 and Dawn +1)", VF, "2.75-2.79", ["Phoebus Athon", "Vulcania surgit Lemnos aquis"], 40.0, 24.7,
              "the drafter's point between Mount Athos (40.158 N 24.327 E) and Lemnos (39.917 N 25.25 E), Wikipedia; the text names the landmarks, not the ship's position"),
        place("Lemnos (Day L)", VF, "2.79", ["Lemnos"], 39.8833, 25.0667, "Myrina, Lemnos (Wikipedia, fetched 2026-10-04)"),
    ],
    window_width_years=WIN,
    pinned_readings={"literal": {"VF-LEMNOS-01": "a", "VF-LEMNOS-02": "b", "VF-LEMNOS-03": "a", "VF-LEMNOS-04": "c", "VF-LEMNOS-05": "a", "VF-LEMNOS-06": "a", "VF-LEMNOS-07": "w60"},
                     "BM-analogue": {"VF-LEMNOS-01": "a", "VF-LEMNOS-02": "a", "VF-LEMNOS-03": "a", "VF-LEMNOS-04": "a", "VF-LEMNOS-05": "none", "VF-LEMNOS-06": "none", "VF-LEMNOS-07": "w60"}},
    odyssey_slots={
        "day0_phase": dict(status="text", clue_ids=["VF-LEMNOS-02", "VF-LEMNOS-06"], note="a clear horned Moon at nightfall of Night 0 (a young crescent under option a: a few days after conjunction); a fourth-day Moon during the Lemnos stay"),
        "season_stars": dict(status="text", clue_ids=["VF-LEMNOS-03", "VF-LEMNOS-04", "VF-LEMNOS-05"], note="Orion and Perseus setting on Night 0, a Pleiad at Dawn +1, the Pleiad's stormy setting at Lemnos"),
        "morning_star": dict(status="empty", clue_ids=[], note="the dawn star of 2.72 is a Pleiad, not Venus"),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note=""),
        "darkness_eclipse": dict(status="empty", clue_ids=[], note=""),
    },
    notes="Both lunar statements render Aratus' weather signs (Phaenomena 783-787): the clear thin third-day moon means fair weather, the thick fourth-day moon means rain.",
))

clue("VF-LEMNOS", "VF-LEMNOS-01", "interval",
     "The Argo sails at the dawn of 1.311; after a day's coasting past Pelion, Sciathos, Sepias and Pallene the Sun sets (2.34-37): Night 0 follows.",
     VF, ["1.310-1.311", "2.34-2.35"], ["Minyas simul optulit omnis alma novo crispans pelagus Tithonia Phoebo", "Iamque Hyperionius metas maris urget Hiberi currus"],
     "narrator",
     forks=[O("a", "the departure day is Day 0", "the coasting of 2.6-33 reads as one day"),
            O("b", "the departure day is Day -3 to Day 0", "no count is given for the coasting; the bound is the drafter's")])

clue("VF-LEMNOS", "VF-LEMNOS-02", "moon-phase",
     "At nightfall of Night 0 Tiphys tells the frightened crew the sky is steady and the Moon has risen clear, her horn not swollen, with no redness on her face.",
     VF, ["2.55-2.57"], ["micat immutabile caelum puraque nec gravido surrexit Cynthia cornu, nullus in ore rubor"],
     "character speech",
     forks=[O("a", "the Moon is above the horizon in the evening twilight of Night 0 with illuminated fraction <= 0.25", "a horned Moon at nightfall is a young crescent; Aratus' clear, thin third-day moon means fair weather [aratus-phaenomena-grc.tsv 783-784]"),
            O("b", "the Moon is above the horizon at some instant between sunset and local midnight of Night 0 (any phase)", "'surrexit': the Moon is up; 'cornu' as a stock attribute"),
            NONE("Aratean weather-sign diction in a speech meant to reassure")])

clue("VF-LEMNOS", "VF-LEMNOS-03", "star",
     "Tiphys: he does not steer by the stars that slip from the pole into the sea, 'great Orion already sets, already Perseus hisses in the angry sea', but by the never-setting Serpent.",
     VF, ["2.61-2.65"], ["non illa sequi mihi sidera monstrat, quae delapsa polo reficit mare: tantus Orion iam cadit, irato iam stridet in aequore Perseus", "axe nitet serpens"],
     "character speech",
     forks=[O("a", "Betelgeuse, Rigel and Mirfak (alpha Persei) are above the horizon at the end of evening nautical twilight of Night 0 and each sets before local midnight", "'iam cadit ... iam stridet': setting now, at nightfall"),
            O("b", "Night 0 within +-15 days of Orion's morning setting (setting at dawn)", "'iam cadit' read as the season of Orion's setting"),
            NONE("a general contrast between setting stars and the circumpolar Serpent")])

clue("VF-LEMNOS", "VF-LEMNOS-04", "star",
     "At Dawn +1 the fields whiten 'under the dim fires of the dawn Atlantid', the Sun first strikes Athos, and Lemnos rises from the sea.",
     VF, ["2.72-2.73", "2.75-2.79"], ["Iamque sub Eoae dubios Atlantidis ignes albet ager", "Phoebus Athon", "Vulcania surgit Lemnos aquis"],
     "narrator",
     forks=[O("a", "Dawn +1 within +-7 days of the Pleiades' heliacal rising (first morning visibility of Alcyone at the site)", "an Atlantid (a Pleiad) seen dimly at dawn: the first dawn appearance"),
            O("b", "Dawn +1 within +-7 days of the Pleiades' morning setting (setting at dawn)", "Virgil uses 'Eoae Atlantides' for the Pleiades' dawn setting [virgil-georgics-lat.tsv 1.221]"),
            O("c", "Alcyone above the horizon at the start of morning nautical twilight of Dawn +1", "the Pleiad is visible at dawn, phase unspecified"),
            NONE("an elaborate dawn periphrasis")])

clue("VF-LEMNOS", "VF-LEMNOS-05", "season",
     "On Day L, during the stay at Lemnos, Jupiter by the law of the sky had set the Pleiad moving with her stormy star, and storms burst on land and sea.",
     VF, ["2.357-2.359"], ["Pliada lege poli nimboso moverat astro Iuppiter", "simul undis cuncta ruunt"],
     "narrator",
     forks=[O("a", "Day L within +-15 days of the Pleiades' morning setting", "the Pleiad's stormy setting that closed the sailing season"),
            O("b", "Day L between the Pleiades' morning setting and the vernal equinox", "the winter storm season"),
            NONE("Jupiter's storm told in astronomical periphrasis; no phase or day is named")])

clue("VF-LEMNOS", "VF-LEMNOS-06", "moon-phase",
     "On a day of the Lemnos stay Tiphys sees the Moon thick with rain at her fourth rising.",
     VF, ["2.367-2.368"], ["et lunam quarto densam videt imbribus ortu Thespiades"],
     "narrator",
     forks=[O("a", "some day of the Lemnos stay (row 07) has a Moon 2.5 to 4.5 days past conjunction at sunset, visible in the evening", "'quarto ortu': the fourth day of the Moon; Aratus' thick fourth-day moon presages rain [aratus-phaenomena-grc.tsv 785-787]"),
            NONE("an Aratean weather sign; the day is not fixed")])

clue("VF-LEMNOS", "VF-LEMNOS-07", "interval",
     "The Argonauts stay at Lemnos an unstated time, kept by the storms and by love, until Heracles rouses them.",
     VF, ["2.369-2.372"], ["urbe sedent laeti Minyae", "nec iam velle vias"],
     "narrator",
     forks=[O("w60", "Day L (rows 05 and 06) lies 1 to 60 days after Dawn +1 (the bound is the drafter's)", "the text gives no count"),
            NONE("rows 05 and 06 are unlinked")])

excl(VF, "1.283-1.285", "narrator", "Orpheus' song of Phrixus' flight (seven dawns and as many moon-shadows): an embedded myth, not the voyage")

# ============================================================ VF-CYZICUS
SETS.append(dict(
    set="VF-CYZICUS", role="negative", searchable=True,
    text="Valerius Flaccus, Argonautica 3.1-3.258 (the night battle at Cyzicus)", text_file=VF, edition_id=2081,
    day0="Day 0 is the day the Argo leaves Cyzicus (the third dawn there); Night 0 is the night it is driven back and the battle; Dawn +1 shows the dead.",
    day_convention=DAYCONV,
    observer_places=[place("Cyzicus", VF, "3.42", ["portuque refertur amico"], 40.3878, 27.8706,
                           "Cyzicus (Wikipedia, fetched 2026-10-04); the port is the text's 'friendly harbour' of the Doliones")],
    window_width_years=WIN,
    pinned_readings={"literal": {"VF-CYZICUS-02": "a"}, "BM-analogue": {"VF-CYZICUS-02": "a"}},
    odyssey_slots={
        "day0_phase": dict(status="text", clue_ids=["VF-CYZICUS-02"], note="a Moon up in the second half of Night 0"),
        "season_stars": dict(status="empty", clue_ids=[], note=""),
        "morning_star": dict(status="empty", clue_ids=[], note=""),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note=""),
        "darkness_eclipse": dict(status="empty", clue_ids=[], note="the long night of 3.210-211 is divine (the stars stand still)"),
    },
    notes="One lunar clue: many survivors expected. Compare Apollonius' version of the same night (ARG-CIUS-05), where no Moon is named.",
))

clue("VF-CYZICUS", "VF-CYZICUS-01", "time-of-day",
     "The third dawn at Cyzicus begins Day 0 and the Argo sails; in Night 0, as the stars incline and bring sleep, Tiphys dozes and the ship is carried back to the Doliones' harbour.",
     VF, ["3.1-3.2", "3.32-3.33", "3.40-3.42"], ["Tertia iam gelidas Tithonia solverat umbras", "Nox erat et leni canebant aequora sulco, et iam prona leves spargebant sidera somnos", "portuque refertur amico"],
     "narrator")

clue("VF-CYZICUS", "VF-CYZICUS-02", "moon-phase",
     "In the battle of Night 0 the Moon, pitying, shines out from the pitch-black sky and turns a spear from Erymus.",
     VF, ["3.194-3.196"], ["venatori Erymo", "piceo comitem miserata refulsit Luna polo"],
     "narrator",
     forks=[O("a", "the Moon is above the horizon at some instant between local midnight and the start of morning nautical twilight of Night 0", "the battle follows the return late in the night ('prona sidera', 3.33)"),
            O("b", "the Moon is above the horizon at some instant of Night 0", "looser timing"),
            NONE("the Moon as a goddess intervening; a divine act, not a sky state")])

clue("VF-CYZICUS", "VF-CYZICUS-03", "time-of-day",
     "Dawn +1 lights the harbour and the towers they know.",
     VF, ["3.257-3.258"], ["primo iam spargere lumine portus orta dies notaeque", "albescere turres"], "narrator")

excl(VF, "3.210-3.211", "narrator", "the stars stand still and the night lingers: divine lengthening of the night (cf. Od. 23.243)")
excl(VF, "3.359-3.361", "simile", "simile (birds returning in mid-spring)")
excl(VF, "3.558-3.559", "simile", "simile (moon and sun reflected in a pool)")

# ============================================================ VF-COLCHIS
SETS.append(dict(
    set="VF-COLCHIS", role="negative", searchable=True,
    text="Valerius Flaccus, Argonautica 7.1-7.24 (Medea's sleepless night)", text_file=VF, edition_id=2081,
    day0="Day 0 is the day Medea parts from her Thessalian guest at evening; Night 0 is her sleepless night; Dawn +1 whitens her threshold.",
    day_convention=DAYCONV,
    observer_places=[place("Colchis at the mouth of the Phasis (Aeetes' city)", VF, "5.178-5.180", ["optatos iam lux ostendere Colchos", "Phasis in aequor ore ruit"], 42.15, 41.6667,
                           "Phasis (Wikipedia, fetched 2026-10-04)")],
    window_width_years=WIN,
    pinned_readings={"literal": {"VF-COLCHIS-01": "vis7", "VF-COLCHIS-02": "vis7"}, "BM-analogue": {"VF-COLCHIS-01": "none", "VF-COLCHIS-02": "lead90"}},
    odyssey_slots={
        "day0_phase": dict(status="empty", clue_ids=[], note=""),
        "season_stars": dict(status="empty", clue_ids=[], note=""),
        "morning_star": dict(status="fork", clue_ids=["VF-COLCHIS-02"], note="'eoo' at Dawn +1"),
        "mercury_turning_point": dict(status="empty", clue_ids=[], note=""),
        "darkness_eclipse": dict(status="empty", clue_ids=[], note=""),
    },
    notes="Read literally, Venus is both the evening star on Day 0 and the morning star at Dawn +1, which happens only near inferior conjunction; the literal pinned reading may therefore have no survivors.",
))

clue("VF-COLCHIS", "VF-COLCHIS-01", "planet",
     "On Day 0 the late evening star parts Medea from her Thessalian guest, and night falls.",
     VF, ["7.1-7.3"], ["Te quoque Thessalico iam serus ab hospite vesper dividit", "noxque ruit"],
     "narrator", forks=F4eve("Day 0"))

clue("VF-COLCHIS", "VF-COLCHIS-02", "planet",
     "After a sleepless Night 0 Medea sees her threshold whiten with the thin light of Eous: Dawn +1.",
     VF, ["7.21-7.23"], ["ecce videt tenui candescere limen eoo", "lux orta"],
     "narrator", forks=F4("Dawn +1")[:-1] + [NONE("'eous' read as the dawn light")])

# ============================================================ IL-PATROCLUS (same-tradition comparison)
SETS.append(dict(
    set="IL-PATROCLUS", role="same-tradition comparison (not a negative: same tradition and diction as the Odyssey; critique-design issue 15)", searchable=True,
    text="Homer, Iliad 11.1-24.695 (the day Patroclus dies through Priam's night journey)", text_file=IL, edition_id=488,
    day0="Day 0 is the day of Patroclus' death (dawn at 11.1, early sunset at 18.241). Hector dies on Day +1; the pyre burns in Night +2; Heosphoros rises at Dawn +3; Hermes guides Priam on Day H, the twelfth dawn after Hector's death.",
    day_convention=DAYCONV,
    observer_places=[
        place("the plain of Troy and the Achaean camp on the shore", IL, "24.346", ["Τροίην τε καὶ Ἑλλήσποντον"], 39.9575, 26.2389),
        place("the shore by the ships (Achilles, Nights +1 to +2)", IL, "23.59", ["ἐπὶ θινὶ πολυφλοίσβοιο θαλάσσης"], 39.9575, 26.2389,
              "Troy (Wikipedia, fetched 2026-10-04); the camp lies a few km from the citadel"),
    ],
    window_width_years=WIN,
    pinned_readings={"literal": {"IL-PATROCLUS-02": "none", "IL-PATROCLUS-04": "none", "IL-PATROCLUS-05": "none", "IL-PATROCLUS-06": "none", "IL-PATROCLUS-08": "vis7", "IL-PATROCLUS-09": "h13", "IL-PATROCLUS-10": "none"},
                     "BM-analogue": {"IL-PATROCLUS-02": "conj", "IL-PATROCLUS-04": "none", "IL-PATROCLUS-05": "none", "IL-PATROCLUS-06": "a", "IL-PATROCLUS-08": "lead90", "IL-PATROCLUS-09": "h13", "IL-PATROCLUS-10": "mwra"},
                     "eclipse-reading": {"IL-PATROCLUS-02": "conj", "IL-PATROCLUS-04": "a", "IL-PATROCLUS-05": "none", "IL-PATROCLUS-06": "none", "IL-PATROCLUS-08": "lead90", "IL-PATROCLUS-09": "h13", "IL-PATROCLUS-10": "mwra"}},
    odyssey_slots={
        "day0_phase": dict(status="fork", clue_ids=["IL-PATROCLUS-02"], note="a conjunction anchor exists only through the darkness forks"),
        "season_stars": dict(status="fork", clue_ids=["IL-PATROCLUS-06"], note="the Shield's stars, the very lines Od. 5.273-275 repeat"),
        "morning_star": dict(status="text", clue_ids=["IL-PATROCLUS-08"], note="Heosphoros at Dawn +3, the same device as Od. 13.93-95"),
        "mercury_turning_point": dict(status="fork", clue_ids=["IL-PATROCLUS-10"], note="Hermes' journey on Day H, told in the seven lines Od. 5.43-49 repeat"),
        "darkness_eclipse": dict(status="text", clue_ids=["IL-PATROCLUS-02", "IL-PATROCLUS-04", "IL-PATROCLUS-05"], note="three darkness statements on Day 0; the text itself localises the darkness of book 17 as mist"),
    },
    notes=("Rebuilt NC1. Every Odyssey slot has an Iliad counterpart in the same diction, so this set measures what B&M's reading does to the Odyssey's "
           "own tradition. Cross-text link for DESIGN 4.4's consistency check: the Iliad is set in the ninth-to-tenth year (2.295, 2.328-329); no position is given here."),
))

clue("IL-PATROCLUS", "IL-PATROCLUS-01", "time-of-day",
     "Dawn of Day 0 (11.1); Hera sends the unwilling Sun down to Ocean and it sets, ending Day 0 (18.239-241); Dawn +1 (19.1).",
     IL, ["11.1", "18.239-18.241", "19.1"], ["Ἠὼς δʼ ἐκ λεχέων", "ἠέλιος μὲν ἔδυ", "Ἠὼς μὲν κροκόπεπλος ἀπʼ Ὠκεανοῖο ῥοάων"],
     "narrator", notes="Books 11-18 are one day.")

clue("IL-PATROCLUS", "IL-PATROCLUS-02", "darkness",
     "Before noon of Day 0, in the fight over Sarpedon's body, Zeus stretches deadly night over the battle.",
     IL, ["16.567"], ["Ζεὺς δʼ ἐπὶ νύκτʼ ὀλοὴν τάνυσε κρατερῇ ὑσμίνῃ"],
     "narrator",
     forks=[O("conj", "Day 0 is a conjunction date (LMT at Troy)", "the eclipse-compatible anchor (DESIGN NC1's 'Day D a new moon'), without requiring an eclipse; not in the text"),
            O("solar_am", "a solar eclipse of class X1-X4 (DESIGN 3.1) visible at Troy on Day 0 with maximum before local apparent noon", "the narrative puts this darkness before the noon line 16.777"),
            NONE("the scholia gloss 'deadly night' as murk, citing Od. 5.294 [scholia-iliad-grc.tsv key 6.16.341.1]")])

clue("IL-PATROCLUS", "IL-PATROCLUS-03", "time-of-day",
     "While the Sun bestrode mid-heaven the two sides were even; when it passed to the hour of unyoking oxen the Achaeans prevailed: noon, then afternoon of Day 0.",
     IL, ["16.777-16.780"], ["ὄφρα μὲν Ἠέλιος μέσον οὐρανὸν ἀμφιβεβήκει", "ἦμος δʼ Ἠέλιος μετενίσετο βουλυτὸν δέ"],
     "narrator")

clue("IL-PATROCLUS", "IL-PATROCLUS-04", "darkness",
     "In the afternoon of Day 0, over Patroclus' body, 'you would not have said the Sun or the Moon was safe', for mist held the best fighters; the rest fought under a clear sky in bright sun with no cloud anywhere; later Zeus scatters the mist and the Sun shines out.",
     IL, ["17.366-17.373", "17.649-17.650"],
     ["οὐδέ κε φαίης οὔτέ ποτʼ ἠέλιον σῶν ἔμμεναι οὔτε σελήνην", "ἠέρι γὰρ κατέχοντο", "πέπτατο δʼ αὐγὴ ἠελίου ὀξεῖα, νέφος δʼ οὐ φαίνετο πάσης γαίης οὐδʼ ὀρέων", "ἠέρα μὲν σκέδασεν καὶ ἀπῶσεν ὀμίχλην, ἠέλιος δʼ ἐπέλαμψε"],
     "narrator",
     forks=[O("a", "a solar eclipse of class X1-X4 visible at Troy on Day 0 with maximum after local apparent noon and last contact before sunset", "an ancient scholiast already says one would have taken it for an eclipse [scholia-iliad-grc.tsv key 6.17.183.1]; the order of 16.777-780 puts it after noon; the Sun shines again (17.650)"),
            O("b", "the Moon is above the horizon at some instant of the afternoon of Day 0", "'neither Sun nor Moon' read as both lights being in the sky"),
            NONE("the text localises the darkness: mist over the best fighters while the rest fought in bright sun (17.370-373; schol. Il. 17.368, key 2.17.136.1, 'not over the whole battle')")])

clue("IL-PATROCLUS", "IL-PATROCLUS-05", "darkness",
     "At the end of Day 0 Hera sends the tireless Sun, unwilling, to the streams of Ocean, and it sets.",
     IL, ["18.239-18.241"], ["Ἠέλιον δʼ ἀκάμαντα βοῶπις πότνια Ἥρη πέμψεν ἐπʼ Ὠκεανοῖο ῥοὰς ἀέκοντα νέεσθαι"],
     "narrator",
     forks=[O("a", "a solar eclipse of class X1-X4 visible at Troy on Day 0 with maximum within the last 2 hours before sunset", "a premature 'sunset' read as an eclipse; the drafter's inference"),
            NONE("divine machinery shortening the day; the scholia call it wholly mythical and compare Od. 23.243 [scholia-iliad-grc.tsv keys 4.18.84.1, 6.18.109.1]")])

clue("IL-PATROCLUS", "IL-PATROCLUS-06", "star",
     "In Night 0 Hephaestus makes the Shield: earth, sky and sea, the tireless Sun and the full Moon, and all the constellations: Pleiades, Hyades, Orion's strength and the Bear that alone never bathes in Ocean.",
     IL, ["18.483-18.489"], ["ἠέλιόν τʼ ἀκάμαντα σελήνην τε πλήθουσαν", "Πληϊάδας θʼ Ὑάδας τε τό τε σθένος Ὠρίωνος", "Ἄρκτόν θʼ"],
     "narrator",
     forks=[O("a", "Alcyone, Aldebaran, Betelgeuse and Rigel are each >= 2 deg above the horizon at some instant of the dark hours of Night 0", "the Shield read as the sky of the night it was made, as B&M read the same lines in Od. 5"),
            O("b", "Day 0 within +-15 days of the Pleiades' morning setting", "18.486 is the verse of Hes. WD 615, where the setting of the Pleiades, Hyades and Orion (WD 616 'δύνωσιν') marks the ploughing season [hesiod-worksdays-grc.tsv 615-616; txt 5.8]"),
            O("c", "opposition within +-1 day of local midnight of Night 0", "'σελήνην τε πλήθουσαν': the full Moon on the Shield, which the scholia gloss as πανσέληνον [scholia-iliad-grc.tsv key 2.18.196.1]"),
            NONE("decoration of an artefact; 18.487-489 = Od. 5.273-275 [txt 5.8]")],
     notes="Option c contradicts the conjunction options of row 02; the garden carries both.")

clue("IL-PATROCLUS", "IL-PATROCLUS-07", "interval",
     "Hector dies on Day +1; Achilles sleeps on the shore in Night +1; at Dawn +2 they gather wood and build the pyre; the winds fan it all through Night +2; Heosphoros rises at its end, Dawn +3.",
     IL, ["23.58-23.62", "23.109", "23.217-23.218"], ["Πηλεΐδης δʼ ἐπὶ θινὶ πολυφλοίσβοιο θαλάσσης", "μυρομένοισι δὲ τοῖσι φάνη ῥοδοδάκτυλος Ἠὼς", "παννύχιοι δʼ ἄρα τοί γε πυρῆς ἄμυδις φλόγʼ ἔβαλλον"],
     "narrator")

clue("IL-PATROCLUS", "IL-PATROCLUS-08", "planet",
     "At Dawn +3, when the light-bringer goes forth to announce light on the earth and saffron Dawn spreads over the sea after it, the pyre dies down.",
     IL, ["23.226-23.228"], ["ἦμος δʼ ἑωσφόρος εἶσι φόως ἐρέων ἐπὶ γαῖαν, ὅν τε μέτα κροκόπεπλος ὑπεὶρ ἅλα κίδναται ἠώς, τῆμος πυρκαϊὴ ἐμαραίνετο"],
     "narrator", forks=F4("Dawn +3"),
     notes="The scholia gloss φόως ἐρέων as foretelling the light by its rising [scholia-iliad-grc.tsv key 2.23.90.1].")

clue("IL-PATROCLUS", "IL-PATROCLUS-09", "interval",
     "Day H, when Priam goes to Achilles, is the twelfth dawn after Hector's death.",
     IL, ["24.31", "24.413-24.414"], ["ἀλλʼ ὅτε δή ῥʼ ἐκ τοῖο δυωδεκάτη γένετʼ ἠώς", "δυωδεκάτη δέ οἱ ἠὼς κειμένῳ"],
     "narrator",
     forks=[O("h13", "Day H = Day +13", "twelve dawns after the death on Day +1"),
            O("h12", "Day H = Day +12", "the death day counted as the first, as the scholion counts (wood-cutting, the games as the third day, then nine) [scholia-iliad-grc.tsv key 4.24.22.1]"),
            O("h15", "Day H = Day +15", "'ἐκ τοῖο' counted from the end of the games (Day +3); the scholion's 'from when Hector died' is against it")],
     notes="24.413-414 is Hermes speaking in disguise (character speech within a deception); it is cited only as agreeing with the narrator's 24.31.")

clue("IL-PATROCLUS", "IL-PATROCLUS-10", "planet",
     "On the evening of Day H Hermes ties on his sandals, takes his wand and flies to Troy and the Hellespont (the seven lines that Od. 5.43-49 repeat); he meets Priam at dusk and leaves for Olympus as Dawn H+1 spreads over the earth.",
     IL, ["24.339-24.346", "24.351", "24.694-24.695"],
     ["οὐδʼ ἀπίθησε διάκτορος ἀργεϊφόντης", "ὑπὸ ποσσὶν ἐδήσατο καλὰ πέδιλα", "εἵλετο δὲ ῥάβδον", "αἶψα δʼ ἄρα Τροίην τε καὶ Ἑλλήσποντον ἵκανε", "ἐπὶ κνέφας ἤλυθε γαῖαν", "Ἑρμείας μὲν ἔπειτʼ ἀπέβη πρὸς μακρὸν Ὄλυμπον, Ἠὼς δὲ κροκόπεπλος ἐκίδνατο πᾶσαν ἐπʼ αἶαν"],
     "narrator",
     forks=F5("Day H")[:-1] + [
         O("dawnvis", "Mercury visible as a morning object at Dawn H+1 (arcus visionis 10 deg)", "Hermes leaves as dawn spreads; B&M's rule read as a morning appearance"),
         NONE("Hermes is the messenger god; the journey is a type-scene shared with Od. 5.43-49 [txt 5.9]")],
     notes="The Mercury slot of the Odyssey's grammar, in the Odyssey's own words. In the Odyssey it falls 34 days before the anchor; here 12-15 days after.")

excl(IL, "22.26-22.31", "simile", "simile (Achilles like the late-summer star, Orion's dog), Day +1")
excl(IL, "22.317-22.318", "simile", "simile (Hesperos), Day +1")
excl(IL, "11.62-11.63", "simile", "simile (the baneful star among clouds), Day 0")

# ---------------------------------------------------------------- checks and output
ECLIPSE_COMPAT = {
    "AEN-TROY": ["AEN-TROY-02:ii-a", "AEN-TROY-02:ii-b", "AEN-TROY-05:conj"],
    "AEN-CRETE": [], "AEN-ITALY": [], "AEN-ETNA": [], "AEN-CARTHAGE": [],
    "ARG-CIUS": [], "ARG-COLCHIS": [],
    "ARG-RETURN": ["ARG-RETURN-04:b", "ARG-RETURN-04:c"],
    "QS-SACK": ["QS-SACK-02:a", "QS-SACK-02:c", "QS-SACK-06:a"],
    "VF-LEMNOS": [], "VF-CYZICUS": [], "VF-COLCHIS": [],
    "IL-PATROCLUS": ["IL-PATROCLUS-02:conj", "IL-PATROCLUS-02:solar_am", "IL-PATROCLUS-04:a", "IL-PATROCLUS-05:a"],
}
for _s in SETS:
    _s["eclipse_compatible_options"] = ECLIPSE_COMPAT[_s["set"]]
    _s["eclipse_compatible_note"] = ("clue:option pairs that put a conjunction or an eclipse in the reading (DESIGN's 'eclipse-compatible'); "
                                     "lunar-eclipse options (ARG-RETURN-04:c, QS-SACK-02:a) are not solar class X and are listed for completeness")


def check():
    ids = {c["clue_id"] for c in CLUES}
    assert len(ids) == len(CLUES), "duplicate clue ids"
    sets = {s["set"] for s in SETS}
    for c in CLUES:
        assert c["set"] in sets, c["clue_id"]
        assert c["narrative_level"] in ("narrator", "character speech", "simile", "lying tale"), c["clue_id"]
        assert c["kind"] in ("eclipse-solar", "eclipse-lunar", "moon-phase", "planet", "star", "season", "time-of-day", "interval", "site", "darkness", "other"), c["clue_id"]
        opts = [o["option"] for o in c["fork_options"]]
        assert len(opts) == len(set(opts)), c["clue_id"]
    byid = {c["clue_id"]: c for c in CLUES}
    for s in SETS:
        for name, pin in s["pinned_readings"].items():
            for cid, opt in pin.items():
                assert cid in byid and byid[cid]["set"] == s["set"], (s["set"], name, cid)
                assert opt in [o["option"] for o in byid[cid]["fork_options"]], (s["set"], name, cid, opt)
        for slot, v in s["odyssey_slots"].items():
            for cid in v["clue_ids"]:
                assert cid in byid, (s["set"], slot, cid)
        for pair in s["eclipse_compatible_options"]:
            cid, opt = pair.split(":")
            assert cid in byid and byid[cid]["set"] == s["set"], pair
            assert opt in [o["option"] for o in byid[cid]["fork_options"]], pair


LEAK = [
    re.compile(r"\d\s*(BC|BCE|B\.C\.|AD|CE)\b"),
    re.compile(r"(?<![\w.])[−-]1\d{3}(?![\d.])"),
    re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b"),
    re.compile(r"\b(Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\b"),
    re.compile(r"Julian date|\bJD\b"),
]


def main():
    check()
    doc = dict(
        file="data/prereg/negatives.json",
        written="2026-10-04",
        purpose=("Clean negative-control clue sets (fiction or legend composed long after the events it tells) and the Iliad as a same-tradition "
                 "comparison, built under the Odyssey's selection rules: narrator or character statements only; no similes, no lying tales; a feature "
                 "the words do not state enters only as a fork with an explicit 'none'. There is no truth file: these texts have no true date."),
        drafting_notes="docs/negatives-drafting.md",
        builder="results/negatives/build_negatives.py (verifies every licence_words fragment against the cited rows of data/text)",
        conventions=dict(
            day_labels=DAYCONV,
            time_scales="LMT and LAT at the set's site; local midnight is LAT 00:00; nautical twilight = Sun centre at -12 deg.",
            windows="window_width_years gives widths only; the bench places each window at a pre-drawn random position (DESIGN 4.3). No set carries a position.",
            eclipse_classes="X1-X4 as defined in DESIGN 3.1 (to be revised under critique-design issue 10); computed at the set's site.",
            arcus_visionis="Venus 5 deg / 7 deg, Mercury 10 deg, Jupiter 10 deg, Mars 11.5 deg, Saturn 11 deg [vis 1.2]; stars by the bench's star-phase routine.",
            fork_menus="F4 (morning star) and F5 (Hermes = Mercury) reproduce DESIGN 3.4 so that each set's garden uses the same fork types as the Odyssey's.",
            licence_words="exact characters of the cited rows; ' … ' separates discontinuous fragments.",
            ref="list of exact row keys in text_file (data/text/).",
        ),
        sets=SETS, clues=CLUES, excluded_rows=EXCLUDED,
    )
    s = json.dumps(doc, ensure_ascii=False, indent=1)
    for rx in LEAK:
        m = rx.search(s)
        if m:
            raise SystemExit(f"leak check failed: {m.group(0)!r} near {s[max(0, m.start()-80):m.end()+80]!r}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(s + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"wrote {OUT}: {len(SETS)} sets, {len(CLUES)} clues, {len(EXCLUDED)} excluded rows")
    for st in SETS:
        n = sum(1 for c in CLUES if c["set"] == st["set"])
        g = 1
        for c in CLUES:
            if c["set"] == st["set"] and c["fork_options"]:
                g *= len(c["fork_options"])
        print(f"  {st['set']:<14} {n:2d} clues  fork-product {g}")


if __name__ == "__main__":
    main()
