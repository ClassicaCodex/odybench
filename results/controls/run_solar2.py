import sys
sys.stdout.reconfigure(encoding='utf-8')
from local import solar_local, fmt_h
def td(h,m,s): return (h + m/60 + s/3600)/24
E = [
 ('Xen Anab 3.4.8 -556 May 19','Larisa=Nimrud',43.33,36.10,-556,5,19,17,51,44,17958),
 ('Xen Hell 2.3.4 -403 Sep 03','Pherae (Thessaly)',22.75,39.38,-403,9,3,12,41,28,15495),
 ('Xen Hell 4.3.10 -393 Aug 14','Coronea (Boeotia)',22.96,38.36,-393,8,14,13,27,45,15342),
 ('Plut Dion 19.4 -360 May 12','Syracuse',15.29,37.07,-360,5,12,18,53,4,14852),
 ('Livy 22.1.9 -216 Feb 11','Rome',12.49,41.89,-216,2,11,17,39,22,12926),
 ('Livy 30.38.8 -202 May 06','Cumae',14.05,40.85,-202,5,6,16,47,22,12752),
 ('Pindar alt -487 Sep 01','Thebes',23.32,38.32,-487,9,1,10,39,47,16882),
 ('Thales at Miletus -584 May 28','Miletus',27.28,37.53,-584,5,28,19,28,50,18384),
]
for lab, place, lon, lat, y, mo, d, h, mi, s, dTn in E:
    r = solar_local(lon, lat, y, mo, d + td(h,mi,s), dTn, dT_alt=dTn)
    a = r['horizons']; b = r['alt']
    mu=lambda x: 'n/a' if x['magup'] is None else f"{x['magup']:.3f}"
    yy,mm,dd=a['ut']
    print(f"{lab:30s} | {place:18s} | dT_H={a['dT']:.0f}s max={a['mag']:.3f}{' TOTAL' if a['total'] else ''} sunUp={mu(a)} {yy} {mm:02d} {int(dd):02d} {fmt_h((dd%1)*24)}UT LMT {fmt_h(a['lmt_h'])} sunEl={a['sun_el']:.1f} | dT_NASA={b['dT']:.0f}s max={b['mag']:.3f}{' TOTAL' if b['total'] else ''} sunUp={mu(b)} LMT {fmt_h(b['lmt_h'])}")
