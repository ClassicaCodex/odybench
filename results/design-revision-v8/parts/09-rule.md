# gate 3a: four legs, the decision taken against "the method can see" (6.3.2)
def fire3a(v): return min(seen_PCR[v][leg] for leg in LEGS3A) < 4
side = fire3a(main)
if side:                                              labels += 3a
if side and max(seen_PCR[main][leg] for leg in LEGS3A) >= 4:
                                                      qualifiers += Q_score3a
# gate 3b: six legs, under the frozen meaning of same_apparition (6.4)
fire3b = min(seen_ALM_SL[leg] for leg in LEGS3B) < 6
if fire3b:                                            labels += 3b
fire3b_other = min(seen_ALM_SL_side[leg] for leg in LEGS3B) < 6   # the other meaning; no label
if (fire3b and max(seen_ALM_SL[leg] for leg in LEGS3B) >= 6) or (fire3b_other != fire3b):
                                                      qualifiers += Q_score3b
# could the gates have passed? null side; printed only beside a gate that fired (6.3.2, 6.4)
if side and min(N_narrow_3a[leg] for leg in LEGS3A) < 4:     qualifiers += Q_attain3a
if fire3b and min(N_narrow_3b[leg] for leg in LEGS3B) < 6:   qualifiers += Q_attain3b
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

# target-side qualifier
if Q_contra:                                          qualifiers += Q_contra   # from heldout.json, 7.1

# 4: the eclipse-matching method dates fiction
if any(hit_j[j] and G_j_hi[j] <= G_BM_u_lo for j in clean_negatives):
                                                      labels += 4
# could outcome 4 have fired? null side, from attain.json (6.5); never beside a label 4
if 4 not in labels and \
   not any(0 < G_j[j] and G_j_hi[j] <= G_BM_u_lo and hit_hat_j[j] for j in clean_negatives):
                                                      qualifiers += Q_attain4   # hit_hat_j = hit_j(m̂)