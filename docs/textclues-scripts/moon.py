# Low-precision Sun/Moon (Meeus ch.25 / ch.47 main terms) for a sanity check only.
import math, sys
D2R = math.pi/180
def jd_julian(Y, M, D):
    if M <= 2: Y -= 1; M += 12
    return math.floor(365.25*(Y+4716)) + math.floor(30.6001*(M+1)) + D - 1524.5
def norm(x): return x % 360.0
def sun(T):
    L0 = 280.46646 + 36000.76983*T + 0.0003032*T*T
    M = 357.52911 + 35999.05029*T - 0.0001537*T*T
    C = (1.914602 - 0.004817*T - 0.000014*T*T)*math.sin(M*D2R) + (0.019993 - 0.000101*T)*math.sin(2*M*D2R) + 0.000289*math.sin(3*M*D2R)
    return norm(L0 + C), 0.0
# Meeus table 47.A (largest terms) : D, M, M', F, coeff(1e-6 deg)
LT = [(0,0,1,0,6288774),(2,0,-1,0,1274027),(2,0,0,0,658314),(0,0,2,0,213618),(0,1,0,0,-185116),(0,0,0,2,-114332),
      (2,0,-2,0,58793),(2,-1,-1,0,57066),(2,0,1,0,53322),(2,-1,0,0,45758),(0,1,-1,0,-40923),(1,0,0,0,-34720),
      (0,1,1,0,-30383),(2,0,0,-2,15327),(0,0,1,2,-12528),(0,0,1,-2,10980),(4,0,-1,0,10675),(0,0,3,0,10034),
      (4,0,-2,0,8548),(2,1,-1,0,-7888),(2,1,0,0,-6766),(1,0,-1,0,-5163),(1,1,0,0,4987),(2,-1,1,0,4036),(2,0,2,0,3994)]
BT = [(0,0,0,1,5128122),(0,0,1,1,280602),(0,0,1,-1,277693),(2,0,0,-1,173237),(2,0,-1,1,55413),(2,0,-1,-1,46271),
      (2,0,0,1,32573),(0,0,2,1,17198),(2,0,1,-1,9266),(0,0,2,-1,8822),(2,-1,0,-1,8216),(2,0,-2,-1,4324)]
def moon(T):
    Lp = 218.3164477 + 481267.88123421*T - 0.0015786*T*T + T**3/538841 - T**4/65194000
    D  = 297.8501921 + 445267.1114034*T - 0.0018819*T*T + T**3/545868 - T**4/113065000
    M  = 357.5291092 + 35999.0502909*T - 0.0001536*T*T + T**3/24490000
    Mp = 134.9633964 + 477198.8675055*T + 0.0087414*T*T + T**3/69699 - T**4/14712000
    F  = 93.2720950 + 483202.0175233*T - 0.0036539*T*T - T**3/3526000 + T**4/863310000
    E = 1 - 0.002516*T - 0.0000074*T*T
    sl = 0; sb = 0
    for d,m,mp,f,c in LT:
        a = (d*D+m*M+mp*Mp+f*F)*D2R; c = c*(E**abs(m)); sl += c*math.sin(a)
    for d,m,mp,f,c in BT:
        a = (d*D+m*M+mp*Mp+f*F)*D2R; c = c*(E**abs(m)); sb += c*math.sin(a)
    return norm(Lp + sl/1e6), sb/1e6
def obl(T):
    t = T/100
    return (84381.448 - 4680.93*t - 1.55*t*t + 1999.25*t**3 - 51.38*t**4)/3600
def eq(lam, beta, eps):
    l,b,e = lam*D2R, beta*D2R, eps*D2R
    ra = math.atan2(math.sin(l)*math.cos(e) - math.tan(b)*math.sin(e), math.cos(l))
    dec = math.asin(math.sin(b)*math.cos(e) + math.cos(b)*math.sin(e)*math.sin(l))
    return ra/D2R % 360, dec/D2R
def alt(jd_ut, dT, lat, lon, body):
    jd_tt = jd_ut + dT/86400
    T = (jd_tt - 2451545.0)/36525
    lam, beta = (sun if body=="sun" else moon)(T)
    ra, dec = eq(lam, beta, obl(T))
    Tu = (jd_ut - 2451545.0)/36525
    gmst = norm(280.46061837 + 360.98564736629*(jd_ut-2451545.0) + 0.000387933*Tu*Tu - Tu**3/38710000)
    H = (gmst + lon - ra)*D2R
    h = math.asin(math.sin(lat*D2R)*math.sin(dec*D2R) + math.cos(lat*D2R)*math.cos(dec*D2R)*math.cos(H))/D2R
    return h, lam
def elong(jd_tt):
    T = (jd_tt - 2451545.0)/36525
    ls,_ = sun(T); lm,bm = moon(T)
    return (lm - ls) % 360
if __name__ == "__main__":
    dT = 27603  # s, B&M's value
    lat, lon = 38.4, 20.7  # Ithaca (approx)
    tz = lon/15/24  # local mean time offset in days
    sys.stdout.reconfigure(encoding="utf-8")
    # find conjunction near -1177 Apr 16
    jd0 = jd_julian(-1177, 4, 16.0)
    lo, hi = jd0-3, jd0+3
    f = lambda j: ((elong(j)+180) % 360) - 180
    for _ in range(60):
        mid = (lo+hi)/2
        if f(lo)*f(mid) <= 0: hi = mid
        else: lo = mid
    conj_tt = (lo+hi)/2
    print(f"conjunction (TT) JD {conj_tt:.3f}; local mean time = JD_UT+{tz:.4f} -> local frac {(conj_tt - dT/86400 + tz + 0.5)%1*24:.2f} h")
    for (Y,M,Dd,label) in [(-1177,4,11,"night 11/12 Apr (B&M Day -5 seq)"),(-1177,4,12,"night 12/13 Apr (Day -4)"),(-1177,4,15,"night 15/16 Apr (Day -1)"),(-1177,3,18,"night 18/19 Mar (Day -29)"),(-1177,3,13,"13 Mar (Day -34)")]:
        base = jd_julian(Y,M,Dd) + 0.5 - tz   # local noon in UT
        # scan from local 12:00 to next 12:00
        sunset=sunrise=mrise=mset=None; prev=None
        for k in range(0, 24*60+1, 2):
            j = base + k/1440
            hs,_ = alt(j, dT, lat, lon, "sun"); hm,_ = alt(j, dT, lat, lon, "moon")
            if prev:
                if prev[0] > -0.833 >= hs: sunset = k
                if prev[0] < -0.833 <= hs: sunrise = k
                if prev[1] < 0.125 <= hm: mrise = k
                if prev[1] > 0.125 >= hm: mset = k
            prev = (hs, hm)
        e = elong(base + dT/86400 + 0.5)
        frac = (1 - math.cos(e*D2R))/2
        fmt = lambda k: None if k is None else f"{(12 + k/60) % 24:05.2f}h"
        print(f"{label}: elong(midnight) {e:6.1f} deg, illum ~{frac*100:4.1f}%, sunset {fmt(sunset)}, moonrise {fmt(mrise)}, moonset {fmt(mset)}, sunrise {fmt(sunrise)}  [local mean time]")
