"""
Almagest dated observations used for the B&M-type positive control
(docs/controls-almagest.md).  Scratch module for results/controls-almagest/.

Every Greek string below is an exact substring of the row `ref` in
data/text/ptolemy-syntaxis-grc.tsv (Heiberg's text as exported from ClassicaCodex
EditionId 2977); `check_licences()` asserts this.  Numbers that Ptolemy states
(mean-sun longitudes, hours) are transcribed from the same rows; where the
export's numeral is damaged ('??', dropped letters) the record says so.

Calendar (all from the text, no modern dates enter here):
  * Egyptian civil calendar: 12 months x 30 days + 5 epagomenal days = 365 d,
    no leap day.  Months 1..12 = Thoth .. Mesore, 13 = epagomenai.
  * Nabonassar era: day count from Nab 1 Thoth 1, noon (Ptolemy's epoch for
    all mean motions, 3.7.4 / 3.9.5: "τῷ α΄ ἔτει Ναβονασσάρου κατʼ Αἰγυπτίους
    Θὼθ α΄ τῆς μεσημβρίας").
  * Regnal / era years -> Nabonassar years, each from Ptolemy's own words:
      Hadrian n   = Nab 863+n   (3.7.4: Augustus 1 = Philip 295 [σ??δ = 294 years
                                 from Alexander's death to Augustus], Philip n =
                                 Nab 424+n [υκδ], and Augustus 1 Thoth 1 to
                                 Hadrian 17 Athyr 7 = 161 Egyptian years + 66 d,
                                 so Hadrian 17 = Nab 719+161 = 880)
      Antoninus n = Nab 884+n   (9.10.3 "τῷ βʹ ἔτει Ἀντωνίνου, ὅ ἦν κατὰ τὸ ωπϚʹ
                                 ἔτος ἀπὸ Ναβονασσάρου"; 10.4.6 "μέχρι τῆς
                                 Ἀντωνίνου βασιλείας ωπδ΄")
      Philip (years from Alexander's death) n = Nab 424+n (3.7.4 "υκδ";
                                 10.9.2 "νβ΄ ... υοϚ΄")
      Philadelphus 13 = Nab 476 (10.4.6 "τὸ μὲν τῆς τηρήσεως ἔτος υος΄")
      Dionysian and Chaldean dates: Ptolemy gives the Nabonassar/Egyptian
                                 equivalent in the same sentence (used as is).
"""
import sys, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TSV = ROOT / "data" / "text" / "ptolemy-syntaxis-grc.tsv"
PRE = "urn:cts:greekLit:tlg0363.tlg001.1st1K-grc1."

NAB_EPOCH_JD = 1448638          # Nab 1 Thoth 1, noon (JD integer = Greenwich noon); task brief + research-controls 4.19
MONTHS = ["Thoth", "Phaophi", "Athyr", "Choiak", "Tybi", "Mecheir", "Phamenoth", "Pharmouthi",
          "Pachon", "Payni", "Epiphi", "Mesore", "epagomenai"]
# Ptolemy's mean daily motion of the Sun, 0;59,8,17,13,12,31 deg/day (Alm. III.1, solar tables)
PTOL_SUN_N = 59/60 + 8/60**2 + 17/60**3 + 13/60**4 + 12/60**5 + 31/60**6
PTOL_SUN_EPOCH = 330.75         # Pisces 0;45 at Nab 1 Thoth 1 noon (3.7.4 "τῶν Ἰχθύων τῆς α μοίρας ἑξηκοστὰ με")

ALEXANDRIA = (31.20, 29.92)     # lat, lon (deg); Ptolemy's site per 9.10.3 etc. ("ἐν Ἀλεξανδρείᾳ")
BABYLON = (32.54, 44.42)

ZOD = dict(Aries=0, Taurus=30, Gemini=60, Cancer=90, Leo=120, Virgo=150, Libra=180, Scorpius=210,
           Sagittarius=240, Capricorn=270, Aquarius=300, Pisces=330)


def Z(sign, deg):
    return ZOD[sign] + deg


def nab_jd_noon(nab_year, month, day):
    """JD (integer, = noon) of Egyptian civil day `day` of `month` in Nabonassar year."""
    return NAB_EPOCH_JD + 365 * (nab_year - 1) + 30 * (month - 1) + (day - 1)


# ----------------------------------------------------------------------------
# part (time-of-day words) -> which civil day (Egyptian day d of "d into d+1")
#   'evening'          : evening of day d                       civil day d
#   'morning'          : dawn ending the night d/d+1            civil day d+1
#   'h_before_midnight': hours before the midnight d/d+1        civil day d
#   'h_after_midnight' : hours after the midnight d/d+1         civil day d+1
#   'h_after_noon'     : hours after the noon of day d          civil day d
#   'noon'             : noon of day d                           civil day d
# hours are equinoctial hours on Ptolemy's local apparent clock.
# ----------------------------------------------------------------------------

R = []


def rec(**k):
    R.append(k)
    return k


# =============================== BOOK IX : MERCURY ==========================
rec(id="IX.7.4", ref="9.7.4", body="mercury", observer="Ptolemy", observer_words="ἐτηρήσαμεν γὰρ ἡμεῖς",
    era="Hadrian 16", nab=863 + 16, month=7, day=16, part="evening",
    date_words="τῷ ιϚ´ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Φαμενὼθ ιϚ´ εἰς τὴν ιζʹ ἑσπέρας",
    phen="GE", side="E",
    phen_words="τὸ πλεῖστον ἀποστάντα τῆς μέσης τοῦ ἡλίου παρόδου",
    side_words="ἡ μεγίστη ἄρα τῆς μέσης ἀπόστασις ἑσπερία",
    ref_star="aldebaran", ref_star_words="διοπτευόμενος πρὸς τὴν λαμπρὰν Ὑάδα",
    ptol_lon=Z("Pisces", 1), ptol_mean_sun=Z("Aquarius", 9.75),
    measured="astrolabe longitude of Mercury (Pisces 1) against Aldebaran; greatest elongation from the mean sun 21 1/4 deg")
rec(id="IX.7.5", ref="9.7.5", body="mercury", observer="Ptolemy (continues 'ἐτηρήσαμεν' of 9.7.4)", observer_words="",
    era="Hadrian 18", nab=863 + 18, month=11, day=18, part="morning",
    date_words="τῷ ιηʹ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Ἐπιφὶ ιηʹ εἰς τὴν ιθʹ ὄρθρου",
    phen="GE", side="W",
    phen_words="ἐπὶ τῆς μεγίστης ὢν ἀποστάσεως",
    side_words="ἡ μεγίστη τῆς μέσης ἀπόστασις ἑῴα",
    extra_words="σφόδρα λεπτὸς καὶ ἀμαυρὸς φαινόμενος",
    ref_star="aldebaran", ref_star_words="διοπτευόμενός τε πρὸς τὴν λαμπρὰν Ὑάδα",
    ptol_lon=Z("Taurus", 18.75), ptol_mean_sun=Z("Gemini", 10),
    measured="astrolabe longitude (Taurus 18 3/4); Mercury 'very faint and dim'; elongation from mean sun 21 1/4")
rec(id="IX.7.6", ref="9.7.6", body="mercury", observer="Ptolemy", observer_words="πάλιν ἡμεῖς ἐτηρήσαμεν διὰ τοῦ ἀστρολάβου",
    era="Antoninus 1", nab=884 + 1, month=11, day=20, part="evening",
    date_words="τῷ αʹ Ἀντωνίνου ἔτει κατʼ Αἰγυπτίους κʹ τοῦ Ἐπιφὶ εἰς τὴν καʹ ἑσπέρας",
    phen="GE", side="E",
    phen_words="τὸ πλεῖστον ἀποστάντα τῆς τοῦ ἡλίου μέσης παρόδου",
    side_words="ἡ μεγίστη τῆς μέσης ἀπόστασις ἑσπερία",
    ref_star="regulus", ref_star_words="διοπτευόμενος δὲ τότε πρὸς τὸν ἐπὶ τῆς καρδίας τοῦ Λέοντος",
    ptol_lon=Z("Cancer", 7), ptol_mean_sun=Z("Gemini", 10.5),
    measured="astrolabe longitude (Cancer 7) against Regulus; elongation from mean sun 26 1/2")
