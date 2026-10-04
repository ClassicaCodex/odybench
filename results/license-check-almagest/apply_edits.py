"""Licence check of data/prereg/controls_almagest.json (license-check-almagest task).

Reads the pre-edit copy results/license-check-almagest/controls_almagest.before.json,
applies the edits listed in docs/license-check-almagest.md, adds a
'license_check' field to every clue row, validates, and writes
data/prereg/controls_almagest.json in place (indent 1, UTF-8, CRLF, as before).

No truth file and not docs/research-controls.md were read. Every Greek fragment
added to a licence_words string is cut out of the cited data/text row by
frag() below, so it is an exact substring by construction.
"""
import json, sys, copy, hashlib, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = 'C:/Projects/odybench/'
SRC = BASE + 'results/license-check-almagest/controls_almagest.before.json'
DST = BASE + 'data/prereg/controls_almagest.json'
PRE = 'urn:cts:greekLit:tlg0363.tlg001.1st1K-grc1.'
ROWS = {}
for line in open(BASE + 'data/text/ptolemy-syntaxis-grc.tsv', encoding='utf-8'):
    k, _, t = line.rstrip('\n').partition('\t')
    ROWS[k.replace(PRE, '')] = t

import unicodedata
def _n1(s):
    """per-character NFC (oxia -> tonos etc.); keeps length so indices map 1:1"""
    out = []
    for ch in s:
        n = unicodedata.normalize('NFC', ch)
        out.append(n if len(n) == 1 else ch)
    return ''.join(out)

def frag(ref, start, end=None, nth=0):
    """exact (raw) substring of row `ref` from the nth occurrence of `start` to the
    first following occurrence of `end` (inclusive); `end` None -> start only.
    Matching ignores the tonos/oxia accent-encoding difference; the returned
    text is the row's own characters."""
    t = ROWS[ref]
    tn, sn = _n1(t), _n1(start)
    i = -1
    for _ in range(nth + 1):
        i = tn.find(sn, i + 1)
        assert i >= 0, (ref, start)
    if end is None:
        return t[i:i + len(start)]
    en = _n1(end)
    j = tn.find(en, i + len(sn))
    assert j >= 0, (ref, end)
    return t[i:j + len(en)]

E = ' … '
d = json.load(open(SRC, encoding='utf-8'))
before_sha = hashlib.sha256(open(SRC, 'rb').read()).hexdigest()
C = {c['clue_id']: c for c in d['clues']}
S = {s['set']: s for s in d['sets']}
log = {}

def edit(cid, why):
    log.setdefault(cid, []).append(why)

def fork(cid, name):
    return next(o for o in C[cid]['fork_options'] if o['option'] == name)

def add_unbounded(cid, side):
    """add the literal, unbounded reading of 'not yet at' / 'past' greatest elongation"""
    if side == 'after':
        opt = {'option': 'ge_after_same_apparition',
               'justification': "literal reading of the words: the greatest elongation on this side is still to come in the SAME apparition; the words give no number of days, so no bound is imposed (the j-day options above are narrower readings)",
               'operational': {'bound': 'same_apparition'}, 'primary': False}
    else:
        opt = {'option': 'ge_before_same_apparition',
               'justification': "literal reading of the words: the greatest elongation on this side already fell earlier in the SAME apparition; the words give no number of days, so no bound is imposed (the j-day options above are narrower readings)",
               'operational': {'bound': 'same_apparition'}, 'primary': False}
    C[cid]['fork_options'].insert(1, opt)

BODY_NOTE = ' The planet is not named in this row: {w} ({r}) names it.'

