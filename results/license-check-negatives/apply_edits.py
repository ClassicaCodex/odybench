"""Apply the independent licence check to data/prereg/negatives.json in place.

Every clue row gets a "license_check" field ("ok" or "edited: <what and why>").
Edits are listed in docs/license-check-negatives.md. The pre-edit file is kept
at results/license-check-negatives/negatives.before.json.

Run:  py results/license-check-negatives/apply_edits.py
Read-only on data/text; writes only data/prereg/negatives.json.
Does not open any truth file or docs/research-controls.md.
"""
import json, os, sys

ROOT = r"C:\Projects\odybench"
PATH = os.path.join(ROOT, "data", "prereg", "negatives.json")
BEFORE = os.path.join(ROOT, "results", "license-check-negatives", "negatives.before.json")
AP = "\u02bc"  # the apostrophe the Perseus Greek files use
SEP = " \u2026 "

src = open(BEFORE, encoding="utf-8").read()
d = json.loads(src)
C = {c["clue_id"]: c for c in d["clues"]}
S = {s["set"]: s for s in d["sets"]}
CHECK = {}


def opt(c, name):
    for o in c["fork_options"]:
        if o["option"] == name:
            return o
    raise KeyError(c["clue_id"] + ":" + name)


def insert_before(c, before_name, new):
    i = [o["option"] for o in c["fork_options"]].index(before_name)
    c["fork_options"].insert(i, new)


def ap_urn(prefix, keys):
    return [prefix + k for k in keys]


ARG = "urn:cts:greekLit:tlg0001.tlg001.perseus-grc2."
QS = "urn:cts:greekLit:tlg2046.tlg001.perseus-grc2."

# ---------------------------------------------------------------- AEN-TROY-02
c = C["AEN-TROY-02"]
opt(c, "i-a")["justification"] = (
    "reading i: 'amica' lunar light guides the fleet; the >= 0.5 threshold is DESIGN NC2's addition, not in the words; "
    "the local-midnight bound is not stated either: it is inferred from the order nightfall (2.250) -> fleet under way (2.254) "
    "-> horse opened (2.259) -> 'Tempus erat, quo prima quies ... incipit' (2.268)")
opt(c, "i-b")["justification"] = (
    "reading i without the phase threshold the words do not give; the midnight bound is the same inference as in i-a")
insert_before(c, "ii-a", {
    "option": "i-c",
    "operational": "the Moon is above the horizon at some instant between the end of evening nautical twilight and the start of morning nautical twilight of Night 0 (any phase)",
    "justification": "reading i with neither the phase threshold nor the inferred midnight bound: the words put the sailing after nightfall and name no hour"})
CHECK["AEN-TROY-02"] = ("edited: options i-a and i-b bounded the moonlight by local midnight, which the words do not state "
                        "(it is inferred from the order 2.250 -> 2.254 -> 2.259 -> 2.268 'prima quies'); the inference is now "
                        "spelled out in their justifications and option i-c, without the midnight bound, is added")

# ---------------------------------------------------------------- AEN-ETNA-04
c = C["AEN-ETNA-04"]
c["fork_options"] = [o for o in c["fork_options"] if o["option"] != "c"]
opt(c, "none")["justification"] = (
    "'tertia' counts about three lunations since Achaemenides was left behind, an event outside this set; read so, the line "
    "states elapsed time, not the phase on Day +1 (this absorbs the former option c, 'no phase constraint on Day +1', which "
    "had the same operational content)")
CHECK["AEN-ETNA-04"] = ("edited: option 'none' had no justification ('dropped'), and option c ('no phase constraint on Day +1') "
                        "was operationally identical to 'none', so the garden counted one path twice; c is merged into 'none', "
                        "which now carries c's justification")

# ------------------------------------------------------------ AEN-CARTHAGE-01
c = C["AEN-CARTHAGE-01"]
c["statement"] = ("On Day M1 Mercury (Cyllenius) binds on his golden sandals, takes his wand, flies until he sees Atlas, "
                  "alights there, plunges headlong toward the waves, and reaches Carthage, where he finds Aeneas building.")
c["licence_words"] = SEP.join([
    "pedibus talaria nectit aurea",
    "tum virgam capit",
    "iamque volans apicem et latera ardua cernit Atlantis",
    "Hic primum paribus nitens Cyllenius alis constitit; hinc toto praeceps se corpore ad undas misit",
    "Ut primum alatis tetigit magalia plantis, Aenean fundantem arces ac tecta novantem conspicit"])
