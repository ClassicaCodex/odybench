# Independent licence-string check of controls_real.json and controls_almagest.json (no truth file read).
# Each licence string is split on the ellipsis; every fragment must occur in the cited row's raw text,
# fragments in text order. Rows whose licence is a bracketed placeholder (withheld date words) are listed apart.
# Also scans every operational field for date-like content (years, BC/AD, JD-sized integers, month names).
import json, re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
R = 'C:/Projects/odybench/'
_cache = {}

def rows_of(tf):
    if tf not in _cache:
        d = {}
        for line in open(R + tf, encoding='utf-8'):
            k, _, t = line.rstrip('\n').partition('\t')
            d[k] = t
        _cache[tf] = d
    return _cache[tf]

def find_row(tf, ref):
    rows = rows_of(tf)
    if ref in rows:
        return rows[ref]
    # some files key rows by a short ref; try suffix match
    cands = [k for k in rows if k.endswith(ref) or k.endswith('.' + ref) or k.endswith(':' + ref)]
    if len(cands) == 1:
        return rows[cands[0]]
    return None

def check(clues, label):
    n = ok = 0
    placeholders = []
    for c in clues:
        lw = c.get('licence_words')
        lws = lw if isinstance(lw, list) else ([lw] if lw else [])
        tfs = c.get('text_file'); refs = c.get('ref')
        tfs = tfs if isinstance(tfs, list) else [tfs] * len(lws)
        refs = refs if isinstance(refs, list) else [refs] * len(lws)
        for one, tf, ref in zip(lws, tfs, refs):
            if one is None:
                continue
            if one.strip().startswith('['):
                placeholders.append(c['clue_id']); continue
            n += 1
            row = find_row(tf, ref) if tf and ref else None
            if row is None:
                print(f"{label} {c['clue_id']}: ROW NOT FOUND {tf} {ref}"); continue
            frags = [f.strip() for f in re.split(r'…|\.\.\.', one) if f.strip()]
            pos = 0; good = True
            for fr in frags:
                i = row.find(fr, pos)
                if i < 0:
                    j = row.find(fr)
                    print(f"{label} {c['clue_id']}: fragment {'OUT OF ORDER' if j >= 0 else 'MISSING'}: {fr[:80]!r}")
                    good = False
                else:
                    pos = i + len(fr)
            ok += good
    print(f"{label}: {ok}/{n} licence strings verified; {len(placeholders)} placeholder rows: {placeholders}")

def scan_ops(clues, label):
    pat = re.compile(r'\b(\d{3,4}\s*(BC|AD|BCE|CE)|(BC|AD)\s*\d{1,4}|[+\-\u2212]\d{3,4}\b|1[0-9]{6}(\.\d+)?|Nabonass|Thoth|Phaophi|Athyr|Choiak|Tybi|Mechir|Phamenoth|Pharmuthi|Pachon|Payni|Epiphi|Mesore|January|February|March|April|June|July|August|September|October|November|December)\b')
    for c in clues:
        for o in c.get('fork_options', []):
            s = json.dumps(o.get('operational', {}), ensure_ascii=False)
            for m in pat.finditer(s):
                print(f"{label} {c['clue_id']} option {o.get('option')}: date-like {m.group(0)!r} in {s[:160]}")
        for fld in ('statement',):
            s = c.get(fld, '') or ''
            for m in pat.finditer(s):
                print(f"{label} {c['clue_id']} {fld}: date-like {m.group(0)!r}: {s[:160]}")

alm = json.load(open(R + 'data/prereg/controls_almagest.json', encoding='utf-8'))
check(alm['clues'], 'ALM')
scan_ops(alm['clues'], 'ALM')
real = json.load(open(R + 'data/prereg/controls_real.json', encoding='utf-8'))
allc = []
for s in real['sets']:
    for c in s.get('clues', []):
        allc.append(c)
check(allc, 'REAL')
scan_ops(allc, 'REAL')
