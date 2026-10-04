# Round-2 licence check of data/prereg/negatives.json.
# Input : results/license-check-negatives/r2/negatives.r2-before.json (the file as round 1 left it)
# Output: data/prereg/negatives.json (overwritten)
# Every edit asserts the old value first, so a re-run on a changed input fails loudly.
# Re-runnable: always starts from the r2-before copy.
import json, os, sys

ROOT = r"C:\Projects\odybench"
BEFORE = os.path.join(ROOT, "results", "license-check-negatives", "r2", "negatives.r2-before.json")
PATH = os.path.join(ROOT, "data", "prereg", "negatives.json")
sys.stdout.reconfigure(encoding="utf-8")

d = json.load(open(BEFORE, encoding="utf-8"))
sets = {s["set"]: s for s in d["sets"]}
rows = {c["clue_id"]: c for c in d["clues"]}

def opt(row, name):
    for o in row["fork_options"]:
        if o["option"] == name:
            return o
    raise KeyError((row["clue_id"], name))

def expect(actual, old, what):
    if actual != old:
        raise SystemExit(f"UNEXPECTED {what}:\n  have: {actual!r}\n  want: {old!r}")

R2 = {}      # clue_id -> round-2 verdict for edited rows
R2SET = {}   # set -> round-2 verdict for edited sets

# ---------------------------------------------------------------- AEN-TROY (set)
s = sets["AEN-TROY"]
ida = s["observer_places"][2]
expect(ida["place"], "Mount Ida (the ridge over which Lucifer rises, as seen from Troy)", "AEN-TROY Ida place")
s["observer_places"] = s["observer_places"][:2]
ida = dict(ida)
ida["place"] = ("Mount Ida, the ridge over which Lucifer rises as seen from Troy: the bearing target of "
                "AEN-TROY-07's 'ida' rider, not a place the narrative puts an observer")
# keep key order: put 'landmarks' right after observer_places
new_s = {}
for k, v in s.items():
    new_s[k] = v
    if k == "observer_places":
        new_s["landmarks"] = [ida]
s.clear(); s.update(new_s)

pr = s["pinned_readings"]
pr["R-iii (silent moon = not yet up when the fleet sails; up later, so 2.340 is kept)"] = {
    "AEN-TROY-02": "iii", "AEN-TROY-04": "a", "AEN-TROY-05": "none", "AEN-TROY-07": "vis7"}
# order: put R-iii before BM-analogue
order = [k for k in pr if k != "BM-analogue"] + ["BM-analogue"]
s["pinned_readings"] = {k: pr[k] for k in order}

slot = s["odyssey_slots"]["day0_phase"]
expect(slot["note"], "only reading ii of 2.255 (silens luna = conjunction) gives the Odyssey's Day-0 conjunction; "
       "reading i puts a lit moon in the sky instead", "AEN-TROY day0_phase note")
slot["note"] += "; reading iii (no Moon up when the fleet sails) is a waning or very young Moon, not a conjunction"

old_notes = ("Both readings of 2.255 are pinned, as critique-design issue 15 requires. Under reading ii the "
             "moonlight of 2.340 contradicts the conjunction; R-ii drops 2.340, R-ii-literal keeps it.")
expect(s["notes"], old_notes, "AEN-TROY notes")
s["notes"] = (old_notes + " Reading iii (added by the round-2 licence check: the Moon not yet up when the fleet "
              "sails) is the one reading under which 2.255 and 2.340 agree; it is pinned as R-iii. Mount Ida, "
              "listed in observer_places until round 2, is a landmark for the 'ida' rider and now sits under "
              "'landmarks'.")
R2SET["AEN-TROY"] = ("edited: Mount Ida moved from observer_places to a new 'landmarks' list (it is the bearing "
                     "target of AEN-TROY-07's 'ida' rider; the narrative puts no observer there); pinned reading "
                     "R-iii added for the new option AEN-TROY-02:iii; the day0_phase note and the set notes "
                     "updated to match")

