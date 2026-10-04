I14(b) checks every set against C1–C12. I14(c) reruns the sets at the
null-side stage with the measured values.

| # | constraint | why |
|---|---|---|
| C1 | 0 ≤ G_lo ≤ G ≤ G_hi ≤ 1 for every G, G_j and G_BM,u included, and G_hi ≥ U0(n) = 3.69/n with n its pool size | the interval of 5.3 |
| C2 | G_BM,u = (n_A(v)/n_T) · G_BM(v) for v1–v5, the same number for each | no target outside T_A(v) is reached by 𝒢_BM* (4.2) |
| C3 | if r_Ody = 0, pct_N4 is undefined; otherwise pct_N4,lo ≤ pct_N4 ≤ pct_N4,hi, each computed from integer counts x_gt, x_eq and n_stratum ≥ 200 as in 5.4 | 5.4 |
| C4 | if hit_j, then G_j > 0, G_j,hi ≥ U0(n_j) and E_j ≥ 1 | a unique survivor in the core has reach > 0; hit_j needs an eclipse-compatible unique survivor with h_tot ≥ M_Ody, for which m̂ stands in on the null side (6.5) [r2v6 #71] |
| C5 | the counts are integers: every seen_PCR leg of every variant, and strict_PCR, lie in 0..7; every seen_ALM_SL and seen_ALM_SL_side leg, and rec_ALM_BM, in 0..11; held_ALM in 0..8 at every step; E_j ≥ 0 | definitions; three counted sets have no held-out row (6.4) |
| C6 (attainability) | outcome 1 is attainable only if p_H,min ≤ 0.05; outcome 4 only if some clean negative has 0 < G_j, G_j,hi ≤ G_BM,u,lo and E_j ≥ 1; gate 3a can pass only if N_narrow[3a] ≥ 4 on every leg, and gate 3b only if N_narrow[3b] ≥ 6 on every leg. All are null-side | 7.2, 6.3.2, 6.4, 6.5 [r1v5 N5; r2v6 N1, #71] |
| C7 (the null side is fixed) [r2 R2-1 fix 2] | the null-side fields equal the design-stage estimates of 2.6 and 2.9, or after the null-side stage the measured values: n_T, n_A(v), G_BM(v) with bounds, G_BM,u with bounds; for each of the four held-out pools its n, x_max and the counts of members passing H3 and H4; p_H,min; Q_record; Q_exch; and N_narrow on every leg of both gates. **G_j, its bounds, n_j and E_j have no design-stage estimate** [r1v5 N5; r2v6 #71]. Until the null-side stage, every set's Q_attain4 is provisional. A set whose labels the placeholders decide (S4, S4b, S6b, S15), or that exists to show Q_attain4 (S14, S14b), is marked **pending**: it shows that a code branch works, and proves no outcome reachable. A set that departs from the other null-side fields is a **branch test** | R2-1 |
| C8 | in each pool P, p_P = (1 + x)/(1 + n_P) for an integer x with x_max,P ≤ x ≤ n_P, x fixed by the target's pass pattern (both, H4 only, H3 only, neither) and the pool's counts; p_H = the largest of the four p_P ≥ p_H,min. With the design-stage counts the attainable values of p_H are 0.040 (both), 0.069 (H4 only), 0.276 (H3 only) and 1 (neither) | 7.2 |
| C9 | T0 ∈ {R, RE} implies T0_pass | 3.5 |
| C10 | within one projection and one rounding step, a strict leg is at most its best-fit leg: seen_PCR[v][AL_st] ≤ seen_PCR[v][AL_bf], seen_PCR[v][WO_st] ≤ seen_PCR[v][WO_bf], and seen_ALM_SL[st, s] ≤ seen_ALM_SL[bf, s] for each step s, under both meanings of `same_apparition` | a set seen strictly has a non-empty S₀, so B = S₀ (6.3.2) |
| C11 | the disclosure table's `determined` values are frozen, and a set may not change them. A set whose target flags contradict them is realisable, and it must print Q_contra | 7.1 |
| C12 | N_narrow[3a][leg] lies in 0..7 and N_narrow[3b][leg] in 0..11 | definitions (6.3.2, 6.4) |

**Known facts, not constraints.** Some target-side and control facts are
already known or inferred:

- T0_pass is true and T0 is RE;
- the disclosure table settles H4 to fail, so p_H ≥ 0.276 (2.10);
- the target passes MWRA readings, so it is a member of all four pools
  (2.9);
- rec_ALM_BM ≤ 5;
- seen_ALM_SL ≤ 8 on any leg, because at most 8 sets can be narrowed (a C7
  field), and fewer by the truth-side count of [AppT 6];
- both all-must-pass legs of gate 3a are at most 3, and strict recall holds
  in 4 counted sets (rough; AppT 6).
