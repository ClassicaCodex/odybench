# Licence check, round 2: apply this round's edits to data/prereg/controls_almagest.json.
# Input : results/license-check-almagest/r2/controls_almagest.pre_r2.json (the file as round 1 left it;
#         SHA-256 758ee789193af1077e1bbe1ca4772a65129aa94e65a3315d9fb0ee9655ba4c83)
# Output: data/prereg/controls_almagest.json (CRLF, indent 1, ensure_ascii=False: the file's own format)
# Every new licence fragment is cut from the cited row's own characters (cut()), so it is an exact substring.
# Re-running is idempotent: it always starts from the pre_r2 copy.
import io, json, sys, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = "C:/Projects/odybench/"
SRC = ROOT + "results/license-check-almagest/r2/controls_almagest.pre_r2.json"
DST = ROOT + "data/prereg/controls_almagest.json"
PFX = "urn:cts:greekLit:tlg0363.tlg001.1st1K-grc1."
ELL = " \u2026 "
rows = {}
for line in open(ROOT + "data/text/ptolemy-syntaxis-grc.tsv", encoding="utf-8"):
    k, _, v = line.rstrip("\n").partition("\t")
    rows[k] = v

d = json.load(open(SRC, encoding="utf-8"))
C = {c["clue_id"]: c for c in d["clues"]}
NEW = {}   # clue_id -> this round's verdict
LOG = []


def row_of(cid):
    return rows[C[cid]["ref"]]


def cut(cid, phrase):
    """Return `phrase` as the row's own characters (tolerating only the tonos/oxia encoding difference)."""
    t = row_of(cid)
    if phrase in t:
        return phrase
    nt, np_ = unicodedata.normalize("NFC", t), unicodedata.normalize("NFC", phrase)
    assert len(nt) == len(t), "NFC changed the row length; cannot map indices"
    i = nt.find(np_)
    assert i >= 0, (cid, phrase)
    s = t[i:i + len(np_)]
    assert unicodedata.normalize("NFC", s) == np_
    return s


def set_licence(cid, frags):
    t = row_of(cid)
    pos = -1
    for f in frags:
        i = t.find(f, pos + 1)
        assert i > pos, (cid, "fragment missing or out of order", f)
        pos = i
    old = C[cid]["licence_words"]
    C[cid]["licence_words"] = ELL.join(frags)
    LOG.append("%s licence_words:\n   OLD %s\n   NEW %s" % (cid, old, C[cid]["licence_words"]))


def set_field(cid, field, new, old_expected=None):
    old = C[cid][field]
    if old_expected is not None:
        assert old == old_expected, (cid, field, old)
    C[cid][field] = new
    LOG.append("%s %s:\n   OLD %s\n   NEW %s" % (cid, field, old, new))


def opt(cid, name):
    for o in C[cid]["fork_options"]:
        if o["option"] == name:
            return o
    raise KeyError((cid, name))


def set_just(cid, name, new, old_expected=None):
    o = opt(cid, name)
    if old_expected is not None:
        assert o["justification"] == old_expected, (cid, name, o["justification"])
    LOG.append("%s option %s justification:\n   OLD %s\n   NEW %s" % (cid, name, o["justification"], new))
    o["justification"] = new


# ---------------------------------------------------------------- 1. unstated day bounds spelled out
for cid, words, js, other in [
    ("ALM-A.1", "'μηδέπω … ἐληλυθότα'", "7/15/30", "ge_after_same_apparition"),
    ("ALM-I.1", "'οὐδέπω … ἐληλύθει'", "7/15/30", "ge_after_same_apparition"),
]:
    o = opt(cid, "ge_after_within_j")
    set_just(cid, "ge_after_within_j", o["justification"] + ". The words (%s) give no number of days: j (%s) is the drafter's bound, an inference, not a stated interval; the unbounded literal reading is '%s'" % (words, js, other))
    NEW[cid] = ("edited: the j-day option (primary) did not say that its bound is not in the words; %s gives no number of days. Justification now says j is the drafter's bound and names the unbounded literal option. Values and primary unchanged" % words)
