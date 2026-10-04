  - A0 drafts the table from that list and from the published sources, and
    A9 checks it.
  - **Sealed values** [r2v6 N7]. Revision 6 promised that nobody would read
    a value the table marks "constrains" before the second freeze. But the
    public whitelist served two of them, D3's lines in two notes and D5's
    files in `data/ephem/`, and the access check could not see whether the
    promise was kept. Revision 7 makes it checkable for direct reads:
    - `access.json` holds a frozen **sealed list**: every line and file
      that the scan lists under a "constrains" fact. That is D3's lines of
      `docs/research-bm2008.md` and `docs/research-bm2008-b.md`, by line
      number; D5's files; and every output that prints their values:
      `results/validate_ephem.txt`, `results/data-acquisition/validate_ephem.*.txt`
      and I1's rerun in `results/instrument/`;
    - the public export omits the sealed files, and serves the two notes
      with the sealed lines masked;
    - `tools/check_access.py` flags a direct read of a sealed path by
      **any** agent, of either tier, before `prereg-2`;
    - I1's rerun runs from `tools/run_i1.py`, which prints only the check
      summary (6.1).
  - **What stays unchecked:** code that reads a sealed file without
    printing it, such as `tests/test_ephem.py`, and what an agent
    remembers. The report says so. H3's value at the target can change a
    label only if H4 contradicts the record (Q_contra): with H4 failing, no
    pass pattern reaches 0.05 (Q_record).
