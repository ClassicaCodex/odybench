**Which sets can be narrowed: gate 3a's attainability** [r2v6 N1 fixes 2–3].
Narrowing, |S₀| ≤ 0.05 N_cand (or |B| for a best-fit leg), does not depend
on the truth. It is a property of a set's projection and of the window, so
it is computed on the null side.

- **narrowable[3a][leg][set]** is true if the set's |S₀| (strict legs) or
  |B| (best-fit legs) is at most 5% of the candidates in at least 11 of the
  21 null windows of I16(a). Those windows are placed at random over
  −1999..+300 by a frozen seed, around no truth, so no truth is read. The
  bench's own search computes it at the null-side stage, and I16(a) checks
  that search on the same windows.
- **N_narrow[3a][leg]** is the number of the 7 counted sets that can be
  narrowed on that leg. It is frozen at the second freeze in `attain.json`.
- **Q_attain3a holds if N_narrow[3a][leg] < 4 on some leg.** The gate fires
  if any leg is below 4, so it could not then have passed, whatever the
  method. Label 3a is printed as "untested by these controls", and every
  eclipse-dependent "no" stays "could not have seen it".
- **Expected.** R-THUC and R-XEN cannot be narrowed on any leg, because
  their "none" site primaries leave S₀ far wider than 5% (6.3.4; for
  R-THUC the recheck's hand estimate is about 35 survivors against a bound
  of about 16 [r2v6 §5]). The other five are expected to narrow. So
  N_narrow is 5 on every leg, and Q_attain3a is not expected (R28).