# ---------------------------------------------------------------- AEN-TROY-02
r = rows["AEN-TROY-02"]
names = [o["option"] for o in r["fork_options"]]
expect(names, ["i-a", "i-b", "i-c", "ii-a", "ii-b", "none"], "AEN-TROY-02 options")
iii = {
    "option": "iii",
    "operational": "the Moon is below the horizon at the end of evening nautical twilight of Night 0 (any phase)",
    "justification": ("reading iii: 'tacitae ... lunae' as a Moon that gives no light because it is not up when "
                      "the fleet sails after nightfall ('et iam', 2.254, follows 2.250-253); with row 04's 'per "
                      "lunam' (2.340) kept, it becomes a Moon that rises later in Night 0, the one reading under "
                      "which rows 02 and 04 agree; the end-of-twilight instant stands for 'after nightfall' and is "
                      "the checker's choice, since the words name no hour; added by the round-2 licence check"),
}
r["fork_options"].insert(5, iii)
R2["AEN-TROY-02"] = ("edited: the fork lacked a reading the words admit, 'tacitae ... lunae' as a Moon not up "
                     "(not yet risen, or already set) when the fleet sails; unlike readings i and ii it agrees "
                     "with 'per lunam' at 2.340 (row 04). Option iii added (not eclipse-compatible) and pinned as "
                     "R-iii. Round 1's edits (option i-c; the midnight bound stated as an inference) are kept")

# ---------------------------------------------------------------- AEN-TROY-07 (follows the Ida move)
r = rows["AEN-TROY-07"]
o = opt(r, "ida")
old_cite = "[me: great-circle bearing from the coordinates in observer_places]"
if old_cite not in o["operational"]:
    raise SystemExit(f"UNEXPECTED AEN-TROY-07 ida: {o['operational']!r}")
o["operational"] = o["operational"].replace(
    old_cite, "[me: great-circle bearing from Troy's coordinates in observer_places to Ida's in landmarks]")
R2["AEN-TROY-07"] = ("edited: the 'ida' rider cited the Ida coordinates as part of observer_places; Ida is now "
                     "under the set's 'landmarks' (set-level edit: the narrative puts no observer on Ida), and the "
                     "citation is updated. Operational content, the 119-deg bearing and the rider's other text are "
                     "unchanged")

# ---------------------------------------------------------------- AEN-TROY-03
r = rows["AEN-TROY-03"]
expect(r["statement"], "The royal ship raises the fire signal and the men in the horse come out; Hector's ghost "
       "appears to Aeneas at the hour of first sleep. The sack fills the rest of Night 0.", "AEN-TROY-03 statement")
expect(r["licence_words"], "flammas cum regia puppis extulerat … Tempus erat, quo prima quies mortalibus aegris "
       "incipit", "AEN-TROY-03 licence")
expect(r["ref"], ["2.256", "2.257", "2.268", "2.269", "2.270"], "AEN-TROY-03 ref")
r["statement"] = ("The royal ship raises the fire signal and Sinon lets the men out of the horse; Hector's ghost "
                  "appears to Aeneas at the hour of first sleep. The fighting then runs to the end of Night 0 "
                  "('consumpta nocte', 2.795, row 06).")
r["licence_words"] = ("flammas cum regia puppis extulerat … laxat claustra Sinon. Illos patefactus ad auras reddit "
                      "equus … Tempus erat, quo prima quies mortalibus aegris incipit")
r["ref"] = ["2.256", "2.257", "2.259", "2.260", "2.268", "2.269", "2.270"]
R2["AEN-TROY-03"] = ("edited: two features of the statement were not in the cited rows: the men leaving the horse "
                     "(now quoted from 2.259-260, refs added) and 'the sack fills the rest of Night 0', which rests "
                     "on 'consumpta nocte' (2.795) and is now attributed to row 06. No option; ordering only")

# ---------------------------------------------------------------- AEN-CARTHAGE-03
r = rows["AEN-CARTHAGE-03"]
o = opt(r, "b")
old_b = ("the whole closed sailing season; the words date Dido's speech and the fleet-building (between Day M1 "
         "and Night 0), not Night 0 itself: applying them to Night 0 assumes the unstated interval of row 02 is short")
expect(o["justification"], old_b, "AEN-CARTHAGE-03 b justification")
o["justification"] = ("the winter half-year between the equinoxes, the widest reading of 'hiberno' (the width is "
                      "the drafter's; the earlier wording equated it with 'the whole closed sailing season', which "
                      "no cited source supports); the words date Dido's speech and the fleet-building (between Day "
                      "M1 and Night 0), not Night 0 itself: applying them to Night 0 assumes the unstated interval "
                      "of row 02 is short")
R2["AEN-CARTHAGE-03"] = ("edited: option b's justification equated the equinox-to-equinox window with 'the whole "
                         "closed sailing season', an equation no cited source supports; it now describes the window "
                         "as what it is (the winter half-year, the widest reading of 'hiberno', the drafter's width). "
                         "Operational content unchanged; round 1's edit (the transfer to Night 0 stated as an "
                         "inference) is kept")

