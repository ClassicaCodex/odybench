### 5.7 Evidential weight: an identity, a ceiling and a Bayes factor

Revision 2's bottom line was a likelihood ratio, LR = R_obs/G. In it,
R_obs was the mean reach of a truth whose sky an observer had described.
The recheck showed that it can never pass about 6.5, whatever the data
[r1 N1]. The argument has four steps.

1. With the poem held fixed, every truth accepted in PC-S science mode
   carries the Odyssey's clue set at the Odyssey's offsets.
2. So the survivor sets are the Odyssey's, and R_obs and G are two
   weightings of one reach function: R_obs = E[reach · 1_A] / P(A) and
   G = E[reach], both over T_C.
3. Hence

   **LR_slot = P_w(A) / P(A) ≤ 1 / P(A)**, where P_w is the reach-weighted
   probability.
4. P(A) is 0.154, so the ceiling is about 6.5 (5.1–9.0) (2.8).

**The identity is a finding, not a bug.** An observer who records that a
bright star heralded the dawn and that Hermes flew can raise the odds of a
target by at most the inverse of how often a sky has those features. The
precision that B&M's criteria carry (90 minutes, ±1 day) belongs to the
reader, not to the text. Two consequences follow:

- under the conditioning of 5.3, where the categorical readings were formed
  with the target in view, LR_slot over T_A is identically 1;
- any rule threshold on such a ratio is decided by the observation model,
  not by the Odyssey.

**So no likelihood ratio enters the decision rule** [r1 N1 fix 2(a)].
Outcome 1 rests on G over T_A, on pct_N4 and on T0. Outcome 2 rests on G
and pct_N4. Revision 2's R_obs/G, its curve over noise and LR_sf are
withdrawn as rule inputs. What is reported, as standing findings beside the
verdict:

1. **The ceiling.** P(A), with its interval, and 1/P(A), recomputed on the
   bench's sky tables over T_C. **LR_slot(ν)** is also given as a curve over
   the noise grid of 6.2. Its numerator is computed exactly, not by
   sampling [r1 N8 fix 1]:

   R_obs(ν) = Σ_t Σ_δ reach(t) · 1[A(t, δ)] · w(δ) / Σ_t Σ_δ 1[A(t, δ)] · w(δ),

   - t runs over T_C;
   - δ runs over every vector of slot-day offsets in [−j, j], with weight
     w(δ) uniform, and with the Mercury displacement s_M applied to the slot
     tolerance;
   - reach is taken from the same garden and the same W as the denominator
     [r1 N8 fix 3].

   No new survivor sets are needed, because the poem is fixed.
2. **The Bayes factor of the residual fit under B&M's own hypothesis.**
   H1_BM says that the poet encoded the phenomena of some reading r of
   𝒢_BM*, each reading equally likely (π_r = 1/36). H0 says the clues are
   unrelated to the target. Under H1_BM, with probability ρ_r the target's
   sky passes reading r. Otherwise it is a sky drawn from T_A that fails r.
   For the target t_S = 16 Apr −1177,

   BF_BM(ρ) = Σ_r π_r [ ρ_r · 1{t_S passes r} / p_r + (1 − ρ_r) · 1{t_S fails r} / (1 − p_r) ],

   where p_r = (number of targets of T_A \ {t_S} passing r + 1)/(n_A + 1).
   This is the pass rate of reading r as a filter (survival, not uniqueness),
   with the add-one rule so that no p_r is 0. BF_BM is exact for the
   whole pass/fail vector of t_S under that model.
   - It is reported at ρ_r = 1, the model most favourable to B&M, and at
     ρ_r = the PC-S science-mode recall of r at ν_real (6.2).
   - Its ceiling is BF_max = Σ_r π_r/p_r, reached when t_S passes every
     reading.
   - From the recheck's numbers, B&M's reading alone passes about 5 of 41
     targets of T_A, so it can contribute at most about 8 (2.8). That figure
     is rough.
3. **The *Almagest* calibration** [r1 N1 fix 4]. The same estimator is
   applied to each counted *Almagest* set:
   - it gives the BF of the set's true date under the set's own garden (its
     fork options, at regime-SL tolerances);
   - p_r is the share of civil days in the background that pass reading r.

   This shows what truly observed records, whose statements carry their own
   precision, earn under the machinery that scores the Odyssey.
4. **The blind version of the words.** The words' ceiling if the categorical
   readings had been formed blind is 1/P(A), about 6.5. The bench prints it
   beside BF_BM as "what the words could carry if C, V and M had been
   proposed without the target".

The bench reports these figures, together with G, p_fix and the bit budget.
It does not multiply any of them by a prior.

---

