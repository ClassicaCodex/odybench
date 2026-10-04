# Licence check round 2 (independent of round 1's egyptian_check.py / meansun_check.py, which were not read).
# Recomputes every interval row of data/prereg/controls_almagest.json from the Egyptian dates AS PRINTED in
# data/text/ptolemy-syntaxis-grc.tsv, and cross-checks each against the mean-Sun longitudes Ptolemy states.
#
# WARNING: the output of this script contains date words (era years, Egyptian months and days). It is a
# licence-check record, like the truth file; the searcher must never read it.
#
# Method:
#  * each date phrase is given as an exact substring of the cited row (asserted), and its Greek numerals are
#    parsed here (not typed in as integers);
#  * Egyptian year = 12 x 30 days + 5 epagomenal days; day number N = 365*Y + 30*(m-1) + d;
#  * civil day (midnight to midnight, the file's convention): an observation in the evening of the night
#    "D into D+1" is on D, a pre-dawn one on D+1;
#  * era links only from the text: Antoninus 2 = Nabonassar 886 (9.10.3); Antoninus 3 = 463 after Alexander's
#    death (3.1.9); Nabonassar -> Alexander's death = 424 Egyptian years (3.7.4; also 52 = 476 at 10.9.2);
#    Philadelphus 13 = Nabonassar 476 (10.4.6). Hadrian's years are used only within one set, consecutive.
#  * mean Sun: Ptolemy's daily mean motion 0;59,8,17,13,12,31 deg (row 3.1.14); instants as local
#    apparent hours from the words (evening ~ 19 h, dawn ~ 5 h where no hour is given).
import io, json, sys, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = "C:/Projects/odybench/"
PFX = "urn:cts:greekLit:tlg0363.tlg001.1st1K-grc1."
rows = {}
for line in open(ROOT + "data/text/ptolemy-syntaxis-grc.tsv", encoding="utf-8"):
    k, _, v = line.rstrip("\n").partition("\t")
    # NFC only for these presence checks: the export mixes tonos (U+03AF) and oxia (U+1F77) forms
    rows[k.replace(PFX, "")] = unicodedata.normalize("NFC", v)
clues = json.load(open(ROOT + "data/prereg/controls_almagest.json", encoding="utf-8"))["clues"]

VAL = {"α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5, "ἐ": 5, "ϛ": 6, "Ϛ": 6, "ς": 6, "ζ": 7, "η": 8, "θ": 9,
       "ι": 10, "ῑ": 10, "κ": 20, "λ": 30, "μ": 40, "ν": 50, "ξ": 60, "ο": 70, "π": 80, "ϙ": 90, "9": 90,
       "ρ": 100, "σ": 200, "τ": 300, "υ": 400, "φ": 500, "χ": 600, "ψ": 700, "ω": 800, "ᾱ": 1}


def gnum(tok):
    tok = tok.strip().rstrip("ʹ΄´'·")
    return sum(VAL[c] for c in tok if c in VAL)


MONTH = {"Θὼθ": 1, "Φαωφὶ": 2, "Ἀθὺρ": 3, "Χοιὰκ": 4, "Χοϊὰκ": 4, "Τυβὶ": 5, "Μεχὶρ": 6, "Φαμενὼθ": 7,
         "Φαρμουθὶ": 8, "ἴαρμουθὶ": 8, "Παχὼν": 9, "Παϋνὶ": 10, "Ἐπιφὶ": 11, "Μεσορὴ": 12}

# record: (row, exact date phrase in the row, era year in a common Nabonassar count, month word, day token,
#          part of night/day -> 'eve' (civil day D) | 'pre' (civil day D+1 of "D into D+1") | 'day' (D),
#          local apparent hour of the instant, mean-Sun phrase (exact substring) or None, mean-Sun degrees)
SIGN = {"Κριοῦ": 0, "Ταύρου": 30, "Διδύμων": 60, "Καρκίνου": 90, "Λέοντος": 120, "Παρθένου": 150,
        "Ζυγοῦ": 180, "Χηλῶν": 180, "Σκορπίου": 210, "Τοξότου": 240, "Αἰγόκερω": 270, "Ὑδροχόου": 300,
        "Ἰχθύων": 330}
