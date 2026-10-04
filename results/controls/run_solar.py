import sys
sys.stdout.reconfigure(encoding='utf-8')
from local import solar_local, fmt_h
def td(h,m,s): return (h + m/60 + s/3600)/24
E = [
 # label, place, lon, lat, y, mon, day, TDh,m,s, dT_nasa
 ('Odyssey/B&M -1177 Apr 16','Ithaca',20.72,38.37,-1177,4,16,17,57,28,28590),
 ('Odyssey/B&M dT=B&M 27602.7','Ithaca',20.72,38.37,-1177,4,16,17,57,28,27602.7),
 ('Assyrian eponym -762 Jun 15','Assur',43.26,35.46,-762,6,15,14,7,32,21211),
 ('Assyrian eponym -762 Jun 15','Nineveh',43.15,36.36,-762,6,15,14,7,32,21211),
 ('Archilochus -647 Apr 06','Thasos',24.71,40.78,-647,4,6,13,53,47,19364),
 ('Archilochus -647 Apr 06','Paros',25.15,37.08,-647,4,6,13,53,47,19364),
 ('Thales -584 May 28','Halys (approx. Kizilirmak crossing)',34.0,39.5,-584,5,28,19,28,50,18384),
 ('Thales alt -609 Sep 30','Halys (approx.)',34.0,39.5,-609,9,30,13,10,6,18764),
 ('Thales alt -602 May 18','Halys (approx.)',34.0,39.5,-602,5,18,12,4,25,18661),
 ('Hdt 9.10 -479 Oct 02','Isthmus of Corinth',22.98,37.93,-479,10,2,16,30,1,16741),
 ('Hdt 7.37 cand -479 Oct 02','Sardis',28.04,38.49,-479,10,2,16,30,1,16741),
 ('Hdt 7.37 cand -480 Apr 19','Sardis',28.04,38.49,-480,4,19,9,7,31,16766),
 ('Hdt 7.37 cand -477 Feb 17','Sardis',28.04,38.49,-477,2,17,14,37,28,16717),
 ('Pindar Pae.9 -462 Apr 30','Thebes',23.32,38.32,-462,4,30,16,32,38,16456),
 ('Thuc 2.28 -430 Aug 03','Athens',23.73,37.97,-430,8,3,19,20,15,15923),
 ('Thuc 4.52 -423 Mar 21','Athens',23.73,37.97,-423,3,21,12,18,6,15817),
 ('Ennius -399 Jun 21','Rome',12.49,41.89,-399,6,21,21,52,27,15437),
 ('Pelopidas -363 Jul 13','Thebes',23.32,38.32,-363,7,13,12,47,19,14894),
 ('Agathocles -309 Aug 15','Syracuse',15.29,37.07,-309,8,15,11,56,49,14127),
 ('Livy 37.4.4 -189 Mar 14','Rome',12.49,41.89,-189,3,14,10,29,38,12597),
 ('Livy 38.36.4 -187 Jul 17','Rome',12.49,41.89,-187,7,17,10,29,18,12569),
 ('Tarutius/Romulus -771 Jun 24','Rome',12.49,41.89,-771,6,24,14,24,39,21358),
 ('De facie 71 Mar 20','Chaeronea',22.84,38.49,71,3,20,11,58,48,9830),
 ('Ugarit cand -1222 Mar 05','Ugarit',35.78,35.60,-1222,3,5,18,48,58,29458),
 ('Ugarit cand -1374 May 03','Ugarit',35.78,35.60,-1374,5,3,13,52,19,32475),
 ('Mursili cand -1311 Jun 24','Hattusa',34.61,40.02,-1311,6,24,19,10,53,31203),
]
for lab, place, lon, lat, y, mo, d, h, mi, s, dTn in E:
    r = solar_local(lon, lat, y, mo, d + td(h,mi,s), dTn, dT_alt=dTn)
    a = r['horizons']; b = r['alt']
    def f(x): 
        yy, mm, dd = x['ut']; return f"{yy} {mm:02d} {int(dd):02d} {fmt_h((dd%1)*24)}UT"
    mu=lambda x: 'n/a' if x['magup'] is None else f"{x['magup']:.3f}"
    print(f"{lab:30s} | {place:22s} | dT_H={a['dT']:.0f}s max={a['mag']:.3f}{' TOTAL' if a['total'] else ''}{' EDGE' if a['edge'] else ''} sunUp={mu(a)} {f(a)} LMT {fmt_h(a['lmt_h'])} sunEl={a['sun_el']:.1f} | dT_NASA={b['dT']:.0f}s max={b['mag']:.3f}{' TOTAL' if b['total'] else ''} sunUp={mu(b)} LMT {fmt_h(b['lmt_h'])} sunEl={b['sun_el']:.1f}")