rec(id="IX.7.7", ref="9.7.7", body="mercury", observer="Ptolemy ('ὡσαύτως', continuing 9.7.6)", observer_words="",
    era="Antoninus 4", nab=884 + 4, month=7, day=18, part="morning",
    date_words="τῷ δʹ ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους Φαμενὼθ ιηʹ εἰς τὴν ιθʹ ὄρθρου",
    phen="GE", side="W",
    phen_words="πάλιν ἐπὶ τῆς μεγίστης ὢν ἀποστάσεως",
    side_words="ἡ μεγίστη τῆς μέσης ἀπόστασις ἑῴα",
    ref_star="antares", ref_star_words="διοπτευόμενος πρὸς τὸν καλούμενον Ἀντάρην",
    ptol_lon=Z("Capricorn", 13.5), ptol_mean_sun=Z("Aquarius", 10),
    measured="astrolabe longitude (Capricorn 13 1/2) against Antares; elongation from mean sun 26 1/2 "
             "(export prints 'κ ∠' = 20 1/2 but says 'τῶν ἴσων', equal to 9.7.6's 26 1/2, and 310-283.5 = 26.5: a dropped Ϛ)")
rec(id="IX.7.9", ref="9.7.9", body="mercury", observer="unnamed (Dionysian-calendar record)", observer_words="",
    era="Dionysian 23 Hydron 29 = Nab 486 Choiak 17/18", nab=486, month=4, day=17, part="morning",
    date_words="ἔτους γὰρ κγ΄ κατὰ Διονύσιον Ὑδρῶνος κθ´",
    date_words_nab="ἦν γὰρ ὁ χρόνος κατὰ τὸ υπϚʹ ἔτος ἀπὸ Ναβοωασσάρου κατʼ Αἰγυπτίους Χοιὰκ ιζʹ εἰς τὴν ιηʹ ὄρθρου",
    phen="GEold", side="W",
    phen_words="ἑῷος ὁ Στίλβων",
    ge_claim_ref="9.7.8", ge_claim_words="διὰ δὲ τῶν παλαιῶν τῶν περὶ τὰς μεγίστας ἀποστάσεις τετηρημένων",
    stars=[dict(kind="offset", star="delta_cap", dlon=0.0, dlat=+1.5,
                words="τοῦ λαμπροτάτου οὐραίου ἐν Αἱγοκέρῳ διεῖχεν εἰς τὰ πρὸς ἄρκτους σελήνας γ",
                reading="3 'moons' (1 moon taken as 0.5 deg) north of delta Cap; Ptolemy then gives Mercury the star's own longitude")],
    ptol_lon=Z("Capricorn", 22 + 1/3), ptol_mean_sun=Z("Aquarius", 18 + 1/6),
    measured="Mercury relative to delta Cap; Ptolemy treats it as a greatest morning elongation (25 5/6 from mean sun)")
rec(id="IX.7.11", ref="9.7.11", body="mercury", observer="unnamed (Dionysian-calendar record)", observer_words="",
    era="Dionysian 23 Tauron 4 = Nab 486 Phamenoth 30/Pharmouthi 1", nab=486, month=7, day=30, part="evening",
    date_words="τῷ μὲν γὰρ αὐτῷ κγʹ ἔτει κατὰ Διονύσιον Ταυρῶνος δʹ ἑσπέρας",
    date_words_nab="κατὰ τὸ υπϚʹ ἔτος πάλιν ἀπὸ Ναβονασσάρου κατʼ Αἰγυπτίους Φαμενὼθ λʹ εἰς τὴν αʹ ἐσπέρας",
    emend=dict(month=6, day=30, label="Nab 486 Mecheir 30/Phamenoth 1, evening",
               why="TEXTUAL CRUX. The printed Egyptian date (Phamenoth 30/Pharmouthi 1) gives Ptolemy's mean sun at "
                   "Taurus 29.08 under his own tables, but he states 'Κριοῦ μοίρας κθ ∠' (Aries 29 1/2) in this sentence and "
                   "uses Aries 29 1/2 again in 9.7.13 (mean-sun difference 33 1/3 deg to IX.7.12). Mecheir 30/Phamenoth 1 "
                   "(30 days earlier) reproduces 29.51 deg. Both readings are carried; the interval is a fork."),
    phen="GEold", side="E",
    phen_words="ἑσπέρας",
    ge_claim_ref="9.7.10", ge_claim_words="διὰ δὲ δύο τῶν ἔγγιστα τὴν ἴσην ἐπελογισάμιιεθα",
    stars=[dict(kind="line_east", star="beta_tau", star2="zeta_tau", dist=+1.5,
                words="τῆς διὰ τῶν τοῦ Ταύρου κεράτων εὐθείας ὑπελείπετο τρεῖς σελήνας",
                reading="1.5 deg (3 moons) to the rear (east) of the line through the horns of Taurus (beta Tau - zeta Tau)"),
           dict(kind="offset", star="beta_tau", dlon=None, dlat=-1.5, cmp="lt",
                words="ἐδόκει δὲ παραπορευόμενος τοῦ κοινοῦ ἀφέξειν πρὸς μεσημβρίαν πλεῖον τριῶν σεληνῶν",
                reading="seemed, as it passed, to stand more than 3 moons (>1.5 deg) south of the common star (beta Tau)")],
    ptol_lon=None, ptol_mean_sun=Z("Aries", 29.5),
    measured="Mercury relative to the horns of Taurus; Ptolemy uses it (with 9.7.12) to interpolate an evening elongation "
             "(longitude numeral damaged in the export: 'Ταύρου μοίρας ἄγ ??')")
rec(id="IX.7.12", ref="9.7.12", body="mercury", observer="unnamed (Dionysian-calendar record)", observer_words="",
    era="Dionysian 28 Didymon 7 = Nab 491 Pharmouthi 5/6", nab=491, month=8, day=5, part="evening",
    date_words="τῷ δὲ κηʹ ἔτει κατὰ Διονύσιον Διδυμῶνος ζ´ ἑσπέρας",
    date_words_nab="κατὰ τὸ υ??α´ ἔτος ἀπὸ Ναβονασσάρου κατʼ Αἰγυπτίους Φαρμουθὶ εʹ εἰς τὴν Ϛʹ ἑσπέρας",
    nab_note="Nabonassar numeral damaged in the export ('υ??α´'); read 491 = υ (400) + koppa (90) + α (1), "
             "which also follows from Dionysian 28 being 5 years after Dionysian 23 = Nab 486 (9.7.9); "
             "confirmed by Ptolemy's own mean sun (Gemini 2 5/6) under his solar tables (see mean-sun check)",
    phen="GEold", side="E",
    phen_words="ἑσπέρας",
    ge_claim_ref="9.7.10", ge_claim_words="διὰ δὲ δύο τῶν ἔγγιστα τὴν ἴσην ἐπελογισάμιιεθα",
    stars=[dict(kind="heads_line", star="castor", star2="pollux",
                words="κατʼ εὐθεῖαν ἦν μάλιστα ταῖς κεφαλαῖς τῶν Διδύμων, πρὸς μεσημβρίαν δὲ τῆς νοτίου διεῖχεν τριτημορίῳ σελήνης ἔλασσον ἢ διπλάσιον, οὗ αἱ κεφαλαὶ διεστήκασιν",
                reading="on the line through Castor and Pollux, south of Pollux by (2 x the Castor-Pollux distance) - 1/3 moon")],
    ptol_lon=Z("Gemini", 29 + 1/3), ptol_mean_sun=Z("Gemini", 2 + 5/6),
    measured="Mercury relative to the heads of Gemini; evening elongation 26 1/2 from mean sun")
rec(id="IX.7.14", ref="9.7.14", body="mercury", observer="unnamed record, reduced by Hipparchus", observer_words="ἐξ ὧν ὁ Ἵππαρχος ἐπιλογίζεται",
    era="Dionysian 24 Leonton 28 = Nab 486 Payni 30", nab=486, month=10, day=30, part="evening",
    date_words="πάλιν ἔτους κδʹ κατὰ Διονύσιον Λεοντῶνος κη´ ἑσπέρας",
    date_words_nab="κατὰ τὸ υπϚʹ ἔτος ἀπὸ Ναβονασσάρο κατʼ Αἰγυπτίους Παϋνὶ λʹ ἐσπέρας",
    phen="GEold", side="E",
    phen_words="ἑσπέρας",
    ge_claim_ref="9.7.14", ge_claim_words="γέγονεν ἄρα ἡ μεγίστη τῆς μέσης ἀπόστασις ἑσπερία",
    stars=[dict(kind="offset", star="spica", dlon=-3.0, dlat=None, cmp="lon_more_west",
                words="προηγεῖτο τοῦ Στάχυος, ἐξ ὧν ὁ Ἵππαρχος ἐπιλογίζεται, μικρῷ πλεῖον γ μοιρῶν",
                clue_words="προηγεῖτο τοῦ Στάχυος, … μικρῷ πλεῖον γ μοιρῶν",
                reading="preceded (west of) Spica by a little more than 3 deg (as reckoned by the astronomer the text names)")],
    ptol_lon=Z("Virgo", 19.5), ptol_mean_sun=Z("Leo", 27 + 5/6),
    measured="Mercury relative to Spica (reduced by Hipparchus); evening elongation 21 2/3 from mean sun (fraction damaged in export: 'κα ??')")