for cid, words, js in [("ALM-B.1", "'μετὰ τὴν μεγίστην ἑῴαν ἀπόστασιν'", "7/15/30/60"),
                       ("ALM-J.4", "'παρεληλύθει … τὴν μεγίστην ἑῴαν ἀπόστασιν'", "15/30/60")]:
    o = opt(cid, "ge_before_within_j")
    base = o["justification"]
    if cid == "ALM-J.4":
        base += ", read as: the greatest morning elongation fell 0..j days earlier"
    set_just(cid, "ge_before_within_j", base + ". The words (%s) give no number of days: j (%s) is the drafter's bound, an inference, not a stated interval; the unbounded literal reading is 'ge_before_same_apparition'" % (words, js))
    NEW[cid] = ("edited: the j-day option (primary) did not say that its bound is not in the words; %s gives no number of days. Justification now says j is the drafter's bound and names the unbounded literal option. Values and primary unchanged" % words)

# ---------------------------------------------------------------- 2. statement features without quoted words
# A.10: 'Before sunrise' in the statement, and the longitudes its primary phase class rests on
f1 = cut("ALM-A.10", "πρὸ τῆς τοῦ ἡλίου ἀνατολῆς, τουτέστιν μετὰ ε ὥρας ἔγγιστα ἰσημερινὰς τοῦ μεσονυκτίου, ἐπειδήπερ ἡ μὲν μέση τοῦ ἡλίου πάροδος ἐπεῖχεν Καρκίνου μοίρας ῑϚ ῑᾱ")
f2 = cut("ALM-A.10", "ὁ τοῦ Διὸς ἐπέχων ἐφαίνετο Διδύμων μοίρας ῑε U+2220 δ΄, τῷ δὲ κέντρῳ τῆς σελήνης νοτιωτέρας οὔσης ἐξ ἴσου ἐφαίνετο")
assert C["ALM-A.10"]["licence_words"].split(ELL)[1] in f2
set_licence("ALM-A.10", [f1, f2])
NEW["ALM-A.10"] = ("edited: (1) the statement's 'Before sunrise' had no quoted words (the licence began at 'μετὰ ε ὥρας'); the licence now starts at 'πρὸ τῆς τοῦ ἡλίου ἀνατολῆς' (same row, contiguous). "
                   "(2) the primary phase_class (waning crescent) rests on Jupiter's sighted longitude and the mean Sun's, both stated in the row, which were not quoted; added them (the mean Sun's longitude is a season statement and is used only through the Sun-Moon difference; see rules_applied). Options unchanged")

# A.2: the evening-star status its primary phase class rests on
old = C["ALM-A.2"]["licence_words"].split(ELL)
set_licence("ALM-A.2", [cut("ALM-A.2", "μηδέπω ἐπὶ τὴν μεγίστην ἑσπερίαν ἀπόστασιν ἐληλυθότα")] + old)
NEW["ALM-A.2"] = "edited: the statement's 'while Mercury is an evening star', on which the primary phase_class inference (young crescent) rests, had no quoted words; added 'μηδέπω ἐπὶ τὴν μεγίστην ἑσπερίαν ἀπόστασιν ἐληλυθότα' (same row). Options unchanged"

# A.5: the 'about three days after opposition' its primary phase class rests on
old = C["ALM-A.5"]["licence_words"].split(ELL)
set_licence("ALM-A.5", [cut("ALM-A.5", "μετὰ γ ἔγγιστα ἡμέρας τῆς γ΄ ἀκρωνύκτου")] + old)
NEW["ALM-A.5"] = "edited: the statement's 'about three days after Mars' opposition', a day interval on which the primary phase_class inference (near full) rests, had no quoted words; added 'μετὰ γ ἔγγιστα ἡμέρας τῆς γ΄ ἀκρωνύκτου' (same row). Options unchanged"

# B.5: the longitudes its primary phase class rests on
old = C["ALM-B.5"]["licence_words"].split(ELL)
set_licence("ALM-B.5", [old[0], cut("ALM-B.5", "τοῦ μέσου ἡλίου ἐπέχοντος Τοξότου μοίρας κη μα"), old[1],
                        cut("ALM-B.5", "ὤφειλεν ἐπέχειν Ὑδροχόου μοίρας θ μ, ἡ δὲ ἐν Ἀλεξανδρείᾳ φαινομένη μοίρας η λδ")])
