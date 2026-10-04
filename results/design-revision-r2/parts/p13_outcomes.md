### 1.3 Outcomes

The verdict is a set of labels computed mechanically by `verdict.py` from
named quantities (section 9). Every condition names its garden and its
target pool (section 5.3), and every interval is taken against the claim
being made. The labels:

1. **The text dates the return.** Five things must all hold:
   - B&M's search reproduces as stated, without the equinox clue
     (T0 = R, section 3.5).
   - After the conditioning of section 5.3, a target fixed in advance is
     rarely made the unique match by any of B&M's own readings
     (G_BM,hi ≤ 0.05).
   - Random poems of the same grammar, read with the same freedom, rarely
     reach Schoch's target as well as the Odyssey does (pct_N4,hi ≤ 0.05).
   - Both components of the method can see (section 6).
   - No clean negative dates itself.

   When B&M's tolerances cannot recover expert records (Q_BM), the second
   condition must also hold for the documented garden. The bench then says
   so, and it prints beside the label the evidential weight the words can
   carry (section 5.7).
2. **The match is ordinary.** Either condition is enough:
   - some reading B&M raised often makes a comparable target the unique match
     (G_BM,lo ≥ 0.20);
   - at least half the random poems of the same specificity reach Schoch's
     target as well as the Odyssey does (pct_N4,lo ≥ 0.50).

   The coincidence then carries no evidential weight, whatever its
   fixed-reading p-value.
3. **The method cannot see**, split by component [rev #3]:
   - **3a, the eclipse component**: the method does not recover the dates of
     real eclipse records (PC-R, section 6.3).
   - **3b, the B&M-type component** (lunar phase, star season, morning star,
     Mercury turning point): the method does not recover the dates of real
     planetary and lunar records of B&M's own kinds, at observer slack
     calibrated on the *other* records (the *Almagest* control, section
     6.4).

   Every "no" about the Odyssey that depends on the failing component is
   reported as "could not have seen it".
4. **The method dates fiction.** A clean negative (fiction composed long
   after the events it tells) yields, under its own sourced readings, an
   eclipse match at least as strong as the Odyssey's (hit_j). Its
   significance must also be at least as great, even at the negative's
   least favourable bound (G_j,hi ≤ G_BM,u). That retires the method, not
   only the claim.

**Inconclusive** is reported when none of the labels applies, with every
quantity and threshold beside it. Labels 2, 3a, 3b and 4 can hold together;
label 1 excludes all the others.

**Qualifiers** are reported whenever they hold:

| qualifier | meaning | section |
|---|---|---|
| Q_BM | B&M's own tolerances and proxies cannot recover expert planetary records | 6.4 |
| Q_strict | an all-clues-must-pass rule rejects the true date of most real eclipse records | 6.3 |
| Q_exposure | gate 3a changes when the possibly steered control rows are re-drafted blind, or when they are set to their sibling convention | 6.3.4 |
| Q_ΔT | gate 3a changes when the controls whose eclipses helped fit the ΔT models are scored without that fit | 6.3.3 |
| Q_attain | with the measured pool sizes, outcome 1 could not have been reached at all; every "no" is then a "could not have said yes" | 9.4 |

**Standing findings** are printed with every verdict and never change a
label. They are: the evidential ceiling of the words (1/P(A), and the Bayes
factor BF_BM under B&M's own encoding hypothesis, section 5.7); the T0 grid
(3.5); the ancient reading R_anc (5.3); and the held-out clues (7).

"What, if anything, the text can date" is reported in every case, at the
level the tests support: a relative chronology [chron §5], a month-turn on
Day 0 under one reading [txt §5.1], a season the text does not determine
[txt §5.6], and a year only if outcome 1 holds.

---

