"""Design revision 8 scratch: an executable transcription of the rule of
DESIGN 9.2 (revision 8), run on the synthetic sets of 9.5, with the
constraints C1-C12 of 9.4 checked for every set marked realisable.

Changes from results/design-revision-v7/verdict_trace.py (revision 7), each
answering an issue of the recheck of revision 7 (docs/critique-design-r3.md,
cited [r3v7]):
  * Q_score is split into Q_score3a (gate 3a fires and some leg reaches 4) and
    Q_score3b (gate 3b fires and some leg reaches 6, or its decision changes
    under the other meaning of `same_apparition`) [r3v7 R3-10];
  * Q_attain3a and Q_attain3b are printed only beside a gate that fires:
    `narrowable` is a majority over 21 null windows, while "seen" uses the
    gate's own window, so a set near the 5% line can be narrowed in the one
    and not by majority [r3v7 R3-8];
  * Q_attain4 reads hit_j(m_hat), not E_j: some eclipse-compatible reading has,
    in one of the Odyssey's two fixed windows (the only windows where label 4
    is scored), a unique survivor with h_tot >= m_hat = 0.304, on the masked
    pool. E_j (the same over the whole core) is reported beside it as context.
    Q_attain4 is not printed beside a label 4 [r3v7 R3-2];
  * C4 reads hit_j(m_hat); the integer check of E_j is labelled C5 (revision
    7's trace called it "C14" and said it checked "C1-C14"; 9.4 has C1-C12)
    [r3v7 R3-11];
  * three new sets: S4c (the Q_attain4 guard), S14c (E_j >= 1 without a hit in
    the two windows) and S20 (gates that pass with N_narrow below threshold).
`decide_v7` keeps revision 7's rule, to list which outputs change.
This checks the design text; it is not bench code.
Run: py results/design-revision-v8/verdict_trace.py
"""
import copy
import math
from scipy.stats import beta

SLOTS = ["v0", "v1", "v2", "v3", "v4", "v5"]
POOLS = ["P_BM", "P_MWRA", "P_BM_E", "P_MWRA_E"]       # _E: within +-700 years of -1177
LEGS3A = ["AL_bf", "AL_st", "WO_bf", "WO_st"]
STEPS = ["fine", "mid", "coarse"]                       # rounding family of the ceilings (6.4)
LEGS3B = [f"{sc}_{st}" for sc in ("bf", "st") for st in STEPS]
U0 = 3.69                                               # gamma upper bound with no target reached, x n

# design-stage null side (DESIGN 2.6, 2.9; r2 check_gbm.py, check_slot_scaling.py;
# revision 4 heldout_attain.py; revision 5 heldout_strata.py; revision 6
# heldout_epochs.py; revision 7 heldout_exch.py; r2v6 narrowing_3b.py and
# r3v7 narrowing_inferred_phase.py, as assembled in narrowing_v8.py)
NULL = {
    "G_BM": {"v0": (0.224, 0.139, 0.344, 82), "v1": (0.140, 0.087, 0.215, 131),
             "v2": (0.211, 0.131, 0.324, 87), "v3": (0.278, 0.172, 0.427, 66),
             "v4": (0.182, 0.112, 0.279, 101), "v5": (0.327, 0.203, 0.504, 56)},
    "n_T": 10690, "G_BM_u": 0.00172, "G_BM_u_lo": 0.00107,
    # pool counts: n, members passing H3 only, H4 only, both
    "pools": {"P_BM": dict(n=76, h3=14, h4=1, both=1),
              "P_MWRA": dict(n=43, h3=8, h4=1, both=0),
              "P_BM_E": dict(n=49, h3=9, h4=1, both=1),
              "P_MWRA_E": dict(n=28, h3=6, h4=1, both=0)},
    # the frozen disclosure table (7.1): values on record before the freeze
    "determined": {"H4": False},          # H4 fails at the target, by inference
    # null-side narrowability (6.3.2, 6.4): counted sets that can be narrowed
    "N_narrow_3a": {leg: 5 for leg in LEGS3A},      # R-THUC, R-XEN cannot (6.3.2)
    "N_narrow_3b": {leg: 8 for leg in LEGS3B},      # ALM-I, J, K cannot; A, B, H near the line
    "Q_exch": False,                                 # heldout_exch.py: every Fisher p >= 0.17
}


def cp_lo(k, n):
    return 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)