# ---------------------------------------------------------------- AEN-CARTHAGE-05
r = rows["AEN-CARTHAGE-05"]
old_st = ("Later in Night 0 Mercury appears again to the sleeping Aeneas on his ship, urges him to flee before "
          "dawn, and vanishes into the black night.")
expect(r["statement"], old_st, "AEN-CARTHAGE-05 statement")
r["statement"] = ("In Night 0 (after the midnight scene of row 04 in the narrative order; no hour is stated) "
                  "Mercury appears again to the sleeping Aeneas on his ship, urges him to flee before dawn, and "
                  "vanishes into the black night.")
R2["AEN-CARTHAGE-05"] = ("edited: 'Later in Night 0' gave a relative time of night that the words do not state; "
                         "the statement now says the order is narrative order (after row 04's midnight scene) and "
                         "that no hour is given. No option used it. Round 1's additions to the licence (4.565, "
                         "4.568) are kept")

# ---------------------------------------------------------------- ARG-CIUS (set) and ARG-CIUS-05
s = sets["ARG-CIUS"]
p = s["observer_places"][1]
expect(p["place"], "Cyzicus, land of the Doliones (Night -17)", "ARG-CIUS place 2")
p["place"] = "Cyzicus, land of the Doliones (the battle night: Night -17, -16 or -18 by ARG-CIUS-06)"
R2SET["ARG-CIUS"] = ("edited: the Cyzicus place label fixed the battle night at Night -17, which is only option "
                     "n17 of ARG-CIUS-06; relabelled")

r = rows["ARG-CIUS-05"]
old_st = ("On Night -17 (row 06) the Argo, after a full day's sail, is driven back to Cyzicus in the night; in the "
          "night the Doliones do not recognise the returning heroes and the two sides fight.")
expect(r["statement"], old_st, "ARG-CIUS-05 statement")
r["statement"] = ("On the battle night (Night -17 under row 06's n17, Night -16 under n16, Night -18 under n18) "
                  "the Argo, after a full day's sail, is driven back to Cyzicus in the night; in the night the "
                  "Doliones do not recognise the returning heroes and the two sides fight.")
o = opt(r, "b")
expect(o["justification"], "a weaker form", "ARG-CIUS-05 b justification")
o["justification"] = ("a weaker form; the midnight instant is the drafter's: the words put the landing and the "
                      "fight in the night ('αὐτονυχί', 'ὑπὸ νυκτὶ') and name no hour")
R2["ARG-CIUS-05"] = ("edited: the statement fixed the battle night at Night -17, which is only one of row 06's "
                     "counts (n16, n17, n18), and option b's local-midnight instant, which the words do not give, "
                     "was not marked as the drafter's; both corrected")

# ---------------------------------------------------------------- ARG-COLCHIS (set) and ARG-COLCHIS-01
s = sets["ARG-COLCHIS"]
p = s["observer_places"][1]
expect(p["place"], "the Island of Ares (Night -7)", "ARG-COLCHIS place 2")
p["place"] = ("the Island of Ares (the storm night, which ARG-COLCHIS-02 places: Night -7 under a3, Night -8 "
              "under a4, Night -7 to -10 under afree)")
R2SET["ARG-COLCHIS"] = ("edited: the Island of Ares label fixed the storm night at Night -7, which is only option "
                        "a3 of ARG-COLCHIS-02; relabelled")

r = rows["ARG-COLCHIS-01"]
old_st = ("On Night -7, the day the sons of Phrixus near the Island of Ares, Zeus stirs the north wind, 'marking "
          "with rain the wet path of Arcturus'; by night a storm wrecks their ship.")
expect(r["statement"], old_st, "ARG-COLCHIS-01 statement")
r["statement"] = ("On the storm night (Night -7 under ARG-COLCHIS-02:a3, Night -8 under a4, Night -7 to -10 under "
                  "afree; not placed under none), which ends the day the sons of Phrixus near the Island of Ares, "
                  "Zeus stirs the north wind, 'marking with rain the wet path of Arcturus'; by night a storm wrecks "
                  "their ship.")
for name in ["a", "b", "c", "d"]:
    o = opt(r, name)
    if not o["operational"].startswith("Night -7 within +-15 days of "):
        raise SystemExit(f"UNEXPECTED ARG-COLCHIS-01 {name}: {o['operational']!r}")
    o["operational"] = o["operational"].replace("Night -7 within", "the storm night (as ARG-COLCHIS-02 places it) "
                                                "within", 1)