# ---------------- ALM-A ----------------
t_9103 = frag('9.10.3', 'πρὸ δ', 'ἰσημερινῶν') + E + frag('9.10.3', 'μεσονυκτίου')
C['ALM-A.1']['licence_words'] += E + t_9103
add_unbounded('ALM-A.1', 'after')
edit('ALM-A.1', "licence_words lacked the words for the time of day the statement gives (4 1/2 equinoctial hours before midnight); added them (the day numeral inside the phrase is left out, as a date word). Fork set incomplete: every option bounded 'not yet' to <= 30 days or dropped it; added the literal unbounded option 'ge_after_same_apparition'")
C['ALM-A.2']['licence_words'] += E + t_9103
edit('ALM-A.2', 'licence_words lacked the words for the stated time of day (4 1/2 equinoctial hours before midnight); added them')
C['ALM-A.5']['licence_words'] = frag('10.8.2', 'πρὸ τριῶν', 'μεσονυκτίου') + E + C['ALM-A.5']['licence_words']
edit('ALM-A.5', 'licence_words lacked the words for the stated time of day (3 equinoctial hours before midnight); added them')
C['ALM-A.7']['licence_words'] = frag('9.9.4', 'ὄρθρου') + E + C['ALM-A.7']['licence_words']
C['ALM-A.7']['notes'] += BODY_NOTE.format(w="the chapter heading 'τῶν τοῦ τοῦ Ἑρμοῦ ἀνωμαλιῶν'", r='9.9.1') + " (the row has only 'αὐτοῦ')."
edit('ALM-A.7', "licence_words lacked the word for the stated time of day ('ὄρθρου', at dawn); added it. Note added: Mercury is named only in the chapter heading 9.9.1, not in this row")
t_1122 = frag('11.2.2', 'πρὸ τῆς τοῦ ἡλίου ἀνατολῆς', 'μεσονυκτίου')
C['ALM-A.9']['statement'] = 'Jupiter is seen (sighted with the astrolabe) before sunrise, about 5 equinoctial hours after midnight.'
C['ALM-A.9']['licence_words'] = t_1122 + E + frag('11.2.2', 'ὁ τοῦ Διὸς ἐπέχων ἐφαίνετο')
edit('ALM-A.9', "statement said '(a morning object)', which can be read as heliacal morning-star status; the words say only that Jupiter was sighted before sunrise, about 5 equinoctial hours after midnight. Statement reworded and the licence extended to the time words and the sighting words. Operational option unchanged")
C['ALM-A.10']['licence_words'] = frag('11.2.2', 'μετὰ ε ὥρας', 'μεσονυκτίου') + E + C['ALM-A.10']['licence_words']
edit('ALM-A.10', 'licence_words lacked the words for the stated time of day (about 5 equinoctial hours after midnight); added them')

# ---------------- ALM-B ----------------
t_1043 = frag('10.4.3', 'ὁ δὲ χρόνος ἦν μετὰ', 'μεσονυκτίου')
C['ALM-B.1']['licence_words'] += E + t_1043
add_unbounded('ALM-B.1', 'before')
edit('ALM-B.1', "licence_words lacked the words for the stated time of day (4 3/4 equinoctial hours after midnight); added them. Fork set incomplete: 'after greatest elongation' was bounded to <= 60 days or dropped; added the literal unbounded option 'ge_before_same_apparition'")
C['ALM-B.2']['statement'] = "At 4 3/4 equinoctial hours after midnight the Moon's apparent centre, Venus and beta Sco stand in one line, Venus just west of the Moon."
C['ALM-B.2']['licence_words'] += E + t_1043
edit('ALM-B.2', "statement said 'Before dawn', which the words do not say (they give 4 3/4 equinoctial hours after midnight; whether that is before dawn depends on the season, which the clue file does not use). Reworded to the stated hour and added the time words to the licence")
C['ALM-B.5']['licence_words'] = frag('11.6.2', 'πρὸ δ ὡρῶν', 'μεσονυκτίου') + E + C['ALM-B.5']['licence_words']
edit('ALM-B.5', 'licence_words lacked the words for the stated time of day (4 equinoctial hours before midnight); added them')
C['ALM-B.7']['licence_words'] = frag('5.3.2', 'μετὰ μὲν τὴν ἀνατολὴν', 'μεσημβρίας') + E + C['ALM-B.7']['licence_words']
edit('ALM-B.7', 'licence_words lacked the words for the stated time of day (after sunrise, 5 1/4 equinoctial hours before noon); added them')
C['ALM-B.9']['licence_words'] = (frag('7.2.4', 'μέλλοντος μὲν δύνειν', 'ἡλίου') + E +
                                  frag('7.2.4', 'μετὰ ἐ', 'ἴσημερινὰς') + E +
                                  C['ALM-B.9']['licence_words'] + E +
                                  frag('7.2.4', 'μοιρῶν εἰς τὰ ἑπόμενα', 'διάστασιν'))
edit('ALM-B.9', "licence_words lacked the words for the stated time (Sun about to set, 5 1/2 hours after noon) and for the direction 'east' ('εἰς τὰ ἑπόμενα', later in the same row); added them (the day numeral in the time phrase is left out)")

