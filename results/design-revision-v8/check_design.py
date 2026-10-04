"""Design revision 8 scratch (revision 7 script, extended): mechanical checks of DESIGN.md.

Revision 5's checks (results/design-revision-v5/check_design.py), kept:
  * every markdown table row has as many cells as its header;
  * code fences are balanced;
  * every section reference "(n.m)" points at an existing heading (known
    false positives, such as Thucydides 5.20.3 or a magnitude, are listed);
  * every prediction or expectation id cited outside sections 2.7, 8 and 14
    exists in section 8;
  * every [r2 R2-n] tag names an existing issue (1..12);
  * the Appendix T marker occurs exactly once, and every [AppT n] / [AppT n–m]
    names an existing "### Tn." heading below it (T2b counts as T2);
  * no hidden escape sequence (a backslash-u followed by four hex digits).
Changed or added for revision 6:
  * the issue numbers of section 14 run 1..81 without gaps;
  * every "[r1v5 Nn]" names an issue 1..15;
  * every qualifier the rule of 9.2 can print is defined in 1.3's table;
  * the synthetic sets named in 9.5's table are exactly those of
    results/design-revision-v8/verdict_trace.py;
  * every 13-row reference "13 row n" names an existing row of section 13.
Changed or added for revision 8 (section 14 now runs 1..102):
  * every "[r3v7 R3-n]" or "R3-n" names an issue 1..11, and "R3-n–R3-m"
    ranges stay inside it;
  * 9.2 prints Q_score3a and Q_score3b and no bare Q_score, and Q_attain4 is
    computed after label 4 and reads hit_hat_j, not E_j;
  * no table row names a qualifier "Q_score" outside sections 2.7, 14 and the
    history sentences that say it was split;
  * every results/design-revision-v8/ script the text cites exists, with its
    .out.txt where the text cites one;
  * the title says revision 8, and 14.7 exists with rows 92..102.
Added after the check of revision 8 [c8] (results/design-check-v8/):
  * no public wording about revision 7's P21 that rests on truth-side facts
    (public_inference.characterisation_hits finds nothing above the Appendix
    T marker), while Appendix T still states it;
  * the tag [c8] is defined in section 0, and 14.7 records the check.
Run: py results/design-revision-v8/check_design.py
"""
import re
from pathlib import Path

s = Path("C:/Projects/odybench/DESIGN.md").read_text(encoding="utf-8")
lines = s.split("\n")
problems = []

# tables
hdr = None
in_code = False
for i, l in enumerate(lines, 1):
    if l.startswith("```"):
        in_code = not in_code
        continue
    if in_code:
        continue
    t = l.strip()
    if t.startswith("|") and t.endswith("|"):
        cells = len(re.findall(r"(?<!\\)\|", t)) - 1
        if hdr is None:
            hdr = cells
        elif re.fullmatch(r"\|[\s:|-]+\|", t):
            pass
        elif cells != hdr:
            problems.append(f"l. {i}: table row has {cells} cells, header {hdr}")
    else:
        hdr = None
if in_code:
    problems.append("unbalanced code fence")

# headings
heads = set()
for l in lines:
    m = re.match(r"^#{2,4} (\d+(?:\.\d+){0,2})[. ]", l)
    if m:
        heads.add(m.group(1).rstrip("."))
KNOWN_NON_SECTIONS = {"5.20.3", "17.24", "1.5", "16.1", "0.25", "4.6.3", "1.9", "2.17"}
for i, l in enumerate(lines, 1):
    for m in re.finditer(r"\((\d{1,2}\.\d{1,2}(?:\.\d)?)(?:[,;)]| item| and)", l):
        ref = m.group(1)
        if ref in KNOWN_NON_SECTIONS:
            continue
        if ref not in heads and not re.search(r"\d\.\d+[°%]", m.group(0)):
            if not re.search(r"\(\d\.\d+–", l[m.start():m.start() + 12]):
                problems.append(f"l. {i}: section ({ref}) not found")

# predictions
sec8 = s[s.index("## 8. Pre-registered predictions"):s.index("## 9. The decision rule")]
defined = set(re.findall(r"\*\*(P\d+)\.\*\*", sec8)) | set(re.findall(r"^\| (R\d+) \|", sec8, re.M))
outside = s.replace(sec8, "")
outside = outside[:outside.index("### 2.7")] + outside[outside.index("### 2.8"):outside.index("## 14.")]
for m in re.finditer(r"\b([PR]\d{1,2})\b", outside):
    tok = m.group(1)
    ctx = outside[max(0, m.start() - 30):m.end() + 10].replace("\n", " ")
    if tok not in defined and tok not in ("R2",) and "revision 3's P" not in ctx and "v5 P" not in ctx:
        problems.append(f"undefined prediction/expectation {tok}: ...{ctx}...")

for m in re.finditer(r"R2-(\d+)", s):
    if not 1 <= int(m.group(1)) <= 12:
        problems.append(f"bad R2 issue {m.group(0)}")