c["ref"] = ["4.239", "4.240", "4.241", "4.242", "4.246", "4.247", "4.252", "4.253", "4.254", "4.259", "4.260", "4.261"]
c["notes"] = (c["notes"] + " 4.254-4.258 ('avi similis, quae ... volat aequora iuxta. Haud aliter ...') is a simile (a "
              "low-flying seabird) and is kept out of the licence: it carries no date, as the Odyssey's gull comparison "
              "(Od. 5.51-54) carries none. The god is named 'Cyllenius' (4.252) and 'Mercurium' (4.222).").strip()
CHECK["AEN-CARTHAGE-01"] = ("edited: the licence and the statement included the simile 'avi similis, quae circum litora ... "
                            "volat aequora iuxta' (4.254-255, closed by 'Haud aliter', 4.256), and the statement's Atlas "
                            "and arrival at Carthage were not quoted; the simile is removed, the non-simile frame (4.246-247, "
                            "4.252-254, 4.259-261) is quoted and the refs corrected. No fork option used the simile, so the "
                            "operational content is unchanged")

# ------------------------------------------------------------ AEN-CARTHAGE-03
c = C["AEN-CARTHAGE-03"]
note = ("; the words date Dido's speech and the fleet-building (between Day M1 and Night 0), not Night 0 itself: applying "
        "them to Night 0 assumes the unstated interval of row 02 is short")
opt(c, "a")["justification"] += note
opt(c, "b")["justification"] += note
CHECK["AEN-CARTHAGE-03"] = ("edited: options a and b put the season on Night 0, but the words belong to Dido's reproach on "
                            "an earlier, uncounted day; that transfer is now stated as an inference in both justifications")

# ------------------------------------------------------------ AEN-CARTHAGE-05
c = C["AEN-CARTHAGE-05"]
c["licence_words"] = SEP.join([
    "Aeneas celsa in puppi", "carpebat somnos",
    "Huic se forma dei voltu redeuntis eodem obtulit in somnis", "omnia Mercurio similis",
    "Non fugis hinc praeceps", "si te his attigerit terris Aurora morantem",
    "nocti se immiscuit atrae"])
c["ref"] = ["4.554", "4.555", "4.556", "4.557", "4.558", "4.565", "4.568", "4.570"]
CHECK["AEN-CARTHAGE-05"] = ("edited: the statement's 'urges him to flee before dawn' was not in the quoted words; "
                            "'Non fugis hinc praeceps' (4.565) and 'si te his attigerit terris Aurora morantem' (4.568) added "
                            "to the licence and refs")

# ------------------------------------------------------------ AEN-CARTHAGE-06
c = C["AEN-CARTHAGE-06"]
c["licence_words"] = SEP.join([
    "litora deseruere",
    "Et iam prima novo spargebat lumine terras Tithoni croceum linquens Aurora cubile",
    "classem procedere velis"])
c["ref"] = ["4.582", "4.584", "4.585", "4.586", "4.587"]
CHECK["AEN-CARTHAGE-06"] = ("edited: 'the fleet leaves at once' (before Dawn +1) was not in the quoted words; "
                            "'litora deseruere' (4.582) added to the licence and refs")

# ------------------------------------------------------------ AEN-CARTHAGE-07
c = C["AEN-CARTHAGE-07"]
c["statement"] = ("At the banquet on the night Aeneas reaches Carthage (an unstated time before Night 0 of this set), Dido "
                  "says the seventh 'aestas' (summer, or by the common synecdoche year) is now carrying him in his wandering "
                  "over all lands and seas.")
opt(c, "a")["justification"] = (
    "'septima aestas' counts the summers of wandering at the banquet; everything else is inference: the wandering began in "
    "the first summer after the fall (3.8 'Vix prima inceperat aestas', Aeneas' narrative), and Night 0 here falls in a "
    "later winter if Dido's 'hiberno ... sidere' (4.309, row 03) is taken literally; 6 to 8 years covers inclusive or "
    "exclusive counting, the months from the fall to that first summer, and the stay at Carthage. The range is the drafter's")
c["notes"] = ("The only year count in the Aeneid sets. The text states the count of summers at the banquet; the interval "
              "between the two Night 0s is inferred from it (option a). It allows AEN-TROY and AEN-CARTHAGE to be run as "
              "one linked set.")