set_just("ALM-B.5", "phase_class",
         opt("ALM-B.5", "phase_class")["justification"].replace("Ptolemy states in the same sentence", "Ptolemy states in this row"))
NEW["ALM-B.5"] = "edited: the primary phase_class (waxing crescent) rests on the Moon's apparent longitude and the mean Sun's, both stated in the row, which were not quoted; added them (the mean Sun's longitude is a season statement and is used only through the Sun-Moon difference; see rules_applied). Justification: 'same sentence' corrected to 'this row'. Options unchanged"

# A.4: 'to the mean Sun' rests on Ptolemy's definition in 10.7.2 (cut from that row's own characters)
_t = rows[PFX + "10.7.2"]
_p = unicodedata.normalize("NFC", "τριῶν ἀκρωνύκτων τῶν πρὸς τὴν μέσην τοῦ ἡλίου πάροδον διαμέτρων")
_i = unicodedata.normalize("NFC", _t).find(_p)
assert _i >= 0 and len(unicodedata.normalize("NFC", _t)) == len(_t)
def107 = _t[_i:_i + len(_p)]
set_field("ALM-A.4", "notes", C["ALM-A.4"]["notes"] + ". 'To the mean Sun' is Ptolemy's definition of his acronychal observations at 10.7.2: '" + def107 + "'")
NEW["ALM-A.4"] = "edited: notes only: the statement's 'to the mean Sun' rests on a definition in another row; quoted it (10.7.2 '" + def107 + "')"

# J.2: '(morning)'
set_licence("ALM-J.2", [cut("ALM-J.2", "ἑῷος ὁ τοῦ Ἄρεως τῷ βορείῳ μετώπῳ τοῦ Σκορπίου ἐδόκει ἐπιπροσθετηκέναι")])
NEW["ALM-J.2"] = "edited: the statement's '(morning)' had no quoted words; the licence now starts at 'ἑῷος ὁ τοῦ Ἄρεως' (same row, contiguous). Options unchanged"

# K.5: 'morning'
set_licence("ALM-K.5", [cut("ALM-K.5", "ἑῷος ἐπεκάλυψεν τὸν νότιον Ὄνον")])
NEW["ALM-K.5"] = "edited: the statement's 'morning' had no quoted words; the licence now starts at 'ἑῷος' (same row, contiguous). Options unchanged"

# J.5: Ptolemy's identification of the star
old = C["ALM-J.5"]["licence_words"]
set_licence("ALM-J.5", [old,
                        cut("ALM-J.5", "ὁ καθʼ ἡμιᾶς μετὰ τὸν ἐπʼ ἄκρας τῆς νοτίου πτέρυγος τῆς Παρθένου"),
                        cut("ALM-J.5", "Παρθένου μοίρας η δ΄")])
NEW["ALM-J.5"] = "edited: the statement's identification (Ptolemy: the star after the tip of Virgo's southern wing, at Virgo 8 1/4 in his catalogue) had no quoted words; added 'ὁ καθʼ ἡμιᾶς μετὰ τὸν ἐπʼ ἄκρας τῆς νοτίου πτέρυγος τῆς Παρθένου' and 'Παρθένου μοίρας η δ΄' (same row; the catalogue-epoch words between them are left out as date words). 'eta Vir' remains the drafter's gloss. Options unchanged"

# D.4: Ptolemy's value of the Pleiad length
old = C["ALM-D.4"]["licence_words"]
set_licence("ALM-D.4", [old, cut("ALM-D.4", "τὸ δὲ μῆκος αὐτῆς α U+2220΄ ἐστιν ἔγγιστα μοίρας")])
set_just("ALM-D.4", "positional",
         "the stated offset in longitude holds within the tolerance: west of the middle of the Pleiades by one Pleiad length, 1 1/2 deg by Ptolemy's value in this row. Latitude: the words give only the side ('μικρῷ νοτιώτερος', a little to the south) and no amount, so only 'south of' is tested",
         "the stated offsets in longitude/latitude hold within the tolerance (unit conventions in notes)")