for m in re.finditer(r"r1v5 N(\d+)", s):
    if not 1 <= int(m.group(1)) <= 15:
        problems.append(f"bad r1v5 issue {m.group(0)}")

# Appendix T
marker = "<!-- APPENDIX-T"
if s.count(marker) != 1:
    problems.append(f"Appendix T marker occurs {s.count(marker)} times")
else:
    app = s[s.index(marker):]
    tnums = set(int(x) for x in re.findall(r"^### T(\d+)b?\.", app, re.M))
    for m in re.finditer(r"\[AppT (\d+)(?:[–-](\d+))?", s):
        a = int(m.group(1)); b = int(m.group(2) or a)
        for k in range(a, b + 1):
            if k not in tnums:
                problems.append(f"[AppT {k}] has no heading T{k}")
    print(f"Appendix T items: {sorted(tnums)}")

# licence-check tags
for i, l in enumerate(lines, 1):
    if re.search(r"\[lca\]|\[lca |; lca\]|; lca;|\[lca;", l) and '"[lca]"' not in l:
        problems.append(f"l. {i}: bare [lca] tag")

# section 14 issue numbering
sec14 = s[s.index("## 14. Resolution of the reviews"):s.index("## Sources")]
nums = [int(x) for x in re.findall(r"^\| (\d+) \|", sec14, re.M)]
if sorted(nums) != list(range(1, 103)):
    missing = sorted(set(range(1, 103)) - set(nums))
    extra = sorted(set(nums) - set(range(1, 103)))
    problems.append(f"section 14 issue numbers: missing {missing}, extra {extra}, total {len(nums)}")
for m in re.finditer(r"14\.4 #(\d+)", s):
    if not 55 <= int(m.group(1)) <= 66:
        problems.append(f"bad 14.4 reference {m.group(0)}")

# qualifiers printed by 9.2 are defined in 1.3
sec92 = s[s.index("### 9.2 The rule"):s.index("### 9.3 How to read it")]
sec13 = s[s.index("### 1.3 Outcomes"):s.index("## 2. What is already known")]
quals = set(re.findall(r"qualifiers \+= (Q_\w+)", sec92))
for q in sorted(quals):
    qq = q.replace("Q_dT", "Q_ΔT")
    if f"| {qq} |" not in sec13:
        problems.append(f"qualifier {q} printed by 9.2 but not defined in 1.3")
print(f"qualifiers in 9.2: {sorted(quals)}")

# synthetic sets of 9.5 against the trace
sec95 = s[s.index("### 9.5 Synthetic input sets"):s.index("## 10. Software")]
sets_doc = set(re.findall(r"^\| \*{0,2}(S\d+[a-z]*)\*{0,2} \|", sec95, re.M))
trace = Path("C:/Projects/odybench/results/design-revision-v8/verdict_trace.py").read_text(encoding="utf-8")
sets_trace = set(re.findall(r'^    "(S\d+[a-z]*)": \(', trace, re.M))
if sets_doc != sets_trace:
    problems.append(f"9.5 sets {sorted(sets_doc)} differ from the trace {sorted(sets_trace)}")
print(f"synthetic sets: {len(sets_doc)} in 9.5, {len(sets_trace)} in the trace")

# 13-row references
sec13t = s[s.index("## 13. What the dossier could not settle"):s.index("## 14. Resolution of the reviews")]
rows13 = set(int(x) for x in re.findall(r"^\| (\d+) \|", sec13t, re.M))
for m in re.finditer(r"13 rows? (\d+)", s):
    if int(m.group(1)) not in rows13:
        problems.append(f"'{m.group(0)}' names no row of section 13")
print(f"section 13 rows: {min(rows13)}..{max(rows13)} ({len(rows13)})")

if re.search(r"\\u[0-9a-fA-F]{4}", s):
    problems.append("a backslash-u escape survives in the text")

print(f"{len(lines)} lines; {len(heads)} numbered headings")
print("\n".join(problems) if problems else "no problems found")

# revision 7: the recheck of revision 6 has issues N1..N10 [r2v6]
extra = []
for m in re.finditer(r"r2v6 N(\d+)", s):
    if not 1 <= int(m.group(1)) <= 10:
        extra.append(f"bad r2v6 issue {m.group(0)}")
for m in re.finditer(r"r2v6 N(\d+)[–-]N?(\d+)", s):
    if not (1 <= int(m.group(1)) <= 10 and 1 <= int(m.group(2)) <= 10):
        extra.append(f"bad r2v6 range {m.group(0)}")
# every part file was spliced in (no placeholder survives) and every new qualifier is printed by 9.2
for q in ("Q_attain3a", "Q_attain3b", "Q_exch"):
    if f"qualifiers += {q}" not in sec92:
        extra.append(f"{q} is not printed by 9.2")
print("revision-7 checks:", "\n".join(extra) if extra else "no problems found")

# revision 8: the recheck of revision 7 has issues R3-1..R3-11 [r3v7]
extra8 = []
for m in re.finditer(r"R3-(\d+)", s):
    if not 1 <= int(m.group(1)) <= 11:
        extra8.append(f"bad R3 issue {m.group(0)}")
