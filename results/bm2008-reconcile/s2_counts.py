"""Counts from Table S2 (transcription data/bm2008-a/table_s2.tsv, identical
cell-for-cell to data/sources/bm2008-b/table_s2.tsv), plus arithmetic checks."""
import sys, math
sys.path.insert(0, '.')
from odybench import ephem as E
MON = {m: i+1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
def load():
    with open('data/bm2008-a/table_s2.tsv', encoding='utf-8') as f:
        L = [l.rstrip('\n') for l in f if l.strip() and not l.startswith('#')]
    h = L[0].split('\t'); out = []
    for l in L[1:]:
        c = l.split('\t'); c += [''] * (len(h) - len(c)); out.append(dict(zip(h, c)))
    return out
rows = load()
def jd(yb, s):
    d, m = s.split('-'); return E.jd_from_julian(1 - yb, MON[m], int(d))
def doy365(s):  # day-of-year ignoring 29 Feb
    d, m = s.split('-'); cum = [0,31,59,90,120,151,181,212,243,273,304,334]
    return cum[MON[m]-1] + int(d)
def secs(t):
    h, m, s = map(int, t.split(':')); return h*3600 + m*60 + s
W = [r for r in rows if 1115 <= int(r['year']) <= 1250]
print('rows total', len(rows), 'in 1250-1115 BC', len(W))
# arithmetic checks
bad11 = [r['year'] for r in rows if jd(int(r['year']), r['Ti']) - 11 != jd(int(r['year']), r['ti_m11'])]
print('Ti-11 column inconsistent with Ti (true Julian):', bad11)
bad11b = [r['year'] for r in rows if (doy365(r['Ti']) - 11) != doy365(r['ti_m11'])]
print('Ti-11 column inconsistent with Ti (365-day):', bad11b)
dtrue = {}; m365 = 0; mtrue = 0; leapdiff = []
for r in rows:
    yb = int(r['year'])
    t = jd(yb, r['Ti']) - 34 - jd(yb, r['mwra'])
    if r['mwra'] in ('', None): continue
    # MWRA may be in Jan..Apr, same year
    d365 = (doy365(r['Ti']) - 34) - doy365(r['mwra'])
    p = int(r['delta'])
    dtrue[yb] = int(t)
    m365 += (p == d365); mtrue += (p == t)
    if p != t: leapdiff.append((yb, p, int(t)))
print('delta printed == 365-day arithmetic:', m365, '/', len(rows), '; == true Julian:', mtrue)
print('rows where printed delta != true Julian delta (yearBC, printed, true):', leapdiff)
# venus
def vlead(r): return secs(r['diff']) if r['diff'] else None
for lab, S in (('1250-1115', W), ('all S2', rows)):
    morning = [r for r in S if r['diff']]
    O = [r for r in S if r['c_diff'] == 'O']; Y = [r for r in S if r['c_diff'] == 'Y']; y = [r for r in S if r['c_diff'] == 'y']
    print(f'[{lab}] Venus morning (non-blank) {len(morning)}; orange {len(O)}; yellow {len(Y)}; pale {len(y)}')
    if lab == '1250-1115':
        print('   min orange lead', min(vlead(r) for r in O)/60, 'max non-orange lead', max(vlead(r) for r in morning if r['c_diff'] != 'O')/60,
              'min yellow', min(vlead(r) for r in Y)/60, 'max white', max(vlead(r) for r in morning if r['c_diff'] == '')/60)
    print('   orange iff lead>=90min:', all((vlead(r) is not None and vlead(r) >= 5400) == (r['c_diff'] == 'O') for r in S))
    for k in (1, 2, 3):
        print(f'   Mercury |printed delta|<={k}:', sorted([int(r['year']) for r in S if abs(int(r['delta'])) <= k], reverse=True))
    print('   Mercury colours: O', sorted([int(r['year']) for r in S if r['c_delta']=='O'], reverse=True),
          'Y', sorted([int(r['year']) for r in S if r['c_delta']=='Y'], reverse=True),
          'y', sorted([int(r['year']) for r in S if r['c_delta']=='y'], reverse=True))
    print('   colour rule check (O<=1,Y=2,y=3):', all(({0:'O',1:'O',2:'Y',3:'y'}.get(abs(int(r['delta'])), '')) == r['c_delta'] for r in S))
    E15 = [r for r in S if MON[r['ti_m11'].split('-')[1]] == 4 and int(r['ti_m11'].split('-')[0]) <= 5]
    E14 = [r for r in S if MON[r['ti_m11'].split('-')[1]] == 4 and int(r['ti_m11'].split('-')[0]) <= 4]
    EX = [r for r in S if r['before'] == 'XXX']
    EO = [r for r in S if r['c_ti_m11'] == 'O']
    print(f'   Equinox: Ti-11 in 1-5 Apr {len(E15)}; 1-4 Apr {len(E14)}; XXX {len(EX)}; orange Ti-11 cell {len(EO)}; XXX==orange {set(map(id,EX))==set(map(id,EO))}')
    print('   max Ti-11 in table', max((jd(int(r["year"]), r['ti_m11']) - jd(int(r['year']), '1-Jan'), r['ti_m11']) for r in S)[1])
    print('   XXX iff Ti-11>=1 Apr:', all((r['before']=='XXX') == (jd(int(r['year']), r['ti_m11']) >= jd(int(r['year']), '1-Apr')) for r in S))
    V = {int(r['year']) for r in O}; M1 = {int(r['year']) for r in S if r['c_delta']=='O'}
    Ex5 = {int(r['year']) for r in E15}; EX6 = {int(r['year']) for r in EX}
    Vy = {int(r['year']) for r in S if r['c_diff'] in ('O','Y')}; M3 = {int(r['year']) for r in S if r['c_delta'] in ('O','Y','y')}
    print('   V&M', sorted(V & M1), '; V&E(1-5)', sorted(V & Ex5), '; V&E(XXX)', sorted(V & EX6), '; M&E(XXX)', sorted(M1 & EX6), '; V&M&E', sorted(V & M1 & EX6))
    print('   (V or Vyellow)&(M within 3)', sorted(Vy & M3, reverse=True), '; V & M within 2', sorted(V & {int(r["year"]) for r in S if abs(int(r["delta"]))<=2}, reverse=True))
    print('   year-cell colours non-white:', [(r['year'], r['c_year']) for r in S if r['c_year']])
    n = len(S); pv = len(O)/n; pm = len(M1)/n; pe = len(EX)/n
    lam = n*pv*pm
    print(f'   independence: E[V&M]={lam:.2f}, P(>=1)={1-math.exp(-lam):.2f}; E[V&M&E(XXX)]={n*pv*pm*pe:.3f}; E[V&M&E(1-5Apr)]={n*pv*pm*len(E15)/n:.3f}')
for yb in (1178, 1157, 1191, 1111, 1224, 1243, 1177, 1189):
    r = next(r for r in rows if int(r['year']) == yb)
    print(yb, {k: r[k] for k in ('Ti','venus_rise','sunrise','diff','mwra','delta','ti_m11','before','c_year','c_diff','c_delta','c_ti_m11')}, 'true delta', dtrue.get(yb))
