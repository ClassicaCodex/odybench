**`odybench/deltat_mix.py`** (the four-model mixture, 0 and 6.3.3) [r2v6 N2]

```
models(jd_tt, frame="canon"|"de431") -> list[(mu_s, sigma_s)]    # the four models, in that frame
intervals(fn: Callable[[f8[m]], bool[m]], lo_s, hi_s, scan_s=10.0, tol_s=0.1)
      -> list[(a_s, b_s)]        # the ΔT intervals where fn passes: a scan at scan_s,
                                 # then every change of value bisected to tol_s
p_exact(fn, jd_tt, frame, sigma_scale=1.0, span_sigma=6.0, scan_s=10.0, tol_s=0.1) -> float
      # the rule's P_mix (6.3.3): over [min(mu - 6 sigma), max(mu + 6 sigma)], the mean over the
      # four models of the sum over passing intervals of Phi((b - mu)/(s sigma)) - Phi((a - mu)/(s sigma))
grid(jd_tt, frame, n=41) -> (dt_s: f8[4, n], w: f8[4, n])       # diagnostic only; never a rule input
```

- **Vectorised.** `fn` takes a vector of ΔT values, so `eclipses.local` and
  `lunar.local` evaluate a whole scan in one call.
- **Totality.** A totality row hands `p_exact` the window of
  `eclipses.totality_window` directly, as h_tot does (4.4).
- **What the scan can miss.** A passing interval narrower than the 10-s
  step can be missed. It carries at most about 0.007 of one model's mass at
  σ = 541 s. I2(c)'s synthetic cases include intervals narrower than the
  step, to measure that loss.
