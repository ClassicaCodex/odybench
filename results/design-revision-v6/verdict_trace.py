"""Design revision 6 scratch: an executable transcription of the rule of
DESIGN 9.2 (revision 6), run on the synthetic sets of 9.5, with the
constraints C1-C11 of 9.4 checked for every set marked realisable.

Changes from results/design-revision-v5/verdict_trace.py (revision 5):
  * gate 3a is scored on a frozen family of four legs (6.3.2):
      AL_bf, AL_st  the as-licensed primaries, best-fit and strict;
      WO_bf, WO_st  the words-only projection, best-fit and strict;
    3a fires if any leg is below 4 (the bound against "the method can see").
    Q_exposure and Q_dT compare the same combined decision (recheck N1);
  * gate 3b is scored on two legs, best-fit and strict, on the regime-SL
    projection; 3b fires if either is below 6;
  * Q_score: within gate 3a's or 3b's family, the legs fall on both sides of
    the threshold (the decision rests on the scoring choice); it replaces
    revision 5's Q_strict;
  * label 1 is no longer vetoed by 3a, 3b or 4: it rests on an exact test,
    whose validity needs no power calibration (recheck N1 fix 5);
  * the held-out test reads four pools: P_BM, P_MWRA and their members within
    +-700 years of the target (epoch-matched; recheck N11, revision 6's
    heldout_epochs.py); p_H is the largest of the four exact p-values;
  * Q_record (null side + the frozen disclosure table, 7.1): no pass pattern
    consistent with the values the table records as determined reaches
    p_H <= 0.05. Q_contra (target side): a measured held-out flag
    contradicts a value the table records as determined (recheck N2);
  * Q_attain4 (null side): no clean negative has 0 < G_j and
    G_j,hi <= G_BM,u, so outcome 4 could not have fired (recheck N5).
    G_j has no design-stage estimate: sets that depend on it are marked
    "pending" (C7);
  * C5 caps the 3a legs at 7 and the 3b legs at 11; C10 (strict leg <=
    best-fit leg within a projection) and C11 (Q_record is not free) are new.
This checks the design text; it is not bench code.
Run: py results/design-revision-v6/verdict_trace.py
"""
import copy
import math
from scipy.stats import beta

SLOTS = ["v0", "v1", "v2", "v3", "v4", "v5"]
POOLS = ["P_BM", "P_MWRA", "P_BM_E", "P_MWRA_E"]       # _E: within +-700 years of -1177
LEGS3A = ["AL_bf", "AL_st", "WO_bf", "WO_st"]
LEGS3B = ["bf", "st"]