ANT = lambda n: 884 + n          # 9.10.3: Antoninus 2 = Nabonassar 886
ALEX = lambda n: 424 + n         # 3.7.4: 424 Egyptian years from Nabonassar to Alexander's death
R = {
 # set A (Antoninus 2)
 "IX.10.3":  ("9.10.3", "Ἐπιφὶ βʹ εἰς τὴν γʹ", ANT(2), "Ἐπιφὶ", "βʹ", "eve", 19.5, "ἡ μὲν τοῦ ἡλίου μέση πάροδος κατὰ τὰς ἀποδεδειγμένας ἡμῖν ὑποθέσεις ἐπεῖχεν Ταύρου μοίρας κβ λδ", ("Ταύρου", 22, 34)),
 "X.8.2":    ("10.8.2", "Ἐπιφὶ ιε΄ εἰς τὴν ις΄", ANT(2), "Ἐπιφὶ", "ιε΄", "eve", 21.0, "τοῦ ἡλίου κατ μέσην πάροδον ἐπέχοντος τότε Διδύμων μοίρας ε κζ", ("Διδύμων", 5, 27)),
 # 9.9.4 prints only the post-midnight day ("into the 24th, at dawn"): part 'on' = that numeral is the civil day
 "IX.9.4":   ("9.9.4", "Μεσορὴ εἰς τὴν κδʹ ὄρθρου", ANT(2), "Μεσορὴ", "κδʹ", "on", 5.0, "τοῦ μέσου ἡλίου πάλιν ὄντος περὶ Καρκίνου μοίρας ῑ καὶ γ´", ("Καρκίνου", 10, 20)),
 "XI.2.2":   ("11.2.2", "Μεσορὴ κϚ΄ εἰς τὴν κζ΄", ANT(2), "Μεσορὴ", "κϚ΄", "pre", 5.0, "ἡ μὲν μέση τοῦ ἡλίου πάροδος ἐπεῖχεν Καρκίνου μοίρας ῑϚ ῑᾱ", ("Καρκίνου", 16, 11)),
 # set B (Antoninus 2)
 "X.4.3":    ("10.4.3", "Τυβὶ κθ΄εἰς τὴν λ΄", ANT(2), "Τυβὶ", "κθ΄", "pre", 4.75, "ὁ μὲν ἥλιος μέσως ἐπεῖχεν Τοξότου μοίρας κβ θ", ("Τοξότου", 22, 9)),
 "XI.6.2":   ("11.6.2", "Μεχὶρ Ϛ΄ εἰς τὴν ζ΄", ANT(2), "Μεχὶρ", "Ϛ΄", "eve", 20.0, "τοῦ μέσου ἡλίου ἐπέχοντος Τοξότου μοίρας κη μα", ("Τοξότου", 28, 41)),
 "V.3.2":    ("5.3.2", "Φαμενὼθ κε΄", ANT(2), "Φαμενὼθ", "κε΄", "day", 6.75, "τὸν ἥλιον εὑρίσκομεν μέσως μὲν ἐπέχοντα Ὑδροχόου μοίρας ις κζ", ("Ὑδροχόου", 16, 27)),
 "VII.2.4":  ("7.2.4", "ἴαρμουθὶ θʹ", ANT(2), "ἴαρμουθὶ", "θʹ", "day", 17.5, None, None),
 # set C (Hadrian 19 -> only the difference matters; a dummy common year 0 is used per set)
 "IX.8.3":   ("9.8.3", "Ἀθὺρ ιδʹ εἰς τὴν ιεʹ ἑῷος", 0, "Ἀθὺρ", "ιδʹ", "pre", 5.0, "τοῦ μέσου ἡλίου περὶ τὰς θ καὶ δʹ μοίρας ὄντος τῶν Χηλῶν", ("Χηλῶν", 9, 15)),
 "IV.6.14":  ("4.6.14", "Χοϊὰκ βʹ εἰς τὴν γʹ", 0, "Χοϊὰκ", "βʹ", "eve", 23.0, None, None),
 # set D (Hadrian 16)
 "IX.7.4":   ("9.7.4", "Φαμενὼθ ιϚ´ εἰς τὴν ιζʹ ἑσπέρας", 0, "Φαμενὼθ", "ιϚ´", "eve", 19.0, "ἡ μέση τοῦ ἡλίου πάροδος ἐπεῖχεν Ὑδροχόου μοίρας θ U+2220ʹ δʹ", ("Ὑδροχόου", 9, 45)),
 "X.1.3":    ("10.1.3", "Φαρμουθὶ κα· εἰς τὴν κβ΄, καθʼ ἥν φησιν ὅτι ὁ τῆς Ἀφροδίτης ἑσπέριος", 0, "Φαρμουθὶ", "κα·", "eve", 19.0, "ὁ ἥλιος ὁ μέσος ἐπεῖχεν τότε τῶν Ἰχθύων μοίρας ιδ δʹ", ("Ἰχθύων", 14, 15)),
 # set E (Antoninus 3 = 463 after Alexander's death, 3.1.9)
 "X.3.2b":   ("10.3.2", "Φαρμουθὶ δ΄ εἰς τὴν ε΄ ἐσπέρας", ANT(3), "Φαρμουθὶ", "δ΄", "eve", 19.0, "τοῦ μέσου ἡλίου πάλιν ἐπέχοντος τὰς τοῦ Ὑδροχόου μοίρας κε U+2220΄", ("Ὑδροχόου", 25, 30)),
 "III.1.10": ("3.1.10", "τῷ υξγ΄ ἀπὸ τῆς Ἀλεξάνδρου τελευτῆς ἐαρινὴν ἰσημερίαν εὑρίσκομεν γεγενημένην τῇ ζ΄ τοῦ Παχὼν", ALEX(463), "Παχὼν", "ζ΄", "day", 13.0, None, None),
 # set F (Hadrian 21)
 "X.2.4":    ("10.2.4", "Τυβὶ βʹ εἰς τὴν γʹ ἑσπέρας", 0, "Τυβὶ", "βʹ", "eve", 19.0, "τοῦ μέσου ἡλίου ἐπέχοντος Σκορπίου μοίρας κὲ U+2220΄", ("Σκορπίου", 25, 30)),
 "X.1.6":    ("10.1.6", "Μεχὶρ θ εἰς τὴν ιʹ ἐσπέρας", 0, "Μεχὶρ", "θ", "eve", 19.0, "ὁ δὲ μέσος ὕλιος ἐπεῖχεν Αἰγόκερω μοίρας β ιε'", ("Αἰγόκερω", 2, 15)),
 # set G (Hadrian 18)
 "X.3.2a":   ("10.3.2", "Φαρμουθὶ β΄ εἰς τὴν γ΄, καθʼ ἣν ἑῷος", 0, "Φαρμουθὶ", "β΄", "pre", 5.0, "τοῦ μέσου ἡλίου τότε ἐπέχοντος Ὑδροχόου μοίρας κε U+2220΄", ("Ὑδροχόου", 25, 30)),
 "IX.7.5":   ("9.7.5", "Ἐπιφὶ ιηʹ εἰς τὴν ιθʹ ὄρθρου", 0, "Ἐπιφὶ", "ιηʹ", "pre", 5.0, "ἐπεῖχεν ὁ μέσος ἥλιος Διδύμων μοίρας ῑ·", ("Διδύμων", 10, 0)),
 # set H (Nabonassar 486)
 "IX.7.9":   ("9.7.9", "κατὰ τὸ υπϚʹ ἔτος ἀπὸ Ναβοωασσάρου κατʼ Αἰγυπτίους Χοιὰκ ιζʹ εἰς τὴν ιηʹ ὄρθρου", 486, "Χοιὰκ", "ιζʹ", "pre", 5.0, "ὁ μέσος δηλονότι ἥλιος ἐπεῖχεν Ὑδροχόου μοίρας ιη Ϛ´", ("Ὑδροχόου", 18, 10)),
 "IX.7.11":  ("9.7.11", "κατὰ τὸ υπϚʹ ἔτος πάλιν ἀπὸ Ναβονασσάρου κατʼ Αἰγυπτίους Φαμενὼθ λʹ εἰς τὴν αʹ ἐσπέρας", 486, "Φαμενὼθ", "λʹ", "eve", 19.0, "ὁ μέσος ἥλιος ἐπεῖχεν Κριοῦ μοίρας κθ U+2220´", ("Κριοῦ", 29, 30)),
 "IX.7.14":  ("9.7.14", "κατὰ τὸ υπϚʹ ἔτος ἀπὸ Ναβονασσάρο κατʼ Αἰγυπτίους Παϋνὶ λʹ ἐσπέρας", 486, "Παϋνὶ", "λʹ", "eve", 19.0, "ὁ μέσος ἥλιος ἐπεῖχεν Λέοντος μοίρας κζ U+2220ʹ γʹ", ("Λέοντος", 27, 50)),
 # set I (Nabonassar 484; the +4 is stated in words)
 "IX.10.6a": ("9.10.6", "κατὰ τὸ υπδ ἔτος ἀπὸ Ναβονασσάρου, Σκορπιῶνος κβ κατʼ Αἰγυπτίους Θὼθ ιηʹ εἰς τὴν ιθʹ ἑῷος", 484, "Θὼθ", "ιηʹ", "pre", 5.0, "ἐπεῖχεν ὁ μέσος ἥλιος τῇ ιθʹ τοῦ Θὼθ ὄρθρου καθʼ ἡμᾶς Σκορπίου μοίρας κ U+2220ʹγ΄", ("Σκορπίου", 20, 50)),
 # set J (Nabonassar 476 for both, stated at 10.9.2 and 10.4.6)
 "X.9.2":    ("10.9.2", "κατὰ τὸ υοϚ΄ ἔτος ἀπὸ Ναβονασσάρου, κατʼ Αἰγυπτίους Ἀθὺρ κ΄ εἰς τὴν κα΄ ὄρθρου", 476, "Ἀθὺρ", "κ΄", "pre", 5.0, "τὸν ἥλιον εὑρίσκομεν κατὰ μέσην πάροδον ἐπέχοντα Αἰγόκερω μοίρας κγ νδ", ("Αἰγόκερω", 23, 54)),
 "X.4.6a":   ("10.4.6", "Μεσορὴ ιζ΄ εἰς τὴν ιη΄ ὥρᾳ ιβ΄", 476, "Μεσορὴ", "ιζ΄", "pre", 5.0, "κατὰ μὲν τὴν προτήρησιν ἐπεχούσης Χηλῶν μοίρας ιζ γ", ("Χηλῶν", 17, 3)),
 "X.4.6b":   ("10.4.6", "μετὰ γὰρ δ ἡμέρας τῆς προκειμένης τηρήσεως τῇ κα τοῦ Μεσορὴ εἰς τὴν κβ΄", 476, "Μεσορὴ", "κα", "pre", 5.0, "κατὰ δὲ τὴν ἐξῆς Χηλῶν μοίρας κ νθ", ("Χηλῶν", 20, 59)),
 # set K (Nabonassar 504; 83 after Alexander's death; Nabonassar 512)
 "IX.7.16":  ("9.7.16", "κατὰ τὸ φδʹ ἔτος ἀπὸ Ναβονασσάρου κατʼ Αἰγυπτίους Θὼθ κζʹ εἰς τὴν κηʹ ὄρθρου", 504, "Θὼθ", "κζʹ", "pre", 5.0, "ὁ μέσος ἥλιος Σκορπίου ἐπεῖχεν μοίρας κδ U+2220ʹ γʹ", ("Σκορπίου", 24, 50)),
 "XI.3.2":   ("11.3.2", "κατὰ τὸ πγ΄ ἔτος ἀπὸ τῆς Ἀλεξάνδρου τελευτῆς κατʼ Αἰγυπτίους Ἐπιφὶ ιζ΄ εἰς τὴν ιη΄ ὄρθρου", ALEX(83), "Ἐπιφὶ", "ιζ΄", "pre", 5.0, "τὸν ἥλιον εὑρίσκομεν κατὰ μέσην πάροδον ἐπέχοντα Παρθένου μοίρας θ νϚ", ("Παρθένου", 9, 56)),
 "IX.7.15":  ("9.7.15", "κατὰ τὸ φιβʹ ἔτος ἀπὸ Ναβονασσάρου κατʼ Αἰγυπτίους Θὼθ θʹ εἰς τὴν ιʹ ὄρθρου", 512, "Θὼθ", "θʹ", "pre", 5.0, "ὁ μέσος ἥλιος ἐπεῖχεν Σκορπίου μοίρας ε Ϛ´", ("Σκορπίου", 5, 10)),
 # set L (Hadrian 12, 13, 14: consecutive Egyptian years -> 0, 1, 2)
 "X.1.5":    ("10.1.5", "Ἀθὺρ καʹ εἰς τὴν κβʹ ὁ τῆς Ἀφροδίτης ἑῷος", 0, "Ἀθὺρ", "καʹ", "pre", 5.0, "ὁ δὲ μέσος ἥλιος Ζυγοῦ μοίρας ιζ U+2220΄ γʹ λ΄", ("Ζυγοῦ", 17, 52)),
 "X.2.3":    ("10.2.3", "Ἐπιφὶ β εἰς τὴν γ ἑῷος", 1, "Ἐπιφὶ", "β", "pre", 5.0, "ὁ μέσος ἥλιος ἐπεῖχε τότε Ταύρου μοίρας κε καὶ δύο πέμπτα", ("Ταύρου", 25, 24)),
 "IX.9.3":   ("9.9.3", "Μεσορὴ ιηʹ ἑσπέρας", 2, "Μεσορὴ", "ιηʹ", "eve", 19.0, "τοῦ μέσου ἡλίου τότε ὄντος περὶ Καρκίνου μοίρας ῑ καὶ ιβ´", ("Καρκίνου", 10, 5)),
}
# year-designation check phrases (exact substrings) that make the per-set common year legitimate
YEARS = {"9.10.3": "τῷ βʹ ἔτει Ἀντωνίνου, ὅ ἦν κατὰ τὸ ωπϚʹ ἔτος ἀπὸ Ναβονασσάρου", "10.8.2": "τῷ β΄ ἔτει Ἀντωνίνου",
         "9.9.4": "τῷ δὲ βʹ ἔτει Ἀντωνίνου", "11.2.2": "τῷ β΄ ἔτει Ἀντωνίνου", "10.4.3": "τῷ β΄ ἔτει Ἀντωνίνου",
         "11.6.2": "τῷ β΄ ἔτει Ἀντωνίνου", "5.3.2": "τῷ β΄ ἔτει Ἀντωνίνου", "7.2.4": "τῷ β ἔτει Ἀντωνίνου",
         "9.8.3": "τῷ μὲν οὖν ιθʹ ἔτει Ἀδριανοῦ", "4.6.14": "τῷ ιθʹ ἔτει Ἀδριανοῦ", "9.7.4": "τῷ ιϚ´ ἔτει Ἀδριανοῦ",
         "10.1.3": "τῷ ιϚʹ ἔτει Ἀδριανοῦ", "3.1.9": "τῷ γ΄ ἔτει Ἀντωνίνου, ὅ ἐστιν υξγ΄ ἀπὸ τῆς Ἀλεξάνδρου τελευτῆς",
         "10.2.4": "τῷ κα· ἔτει Ἀδριανοῦ", "10.1.6": "τῷ καʹ ἔτει Ἀδριανοῦ", "9.7.5": "τῷ ιηʹ ἔτει Ἀδριανοῦ",
         "10.4.6": "τὸ μὲν τῆς τηρήσεως ἔτος υος΄ ἐστὶν ἀπὸ Ναβονασσάρου", "10.9.2": "κατὰ τὸ νβ΄ ἔτος ἀπὸ τῆς Ἀλεξάνδρου τελευτῆς, τουτέστιν κατὰ τὸ υοϚ΄ ἔτος ἀπὸ Ναβονασσάρου",
         "3.7.4": "ἀπὸ μὲν τῆς Ναβονασάρου βασιλείας μέχρι τῆς Ἀλεξάνδρου τελευτῆς ἔτη συνάγεται κατʼ Αἰγυπτίους υκδ",
         "10.1.5": "τῷ ιβ΄ ἔτει Ἀδριανοῦ", "10.2.3": "τῷ ιγʹ ἔτει Ἀδριανοῦ", "9.9.3": "τῷ μὲν γὰρ ιδʹ ἔτει Ἀδριανοῦ"}
