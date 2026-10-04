"""Scratch reader for the negatives drafting task.

py tx.py show <file> <book.line>[-<line>]      print a range of rows
py tx.py grep <file> <regex> [book]            regex search (diacritics-insensitive for Greek)
Reads only data/text/*.tsv.
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT = ROOT / "data" / "text"


def load(name):
    rows = []
    with open(TEXT / name, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if "\t" not in line:
                continue
            ref, text = line.split("\t", 1)
            rows.append((ref, text))
    return rows


def short(ref):
    # strip CTS urn prefix
    m = re.match(r"urn:cts:[^:]+:(.*)", ref)
    if m:
        s = m.group(1)
        # tlg0001.tlg001.perseus-grc2.1.1 -> 1.1
        parts = s.split(".")
        # find edition token
        for i, p in enumerate(parts):
            if "perseus" in p or "grc" in p or "lat" in p:
                return ".".join(parts[i + 1:])
        return s
    return ref


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower().replace("ς", "σ")


def show(name, spec):
    rows = load(name)
    if "-" in spec:
        a, b = spec.split("-")
    else:
        a, b = spec, spec
    book, la = a.rsplit(".", 1)
    if "." in b:
        bookb, lb = b.rsplit(".", 1)
    else:
        bookb, lb = book, b
    on = False
    for ref, text in rows:
        s = short(ref)
        if "." not in s:
            continue
        bk, ln = s.rsplit(".", 1)
        if bk == book and ln == la:
            on = True
        if on:
            print(f"{s}\t{text}")
        if on and bk == bookb and ln == lb:
            break


def grep(name, pat, book=None):
    rows = load(name)
    rx = re.compile(norm(pat))
    for ref, text in rows:
        s = short(ref)
        if book and not s.startswith(book + "."):
            continue
        if rx.search(norm(text)):
            print(f"{s}\t{text}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1]
    if cmd == "show":
        show(sys.argv[2], sys.argv[3])
    elif cmd == "grep":
        grep(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
