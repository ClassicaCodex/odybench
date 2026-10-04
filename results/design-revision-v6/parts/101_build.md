### 10.1 Build plan

The build is done by agents in parallel. Each agent owns the files listed
for it, works to the interfaces of 10.2, and reads only what its tier allows
(below). The lead writes `odybench/model.py`, the shared types, first, and
it is frozen as the contract. Code inside the package runs as
`py -m odybench.x`, never as `py odybench/x.py`, because the file would
then shadow the standard library's `calendar` [acq §4].

**Three reading tiers** (since revision 5) [14.4 #57]. This design, several
dossier notes and every recheck carry the controls' accepted dates, or facts
measured at them. An agent who translates a control's prose into a predicate,
or builds the code that searches it, could be steered by them.

- **Truth tier:** A0, A6 and A11. Their tasks need the truth or the
  measured slack. They read this file in full. Their outputs are of three
  kinds:
  - mechanical: A0's regime file and projection file, built by rule;
  - truth-side by name: A11's `deltat_circular_truth.json`, A6's
    `i2b_truth.json`;
  - the harness, which is allowed to read the truth (A6).
- **Public tier:** A1, A2, A3, A4, A5, A7, A9 and A10. They work in
  `build/public/`, an exported directory, and read only the paths listed in
  `data/prereg/access.json`:
  - `build/DESIGN.public.md`, this file without Appendix T
    (`tools/public_design.py`; I13(h));
  - the code (`odybench/`, `tools/`, `tests/`);
  - `data/prereg/*.json` except `*truth*`, and `data/jsex/`, `data/ephem/`
    and `data/stars.json`;
  - **a text export, `build/public/text/`, in place of `data/text/`**
    [r1v5 N3]:
    - it holds whole files for the Odyssey (Greek, Murray, Butler), the
      Iliad, both scholia, Virgil, Apollonius, Quintus Smyrnaeus, Valerius
      Flaccus, Hesiod, Aratus, Geminus and Plutarch's *De facie*;
    - for every other file it holds only the rows that `negatives.json`
      cites (five rows of Pliny);
    - it holds **no row of Ptolemy's *Syntaxis*, and none of the historians
      of PC-R**. The Ptolemy rows state the Nabonassar year and Egyptian day
      of every *Almagest* record, which the clue file withholds; one line of
      arithmetic turns them into the truth. A3 needs only the clue files'
      operational fields, and A9 needs the negatives' texts and, for the
      sibling pairs, the licence words already in `controls_real.json`;
  - these notes: `docs/research-bm2008*.md`, `research-chronology.md`,
    `research-textclues.md`, `research-ephemeris.md`,
    `research-visibility.md` with `research_visibility_calc.py`,
    `research-window.md`, `research-unread-primaries.md`,
    `data-acquisition.md`, `controls-real-drafting.md`,
    `license-check-controls-real.md`, `license-check-almagest.md` and its
    round-1 copy, `negatives-drafting.md`, `license-check-negatives.md` and
    [lcn2];
  - by name, the reference scripts of 10.4 and of I2 in `results/`:
    `critique-design/check_bessel.py` and `check_mwra.py`,
    `bm2008-reconcile/check_mwra.py`, `design-revision-r2/ranc_season.py`,
    `research-critiques/eclipse_local.py` (the source of the `eclipses.py`
    port), and `design-revision-v6/alm_rows.py`, `pcr_rows.py` and
    `verdict_trace.py`. None of them holds a control's date [me: grep].

  Not on the list, because each carries a control's accepted date or a fact
  measured at it: `data/text/` itself, `docs/research-controls.md`,
  `docs/controls-almagest.md`, `docs/research-critiques.md` (it dates two of
  Thucydides' eclipses), `docs/critique-design*.md`, `docs/DESIGN-v*.md`,
  `data/ref*/`, and the rest of `results/`.

  `data-acquisition.md` stays on the list. One of the four Ithaca totalities
  it tabulates for −599..+300 is a control's date, but the table names no
  control. So it tells an agent no more than the background knowledge a
  language model already has [AppT 8; 13 row 50].
- **Brief tier:** A8 reads `data/prereg/pcr_redraft_brief.json` and nothing
  else (6.3.4).

**The order, so that the access record can hold** [r1v5 N9].

1. **Before any public-tier agent starts**, A0 writes `access.json`. A6 then
   writes `tools/public_design.py`, `tools/export_public.py` and
   `tools/check_access.py`, and produces `build/DESIGN.public.md` and
   `build/public/` from the current DESIGN.md. It records their SHA-256 in
   `build/public_served.log`. Revision 5 made the public copy at step 4,
   "from the frozen DESIGN.md", so its public agents had either the full
   design or none at step 1.
2. **Every later change** to DESIGN.md, or to a whitelisted file, does three
   things:
   - it regenerates both;
   - it appends the new hashes and the diff to the log;
   - it is announced to the public-tier agents.
3. **At the first freeze**, `freeze.py` checks that the public copy of the
   frozen DESIGN.md is the last copy served.
   - If it is not, the difference is listed.
   - Every public-tier agent whose code predates the difference re-checks
     its code against the frozen copy before the freeze completes (12.1).

**What the access check sees, and what it does not** [r1v5 N9].

- **The log.** The orchestrator's journal records every tool call of every
  agent:
  - file reads (Read, Grep, Glob) with their paths;
  - shell commands, in either shell, with their full command lines.
- **What `tools/check_access.py` flags:**
  - a file read outside the agent's whitelist;
  - a shell command line that names a path outside it;
  - a file-reading command (cat, type, Get-Content, grep, rg, findstr,
    Select-String, head, tail, sed, awk, less, more) applied outside
    `build/public/`;
  - a script the agent wrote or ran that names such a path.
- **What it cannot see:** a path an agent's code builds at run time, and
  what an agent remembers. The report says so.

**What the tiers protect, and what they do not** [r1v5 N3 fix 2].

- **For the two Ptolemy sets of PC-R the protection is weak.** The clue
  file's own statements, on the whitelist, name Mardokempados' and
  Hadrian's regnal years, and a language model can convert them. The
  Nabonassar epoch is common knowledge.
- **The real protections are mechanical:**
  - the searcher reads only operational fields (I13(c));
  - no search module names a set or a clue (I13(i));
  - an independent evaluator reproduces every gate count (I16);
  - the harness alone places the windows, from frozen seeds.
- **What the tiers do achieve:** no agent reads a truth file, or a
  truth-side computation, by accident; and the design's own truth-side
  facts stay out of the agents' copy.

| agent | tier | owns | depends on |
|---|---|---|---|
| A0 lead | truth | `odybench/model.py`; `data/prereg/access.json` (first, step 1 above); `sites.json` (with a span and a column set per site), `windows.json`, `seeds.json`, `deltat_models.json`, `slots.json` (4.2), `verdict_rule.json`; `tools/build_regimes.py` and its output `almagest_regimes.json` (6.4: options, parameters, held-out rows and their ceiling tolerances, all by rule); `tools/build_pcr_projection.py` and its output `pcr_projection.json` (6.3, by rule); `tools/disclosure_scan.py` and the draft of `heldout_disclosure.json` (7.1) | this design |
| A1 sky | public | `odybench/sky.py`, `odybench/events.py`, `tools/build_sky.py`, `tools/build_events.py`, `tools/validate_events.py` (I5, I6, I12), `tools/fetch_horizons_obs.py` (observer and geocentric tables for I5, I6(b), I15(b) and I10; it replaces revision 5's `fetch_horizons_rts.py`) | `model.py`, `ephem.py`, `calendar.py` |
| A2 eclipses | public | `odybench/eclipses.py`, `odybench/lunar.py` (with I4's convention check first), `odybench/deltat_mix.py`, `data/prereg/eclipse_hit.json`, `tools/build_eclipses.py`, `tools/validate_eclipses.py` (I2, I4), `tools/fetch_lecat.py`, `tests/test_eclipses.py`, `tests/test_lunar.py` | `model.py`, `ephem.py`, `data/jsex/` (I2b runs from A6's tool) |
| A3 clues | public | `odybench/prereg_io.py`, `odybench/clues.py` (with the target mask, 4.2), `odybench/search.py` (with the site-"none" shortcut, 6.3.1), the controls sections of `data/prereg/operational_map.json`, a draft of its negatives section (with round 2's new options, 6.5), a draft of `data/prereg/sibling_pairs.json` (6.3.4), `tools/make_redraft_brief.py`, `tests/test_clues.py`, `tests/test_prereg_io.py` | A1 and A2 interfaces |
| A4 garden | public | `odybench/readings.py` (with the joint options of 6.5), `odybench/pools.py` (slot family, the four held-out pools, the mask), `odybench/reach.py` (I9, with the block bootstrap), `odybench/evidence.py`, `data/prereg/garden.json`, `readings.json`, `attain.py` (the null-side stage, 12.3, with G_j and Q_record), `rates.py`, `coincidence.py`, `garden.py`, `windows.py` | A3; `odybench/heldout.py`'s interface |
| A5 epics and PC-S | public | `odybench/epic.py`, `odybench/pcs.py`, `data/prereg/epic_grammar.json`, `randomepic.py`, `synthetic.py` (I10, I10b) | A3, A4 |
| A6 harness and verdict | truth | `tools/public_design.py`, `tools/export_public.py`, `tools/check_access.py` (all first, step 1 above); `odybench/harness.py`, `tools/build_truth_index.py`, `tools/run_i2b.py` and `data/prereg/i2b_truth.json`, written from [ctl §3] [r1v5 N15d]; `controls.py`, `almagest.py`, `negatives.py`, `odybench/heldout.py` and the script `heldout.py` (7), `data/prereg/heldout.json`, `odybench/verdict_rule.py`, `verdict.py`, `read.py`, `odybench/stats.py`, `odybench/prereg.py`, `tools/freeze.py` (both stages), `tests/test_verdict.py` (I14), `tests/test_heldout.py`, `data/prereg/verdict_synthetic/` | all |
| A7 second implementations | public | `tests/bm_reference.py` (I7); `tests/heldout_reference.py` (I15(a), on `ephem` positions); `tests/mwra_reference.py` (I6(a)); `tests/control_reference.py` (I16) | `ephem.py`, `calendar.py`, the review's rise routine, NASA's `program.js`, the clue files' operational fields, `operational_map.json`, `pcr_projection.json`, `almagest_regimes.json`, and sections 3.2, 6.3, 6.4, 7.1, 7.2 and 10.3 of the public copy; no other bench module |
| A8 unexposed re-drafter | brief | `data/prereg/pcr_redraft.json` | `data/prereg/pcr_redraft_brief.json` only (6.3.4) |
| A9 second reader | public | the review of the negatives section of `operational_map.json`; the interval forks, caps and joint options; the literal pins, the X-class decision and the storm rule (6.5); the replay script of its edits; the review of `sibling_pairs.json` (6.3.4); the review of `heldout_disclosure.json` (7.1) | `negatives.json`, `controls_real.json`, `build/public/text/`, the public copy |
| A10 reproduction and ΔT | public | `reproduce.py`, `deltat.py`, `odybench/s2.py`, `tests/test_t0.py` | A1, A2 |
| A11 ΔT-fit reader | truth | `data/prereg/deltat_circular_truth.json` (6.3.3), with page locators into SMH2016 and the 2020 Addendum | the two papers and their supplementary tables; the truth files, to match a table entry to a control |