NFC = lambda x: unicodedata.normalize("NFC", x)
for r, ph in YEARS.items():
    assert NFC(ph) in rows[r], (r, ph)
# the second record of 10.3.2 is Antoninus 3, the first Hadrian 18
assert "τὴν δʼ ἑτέραν ἐτηρήσαμεν τῷ γ΄ ἔτει Ἀντωνίνου" in rows["10.3.2"]
assert "ὧν τὴν μὲν ἑτέραν ἐτηρήσαμεν τῷ ιη΄ ἔτει Ἀδριανοῦ" in rows["10.3.2"]
# civil-day assignment for records whose hour is not stated comes from ἑῷος / ἑσπέριος / the night designation

MOT = (59 + 8 / 60 + 17 / 3600 + 13 / 60 ** 3 + 12 / 60 ** 4 + 31 / 60 ** 5) / 60  # deg/day, row 3.1.14


def civil(rec):
    row, phrase, year, mword, dtok, part, hour, ms, msv = R[rec]
    assert NFC(phrase) in rows[row], (rec, phrase)
    assert mword in phrase and dtok in phrase, rec
    d = gnum(dtok)
    m = MONTH[mword]
    n = 365 * year + 30 * (m - 1) + d + (1 if part == "pre" else 0)
    return n, d, m, part, hour