for m in re.finditer(r"R3-(\d+)[–-]R3-(\d+)", s):
    if not (1 <= int(m.group(1)) < int(m.group(2)) <= 11):
        extra8.append(f"bad R3 range {m.group(0)}")
for q in ("Q_score3a", "Q_score3b", "Q_attain4"):
    if f"qualifiers += {q}" not in sec92:
        extra8.append(f"{q} is not printed by 9.2")
if re.search(r"qualifiers \+= Q_score\b(?!3)", sec92):
    extra8.append("9.2 still prints a bare Q_score")
i4 = sec92.find("labels += 4")
ia = sec92.find("qualifiers += Q_attain4")
if not (0 <= i4 < ia):
    extra8.append("Q_attain4 is not computed after label 4 in 9.2")
if "E_j[j]" in sec92 or "hit_hat_j[j]" not in sec92:
    extra8.append("Q_attain4 in 9.2 does not read hit_hat_j")
# bare "Q_score" in current text (history in 2.7 and 14 allowed, and sentences about the split)
cur = s[:s.index("### 2.7")] + s[s.index("### 2.8"):s.index("## 14. Resolution of the reviews")]
for i, l in enumerate(cur.split("\n"), 1):
    for m in re.finditer(r"Q_score(?![3a-z_])", l):
        if not re.search(r"split|replaced|single Q_score|one Q_score|Revision 6's Q_score|Q_score into", l):
            extra8.append(f"bare Q_score outside 2.7/14: ...{l.strip()[:120]}...")
# cited revision-8 scripts exist
v8 = Path("C:/Projects/odybench/results/design-revision-v8")
for m in set(re.findall(r"results/design-revision-v8/([\w.-]+)", s)):
    if not (v8 / m).exists():
        extra8.append(f"cited file results/design-revision-v8/{m} does not exist")
for m in set(re.findall(r"results/design-revision-v8/(\w+)\.py", s)):
    if not (v8 / f"{m}.out.txt").exists():
        extra8.append(f"no output beside results/design-revision-v8/{m}.py")
if not lines[0].startswith("# odybench — design (revision 8)"):
    extra8.append("title does not say revision 8")
sec147 = s[s.index("### 14.7 The recheck of revision 7"):s.index("## Sources")]
rows147 = [int(x) for x in re.findall(r"^\| (\d+) \|", sec147, re.M)]
if rows147 != list(range(92, 103)):
    extra8.append(f"14.7 rows are {rows147}")
print("revision-8 checks:", "\n".join(extra8) if extra8 else "no problems found")

# revision 8: every 9.5 row's labels and qualifiers equal the trace's output
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location(
    "vt8", "C:/Projects/odybench/results/design-revision-v8/verdict_trace.py")
_vt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_vt)
mism = []
for line in sec95.split("\n"):
    m = re.match(r"^\| \*{0,2}(S\d+[a-z]*)\*{0,2} \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", line)
    if not m:
        continue
    name, _diff, labels_txt, quals_txt = m.group(1), m.group(2), m.group(3), m.group(4)
    q = _vt.SETS[name][0]
    L, Q, _ = _vt.decide(q)
    lt = labels_txt.replace("*", "").strip()
    if L == "BLOCKED":
        ok_l = lt == "BLOCKED"
    else:
        doc_l = set(x.strip() for x in lt.strip("{}").split(",")) if lt.startswith("{") else {lt}
        ok_l = doc_l == set(L)
    qt = re.sub(r"\([^)]*\)", "", quals_txt.replace("*", ""))
    doc_q = set(t.replace("Q_ΔT", "Q_dT") for t in re.findall(r"Q_[\wΔ]+", qt))
    ok_q = doc_q == set(Q)
    if not (ok_l and ok_q):
        mism.append(f"{name}: 9.5 says {lt} / {sorted(doc_q)}; trace gives {sorted(L) if L != 'BLOCKED' else L} / {sorted(Q)}")
print("9.5 rows against the trace:", "\n".join(mism) if mism else "every label and qualifier agrees")

# after the check of revision 8 [c8]: no public wording about revision 7's P21 rests on truth-side facts
import sys as _sys  # noqa: E402
_sys.path.insert(0, "C:/Projects/odybench/results/design-revision-v8")
import public_inference as _PI  # noqa: E402
extra_c8 = []
_hits = _PI.characterisation_hits(s)
for h in _hits:
    if h[1] == "public":
        extra_c8.append(f"l. {h[0]}: public wording '{h[2]}' ({h[3]})")
if not any(h[1] == "AppT" and h[3] == "P21v7" for h in _hits):
    extra_c8.append("Appendix T no longer states the finding behind revision 7's P21")
if "| [c8] |" not in s:
    extra_c8.append("the tag [c8] is not defined in section 0")
if "**The check of revision 8** [c8]" not in sec147:
    extra_c8.append("14.7 does not record the check of revision 8")
print(f"check-of-revision-8 checks ({sum(h[1] == 'AppT' for h in _hits)} Appendix T hits kept):",
      "\n".join(extra_c8) if extra_c8 else "no problems found")
