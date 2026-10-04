import sys, math
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moon import *
sys.stdout.reconfigure(encoding="utf-8")
dT=27603; lat,lon=38.4,20.7; tz=lon/15/24
# equinox: sun longitude 0 crossing in -1177 March/April (TT)
lo,hi = jd_julian(-1177,3,20), jd_julian(-1177,4,10)
g=lambda j: ((sun((j-2451545)/36525)[0]+180)%360)-180
for _ in range(60):
    m=(lo+hi)/2
    if g(lo)*g(m)<=0: hi=m
    else: lo=m
eq=(lo+hi)/2
fr=(eq - dT/86400 + tz + 0.5)
print("vernal equinox (computed): JD_TT %.3f -> Julian %s, LMT %.2f h" % (eq, "April %d" % (math.floor(fr - (jd_julian(-1177,4,1)+0.5)) + 1), (fr%1)*24))
def nightlen(Y,M,D):
    base = jd_julian(Y,M,D)+0.5-tz; ss=sr=None; prev=None
    for k in range(0,24*60+1,1):
        j=base+k/1440; h,_=alt(j,dT,lat,lon,"sun")
        if prev is not None:
            if prev>-0.833>=h: ss=k
            if prev<-0.833<=h: sr=k
        prev=h
    return (sr-ss)/60
for (M,D,lab) in [(12,15,"15 Dec"),(10,15,"15 Oct"),(11,15,"15 Nov"),(3,18,"18 Mar"),(4,11,"11 Apr"),(4,16,"16 Apr"),(6,15,"15 Jun")]:
    Y = -1177
    print(f"night length {lab} {Y}: {nightlen(Y,M,D):.2f} h (sun centre+refraction, -0.833 deg)")