R2["ARG-COLCHIS-01"] = ("edited: the statement and options a-d fixed the storm at Night -7, which is only option "
                        "a3 of ARG-COLCHIS-02 (a4 puts it on Night -8, afree on Night -7 to -10); they now refer "
                        "to the storm night as row 02 places it. Round 1's edits (option d; the +-15-day widths "
                        "marked as the drafter's) are kept")

# ---------------------------------------------------------------- ARG-RETURN (set) and ARG-RETURN-04
s = sets["ARG-RETURN"]
old_day0 = ("Day 0 is the day the Argo leaves Crete; Night 0 is the 'pall' night with neither stars nor moon; "
            "Dawn +1 shows Anaphe. The evening star is on Day E = Day -(3 + x).")
expect(s["day0"], old_day0, "ARG-RETURN day0")
s["day0"] = ("Day 0 is the day the Argo leaves Crete at dawn; the 'pall' darkness, with neither stars nor moon, "
             "falls 'at once' (Αὐτίκα, 4.1694) as they run over the Cretan sea, in the daylight of Day 0 or at its "
             "nightfall (the text does not say which; ARG-RETURN-04), and lasts through Night 0; Dawn +1 shows "
             "Anaphe. The evening star is on Day E = Day -(3 + x).")
p = s["observer_places"][0]
expect(p["place"], "the Cretan sea beyond Cape Salmonis (Night 0)", "ARG-RETURN place 1")
p["place"] = "the Cretan sea beyond Cape Salmonis (Day 0 after the embarkation, and Night 0)"
slot = s["odyssey_slots"]["darkness_eclipse"]
expect(slot["note"], "a night darkness; eclipse-compatible only as a lunar eclipse (option c)",
       "ARG-RETURN darkness note")
slot["note"] = ("a darkness the text calls night, whose onset may fall in the daylight of Day 0; eclipse-compatible "
                "as the dark of the Moon (option b, a conjunction anchor) or as a solar eclipse in the daylight of "
                "Day 0 (option d); option c is a lunar eclipse, not solar")
slot = s["odyssey_slots"]["day0_phase"]
old_note = ("a moonless night on Night 0, the analogue of the Odyssey's σκοτομήνιος (14.457) rather than of its "
            "Day-0 conjunction; option b turns it into a conjunction anchor")
expect(slot["note"], old_note, "ARG-RETURN day0_phase note")
slot["note"] = old_note + "; option d (a solar eclipse on Day 0) does too"
eco = s["eclipse_compatible_options"]
expect(eco, ["ARG-RETURN-04:b", "ARG-RETURN-04:c"], "ARG-RETURN eclipse_compatible_options")
s["eclipse_compatible_options"] = ["ARG-RETURN-04:b", "ARG-RETURN-04:c", "ARG-RETURN-04:d"]
R2SET["ARG-RETURN"] = ("edited: day0, the first place label and the two slot notes now allow the darkness of "
                       "ARG-RETURN-04 to begin in the daylight of Day 0, which the text does not exclude; "
                       "'ARG-RETURN-04:d' (new) is listed in eclipse_compatible_options; the darkness note no "
                       "longer says the darkness is eclipse-compatible only as a lunar eclipse (option b, a "
                       "conjunction, was already listed)")

r = rows["ARG-RETURN-04"]
old_st = ("On Night 0, as they run over the Cretan sea, the night they call 'the pall' terrifies them: neither "
          "stars nor moonbeams pierce it; black chaos from heaven, or darkness risen from the depths.")
expect(r["statement"], old_st, "ARG-RETURN-04 statement")
old_lw = ("νὺξ ἐφόβει, τήνπερ τε κατουλάδα κικλήσκουσιν … νύκτʼ ὀλοὴν οὐκ ἄστρα διίσχανεν, οὐκ ἀμαρυγαὶ μήνης "
          "… οὐρανόθεν δὲ μέλαν χάος")
expect(r["licence_words"], old_lw, "ARG-RETURN-04 licence")
r["statement"] = ("After they embark at the new dawn of Day 0 (row 03), 'at once' (Αὐτίκα), as they run over "
                  "the Cretan sea, the night they call 'the pall' terrifies them: neither stars nor moonbeams "
                  "pierce it; black chaos from heaven, or darkness risen from the depths. No sunset is narrated "
                  "between the embarkation and this darkness, so its onset is not stated: in the daylight of Day 0 "
                  "or at its nightfall. It ends at Dawn +1 (row 05).")
