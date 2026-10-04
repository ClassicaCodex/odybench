import re, html, math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT))
from odybench import ephem as E, calendar as C
NUM = re.compile(r"[-+]?\d+\.\d*(?:[eE][-+]?\d+)?|[-+]?\d+(?:[eE][-+]?\d+)?")
def elements(name):
    src = (ROOT / "data/jsex" / f"{name}.js").read_text()
    body = src.split("new Array(", 1)[1].rsplit(")", 1)[0]
    body = "\n".join(l.split("//")[0] for l in body.splitlines())
    vals = [float(v) for v in NUM.findall(body)]
    return [vals[i:i + 28] for i in range(0, len(vals), 28)]
for el in elements("SEm1199"):
    if abs(el[0] - 1291264.248) < 0.01:
        print(el)
t = (ROOT / "data/jsex/secat5/SE-1999--1900.html").read_text(encoding="latin-1")
t = html.unescape(re.sub(r"<[^>]+>", " ", t))
lines = [l for l in t.splitlines() if re.match(r"\s*\d{5}\s", l)]
print(len(lines)); print("\n".join(lines[:5]))
worst = []
for c in ["SEm1999", "SEm0599", "SEm0099", "SE0201"]:
    for el in elements(c):
        y, m, d, h = C.julian_from_jd(el[0])
        v = float(E.dt_em2006_canon(y + (m - 0.5) / 12))
        worst.append((round(abs(v - el[4]), 2), y, m, d, el[4], round(v, 2)))
worst.sort(reverse=True); print(worst[:6])
print("--- decimal-year conventions")
conv = {
 "mid-month y+(m-0.5)/12": lambda y, m, d, h: y + (m - 0.5) / 12,
 "y+(doy-1+h/24)/len": lambda y, m, d, h: y + (C.day_of_year(y, m, d) - 1 + h / 24) / C.days_in_year(y),
 "y+(m-1)/12+(d-1+h/24)/(12*mlen)": lambda y, m, d, h: y + (m - 1) / 12 + (d - 1 + h / 24) / (12 * C.days_in_month(y, m)),
}
allel = []
for c in [f"SEm{y:04d}" for y in range(1999, 0, -100)] + ["SE0001", "SE0101", "SE0201"]:
    allel += elements(c)
for name, f in conv.items():
    w = []
    for el in allel:
        y, m, d, h = C.julian_from_jd(el[0])
        v = float(E.dt_em2006_canon(f(y, m, d, h)))
        w.append(abs(v - el[4]))
    import numpy as np
    w = np.array(w)
    print(f"{name:40s} max {w.max():.3f}  p99 {np.percentile(w, 99):.3f}  mean {w.mean():.3f}  n>0.06 {int((w > 0.06).sum())}")
print("--- gamma debug")
def gamma_at(el):
    t = (el[0] - math.floor(el[0] - 0.5) - 0.5) * 24 - el[1]
    x = el[6] + t * (el[7] + t * (el[8] + t * el[9]))
    y = el[10] + t * (el[11] + t * (el[12] + t * el[13]))
    return t, math.copysign(math.hypot(x, y), y)
for el in elements("SEm1999")[:4]:
    print(el[:2], gamma_at(el))
