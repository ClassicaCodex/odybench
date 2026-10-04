**What each set shows:**

- **The four outcomes and the inconclusive verdict.** S1 reaches 1, S2 and
  S2nm reach 2 in both forms, S3a and S3b reach 3 in both parts, S4 reaches
  4, and S0 is inconclusive.
- **Which are proven reachable now.** S1, S2, S2nm, S3a, S3b and S0 are
  realisable on the design-stage null side. The only known fact S1
  contradicts is target-side: H4, which the record settles to fail. That is
  why Q_record holds in every set, and why S1 also prints Q_contra. S4's
  realisability waits for G_j and hit_j(m̂).
- **The expected verdicts.** S0x reproduces the verdict expected if gate 3b
  passes: {3a}, with Q_score3a, because gate 3a's best-fit leg sits at its
  threshold, and Q_score3b, because gate 3b's pass rests on the meaning of
  `same_apparition`. Revision 7 printed one Q_score for both [r3v7 R3-10].
  S0y reproduces the verdict expected if it does not: {3a, 3b}, with
  Q_score3a.
- **One way to a "yes".** S1 passes both held-out predicates. S1b passes H4
  alone: on the four-pool lattice that gives 0.069, so it is not enough.
- **What blocks label 1:** T0_pass false (S8); a target outside some pools
  (S12); or a pool whose floor exceeds 0.05 (S13, a branch test, because on
  the design-stage counts every pool's floor is below 0.05).
- **What does not block it:** the gates and the control qualifiers. S9 shows
  label 1 with 3a, S15 with 3b and 4 (pending), S11 with Q_H and without
  Q_BM, and S18 with Q_exch, which qualifies label 1 but leaves it standing.
- **Outcome 4 against the Odyssey's lower bound** [r2v6 N8]. S4b's negative
  would have fired outcome 4 under revision 6's comparison with the point
  value, and does not now.
- **What Q_attain4 needs** [r2v6 #71; r3v7 R3-2]. S14 lacks the G condition,
  and S14b the eclipse condition: in S14b every negative's G condition
  holds, but no eclipse-compatible reading reaches an eclipse of the
  Odyssey's strength. S14c shows revision 8's change. Its negatives make
  such eclipses unique (E_j 2), but only outside the Odyssey's two windows,
  where label 4 cannot score them. So Q_attain4 holds; revision 7's rule,
  which read E_j, would not have printed it.
- **The Q_attain4 guard** [r3v7 R3-2]. In S4c AEN-TROY's only hit is the
  masked target's own date, so no negative has hit_j(m̂) and the null-side
  record printed Q_attain4. Label 4 fires after the second freeze, and the
  rule does not print Q_attain4 beside it (6.5).
- **The gates' attainability** [r2v6 N1; r3v7 R3-8]. S16 and S17 show 3a
  and 3b printed as "untested by these controls". S20 shows the other side:
  both gates pass, although fewer sets can be narrowed by majority than
  their thresholds, as when sets near the line are narrowed in the gates'
  own windows. Revision 7's rule printed Q_attain3a and Q_attain3b beside
  the passing gates; revision 8's prints neither. All three are branch
  tests: the design-stage N_narrow (5 and 8) clears both thresholds.
- **The rounding family** [r2v6 N6]. S19 shows Q_H from the fine step alone.
- **Co-occurrence.** S6 shows labels 1 and 2 together. S6b shows labels and
  every control qualifier together.
- **Branch tests.** S5 shows the Q_attain branch, S10 the label-2 G leg, S13
  a single pool's veto, S16, S17 and S20 the gates' attainability, and S18
  Q_exch. Each needs null-side values that contradict 2.6 or 2.9, so none
  proves an outcome reachable. S14, S14b and S14c show Q_attain4, and S4c
  its guard; all four are pending.
- **S7** shows the instrument block.

**At the null-side stage** (12.3), I14(c) replaces the null-side fields by
the measured values, G_j, hit_j(m̂) and E_j included, and reruns S0–S20.

- Each set keeps the target's pass pattern (both, H4 only, H3 only,
  neither), and each pool's p is recomputed with the measured counts.
- If S1 then no longer returns {1}, outcome 1 is unattainable, and Q_attain
  says so in every verdict.
- The measured G_j and hit_j(m̂) settle S4, S4b, S4c, S6b, S14, S14b, S14c and
  S15. If no clean negative meets both conditions of Q_attain4, outcome 4 is
  unattainable, and Q_attain4 says so.
- The measured N_narrow settles whether Q_attain3a or Q_attain3b would
  print beside a firing gate, and Q_exch is read from the measured tests.
- Q_record is recomputed from the measured lattice.
- All of this is recorded at the second freeze, before any target-side
  number exists.