S["AEN-CARTHAGE"]["notes"] = S["AEN-CARTHAGE"]["notes"].replace(
    "Row 07 links it to AEN-TROY by a year count the text states.",
    "Row 07 links it to AEN-TROY through Dido's count of summers of wandering ('septima aestas', 1.755-756); the year "
    "interval between the two Night 0s is inferred from that count, not stated.")
assert "inferred from that count" in S["AEN-CARTHAGE"]["notes"]
CHECK["AEN-CARTHAGE-07"] = ("edited: the statement put the banquet 'in the summer before Night 0' and counted 'since Troy', "
                            "neither of which the words state ('aestas' can stand for a year; the count is of summers of "
                            "wandering, which began after the fall); the statement is reworded, option a's chain of "
                            "inference is spelled out, and the row's notes and the set's notes no longer call the "
                            "interval between the two Night 0s 'stated'")

# ---------------------------------------------------------------- ARG-CIUS-06
c = C["ARG-CIUS-06"]
c["statement"] = ("From the battle night to Night 0: three whole days of mourning; from then on storms for twelve days and "
                  "nights; the halcyon on the night then coming on (row 07); Jason rouses the crew and they drive cattle up "
                  "Dindymon, where a daylight view is described (1.1112-1113: no dawn is named, so putting the sacrifice on "
                  "the next day is an inference from that daylight); a feast; at dawn they leave, and reach Cius that "
                  "evening (row 01).")
c["licence_words"] = SEP.join([
    "ἤματα δὲ τρία πάντα γόων",
    "ἐκ δὲ τόθεν τρηχεῖαι ἀνηέρθησαν ἄελλαι ἤμαθ" + AP + " ὁμοῦ νύκτας τε δυώδεκα",
    "ἐπιπλομένῃ δ" + AP + " ἐνὶ νυκτὶ",
    "Δινδύμου",
    "Μακριάδες σκοπιαὶ καὶ πᾶσα περαίη Θρηικίης ἐνὶ χερσὶν ἑαῖς προυφαίνετ" + AP + " ἰδέσθαι",
    "αὐτὰρ ἐς ἠὼ ληξάντων ἀνέμων νῆσον λίπον εἰρεσίῃσιν"])
c["ref"] = ap_urn(ARG, ["1.1057", "1.1078", "1.1079", "1.1080", "1.1092", "1.1093", "1.1112", "1.1113",
                        "1.1150", "1.1151", "1.1152"])
opt(c, "n16")["justification"] = (
    "the twelve storm nights counted from the night after the third mourning day (Nights -13 to -2), so the halcyon night "
    "(-2) is the twelfth and the storm days run to Day -1; mourning Days -15 to -13")
CHECK["ARG-CIUS-06"] = ("edited: the statement gave 'next day the sacrifice' as if stated; the text names no dawn between "
                        "the halcyon night and the sacrifice, only a daylight view (1.1112-1113, now quoted); the inference "
                        "is spelled out. Option n16's justification did not distinguish it from n17 and is restated")

# ---------------------------------------------------------------- ARG-CIUS-07
c = C["ARG-CIUS-07"]
opt(c, "b")["justification"] += "; the +-15-day width is the drafter's (Pliny gives none)"
CHECK["ARG-CIUS-07"] = ("edited: option b's +-15-day width around the Pleiades' setting and the solstices is not in Pliny "
                        "('circa solstitia'); now marked as the drafter's. The season itself enters only through Pliny's "
                        "bird lore, as the row already says, with a 'none' option")

# ------------------------------------------------------------- ARG-COLCHIS-01
c = C["ARG-COLCHIS-01"]
for n in ("a", "b", "c"):
    opt(c, n)["justification"] += "; the +-15-day width is the drafter's"
insert_before(c, "none", {
    "option": "d",
    "operational": "Night -7 within +-15 days of Arcturus' evening (acronychal) rising (first rising seen after sunset)",
    "justification": "the fourth seasonal phase of Arcturus in Greek calendars: Hesiod marks the end of winter by it "
                     "[hesiod-worksdays-grc.tsv 564-567, 'ἐπιτέλλεται ἀκροκνέφαιος']; the text names no phase; the "
                     "+-15-day width is the drafter's"})
CHECK["ARG-COLCHIS-01"] = ("edited: the text names no phase of Arcturus, but the menu offered only three of its four "
                           "seasonal phases; option d (evening rising, Hes. WD 564-567) added, and the +-15-day widths "
                           "marked as the drafter's")

