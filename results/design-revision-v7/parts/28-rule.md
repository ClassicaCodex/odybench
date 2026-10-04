```
if not INSTR:                                         return BLOCKED (no verdict is read)
labels, qualifiers = {}, {}
LEGS3A = (AL_bf, AL_st, WO_bf, WO_st)
STEPS  = (fine, mid, coarse)                          # the rounding family of the ceilings (6.4)
LEGS3B = ((bf, s) for s in STEPS) + ((st, s) for s in STEPS)
POOLS  = (P_BM, P_MWRA, P_BM_E, P_MWRA_E)

# gate 3a: four legs, the decision taken against "the method can see" (6.3.2)
def fire3a(v): return min(seen_PCR[v][leg] for leg in LEGS3A) < 4
side = fire3a(main)
if side:                                              labels += 3a
# gate 3b: six legs, under the frozen meaning of same_apparition (6.4)
fire3b = min(seen_ALM_SL[leg] for leg in LEGS3B) < 6
if fire3b:                                            labels += 3b
fire3b_other = min(seen_ALM_SL_side[leg] for leg in LEGS3B) < 6   # the other meaning; no label
if (side and max(seen_PCR[main][leg] for leg in LEGS3A) >= 4) or \
   (fire3b and max(seen_ALM_SL[leg] for leg in LEGS3B) >= 6) or \
   (fire3b_other != fire3b):
                                                      qualifiers += Q_score
# could the gates have passed? (null side, 6.3.2, 6.4)
if min(N_narrow_3a[leg] for leg in LEGS3A) < 4:       qualifiers += Q_attain3a
if min(N_narrow_3b[leg] for leg in LEGS3B) < 6:       qualifiers += Q_attain3b
if rec_ALM_BM < 6:                                    qualifiers += Q_BM
if min(held_ALM[s] for s in STEPS) < 6:               qualifiers += Q_H
if fire3a(redraft) != side or fire3a(sibling) != side:
                                                      qualifiers += Q_exposure
if fire3a(noncirc) != side:                           qualifiers += Q_dT

# null-side qualifiers (known at the second freeze)
p_H_min = max((1 + x_max[P]) / (1 + n[P]) for P in POOLS)    # 7.2
if p_H_min > 0.05:                                    qualifiers += Q_attain
if Q_record:                                          qualifiers += Q_record   # from attain.json, 7.2
if Q_exch:                                            qualifiers += Q_exch     # from attain.json, 7.2
g2  = {v: G_BM_lo[v] >= 0.20 for v in SLOTS}           # SLOTS = v0..v5
tol = {v: G_BM_lo[v] >  0.05 for v in SLOTS}
if all(tol.values()):                                 qualifiers += Q_tol
if len(set(g2.values())) > 1 or len(set(tol.values())) > 1:
                                                      qualifiers += Q_slot
if not any(0 < G_j[j] and G_j_hi[j] <= G_BM_u_lo and E_j[j] >= 1 for j in clean_negatives):
                                                      qualifiers += Q_attain4

# target-side qualifier
if Q_contra:                                          qualifiers += Q_contra   # from heldout.json, 7.1

# 4: the eclipse-matching method dates fiction
if any(hit_j[j] and G_j_hi[j] <= G_BM_u_lo for j in clean_negatives):
                                                      labels += 4

# 2: B&M's match carries no weight
if r_Ody == 0:                                        labels += "2 (no match)"
elif all(g2.values()) or pct_N4_lo >= 0.50:           labels += "2 (ordinary)"

# 1: the text dates the return, by the clues nobody fitted; no gate vetoes it (1.3)
p_H = max(p[P] for P in POOLS)                        # p[P] = 1 if the target is not a member of P
if T0_pass and p_H <= 0.05:                           labels += 1

if labels is empty:                                   labels = {inconclusive}
return labels, qualifiers
```

U0(n) = 3.69/n is the gamma upper bound of a G with no target reached.
Revision 6 also defined CP_hi, which no line of the rule used; it is gone
[r2v6 N10d].
