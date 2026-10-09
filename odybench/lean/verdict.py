"""
odybench.lean.verdict -- the decision rule of the lean run (LEAN.md, "The rule,
restricted"; DESIGN 9.2 with the deferred inputs marked "not tested").

decide(q, thresholds) -> (labels, qualifiers, notes) is a pure function.

The restriction, as LEAN.md states it:
* 3a and 4 are not evaluated; the verdict prints "not tested" for each.
* 3b fires if seen_ALM_SL < 6 on some leg (min over the six legs of 6.4), when
  gate 3b runs.  If it did not run, 3b is printed "not run".
* Label 2 holds as "no match" if r_Ody = 0, and as "ordinary" if
  G_BM,lo(v) >= 0.20 for every slot variant v0..v5.  The pct_N4 leg is not
  tested.
* Label 1 holds if T0_pass and p_H <= 0.05, printed "provisional: 3a and 4
  not tested".  As in DESIGN 9.2, no gate vetoes it (LEAN.md as corrected on
  2026-10-09; its first text added "and not 3b").
* Qualifiers: Q_attain, Q_record, Q_contra, Q_exch, Q_tol, Q_slot and Q_BM,
  as 7.2, 9.2 and 6.4 define them.  9.2's other qualifiers (Q_score3a,
  Q_score3b, Q_attain3a, Q_attain3b, Q_H, Q_exposure, Q_dT, Q_attain4) are
  outside the lean rule and are listed as not evaluated.
* Otherwise the verdict is inconclusive.
* As in 9.2, no verdict is read unless INSTR holds (BLOCKED).

q (a flat dict; a missing or None input leaves its leg "not evaluated"):
  INSTR: bool                     the instrument checks the lean run keeps
  T0_pass: bool; T0: 'R' | 'RE' | 'NR' (reported)
  r_Ody: float
  G_BM_lo: {v0..v5: float}        G_BM,lo(v) (5.3); G_BM: {v: (G, lo, hi)} is
                                  accepted instead
  p_H_min: float; Q_record: bool; Q_exch: bool            (null side, 7.2)
  p_H: float; Q_contra: bool                              (target side, 7.2)
  gate3b_run: bool; seen_ALM_SL: {leg: int} (six legs); rec_ALM_BM: int   (6.4)
thresholds: data/prereg/verdict_rule.json's "thresholds" (unchanged).
"""
from __future__ import annotations

SLOTS = ("v0", "v1", "v2", "v3", "v4", "v5")
LEGS3B = ("bf_fine", "bf_mid", "bf_coarse", "st_fine", "st_mid", "st_coarse")
LEAN_QUALIFIERS = ("Q_contra", "Q_exch", "Q_attain", "Q_record", "Q_tol", "Q_slot", "Q_BM")
OUTSIDE_LEAN = ("Q_score3a", "Q_score3b", "Q_attain3a", "Q_attain3b", "Q_H", "Q_exposure", "Q_dT", "Q_attain4")
LABEL_ORDER = ("BLOCKED", "1", "3b", "2 (no match)", "2 (ordinary)", "inconclusive")
QUAL_ORDER = ("Q_contra", "Q_exch", "Q_BM", "Q_tol", "Q_slot", "Q_attain", "Q_record")
PROVISIONAL = "provisional: 3a and 4 not tested"


def _thr(thresholds):
    t = thresholds
    return dict(
        p_H_max=float(t["label_1"]["p_H_max"]),
        g2=float(t["label_2"]["g2_G_BM_lo_at_least"]),
        no_match=float(t["label_2"]["no_match_if_r_Ody"]),
        tol=float(t["q_tol"]["G_BM_lo_above"]),
        attain=float(t["q_attain"]["p_H_min_above"]),
        fire3b=int(t["gate_3b"]["fires_if_min_below"]),
        q_bm=int(t["q_bm"]["rec_ALM_BM_below"]),
    )


def g_bm_lo(q):
    """{v: G_BM,lo(v)} from q['G_BM_lo'] or q['G_BM'] ({v: (G, lo, hi)} or
    {v: {'lo': ...}}); None when any slot variant is missing."""
    if q.get("G_BM_lo") is not None:
        d = q["G_BM_lo"]
    elif q.get("G_BM") is not None:
        d = {}
        for v, x in q["G_BM"].items():
            d[v] = x["lo"] if isinstance(x, dict) else x[1]
    else:
        return None
    if any(d.get(v) is None for v in SLOTS):
        return None
    return {v: float(d[v]) for v in SLOTS}