NEW["ALM-D.4"] = "edited: the statement's '(Ptolemy: about 1 1/2 deg)' had no quoted words; added 'τὸ δὲ μῆκος αὐτῆς α U+2220΄ ἐστιν ἔγγιστα μοίρας' (same row). The positional justification spoke of stated latitude offsets, but the words give only 'a little to the south' (no amount); it now says only the side is tested. Tolerances and primary unchanged"

# ---------------------------------------------------------------- 3. B.2: an absolute offset the words do not state
b3 = C["ALM-B.3"]["licence_words"]
b2old = C["ALM-B.2"]["licence_words"].split(ELL)
set_licence("ALM-B.2", [cut("ALM-B.2", "τὸν τῆς Ἀφροδίτης ἀστέρα μετὰ τὴν μεγίστην ἑῴαν ἀπόστασιν"),
                        cut("ALM-B.2", b3 + ", " + b2old[0]), b2old[1]])
set_field("ALM-B.2", "statement",
          "At 4 3/4 equinoctial hours after midnight Venus stands between beta Sco and the Moon's apparent centre, in line with them, and west of the Moon's centre by 1 1/2 times the amount by which it is east of beta Sco (the words give this ratio, not a distance).",
          "At 4 3/4 equinoctial hours after midnight the Moon's apparent centre, Venus and beta Sco stand in one line, Venus just west of the Moon.")
set_just("ALM-B.2", "phase_class",
         "Venus is a morning star past its greatest elongation, which never exceeds about 47 deg, so a Moon beside it lies west of the Sun by less than about 47 deg: a waning crescent (drafter's inference; it needs no time of day)",
         "Venus is a morning star past greatest elongation, so a Moon beside it before dawn is waning, roughly a crescent 40-50 deg west of the Sun (my inference)")
o = opt("ALM-B.2", "positional")
LOG.append("ALM-B.2 option positional operational:\n   OLD %s" % json.dumps(o["operational"], ensure_ascii=False))
o["operational"] = {"relation": "moon_app_lon - venus_lon = 1.5 * (venus_lon - star_lon), with venus_lon between star_lon and moon_app_lon",
                    "star": "beta Sco", "tolerance_deg": [0.5, 1.0, 2.0]}
LOG.append("   NEW %s" % json.dumps(o["operational"], ensure_ascii=False))
set_just("ALM-B.2", "positional",
         "the words state no Venus-Moon distance, only a ratio ('τοῦ δὲ κέντρου τῆς σελήνης προηγεῖτο ἡμιόλιον, οὗ ὑπελείπετο τοῦ βορειοτάτου'): in longitude, (Moon's apparent centre - Venus) = 1 1/2 x (Venus - beta Sco), Venus between them; the relation holds within the tolerance (topocentric Moon)",
         "the stated body-Moon offset in longitude holds within the tolerance (topocentric)")
set_field("ALM-B.2", "notes",
          C["ALM-B.2"]["notes"] + ". That 1/4 deg is derived from Ptolemy's computed lunar longitude: it is not a stated offset and no option uses it")
NEW["ALM-B.2"] = ("edited: (1) the 'positional' option tested 'the stated body-Moon offset', but the words state no Venus-Moon distance, only that Venus preceded the Moon's centre by 1 1/2 times its distance east of beta Sco; the only number available was the notes' 'about 1/4 deg', derived from Ptolemy's computed lunar longitude. The option now tests the stated ratio (operational 'relation' added; tolerances unchanged). "
                  "(2) the statement's 'in one line' had no quoted words; the licence now includes 'μεταξὺ καὶ ἐπʼ εὐθείας ἦν … κέντρῳ τῆς σελήνης' (contiguous with the old first fragment), and the statement gives the ratio instead of 'just west'. "
                  "(3) the phase_class justification said 'before dawn', which the words do not say; replaced by a time-free argument. "
                  "(4) that primary phase_class rests on Venus being past its greatest morning elongation, which was not quoted; added 'τὸν τῆς Ἀφροδίτης ἀστέρα μετὰ τὴν μεγίστην ἑῴαν ἀπόστασιν' (same row). Primary unchanged")

