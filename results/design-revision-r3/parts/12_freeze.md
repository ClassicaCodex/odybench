## 12. Freezing and amendments

Revision 1 hashed only `DESIGN.md` and `data/prereg/`, on a machine with no
version control, and it let every script run unfrozen. Nothing covered the
code, and nothing could refute a charge that thresholds or code had changed
after the results came in [rev #4]. The freeze is a local git commit, and
both rechecks found that resolved [r1 §1, #4; r2 §1, #4].

Revision 4 makes the freeze **two-stage** [r2 R2-1 fix 1]:

- **The first freeze, `prereg-1`.** It commits the design, the prereg files,
  the thresholds and all the code. It comes before any null, control or
  held-out result is computed.
- **The null-side stage.** The frozen code then computes only the null-side
  quantities, with the target masked.
- **The second freeze, `prereg-2`.** It commits those quantities. It comes
  before any target-side number is computed.

So the thresholds are frozen before the null side is known, as the recheck
asked. And the bench knows whether it could have said "yes" before it looks
at the target.

### 12.1 Before the first freeze (all must hold)

1. Every module of 10.2 exists and its unit tests pass.
2. The pre-freeze instrument checks pass: I1–I6, I8, I9(a), I13 and
   I14(a, b) (6.1).
3. **The re-draft** (6.3.4) is done, in order:
   - `tools/make_redraft_brief.py` has written
     `data/prereg/pcr_redraft_brief.json`, and I13(e) has passed on it;
   - the unexposed re-drafter has written `data/prereg/pcr_redraft.json`;
   - I2b has run after that, because I2b computes local magnitudes at the
     truth dates and must not run before the re-draft exists.
4. **The negatives' second reading** (6.5) is done. Its re-pinned readings
   and the X-class decision are in `negatives.json` and
   `operational_map.json` as recorded edits: a script that rebuilds from the
   licence-checked copy, like the licence checkers' own.
5. `data/prereg/operational_map.json` is complete and reviewed (I13).
6. **`data/prereg/deltat_circular.json`** lists every control eclipse used in
   SMH2016's and the 2020 Addendum's fits, with page locators (6.3.3).
7. **`data/prereg/almagest_regimes.json`** names the option and parameter
   values of both regimes for every projected row (6.4).
   - It shows the ceiling arithmetic of the leave-one-set-out tolerances.
   - It names each set's held-out rows.
   - It reproduces the known consequences of 2.6 (R9, R10).
8. **`data/prereg/slots.json`** holds the six slot variants of 4.2 with their
   sources, and the reported v6.
9. **`data/prereg/sibling_pairs.json`** lists the sourced conventions and the
   row pairs that state the same feature, with the excluded transplants. It
   is built without the truth (6.3.4).
10. **The three builders are retired.** Each would silently undo the licence
    checks' edits if re-run [lcr; lca; lcn §4.1]:
    - `results/controls-real-drafting/build_controls_real.py`;
    - `results/controls-almagest/build_prereg.py`;
    - `results/negatives/build_negatives.py`.

    The frozen JSON files are the record. The builders are kept for
    provenance, and are marked "do not re-run" in their first line by their
    owners or, failing that, listed here as retired. `tools/freeze.py`
    refuses to freeze if any of the three clue files differs from the output
    of its recorded edit scripts. Those are the licence checkers' replays from
    their saved pre-edit copies, followed, for the negatives, by the second
    reader's script.
11. The new prereg files exist: `sites.json`, `windows.json`, `seeds.json`,
    `deltat_models.json`, `slots.json`, `readings.json`, `garden.json`,
    `epic_grammar.json`, `heldout.json`, `eclipse_hit.json`,
    `verdict_rule.json`, `verdict_synthetic/`, `operational_map.json`,
    `pcr_redraft_brief.json`, `pcr_redraft.json`, `almagest_regimes.json`,
    `sibling_pairs.json`, `deltat_circular.json`, `truth_index.json` and
    `i2b_reference.json`.
12. `data/SHA256SUMS` is extended to every file in `data/text/` and
    `data/refs/`, and to the new ephemeris and catalogue files.
13. **No null result exists.** No survivor set, reach, G, held-out pass rate,
    control search or negative search has been computed by bench code.
    `freeze.py` checks that `results/` holds no output of the scripts of
    10.5. The design-stage estimates of 2.9 were computed by reviewers and by
    this revision's scratch scripts, not by bench code, and they are recorded
    as such.

### 12.2 The repository

- **Where.** `git init` in `C:\Projects\odybench` makes a local repository
  with no remote. Commits use the machine's existing git identity, and
  nothing is pushed.
- **Committed:**
  - `DESIGN.md`, `docs/`, `odybench/`, `tools/`, `tests/` and the top-level
    scripts;
  - `data/prereg/`, truth files included. The searcher's isolation is
    enforced by code and test, not by hiding files;
  - `data/stars.json` and `data/SHA256SUMS`;
  - the scripts in `results/` with their own text outputs, which record
    what was known before the freeze;
  - after the null-side stage, `results/attain/`.
- **Hashed, not committed** (listed in `data/SHA256SUMS`):
  - the ephemeris `.bsp` files and `data/jsex/`;
  - `data/text/*.tsv`, exported from Jon's library, some of them in
    copyright;
  - `data/refs/` (PDFs and their extracted text) and `data/cache/`;
  - every large binary in `results/`;
  - every copy of a publication kept in `results/`. Examples are the
    extracted texts `results/data-acquisition/bond2017.txt` and
    `results/controls-real-drafting/gautschy-eclipsecitations.txt`, and the
    PDFs and HTML in `results/unread-primaries/`.

  Nothing copyrighted enters the repository, so a later decision to publish
  it cannot publish a text by accident.

### 12.3 The two freezes

**The first freeze.** `py tools/freeze.py --stage 1`, run on a clean working
tree, does four things:

1. It checks every hash in `data/SHA256SUMS` and the conditions of 12.1.
2. It commits everything listed in 12.2 as the **freeze commit**, and tags
   it `prereg-1`.
3. It writes `PREREG.sha256` at the repository root. That file holds:
   - the freeze commit hash;
   - the git tree hashes of `odybench/`, `tools/`, `tests/` and
     `data/prereg/` at that commit (`git rev-parse prereg-1:odybench` and so
     on);
   - the blob hashes of `DESIGN.md` and of each top-level script;
   - a git-independent **code tree hash**: the SHA-256 of the sorted lines
     "`<sha256>  <path>`" over every file in `odybench/`, `tools/`, `tests/`,
     `data/prereg/`, `DESIGN.md` and the top-level scripts.
4. It commits `PREREG.sha256` alone in the next commit, because a file cannot
   hold the hash of the commit that contains it.

**The null-side stage.** `py attain.py` refuses to run unless HEAD descends
from `prereg-1`, the working tree is clean and the code tree hash matches.

- **The mask.** It builds every pool with `mask_target=True`. 16 Apr −1177
  is removed before any predicate is evaluated, and `clues.evaluate` raises
  if asked for it. I13(g) has checked both statically and at run time.
- **The checks.** It runs I7(a), I9(b, c) and I15(a) first, and stops if any
  fails.
- **The quantities.** It computes the null-side quantities of 9.1 and writes
  `results/attain/attain.json` and `attain.out.txt`.
- **I14(c).** It reruns the synthetic sets with the measured null side, and
  records three things:
  - whether S1 still returns {1}, which is Q_attain;
  - Q_tol and Q_slot;
  - the measured p_H,min.

**The second freeze.** `py tools/freeze.py --stage 2` does three things:

- it commits `results/attain/` and tags the commit `prereg-2`;
- it appends to `PREREG.sha256`, in the next commit, the `prereg-2` commit
  hash and the SHA-256 of `attain.json`;
- it prints the null-side record:
  - is outcome 1 attainable?
  - Q_tol;
  - Q_slot.

**After the second freeze.** Every later analysis script calls
`prereg.check_frozen(stage=2)` at start, and stops unless three things hold:

- HEAD descends from `prereg-2`;
- the working tree is clean;
- the current code tree hash equals the frozen one, or the latest
  amendment's.

`--unfrozen` lets a script run, but it stamps every output EXPLORATORY in its
first line, and `verdict.py` refuses to read such outputs.

**If the null side shows that outcome 1 is unattainable,** Q_attain records
it, and the rule is not changed. Any change would be an amendment made with
null-side outputs read, and would be marked so (12.4).

### 12.4 Amendments

A change to any frozen file after either freeze, code included, is allowed
only as a dated amendment appended to 12.6 below. The amendment states:

- what changed;
- why;
- the hash of the diff;
- **which outputs had already been read** when it was made, null-side ones
  included, in the way indusbench recorded its correction to test 1
  [indusbench DESIGN §4].

The amendment is committed, and its new code tree hash is appended to
`PREREG.sha256` under the old lines, so the file keeps the whole history.

The clue files' own histories are recorded the same way:

- `controls_real.json` was drafted and frozen before any accepted date was
  looked up (`eb1f0401…9256`). An agent blind to the truth then
  licence-checked it (`135fba67…83f8`) [lcr]. The recheck verified the hash
  [r2 §4].
- `controls_almagest.json` was licence-checked from the pre-edit file
  `e16c559d…37e9` [lca]. The checked file is `758ee789…4c83`.
- `negatives.json` was licence-checked from the copy in
  `results/license-check-negatives/negatives.before.json` [lcn]. The checked
  file is `f4ae3b26…bb00`.

These are the hashes as of this revision, and the recheck confirmed all three
[r2 §4]. If a pre-freeze task of 12.1 changes a file (the negatives' second
reading), `freeze.py` records the new hash with the script that made the
change.

### 12.5 Publishing the hash

Publishing the hash outside the machine would give an outside timestamp. Two
ways to do it are:

- a public commit or gist under the research identity Jon uses for open work;
- an OpenTimestamps proof of `PREREG.sha256`.

Publishing is **optional and needs Jon's explicit permission**, for each of
the two freezes. The bench does not assume it. Until he gives it, the freeze
is verifiable only on this machine, and `VERDICT.md` says so in its first
lines.

### 12.6 Amendments made after the freeze

None yet.

---