rec(id="IX.7.15", ref="9.7.15", body="mercury", observer="unnamed (Chaldean-calendar record)", observer_words="",
    era="Chaldean 75 Dios 14 = Nab 512 Thoth 9/10", nab=512, month=1, day=9, part="morning",
    date_words="ἔτους μὲν γὰρ οεʹ κατὰ Χαλδαίους Δίου ιδʹ",
    date_words_nab="κατὰ τὸ φιβʹ ἔτος ἀπὸ Ναβονασσάρου κατʼ Αἰγυπτίους Θὼθ θʹ εἰς τὴν ιʹ ὄρθρου",
    phen="GEold", side="W",
    phen_words="ἑῷος ἐπάνω ἦν τοῦ νοτίου Ζυγοῦ πήχεως ἥμισυ",
    ge_claim_ref="9.7.15", ge_claim_words="γέγονεν ἄρα ἡ ἑῴα μεγίστη διάστασις",
    stars=[dict(kind="offset", star="alpha2_lib", dlon=None, dlat=+1.0,
                words="ἐπάνω ἦν τοῦ νοτίου Ζυγοῦ πήχεως ἥμισυ",
                reading="half a cubit 'above' the southern pan (alpha Lib); a cubit is about 2-2.5 deg in Babylonian usage "
                        "(my gloss), taken here as 'north by about 1 deg'")],
    ptol_lon=Z("Libra", 14 + 1/6), ptol_mean_sun=Z("Scorpius", 5 + 1/6),
    measured="Mercury relative to alpha Lib; morning elongation 21 from mean sun")
rec(id="IX.7.16", ref="9.7.16", body="mercury", observer="unnamed (Chaldean-calendar record)", observer_words="",
    era="Chaldean 67 Apellaios 5 = Nab 504 Thoth 27/28", nab=504, month=1, day=27, part="morning",
    date_words="ἔτει δὲ ξζ´ κατὰ Χαλδαίους Ἀπελλαίου εʹ",
    date_words_nab="κατὰ τὸ φδʹ ἔτος ἀπὸ Ναβονασσάρου κατʼ Αἰγυπτίους Θὼθ κζʹ εἰς τὴν κηʹ ὄρθρου",
    phen="GEold", side="W",
    phen_words="ἑῷος ἐπάνω ἦν τοῦ βορείου μετώπου τοῦ Σκορπίου πήχεως ἥμισυ",
    ge_claim_ref="9.7.16", ge_claim_words="γέγονεν ἄρα καὶ αὕτη ἡ διάστασις",
    stars=[dict(kind="offset", star="beta1_sco", dlon=None, dlat=+1.0,
                words="ἐπάνω ἦν τοῦ βορείου μετώπου τοῦ Σκορπίου πήχεως ἥμισυ",
                reading="half a cubit above beta Sco (as IX.7.15)")],
    ptol_lon=Z("Scorpius", 2 + 1/3), ptol_mean_sun=Z("Scorpius", 24 + 5/6),
    measured="Mercury relative to beta Sco; morning elongation 22 1/2 from mean sun")
rec(id="IX.8.3", ref="9.8.3", body="mercury", observer="Ptolemy (9.8.2 'τῶν ὑφʼ ἡμῶν διὰ τοῦ ἀστρολάβου τηρηθεισῶν')", observer_words="",
    era="Hadrian 19", nab=863 + 19, month=3, day=14, part="morning",
    date_words="τῷ μὲν οὖν ιθʹ ἔτει Ἀδριανοῦ κατʼ Αἰγυπττίους Ἀθὺρ ιδʹ εἰς τὴν ιεʹ",
    phen="nearGE", side="W",
    phen_words="ἑῷος ὁ τοῦ Ἑρμοῦ περὶ τὴν μεγίστην τυγχάνων ἀπόστασιν",
    ref_star="regulus", ref_star_words="διοπτευόμενος πρὸς τὸν ἐπὶ τῆς καρδίας τοῦ Δέοντος",
    ptol_lon=Z("Virgo", 20.2), ptol_mean_sun=Z("Libra", 9.25),
    measured="astrolabe longitude (Virgo 20 1/5) against Regulus; elongation 19 1/20 from mean sun")
rec(id="IX.8.4", ref="9.8.4", body="mercury", observer="Ptolemy", observer_words="",
    era="Hadrian 19", nab=863 + 19, month=9, day=19, part="evening",
    date_words="τῷ δὲ αὐτά ἔτει Παχὼν ιθʹ ἑσπέρας",
    phen="nearGE", side="E",
    phen_words="περὶ τὴν μεγίστην πάλιν ὢν ἀπόστασιν",
    ref_star="aldebaran", ref_star_words="διοπτευόμενος πρὸς τὴν λαμπράν Ὑάδα",
    ptol_lon=Z("Taurus", 4 + 1/3), ptol_mean_sun=Z("Aries", 11 + 1/12),
    measured="astrolabe longitude (Taurus 4 1/3) against Aldebaran; elongation 23 1/4 from mean sun")
rec(id="IX.9.3", ref="9.9.3", body="mercury", observer="Theon", observer_words="ὡς ἐν ταῖς παρὰ Θέωνος εἰλημμέναις τηρήσεσιν εὕρομεν",
    era="Hadrian 14", nab=863 + 14, month=12, day=18, part="evening",
    date_words="τῷ μὲν γὰρ ιδʹ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Μεσορὴ ιηʹ ἑσπέρας",
    phen="GE", side="E",
    phen_words="τὸ πλεῖστον, φησίν, ἀπέστη τοῦ ἡλίου",
    stars=[dict(kind="offset", star="regulus", dlon=+3.0 + 0.5 + 1/3, dlat=None,
                words="ὑπολειπόμενος τοῦ ἐπὶ τῆς καρδίας τοῦ Λέοντος μοίρας γ ∠ʹ γʹ",
                reading="to the rear (east) of Regulus by 3 1/2 1/3 = 3 5/6 deg")],
    ptol_lon=Z("Leo", 6 + 1/3), ptol_mean_sun=Z("Cancer", 10 + 1/12),
    measured="Mercury 3 5/6 deg east of Regulus; evening elongation 26 1/4 from mean sun")
rec(id="IX.9.4", ref="9.9.4", body="mercury", observer="Ptolemy", observer_words="ἡμεῖς διὰ τοῦ ἀστρολάβου τηροῦντες",
    era="Antoninus 2", nab=884 + 2, month=12, day=23, part="morning",
    date_words="τῷ δὲ βʹ ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους Μεσορὴ εἰς τὴν κδʹ ὄρθρου",
    date_note="the day numeral before 'εἰς τὴν κδʹ' is missing in the export; 'the morning into the 24th' fixes the night 23/24",
    emend=dict(month=12, day=20, label="Nab 886 Mesore 20/21, morning",
               why="TEXTUAL CRUX. As printed (morning into Mesore 24) Ptolemy's tables give a mean sun of Cancer 13.27, but the "
                   "sentence states 'Καρκίνου μοίρας ῑ καὶ γ´' (Cancer 10 1/3) and 9.9.2 requires the mean sun a quadrant from "
                   "the apogee, as in IX.9.3 (Cancer 10 1/12). Mesore 20/21 reproduces 100.31 deg. Both readings are carried; "
                   "the interval is a fork."),
    phen="GE", side="W",
    phen_words="τηροῦντες τὴν μεγίστην αὐτοῦ διάστασιν",
    side_words="ὥστε γεγονέναι καὶ τὴν ἑῴαν μεγίστην ἀπόστασιν",
    ref_star="aldebaran", ref_star_words="διοπτεύοντες αὐτὸν πρὸς τὴν λαμπρὰν Ὑάδα",
    ptol_lon=Z("Gemini", 20 + 1/12), ptol_mean_sun=Z("Cancer", 10 + 1/3),
    measured="astrolabe longitude (Gemini 20 1/12) against Aldebaran; morning elongation 20 1/4 from mean sun (numeral damaged)")