# ---------------- ALM-C ----------------
C['ALM-C.1']['statement'] = 'Mercury is a morning star (ἑῷος) at about its greatest western (morning) elongation on this day; no hour is stated.'
edit('ALM-C.1', "statement said '(before dawn)'; the row has no hour word, only 'ἑῷος' (as a morning star). Reworded; operational options unchanged")

# ---------------- ALM-D ----------------
C['ALM-D.1']['licence_words'] = frag('9.7.4', 'ἑσπέρας', 'ἀστέρα') + E + C['ALM-D.1']['licence_words']
edit('ALM-D.1', "licence_words lacked the word for the stated time of day ('ἑσπέρας', in the evening); added it")

# ---------------- ALM-E ----------------
C['ALM-E.1']['licence_words'] = (frag('10.3.2', 'ἐσπέρας, καθʼ', 'ἡλίου') + E +
                                  frag('10.3.2', 'τὴν ἑσπερίαν τῆς μέσης', 'ἀπόστασιν'))
edit('ALM-E.1', "licence_words did not contain the words for 'evening' (time of day and side of the Sun); replaced by the contiguous phrase that includes 'ἐσπέρας' plus 'τὴν ἑσπερίαν τῆς μέσης μεγίστην ἀπόστασιν' from the same row")
C['ALM-E.2']['notes'] += ". The two records are dated in different eras; the link between them is stated in the text itself at 3.1.9 (Ptolemy equates the regnal year of 10.3.2's second record with the year 'from Alexander's death' that 3.1.10 uses), so the interval needs no outside chronology"
edit('ALM-E.2', 'notes only: recorded that the cross-era link the interval needs is stated at 3.1.9 (checked; interval recomputed = 33)')
C['ALM-E.3']['notes'] = "Ptolemy's verb is 'εὑρίσκομεν' (we find); 3.1.9 says the matching autumn equinox of the same year was observed ('ἐτηρήσαμεν')"
edit('ALM-E.3', "notes said 'observed equinox' and glossed 'εὑρίσκομεν' as observed; corrected to the verb's meaning (we find). Clue unchanged")

# ---------------- ALM-F ----------------
C['ALM-F.1']['licence_words'] = frag('10.2.4', 'ἑσπέρας τὸν τῆς', 'ἡλίου')
edit('ALM-F.1', "licence_words lacked the word for 'evening' ('ἑσπέρας'); replaced by the contiguous phrase that includes it")
C['ALM-F.3']['licence_words'] = frag('10.1.6', 'ἐσπέρας ἐτηρήσαμεν', 'ἡλίου') + E + frag('10.1.6', 'ἡ ἑσπερία μεγίστη διάστασις')
edit('ALM-F.3', "licence_words lacked the words for 'evening'; replaced by the contiguous phrase that includes 'ἐσπέρας' plus 'ἡ ἑσπερία μεγίστη διάστασις'")
f4 = C['ALM-F.4']
f4['statement'] = f4['statement'].replace('seeming to outshine/touch it', 'seeming to outshine it')
f4['notes'] = f4['notes'].replace('seeming to outshine/touch it', 'seeming to outshine it')
for k in ('statement', 'notes'):
    assert 'nearest of lambda, phi, psi1-3 Aqr' in f4[k]
    f4[k] = f4[k].replace('nearest of lambda, phi, psi1-3 Aqr', "drafter's candidates lambda, phi, psi1-3 Aqr, each a separate branch")
fork('ALM-F.4', 'positional')['primary'] = False
fork('ALM-F.4', 'none')['primary'] = True
fork('ALM-F.4', 'positional')['operational']['star_candidates'] = ['lambda Aqr', 'phi Aqr', 'psi1 Aqr', 'psi2 Aqr', 'psi3 Aqr']
fork('ALM-F.4', 'positional')['operational']['candidate_rule'] = 'each candidate is a separate garden branch (the identification is the drafter\'s, not the text\'s); do not pick the best-fitting one silently'
fork('ALM-F.4', 'positional')['justification'] = "the stated offset holds within the tolerance for the named candidate star; the star is not securely identified, so this reading is not the default"
edit('ALM-F.4', "the row's notes said 'none' is the default because the star is not securely identified, but 'positional' was marked primary: made 'none' primary to match. The positional option named no star, so it was not operational; added the candidate list the statement gives, each as its own branch. 'touch' dropped from the gloss of 'καταλάμπειν' (outshine), and 'nearest of' the candidates (a silent best-fit choice) replaced by one branch per candidate")

