"""Apply the independent licence check to data/prereg/controls_real.json.

Reads the frozen copy results/license-check-controls-real/controls_real.before-license-check.json
(sha256 eb1f0401...9256), applies the edits listed in docs/license-check-controls-real.md,
adds "license_check" to every clue row, re-verifies every licence_words string against the
cited row of the cited local text, and writes data/prereg/controls_real.json.

Does NOT open controls_real_truth.json or docs/research-controls.md.
Licence strings that had to be lengthened are cut out of the local rows by anchors,
so their characters are the file's own (the U+2220 artefact, the two prime signs).
"""
import json, os, hashlib

ROOT = r"C:\Projects\odybench"
SRC = os.path.join(ROOT, "results", "license-check-controls-real", "controls_real.before-license-check.json")
DST = os.path.join(ROOT, "data", "prereg", "controls_real.json")
PTOL = "data/text/ptolemy-syntaxis-grc.tsv"
P_URN = "urn:cts:greekLit:tlg0363.tlg001.1st1K-grc1."

_cache = {}


def rows(tf):
    if tf not in _cache:
        d = {}
        with open(os.path.join(ROOT, tf), encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if "\t" in line:
                    k, v = line.split("\t", 1)
                    d[k] = v
        _cache[tf] = d
    return _cache[tf]


def cut(tf, key, start, end_marker, include_end=False):
    """Substring of row `key` from the first occurrence of `start` up to `end_marker`."""
    t = rows(tf)[key]
    i = t.index(start)
    j = t.index(end_marker, i + len(start))
    if include_end:
        j += len(end_marker)
    return t[i:j]


def clue(d, cid):
    for s in d["sets"]:
        for c in s["clues"]:
            if c["clue_id"] == cid:
                return c
    raise KeyError(cid)


def setobj(d, sid):
    for s in d["sets"]:
        if s["set_id"] == sid:
            return s
    raise KeyError(sid)


def make_primary(c, option):
    names = [fo["option"] for fo in c["fork_options"]]
    assert option in names, (c["clue_id"], option, names)
    for fo in c["fork_options"]:
        fo["primary"] = fo["option"] == option


def fork(c, option):
    for fo in c["fork_options"]:
        if fo["option"] == option:
            return fo
    raise KeyError((c["clue_id"], option))


def main():
    rawb = open(SRC, "rb").read()
    assert hashlib.sha256(rawb).hexdigest().startswith("eb1f0401"), "unexpected source file"
    raw = rawb.decode("utf-8")
    d = json.loads(raw)
    edits = {}

    # ---------------------------------------------------------------- PA-INT
    c = clue(d, "PA-INT")
    k = P_URN + "4.6.16"
    lw1 = cut(PTOL, k, "ἐνιαυτοῦ Αἰγυπτιακοῦ ἑνὸς καὶ ἡμερῶν ρξς", ", τῆς δὲ δευτέρας διαστάσεως")
    lw2 = cut(PTOL, k, "ἐνιαυτοῦ πάλιν Αἰγυπτιακοῦ ἑνὸς καὶ ἡμερῶν ρλζ", ". κινεῖται δὲ πάλιν")
    c["licence_words"] = [lw1, lw2]
    c["ref"] = [k, k]
    c["text_file"] = [PTOL, PTOL]
    edits["PA-INT"] = ("edited: licence_words lengthened to take in the hour figures the statement gives "
                       "(23 1/2 1/4 h apparent, 23 1/2 1/8 h mean; 5 h apparent, 5 1/2 h mean). They were in the row "
                       "but not in the quotation, and the first hour figure is what makes the H1->H2 count 532 nights "
                       "rather than 531. Statement and options unchanged.")

    # --------------------------------------------------------------- PC-LINK
    c = clue(d, "PC-LINK")
    k = P_URN + "4.7.1"
    s1 = cut(PTOL, k, "τοῦ τε δευτέρου ἔτους Μαρδοκεμπάδου", "τοῦ μεσονυκτίου", include_end=True)
    s2 = cut(PTOL, k, "τοῦ ιθʹ ἔτους Ἀδρια", "τοῦ μεσονυκτίου", include_end=True)
    s3 = cut(PTOL, k, "περιέχει Αἰγυπτιακὰ ἔτη ωνδ", ", ἀκριβῶς δὲ καὶ πρὸς τὰ ὁμαλὰ")
    s4 = cut(PTOL, k, "πάσας δὲ ἡμέρας M λα καὶ αψπγ", ", αἷς εὑρίσκομεν")
    c["licence_words"] = [s1, s2, s3, s4]
    c["ref"] = [k] * 4
    c["text_file"] = [PTOL] * 4
    edits["PC-LINK"] = ("edited: licence_words lengthened. The old quotation gave only '854 Egyptian years and 73 days' "
                        "and the day total; the statement's hours and the two before-midnight times (E2 5/6 h, H2 1 h) "
                        "were in the row but not quoted, and the 311,784-night count depends on them "
                        "(73 d 23 1/2 1/3 h plus the 1/6 h difference in time of night). Statement and options unchanged.")

    # ------------------------------------------------------------ PB-E3-MAG
    c = clue(d, "PB-E3-MAG")
    c["statement"] = ("E3: eclipsed from the north by 'more than half' (πλεῖον τοῦ ἡμίσους); not said to be total. "
                      "The words do not say half of what. The options read it as a fraction of the diameter, as Ptolemy's "
                      "own records state it (IV.6.14-15 'τῆς διαμέτρου'); umbral magnitude > 0.5 is the weaker of the "
                      "diameter and area readings.")
    edits["PB-E3-MAG"] = ("edited: statement said 'more than half the diameter'; the record says only 'more than half'. "
                          "Statement reworded; options unchanged, because umag > 0.5 is already the weaker of the "
                          "diameter and area readings.")

    # ---------------------------------------------------------------- T2-ECL
    c = clue(d, "T2-ECL")
    c["statement"] = ("T2: 'some eclipse of the Sun' (ἐκλιπές τι), about the new moon. The magnitude is not stated: "
                      "the primary option reads 'τι' as 'partial', the alternative leaves the magnitude open.")
    edits["T2-ECL"] = ("edited: statement asserted 'partial' as though the text said so; the words give only "
                       "'ἐκλιπές τι'. Reworded so that the upper bound shows as a reading (options 'partial' and 'any', "
                       "both unchanged).")

    # ------------------------------------------------------------- T2-SEASON
    c = clue(d, "T2-SEASON")
    fo = fork(c, "early")
    fo["justification"] = ("'εὐθύς' at the head of the summer, and the summer begins 'ἅμα ἦρι ἀρχομένῳ' (2.2.1). "
                           "The 330 deg start (about a month before the equinox) is the drafter's placement of 'the "
                           "beginning of spring', as in the 'campaign' option; the text gives no longitude. The "
                           "two-month width is also the drafter's.")
    edits["T2-SEASON"] = ("edited: the primary option's justification did not say that its 330 deg start is the "
                          "drafter's placement of 'the beginning of spring' (the 'half-year' option of the same row "
                          "starts at 0 deg); added. Bounds unchanged.")

    # ------------------------------------------- site forks: primary -> none
    site_flips = {
        "T1-SITE": ("box", "the Greek mainland and Aegean, 'where the war was being fought'"),
        "T2-SITE": ("box", "the Greek mainland and Aegean, as T1-SITE"),
        "X1-SITE": ("box", "the Aegean box, 'the theatre of the narrative'"),
        "X2-SITE": ("box", "the Aegean box"),
        "L1-SITE": ("italy-box", "Italy, Sicily and Sardinia, the region of the places the prodigy list names"),
        "L3-SITE": ("rome", "Rome, where the narrative stands (the games, the consul leaving the city)"),
        "L4-SITE": ("rome", "Rome, where the expiation and the companion prodigy are"),
    }
    for cid, (old, what) in site_flips.items():
        c = clue(d, cid)
        assert fork(c, old)["primary"] is True, cid
        make_primary(c, "none")
        nf = fork(c, "none")
        nf["justification"] = ("the text names no place from which this sky event was seen, and the set records the "
                               "observer as 'unstated'; by policy 2 the primary option takes no site from narrative "
                               "context or outside knowledge (licence check, 2026-10-04)")
        of = fork(c, old)
        of["justification"] = of["justification"].rstrip(".") + " (an inference from context; kept as an alternative, no longer primary)"
        edits[cid] = ("edited: primary moved from '%s' (%s) to 'none'. The text does not say where the event was seen; "
                      "the set itself records the observer place as 'unstated', and policy 2 bars inference from "
                      "narrative context or outside knowledge in the primary option. The drafter applied that rule to "
                      "the narrative-order seasons (X2-SEASON, X3-SEASON, L1-, L2-, L4-DATE: primary 'none') but not "
                      "to sites. '%s' and the other site options stay as alternatives." % (old, what, old))

    # ------------------------------------------------------- A-TIME-CURTIUS
    c = clue(d, "A-TIME-CURTIUS")
    c["statement"] = ("Curtius: about the first watch ('prima fere vigilia'), at the camp by the Tigris where the king "
                      "had kept a standing camp ('ibi', 4.10.1). The 'two days' of 4.10.1 are how long the camp stood; "
                      "they are narrative context, date nothing, and are not used.")
    edits["A-TIME-CURTIUS"] = ("edited: statement said 'two days after crossing the Tigris', a day interval the words "
                               "do not give: 4.10.1 says the king kept a standing camp there for two days and ordered "
                               "the march for the next day, and the eclipse sentence follows with 'Sed'. Reworded; the "
                               "operational option never used the interval and is unchanged.")

    # ---------------------------------------------------------------- X1-ECL
    c = clue(d, "X1-ECL")
    t3 = fork(clue(d, "T3-ECL"), "penumbral-deep")
    c["fork_options"].insert(1, {
        "option": "penumbral-deep",
        "reading": "umbral, or penumbral with penumbral magnitude >= 0.7, Moon up at the observer",
        "justification": ("'ἐξέλιπεν' gives no magnitude; the umbral requirement of 'use' is an inference that a "
                          "recorded eclipse was umbral. Same relaxation and threshold as T3-ECL (drafter's rough "
                          "threshold, general knowledge)"),
        "operational": json.loads(json.dumps(t3["operational"])),
        "primary": False,
    })
    edits["X1-ECL"] = ("edited: added the alternative 'penumbral-deep' (as in T3-ECL). 'ἐξέλιπεν ἑσπέρας' states no "
                       "magnitude, so the umbral requirement in the primary 'use' is an inference, and the row had no "
                       "option that relaxed it short of dropping X1. Primary unchanged.")

    # ------------------------------------------- set metadata (not clue rows)
    s = setobj(d, "R-THUC")
    keys = s["texts"][0]["local_keys"]
    for k in ["1.1.1.1", "7.50.1.1", "7.50.3.1"]:
        if k not in keys:
            keys.append(k)

    # ------------------------------------------------- license_check on all
    n = 0
    for s in d["sets"]:
        for c in s["clues"]:
            c["license_check"] = edits.get(c["clue_id"], "ok")
            n += 1
    unused = set(edits) - {c["clue_id"] for s in d["sets"] for c in s["clues"]}
    assert not unused, unused

    # ----------------------------------------------------- re-verify strings
    bad = []
    nstr = 0

    def chk(words, refs, tfs, who):
        nonlocal nstr
        assert len(words) == len(refs) == len(tfs), who
        for w, r, tf in zip(words, refs, tfs):
            nstr += 1
            if w not in rows(tf).get(r, ""):
                bad.append((who, w, r))

    for s in d["sets"]:
        for op in s["observer_place"]:
            chk(op["licence_words"], op["ref"], op["text_file"], s["set_id"] + ":observer")
        for c in s["clues"]:
            chk(c["licence_words"], c["ref"], c["text_file"], c["clue_id"])
            if c["fork_options"]:
                prim = [fo for fo in c["fork_options"] if fo.get("primary")]
                assert len(prim) == 1, c["clue_id"]
    assert not bad, bad

    d["license_check_record"] = {
        "checked": "2026-10-04",
        "by": "independent licence check (did not read controls_real_truth.json or docs/research-controls.md)",
        "report": "docs/license-check-controls-real.md",
        "rows_checked": n,
        "rows_edited": len(edits),
        "frozen_before_check_sha256": hashlib.sha256(rawb).hexdigest(),
        "frozen_copy": "results/license-check-controls-real/controls_real.before-license-check.json",
        "note": ("results/controls-real-drafting/build_controls_real.py does not contain these edits; "
                 "re-running it would undo them."),
    }

    out = json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    with open(DST, "w", encoding="utf-8", newline="\r\n") as f:  # the frozen file uses CRLF
        f.write(out)
    print("rows", n, "edited", len(edits), "strings re-verified", nstr)
    print("new sha256", hashlib.sha256(open(DST, "rb").read()).hexdigest())
    for k, v in edits.items():
        print(k, "|", v[:110])


if __name__ == "__main__":
    main()