rec(id="IX.10.3", ref="9.10.3", body="mercury", observer="Ptolemy", observer_words="ἡμεῖς μὲν γὰρ ἐτηρήσαμεν",
    era="Antoninus 2", nab=884 + 2, month=11, day=2, part="h_before_midnight", hours=4.5,
    date_words="τῷ βʹ ἔτει Ἀντωνίνου, ὅ ἦν κατὰ τὸ ωπϚʹ ἔτος ἀπὸ Ναβονασσάρου, κατʼ Αἰγυπτίους Ἐπιφὶ βʹ εἰς τὴν γʹ",
    time_words="ἦν ὁ χρόνος ἐν Ἀλεξανδρείᾳ πρὸ δ U+2220ʹ ὡρῶν ἰσημερινῶν τοῦ εἰς τὴν γʹ μεσονυκτίου",
    phen="beforeGE", side="E",
    phen_words="μηδέπω ἐπὶ τὴν μεγίστην ἑσπερίαν ἀπόστασιν ἐληλυθότα",
    ref_star="regulus", ref_star_words="διοπτευόμενος πρὸς τὸν ἐπὶ τῆς καρδίας τοῦ Λέοντος",
    moon=dict(dlon=+1 - 0 + 1/6, words="τότε δὲ καὶ τοῦ κέντρου τῆς σελήνης ὑπελείπετο μοῖραν α καὶ ϛʹ",
              reading="Mercury 1 1/6 deg to the rear (east) of the Moon's centre",
              ptol_moon_app=Z("Gemini", 16 + 20/60)),
    ptol_lon=Z("Gemini", 17.5), ptol_mean_sun=Z("Taurus", 22 + 34/60),
    measured="astrolabe longitude of Mercury against Regulus and its distance from the Moon; Moon's apparent place computed by Ptolemy")
rec(id="IX.10.6a", ref="9.10.6", body="mercury", observer="unnamed (Dionysian-calendar record)", observer_words="",
    era="Dionysian 21 Scorpion 22 = Nab 484 Thoth 18/19", nab=484, month=1, day=18, part="morning",
    date_words="τῷ καʹ ἔτει κατὰ Διονύσιον, ὃ ἦν κατὰ τὸ υπδ ἔτος ἀπὸ Ναβονασσάρου, Σκορπιῶνος κβ κατʼ Αἰγυπτίους Θὼθ ιηʹ εἰς τὴν ιθʹ",
    phen="beforeGE", side="W",
    phen_words="ἑῷος ὁ Στίλβων",
    before_words="ὅτι οὐδέπω ἐπὶ τὴν μεγίστην ἑῴαν ἀπόστασιν ἐληλύθει",
    stars=[dict(kind="line_east", star="beta1_sco", star2="delta_sco", dist=+0.5,
                words="τῆς διὰ τοῦ βορείου μετώπου τοῦ Σκορπίου καὶ μέσου εὐθείας ἀπεῖχεν εἰς τὰ ὑπολειπόμενα σελήνην",
                reading="one moon (0.5 deg) to the rear (east) of the line through beta Sco and delta Sco"),
           dict(kind="offset", star="beta1_sco", dlon=None, dlat=+1.0,
                words="πρὸς ἄρκτους δὲ τοῦ βορείου μετώπου διεῖχεν β σελήνας",
                reading="two moons (1 deg) north of beta Sco")],
    ptol_lon=None, ptol_mean_sun=Z("Scorpius", 20 + 5/6), mean_sun_words="ἐπεῖχεν ὁ μέσος ἥλιος τῇ ιθʹ τοῦ Θὼθ ὄρθρου καθʼ ἡμᾶς Σκορπίου μοίρας κ U+2220ʹγ΄",
    measured="Mercury relative to the forehead of Scorpius; Ptolemy: not yet at greatest morning elongation")
rec(id="IX.10.6b", ref="9.10.6", body="mercury", observer="unnamed (Dionysian-calendar record)", observer_words="",
    era="Dionysian 21 Scorpion 26 (= 4 days after IX.10.6a, i.e. Nab 484 Thoth 22/23)", nab=484, month=1, day=22, part="morning",
    date_words="μετὰ δ ἡμέρας τῇ κϚʹ τοῦ Σκορπιῶνος",
    phen="pos", side="W",
    phen_words="τῆς αὐτῆς εὐθείας διεῖχεν εἰς τὰ ἑπόμενα ὅλην καὶ ἡμίσειαν σελήνην",
    stars=[dict(kind="line_east", star="beta1_sco", star2="delta_sco", dist=+0.75,
                words="τῆς αὐτῆς εὐθείας διεῖχεν εἰς τὰ ἑπόμενα ὅλην καὶ ἡμίσειαν σελήνην",
                reading="1 1/2 moons (0.75 deg) east of the same line")],
    ptol_lon=None, ptol_mean_sun=None,
    measured="Mercury relative to the same line, 4 days later (the interval is stated)")

# =============================== BOOK X : VENUS =============================
rec(id="X.1.3", ref="10.1.3", body="venus", observer="Theon", observer_words="ἐν μὲν γὰρ ταῖς παρὰ Θέωνος τοῦ μαθηματικοῦ δοθείσαις ἡμῖν",
    era="Hadrian 16", nab=863 + 16, month=8, day=21, part="evening",
    date_words="τῷ ιϚʹ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Φαρμουθὶ κα· εἰς τὴν κβ΄",
    phen="GE", side="E",
    phen_words="ὁ τῆς Ἀφροδίτης ἑσπέριος τὸ πλεῖστον ἀπέστη τοῦ ἡλίου",
    stars=[dict(kind="offset", star="alcyone", dlon=-1.5, dlat=-0.25,
                words="προηγούμενος τοῦ μέσου τῆς Πλειάδος τὸ τῆς Πλειάδος μῆκος· ἐδόκει δὲ καὶ μικρῷ νοτιώτερος αὐτὴν παραπορεύεσθαι",
                reading="west of the middle of the Pleiades by the Pleiades' length (Ptolemy: about 1 1/2 deg), a little to the south")],
    ptol_lon=Z("Taurus", 1.5), ptol_mean_sun=Z("Pisces", 14.25),
    measured="Venus relative to the Pleiades; evening elongation 47 1/4 from mean sun")
rec(id="X.1.4", ref="10.1.4", body="venus", observer="Ptolemy", observer_words="ἡμεῖς δὲ ἐτηρήσαμεν",
    era="Antoninus 4 (export reads ιδʹ = 14; see note)", nab=884 + 4, month=1, day=11, part="morning",
    date_words="τῷ ιδʹ ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους Θὼθ ιαʹ εἰς τὴν ιβʹ",
    nab_note="TEXTUAL CRUX. The export reads 'ιδʹ' (14th year of Antoninus = Nab 898). Ptolemy's own stated mean sun "
             "for the observation (Leo 5 3/4 = 125.75 deg) is reproduced by his solar tables at Antoninus 4 = Nab 888 "
             "(125.70 deg) and not at Antoninus 14 = Nab 898 (123.26 deg), so the text itself fixes the year as 4 "
             "(computed by me with records.py). Carried as Nab 888; kept OUT of the control sets because of the crux.",
    phen="GE", side="W",
    phen_words="τὸν τῆς Ἀφροδίτης ἑῷον τὸ πλεῖστον ἀποστάντα τοῦ ἡλίου",
    stars=[dict(kind="offset", star="zeta_gem", dlon=+0.125, dlat=+0.125,
                words="ἀπεῖχεν τοῦ μέσου γόνατος τῶν Διδύμων πρὸς ἄρκτους καὶ ἀνατολὰς σελήνης μιᾶς διχομήνου τὸ ἥμισυ",
                reading="half a full-moon diameter (0.25 deg) to the north-east of the 'middle knee' of Gemini "
                        "(identified as zeta Gem from Ptolemy's longitude Gemini 18 1/4; my identification)")],
    ptol_lon=Z("Gemini", 18.5), ptol_mean_sun=Z("Leo", 5.75),
    measured="Venus relative to a Gemini star; morning elongation 47 1/4 from mean sun")
rec(id="X.1.5", ref="10.1.5", body="venus", observer="Theon", observer_words="ὁμοίως ἐν μὲν ταῖς παρὰ Θέωνος εὕρομεν",
    era="Hadrian 12", nab=863 + 12, month=3, day=21, part="morning",
    date_words="τῷ ιβ΄ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Ἀθὺρ καʹ εἰς τὴν κβʹ",
    phen="GE", side="W",
    phen_words="ὁ τῆς Ἀφροδίτης ἑῷος τὸ πλεῖστον ἀπέστη τοῦ ἡλίου",
    stars=[dict(kind="offset", star="beta_vir", dlon=+1.5, dlat=+0.5, cmp="lon_le",
                words="ὑπολειπόμενος τοῦ ἐπʼ ἄκρας τῆς νοτίου πτέρυγος τῆς Παρθένου Πλειάδος μῆκος ἢ ἔλασσον τῷ ἑαυτοῦ μεγέθει· ἐδόκει δὲ βορειότερος παραπορεύεσθαι τὸν ἀστέρα σελήνῃ μιᾷ",
                reading="east of the star at the tip of Virgo's southern wing (beta Vir) by a Pleiad-length (1 1/2 deg) or less; "
                        "passing it one moon (0.5 deg) to the north")],
    ptol_lon=Z("Virgo", 1/3), ptol_mean_sun=Z("Libra", 17 + 0.5 + 1/3 + 1/30),
    measured="Venus relative to beta Vir; morning elongation 47 8/15 from mean sun")