# ------------------------------------------------------------- ARG-COLCHIS-02
c = C["ARG-COLCHIS-02"]
opt(c, "a3")["justification"] = (
    "one day's coasting between the Philyra night and the arrival night [me: count]; the text gives no count for the coast "
    "('ἐπιπρὸ γὰρ αἰὲν ἔτεμνον'), so this is the shortest reading, not a stated interval")
c["fork_options"].append({
    "option": "afree",
    "operational": "arrival on Night -4; the Ares storm on Night -7 to Night -10 (0 to 3 extra coasting days; the bound is the drafter's)",
    "justification": "no count is given for the coasting past the Macrones, Becheiri, Sapeires and Byzeres (2.1242-1245)"})
c["fork_options"].append({
    "option": "none",
    "operational": "no link: the Ares storm night is not placed relative to Day 0 (row 01 then fixes no searchable date)",
    "justification": "the coasting passage has no count, so the storm night's offset is not stated"})
CHECK["ARG-COLCHIS-02"] = ("edited: option a3 presented a one-day coasting passage as a count, but the text gives none for "
                           "it; a3 is now labelled the shortest reading, option afree (0-3 extra days, drafter's bound) "
                           "is added beside a4, and a 'none' option (storm night unlinked) is added, as for the other "
                           "uncounted intervals (AEN-CARTHAGE-02, VF-LEMNOS-07, ARG-RETURN-03)")

# ------------------------------------------------------------- ARG-COLCHIS-03
c = C["ARG-COLCHIS-03"]
c["statement"] = ("In Colchis: Day -3 Jason visits Aeetes (Day -3 is the day of the dawn of 2.1285: no dawn or nightfall is "
                  "narrated between 2.1285 and 3.744 [me: search of the Greek for time words]); Night -3 Medea lies "
                  "sleepless; Day -2 she meets Jason at Hecate's temple; at dawn of Day -1 the heroes ask Aeetes for the "
                  "teeth; Night -1 Jason sacrifices; Day 0 is the ordeal, ending at sunset.")
c["licence_words"] = SEP.join([
    "νὺξ μὲν ἔπειτ" + AP + " ἐπὶ γαῖαν ἄγεν κνέφας",
    "ἀλλὰ μάλ" + AP + " οὐ Μήδειαν ἐπὶ γλυκερὸς λάβεν ὕπνος",
    "φέγγος Ἠριγενής",
    "αὐτὰρ ἅμ" + AP + " ἠοῖ",
    "Ἠέλιος μὲν ἄπωθεν ἐρεμνὴν δύετο γαῖαν",
    "ἠριγενὴς Ἠὼς βάλεν ἀντέλλουσα",
    "ἦμαρ ἔδυ, καὶ τῷ τετελεσμένος ἦεν ἄεθλος"])
c["ref"] = ap_urn(ARG, ["3.744", "3.751", "3.823", "3.824", "3.1171", "3.1172", "3.1191", "3.1223", "3.1224", "3.1407"])
CHECK["ARG-COLCHIS-03"] = ("edited: the statement's Night -3 (Medea sleepless) was not in the quoted words, and Day -3 "
                           "rests on the absence of any time marker between 2.1285 and 3.744; 3.744 and 3.751 are now "
                           "quoted and the inference is stated")

# ------------------------------------------------------------- ARG-COLCHIS-04
c = C["ARG-COLCHIS-04"]
for n in ("a", "b"):
    opt(c, n)["operational"] += " (computed at the set's site as a stand-in; see notes)"
c["notes"] = ("The sailors are generic and unlocated ('ἐνὶ πόντῳ'); the nocturne is framed by Medea's night at Aia "
              "(3.751). The words state no observing site, so the set's site (Colchis) is the drafter's stand-in. " + c["notes"]).strip()
CHECK["ARG-COLCHIS-04"] = ("edited: the options were silently computed at the set's site (Colchis), but the words put the "
                           "star-watching sailors only 'at sea'; the site is now marked as the drafter's stand-in")

# ------------------------------------------------------------- ARG-RETURN-03
c = C["ARG-RETURN-03"]
opt(c, "x0")["justification"] = (
    "the shortest reading: the text names no stay at Carpathos and no day for the crossing, so x = 0 assumes none (an inference)")
c["fork_options"].append({
    "option": "none",
    "operational": "no link: Day E is not placed relative to Day 0 (row 01 then fixes no searchable date)",
    "justification": "the text gives no count for the stay at Carpathos or the crossing to Crete"})