# ---------------------------------------------------------------- 4. C.3: fragment order, and an option whose justification and test differ
c3 = C["ALM-C.3"]["licence_words"].split(ELL)
set_licence("ALM-C.3", [cut("ALM-C.3", c3[1] + "· καὶ " + c3[0])])
set_just("ALM-C.3", "magnitude",
         "5/6 (1/2 + 1/3) of the diameter eclipsed; this option tests the magnitude only (the side, 'ἀπʼ ἄρκτων', is tested by 'magnitude_and_side')",
         "5/6 of the diameter, from the north")
mt = opt("ALM-C.3", "magnitude_and_time")
LOG.append("ALM-C.3 option magnitude_and_time operational:\n   OLD %s" % json.dumps(mt["operational"], ensure_ascii=False))
mt["operational"] = {"umbral_mag_range": [[0.7, 0.95], [0.6, 1.0]], "time_tol_h": mt["operational"]["time_tol_h"]}
LOG.append("   NEW %s" % json.dumps(mt["operational"], ensure_ascii=False))
set_just("ALM-C.3", "magnitude_and_time",
         "the magnitude ranges of 'magnitude' plus the stated mid-eclipse time (Ptolemy's computed time, 'ἐπελογισάμεθα')",
         "plus the stated mid-eclipse time")
fo = C["ALM-C.3"]["fork_options"]
i = [o["option"] for o in fo].index("magnitude") + 1
fo.insert(i, {"option": "magnitude_and_side",
              "justification": "the literal reading: 5/6 of the diameter eclipsed from the north ('ἐξέλειπεν ἀπʼ ἄρκτων'), i.e. the Moon's northern limb in the umbra, so at mid-eclipse the Moon's centre lies south of the shadow's centre (negative ecliptic latitude)",
              "operational": {"umbral_mag_range": [[0.7, 0.95], [0.6, 1.0]], "eclipsed_limb": "north"},
              "primary": False})
LOG.append("ALM-C.3 option magnitude_and_side: ADDED (non-primary)")
NEW["ALM-C.3"] = ("edited: (1) the licence's two fragments were out of text order (the time clause precedes the magnitude clause); replaced by the contiguous phrase in text order. "
                  "(2) 'magnitude' (primary) justified itself with 'from the north', but its test is the magnitude only; justification corrected, and the literal reading with the side added as a new non-primary option 'magnitude_and_side' (eclipsed_limb north). "
                  "(3) 'magnitude_and_time' carried only a time tolerance; its magnitude ranges are now explicit. Primary unchanged")

# ---------------------------------------------------------------- 5. wording that went beyond the words
hesp = cut("ALM-D.3", "ἑσπέριος")
set_field("ALM-D.3", "statement",
          "Venus is an evening star (%s) at its greatest eastern (evening) elongation on this day; no hour is stated." % hesp,
          "Venus is an evening star at its greatest eastern (evening) elongation on this day (evening).")
set_field("ALM-D.3", "notes", C["ALM-D.3"]["notes"] + ". The record has no hour or time word: '%s' (as an evening star) places the sighting in the evening part of the night it is dated to, which fixes its civil day (the set's +35; a pre-dawn placement would give +36)" % hesp)
NEW["ALM-D.3"] = "edited: the statement's '(evening)' as the time of the sighting: the row has no hour or time word, only 'ἑσπέριος' (as an evening star). Reworded like the ἑῷος rows C.1, G.1, L.1 and L.4 ('no hour is stated'), and a note records that ἑσπέριος fixes the evening part of the dated night, on which the +35 of ALM-D.2 rests. Options unchanged"

set_field("ALM-E.3", "statement",
          "The spring equinox occurred on this day, about one hour after noon (the words do not say 'equinoctial'; on an equinox day seasonal and equinoctial hours are equal).",
          "The spring equinox occurred on this day, about 1 equinoctial hour after noon.")
NEW["ALM-E.3"] = "edited: the statement said '1 equinoctial hour'; the words are 'μετὰ μίαν ὥραν ἔγγιστα τῆς μεσημβρίας' (about one hour after noon), with no 'ἰσημερινή'. Reworded; no operational change, since on an equinox day the two kinds of hour coincide"

set_field("ALM-H.6", "statement",
          "Mercury relative to a named star: it seemed that, in passing the common star (beta Tau), it would stand more than 3 moons (>1.5 deg) south of it ('ἀφέξειν' is future: the observer's expectation for the passage, not a separation measured on this day).",
          "Mercury relative to a named star on this day: seemed, as it passed, to stand more than 3 moons (>1.5 deg) south of the common star (beta Tau).")