rec(id="X.1.6", ref="10.1.6", body="venus", observer="Ptolemy", observer_words="ἡμεῖς δὲ",
    era="Hadrian 21", nab=863 + 21, month=6, day=9, part="evening",
    date_words="τῷ καʹ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Μεχὶρ θ εἰς τὴν ιʹ ἐσπέρας",
    phen="GE", side="E",
    phen_words="ἐτηρήσαμεν τὸν τῆς Ἀφροδίτης τὸ πλεῖστον ἀποστάντα τοῦ ἡλίου",
    stars=[dict(kind="nearest", candidates=["lambda_aqr", "phi_aqr", "psi1_aqr", "psi2_aqr", "psi3_aqr"],
                dlon=-1/3, dlat=0.0,
                words="προηγεῖτο τοῦ βορειοτάτου τῶν ὡς ἐν τετραπλεύρῳ δ μετὰ τὸν ἑπόμενον καὶ ἐπʼ εὐθείας τοῖς βουβῶσι τοῦ Ὑδροχόου δύο μέρη ἔγγιστα σελήνης διχομήνου καὶ ἐδόκει καταλάμπειν τὸν ἀστέρα",
                reading="west of the northernmost of an Aquarius quadrilateral by about 2/3 of a full moon (1/3 deg), seeming to "
                        "outshine/touch it (star identification uncertain: nearest of lambda, phi, psi1-3 Aqr)")],
    ptol_lon=Z("Aquarius", 19 + 3/5), ptol_mean_sun=Z("Capricorn", 2 + 1/15),
    measured="Venus relative to an Aquarius star; evening elongation 47 8/15 from mean sun")
rec(id="X.2.3", ref="10.2.3", body="venus", observer="Theon", observer_words="ἐν μὲν γὰρ ταῖς παρὰ Θέωνος ἡμῖν δοθείσαις εὑρίσκομεν",
    era="Hadrian 13", nab=863 + 13, month=11, day=2, part="morning",
    date_words="τῷ ιγʹ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Ἐπιφὶ β εἰς τὴν γ",
    phen="GE", side="W",
    phen_words="ἑῷος ὁ τῆς Ἀφροδίτης τὸ πλεῖστον ἀπέστη τοῦ ἡλίου",
    stars=[dict(kind="note_only", star="gamma2_ari",
                words="τῆς εὐθείας τῆς διὰ τοῦ ἡγουμένου τῶν ἐν τῇ κεφαλῇ τοῦ Κριοῦ γ καὶ τοῦ ἐπὶ τοῦ ὀπισθίου σκέλους προηγούμενος μοίρᾳ α καὶ δύο πεμπτημορίοις",
                reading="1 2/5 deg west of the line from the leading star of the three in Aries' head (gamma Ari) to the star on "
                        "the hind leg (not identified here); positional check not computed")],
    ptol_lon=Z("Aries", 10.6), ptol_mean_sun=Z("Taurus", 25.4),
    measured="Venus relative to Aries stars; morning elongation 44 4/5 from mean sun")
rec(id="X.2.4", ref="10.2.4", body="venus", observer="Ptolemy", observer_words="ἡμεῖς δὲ ἐτηρήσαμεν",
    era="Hadrian 21", nab=863 + 21, month=5, day=2, part="evening",
    date_words="τῷ κα· ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Τυβὶ βʹ εἰς τὴν γʹ ἑσπέρας",
    phen="GE", side="E",
    phen_words="τὸν τῆς Ἀφροδίτης τὸ πλεῖστον ἀποστάντα τοῦ ἡλίου",
    ref_star=None, ref_star_words="διοπτευόμενος πρὸς τοὺς ἐν τοῖς κέρασι τοῦ Αἴγόκερω",
    ptol_lon=Z("Capricorn", 12 + 5/6), ptol_mean_sun=Z("Scorpius", 25.5),
    measured="astrolabe longitude (Capricorn 12 5/6) against the stars in Capricorn's horns; evening elongation 47 1/3 from mean sun")
rec(id="X.3.2a", ref="10.3.2", body="venus", observer="Ptolemy", observer_words="ἐτηρήσαμεν",
    era="Hadrian 18", nab=863 + 18, month=8, day=2, part="morning",
    date_words="τῷ ιη΄ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Φαρμουθὶ β΄ εἰς τὴν γ΄",
    phen="GE", side="W",
    phen_words="καθʼ ἣν ἑῷος ὁ τῆς Ἀφροδίτης τὸ πλεῖστον ἀπέστη τοῦ ἡλίου",
    ref_star="antares", ref_star_words="διοπτευόμενος πρὸς τὸν καλούμενον Ἀντάρην",
    ptol_lon=Z("Capricorn", 11 + 7/12), ptol_mean_sun=Z("Aquarius", 25.5),
    measured="astrolabe longitude (Capricorn 11 7/12) against Antares; morning elongation 43 11/12 from mean sun")
rec(id="X.3.2b", ref="10.3.2", body="venus", observer="Ptolemy", observer_words="τὴν δʼ ἑτέραν ἐτηρήσαμεν",
    era="Antoninus 3", nab=884 + 3, month=8, day=4, part="evening",
    date_words="τῷ γ΄ ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους Φαρμουθὶ δ΄ εἰς τὴν ε΄ ἐσπέρας",
    phen="GE", side="E",
    phen_words="τὸ πλεῖστον ὁ τῆς Ἀφροδίτης ἀπέσχεν τοῦ ἡλίου",
    ref_star="aldebaran", ref_star_words="διοπτευόμενος πρὸς τὴν λαμπρὰν Ὑάδα",
    ptol_lon=Z("Aries", 10 + 5/6), ptol_mean_sun=Z("Aquarius", 25.5),
    measured="astrolabe longitude (Aries 10 5/6) against Aldebaran; evening elongation 48 1/3 from mean sun")
rec(id="X.4.3", ref="10.4.3", body="venus", observer="Ptolemy", observer_words="ἡμεῖς μὲν οὖν ἐτηρήσαμεν",
    era="Antoninus 2", nab=884 + 2, month=5, day=29, part="h_after_midnight", hours=4.75,
    date_words="τῷ β΄ ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους Τυβὶ κθ΄εἰς τὴν λ΄",
    time_words="ὁ δὲ χρόνος ἦν μετὰ δ U+2220΄ δ΄ ὥρας ἰσημερινὰς τοῦ μεσονυκτίου",
    phen="afterGE", side="W",
    phen_words="τὸν τῆς Ἀφροδίτης ἀστέρα μετὰ τὴν μεγίστην ἑῴαν ἀπόστασιν",
    ref_star="spica", ref_star_words="πρὸς τὸν Στάχυν",
    stars=[dict(kind="note_only", star="beta1_sco",
                words="μεταξὺ καὶ ἐπʼ εὐθείας ἦν τῷ τε βορειοτάτῳ τῶν ἐν τῷ μετώπῳ τοῦ Σκορπίου καὶ τῷ φαινομένῳ κέντρῳ τῆς σελήνης",
                reading="between and in line with beta Sco and the Moon's apparent centre")],
    moon=dict(dlon=-0.25, words="τοῦ δὲ κέντρου τῆς σελήνης προηγεῖτο ἡμιόλιον, οὗ ὑπελείπετο τοῦ βορειοτάτου τῶν ἐν τῷ μετώπῳ",
              reading="Venus preceded (was west of) the Moon's centre by 1 1/2 times its distance east of beta Sco; with Ptolemy's "
                      "own longitudes (Venus Scorpius 6;30, beta Sco 6;20 in 10.9.2, Moon 6;45) that is about 1/4 deg",
              ptol_moon_app=Z("Scorpius", 6 + 45/60)),
    ptol_lon=Z("Scorpius", 6.5), ptol_mean_sun=Z("Sagittarius", 22 + 9/60),
    measured="astrolabe longitude of Venus against Spica; alignment with beta Sco and the Moon")
rec(id="X.4.6a", ref="10.4.6", body="venus", observer="Timocharis", observer_words="ἢν ἀναγράφει Τμόχαρις οὕτως",
    era="Philadelphus 13 = Nab 476", nab=476, month=12, day=17, part="morning",
    date_words="τῷ ιγ΄ ἔτει Φιλαδέλφου κατʼ Αἰγυπτίους Μεσορὴ ιζ΄ εἰς τὴν ιη΄ ὥρᾳ ιβ΄",
    phen="occ", side="W",
    phen_words="ὁ τῆς Ἀφροδίτης ἐφαίνετο κατειληφὼς τὸν ἀντικείμενον τῷ Προτρυγητῆρι ἀκριβῶς",
    after_words="παρεληλύθει δὲ καὶ ἐνταῦθα ὁ τῆς Ἀφροδίτης τὴν μεγίστην ἑῴαν ἀπόστασιν",
    stars=[dict(kind="conj", star="eta_vir",
                words="κατειληφὼς τὸν ἀντικείμενον τῷ Προτρυγητῆρι ἀκριβῶς",
                reading="Venus exactly overtook the star 'opposite Vindemiatrix' (Ptolemy: the star after the tip of the southern "
                        "wing of Virgo, at Virgo 8 1/4 in his catalogue = eta Vir)")],
    ptol_lon=Z("Virgo", 4 + 1/6), ptol_mean_sun=Z("Libra", 17 + 3/60),
    measured="Venus-star conjunction at the 12th hour (dawn); Ptolemy: Venus already past greatest morning elongation")
