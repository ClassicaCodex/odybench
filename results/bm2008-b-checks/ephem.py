# Low-precision check ephemeris (computed by me): Standish "Keplerian Elements for Approximate Positions
# of the Major Planets", Table 2a (3000 BC - 3000 AD), J2000 ecliptic; IAU1976 precession (Meeus ch.21);
# GMST Meeus 12.4. Good to roughly arcminutes for the inner planets - enough to locate extrema to ~1 day.
import math
R=math.radians; D=math.degrees
EL = {  # a, e, I, L, varpi, Omega ; rates per Julian century
 'mercury': ((0.38709843,0.20563661,7.00559432,252.25166724,77.45771895,48.33961819),
             (0.0,0.00002123,-0.00590158,149472.67486623,0.15940013,-0.12214182)),
 'venus':   ((0.72332102,0.00676399,3.39777545,181.97970850,131.76755713,76.67261496),
             (-0.00000026,-0.00005107,0.00043494,58517.81560260,0.05679648,-0.27274174)),
 'emb':     ((1.00000018,0.01673163,-0.00054346,100.46691572,102.93005885,-5.11260389),
             (-0.00000003,-0.00003661,-0.01337178,35999.37306329,0.31795260,-0.24123856)),
}
def helio(p, T):
    (a,e,I,L,w,O),(da,de,dI,dL,dw,dO) = EL[p]
    a+=da*T; e+=de*T; I+=dI*T; L+=dL*T; w+=dw*T; O+=dO*T
    om=w-O; M=(L-w+180)%360-180
    E=R(M)+e*math.sin(R(M))
    for _ in range(30):
        dE=(R(M)-(E-e*math.sin(E)))/(1-e*math.cos(E)); E+=dE
        if abs(dE)<1e-12: break
    xp=a*(math.cos(E)-e); yp=a*math.sqrt(1-e*e)*math.sin(E)
    co,so=math.cos(R(om)),math.sin(R(om)); cO,sO=math.cos(R(O)),math.sin(R(O)); cI,sI=math.cos(R(I)),math.sin(R(I))
    x=(co*cO-so*sO*cI)*xp+(-so*cO-co*sO*cI)*yp
    y=(co*sO+so*cO*cI)*xp+(-so*sO+co*cO*cI)*yp
    z=(so*sI)*xp+(co*sI)*yp
    return x,y,z
def julian_jd(y,m,d):  # Julian calendar, astronomical year, d may be fractional; returns JD
    if m<=2: y-=1; m+=12
    return math.floor(365.25*(y+4716))+math.floor(30.6001*(m+1))+d-1524.5
EPS0=R(23.4392911)
def geo_eq_j2000(p, jd_tt, lt=True):
    T=(jd_tt-2451545.0)/36525
    ex,ey,ez=helio('emb',T)
    if p=='sun':
        x,y,z=-ex,-ey,-ez
    else:
        px,py,pz=helio(p,T); x,y,z=px-ex,py-ey,pz-ez
        if lt:
            dist=math.sqrt(x*x+y*y+z*z); T2=T-dist*0.0057755183/36525
            px,py,pz=helio(p,T2); x,y,z=px-ex,py-ey,pz-ez
    # ecliptic J2000 -> equatorial J2000
    xe=x; ye=y*math.cos(EPS0)-z*math.sin(EPS0); ze=y*math.sin(EPS0)+z*math.cos(EPS0)
    lam=math.atan2(y,x)
    return xe,ye,ze,lam
def precess(xe,ye,ze,jd_tt):
    T=(jd_tt-2451545.0)/36525
    zeta=R((2306.2181*T+0.30188*T*T+0.017998*T**3)/3600)
    zz  =R((2306.2181*T+1.09468*T*T+0.018203*T**3)/3600)
    th  =R((2004.3109*T-0.42665*T*T-0.041833*T**3)/3600)
    a=math.atan2(ye,xe); r=math.sqrt(xe*xe+ye*ye+ze*ze); d=math.asin(ze/r)
    A=math.cos(d)*math.sin(a+zeta)
    B=math.cos(th)*math.cos(d)*math.cos(a+zeta)-math.sin(th)*math.sin(d)
    C=math.sin(th)*math.cos(d)*math.cos(a+zeta)+math.cos(th)*math.sin(d)
    return (math.atan2(A,B)+zz)%(2*math.pi), math.asin(C)
def gmst_deg(jd_ut):
    T=(jd_ut-2451545.0)/36525
    return (280.46061837+360.98564736629*(jd_ut-2451545.0)+0.000387933*T*T-T**3/38710000)%360
def radec_date(p, jd_tt):
    xe,ye,ze,lam=geo_eq_j2000(p,jd_tt); return precess(xe,ye,ze,jd_tt)
def altaz(p, jd_ut, dt_s, lat, lon):
    jd_tt=jd_ut+dt_s/86400
    ra,dec=radec_date(p,jd_tt)
    H=R(gmst_deg(jd_ut)+lon)-ra
    phi=R(lat)
    alt=math.asin(math.sin(phi)*math.sin(dec)+math.cos(phi)*math.cos(dec)*math.cos(H))
    az=math.atan2(math.sin(H), math.cos(H)*math.sin(phi)-math.tan(dec)*math.cos(phi))  # from south, westward
    return D(alt), (D(az)+180)%360  # azimuth from north, eastward
def ecl_lon_date(p, jd_tt):
    xe,ye,ze,_=geo_eq_j2000(p,jd_tt); ra,dec=precess(xe,ye,ze,jd_tt)
    T=(jd_tt-2451545.0)/36525
    eps=R(23.4392911-(46.8150*T+0.00059*T*T-0.001813*T**3)/3600)
    lam=math.atan2(math.sin(ra)*math.cos(eps)+math.tan(dec)*math.sin(eps), math.cos(ra))
    return D(lam)%360
def rise(p, jd0_ut_localmidnight, dt_s, lat, lon, h0):
    # find rising (alt crosses h0 upward) within the 24 h after jd0
    step=1/288; prev=altaz(p,jd0_ut_localmidnight,dt_s,lat,lon)[0]-h0
    for i in range(1,289):
        t=jd0_ut_localmidnight+i*step; cur=altaz(p,t,dt_s,lat,lon)[0]-h0
        if prev<0<=cur:
            a,b=t-step,t
            for _ in range(40):
                m=(a+b)/2
                if altaz(p,m,dt_s,lat,lon)[0]-h0<0: a=m
                else: b=m
            return (a+b)/2
        prev=cur
    return None