# ---------------- ALM-G ----------------
C['ALM-G.1']['statement'] = 'Venus is a morning star (ἑῷος) at its greatest western (morning) elongation on this day; no hour is stated.'
edit('ALM-G.1', "statement said '(before dawn)'; the record has no hour word, only 'ἑῷος'. Reworded; operational options unchanged")
C['ALM-G.3']['licence_words'] = frag('9.7.5', 'ὄρθρου', 'φαινόμενος') + E + frag('9.7.5', 'ἡ μεγίστη τῆς μέσης ἀπόστασις ἑῴα')
edit('ALM-G.3', "licence_words fragments were out of text order and lacked the time word; replaced by the contiguous phrase from 'ὄρθρου' (at dawn) plus 'ἡ μεγίστη τῆς μέσης ἀπόστασις ἑῴα'")

# ---------------- ALM-H ----------------
C['ALM-H.1']['licence_words'] = frag('9.7.9', 'ἑῷος ὁ Στίλβων') + E + frag('9.7.9', 'ὄρθρου', 'ἑῴα')
C['ALM-H.1']['notes'] = ("the old record's own words say only 'ἑῷος'; the greatest-elongation status is Ptolemy's (narrator's) statement in this row "
                         "('γέγονεν ἄρα ἡ μεγίστη τῆς μέσης ἀπόστασις ἑῴα') and his selection rule for the chapter (9.7.2 'μεγίστων ἀποστάσεων τηρήσεις'; 9.7.8). "
                         "The text also gives a zodiacal longitude and an elongation in degrees; they are NOT used (B&M's clue grammar has no coordinates)")
fork('ALM-H.1', 'ge_true_k')['justification'] = "Ptolemy's statement in this row ('γέγονεν ἄρα ἡ μεγίστη τῆς μέσης ἀπόστασις ἑῴα') and his selection rule (9.7.2, 9.7.8) that these old records are greatest-elongation records; read as GE within k days"
edit('ALM-H.1', "licence_words quoted a fragment from another row (9.7.8) with a '[9.7.8]' prefix, so it was not a substring of the cited row; the cited row 9.7.9 itself carries Ptolemy's greatest-elongation statement and the time word 'ὄρθρου'; replaced with those, and moved the 9.7.2/9.7.8 references into notes and the justification")
for cid, ref in (('ALM-H.4', '9.7.11'), ('ALM-H.8', '9.7.14')):
    C[cid]['licence_words'] = frag(ref, 'ἑσπέρας') + E + frag(ref, 'γέγονεν ἄρα', 'ἑσπερία')
    C[cid]['notes'] = ("the old record's own words say only 'ἑσπέρας'; the greatest-elongation status is Ptolemy's (narrator's) statement in this row "
                       "('γέγονεν ἄρα ἡ μεγίστη τῆς μέσης ἀπόστασις ἑσπερία') and his selection rule for the chapter (9.7.2; for 9.7.11 also 9.7.10 and 9.7.13). "
                       "The planet is not named in this row: the chapter heading 9.7.1 ('τοῦ τοῦ Ἑρμοῦ ἀστέρος') names it. "
                       "The text also gives a zodiacal longitude and an elongation in degrees; they are NOT used (B&M's clue grammar has no coordinates)")
    fork(cid, 'ge_true_k')['justification'] = f"Ptolemy's statement in this row ({ref}: 'γέγονεν ἄρα ἡ μεγίστη τῆς μέσης ἀπόστασις ἑσπερία') and his selection rule (9.7.2) that these old records are greatest-elongation records; read as GE within k days"
    edit(cid, f"licence_words quoted '[{'9.7.10' if cid == 'ALM-H.4' else '9.7.14'}] …' with a bracketed row prefix, so it was not an exact substring of the cited row; replaced with the same-row words of Ptolemy's greatest-elongation statement. Notes: the planet is named only in the chapter heading 9.7.1")
fork('ALM-H.3', 'mean_sun_emended')['justification'] = "day implied by the mean-Sun longitude Ptolemy states in the same sentence, under his own solar tables; the printed date conflicts with it by 30 days, i.e. by one Egyptian month (textual crux; checked independently: results/license-check-almagest/meansun_check.txt)"
edit('ALM-H.3', "fork justification said the printed 'day numeral' conflicts with the mean Sun; the conflict is 30 days (a month, not a day numeral). Wording corrected; the two options and their values (102 / 72) verified independently from the stated mean-Sun longitudes")
for cid in ('ALM-H.5', 'ALM-H.6', 'ALM-H.9'):
    C[cid]['notes'] += '.' + BODY_NOTE.format(w="the chapter heading 'τοῦ τοῦ Ἑρμοῦ ἀστέρος'", r='9.7.1')
    edit(cid, 'notes only: Mercury is named only in the chapter heading 9.7.1, not in the cited row')

