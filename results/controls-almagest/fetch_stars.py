"""Fetch Hipparcos new-reduction (van Leeuwen 2007, VizieR I/311/hip2) astrometry
for the stars named in the Almagest records, plus SIMBAD radial velocities.
Writes results/controls-almagest/stars.json (scratch)."""
import json, sys, urllib.request, urllib.parse
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
STARS = {  # HIP: (key, name)
    21421: ("aldebaran", "alpha Tau (Aldebaran)"), 49669: ("regulus", "alpha Leo (Regulus)"),
    65474: ("spica", "alpha Vir (Spica)"), 80763: ("antares", "alpha Sco (Antares)"),
    78820: ("beta1_sco", "beta1 Sco (northern forehead)"), 78401: ("delta_sco", "delta Sco (middle of forehead)"),
    107556: ("delta_cap", "delta Cap"), 25428: ("beta_tau", "beta Tau (Elnath)"), 26451: ("zeta_tau", "zeta Tau"),
    36850: ("castor", "alpha Gem (Castor)"), 37826: ("pollux", "beta Gem (Pollux)"),
    72622: ("alpha2_lib", "alpha2 Lib"), 34088: ("zeta_gem", "zeta Gem"), 35550: ("delta_gem", "delta Gem"),
    35350: ("lambda_gem", "lambda Gem"), 57757: ("beta_vir", "beta Vir"), 60129: ("eta_vir", "eta Vir"),
    61941: ("gamma_vir", "gamma Vir"), 42911: ("delta_cnc", "delta Cnc (Asellus Australis)"),
    8832: ("gamma2_ari", "gamma2 Ari"), 112961: ("lambda_aqr", "lambda Aqr"), 114724: ("phi_aqr", "phi Aqr"),
    114341: ("chi_aqr", "chi Aqr"), 114855: ("psi1_aqr", "psi1 Aqr"), 115033: ("psi2_aqr", "psi2 Aqr"),
    115115: ("psi3_aqr", "psi3 Aqr"),
}
ids = ",".join(str(h) for h in STARS)
url = ("https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=I/311/hip2&-out=HIP,RArad,DErad,Plx,pmRA,pmDE"
       "&-out.max=100&HIP=" + urllib.parse.quote(ids))
txt = urllib.request.urlopen(url, timeout=120).read().decode()
rows = {}
for line in txt.splitlines():
    p = line.split('\t')
    if len(p) >= 6 and p[0].strip().isdigit():
        h = int(p[0]); rows[h] = dict(ra=float(p[1]), de=float(p[2]), plx=float(p[3]), pmra=float(p[4]), pmde=float(p[5]))
# radial velocities from SIMBAD TAP
q = ("SELECT id, rvz_radvel FROM basic JOIN ident ON oidref=oid WHERE id IN ("
     + ",".join(f"'HIP {h}'" for h in STARS) + ")")
u2 = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync?" + urllib.parse.urlencode(
    dict(request="doQuery", lang="adql", format="tsv", query=q))
rv = {}
try:
    for line in urllib.request.urlopen(u2, timeout=120).read().decode().splitlines()[1:]:
        a, b = line.split('\t')
        h = int(a.strip('"').split()[1]); rv[h] = float(b) if b.strip() else 0.0
except Exception as e:
    print("SIMBAD RV fetch failed:", e)
out = {}
for h, (k, n) in STARS.items():
    if h not in rows:
        print("MISSING", h, k); continue
    r = rows[h]
    out[k] = [h, n, r['ra'], r['de'], r['plx'], r['pmra'], r['pmde'], rv.get(h, 0.0)]
    print(k, out[k])
Path(__file__).with_name('stars.json').write_text(json.dumps(dict(
    source="VizieR I/311/hip2 (van Leeuwen 2007), epoch J1991.25 ICRS; RV SIMBAD basic.rvz_radvel; fetched 2026-10-04",
    url=url, stars=out), indent=1), encoding='utf-8')