def p_pool(pool, pattern, member=True):
    """Exact rank p of the target in one pool (7.2). pattern in
    {'both','h4','h3','none'}; weights over pool + target; ties against target."""
    if not member:
        return 1.0
    n, a3, a4, ab = pool["n"], pool["h3"], pool["h4"], pool["both"]
    t3 = pattern in ("both", "h3")
    t4 = pattern in ("both", "h4")
    x3 = a3 + ab + t3
    x4 = a4 + ab + t4
    w3 = -math.log10(x3 / (n + 1)) if x3 else 0.0
    w4 = -math.log10(x4 / (n + 1)) if x4 else 0.0
    s_t = t3 * w3 + t4 * w4
    scores = [w3 + w4] * ab + [w3] * a3 + [w4] * a4 + [0.0] * (n - ab - a3 - a4)
    x = sum(1 for s in scores if s >= s_t - 1e-12)
    return (1 + x) / (1 + n)


def p_min(pool):
    return (1 + pool["both"]) / (1 + pool["n"])


def p_H_of(pools, pattern, member=None):
    member = member or {P: True for P in POOLS}
    pp = {P: p_pool(pools[P], pattern, member[P]) for P in POOLS}
    return pp, max(pp.values())


def q_record(pools, determined):
    """True if no pass pattern consistent with the determined values reaches 0.05."""
    ok = []
    for pat in ("both", "h4", "h3", "none"):
        t = {"H3": pat in ("both", "h3"), "H4": pat in ("both", "h4")}
        if any(t[h] != v for h, v in determined.items()):
            continue
        ok.append(p_H_of(pools, pat)[1] <= 0.05)
    return not any(ok)


def _common(q, L, Q, fire3a):
    """the parts of 9.2 that revision 8 leaves as revision 7 wrote them."""
    if q["rec_ALM_BM"] < 6:
        Q.add("Q_BM")
    if min(q["held_ALM"].values()) < 6:
        Q.add("Q_H")
    for var_ in ("redraft", "sibling"):
        if (min(q["gate3a"][var_].values()) < 4) != fire3a:
            Q.add("Q_exposure")
    if (min(q["gate3a"]["noncirc"].values()) < 4) != fire3a:
        Q.add("Q_dT")
    pmin = max(p_min(q["pools"][P]) for P in POOLS)
    if pmin > 0.05:
        Q.add("Q_attain")
    if q_record(q["pools"], q["determined"]):
        Q.add("Q_record")
    if q["Q_exch"]:
        Q.add("Q_exch")
    t = {"H3": q["pattern"] in ("both", "h3"), "H4": q["pattern"] in ("both", "h4")}
    if any(t[h] != v for h, v in q["determined"].items()):
        Q.add("Q_contra")
    g2 = {v: q["G_BM"][v][1] >= 0.20 for v in SLOTS}
    tol = {v: q["G_BM"][v][1] > 0.05 for v in SLOTS}
    if all(tol.values()):
        Q.add("Q_tol")
    if len(set(g2.values())) > 1 or len(set(tol.values())) > 1:
        Q.add("Q_slot")
    lo = q["G_BM_u_lo"]
    if any(h and gh <= lo for (h, g, gh, e, hh) in q["negatives"]):
        L.add("4")
    if q["r_Ody"] == 0:
        L.add("2 (no match)")
    else:
        xg, xe, n = q["pct"]
        if all(g2.values()) or cp_lo(xg, n) >= 0.50:
            L.add("2 (ordinary)")
    pp, p_H = p_H_of(q["pools"], q["pattern"], q["member"])
    if q["T0_pass"] and p_H <= 0.05:
        L.add("1")
    return pp, p_H, pmin


def decide(q, guard=True):
    """DESIGN 9.2, revision 8. guard=False drops the clause that keeps Q_attain4 from
    printing beside a label 4 (for the comparison in main only)."""
    if not q["INSTR"]:
        return "BLOCKED", set(), None
    L, Q = set(), set()
    a = q["gate3a"]["main"]
    fire3a = min(a.values()) < 4
    if fire3a:
        L.add("3a")
    if fire3a and max(a.values()) >= 4:
        Q.add("Q_score3a")
    b = q["gate3b"]
    fire3b = min(b.values()) < 6
    if fire3b:
        L.add("3b")
    fire3b_other = min(q["gate3b_side"].values()) < 6
    if (fire3b and max(b.values()) >= 6) or (fire3b_other != fire3b):
        Q.add("Q_score3b")
    # could the gates have passed? printed only beside a gate that fired [r3v7 R3-8]
    if fire3a and min(q["N_narrow_3a"].values()) < 4:
        Q.add("Q_attain3a")
    if fire3b and min(q["N_narrow_3b"].values()) < 6:
        Q.add("Q_attain3b")
    pp, p_H, pmin = _common(q, L, Q, fire3a)
    # could outcome 4 have fired? the G condition and a hit at m_hat in the Odyssey's
    # two windows (null side); not printed beside a label 4 [r3v7 R3-2]
    lo = q["G_BM_u_lo"]
    if (not guard or "4" not in L) and \
            not any(0 < g and gh <= lo and hh for (h, g, gh, e, hh) in q["negatives"]):
        Q.add("Q_attain4")
    if not L:
        L = {"inconclusive"}
    return L, Q, (pp, p_H, pmin)


