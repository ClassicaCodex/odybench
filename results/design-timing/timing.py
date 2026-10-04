import sys, time
sys.path.insert(0, r"C:\Projects\odybench")
import numpy as np
from odybench import ephem as E
t0=time.time()
jd0=E.jd_from_julian(-1249,1,1); jd1=E.jd_from_julian(-1114,12,31)
nm=E.new_moons(jd0,jd1)
t1=time.time(); print("new_moons 136 yr:", len(nm), "%.1fs"%(t1-t0))
# one altaz call on 50k times (daily, 04:00 UT)
jds=np.arange(jd0, jd1, 1.0)+ (4/24)
t2=time.time()
alt,az=E.altaz("venus", jds, 38.37, 20.72, dt=28543.0)
t3=time.time(); print("venus altaz on %d times: %.1fs"%(len(jds), t3-t2))
alt,az=E.altaz("sun", jds, 38.37, 20.72, dt=28543.0)
t4=time.time(); print("sun altaz on %d times: %.1fs"%(len(jds), t4-t3))
# 1-min grid over one morning x 2000 days
g=(np.arange(0,240)/1440.0)
jj=(jds[:2000,None]+g[None,:]-2/24).ravel()
t5=time.time(); alt,az=E.altaz("venus", jj, 38.37, 20.72, dt=28543.0); t6=time.time()
print("venus altaz on %d times: %.1fs"%(len(jj), t6-t5))