def seen_legs(q):
    s = q.get("seen_ALM_SL")
    if s is None:
        return None
    if isinstance(s, dict):
        vals = list(s.values())
    else:
        vals = list(s)
    if len(vals) != len(LEGS3B) or any(v is None for v in vals):
        return None
    return [int(v) for v in vals]


def decide(q, thresholds):
    """The lean rule.  Returns (labels, qualifiers, notes): labels and
    qualifiers as lists in the headline order of 9.3, notes as strings
    (what was not tested or not evaluated, and why a label holds)."""
    th = _thr(thresholds)
    notes = []
    if q.get("INSTR") is not True:
        notes.append("BLOCKED: the instrument checks do not all pass" if q.get("INSTR") is False
                     else "BLOCKED: no instrument record (INSTR) was supplied; no verdict is read")
        return ["BLOCKED"], [], notes
    labels, quals = set(), set()

    notes.append("3a: not tested (PC-R and gate 3a deferred, LEAN.md)")
    notes.append("4: not tested (the negatives deferred, LEAN.md)")
    notes.append("label 2's pct_N4 leg: not tested (N4 deferred, LEAN.md)")
    notes.append("not evaluated in the lean rule: " + ", ".join(OUTSIDE_LEAN))

    # gate 3b (6.4): six legs, the decision taken against "the method can see"
    legs = seen_legs(q)
    fire3b = False
    if q.get("gate3b_run") is False or legs is None:
        notes.append("3b: not run (gate 3b was not built in this run)" if q.get("gate3b_run") is False
                     else "3b: not run (no seen_ALM_SL on all six legs)")
        ran3b = False
    else:
        ran3b = True
        fire3b = min(legs) < th["fire3b"]
        if fire3b:
            labels.add("3b")
    if q.get("rec_ALM_BM") is not None:
        if int(q["rec_ALM_BM"]) < th["q_bm"]:
            quals.add("Q_BM")
    else:
        notes.append("Q_BM: not evaluated (no rec_ALM_BM)")

    # null-side qualifiers (7.2)
    if q.get("p_H_min") is not None:
        if float(q["p_H_min"]) > th["attain"]:
            quals.add("Q_attain")
    else:
        notes.append("Q_attain: not evaluated (no p_H,min)")
    for k in ("Q_record", "Q_exch"):
        if q.get(k) is None:
            notes.append(f"{k}: not evaluated (not supplied)")
        elif q[k]:
            quals.add(k)
    g = g_bm_lo(q)
    if g is not None:
        g2 = {v: g[v] >= th["g2"] for v in SLOTS}
        tol = {v: g[v] > th["tol"] for v in SLOTS}
        if all(tol.values()):
            quals.add("Q_tol")
        if len(set(g2.values())) > 1 or len(set(tol.values())) > 1:
            quals.add("Q_slot")
    else:
        g2 = None
        notes.append("Q_tol, Q_slot and label 2's G leg: not evaluated (G_BM,lo missing for some slot variant)")

    # target-side qualifier (7.1)
    if q.get("Q_contra") is None:
        notes.append("Q_contra: not evaluated (not supplied)")
    elif q["Q_contra"]:
        quals.add("Q_contra")

    # 2: B&M's match carries no weight
    r = q.get("r_Ody")
    if r is not None and float(r) == th["no_match"]:
        labels.add("2 (no match)")
    elif g2 is not None and all(g2.values()):
        labels.add("2 (ordinary)")
    if r is None:
        notes.append("label 2's no-match leg: not evaluated (no r_Ody)")

    # 1: T0_pass and p_H <= 0.05; as in DESIGN 9.2, no gate vetoes it (LEAN.md, corrected 2026-10-09)
    if q.get("T0_pass") is None or q.get("p_H") is None:
        notes.append("label 1: not evaluated (T0_pass or p_H missing)")
    elif q["T0_pass"] and float(q["p_H"]) <= th["p_H_max"]:
        labels.add("1")
        notes.append("label 1 " + PROVISIONAL + ("" if ran3b else "; 3b not run"))

    if not labels:
        labels.add("inconclusive")
    return ([x for x in LABEL_ORDER if x in labels], [x for x in QUAL_ORDER if x in quals], notes)