CHECK["ARG-RETURN-03"] = ("edited: x0 assumes no stay at Carpathos, which the text does not state, and the fork had no "
                          "'none'; x0's justification now says so and a 'none' option (Day E unlinked) is added")

# ------------------------------------------------------------- QS-SACK-02
c = C["QS-SACK-02"]
c["statement"] = ("Among the portents at the Trojans' sacrifices on Night 0, night-birds cry and a mist covers all the stars "
                  "above the city, although the shining sky is cloudless. The hour is not stated; the portents come before "
                  "the meal of 13.1 and the sleep of 13.21, so they fall early in the night by inference.")
opt(c, "a")["justification"] += ("; the before-midnight bound is inferred from the order portents (12.500-520) -> meal "
                                 "(13.1) -> sleep and torch (13.21-23)")
CHECK["QS-SACK-02"] = ("edited: the statement put the portents 'in the evening', and option a bounded them before local "
                       "midnight, but the words give no hour; both now state that the timing is inferred from the order "
                       "12.500-520 -> 13.1 -> 13.21")

# ------------------------------------------------------------- QS-SACK-03
c = C["QS-SACK-03"]
b = opt(c, "b")
b["operational"] = "Alcyone >= 5 deg above the horizon at some instant of the dark hours of Night 0"
b["justification"] = "as a, with a visibility altitude (the 5-deg threshold is the drafter's)"
insert_before(c, "none", {
    "option": "b-late",
    "operational": "Alcyone >= 5 deg above the horizon at some instant between local midnight and the start of morning nautical twilight of Night 0",
    "justification": "the withdrawal is placed 'Ἰλίου ὀλλυμένης' (13.551), during the sack, which begins only after the "
                     "city sleeps (13.21-29); the midnight bound is the drafter's inference from that order"})
CHECK["QS-SACK-03"] = ("edited: option b timed the Pleiades at nightfall ('seen at nightfall'), which the words do not "
                       "state: the passage is set 'Ἰλίου ὀλλυμένης', during the sack, after the city sleeps (13.21-29); "
                       "b now spans the dark hours, and option b-late carries the after-midnight reading with its "
                       "inference spelled out. The BM-analogue pinned reading still names b, which now means the "
                       "dark-hours version")

# ------------------------------------------------------------- VF-LEMNOS-01
c = C["VF-LEMNOS-01"]
c["statement"] = ("The Argo sails at the dawn of 1.311; a storm whose darkness the text calls 'nox' (1.617, 1.670) "
                  "passes and day shines again (1.655); the Argo coasts past Pelion, Sciathos, Sepias and Pallene until "
                  "the Sun sets (2.34-37): Night 0 follows. The text gives no count of days.")
c["licence_words"] = SEP.join([
    "Minyas simul optulit omnis alma novo crispans pelagus Tithonia Phoebo",
    "piceoque premit nox omnia caelo",
    "emicuit reserata dies",
    "Iamque Hyperionius metas maris urget Hiberi currus"])
c["ref"] = ["1.310", "1.311", "1.617", "1.655", "2.34", "2.35"]
opt(c, "a")["justification"] = (
    "the storm's 'nox' (1.617; Jason's 'nox ista', 1.670) read as storm darkness inside the departure day ('emicuit "
    "reserata dies', 1.655) and the coasting of 2.6-33 as the rest of that day; an inference, the text gives no count")
opt(c, "b")["justification"] = (
    "the storm's 'nox' may be a real night, and no count is given for the coasting; the -3 bound is the drafter's")
s = S["VF-LEMNOS"]
s["day0"] = ("Day 0 is the day whose sunset (2.34-37) begins Tiphys' night: the first day of the voyage under VF-LEMNOS-01 "
             "option a only; Night 0 is that night (Tiphys' speech); Dawn +1 brings Lemnos in sight. Day L, the storm at "
             "Lemnos, is an unstated number of days later.")
CHECK["VF-LEMNOS-01"] = ("edited: option a ('the departure day is Day 0') ignored the storm of 1.608-656, whose darkness "
                         "the text calls 'nox' (1.617, 1.670) before day returns (1.655), so a one-day voyage is an "
                         "inference, not a reading of the words; the storm is now quoted, both justifications state the "
                         "inference, and the set's day0 no longer calls Day 0 'the first day of the voyage' outright")

# ------------------------------------------------------------- VF-COLCHIS-01
c = C["VF-COLCHIS-01"]
c["statement"] = ("On Day 0 late 'vesper' (the evening, or the evening star) parts Medea from her Thessalian guest, and "
                  "night falls.")