def meansun(rec):
    row, phrase, year, mword, dtok, part, hour, ms, msv = R[rec]
    if not ms:
        return None
    assert NFC(ms) in rows[row], (rec, ms)
    sgn, deg, mnt = msv
    return SIGN[sgn] + deg + mnt / 60


SETS = {"ALM-A": ["IX.10.3", "X.8.2", "IX.9.4", "XI.2.2"], "ALM-B": ["X.4.3", "XI.6.2", "V.3.2", "VII.2.4"],
        "ALM-C": ["IX.8.3", "IV.6.14"], "ALM-D": ["IX.7.4", "X.1.3"], "ALM-E": ["X.3.2b", "III.1.10"],
        "ALM-F": ["X.2.4", "X.1.6"], "ALM-G": ["X.3.2a", "IX.7.5"], "ALM-H": ["IX.7.9", "IX.7.11", "IX.7.14"],
        "ALM-I": ["IX.10.6a"], "ALM-J": ["X.9.2", "X.4.6a", "X.4.6b"], "ALM-K": ["IX.7.16", "XI.3.2", "IX.7.15"],
        "ALM-L": ["X.1.5", "X.2.3", "IX.9.3"]}
filed = {(c["set"], c["record"]): c["day_offset"] for c in clues if c["kind"] == "interval"}
forks = {(c["set"], c["record"]): {o["option"]: o["operational"]["day_offset"] for o in c["fork_options"]}
         for c in clues if c["kind"] == "interval" and c["fork_options"]}