# design-stage null side (DESIGN 2.9; r2 check_gbm.py, check_slot_scaling.py;
# revision 4 heldout_attain.py; revision 5 heldout_strata.py; revision 6 heldout_epochs.py)
NULL = {
    "G_BM": {"v0": (0.224, 0.139, 0.344, 82), "v1": (0.140, 0.087, 0.215, 131),
             "v2": (0.211, 0.131, 0.324, 87), "v3": (0.278, 0.172, 0.427, 66),
             "v4": (0.182, 0.112, 0.279, 101), "v5": (0.327, 0.203, 0.504, 56)},
    "n_T": 10690, "G_BM_u": 0.00172,
    # pool counts: n, members passing H3 only, H4 only, both
    "pools": {"P_BM": dict(n=76, h3=14, h4=1, both=1),
              "P_MWRA": dict(n=43, h3=8, h4=1, both=0),
              "P_BM_E": dict(n=49, h3=9, h4=1, both=1),
              "P_MWRA_E": dict(n=28, h3=6, h4=1, both=0)},
    # the frozen disclosure table (7.1): values on record before the freeze
    "determined": {"H4": False},          # H4 fails at the target, by inference
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


def decide(q):
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
    if (fire3a and max(a.values()) >= 4) or (fire3b and max(b.values()) >= 6):
        Q.add("Q_score")
    if q["rec_ALM_BM"] < 6:
        Q.add("Q_BM")
    if q["held_ALM"] < 6:
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
    t = {"H3": q["pattern"] in ("both", "h3"), "H4": q["pattern"] in ("both", "h4")}
    if any(t[h] != v for h, v in q["determined"].items()):
        Q.add("Q_contra")
    g2 = {v: q["G_BM"][v][1] >= 0.20 for v in SLOTS}
    tol = {v: q["G_BM"][v][1] > 0.05 for v in SLOTS}
    if all(tol.values()):
        Q.add("Q_tol")
    if len(set(g2.values())) > 1 or len(set(tol.values())) > 1:
        Q.add("Q_slot")
    if not any(0 < g and gh <= q["G_BM_u"] for (_, g, gh) in q["negatives"]):
        Q.add("Q_attain4")
    if any(h and gh <= q["G_BM_u"] for (h, g, gh) in q["negatives"]):
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
    if not L:
        L = {"inconclusive"}
    return L, Q, (pp, p_H, pmin)


def check(q):
    """C1-C11 for a set marked realisable; returns the violated constraints."""
    bad = []
    for v, (g, lo, hi, n) in q["G_BM"].items():
        if not (0 <= lo <= g <= hi <= 1) or hi < 3.69 / n:
            bad.append(f"C1 {v}")
        if v != "v0" and abs(n * g / q["n_T"] - q["G_BM_u"]) > 2e-5:
            bad.append(f"C2 {v}")
    if q["r_Ody"] > 0:
        xg, xe, n = q["pct"]
        if n < 200 or xg + xe > n:
            bad.append("C3")
    for (h, g, gh) in q["negatives"]:
        if h and (g <= 0 or gh < 3.69 / q["n_T"]):
            bad.append("C4")
        if not (0 <= g <= gh):
            bad.append("C1 G_j")
    for var_, legs in q["gate3a"].items():
        if any(not 0 <= x <= 7 for x in legs.values()):
            bad.append("C5 3a")
        if legs["AL_st"] > legs["AL_bf"] or legs["WO_st"] > legs["WO_bf"]:
            bad.append("C10 3a")
    if any(not 0 <= x <= 11 for x in q["gate3b"].values()) or not 0 <= q["rec_ALM_BM"] <= 11:
        bad.append("C5 3b")
    if q["gate3b"]["st"] > q["gate3b"]["bf"]:
        bad.append("C10 3b")
    if not 0 <= q["held_ALM"] <= 8:
        bad.append("C5 held_ALM")
    for k in ("G_BM", "n_T", "G_BM_u", "pools", "determined"):
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


NEG0 = [(False, 0.0006, 0.0012)] * 12
S0 = dict(INSTR=True, T0_pass=True, T0="RE", pattern="h3",
          member={P: True for P in POOLS}, r_Ody=0.0815, pct=(30, 10, 200),
          gate3a=gate3a(5, 5, 5, 5), gate3b={"bf": 7, "st": 7},
          rec_ALM_BM=3, held_ALM=7, negatives=NEG0,
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


NEG4 = [(True, 0.00051, 0.00112)] + [(False, 0.0006, 0.0012)] * 11
NEG_NO4 = [(False, 0.0030, 0.0045)] * 12
S1 = var(pattern="both")
SETS = {
    # name: (set, mark)  mark: "realisable", "branch", or "pending" (depends on G_j, 9.5)
    "S0": (S0, "realisable"),
    "S0x": (var(gate3a=gate3a(4, 2, 3, 3)), "realisable"),
    "S1": (S1, "realisable"),
    "S1b": (var(pattern="h4"), "realisable"),
    "S2": (var(pct=(118, 12, 200)), "realisable"),
    "S2nm": (var(r_Ody=0.0, pct=None), "realisable"),
    "S3a": (var(gate3a=gate3a(2, 2, 2, 2)), "realisable"),
    "S3b": (var(gate3b={"bf": 3, "st": 3}), "realisable"),
    "S4": (var(negatives=NEG4), "pending"),
    "S5": (var(pattern="both", pool_override={"P_BM": dict(both=4, h3=11)}), "branch"),
    "S6": (var(S1, pct=(118, 12, 200)), "realisable"),
    "S6b": (var(pct=(118, 12, 200), gate3a=gate3a(4, 2, 3, 2, redraft=(4, 4, 4, 4), noncirc=(5, 4, 4, 4)),
                gate3b={"bf": 3, "st": 3}, held_ALM=4, negatives=NEG4), "pending"),
    "S7": (var(INSTR=False), "realisable"),
    "S8": (var(S1, T0_pass=False, T0="NR"), "realisable"),
    "S9": (var(S1, gate3a=gate3a(3, 3, 3, 3)), "realisable"),
    "S10": (var(G_BM={v: (0.327, 0.203, 0.504, 56) for v in SLOTS}), "branch"),
    "S11": (var(S1, rec_ALM_BM=7, held_ALM=4), "realisable"),
    "S12": (var(S1, member={"P_BM": True, "P_MWRA": False, "P_BM_E": True, "P_MWRA_E": False}),
            "realisable"),
    "S13": (var(S1, pool_override={"P_MWRA_E": dict(both=2, h3=4)}), "branch"),
    "S14": (var(negatives=NEG_NO4), "pending"),
    "S15": (var(S1, gate3b={"bf": 3, "st": 3}, negatives=NEG4), "pending"),
}
for name, (q, mark) in SETS.items():
    L, Q, extra = decide(q)
    bad = check(q)
    if mark == "realisable":
        tag = "realisable" if not bad else "SHOULD BE REALISABLE but violates " + ", ".join(sorted(set(bad)))
    elif mark == "pending":
        tag = ("pending (G_j)" if not bad else "pending (G_j); violates " + ", ".join(sorted(set(bad))))
    else:
        tag = ("branch test: " + ", ".join(sorted(set(bad)))) if bad else \
            "MARKED BRANCH TEST but satisfies every constraint"
    if extra:
        pp, p_H, pmin = extra
        ptxt = " ".join(f"{P} {pp[P]:.4f}" for P in POOLS) + f" -> p_H {p_H:.4f} (p_H,min {pmin:.4f})"
    else:
        ptxt = "-"
    print(f"{name:5s} {ptxt}\n      labels {sorted(L) if isinstance(L, set) else L}  "
          f"qualifiers {sorted(Q)}  [{tag}]")

print()
print("Lattice at the design-stage counts (target pattern -> p per pool -> p_H):")
for pat in ("both", "h4", "h3", "none"):
    pp, ph = p_H_of(NULL["pools"], pat)
    print(f"  {pat:5s} " + " / ".join(f"{pp[P]:.4f}" for P in POOLS) + f" -> {ph:.4f}")
print("p_H,min =", round(max(p_min(NULL['pools'][P]) for P in POOLS), 4))
print("Q_record on the design-stage null side and the disclosure table:",
      q_record(NULL["pools"], NULL["determined"]))
print("Revision 5's two-pool lattice, for comparison:")
for pat in ("both", "h4", "h3"):
    a = p_pool(NULL["pools"]["P_BM"], pat)
    b = p_pool(NULL["pools"]["P_MWRA"], pat)
    print(f"  {pat:5s} {a:.4f} / {b:.4f} -> {max(a, b):.4f}")