def decide_v7(q):
    """DESIGN 9.2 as revision 7 wrote it (one Q_score; Q_attain3a/3b whatever the gate;
    Q_attain4 on E_j over the core), for comparison only."""
    if not q["INSTR"]:
        return "BLOCKED", set(), None
    L, Q = set(), set()
    a = q["gate3a"]["main"]
    fire3a = min(a.values()) < 4
    if fire3a:
        L.add("3a")
    b = q["gate3b"]
    fire3b = min(b.values()) < 6
    if fire3b:
        L.add("3b")
    fire3b_alt = min(q["gate3b_side"].values()) < 6
    if (fire3a and max(a.values()) >= 4) or (fire3b and max(b.values()) >= 6) or (fire3b_alt != fire3b):
        Q.add("Q_score")
    if min(q["N_narrow_3a"].values()) < 4:
        Q.add("Q_attain3a")
    if min(q["N_narrow_3b"].values()) < 6:
        Q.add("Q_attain3b")
    pp, p_H, pmin = _common(q, L, Q, fire3a)
    lo = q["G_BM_u_lo"]
    if not any(0 < g and gh <= lo and e >= 1 for (h, g, gh, e, hh) in q["negatives"]):
        Q.add("Q_attain4")
    if not L:
        L = {"inconclusive"}
    return L, Q, (pp, p_H, pmin)


NULL_KEYS = ("G_BM", "n_T", "G_BM_u", "G_BM_u_lo", "pools", "determined",
             "N_narrow_3a", "N_narrow_3b", "Q_exch")


def check(q):
    """C1-C12 of DESIGN 9.4 for a set; returns the violated constraints."""
    bad = []
    for v, (g, lo, hi, n) in q["G_BM"].items():
        if not (0 <= lo <= g <= hi <= 1) or hi < U0 / n:
            bad.append(f"C1 {v}")
        if v != "v0" and abs(n * g / q["n_T"] - q["G_BM_u"]) > 2e-5:
            bad.append(f"C2 {v}")
    if not (0 <= q["G_BM_u_lo"] <= q["G_BM_u"]):
        bad.append("C1 G_BM_u")
    if q["r_Ody"] > 0:
        xg, xe, n = q["pct"]
        if n < 200 or xg + xe > n:
            bad.append("C3")
    for (h, g, gh, e, hh) in q["negatives"]:
        if not (0 <= g <= gh) or gh < U0 / q["n_T"]:
            bad.append("C1 G_j")
        # C4: a hit is a unique survivor in the core, so its reach is > 0; a hit at m_hat
        # lies in one of the two windows, inside the core, so E_j >= 1. A hit at M_Ody
        # without a hit at m_hat is allowed: the negative's only hit can be 16 Apr -1177,
        # which the null-side mask hides (6.5)
        if h and g <= 0:
            bad.append("C4 hit_j")
        if hh and (g <= 0 or e < 1):
            bad.append("C4 hit_j(m_hat)")
        if e < 0 or int(e) != e:
            bad.append("C5 E_j")
    for var_, legs in q["gate3a"].items():
        if any(not 0 <= x <= 7 for x in legs.values()):
            bad.append("C5 3a")
        if legs["AL_st"] > legs["AL_bf"] or legs["WO_st"] > legs["WO_bf"]:
            bad.append("C10 3a")
    for name in ("gate3b", "gate3b_side"):
        g = q[name]
        if any(not 0 <= x <= 11 for x in g.values()):
            bad.append("C5 3b")
        if any(g[f"st_{s}"] > g[f"bf_{s}"] for s in STEPS):
            bad.append("C10 3b")
    if not 0 <= q["rec_ALM_BM"] <= 11:
        bad.append("C5 rec_ALM_BM")
    if any(not 0 <= x <= 8 for x in q["held_ALM"].values()):
        bad.append("C5 held_ALM")
    if any(not 0 <= x <= 7 for x in q["N_narrow_3a"].values()) or \
            any(not 0 <= x <= 11 for x in q["N_narrow_3b"].values()):
        bad.append("C12")
    for k in NULL_KEYS:
        if q[k] != NULL[k]:
            bad.append(f"C7 {k}")
    if q["pattern"] not in ("both", "h4", "h3", "none"):
        bad.append("C8")
    if q["T0"] in ("R", "RE") and not q["T0_pass"]:
        bad.append("C9")
    return bad