print("WARNING: contains date words (licence-check record; the searcher must not read this file)\n")
print("mean-Sun motion used: %.8f deg/day (row 3.1.14: 0;59,8,17,13,12,31)\n" % MOT)
bad = 0
for s, recs in SETS.items():
    n0, *_ , h0 = civil(recs[0])
    ms0 = meansun(recs[0])
    for rec in recs[1:]:
        n, d, m, part, h = civil(rec)
        off = n - n0
        f = filed.get((s, rec))
        line = "%s %-9s civil-day offset from text dates = %5d ; file day_offset = %s" % (s, rec, off, f)
        ms = meansun(rec)
        if ms is not None and ms0 is not None:
            # elapsed days implied by the mean Sun (add whole years from the day count)
            el_dates = off + (h - h0) / 24.0
            dl = (ms - ms0) % 360.0
            yrs = round((el_dates * MOT - dl) / 360.0)
            el_sun = (dl + 360.0 * yrs) / MOT
            line += " ; elapsed from dates %.2f d, from Ptolemy's mean Sun %.2f d (diff %+.2f)" % (el_dates, el_sun, el_sun - el_dates)
        if f != off:
            line += "  <-- MISMATCH"
            bad += 1
        if (s, rec) in forks:
            line += "  [file forks: %s]" % forks[(s, rec)]
        print(line)
