import sys; sys.stdout.reconfigure(encoding='utf-8')
from local import lunar_moon_alt, fmt_h
def td(h,m,s): return (h + m/60 + s/3600)/24
L = [
 ('Thuc 7.50 -412 Aug 28','Syracuse',15.29,37.07,-412,8,28,1,15,33,15636),
 ('Xen Hell 1.6.1 -405 Apr 15','Athens',23.73,37.97,-405,4,15,23,33,23,15532),
 ('Plut Dion 24 -356 Aug 09','Zacynthus',20.90,37.78,-356,8,9,22,1,56,14791),
 ('Gaugamela -330 Sep 20','Arbela/Gaugamela',43.4,36.5,-330,9,20,22,24,32,14417),
 ('Polyb 5.78 -217 Sep 01','Mysia (approx.)',28.0,39.5,-217,9,1,20,0,56,12931),
 ('Livy 44.37 Pydna -167 Jun 21','Pydna',22.6,40.37,-167,6,21,22,4,14,12334),
 ('Xerxes alt lunar -478 Mar 14','Sardis',28.04,38.49,-478,3,14,6,55,55,16733),
 ('Alm IV.6 #1 -720 Mar 20','Babylon',44.42,32.54,-720,3,20,0,20,20,20529),
 ('Alm IV.6 #2 -719 Mar 09','Babylon',44.42,32.54,-719,3,9,2,32,11,20513),
 ('Alm IV.6 #3 -719 Sep 01','Babylon',44.42,32.54,-719,9,1,22,43,6,20506),
 ('Alm IV.11 #1 -382 Dec 23','Babylon',44.42,32.54,-382,12,23,9,15,28,15170),
 ('Alm IV.11 #2 -381 Jun 18','Babylon',44.42,32.54,-381,6,18,22,23,7,15162),
 ('Alm IV.11 #3 -381 Dec 13','Babylon',44.42,32.54,-381,12,13,0,15,56,15155),
 ('Alm IV.6 Ptol #1 133 May 06','Alexandria',29.92,31.20,133,5,6,23,20,42,9234),
 ('Alm IV.6 Ptol #2 134 Oct 20','Alexandria',29.92,31.20,134,10,20,23,16,55,9220),
 ('Alm IV.6 Ptol #3 136 Mar 06','Alexandria',29.92,31.20,136,3,6,4,5,42,9207),
 ('Josephus Herod -3 Mar 13','Jerusalem',35.23,31.78,-3,3,13,3,37,6,10562),
]
for lab, place, lon, lat, y, mo, d, h, mi, s, dTn in L:
    r = lunar_moon_alt(lon, lat, y, mo, d + td(h,mi,s), dTn)
    yy, mm, dd = r['ut']
    print(f"{lab:32s} | {place:18s} | greatest {yy} {mm:02d} {int(dd):02d} {fmt_h((dd%1)*24)} UT (NASA dT {dTn}s) | LMT {fmt_h(r['lmt_h'])} | moonEl={r['moon_el']:.1f} sunEl={r['sun_el']:.1f}")