rec(id="X.4.6b", ref="10.4.6", body="venus", observer="Timocharis (as reported by Ptolemy)", observer_words="ἐξ ὧν φησιν ὁ Τιμόχαρις",
    era="4 days after X.4.6a (Nab 476 Mesore 21/22)", nab=476, month=12, day=21, part="morning",
    date_words="μετὰ γὰρ δ ἡμέρας τῆς προκειμένης τηρήσεως τῇ κα τοῦ Μεσορὴ εἰς τὴν κβ΄",
    phen="pos", side="W",
    phen_words="ἐπεῖχεν κατὰ τὰς ἡμετέρας ἀρχὰς Παρθένου μοίρας η U+2220΄γ΄",
    ptol_lon=Z("Virgo", 8 + 5/6), ptol_mean_sun=Z("Libra", 20 + 59/60),
    measured="Venus' longitude 4 days later (Ptolemy's conversion of Timocharis' report); used to show Venus past greatest elongation")

# --------------------------------- Mars ------------------------------------
rec(id="X.7.3a", ref="10.7.3", body="mars", observer="Ptolemy", observer_words="ἐτηρήσαμεν",
    era="Hadrian 15", nab=863 + 15, month=5, day=26, part="h_after_midnight", hours=1,
    date_words="τῷ ιε΄ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Τυβὶ κς΄ εἰς τὴν κζ΄ μετὰ μίαν ὥραν ἰσημερινὴν τοῦ μεσονυκτίου",
    phen="opp", phen_words="τριῶν ἀκρωνύκτων τῶν πρὸς τὴν μέσην τοῦ ἡλίου πάροδον διαμέτρων",
    phen_ref="10.7.2", ptol_lon=Z("Gemini", 21), ptol_mean_sun=None,
    measured="opposition to the mean sun, time and place reduced from astrolabe observations")
rec(id="X.7.3b", ref="10.7.3", body="mars", observer="Ptolemy", observer_words="",
    era="Hadrian 19", nab=863 + 19, month=8, day=6, part="h_before_midnight", hours=3,
    date_words="τῷ ιθ΄ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Φαρμουθὶ ς΄ εἰς τὴν ζ΄ πρὸ ὡρῶν γ τοῦ μεσονυκτίου",
    phen="opp", phen_words="τριῶν ἀκρωνύκτων τῶν πρὸς τὴν μέσην τοῦ ἡλίου πάροδον διαμέτρων", phen_ref="10.7.2", ptol_lon=Z("Leo", 28 + 50/60), ptol_mean_sun=None,
    measured="opposition to the mean sun (reduced)")
rec(id="X.7.3c", ref="10.7.3", body="mars", observer="Ptolemy", observer_words="",
    era="Antoninus 2", nab=884 + 2, month=11, day=12, part="h_before_midnight", hours=2,
    date_words="τῷ β΄ ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους Ἐπιφὶ ιβ΄ εἰς τὴν ιγ΄ πρὸ δύο ὡρῶν ἰσημερινῶν τοῦ μεσονυκτίου",
    phen="opp", phen_words="τριῶν ἀκρωνύκτων τῶν πρὸς τὴν μέσην τοῦ ἡλίου πάροδον διαμέτρων", phen_ref="10.7.2", ptol_lon=Z("Sagittarius", 2 + 34/60), ptol_mean_sun=None,
    measured="opposition to the mean sun (reduced)")
rec(id="X.8.2", ref="10.8.2", body="mars", observer="Ptolemy", observer_words="ἣν διωπτεύσαμεν",
    era="Antoninus 2", nab=884 + 2, month=11, day=15, part="h_before_midnight", hours=3,
    date_words="τῷ β΄ ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους Ἐπιφὶ ιε΄ εἰς τὴν ις΄ πρὸ τριῶν ὡρῶν ἰσημερινῶν τοῦ μεσονυκτίου",
    phen="pos", phen_words="μετὰ γ ἔγγιστα ἡμέρας τῆς γ΄ ἀκρωνύκτου",
    ref_star="spica", ref_star_words="τοῦ μὲν οὖν ἐπὶ τοῦ Στάχυος διοπτευομένου πρὸς τὴν οἰκείαν θέσιν",
    moon=dict(dlon=+1 + 3/5, words="καὶ τοῦ κέντρου τῆς σελήνης ἀπ- έχων ἐφαίνετο εἰς τὰ ἑπόμενα τὴν αὐτὴν μίαν μοῖραν καὶ γ πεμπτημόρια",
              reading="Mars 1 3/5 deg to the east of the Moon's centre", ptol_moon_app=Z("Sagittarius", 0)),
    ptol_lon=Z("Sagittarius", 1 + 3/5), ptol_mean_sun=Z("Gemini", 5 + 27/60),
    measured="astrolabe longitude of Mars against Spica and its distance from the Moon, about 3 days after the third opposition")
rec(id="X.9.2", ref="10.9.2", body="mars", observer="unnamed (Dionysian-calendar record)", observer_words="",
    era="Dionysian 13 Aigon 25 = Philip 52 = Nab 476 Athyr 20/21", nab=476, month=3, day=20, part="morning",
    date_words="τῷ ιγ΄ ἔτει κατὰ Διονύσιον Αἴγωνος κε΄",
    date_words_nab="κατὰ τὸ υοϚ΄ ἔτος ἀπὸ Ναβονασσάρου, κατʼ Αἰγυπτίους Ἀθὺρ κ΄ εἰς τὴν κα΄ ὄρθρου",
    phen="occ", phen_words="ἑῷος ὁ τοῦ Ἄρεως τῷ βορείῳ μετώπῳ τοῦ Σκορπίου ἐδόκει ἐπιπροσθετηκέναι",
    stars=[dict(kind="conj", star="beta1_sco", words="τῷ βορείῳ μετώπῳ τοῦ Σκορπίου ἐδόκει ἐπιπροσθετηκέναι",
                reading="Mars seemed to have occulted beta Sco (morning)")],
    ptol_lon=Z("Scorpius", 2.25), ptol_mean_sun=Z("Capricorn", 23 + 54/60),
    measured="Mars-star occultation (morning)")

# =============================== BOOK XI ===================================
rec(id="XI.1.2a", ref="11.1.2", body="jupiter", observer="Ptolemy", observer_words="ἐτηρήσαμεν διὰ τῶν ἀστρολάβων ὀργάνων",
    era="Hadrian 17", nab=863 + 17, month=11, day=1, part="h_before_midnight", hours=1,
    date_words="τῷ ιζ΄ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Ἐπιφὶ α΄ εἰς τὴν β΄ πρὸ μιᾶς ὥρας τοῦ μεσονυκτίου",
    phen="opp", phen_words="γ ἀκρωνύκτους διαμέτρους πρὸς τὴν μέσην τοῦ ἡλίου πάροδον",
    ptol_lon=Z("Scorpius", 23 + 11/60), ptol_mean_sun=None, measured="opposition to the mean sun (reduced)")
rec(id="XI.1.2b", ref="11.1.2", body="jupiter", observer="Ptolemy", observer_words="",
    era="Hadrian 21", nab=863 + 21, month=2, day=13, part="h_before_midnight", hours=2,
    date_words="τῷ κα΄ ἔτει Φαωφὶ ιγ΄ εἰς τὴν ιδ΄ πρὸ β ὡρῶν τοῦ μεσονυκτίου",
    phen="opp", phen_words="γ ἀκρωνύκτους διαμέτρους πρὸς τὴν μέσην τοῦ ἡλίου πάροδον",
    ptol_lon=Z("Pisces", 7 + 54/60), ptol_mean_sun=None, measured="opposition to the mean sun (reduced)")
rec(id="XI.1.2c", ref="11.1.2", body="jupiter", observer="Ptolemy", observer_words="",
    era="Antoninus 1", nab=884 + 1, month=3, day=20, part="h_after_midnight", hours=5,
    date_words="τῷ α΄ ἔτει Ἀντωνίνου Ἀθὺρ κ΄ εἰς τὴν κα΄ μετὰ ε ὥρας τοῦ μεσονυκτίου",
    phen="opp", phen_words="γ ἀκρωνύκτους διαμέτρους πρὸς τὴν μέσην τοῦ ἡλίου πάροδον",
    ptol_lon=Z("Aries", 14 + 23/60), ptol_mean_sun=None, measured="opposition to the mean sun (reduced)")