# set I: +4 in words, and the second record's day numeral agrees
r = rows["9.10.6"]
assert "μετὰ δ ἡμέρας τῇ κϚʹ τοῦ Σκορπιῶνος" in r and "Σκορπιῶνος κβ" in r
print("ALM-I IX.10.6b stated in words 'μετὰ δ ἡμέρας' = 4 ; day numerals κβ -> κϚ: %d -> %d (+%d) ; file day_offset = %s"
      % (gnum("κβ"), gnum("κϚʹ"), gnum("κϚʹ") - gnum("κβ"), filed.get(("ALM-I", "IX.10.6b"))))
r = rows["10.4.6"]
assert "μετὰ γὰρ δ ἡμέρας τῆς προκειμένης τηρήσεως" in r
print("ALM-J X.4.6b also stated in words 'μετὰ γὰρ δ ἡμέρας' = 4 after X.4.6a")
# Rows that state only the TRUE Sun (or an equinox): convert to the mean Sun with Ptolemy's solar model
# (apogee Gemini 5;30: rows 3.7.3 and 3.8.1; eccentricity 2;30 for radius 60: row 3.4.7; true = mean - q,
#  tan q = e sin a / (1 + e cos a), a = mean - apogee) and compare with the set's anchor.
import math
APO, ECC = 65.5, 2.5 / 60