set_just("ALM-H.6", "positional",
         "Mercury's ecliptic latitude is more than 1.5 deg (3 moons) south of beta Tau's, within the tolerance, tested on this day: a stand-in for the separation at passing that the words describe (drafter's approximation)",
         "the stated offsets in longitude/latitude hold within the tolerance (unit conventions in notes)")
set_field("ALM-H.6", "notes",
          C["ALM-H.6"]["notes"].replace("seemed, as it passed, to stand more than 3 moons (>1.5 deg) south of the common star (beta Tau).",
                                        "it seemed that, in passing the common star (beta Tau), it would stand more than 3 moons (>1.5 deg) south of it ('ἀφέξειν', future)."))
assert "ἀφέξειν', future" in C["ALM-H.6"]["notes"]
NEW["ALM-H.6"] = "edited: the statement read the future infinitive 'ἀφέξειν' as a separation measured on the day; the words give the observer's expectation for the passage ('it seemed it would stand off'). Statement, notes and the positional justification now say so; the same-day latitude test is kept as an approximation, with 'none' still available. Tolerances and primary unchanged"

# ---------------------------------------------------------------- 6. notes only
set_field("ALM-B.9", "notes", C["ALM-B.9"]["notes"] + ". '9β' in the licence is the numeral ϙβ (92), the export printing the koppa as the digit 9; Ptolemy's own reduction in the row confirms it (the Moon's longitude he derives exceeds the Sun's by 92 1/8 deg)")
NEW["ALM-B.9"] = "edited: notes only: the licence's '9β' is the numeral ϙβ = 92 with the koppa printed as the digit 9; recorded, with the check from Ptolemy's own reduction in the same row"

CHK = "results/license-check-almagest/r2/interval_check.txt"
for cid, note, verdict in [
    ("ALM-C.2", "The anchor record IX.8.3 has no hour word: 'ἑῷος' (morning star) places it in the pre-dawn part of the night it is dated to, giving +17 (an evening placement would give +18). Ptolemy's mean-Sun figure for IX.8.3 and true-Sun figure for the eclipse imply 17.72 days between the two instants against 17.75 from the dates (" + CHK + ")",
     "edited: notes only: recorded that the civil day of the hourless anchor IX.8.3 comes from 'ἑῷος' (pre-dawn part of its dated night) and that Ptolemy's own Sun figures confirm +17 rather than +18 (round-2 recomputation)"),
    ("ALM-D.2", "X.1.3 has no hour word: 'ἑσπέριος' (evening star) places it in the evening part of its dated night, giving +35 (a pre-dawn placement would give +36); Ptolemy's mean-Sun figures in the two rows imply 35.00 days (" + CHK + ")",
     "edited: notes only: recorded that the civil day of the hourless record X.1.3 comes from 'ἑσπέριος' and that Ptolemy's mean-Sun figures confirm +35 (round-2 recomputation)"),
    ("ALM-G.2", "The anchor X.3.2a has no hour word: 'ἑῷος' places it in the pre-dawn part of its dated night, giving +106 (an evening placement would give +107); Ptolemy's mean-Sun figures imply 106.02 days (" + CHK + ")",
     "edited: notes only: recorded that the civil day of the hourless anchor X.3.2a comes from 'ἑῷος' and that Ptolemy's mean-Sun figures confirm +106 (round-2 recomputation)"),
    ("ALM-L.3", "Neither record has an hour word: 'ἑῷος' places each in the pre-dawn part of its dated night; Ptolemy's mean-Sun figures imply 585.95 days (" + CHK + ")",
     "edited: notes only: recorded that the civil days of the two hourless records come from 'ἑῷος' and that Ptolemy's mean-Sun figures confirm +586 (round-2 recomputation)"),
    ("ALM-L.5", "The anchor X.1.5 has no hour word: 'ἑῷος' places it in the pre-dawn part of its dated night; to the evening record IX.9.3 Ptolemy's mean-Sun figures imply 996.53 days against 996.58 from the dates (" + CHK + ")",
     "edited: notes only: recorded that the civil day of the hourless anchor X.1.5 comes from 'ἑῷος' and that Ptolemy's mean-Sun figures confirm +996 (round-2 recomputation)"),
]:
    set_field(cid, "notes", C[cid]["notes"] + ". " + note)
    NEW[cid] = verdict

