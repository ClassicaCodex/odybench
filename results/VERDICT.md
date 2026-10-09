# odybench: the lean verdict

LEAN.md (amendment 1 to DESIGN.md revision 8), "The rule, restricted"; thresholds of `data/prereg/verdict_rule.json`, unchanged.

## Headline

- Inconclusive: no label of the lean rule holds
- Q_record: the held-out test could not have said yes for this target, given the facts on record (H4 settled to fail)
- Q_BM: at B&M's own tolerances, fewer than 6 of 11 Almagest record sets are recovered
- Q_tol: under every slot variant G_BM,lo > 0.05, so B&M's tolerances cannot make the match notable
- Q_slot: the verdict on G depends on the slot variant

**Labels:** inconclusive  
**Qualifiers:** Q_BM, Q_tol, Q_slot, Q_record  
**Not tested in the lean run:** 3a, 4, label 2's pct_N4 leg

## Every number beside its threshold

| quantity | value | condition | holds | source |
|---|---|---|---|---|
| INSTR | True | all kept instrument checks pass | True | instrument/summary.json:INSTR |
| T0_pass | True | label 1 needs true | True | t0/t0.json:T0_pass |
| T0 (reported) | RE | R / RE / NR | reported | t0/t0.json:T0 |
| p_H | 1 | label 1 needs <= 0.05 | False | heldout/heldout.json:p_H |
| p_H,min | 0.04 | Q_attain if > 0.05 | False | attain/attain.json:p_H_min |
| Q_record | True | printed if true | True | attain/attain.json:Q_record |
| Q_exch | False | printed if true | False | attain/attain.json:Q_exch |
| Q_contra | False | printed if true | False | heldout/heldout.json:Q_contra |
| r_Ody | 0.08145 | label 2 (no match) if == 0.0 | False | t0/t0.json:r_Ody |
| G_BM,lo(v0) | 0.1456 | label 2 (ordinary) needs >= 0.2 for every v; Q_tol needs > 0.05 for every v | (False, True) | attain/attain.json:G_BM |
| G_BM,lo(v1) | 0.09153 | label 2 (ordinary) needs >= 0.2 for every v; Q_tol needs > 0.05 for every v | (False, True) | attain/attain.json:G_BM |
| G_BM,lo(v2) | 0.1373 | label 2 (ordinary) needs >= 0.2 for every v; Q_tol needs > 0.05 for every v | (False, True) | attain/attain.json:G_BM |
| G_BM,lo(v3) | 0.1831 | label 2 (ordinary) needs >= 0.2 for every v; Q_tol needs > 0.05 for every v | (False, True) | attain/attain.json:G_BM |
| G_BM,lo(v4) | 0.1184 | label 2 (ordinary) needs >= 0.2 for every v; Q_tol needs > 0.05 for every v | (False, True) | attain/attain.json:G_BM |
| G_BM,lo(v5) | 0.2157 | label 2 (ordinary) needs >= 0.2 for every v; Q_tol needs > 0.05 for every v | (True, True) | attain/attain.json:G_BM |
| seen_ALM_SL (six legs) | [6, 6, 6, 6, 6, 6] | 3b fires if min < 6 | False | alm/alm.json:seen_ALM_SL |
| rec_ALM_BM | 3 | Q_BM if < 6 | True | alm/alm.json:rec_ALM_BM |

## Notes

- 3a: not tested (PC-R and gate 3a deferred, LEAN.md)
- 4: not tested (the negatives deferred, LEAN.md)
- label 2's pct_N4 leg: not tested (N4 deferred, LEAN.md)
- not evaluated in the lean rule: Q_score3a, Q_score3b, Q_attain3a, Q_attain3b, Q_H, Q_exposure, Q_dT, Q_attain4

## Held-out test (DESIGN 7.2)

| pool | member | n | p |
|---|---|---|---|
| P_BM | True | 76 | 1 |
| P_MWRA | True | 43 | 1 |
| P_BM_E | True | 49 | 1 |
| P_MWRA_E | True | 28 | 1 |

p_H = 1; disclosure table determined = {'H3': None, 'H4': 'fail'}; Q_contra = False

## N6: the eclipse at Ithaca (reported, not a rule input)

Each Delta-T model taken as a Gaussian with its stated sigma (an assumption, DESIGN 0).

| site | eclipse | P(total) canon frame, mixture | own frames, mixture | P(smag >= 0.9) canon, mixture |
|---|---|---|---|---|
| ithaki | 1178BC | 0.3076 | 0.3091 | 0.9313 |
| ithaki | 1131BC | 0.5001 | 0.4979 | 0.9989 |
| ithaki | joint (common offset) | 0.0691 | 0.06568 | |
| kefalonia | 1178BC | 0.3091 | 0.3106 | 0.9314 |
| kefalonia | 1131BC | 0.4641 | 0.4605 | 0.9985 |
| kefalonia | joint (common offset) | 0.001778 | 0.0002918 | |
| lefkada | 1178BC | 0.3438 | 0.3451 | 0.949 |
| lefkada | 1131BC | 0.5214 | 0.5217 | 0.9988 |
| lefkada | joint (common offset) | 0.2461 | 0.2438 | |
| corfu | 1178BC | 0.4107 | 0.4108 | 0.9732 |
| corfu | 1131BC | 0.4988 | 0.5018 | 0.9981 |
| corfu | joint (common offset) | 0.354 | 0.3581 | |
| zakynthos | 1178BC | 0.246 | 0.2476 | 0.8917 |
| zakynthos | 1131BC | 0.4276 | 0.4234 | 0.9977 |
| zakynthos | joint (common offset) | 0 | 0 | |
| vathy | 1178BC | 0.3076 | 0.3091 | 0.9313 |
| vathy | 1131BC | 0.4997 | 0.4975 | 0.9989 |
| vathy | joint (common offset) | 0.06791 | 0.06448 | |

## Expected on known facts (LEAN.md; not a prediction, never counted as a success)

- T0: RE (18 Mar 1189 BC passes N, C, V and M as well)
- G_BM(v1): about 0.14; lower bounds 0.087-0.20 across the slot family; Q_tol and Q_slot expected
- p_H_min: about 0.040; Q_record holds
- P(total at Ithaki, 16 Apr -1177), mixture: about 0.30
- rec_ALM_BM: <= 5 (Q_BM expected); seen_ALM_SL about 9 of 11

## Provenance

- `C:\Projects\odybench\results\attain\attain.json` sha256 `e955c9dcf16ddcaa41e9e517bba4c92ae89bc12733c55488d54b08ba2d579e06`
- `C:\Projects\odybench\results\t0\t0.json` sha256 `deba80d8cf6747b2bec8f3d2332da07cef23f19ee558e1eea0dd34246d6f8d14`
- `C:\Projects\odybench\results\heldout\heldout.json` sha256 `55d2d9432cd6764b3d216c2b0373862eff726ec992c4577f18903d5c6aa61383`
- `C:\Projects\odybench\results\n6\n6.json` sha256 `c52eb56646ce8eca495a66075cd53474342839fe4a65128a8a259cb7168007fd`
- `C:\Projects\odybench\results\alm\alm.json` sha256 `b2ec7ccd5044ded117516ce42e5f40ad47733544b88b3b3325566b7b2ceabc66`
- `C:\Projects\odybench\results\instrument\summary.json` sha256 `b538aa6b15a86d3852fd94dbf1a186fe6ed2df41e2080c4adfe6fa39d9d9264b`