r["licence_words"] = ("Αὐτίκα δὲ Κρηταῖον ὑπὲρ μέγα λαῖτμα θέοντας νὺξ ἐφόβει, τήνπερ τε κατουλάδα κικλήσκουσιν "
                      "… νύκτʼ ὀλοὴν οὐκ ἄστρα διίσχανεν, οὐκ ἀμαρυγαὶ μήνης … οὐρανόθεν δὲ μέλαν χάος")
names = [o["option"] for o in r["fork_options"]]
expect(names, ["a", "b", "c", "none"], "ARG-RETURN-04 options")
d_opt = {
    "option": "d",
    "operational": ("a solar eclipse of class X1-X4 (DESIGN 3.1) visible at the set's first site (the Cretan sea "
                    "beyond Cape Salmonis) on Day 0, maximum at any time the Sun is above the horizon"),
    "justification": ("the darkness read as falling in daylight and as an eclipse: 'Αὐτίκα' follows the dawn "
                      "embarkation (4.1690-1694) with no sunset between, and 'νύκτʼ ὀλοὴν' is the phrase of the "
                      "Iliad's daytime darkness (Il. 16.567, IL-PATROCLUS-02); against it, the text calls the "
                      "darkness night, names stars and Moon as unseen, and makes it last until dawn (4.1713-1714); "
                      "the eclipse is the checker's inference, as in IL-PATROCLUS-02:solar_any; added by the "
                      "round-2 licence check"),
}
r["fork_options"].insert(3, d_opt)
R2["ARG-RETURN-04"] = ("edited: the statement put the darkness on Night 0, but the text gives no onset: it falls "
                       "'at once' (Αὐτίκα, 4.1694, now quoted) after the dawn embarkation, with no sunset "
                       "narrated, so it may begin in daylight. The statement now says so, and option d (a solar "
                       "eclipse in the daylight of Day 0; eclipse-compatible; the checker's inference, with the "
                       "case against it stated) is added beside the night readings a-c and 'none'")

# ---------------------------------------------------------------- VF-COLCHIS (set)
s = sets["VF-COLCHIS"]
p = s["observer_places"][0]
expect(p["place"], "Colchis at the mouth of the Phasis (Aeetes' city)", "VF-COLCHIS place")
expect(p["coord_source"], "Phasis (Wikipedia, fetched 2026-10-04)", "VF-COLCHIS coord_source")
p["place"] = ("Colchis: Aeetes' city on the Phasis, where Medea spends Night 0 (the quoted words name the river "
              "mouth the Argonauts reach; they do not give the city's position)")
p["coord_source"] = ("Phasis (Wikipedia, fetched 2026-10-04): the river mouth, the drafter's stand-in for Aeetes' "
                     "city, whose position these words do not give")
R2SET["VF-COLCHIS"] = ("edited: the place label put Aeetes' city at the mouth of the Phasis, but the quoted words "
                       "(5.178-180) describe the river mouth the Argonauts reach, not the city where Medea spends "
                       "Night 0; the label and coord_source now call the river mouth a stand-in")

# ---------------------------------------------------------------- verdict fields
for c in d["clues"]:
    prev = c.pop("license_check")
    v = R2.get(c["clue_id"], "ok")
    # rebuild with license_check last and the round-1 verdict after it
    c["license_check"] = v
    c["license_check_r1"] = prev
for name, s in sets.items():
    s["license_check"] = R2SET.get(name, "ok")

# ---------------------------------------------------------------- top-level block
lc = d["license_check"]
d["license_check"] = {
    "round_1": lc,
    "round_2": {
        "done": "2026-10-04",
        "by": ("independent licence check, round 2 (an agent that did not draft these sets or run round 1, and read "
               "no truth file, not docs/research-controls.md and not docs/negatives-drafting.md)"),
        "report": ("returned as text to the workflow that ran this check (the round-2 agent could not write report "
                   "files); docs/license-check-negatives.md still holds the round-1 report unchanged"),
        "pre_edit_copy": "results/license-check-negatives/r2/negatives.r2-before.json",
        "script": "results/license-check-negatives/r2/apply_edits_r2.py",
        "row_fields": ("license_check is the round-2 verdict on the row as it now stands; license_check_r1 keeps "
                       "round 1's verdict. Sets carry a set-level license_check"),
        "warning": ("results/negatives/build_negatives.py writes this file; re-running it would silently undo both "
                    "rounds of edits unless they are ported into it"),
    },
}

out = json.dumps(d, indent=1, ensure_ascii=False) + "\n"
open(PATH, "w", encoding="utf-8", newline="\n").write(out)
print("rows edited:", sorted(R2))
print("sets edited:", sorted(R2SET))
print("wrote", PATH)