# ---------------- ALM-I ----------------
C['ALM-I.1']['licence_words'] += E + frag('9.10.6', 'ὄρθρου')
add_unbounded('ALM-I.1', 'after')
edit('ALM-I.1', "licence_words lacked the time word ('ὄρθρου', in Ptolemy's sentence on the same morning); added it. Fork set incomplete: 'not yet at greatest elongation' was bounded to <= 30 days or dropped; added the literal unbounded option 'ge_after_same_apparition'")
C['ALM-I.4']['licence_words'] = frag('9.10.6', 'μετὰ δ ἡμέρας')
C['ALM-I.4']['notes'] = "interval stated in words ('μετὰ δ ἡμέρας', four days later); the second record carries only a date in another (non-Egyptian) calendar, whose day numeral agrees (+4). Calendar words withheld from this file"
edit('ALM-I.4', "licence_words was the interval phrase followed by a bracketed placeholder, so not an exact substring; the placeholder also called both dates Egyptian, but the second record has only a non-Egyptian calendar date and the interval is stated in words. Licence reduced to 'μετὰ δ ἡμέρας'; notes corrected")

# ---------------- ALM-J ----------------
add_unbounded('ALM-J.4', 'before')
fork('ALM-J.4', 'ge_before_same_apparition')['justification'] = "literal reading of Ptolemy's 'παρεληλύθει … τὴν μεγίστην ἑῴαν ἀπόστασιν': the greatest morning elongation already fell earlier in the SAME apparition; the words give no number of days, so no bound is imposed"
C['ALM-J.4']['notes'] += "; 'twelfth hour' is of the night: the record is dated to the night between two days (date words withheld)"
edit('ALM-J.4', "fork set incomplete: 'had passed greatest elongation' was bounded to <= 60 days or dropped; added the literal unbounded option 'ge_before_same_apparition'. Note added on why 'ὥρᾳ ιβ΄' is the last hour of the night")
C['ALM-J.6']['licence_words'] = frag('10.4.6', 'μετὰ γὰρ δ ἡμέρας', 'τηρήσεως')
C['ALM-J.6']['notes'] = ("+267 days to the first Venus report from the Egyptian dates the text states (the same era year for both records, stated at 10.9.2 and 10.4.6), "
                         "then +4 stated in words ('μετὰ γὰρ δ ἡμέρας'); the Egyptian date of the second report agrees (+4). Date words withheld")
edit('ALM-J.6', "licence_words was the interval phrase followed by a bracketed placeholder, so not an exact substring; reduced to the phrase itself and the derivation (267 from the stated dates + 4 in words) moved to notes")
C['ALM-J.7']['licence_words'] = frag('10.4.6', 'ὁ μὲν τῆς Ἀφροδίτης ἀστὴρ ἐπεῖχεν', 'ς΄') + E + C['ALM-J.7']['licence_words']
edit('ALM-J.7', "licence_words quoted only the second of the two longitudes whose difference the statement uses; added the first ('Παρθένου μοίρας δ ς΄')")