# ---------------------------------------------------------------- 7. file-level fields
ra = d["rules_applied"]
k = ra.index("zodiacal longitudes and elongation magnitudes stated by Ptolemy are not used (B&M grammar has no coordinates)")
ra[k] = ("zodiacal longitudes and elongation magnitudes stated by Ptolemy are not used as clue values (B&M grammar has no coordinates). "
         "Exceptions [licence check r2]: A.10 and B.5 choose their phase class from longitudes stated in the row (the Moon's or the planet's, and the mean Sun's), each forked with 'none'; "
         "J.7 uses the difference of the two Venus longitudes Ptolemy gives, forked with 'none'; B.7 and B.9 use the measured Sun-Moon distance, which is the observation itself. "
         "Where a licence quotes the Sun's longitude (A.10, B.5, B.7, B.9) it is a season statement that no option uses except through the Sun-Moon difference")
LOG.append("rules_applied[%d] amended (exceptions listed)" % k)
d["conventions"]["licence_words"] += ". The export writes the half sign sometimes as '∠' and sometimes as the literal text 'U+2220' (both occur in the TSV); licence strings copy the row's own characters"
LOG.append("conventions.licence_words: note on the two spellings of the half sign")

# ---------------------------------------------------------------- 8. verdicts on every row; keep round 1's
new_clues = []
for c in d["clues"]:
    r1 = c["license_check"]
    out = {}
    for key, val in c.items():
        if key == "license_check":
            out["license_check"] = NEW.get(c["clue_id"], "ok")
            out["license_check_r1"] = r1
        else:
            out[key] = val
    new_clues.append(out)
d["clues"] = new_clues
r1block = d.pop("license_check")
r1block["report"] = "results/license-check-almagest/r2/license-check-almagest.r1.md (copy; docs/license-check-almagest.md now holds round 2's report)"
n_edit = sum(1 for c in new_clues if c["license_check"] != "ok")
d["license_check"] = {
    "checked": "2026-10-04",
    "round": 2,
    "by": "independent licence check, round 2 (an agent that drafted none of these sets and did not do round 1; read no truth file and not docs/research-controls.md, docs/controls-almagest.md or results/controls-almagest/)",
    "report": "docs/license-check-almagest.md",
    "rows_checked": len(new_clues),
    "rows_edited": n_edit,
    "rows_ok": len(new_clues) - n_edit,
    "pre_edit_sha256": "758ee789193af1077e1bbe1ca4772a65129aa94e65a3315d9fb0ee9655ba4c83",
    "pre_edit_copy": "results/license-check-almagest/r2/controls_almagest.pre_r2.json",
    "script": "results/license-check-almagest/r2/apply_edits_r2.py",
    "interval_recomputation": "results/license-check-almagest/r2/interval_check.py -> interval_check.txt (contains date words): all 20 interval rows reproduce from the text (18 from the Egyptian dates as printed, 2 stated in words); Ptolemy's stated Sun positions agree within 0.3 d except at the two forked cruxes, A.6 (mean Sun gives 49) and H.3 (72)",
    "per_row_fields": "license_check = this round's verdict on the row as round 1 left it; license_check_r1 = round 1's verdict (relative to the builder's output)",
    "warning": "results/controls-almagest/build_prereg.py writes this file; re-running it would silently undo both rounds of edits unless they are ported into it (round 1: results/license-check-almagest/apply_edits.py; round 2: results/license-check-almagest/r2/apply_edits_r2.py)",
}
d["license_check_r1"] = r1block

with open(DST, "w", encoding="utf-8") as f:   # text mode: CRLF on Windows, as the file was
    f.write(json.dumps(d, ensure_ascii=False, indent=1))
print("\n".join(LOG))
print("\nrows edited this round: %d of %d" % (n_edit, len(new_clues)))
for cid in sorted(NEW, key=lambda x: [c["clue_id"] for c in new_clues].index(x)):
    print(" ", cid, "|", NEW[cid][:110])