def mean_from_true(lt):
    lm = lt
    for _ in range(50):
        a = math.radians(lm - APO)
        q = math.degrees(math.atan2(ECC * math.sin(a), 1 + ECC * math.cos(a)))
        lm = lt + q
    return lm % 360


TRUE = {"IV.6.14": ("4.6.14", "ἐπεῖχεν ὁ ἥλιος ἀκριβῶς τῶν Χηλῶν μοίρας κε ςʹ", 180 + 25 + 10 / 60, 23.0, "ALM-C", "IX.8.3"),
        "VII.2.4": ("7.2.4", "ἐπεῖχεν ὁ ἥλιος ἀκριβῶς Ἰχθύων μοίρας γ καὶ κʹ ἔγγιστα μιᾶς μοίρας μέρος", 330 + 3 + 1 / 20, 17.5, "ALM-B", "X.4.3"),
        "III.1.10": ("3.1.10", "ἐαρινὴν ἰσημερίαν εὑρίσκομεν γεγενημένην", 0.0, 13.0, "ALM-E", "X.3.2b")}
print("\nrows with only the true Sun (or the equinox), via Ptolemy's solar model:")
for rec, (row, ph, lt, hour, s, anchor) in TRUE.items():
    assert NFC(ph) in rows[row], (rec, ph)
    lm = mean_from_true(lt)
    n0, *_, h0 = civil(anchor)
    n, *_ = civil(rec)
    el_dates = (n - n0) + (hour - h0) / 24.0
    el_sun = ((lm - meansun(anchor)) % 360.0) / MOT
    print("%s %-9s true Sun %.2f -> mean %.2f ; elapsed from dates %.2f d, from the Sun %.2f d (diff %+.2f)"
          % (s, rec, lt, lm, el_dates, el_sun, el_sun - el_dates))
# what the ALM-C anchor's civil day would give if IX.8.3 (ἑῷος, no hour) were put in the evening instead
print("ALM-C if IX.8.3 were an evening sighting (civil day D, not D+1): offset would be %d, elapsed %.2f d"
      % (civil("IV.6.14")[0] - (civil("IX.8.3")[0] - 1), (civil("IV.6.14")[0] - civil("IX.8.3")[0] + 1) + (23.0 - 19.0) / 24))
print("\nmismatches:", bad)
