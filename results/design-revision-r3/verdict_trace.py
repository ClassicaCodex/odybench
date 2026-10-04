"""Design revision 4 scratch: an executable transcription of the rule of
DESIGN 9.2, run on the synthetic sets of 9.5, with the constraints C1-C9 of
9.4 checked for every set marked realisable.  This is a check of the design
text, not bench code.
Run: py results/design-revision-r3/verdict_trace.py
"""
import copy
from scipy.stats import beta

SLOTS = ["v0", "v1", "v2", "v3", "v4", "v5"]
NULL = {   # design-stage estimates, DESIGN 2.9
    "G_BM": {"v0": (0.224, 0.139, 0.344, 82), "v1": (0.140, 0.087, 0.215, 131),
             "v2": (0.211, 0.131, 0.324, 87), "v3": (0.278, 0.172, 0.427, 66),
             "v4": (0.182, 0.112, 0.279, 101), "v5": (0.327, 0.203, 0.504, 56)},
    "n_T": 10690, "G_BM_u": 0.00172, "n_H": 76, "x_max": 1,
}


def cp_lo(k, n):
    return 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)


def cp_hi(k, n):
    return 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)


def decide(q):
    if not q["INSTR"]:
        return "BLOCKED", set()
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
    p_min = (1 + q["x_max"]) / (1 + q["n_H"])
    if p_min > 0.05:
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
    p_H = (1 + q["x_target"]) / (1 + q["n_H"])
    if q["T0_pass"] and p_H <= 0.05 and not ({"3a", "3b", "4"} & L):
        L.add("1")
    if not L:
        L = {"inconclusive"}
    return L, Q


def check(q):
    """C1-C9 for a realisable set; returns violated constraints."""
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
    for k in ("seen_ALM_SL", "rec_ALM_BM", "held_ALM"):
        if not 0 <= q[k] <= 11:
            bad.append("C5")
    for k in ("G_BM", "n_T", "G_BM_u", "n_H", "x_max"):
        if q[k] != NULL[k]:
            bad.append(f"C7 {k}")
    if not q["x_max"] <= q["x_target"] <= q["n_H"]:
        bad.append("C8")
    return bad


S0 = dict(INSTR=True, T0_pass=True, x_target=16, r_Ody=0.0815, pct=(30, 10, 200),
          seen_PCR=5, strict_PCR=4, redraft=5, sibling=5, noncirc=5,
          seen_ALM_SL=7, rec_ALM_BM=3, held_ALM=8, negatives=[(False, 0.0012)] * 12,
          **copy.deepcopy(NULL))


def var(**kw):
    q = copy.deepcopy(S0)
    q.update(kw)
    return q


S1 = var(x_target=1)
S2 = var(pct=(118, 12, 200))
SETS = {
    "S0": (S0, True), "S1": (S1, True), "S1b": (var(x_target=2), True), "S2": (S2, True),
    "S2nm": (var(r_Ody=0.0, pct=None), True),
    "S3a": (var(seen_PCR=2, redraft=2, sibling=2, noncirc=2), True),
    "S3b": (var(seen_ALM_SL=3), True),
    "S4": (var(negatives=[(True, 0.00112)] + [(False, 0.0012)] * 11), True),
    "S5": (var(x_target=4, x_max=4), False),
    "S6": (var(x_target=1, pct=(118, 12, 200)), True),
    "S6b": (var(pct=(118, 12, 200), seen_ALM_SL=3, held_ALM=4, strict_PCR=2, redraft=3, noncirc=3,
                negatives=[(True, 0.00112)] + [(False, 0.0012)] * 11), True),
    "S7": (var(INSTR=False), True),
    "S8": (var(x_target=1, T0_pass=False), True),
    "S9": (var(x_target=1, seen_PCR=3, redraft=3, sibling=3, noncirc=3), True),
    "S10": (var(G_BM={v: (0.327, 0.203, 0.504, 56) for v in SLOTS}), False),
    "S11": (var(x_target=1, rec_ALM_BM=7, held_ALM=4), True),
}
for name, (q, realisable) in SETS.items():
    L, Q = decide(q)
    bad = check(q)
    tag = "realisable" if not bad else ("branch test: " + ", ".join(sorted(set(bad))))
    if realisable and bad:
        tag = "SHOULD BE REALISABLE but violates " + ", ".join(sorted(set(bad)))
    p_H = (1 + q["x_target"]) / (1 + q["n_H"])
    print(f"{name:5s} p_H {p_H:.4f}  labels {sorted(L) if isinstance(L, set) else L}  "
          f"qualifiers {sorted(Q)}  [{tag}]")
