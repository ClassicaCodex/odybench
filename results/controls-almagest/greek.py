"""Locate a (possibly accent/prime-variant) Greek phrase inside a row and return the
EXACT original substring, so licence words are verbatim from the TSV."""
import unicodedata, re

PRIMES = "ʹ´΄'’`"


def _norm_with_map(s):
    out, idx = [], []
    s2 = s.replace("U+2220", "∠")
    # map positions of s2 back to s: build explicit map
    i = 0; back = []
    while i < len(s):
        if s.startswith("U+2220", i):
            back.append(i); i += 6
        else:
            back.append(i); i += 1
    for j, ch in enumerate(s2):
        for c in unicodedata.normalize("NFD", ch):
            if unicodedata.category(c) == "Mn":
                continue
            c = c.lower()
            if c in PRIMES:
                c = "'"
            if c == "ς":
                c = "σ"
            if c in "Ϛϛ":
                c = "ϛ"
            if c.isspace() or c in "·.,;-":
                c = " "
            if c == " " and out and out[-1] == " ":
                continue
            out.append(c); idx.append(back[j])
    return "".join(out), idx


def exact(row_text, phrase):
    """Return the original substring of row_text matching phrase modulo accents/primes/spacing, or None."""
    n, idx = _norm_with_map(row_text)
    p, _ = _norm_with_map(phrase)
    p = p.strip()
    k = n.find(p)
    if k < 0:
        return None
    a = idx[k]
    b = idx[k + len(p) - 1]
    # extend b to cover the full original character (incl. following combining marks / U+2220 token)
    end = b + 1
    if row_text.startswith("U+2220", b):
        end = b + 6
    while end < len(row_text) and unicodedata.category(row_text[end]) == "Mn":
        end += 1
    return row_text[a:end]