# ---------------- ALM-K ----------------
for cid, ref, tail in (('ALM-K.1', '9.7.16', 'γέγονεν ἄρα καὶ αὕτη ἡ διάστασις'),
                       ('ALM-K.7', '9.7.15', 'γέγονεν ἄρα ἡ ἑῴα μεγίστη διάστασις')):
    head = C[cid]['licence_words'].split(E)[0]
    assert head in ROWS[ref]
    C[cid]['licence_words'] = head + E + frag(ref, 'ὄρθρου') + E + frag(ref, tail)
    fork(cid, 'ge_true_k')['justification'] = (f"Ptolemy's statement in this row ({ref}: '{tail}'"
        + (", 'this distance too', i.e. like 9.7.15's 'ἡ ἑῴα μεγίστη διάστασις'" if cid == 'ALM-K.1' else '')
        + ") and 9.7.17 ('τῶν δὲ μεγίστων ἀποστάσεων') that these old records are greatest-elongation records; read as GE within k days")
    C[cid]['notes'] = ("the old record's own words say only 'ἑῷος'; the greatest-elongation status is Ptolemy's (narrator's) statement (this row; 9.7.17). "
                       "The planet is not named in this row: the chapter heading 9.7.1 names it. "
                       "The text also gives a zodiacal longitude and an elongation in degrees; they are NOT used (B&M's clue grammar has no coordinates)")
    edit(cid, f"licence_words carried a '[{ref}]' prefix inside the string, so it was not an exact substring; replaced with exact same-row words and added the time word 'ὄρθρου'. For K.1 the same-row words say only 'this distance too', so the justification now also cites 9.7.17 'τῶν δὲ μεγίστων ἀποστάσεων'. Notes: the planet is named only in 9.7.1" if cid == 'ALM-K.1' else
         f"licence_words carried a '[{ref}]' prefix inside the string, so it was not an exact substring; replaced with exact same-row words and added the time word 'ὄρθρου'. Notes: the planet is named only in 9.7.1")
C['ALM-K.3']['notes'] += ". The two records are dated in different eras; the link (the number of Egyptian years between the two eras) is stated in the text at 3.7.4 and again by the pair of years at 10.9.2, so the interval needs no outside chronology"
edit('ALM-K.3', 'notes only: recorded the text-stated era link (3.7.4; 10.9.2) the interval needs (checked; interval recomputed = 1385)')
for cid in ('ALM-K.2', 'ALM-K.8'):
    C[cid]['notes'] += '.' + BODY_NOTE.format(w="the chapter heading 'τοῦ τοῦ Ἑρμοῦ ἀστέρος'", r='9.7.1')
    edit(cid, 'notes only: Mercury is named only in the chapter heading 9.7.1, not in the cited row')

# ---------------- ALM-L ----------------
for cid in ('ALM-L.1', 'ALM-L.4'):
    C[cid]['statement'] = 'Venus is a morning star (ἑῷος) at its greatest western (morning) elongation on this day; no hour is stated.'
    edit(cid, "statement said '(before dawn)'; the record has no hour word, only 'ἑῷος'. Reworded; operational options unchanged")
l2 = C['ALM-L.2']
old = 'by a Pleiad-length (1 1/2 deg) or less;'
new = "by a Pleiad-length (1 1/2 deg) less the planet's own size ('ἢ ἔλασσον τῷ ἑαυτοῦ μεγέθει');"
assert old in l2['statement'] and old in l2['notes']
l2['statement'] = l2['statement'].replace(old, new)
l2['notes'] = l2['notes'].replace(old, new)
edit('ALM-L.2', "statement glossed 'Πλειάδος μῆκος ἢ ἔλασσον τῷ ἑαυτοῦ μεγέθει' as 'a Pleiad-length or less'; the words say less by the planet's own size (a few arcminutes), not any amount less. Wording corrected; tolerances unchanged")
C['ALM-L.6']['licence_words'] = frag('9.9.3', 'ἑσπέρας') + E + C['ALM-L.6']['licence_words'] + E + frag('9.9.3', 'τὴν ἑσπερίαν μεγίστην ἀπόστασιν')
C['ALM-L.6']['notes'] += '.' + BODY_NOTE.format(w="the chapter heading 'τῶν τοῦ τοῦ Ἑρμοῦ ἀνωμαλιῶν'", r='9.9.1') + " The record is reported ('φησίν')."
edit('ALM-L.6', "licence_words lacked the words for 'evening' (time and side); added 'ἑσπέρας' and 'τὴν ἑσπερίαν μεγίστην ἀπόστασιν'. Note: Mercury is named only in the chapter heading 9.9.1")
C['ALM-L.7']['notes'] += '.' + BODY_NOTE.format(w="the chapter heading 'τῶν τοῦ τοῦ Ἑρμοῦ ἀνωμαλιῶν'", r='9.9.1')
edit('ALM-L.7', 'notes only: Mercury is named only in the chapter heading 9.9.1, not in the cited row')

