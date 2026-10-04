## 12. Freezing and amendments

Revision 1 hashed only `DESIGN.md` and `data/prereg/`, on a machine with no
version control, and it let every script run unfrozen. Nothing covered the
code, and nothing could refute a charge that thresholds or code had changed
after the results came in [rev #4]. The freeze is now a local git commit.
The recheck found this resolved [r1 §1, #4]. Revision 3 changes only the
list of files.

### 12.1 Before the freeze (all must hold)

1. Every module of 10.2 exists and its unit tests pass.
2. The pre-freeze instrument checks I1–I6, I8, I9(a, b), I12, I13 and I14
   pass (6.1).
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
   values of both regimes for every projected row, with the
   leave-one-set-out arithmetic shown (6.4). It reproduces the known
   consequences of 2.6 (R9, R10).
8. **The three builders are retired.** Each would silently undo the licence
   checks' edits if re-run [lcr; lca; lcn §4.1]:
   - `results/controls-real-drafting/build_controls_real.py`;
   - `results/controls-almagest/build_prereg.py`;
   - `results/negatives/build_negatives.py`.

   The frozen JSON files are the record. The builders are kept for
   provenance and marked "do not re-run" in their first line by their owners
   or, failing that, listed here as retired. `tools/freeze.py` refuses to
   freeze if any of the three clue files differs from the output of its
   recorded edit scripts: the licence checkers' replays from their saved
   pre-edit copies, followed, for the negatives, by the second reader's
   script.
9. The new prereg files exist: `sites.json`, `windows.json`, `seeds.json`,
   `deltat_models.json`, `readings.json`, `garden.json`, `epic_grammar.json`,
   `heldout.json`, `eclipse_hit.json`, `verdict_rule.json`,
   `verdict_synthetic/`, `operational_map.json`, `pcr_redraft_brief.json`,
   `pcr_redraft.json`, `almagest_regimes.json`, `deltat_circular.json`,
   `truth_index.json`, `i2b_reference.json`.
10. `data/SHA256SUMS` is extended to every file in `data/text/` and
    `data/refs/`, and to the new ephemeris and catalogue files.
11. `tools/freeze.py` evaluates constraint C6 of 9.4 with the measured pool
    sizes, which are known from the sky tables before any null runs. It
    refuses to freeze if outcome 1 is unattainable [r1 N1 fix 3]. With the
    estimates of 2.8 it is attainable (U0(139) = 0.0265).

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
    what was known before the freeze.
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

### 12.3 The freeze

`tools/freeze.py`, run on a clean working tree:

1. checks every hash in `data/SHA256SUMS` and the conditions of 12.1;
2. commits everything listed above as the **freeze commit**, and tags it
   `prereg-1`;
3. writes `PREREG.sha256` at the repository root. It holds:
   - the freeze commit hash;
   - the git tree hashes of `odybench/`, `tools/`, `tests/` and
     `data/prereg/` at that commit (`git rev-parse prereg-1:odybench` and so
     on);
   - the blob hashes of `DESIGN.md` and of each top-level script;
   - a git-independent **code tree hash**: the SHA-256 of the sorted lines
     "`<sha256>  <path>`" over every file in `odybench/`, `tools/`, `tests/`,
     `data/prereg/`, `DESIGN.md` and the top-level scripts;
4. commits `PREREG.sha256` alone in the next commit, because a file cannot
   hold the hash of the commit that contains it.

Every analysis script calls `prereg.check_frozen()` at start. HEAD must
descend from `prereg-1`, the working tree must be clean, and the current
code tree hash must equal the frozen one or the latest amendment's.
Otherwise the script stops. `--unfrozen` lets it run, but it stamps every
output EXPLORATORY in its first line, and `verdict.py` refuses to read such
outputs.

### 12.4 Amendments

A change to any frozen file after the freeze, code included, is allowed only
as a dated amendment appended to 12.6 below. The amendment states:

- what changed;
- why;
- the hash of the diff;
- **which outputs had already been read** when it was made, in the way
  indusbench recorded its correction to test 1 [indusbench DESIGN §4].

The amendment is committed, and its new code tree hash is appended to
`PREREG.sha256` under the old lines, so the file keeps the whole history.

The clue files' own histories are recorded the same way:

- `controls_real.json` was drafted and frozen before any accepted date was
  looked up (`eb1f0401…9256`), then licence-checked by an agent blind to the
  truth (`135fba67…83f8`) [lcr];
- `controls_almagest.json` was licence-checked from the pre-edit file
  `e16c559d…37e9` [lca];
- `negatives.json` was licence-checked from the copy in
  `results/license-check-negatives/negatives.before.json` [lcn].

### 12.5 Publishing the hash

Publishing the hash outside the machine would give an outside timestamp. Two
ways to do it are a public commit or gist under the research identity Jon
uses for open work, and an OpenTimestamps proof of `PREREG.sha256`.
Publishing is **optional and needs Jon's explicit permission**, and the
bench does not assume it. Until he gives it, the freeze is verifiable only
on this machine, and `VERDICT.md` says so in its first lines.

### 12.6 Amendments made after the freeze

None yet.

---