rec(id="XI.2.2", ref="11.2.2", body="jupiter", observer="Ptolemy", observer_words="ἣν διωπτεύσαμεν",
    era="Antoninus 2", nab=884 + 2, month=12, day=26, part="h_after_midnight", hours=5,
    date_words="τῷ β΄ ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους Μεσορὴ κϚ΄ εἰς τὴν κζ΄ πρὸ τῆς τοῦ ἡλίου ἀνατολῆς, τουτέστιν μετὰ ε ὥρας ἔγγιστα ἰσημερινὰς τοῦ μεσονυκτίου",
    phen="pos", phen_words="πρὸ τῆς τοῦ ἡλίου ἀνατολῆς",
    ref_star="aldebaran", ref_star_words="πρὸς μὲν τὴν λαμπρὰν Ὑάδα διοπτευόμενος",
    moon=dict(dlon=0.0, words="τῷ δὲ κέντρῳ τῆς σελήνης νοτιωτέρας οὔσης ἐξ ἴσου ἐφαίνετο",
              reading="Jupiter appeared level (same longitude) with the Moon's centre, the Moon being further south",
              ptol_moon_app=Z("Gemini", 15 + 45/60)),
    ptol_lon=Z("Gemini", 15.75), ptol_mean_sun=Z("Cancer", 16 + 11/60),
    measured="astrolabe longitude of Jupiter against Aldebaran and relative to the Moon, before sunrise")
rec(id="XI.3.2", ref="11.3.2", body="jupiter", observer="unnamed (Dionysian-calendar record)", observer_words="",
    era="Dionysian 45 Parthenon 10 = Philip 83 (Nab 507) Epiphi 17/18", nab=424 + 83, month=11, day=17, part="morning",
    date_words="τῷ με΄ ἔτει κατὰ Διονύσιον Παρθενῶνος ι΄",
    date_words_nab="κατὰ τὸ πγ΄ ἔτος ἀπὸ τῆς Ἀλεξάνδρου τελευτῆς κατʼ Αἰγυπτίους Ἐπιφὶ ιζ΄ εἰς τὴν ιη΄ ὄρθρου",
    phen="occ", phen_words="ὁ τοῦ Διὸς ἀστὴρ ἑῷος ἐπεκάλυψεν τὸν νότιον Ὄνον",
    stars=[dict(kind="conj", star="delta_cnc", words="ἐπεκάλυψεν τὸν νότιον Ὄνον",
                reading="Jupiter occulted the southern Ass (delta Cnc), morning")],
    ptol_lon=Z("Cancer", 7 + 33/60), ptol_mean_sun=Z("Virgo", 9 + 56/60),
    measured="Jupiter-star occultation (morning)")
rec(id="XI.5.2a", ref="11.5.2", body="saturn", observer="Ptolemy", observer_words="διὰ τῶν ἀστρολάβων ὀργάνων ἐτηρήσαμεν",
    era="Hadrian 11", nab=863 + 11, month=9, day=7, part="evening",
    date_words="τῷ ῑα ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Παχὼν ζ΄ εἰς τὴν η΄ ἑσπέρας",
    phen="opp", phen_words="τρεῖς ἀκρωνύκτους στάσεις τοῦ ἀστέρος πρὸς τὴν μέσην τοῦ ἡλίου πάροδον διαμέτρους",
    ptol_lon=Z("Libra", 1 + 13/60), ptol_mean_sun=None, measured="opposition to the mean sun")
rec(id="XI.5.2b", ref="11.5.2", body="saturn", observer="Ptolemy", observer_words="",
    era="Hadrian 17", nab=863 + 17, month=11, day=18, part="h_after_noon", hours=4,
    date_words="τὸ ιζ΄ ἔτει ὁμοίως Ἀδριανοῦ κατʼ Αἰγυπτίους Ἐπιφὶ ιη΄",
    time_words="μετὰ δ ὥρας τῆς μεσημβρίας τῆς ἐν τῇ ιη΄",
    phen="opp", phen_words="τὸν δὲ τῆς ἀκριβοῦς διαμετρήσεως χρόνον καὶ τόπον συνελογισάμεθα",
    ptol_lon=Z("Sagittarius", 9 + 40/60), ptol_mean_sun=None, measured="opposition to the mean sun, time computed by Ptolemy")
rec(id="XI.5.2c", ref="11.5.2", body="saturn", observer="Ptolemy", observer_words="",
    era="Hadrian 20", nab=863 + 20, month=12, day=24, part="noon",
    date_words="τῷ κ΄ ἔτει πάλιν Ἀδριανοῦ κατʼ Αἱγυπτίους Μεσορὴ κδ΄",
    time_words="γεγονέναι κατʼ αὐτὴν τὴν ἐν τῇ κδ΄ μεσημβρίαν",
    phen="opp", phen_words="τὸν μὲν χρόνον τῆς ἀκριβοῦς διαμετρήσεως ὡσαύτως ἐπελογισάμεθα",
    ptol_lon=Z("Capricorn", 14 + 14/60), ptol_mean_sun=None, measured="opposition to the mean sun, time computed by Ptolemy")
rec(id="XI.6.2", ref="11.6.2", body="saturn", observer="Ptolemy", observer_words="ἣν ἡμεῖς ἐτηρήσαμεν",
    era="Antoninus 2", nab=884 + 2, month=6, day=6, part="h_before_midnight", hours=4,
    date_words="τῷ β΄ ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους Μεχὶρ Ϛ΄ εἰς τὴν ζ΄ πρὸ δ ὡρῶν ἰσημερινῶν τοῦ μεσονυκτίου",
    phen="pos", phen_words="ὁ τοῦ Κρόνου ἀστὴρ πρὸς μὲν τὴν λαμπρὰν Ὑάδα διοπτευόμενος",
    ref_star="aldebaran", ref_star_words="πρὸς μὲν τὴν λαμπρὰν Ὑάδα διοπτευόμενος",
    moon=dict(dlon=+0.5, words="καὶ τοῦ κέντρου δὲ τῆς σελήνης ὑπελείπετο ἥμισυ ἔγγιστα α μοίρας· τοσοῦτον γὰρ αὐτῆς ἀπεῖχεν τοῦ βορείου κέρατος",
              reading="Saturn about 1/2 deg to the rear (east) of the Moon's centre, the same distance from its northern horn",
              ptol_moon_app=Z("Aquarius", 8 + 34/60)),
    ptol_lon=Z("Aquarius", 9 + 1/15), ptol_mean_sun=Z("Sagittarius", 28 + 41/60),
    measured="astrolabe longitude of Saturn against Aldebaran and relative to the Moon")
rec(id="XI.7.2", ref="11.7.2", body="saturn", observer="unnamed (Chaldean-calendar record)", observer_words="",
    era="Chaldean 82 Xanthikos 5 = Nab 519 Tybi 14", nab=519, month=5, day=14, part="evening",
    date_words="τῷ πβ΄ ἔτει κατὰ Χαλδαίους Ξανθικοῦ ε΄ ἐσπέρας",
    date_words_nab="κατὰ τὸ φιθ΄ ἔτος ἀπὸ Ναβονασσάρου κατʼ Αἰγυπτίους Τυβὶ ιδ΄ ἑσπέρας",
    phen="pos", phen_words="ὁ τοῦ Κρόνου ἀστὴρ ὑποκάτω ἦν τοῦ νοτίου ὤμου τῆς Παρθένου δακτύλους β",
    stars=[dict(kind="offset", star="gamma_vir", dlon=0.0, dlat=-2/12,
                words="ὑποκάτω ἦν τοῦ νοτίου ὤμου τῆς Παρθένου δακτύλους β",
                reading="2 fingers below the southern shoulder of Virgo (gamma Vir, from Ptolemy's longitude Virgo 13 1/6); "
                        "a finger taken as 1/12 deg (my gloss); Ptolemy gives Saturn the star's longitude")],
    ptol_lon=Z("Virgo", 9.5), ptol_mean_sun=Z("Pisces", 6 + 10/60),
    measured="Saturn relative to gamma Vir (evening)")

# ========================= OTHER BOOKS (anchors) ===========================
rec(id="III.1.10", ref="3.1.10", body="sun", observer="Ptolemy", observer_words="ἡμεῖς δὲ",
    era="Philip 463 (= Antoninus 3, 3.1.9) = Nab 887", nab=424 + 463, month=9, day=7, part="h_after_noon", hours=1,
    date_words="τῷ υξγ΄ ἀπὸ τῆς Ἀλεξάνδρου τελευτῆς ἐαρινὴν ἰσημερίαν εὑρίσκομεν γεγενημένην τῇ ζ΄ τοῦ Παχὼν μετὰ μίαν ὥραν ἔγγιστα τῆς μεσημβρίας",
    phen="equinox", phen_words="ἐαρινὴν ἰσημερίαν εὑρίσκομεν γεγενημένην",
    ptol_lon=0.0, ptol_mean_sun=None, measured="spring equinox (observed with the equinoctial ring / meridian instruments)")