opt(c, "none")["justification"] = (
    "'vesper' read as the time of day (evening), its commonest sense, rather than the evening star; or the evening star as "
    "a stock marker of nightfall")
CHECK["VF-COLCHIS-01"] = ("edited: the statement asserted 'the late evening star', but 'serus vesper' is just as naturally "
                          "'late evening'; the statement is made neutral and 'none' now gives that reading")

# ---------------------------------------------------------- IL-PATROCLUS-02
c = C["IL-PATROCLUS-02"]
c["statement"] = ("Earlier on Day 0 than the noon and afternoon markers of 16.777-780, in the fight over Sarpedon's body, "
                  "Zeus stretches deadly night over the battle.")
opt(c, "solar_am")["justification"] = (
    "the drafter's reading of the narrative order (16.567 comes before 16.777, 'while the Sun bestrode mid-heaven') as "
    "'before noon'; that line describes a span round noon, so the order does not fix the hour")
insert_before(c, "none", {
    "option": "solar_any",
    "operational": "a solar eclipse of class X1-X4 (DESIGN 3.1) visible at Troy on Day 0, maximum at any time the Sun is above the horizon",
    "justification": "the darkness read as an eclipse without the before-noon bound: the words state no hour"})
s = S["IL-PATROCLUS"]
eco = s["eclipse_compatible_options"]
eco.insert(eco.index("IL-PATROCLUS-02:solar_am") + 1, "IL-PATROCLUS-02:solar_any")
CHECK["IL-PATROCLUS-02"] = ("edited: the statement said 'before noon' and option solar_am required a maximum before local "
                            "apparent noon, but the words state no hour (16.567 only precedes 16.777, which describes a "
                            "span round noon); the statement is reworded, solar_am's justification states the inference, "
                            "and option solar_any (any daylight hour) is added and listed in eclipse_compatible_options")

# ---------------------------------------------------------- IL-PATROCLUS-07
c = C["IL-PATROCLUS-07"]
c["notes"] = ("Hector's death on Day +1 rests on the dawn of 19.1 (row 01) and on the absence of any narrated sunset or "
              "dawn between 19.2 and 23.58 [me: search of the Greek for time words; only speeches and the excluded "
              "similes 22.26-31 and 22.317-318 mention night or stars]. " + c["notes"]).strip()
CHECK["IL-PATROCLUS-07"] = ("edited: 'Hector dies on Day +1' was not supported by the quoted words; the note now gives "
                            "its basis (the dawn of 19.1 and no time marker until 23.58)")

# ---------------------------------------------------------- IL-PATROCLUS-09
c = C["IL-PATROCLUS-09"]
c["licence_words"] = "ἀλλ" + AP + " ὅτε δή ῥ" + AP + " ἐκ τοῖο δυωδεκάτη γένετ" + AP + " ἠώς"
c["ref"] = ["24.31"]
c["notes"] = ("Hermes, disguised as a Myrmidon squire, also says the twelfth dawn has come (24.413-414); that speech is "
              "a deception and is not used as a date carrier. It agrees with the narrator's 24.31.")
CHECK["IL-PATROCLUS-09"] = ("edited: the licence quoted 24.413-414, which Hermes speaks in disguise (a lying persona); "
                            "it is removed from the licence and refs and kept only in the notes; the narrator's 24.31 "
                            "alone carries the interval")

# ---------------------------------------------------------------- finalise
missing = set(CHECK) - set(C)
assert not missing, missing
for c in d["clues"]:
    c["license_check"] = CHECK.get(c["clue_id"], "ok")
d["license_check"] = {
    "done": "2026-10-04",
    "by": "independent licence check (an agent that did not draft these sets and read no truth file and not docs/research-controls.md)",
    "report": "docs/license-check-negatives.md",
    "pre_edit_copy": "results/license-check-negatives/negatives.before.json",
    "script": "results/license-check-negatives/apply_edits.py",
    "warning": "results/negatives/build_negatives.py writes this file; re-running it would silently undo these edits unless they are ported into it",
}
out = json.dumps(d, indent=1, ensure_ascii=False) + "\n"
open(PATH, "w", encoding="utf-8", newline="\n").write(out)
n_ed = sum(1 for c in d["clues"] if c["license_check"] != "ok")
print("clues:", len(d["clues"]), "edited:", n_ed, "ok:", len(d["clues"]) - n_ed)
