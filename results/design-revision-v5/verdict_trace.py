"""Design revision 5 scratch: an executable transcription of the rule of
DESIGN 9.2 (revision 5), run on the synthetic sets of 9.5, with the
constraints C1-C9 of 9.4 checked for every set marked realisable.

Changes from results/design-revision-r3/verdict_trace.py (revision 4):
  * the held-out test reads two pools, P_BM and P_MWRA, and p_H is the larger
    of the two exact p-values (7.2); a pool's p is 1 if the target is not a
    member of it;
  * each pool is described by its counts (n, members passing H3 only, H4 only,
    both), and the target by its pass pattern; the weights -log10 q are
    computed over pool + target, exactly as 7.2 says;
  * C5 caps held_ALM at 8 (three counted Almagest sets have no held-out row);
  * C7 fixes both pools' counts; C8 is the two-pool lattice.
This checks the design text; it is not bench code.
Run: py results/design-revision-v5/verdict_trace.py
"""
import copy
import math
from scipy.stats import beta

SLOTS = ["v0", "v1", "v2", "v3", "v4", "v5"]
# design-stage null side (DESIGN 2.9; r2 check_gbm.py, check_slot_scaling.py;
# revision 4 heldout_attain.py; revision 5 heldout_strata.py)
NULL = {
    "G_BM": {"v0": (0.224, 0.139, 0.344, 82), "v1": (0.140, 0.087, 0.215, 131),
             "v2": (0.211, 0.131, 0.324, 87), "v3": (0.278, 0.172, 0.427, 66),
             "v4": (0.182, 0.112, 0.279, 101), "v5": (0.327, 0.203, 0.504, 56)},
    "n_T": 10690, "G_BM_u": 0.00172,
    # pool counts: n, members passing H3 only, H4 only, both
    "pools": {"P_BM": dict(n=76, h3=14, h4=1, both=1),
              "P_MWRA": dict(n=43, h3=8, h4=1, both=0)},
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
    x3 = a3 + ab + t3          # passers of H3 over pool + target
    x4 = a4 + ab + t4
    w3 = -math.log10(x3 / (n + 1)) if x3 else 0.0
    w4 = -math.log10(x4 / (n + 1)) if x4 else 0.0
    s_t = t3 * w3 + t4 * w4
    scores = [w3 + w4] * ab + [w3] * a3 + [w4] * a4 + [0.0] * (n - ab - a3 - a4)
    x = sum(1 for s in scores if s >= s_t - 1e-12)
    return (1 + x) / (1 + n)


def p_min(pool):
    return (1 + pool["both"]) / (1 + pool["n"])


def decide(q):
    if not q["INSTR"]:
        return "BLOCKED", set(), None
    L, Q = set(), set()
    if q["seen_PCR"] < 4:
        L.add("3a")
    if q["seen_ALM_SL"] < 6:
        L.add("3b")
    if q["rec_ALM_BM"] < 6:
        Q.add("Q_BM")
    if q["held_ALM"] < 6:
        Q.add("Q_H")
    if q["strict_PCR"] < 4:
        Q.add("Q_strict")
    side = q["seen_PCR"] < 4
    if (q["redraft"] < 4) != side or (q["sibling"] < 4) != side:
        Q.add("Q_exposure")
    if (q["noncirc"] < 4) != side:
        Q.add("Q_dT")
    pmin = max(p_min(q["pools"][P]) for P in ("P_BM", "P_MWRA"))
    if pmin > 0.05:
        Q.add("Q_attain")
    g2 = {v: q["G_BM"][v][1] >= 0.20 for v in SLOTS}
    tol = {v: q["G_BM"][v][1] > 0.05 for v in SLOTS}
    if all(tol.values()):
        Q.add("Q_tol")
    if len(set(g2.values())) > 1 or len(set(tol.values())) > 1:
        Q.add("Q_slot")
    if any(h and gh <= q["G_BM_u"] for h, gh in q["negatives"]):
        L.add("4")
    if q["r_Ody"] == 0:
        L.add("2 (no match)")
    else:
        xg, xe, n = q["pct"]
        if all(g2.values()) or cp_lo(xg, n) >= 0.50:
            L.add("2 (ordinary)")
    pp = {P: p_pool(q["pools"][P], q["pattern"], q["member"][P]) for P in ("P_BM", "P_MWRA")}
    p_H = max(pp.values())
    if q["T0_pass"] and p_H <= 0.05 and not ({"3a", "3b", "4"} & L):
        L.add("1")
    if not L:
        L = {"inconclusive"}
    return L, Q, (pp, p_H, pmin)


def check(q):
    """C1-C9 for a set marked realisable; returns the violated constraints."""
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
    for h, gh in q["negatives"]:
        if h and gh < 3.69 / q["n_T"]:
            bad.append("C4")
    for k in ("seen_PCR", "strict_PCR", "redraft", "sibling", "noncirc"):
        if not 0 <= q[k] <= 7:
            bad.append("C5")
    for k in ("seen_ALM_SL", "rec_ALM_BM"):
        if not 0 <= q[k] <= 11:
            bad.append("C5")
    if not 0 <= q["held_ALM"] <= 8:
        bad.append("C5 held_ALM")
    for k in ("G_BM", "n_T", "G_BM_u", "pools"):
        if q[k] != NULL[k]:
            bad.append(f"C7 {k}")
    if q["pattern"] not in ("both", "h4", "h3", "none"):
        bad.append("C8")
    if q["T0"] in ("R", "RE") and not q["T0_pass"]:
        bad.append("C9")
    return bad


S0 = dict(INSTR=True, T0_pass=True, T0="RE", pattern="h3",
          member={"P_BM": True, "P_MWRA": True}, r_Ody=0.0815, pct=(30, 10, 200),
          seen_PCR=5, strict_PCR=4, redraft=5, sibling=5, noncirc=5,
          seen_ALM_SL=7, rec_ALM_BM=3, held_ALM=8, negatives=[(False, 0.0012)] * 12,
          **copy.deepcopy(NULL))


def var(**kw):
    q = copy.deepcopy(S0)
    for k, v in kw.items():
        if k == "pool_override":
            for P, d in v.items():
                q["pools"][P].update(d)
        else:
            q[k] = v
    return q


NEG4 = [(True, 0.00112)] + [(False, 0.0012)] * 11
SETS = {
    "S0": (S0, True),
    "S1": (var(pattern="both"), True),
    "S1b": (var(pattern="h4"), True),
    "S2": (var(pct=(118, 12, 200)), True),
    "S2nm": (var(r_Ody=0.0, pct=None), True),
    "S3a": (var(seen_PCR=2, redraft=2, sibling=2, noncirc=2), True),
    "S3b": (var(seen_ALM_SL=3), True),
    "S4": (var(negatives=NEG4), True),
    "S5": (var(pattern="both", pool_override={"P_BM": dict(both=4, h3=11)}), False),
    "S6": (var(pattern="both", pct=(118, 12, 200)), True),
    "S6b": (var(pct=(118, 12, 200), seen_ALM_SL=3, held_ALM=4, strict_PCR=2, redraft=3,
                noncirc=3, negatives=NEG4), True),
    "S7": (var(INSTR=False), True),
    "S8": (var(pattern="both", T0_pass=False, T0="NR"), True),
    "S9": (var(pattern="both", seen_PCR=3, redraft=3, sibling=3, noncirc=3), True),
    "S10": (var(G_BM={v: (0.327, 0.203, 0.504, 56) for v in SLOTS}), False),
    "S11": (var(pattern="both", rec_ALM_BM=7, held_ALM=4), True),
    "S12": (var(pattern="both", member={"P_BM": True, "P_MWRA": False}), True),
    "S13": (var(pattern="h4", pool_override={"P_MWRA": dict(h4=2)}), False),
}
for name, (q, realisable) in SETS.items():
    L, Q, extra = decide(q)
    bad = check(q)
    tag = "realisable" if not bad else ("branch test: " + ", ".join(sorted(set(bad))))
    if realisable and bad:
        tag = "SHOULD BE REALISABLE but violates " + ", ".join(sorted(set(bad)))
    if not realisable and not bad:
        tag = "MARKED BRANCH TEST but satisfies every constraint"
    if extra:
        pp, p_H, pmin = extra
        ptxt = f"p_BM {pp['P_BM']:.4f} p_MWRA {pp['P_MWRA']:.4f} -> p_H {p_H:.4f} (p_H,min {pmin:.4f})"
    else:
        ptxt = "-"
    print(f"{name:5s} {ptxt}  labels {sorted(L) if isinstance(L, set) else L}  "
          f"qualifiers {sorted(Q)}  [{tag}]")

print()
print("Lattice at the design-stage counts (target pattern -> p_BM / p_MWRA -> p_H):")
for pat in ("both", "h4", "h3", "none"):
    a = p_pool(NULL["pools"]["P_BM"], pat)
    b = p_pool(NULL["pools"]["P_MWRA"], pat)
    print(f"  {pat:5s} {a:.4f} / {b:.4f} -> {max(a, b):.4f}")
print("p_H,min =", round(max(p_min(NULL['pools'][P]) for P in ('P_BM', 'P_MWRA')), 4))
