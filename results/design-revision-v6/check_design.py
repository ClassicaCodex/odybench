"""Design revision 6 scratch: mechanical checks of DESIGN.md.

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
    results/design-revision-v6/verdict_trace.py;
  * every 13-row reference "13 row n" names an existing row of section 13.
Run: py results/design-revision-v6/check_design.py
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
if sorted(nums) != list(range(1, 82)):
    missing = sorted(set(range(1, 82)) - set(nums))
    extra = sorted(set(nums) - set(range(1, 82)))
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
trace = Path("C:/Projects/odybench/results/design-revision-v6/verdict_trace.py").read_text(encoding="utf-8")
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
