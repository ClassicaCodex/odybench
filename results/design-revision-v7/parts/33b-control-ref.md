reference_fails(clueset_json: dict, projection: dict, window: (jd0, jd1),
                catalogues: dict) -> dict(candidates: f8[n], row_pass: bool[n_rows, n],
                                          fails: i2[n],       # f(c), per-row flags (6.1, I16)
                                          linked: i8[n_links, n],    # linked event chosen per anchor
                                          witness: dict)      # (row, candidate) -> (lat, lon), site-free rows
reference_score(fails: i2[n], truth_index: int | None, n_cand: int)
      -> dict(seen_bf, seen_st, strict_recall, resolution, frac_strict, frac_bf)
      # truth_index is given only by the harness; frac_* (the narrowing) need no truth
```

**`tests/bessel_vec.py`** (I16's solar reference, A7) [r2v6 N3]:

```
local(elements: dict, lat: f8[m], lon: f8[m], dt_s: float)
      -> dict(smag, central, t_max_ut, sun_alt, c1_ut, c4_ut)    # arrays of length m; iterated maximum
site_free(elements, predicate, dt_s) -> (passes: bool, witness: (lat, lon) | None)
      # early exit: the greatest-eclipse point; then the central line, or the curve of closest
      # approach to the axis, every minute; then a 2-degree grid with the Sun up
check(n=1000, seed) -> dict(max_dmag, max_dt_s)      # against check_bessel.maxecl, before I16 runs
```

It reads NASA's elements from `data/jsex/`, never from `data/refs/`.