# ---------------- set-level descriptions ----------------
S['ALM-A']['description'] = "Mercury evening star beside the Moon (Day 0); Mars about three days past opposition beside the Moon; Mercury at greatest morning elongation; Moon beside Jupiter before sunrise. Four records over about 55 days. (Lunar phases are inferred, and entered only as forks with a 'none' option.)"
S['ALM-B']['description'] = "Venus morning star past greatest elongation beside the Moon (Day 0); Moon beside Saturn 4 hours before midnight; two Sun-Moon elongation measurements (about last and first quarter). Four records over about 70 days. (The phase of the Moon in the first two records is inferred, fork with 'none'.)"
S['ALM-C']['description'] = 'Mercury morning star about greatest elongation (Day 0) and a partial lunar eclipse on civil day +17.'
S['ALM-L']['description'] = "LONG (about 2.7 years): three records of one written collection: Venus at greatest morning elongation twice, then Mercury at greatest evening elongation 3 5/6 deg east of Regulus."

# ---------------- license_check field ----------------
for c in d['clues']:
    why = log.get(c['clue_id'])
    c['license_check'] = 'ok' if not why else 'edited: ' + ' | '.join(why)

d['license_check'] = {
    'checked': '2026-10-04',
    'by': 'independent licence check (an agent that did not draft these sets; read no truth file and not docs/research-controls.md or docs/controls-almagest.md)',
    'report': 'docs/license-check-almagest.md',
    'rows_checked': len(d['clues']),
    'rows_edited': sum(1 for c in d['clues'] if c['license_check'] != 'ok'),
    'pre_edit_sha256': before_sha,
    'pre_edit_copy': 'results/license-check-almagest/controls_almagest.before.json',
    'script': 'results/license-check-almagest/apply_edits.py',
    'interval_recomputation': 'results/license-check-almagest/egyptian_check.txt (Egyptian dates as they stand in the text) and meansun_check.txt (Ptolemy\'s stated mean-Sun longitudes): all 19 date-derived intervals reproduce; the two forked cruxes (ALM-A.6, ALM-H.3) are confirmed',
    'set_descriptions_edited': ['ALM-A', 'ALM-B', 'ALM-C', 'ALM-L'],
    'warning': 'results/controls-almagest/build_prereg.py writes this file; re-running it would silently undo these edits unless they are ported into it',
}

# ---------------- validation ----------------
problems = []
for c in d['clues']:
    t = ROWS[c['ref'].replace(PRE, '')]
    lw = c['licence_words']
    if not lw.startswith('['):
        for p in [p.strip() for p in lw.split('…') if p.strip()]:
            if p not in t:
                problems.append((c['clue_id'], 'licence fragment not in row', p[:50]))
    fo = c['fork_options']
    if fo:
        n = sum(1 for o in fo if o.get('primary'))
        if n != 1:
            problems.append((c['clue_id'], 'primary count', n))
        names = [o['option'] for o in fo]
        if len(set(names)) != len(names):
            problems.append((c['clue_id'], 'duplicate option names'))
        for o in fo:
            if not o.get('justification'):
                problems.append((c['clue_id'], 'option without justification', o['option']))
    if c['kind'] == 'moon-phase' and any(o['option'] == 'phase_class' and 'inference' in o['justification'] for o in fo):
        if not any(o['option'] == 'none' for o in fo):
            problems.append((c['clue_id'], "inferred phase without 'none'"))
# day_offset consistency per record
rec_off = {}
for c in d['clues']:
    rec_off.setdefault((c['set'], c['record']), set()).add(c['day_offset'])
for k, v in rec_off.items():
    if len(v) != 1:
        problems.append((k, 'record with several day_offsets', v))
# leak scan
s = json.dumps(d, ensure_ascii=False)
for pat in [r'\bBC\b', r'\bAD\b', 'Julian', 'Ἀντωνίνου', 'Ἀδριανοῦ', 'Ναβον', 'Διονύσ', 'Θέων', 'Τιμόχαρ', 'Ἵππαρχ', 'Χαλδ',
            'Θὼθ', 'Μεσορ', 'Ἐπιφ', 'Παχ', 'Ἀθὺρ', 'Τυβ', 'Μεχ', 'Φαμεν', 'Φαρμ', 'Παϋν', 'Χοι', 'Ἰαρμ',
            'Hadrian', 'Antonin', 'Nabonass', 'Dionys', 'Theon', 'Timochar', 'Hipparch', 'Chalde']:
    if re.search(pat, s):
        problems.append(('LEAK?', pat))
print('problems:', problems)
assert not problems
with open(DST, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(json.dumps(d, ensure_ascii=False, indent=1))
print('rows edited:', d['license_check']['rows_edited'], 'of', len(d['clues']))
for c in d['clues']:
    print(c['clue_id'], '|', c['license_check'][:110])