def legs(al_bf, al_st, wo_bf, wo_st):
    return {"AL_bf": al_bf, "AL_st": al_st, "WO_bf": wo_bf, "WO_st": wo_st}


def gate3a(al_bf, al_st, wo_bf, wo_st, **variants):
    g = {k: legs(al_bf, al_st, wo_bf, wo_st) for k in ("main", "redraft", "sibling", "noncirc")}
    for k, v in variants.items():
        g[k] = legs(*v)
    return g


def gate3b(bf, st=None):
    st = bf if st is None else st
    return {**{f"bf_{s}": bf for s in STEPS}, **{f"st_{s}": st for s in STEPS}}


def held(fine, mid=None, coarse=None):
    return {"fine": fine, "mid": fine if mid is None else mid, "coarse": fine if coarse is None else coarse}


# a negative: (hit_j, G_j, G_j_hi, E_j, hit_j(m_hat)); placeholders until the null side (C7)
NEG0 = [(False, 0.0004, 0.0009, 2, True)] * 12
S0 = dict(INSTR=True, T0_pass=True, T0="RE", pattern="h3",
          member={P: True for P in POOLS}, r_Ody=0.0815, pct=(30, 10, 200),
          gate3a=gate3a(5, 5, 5, 5), gate3b=gate3b(7), gate3b_side=gate3b(7),
          rec_ALM_BM=3, held_ALM=held(7), negatives=NEG0,
          **copy.deepcopy(NULL))


def var(base=S0, **kw):
    q = copy.deepcopy(base)
    for k, v in kw.items():
        if k == "pool_override":
            for P, d in v.items():
                q["pools"][P].update(d)
        else:
            q[k] = v
    return q


NEG4 = [(True, 0.0004, 0.0009, 2, True)] + [(False, 0.0004, 0.0009, 2, True)] * 11
NEG4b = [(True, 0.0005, 0.0012, 2, True)] + [(False, 0.0004, 0.0009, 2, True)] * 11
NEG4c = [(True, 0.0004, 0.0009, 2, False)] + [(False, 0.0004, 0.0009, 2, False)] * 11
NEG_NO4 = [(False, 0.0030, 0.0045, 2, True)] * 12
NEG_NOECL = [(False, 0.0004, 0.0009, 0, False)] * 12
NEG_ELSEWHERE = [(False, 0.0004, 0.0009, 2, False)] * 12
S1 = var(pattern="both")
SETS = {
    # name: (set, mark)  mark: "realisable", "branch", or "pending" (depends on G_j, hit_j(m_hat), E_j; 9.5)
    "S0": (S0, "realisable"),
    "S0x": (var(gate3a=gate3a(4, 2, 3, 3), gate3b=gate3b(6), gate3b_side=gate3b(5)), "realisable"),
    "S0y": (var(gate3a=gate3a(4, 2, 3, 3), gate3b=gate3b(5), gate3b_side=gate3b(5)), "realisable"),
    "S1": (S1, "realisable"),
    "S1b": (var(pattern="h4"), "realisable"),
    "S2": (var(pct=(118, 12, 200)), "realisable"),
    "S2nm": (var(r_Ody=0.0, pct=None), "realisable"),
    "S3a": (var(gate3a=gate3a(2, 2, 2, 2)), "realisable"),
    "S3b": (var(gate3b=gate3b(3), gate3b_side=gate3b(3)), "realisable"),
    "S4": (var(negatives=NEG4), "pending"),
    "S4b": (var(negatives=NEG4b), "pending"),
    "S4c": (var(negatives=NEG4c), "pending"),
    "S5": (var(pattern="both", pool_override={"P_BM": dict(both=4, h3=11)}), "branch"),
    "S6": (var(S1, pct=(118, 12, 200)), "realisable"),
    "S6b": (var(pct=(118, 12, 200), gate3a=gate3a(4, 2, 3, 2, redraft=(4, 4, 4, 4), noncirc=(5, 4, 4, 4)),
                gate3b=gate3b(3), gate3b_side=gate3b(3), held_ALM=held(4), negatives=NEG4), "pending"),
    "S7": (var(INSTR=False), "realisable"),
    "S8": (var(S1, T0_pass=False, T0="NR"), "realisable"),
    "S9": (var(S1, gate3a=gate3a(3, 3, 3, 3)), "realisable"),
    "S10": (var(G_BM={v: (0.327, 0.203, 0.504, 56) for v in SLOTS}), "branch"),
    "S11": (var(S1, rec_ALM_BM=7, held_ALM=held(4)), "realisable"),
    "S12": (var(S1, member={"P_BM": True, "P_MWRA": False, "P_BM_E": True, "P_MWRA_E": False}),
            "realisable"),
    "S13": (var(S1, pool_override={"P_MWRA_E": dict(both=2, h3=4)}), "branch"),
    "S14": (var(negatives=NEG_NO4), "pending"),
    "S14b": (var(negatives=NEG_NOECL), "pending"),
    "S14c": (var(negatives=NEG_ELSEWHERE), "pending"),
    "S15": (var(S1, gate3b=gate3b(3), gate3b_side=gate3b(3), negatives=NEG4), "pending"),
    "S16": (var(gate3a=gate3a(2, 2, 2, 2), N_narrow_3a={leg: 3 for leg in LEGS3A}), "branch"),
    "S17": (var(gate3b=gate3b(4), gate3b_side=gate3b(4), N_narrow_3b={leg: 5 for leg in LEGS3B}), "branch"),
    "S18": (var(S1, Q_exch=True), "branch"),
    "S19": (var(held_ALM=held(5, 7, 7)), "realisable"),
    "S20": (var(gate3a=gate3a(4, 4, 4, 4), gate3b=gate3b(6), gate3b_side=gate3b(6),
                N_narrow_3a={leg: 3 for leg in LEGS3A}, N_narrow_3b={leg: 5 for leg in LEGS3B}), "branch"),
}