def numbers(q, thresholds):
    """Every rule number beside its threshold: rows (quantity, value,
    condition, holds) for the report.  holds is None when not evaluated."""
    th = _thr(thresholds)
    rows = []

    def row(name, val, cond, holds):
        rows.append((name, val, cond, holds))
    row("INSTR", q.get("INSTR"), "all kept instrument checks pass", q.get("INSTR"))
    row("T0_pass", q.get("T0_pass"), "label 1 needs true", q.get("T0_pass"))
    if q.get("T0") is not None:
        row("T0 (reported)", q.get("T0"), "R / RE / NR", "reported")
    ph = q.get("p_H")
    row("p_H", ph, f"label 1 needs <= {th['p_H_max']}", None if ph is None else float(ph) <= th["p_H_max"])
    pm = q.get("p_H_min")
    row("p_H,min", pm, f"Q_attain if > {th['attain']}", None if pm is None else float(pm) > th["attain"])
    for k in ("Q_record", "Q_exch", "Q_contra"):
        row(k, q.get(k), "printed if true", q.get(k))
    r = q.get("r_Ody")
    row("r_Ody", r, f"label 2 (no match) if == {th['no_match']}", None if r is None else float(r) == th["no_match"])
    g = g_bm_lo(q)
    for v in SLOTS:
        val = None if g is None else g[v]
        row(f"G_BM,lo({v})", val, f"label 2 (ordinary) needs >= {th['g2']} for every v; Q_tol needs > {th['tol']} "
            f"for every v", None if val is None else (val >= th["g2"], val > th["tol"]))
    legs = seen_legs(q)
    row("seen_ALM_SL (six legs)", legs, f"3b fires if min < {th['fire3b']}",
        None if legs is None else min(legs) < th["fire3b"])
    rb = q.get("rec_ALM_BM")
    row("rec_ALM_BM", rb, f"Q_BM if < {th['q_bm']}", None if rb is None else int(rb) < th["q_bm"])
    return rows


def headline(labels, qualifiers):
    """The headline order of DESIGN 9.3, restricted to the lean labels."""
    out = []
    if "BLOCKED" in labels:
        return ["BLOCKED: no verdict is read"]
    if "Q_contra" in qualifiers:
        out.append("Q_contra: a measured flag of the target contradicts the disclosure table; the record, the "
                   "inference or the bench is wrong")
    if "1" in labels:
        s = "Label 1 (" + PROVISIONAL + "): the clues nobody fitted date the return, by an exact test"
        if "Q_exch" in qualifiers:
            s += "; Q_exch: the exchangeability of the pools with the target is in doubt"
        out.append(s)
    if "3b" in labels:
        out.append("Label 3b: the B&M-type component is not shown to recover real records (the Almagest control)")
    if "2 (no match)" in labels:
        out.append("Label 2 (no match): B&M's match does not reach the Odyssey (r_Ody = 0)")
    if "2 (ordinary)" in labels:
        out.append("Label 2 (ordinary): B&M's match carries no weight (G_BM,lo >= 0.20 under every slot variant)")
    if "1" in labels and any(x.startswith("2") for x in labels):
        out.append("The clues nobody fitted date the return, and B&M's own match is not what shows it")
    if labels == ["inconclusive"]:
        out.append("Inconclusive: no label of the lean rule holds")
    for k, text in (("Q_attain", "Q_attain: the held-out test could not have said yes for any target "
                                  "(p_H,min > 0.05)"),
                    ("Q_record", "Q_record: the held-out test could not have said yes for this target, given "
                                 "the facts on record (H4 settled to fail)"),
                    ("Q_exch", None if "1" in labels else "Q_exch: the exchangeability that label 1's test "
                                                          "rests on is in doubt"),
                    ("Q_BM", "Q_BM: at B&M's own tolerances, fewer than 6 of 11 Almagest record sets are "
                             "recovered"),
                    ("Q_tol", "Q_tol: under every slot variant G_BM,lo > 0.05, so B&M's tolerances cannot make "
                              "the match notable"),
                    ("Q_slot", "Q_slot: the verdict on G depends on the slot variant")):
        if k in qualifiers and text:
            out.append(text)
    return out