rec(id="IV.6.14", ref="4.6.14", body="moon", observer="Ptolemy (4.6.13: 'ἡμῖν ἐν Ἀλεξανδρείᾳ τετηρημένων')", observer_words="",
    era="Hadrian 19", nab=863 + 19, month=4, day=2, part="h_before_midnight", hours=1,
    date_words="τῷ ιθʹ ἔτει Ἀδριανοῦ κατʼ Αἰγυπτίους Χοϊὰκ βʹ εἰς τὴν γʹ, τὸν δὲ μέσον χρόνον ἐπελογισάμεθα γεγονέναι πρὸ α ὥρας ἰσημερινῆς τοῦ μεσονυκτίου",
    phen="ecl", phen_words="ἐξέλειπεν ἀπʼ ἄρκτων τὸ U+2220ʹ καὶ γʹ τῆς διαμέτρου",
    ptol_lon=None, ptol_mean_sun=None, measured="lunar eclipse, 1/2 + 1/3 of the diameter from the north; mid-eclipse computed")
rec(id="V.3.2", ref="5.3.2", body="moon", observer="Ptolemy", observer_words="διωπτεύσαμεν τόν τε ἥλιον καὶ τὴν σελήνην",
    era="Antoninus 2", nab=884 + 2, month=7, day=25, part="h_before_noon", hours=5.25,
    date_words="τῷ β΄ ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους Φαμενὼθ κε΄ μετὰ μὲν τὴν ἀνατολὴν τὴν τοῦ ἡλίου, πρὸ πέντε δὲ καὶ δʼ ὡρῶν ἰσημερινῶν τῆς μεσημβρίας",
    phen="moonsun", phen_words="ὡς τεταρτημορίου τυγχάνειν ἔγγιστα τὴν μέσην ἀποχὴν τοῦ ἡλίου",
    moonsun=dict(stated=Z("Scorpius", 9 + 2/3) - Z("Aquarius", 18 + 5/6),
                 words="τοῦ γὰρ ἡλίου διοπτευομένου κατὰ Ὑδροχόου μοίρας ιη U+2220΄ γʹ καὶ μέσουρανούσης Τοξότου μοίρας δ΄ ἡ σελήνη ἐφαίνετο ἐπέχουσα Σκορπίου μοίρας θ",
                 reading="Sun sighted at Aquarius 18 5/6, Moon at Scorpius 9 + a damaged fraction ('θ Γ??', read 2/3): "
                         "Moon about 99 deg west of the Sun, seen after sunrise"),
    ptol_lon=None, ptol_mean_sun=Z("Aquarius", 16 + 27/60), measured="astrolabe sighting of Sun and Moon in daylight")
rec(id="VII.2.4", ref="7.2.4", body="moon", observer="Ptolemy", observer_words="ἐτηρήσαμεν",
    era="Antoninus 2", nab=884 + 2, month=8, day=9, part="h_after_noon", hours=5.5,
    date_words="τῷ β ἔτει Ἀντωνίνου κατʼ Αἰγυπτίους ἴαρμουθὶ θʹ μέλλοντος μὲν δύνειν ἐν Ἀλεξανδρείᾳ τοῦ ἡλίου",
    time_words="μετὰ ἐ U+2220ʹ ὥρας ἴσημερινὰς τῆς ἐν τῇ θʹμεσημβρίας",
    phen="moonsun", phen_words="τὴν φαινομένην σελήνην ἀπέχουσαν τοῦ ἡλίου",
    moonsun=dict(stated=92 + 1/8,
                 words="τὴν φαινομένην σελήνην ἀπέχουσαν τοῦ ἡλίου περὶ τὰς τρεῖς μοίρας τῶν Ἰχθύων διοπτευομένου τμήματα 9β καὶ η΄",
                 reading="apparent Moon 92 1/8 deg east of the Sun along the ecliptic, the Sun about to set "
                         "('9β' in the export is the numeral 92 with a damaged ninety-sign)"),
    ptol_lon=None, ptol_mean_sun=None, measured="astrolabe Sun-Moon distance at sunset (then Regulus vs Moon half an hour later)")


def _resolve():
    """Replace every licence string by the exact substring of its row (accent/prime variants differ in code points)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import greek
    T = rows()
    keys = ("date_words", "date_words_nab", "phen_words", "side_words", "extra_words", "observer_words",
            "ref_star_words", "time_words", "before_words", "after_words", "mean_sun_words")
    for r in R:
        for k in keys:
            w = r.get(k)
            if not w:
                continue
            ref = r["phen_ref"] if (k == "phen_words" and r.get("phen_ref")) else r["ref"]
            e = greek.exact(T[ref], w)
            if e is None:
                raise ValueError(f"{r['id']} {k}: not found in {ref}: {w}")
            r[k] = e
        for sub in r.get("stars", []) + ([r["moon"]] if r.get("moon") else []) + ([r["moonsun"]] if r.get("moonsun") else []):
            e = greek.exact(T[r["ref"]], sub["words"])
            if e is None:
                raise ValueError(f"{r['id']}: not found: {sub['words']}")
            sub["words"] = e
        if r.get("ge_claim_words"):
            e = greek.exact(T[r["ge_claim_ref"]], r["ge_claim_words"])
            if e is None:
                raise ValueError(f"{r['id']} ge_claim not found")
            r["ge_claim_words"] = e


def rows():
    out = {}
    for line in TSV.open(encoding="utf-8"):
        ref, _, txt = line.rstrip("\n").partition("\t")
        out[ref.replace(PRE, "")] = txt
    return out


_RESOLVED = False


def resolve():
    global _RESOLVED
    if not _RESOLVED:
        _resolve()
        _RESOLVED = True


def check_licences():
    T = rows()
    bad = []
    for r in R:
        txt = T[r["ref"]]
        for k in ("date_words", "date_words_nab", "phen_words", "side_words", "extra_words", "observer_words",
                  "ref_star_words", "time_words", "before_words", "after_words", "mean_sun_words"):
            w = r.get(k)
            if k == "phen_words" and r.get("phen_ref"):
                continue
            if w and w not in txt:
                bad.append((r["id"], k, w))
        for s in r.get("stars", []):
            if s["words"] not in txt:
                bad.append((r["id"], "star", s["words"]))
        if r.get("moon") and r["moon"]["words"] not in txt:
            bad.append((r["id"], "moon", r["moon"]["words"]))
        if r.get("moonsun") and r["moonsun"]["words"] not in txt:
            bad.append((r["id"], "moonsun", r["moonsun"]["words"]))
        if r.get("ge_claim_words") and r["ge_claim_words"] not in T[r["ge_claim_ref"]]:
            bad.append((r["id"], "ge_claim", r["ge_claim_words"]))
        if r.get("phen_ref") and r["phen_words"] not in T[r["phen_ref"]]:
            bad.append((r["id"], "phen_ref", r["phen_words"]))
    return bad


def civil_day_offset(part):
    return 1 if part in ("morning", "h_after_midnight") else 0


def ptolemy_mean_sun(r):
    """Ptolemy's mean sun (his own epoch and mean motion) at the record's local time."""
    jd_noon = nab_jd_noon(r["nab"], r["month"], r["day"])
    part = r["part"]
    if part == "evening":
        frac = 0.25                      # ~18h local
    elif part == "morning":
        frac = 0.75                      # ~6h local next day
    elif part == "h_before_midnight":
        frac = 0.5 - r["hours"] / 24
    elif part == "h_after_midnight":
        frac = 0.5 + r["hours"] / 24
    elif part == "h_after_noon":
        frac = r["hours"] / 24
    elif part == "h_before_noon":
        frac = -r["hours"] / 24
    else:
        frac = 0.0
    days = jd_noon - NAB_EPOCH_JD + frac
    return (PTOL_SUN_EPOCH + PTOL_SUN_N * days) % 360.0, days


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    resolve()
    bad = check_licences()
    print("licence-word mismatches:", len(bad))
    for b in bad:
        print("  ", b)
    print(f"Ptolemy mean daily solar motion = {PTOL_SUN_N:.10f} deg/day")
    for r in R:
        ms, days = ptolemy_mean_sun(r)
        st = r.get("ptol_mean_sun")
        d = "" if st is None else f"stated {st:8.3f}  diff {((st - ms + 180) % 360) - 180:+.3f}"
        print(f"{r['id']:10s} Nab {r['nab']:4d} {MONTHS[r['month']-1]:10s} {r['day']:2d} {r['part']:18s} "
              f"days {days:10.2f}  Ptolemy mean sun {ms:8.3f}  {d}")
