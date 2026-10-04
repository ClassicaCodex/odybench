"""Consistency checks on DESIGN.md (revision 2): escape sequences, dangling
section references, prediction references. Scratch script for the design
revision task; reads DESIGN.md only."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
s = open("DESIGN.md", encoding="utf-8").read()
bs = chr(92)
print("literal backslash-u sequences:", [m for m in re.findall(re.escape(bs) + "u[0-9a-fA-F]{4}", s)][:5])
secs = set(re.findall(r"^#+ (\d+(?:\.\d+)*)", s, re.M))
refs = set(re.findall(r"(?:section |sections |\(|, |; )(\d+\.\d+(?:\.\d+)?)\b", s))
missing = sorted(r for r in refs if r not in secs)
print("section refs not matching a heading:", missing)
pref = set(re.findall(r"\bP(\d+)\b", s))
pdef = set(re.findall(r"\*\*P(\d+)\.\*\*", s))
print("predictions defined:", len(pdef), "referenced but undefined:", sorted(pref - pdef, key=int))
iref = set(re.findall(r"\bI(\d+)b?\b", s))
print("instrument checks referenced:", sorted(iref, key=int))
