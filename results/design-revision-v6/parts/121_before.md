### 12.1 Before the first freeze (all must hold)

1. Every module of 10.2 exists and its unit tests pass.
2. The pre-freeze instrument checks pass: I1, I2, I4 (after its convention
   check on three pages), I5, I6, I8, I9(a), I13 and I14(a, b), with I2b
   after the re-draft (item 3). I3 and I12 have run and are reported (6.1).
3. **The re-draft** (6.3.4) is done, in order:
   - `tools/make_redraft_brief.py` has written
     `data/prereg/pcr_redraft_brief.json`, and I13(e) has passed on it;
   - the unexposed re-drafter has written `data/prereg/pcr_redraft.json`;
   - I2b has run after that, because I2b computes local magnitudes at the
     truth dates and must not run before the re-draft exists. It runs from
     `tools/run_i2b.py`, which writes only `results/instrument/i2b_truth_check.json`,
     so it is not an output of a 10.5 script [r1v5 N9].
4. **The negatives' second reading** (6.5) is done. Its re-pinned readings
   (VF-COLCHIS-01 among them), the X-class decision, the joint options of
   the linked rows and the storm rule are in `negatives.json` and
   `operational_map.json` as recorded edits: a script that rebuilds from the
   licence-checked copy, like the licence checkers' own.
5. `data/prereg/operational_map.json` is complete and reviewed (I13).
6. **`data/prereg/deltat_circular_truth.json`** lists every control eclipse used in
   SMH2016's and the 2020 Addendum's fits, with page locators (6.3.3).
7. **`data/prereg/almagest_regimes.json`** names the option and parameter
   values of both regimes for every projected row, and the ceiling
   tolerances of every held-out row (6.4). `tools/build_regimes.py` writes
   it by rule.
   - It shows the ceiling arithmetic of the leave-one-set-out tolerances,
     for the greatest-elongation rows and for the held-out rows.
   - It names each set's projection and held-out rows, which must equal the
     lists of `results/design-revision-v6/alm_rows.out.txt` (I13(f)).
   - It reproduces the known consequences of 2.6 (R9, R10).
8. **`data/prereg/pcr_projection.json`** names, for every row of the nine
   PC-R sets, its option under the as-licensed and the words-only
   projections (6.3). `tools/build_pcr_projection.py` writes it by rule, and
   it must equal `results/design-revision-v6/pcr_rows.out.txt` (I13(f))
   [r1v5 N7].
9. **`data/prereg/heldout_disclosure.json`** (7.1) [r1v5 N2]:
   - `tools/disclosure_scan.py` has listed every file in `docs/`, `results/`
     and `data/` that holds a quantity of the target's sky between Day −40
     and Day +1, by name, date and quantity code, without values;
   - A0 has drafted the table from that list and the published sources,
     with a `determined` field per predicate;
   - A9 has checked it;
   - nobody has read a value that the table marks "constrains".
10. **`data/prereg/slots.json`** holds the six slot variants of 4.2 with
    their sources, and the reported v6.
11. **`data/prereg/sibling_pairs.json`** lists the sourced conventions and
    the row pairs that state the same feature, with the excluded
    transplants. It is built without the truth (6.3.4).
12. **The three builders are retired.** Each would silently undo the licence
    checks' edits if re-run [lcr; lca1 item 1; lca2 item 2; lcn §4.1; lcn2
    problem 3]:
    - `results/controls-real-drafting/build_controls_real.py`;
    - `results/controls-almagest/build_prereg.py`;
    - `results/negatives/build_negatives.py`.

    The frozen JSON files are the record. The builders are kept for
    provenance, and are marked "do not re-run" in their first line by their
    owners or, failing that, listed here as retired. `tools/freeze.py`
    refuses to freeze if any of the three clue files differs from the output
    of its recorded edit scripts. Those are the licence checkers' replays from
    their saved pre-edit copies, followed, for the negatives, by the second
    reader's script:
    - `controls_real.json`: `results/license-check-controls-real/apply_license_check.py`
      on `controls_real.before-license-check.json`;
    - `controls_almagest.json`: `results/license-check-almagest/apply_edits.py`
      on `controls_almagest.before.json` (round 1), then
      `results/license-check-almagest/r2/apply_edits_r2.py` on
      `r2/controls_almagest.pre_r2.json` (round 2);
    - `negatives.json`: `results/license-check-negatives/apply_edits.py` on
      `negatives.before.json` (round 1), then
      `results/license-check-negatives/r2/apply_edits_r2.py` on
      `r2/negatives.r2-before.json` (round 2), then the second reader's
      script.
13. The new prereg files exist: `sites.json`, `windows.json`, `seeds.json`,
    `deltat_models.json`, `slots.json`, `readings.json`, `garden.json`,
    `epic_grammar.json`, `heldout.json`, `heldout_disclosure.json`,
    `eclipse_hit.json`, `verdict_rule.json`, `verdict_synthetic/`,
    `operational_map.json`, `pcr_projection.json`, `pcr_redraft_brief.json`,
    `pcr_redraft.json`, `almagest_regimes.json`, `sibling_pairs.json`,
    `deltat_circular_truth.json`, `truth_index.json`, `i2b_truth.json` and
    `access.json`.
14. `data/SHA256SUMS` is extended to every file in `data/text/` and
    `data/refs/`, and to the new ephemeris and catalogue files.
15. **No null result exists.** No survivor set, reach, G, held-out pass rate,
    control search or negative search has been computed by bench code.
    - `freeze.py` checks that `results/` holds no output of the scripts of
      10.5.
    - Instrument outputs in `results/instrument/` are allowed and are
      committed. They are comparisons of code paths, not null results.
    - The design-stage estimates of 2.9 were computed by reviewers and by
      the revisions' scratch scripts, not by bench code, and they are
      recorded as such.
16. **The public copy and the access record** (10.1) [r1v5 N9]:
    - the public copy of the frozen `DESIGN.md` equals the last copy served
      (`build/public_served.log`), or every difference has been listed and
      re-checked by the agents whose work predates it;
    - I13(h) has passed on both the copy and the text export;
    - every public-tier agent's logged tool calls have been compared with
      `access.json`;
    - the logs are committed with the code.

