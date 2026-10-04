# Leak scan for the public tier of DESIGN revision 5 (10.1).
# Reads the two truth files ONLY to build the list of accepted dates, then searches every
# file on the public whitelist (and the public copy of DESIGN.md, i.e. the text above the
# Appendix T marker) for those dates in the usual printed forms.
# Copied from results/critique-design-r1/v5/scan_public_leaks.py for the recheck of revision 6 (round 2); whitelist updated to DESIGN 10.1 of revision 6.
import json, re, sys, io, glob, os
sys.path.insert(0, 'C:/Projects/odybench')
from odybench import calendar as cal

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
R = 'C:/Projects/odybench/'
MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
MONFULL = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
           'September', 'October', 'November', 'December']

# ---- accepted dates (astronomical year, month, day, label)
dates = []
real = json.load(open(R + 'data/prereg/controls_real_truth.json', encoding='utf-8'))
pat_acc = re.compile(r'(\d{1,2})(?:/\d{1,2})? (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (?:(\d{1,4}) BC|AD (\d{1,4}))')
for s in real['sets']:
    for e in s.get('events', []):
        if not isinstance(e, dict) or not e.get('accepted'):
            continue
        m = pat_acc.search(e['accepted'])
        if not m:
            print('UNPARSED', s['set_id'], e['accepted']); continue
        d = int(m.group(1)); mo = MON.index(m.group(2)) + 1
        y = 1 - int(m.group(3)) if m.group(3) else int(m.group(4))
        dates.append((y, mo, d, f"{s['set_id']}:{e['event_id']}"))
alm = json.load(open(R + 'data/prereg/controls_almagest_truth.json', encoding='utf-8'))
for s in alm['sets']:
    for r in s.get('records', []):
        cd = r.get('civil_date_julian')
        if not cd:
            continue
        m = re.match(r'([+-]\d{4})-(\d{2})-(\d{2})', cd)
        dates.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), f"{s['set']}:{r['record']}"))
print(len(dates), 'accepted dates')

def forms(y, mo, d):
    out = set()
    mon, monf = MON[mo - 1], MONFULL[mo - 1]
    for sign in ('-', '\u2212'):
        ys = (sign if y < 0 else '+') + f"{abs(y):04d}"
        out.add(f"{ys}-{mo:02d}-{d:02d}")
        if y < 0:
            out.add(f"{sign}{abs(y)} {mon} {d}")
            out.add(f"{sign}{abs(y)}-{mo:02d}-{d:02d}")
            out.add(f"{sign}{abs(y):04d} {mon} {d}")
    if y <= 0:
        bc = 1 - y
        for mn in (mon, monf):
            out.add(f"{d} {mn} {bc} BC")
            out.add(f"{mn} {d}, {bc} BC")
            out.add(f"{mn} {d} {bc} BC")
            out.add(f"{bc} BC {mn} {d}")
            out.add(f"{bc} BC, {mn} {d}")
    else:
        for mn in (mon, monf):
            out.add(f"{d} {mn} AD {y}")
            out.add(f"{mn} {d}, AD {y}")
            out.add(f"AD {y} {mn} {d}")
            out.add(f"{y} {mn} {d}")
            out.add(f"+{y} {mn} {d}")
    jdn = cal.jdn_from_julian(y, mo, d)
    out.add(str(jdn)); out.add(str(jdn - 1)); out.add(f"{jdn - 0.5:.1f}")
    return out

# ---- public whitelist (DESIGN 10.1)
files = []
for p in ['docs/research-bm2008*.md', 'docs/research-chronology.md', 'docs/research-textclues.md',
          'docs/research-ephemeris.md', 'docs/research-visibility.md', 'docs/research_visibility_calc.py',
          'docs/research-window.md', 'docs/research-unread-primaries.md', 'docs/data-acquisition.md',
          'docs/controls-real-drafting.md', 'docs/license-check-controls-real.md',
          'docs/license-check-almagest.md', 'results/license-check-almagest/r2/license-check-almagest.r1.md',
          'docs/negatives-drafting.md', 'docs/license-check-negatives.md',
          'results/design-revision-v5/license-check-negatives-r2.relayed.md',
          'results/critique-design/check_bessel.py', 'results/critique-design/check_mwra.py',
          'results/bm2008-reconcile/check_mwra.py',
          'results/design-revision-r2/ranc_season.py', 'results/research-critiques/eclipse_local.py',
          'results/design-revision-v6/alm_rows.py', 'results/design-revision-v6/pcr_rows.py', 'results/design-revision-v6/verdict_trace.py',
          'data/prereg/*.json', 'data/stars.json', 'odybench/*.py', 'tools/*.py', 'tools/*.js', 'tests/*.py',
          'data/ephem/horizons/*.txt', 'docs/textclues-scripts/*']:
    for f in glob.glob(R + p):
        if 'truth' in os.path.basename(f):
            continue
        files.append(f)

texts = {}
for f in files:
    try:
        texts[f] = open(f, encoding='utf-8', errors='replace').read()
    except Exception as ex:
        print('cannot read', f, ex)
design = open(R + 'DESIGN.md', encoding='utf-8').read()
cut = design.index('<!-- APPENDIX-T')
texts['DESIGN.md (public part, above the Appendix T marker)'] = design[:cut]

hits = 0
for (y, mo, d, lab) in dates:
    for form in sorted(forms(y, mo, d)):
        for f, t in texts.items():
            # digits must not be part of a longer number
            for m in re.finditer(re.escape(form), t):
                a, b = m.start(), m.end()
                if (a > 0 and t[a - 1].isdigit()) or (b < len(t) and t[b].isdigit()):
                    continue
                ln = t.count('\n', 0, a) + 1
                ctx = t[max(0, a - 70):b + 50].replace('\n', ' ')
                print(f"HIT {lab} [{form}] {os.path.relpath(f, R) if os.path.exists(f) else f}:{ln}: ...{ctx}...")
                hits += 1
print('total hits', hits)

# year-only mentions (weaker: background knowledge) in every public-tier text and the public design
print('\n--- year-only mentions of control years in public-tier texts ---')
years = sorted(set(y for (y, _, _, _) in dates))
for f, t in texts.items():
    if f.endswith('.json') or '/data/ephem/' in f.replace('\\', '/'):
        continue
    for y in years:
        pats = [f"{1 - y} BC"] if y <= 0 else [f"AD {y}"]
        pats += [f"\u2212{abs(y)}", f"-{abs(y)}"] if y < 0 else [f"+{y}"]
        for p in pats:
            for m in re.finditer(re.escape(p), t):
                a, b = m.start(), m.end()
                if (a > 0 and t[a - 1].isdigit()) or (b < len(t) and t[b].isdigit()):
                    continue
                ln = t.count('\n', 0, a) + 1
                name = os.path.relpath(f, R) if os.path.exists(f) else f
                print(f"YEAR {y} [{p}] {name}:{ln}: ...{t[max(0, a - 60):b + 40].replace(chr(10), ' ')}...")
