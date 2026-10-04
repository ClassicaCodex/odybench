"""Scratch (A0, truth tier): writes data/prereg/access.json (DESIGN 10.1, 7.1).

  * the whitelist of each reading tier (paths and globs, repository-relative);
  * the sealed list of 7.1, copied from data/prereg/heldout_disclosure.json's
    "sealed" block (which tools/disclosure_scan.py's sealed_list derives from
    the table's "constrains" facts), with a position anchor for every sealed
    line: the SHA-256 of the nearest unsealed line above it and its distance,
    so that the export (A6) can check that the line numbers still point at the
    same place.  No sealed line is hashed: a hash of a short line of numbers
    could be inverted by trying values;
  * the agent-to-tier map (A0..A11 and the integrator) and what each agent
    owns (10.1's table).

Run from C:\\Projects\\odybench:  py results/build-A0/make_access.py
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DISC = ROOT / "data" / "prereg" / "heldout_disclosure.json"
OUT = ROOT / "data" / "prereg" / "access.json"

NOTES = ["docs/research-bm2008.md", "docs/research-bm2008-a.md", "docs/research-bm2008-b.md",
         "docs/research-chronology.md", "docs/research-textclues.md", "docs/research-ephemeris.md",
         "docs/research-visibility.md", "docs/research_visibility_calc.py", "docs/research-window.md",
         "docs/research-unread-primaries.md", "docs/data-acquisition.md", "docs/controls-real-drafting.md",
         "docs/license-check-controls-real.md", "docs/license-check-almagest.md",
         "results/license-check-almagest/r2/license-check-almagest.r1.md", "docs/negatives-drafting.md",
         "docs/license-check-negatives.md",
         "results/design-revision-v5/license-check-negatives-r2.relayed.md"]
REFERENCE_SCRIPTS = ["results/critique-design/check_bessel.py", "results/critique-design/check_mwra.py",
                     "results/bm2008-reconcile/check_mwra.py", "results/design-revision-r2/ranc_season.py",
                     "results/research-critiques/eclipse_local.py", "results/design-revision-v8/alm_rows.py",
                     "results/design-revision-v8/verdict_trace.py", "results/design-revision-v7/pcr_rows.py"]

OWNS = {
    "A0": ["odybench/model.py", "tests/test_model.py", "data/prereg/access.json", "data/prereg/sites.json",
           "data/prereg/windows.json", "data/prereg/seeds.json", "data/prereg/deltat_models.json",
           "data/prereg/slots.json", "data/prereg/verdict_rule.json", "tools/build_regimes.py",
           "data/prereg/almagest_regimes.json", "tools/build_pcr_projection.py",
           "data/prereg/pcr_projection.json", "tools/disclosure_scan.py",
           "data/prereg/heldout_disclosure.json", "tests/test_build_regimes.py",
           "tests/test_build_pcr_projection.py", "tests/test_disclosure_scan.py", "tests/test_prereg_a0.py",
           "results/build-A0/**"],
    "A1": ["odybench/sky.py", "odybench/events.py", "tools/build_sky.py", "tools/build_events.py",
           "tools/validate_events.py", "tools/fetch_horizons_obs.py", "tests/test_events.py",
           "results/build-A1/**"],
    "A2": ["odybench/eclipses.py", "odybench/lunar.py", "odybench/deltat_mix.py", "data/prereg/eclipse_hit.json",
           "tools/build_eclipses.py", "tools/validate_eclipses.py", "tools/fetch_lecat.py",
           "tests/test_eclipses.py", "tests/test_lunar.py", "results/build-A2/**"],
    "A3": ["odybench/prereg_io.py", "odybench/clues.py", "odybench/search.py",
           "data/prereg/operational_map.json", "data/prereg/sibling_pairs.json", "tools/make_redraft_brief.py",
           "data/prereg/pcr_redraft_brief.json", "tests/test_clues.py", "tests/test_prereg_io.py",
           "results/build-A3/**"],
    "A4": ["odybench/readings.py", "odybench/pools.py", "odybench/reach.py", "odybench/evidence.py",
           "data/prereg/garden.json", "data/prereg/readings.json", "attain.py", "rates.py", "coincidence.py",
           "garden.py", "windows.py", "tests/test_reach.py", "results/build-A4/**"],
    "A5": ["odybench/epic.py", "odybench/pcs.py", "data/prereg/epic_grammar.json", "randomepic.py",
           "synthetic.py", "results/build-A5/**"],
    "A6": ["tools/public_design.py", "tools/export_public.py", "tools/check_access.py", "tools/run_i1.py",
           "odybench/harness.py", "tools/build_truth_index.py", "tools/run_i2b.py",
           "data/prereg/i2b_truth.json", "data/prereg/truth_index.json", "controls.py", "almagest.py",
           "negatives.py", "odybench/heldout.py", "heldout.py", "data/prereg/heldout.json",
           "odybench/verdict_rule.py", "verdict.py", "read.py", "odybench/stats.py", "odybench/prereg.py",
           "tools/freeze.py", "tests/test_verdict.py", "tests/test_heldout.py",
           "data/prereg/verdict_synthetic/**", "build/**", "results/instrument/**", "results/build-A6/**"],
    "A7": ["tests/bm_reference.py", "tests/heldout_reference.py", "tests/mwra_reference.py",
           "tests/control_reference.py", "tests/bessel_vec.py", "results/build-A7/**"],
    "A8": ["data/prereg/pcr_redraft.json"],
    "A9": ["data/prereg/operational_map.json (review of its negatives section)",
           "data/prereg/sibling_pairs.json (review)", "data/prereg/heldout_disclosure.json (review)",
           "results/build-A9/**"],
    "A10": ["reproduce.py", "deltat.py", "odybench/s2.py", "tests/test_t0.py", "results/build-A10/**"],
    "A11": ["data/prereg/deltat_circular_truth.json", "results/build-A11/**"],
    "integrator": ["any file, by merging the agents' work; no new content of its own"],
}
TIER = {"A0": "truth", "A6": "truth", "A11": "truth", "integrator": "truth",
        "A1": "public", "A2": "public", "A3": "public", "A4": "public", "A5": "public", "A7": "public",
        "A9": "public", "A10": "public", "A8": "brief"}


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def anchors(path: str, sealed_lines: list[int]) -> list[dict]:
    lines = (ROOT / path).read_text(encoding="utf-8", errors="replace").splitlines()
    sealed = set(sealed_lines)
    out = []
    for n in sorted(sealed):
        k = n - 1
        while k >= 1 and (k in sealed or not lines[k - 1].strip()):
            k -= 1
        out.append({"line": n, "anchor_line": k, "anchor_sha256": sha(lines[k - 1]) if k >= 1 else None,
                    "n_lines_in_file": len(lines)})
    return out


def main():
    disc = json.loads(DISC.read_text(encoding="utf-8"))
    sealed = disc["sealed"]
    sealed_lines = []
    for e in sealed["lines"]:
        sealed_lines.append({"path": e["path"], "lines": e["lines"], "anchors": anchors(e["path"], e["lines"])})
    sealed_file_sha = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sealed["files"]}

    public_read = (["build/DESIGN.public.md", "build/public/**",
                    "odybench/**", "tools/**", "tests/**",
                    "data/prereg/*.json", "data/prereg/verdict_synthetic/**",
                    "data/jsex/**", "data/ephem/**", "data/stars.json",
                    "data/bm2008-a/table_s2.tsv"]
                   + REFERENCE_SCRIPTS)
    public_deny = (["data/prereg/*truth*"]
                   + [p for p in sealed["files"] if p.startswith("data/")])
    acc = {
        "schema": "odybench access v1 (DESIGN 10.1, 7.1)",
        "written": "2026-10-04 by A0 (truth tier), before any public-tier agent starts (10.1 step 1)",
        "design": {"path": "DESIGN.md", "revision": 8,
                   "sha256": hashlib.sha256((ROOT / "DESIGN.md").read_bytes()).hexdigest()},
        "paths": "repository-relative, forward slashes; globs in fnmatch syntax where ** spans directories",
        "tiers": {
            "truth": {
                "agents": ["A0", "A6", "A11", "integrator"],
                "read": ["**"],
                "except": "the sealed list, before prereg-2",
                "note": "reads this design in full and the truth files its task needs (10.1)"},
            "public": {
                "agents": ["A1", "A2", "A3", "A4", "A5", "A7", "A9", "A10"],
                "read": public_read,
                "deny": public_deny,
                "default": "deny: a path matched by no read glob is off the whitelist",
                "deny_overrides_read": True,
                "notes_via_export": {p: f"build/public/{p}" for p in NOTES},
                "text_export": "build/public/text/ (in place of data/text/): whole files for the Odyssey "
                               "(Greek, Murray, Butler), the Iliad, both scholia, Virgil, Apollonius, Quintus "
                               "Smyrnaeus, Valerius Flaccus, Hesiod, Aratus, Geminus and Plutarch's De facie; "
                               "of every other file only the rows negatives.json cites and the six rows of the "
                               "re-draft (Thucydides 2.28.1, 2.47.1, 4.51.1, 4.52.1; Diodorus 20.5.5; Livy "
                               "38.36.4); no row of Ptolemy's Syntaxis and no other row of the PC-R historians",
                "shell_reads_only_under": "build/public/",
                "design_copy": "build/DESIGN.public.md (everything above Appendix T's marker line)",
                "note": "the notes and the reference scripts are read in the export, which masks the sealed "
                        "lines; data/bm2008-a/table_s2.tsv is added for A10's S2 replay (T0a, test_t0.py), "
                        "which 10.1's list omits; it holds B&M's Table S2 and no control truth"},
            "brief": {
                "agents": ["A8"],
                "read": ["data/prereg/pcr_redraft_brief.json"],
                "note": "reads nothing else in the repository (6.3.4)"},
        },
        "not_whitelisted": {
            "carry a control's accepted date or a fact measured at it": [
                "data/text/", "docs/research-controls.md", "docs/controls-almagest.md",
                "docs/research-critiques.md", "docs/critique-design*.md", "docs/DESIGN-v*.md", "data/ref*/",
                "the rest of results/"],
            "hold the target's sky (7.1)": "the sealed files below"},
        "sealed": {
            "until": "prereg-2",
            "applies_to": "every agent of every tier (7.1; tools/check_access.py flags a direct read)",
            "from": "data/prereg/heldout_disclosure.json, block 'sealed' (facts " + ", ".join(sealed["facts"])
                    + "; D4 is public by design)",
            "files": [{"path": p, "sha256": sealed_file_sha[p]} for p in sealed["files"]],
            "lines": sealed_lines,
            "globs": sealed["globs"],
            "export": "the public export omits the sealed files and serves each note with its sealed "
                      "lines masked (10.1, 7.1)",
            "unchecked": "code that reads a sealed file without printing it (tests/test_ephem.py, "
                         "tools/disclosure_scan.py), and what an agent remembers (7.1)"},
        "rules": [
            {"applies_to": "public", "rule": "read only the paths of tiers.public.read, less tiers.public.deny"},
            {"applies_to": "public", "rule": "a file-reading shell command (cat, type, Get-Content, grep, rg, "
                                             "findstr, Select-String, head, tail, sed, awk, less, more) "
                                             "applies only under build/public/"},
            {"applies_to": "all", "rule": "no direct read of a sealed path or line before prereg-2"},
            {"applies_to": "all", "rule": "do not run docs/research_visibility_calc.py as a script before "
                                          "prereg-2: its sections planets, mercury_events, bm_rates and "
                                          "herald recompute sealed facts D7 and D8 and write them to "
                                          "results/; importing its functions (the star routines of I6(c) "
                                          "and I10) is allowed"},
            {"applies_to": "all", "rule": "write only the files the agent owns (agents.<id>.owns); scratch "
                                          "work under results/build-<agent>/"},
        ],
        "agents": {a: {"tier": TIER[a], "owns": OWNS[a]} for a in
                   ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "integrator"]},
    }
    OUT.write_text(json.dumps(acc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(sealed['files'])} sealed files, "
          f"{sum(len(e['lines']) for e in sealed_lines)} sealed lines, {len(acc['agents'])} agents")


if __name__ == "__main__":
    main()