def tag_of(mark, bad):
    if mark == "realisable":
        return "realisable" if not bad else "SHOULD BE REALISABLE but violates " + ", ".join(sorted(set(bad)))
    if mark == "pending":
        return ("pending (G_j, hit_j(m_hat), E_j)" if not bad else
                "pending; violates " + ", ".join(sorted(set(bad))))
    return ("branch test: " + ", ".join(sorted(set(bad)))) if bad else \
        "MARKED BRANCH TEST but satisfies every constraint"


def main():
    changed = []
    for name, (q, mark) in SETS.items():
        L, Q, extra = decide(q)
        bad = check(q)
        if extra:
            pp, p_H, pmin = extra
            ptxt = " ".join(f"{P} {pp[P]:.4f}" for P in POOLS) + f" -> p_H {p_H:.4f} (p_H,min {pmin:.4f})"
        else:
            ptxt = "-"
        print(f"{name:5s} {ptxt}\n      labels {sorted(L) if isinstance(L, set) else L}  "
              f"qualifiers {sorted(Q)}  [{tag_of(mark, bad)}]")
        L7, Q7, _ = decide_v7(q)
        Q8n = {"Q_score" if x in ("Q_score3a", "Q_score3b") else x for x in Q}
        if L7 != L or Q7 != Q8n:
            changed.append(f"{name}: revision 7's rule gives labels {sorted(L7) if isinstance(L7, set) else L7} "
                           f"qualifiers {sorted(Q7)}")

    print("\nSets whose output differs under revision 7's rule (Q_score3a/3b counted as Q_score):")
    print("\n".join("  " + c for c in changed) if changed else "  none")
    print("Sets in which the Q_attain4 guard (no Q_attain4 beside a label 4) changes the output:")
    g = [n for n, (q, _) in SETS.items() if decide(q) != decide(q, guard=False)]
    print("  " + (", ".join(g) if g else "none"))
    print()
    print("Lattice at the design-stage counts (target pattern -> p per pool -> p_H):")
    for pat in ("both", "h4", "h3", "none"):
        pp, ph = p_H_of(NULL["pools"], pat)
        print(f"  {pat:5s} " + " / ".join(f"{pp[P]:.4f}" for P in POOLS) + f" -> {ph:.4f}")
    print("p_H,min =", round(max(p_min(NULL['pools'][P]) for P in POOLS), 4))
    print("Q_record on the design-stage null side and the disclosure table:",
          q_record(NULL["pools"], NULL["determined"]))
    print("G_BM,u and its bounds (design stage, v1 scaled by n_A/n_T):",
          round(131 / 10690 * 0.140, 5), round(131 / 10690 * 0.087, 5), round(131 / 10690 * 0.215, 5))
    print(f"{len(SETS)} synthetic sets")


if __name__ == "__main__":
    main()
