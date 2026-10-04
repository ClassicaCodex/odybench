"""
Fetch and verify the star data the bench uses, and write data/stars.json.

    cd C:\\Projects\\odybench && py tools/fetch_stars.py          # uses cached responses if present
    py tools/fetch_stars.py --refetch                            # query the services again

For each star:
  * SIMBAD TAP (https://simbad.cds.unistra.fr/simbad/sim-tap): identifiers
    (HIP, HR, HD, proper names), ICRS J2000 position and its bibcode, V
    magnitude, radial velocity with error, quality and bibcode.
  * VizieR I/311/hip2 (Hipparcos new reduction, van Leeuwen 2007): ICRS
    position at epoch J1991.25, parallax, proper motions, errors, Hp, B-V,
    solution types.
  * VizieR I/239/hip_main (Hipparcos 1997): the same, plus AstroRef (what the
    astrometry refers to: component, photocentre '*' or centre of mass '+')
    and MultFlag (C, G, O, V, X annexes).
The HIP number is NOT taken from memory: it is read from SIMBAD's identifier
list for the Bayer designation, then the hip2 row of that number is checked
against SIMBAD's position (propagated J1991.25 -> J2000 with the hip2 proper
motion, < 1") and magnitude (|Hp - V| < 0.6 mag).

Sirius (critique-design issue 25): the Hipparcos solution for HIP 32349 is
an ORBITAL solution (hip_main MultFlag 'O', Double and Multiple Systems
Annex part O) whose astrometric parameters refer to the CENTRE OF MASS
(AstroRef '+'); hip2 carries it over (solution types Sn 0, So 4 = "orbital
binary as resolved in the published catalog").  So the adopted proper motion
is the Hipparcos value, which is already orbit-corrected and barycentric.
The script quantifies at -1177 (a) the long-baseline ground-based FK5
proper motion (VizieR I/149A) and (b) the instantaneous motion of Sirius A
at J1991.25 (barycentric + its orbital velocity from Bond et al. 2017,
ApJ 840:70, Tables 4-5), against the adopted value, in arcminutes.

Raw responses are cached in data/refs/stars/ (one file per query, the URL
on the first line).  Writes data/stars.json.
"""
import argparse
import hashlib
import json
import math
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import erfa
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import calendar as C  # noqa: E402

CACHE = ROOT / "data" / "refs" / "stars"
OUT = ROOT / "data" / "stars.json"
SIMBAD_TAP = "https://simbad.cds.unistra.fr/simbad/sim-tap/sync"
VIZIER_ASU = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"
EPOCH_HIP = 2448349.0625          # J1991.25 (TT), the Hipparcos catalogue epoch
JD_M1177 = C.jd_from_julian(-1177, 4, 16)   # 1291263.5, the epoch of the comparisons

# key: (SIMBAD identifier, role, HIP number as previously stated, where it was stated)
STARS = {
    "alcyone": ("* eta Tau", "grammar: Pleiades (Alcyone)", 17702, "odybench/ephem.py HIP_STARS"),
    "arcturus": ("* alf Boo", "grammar: Arcturus / Bootes", 69673, "odybench/ephem.py HIP_STARS"),
    "eps_boo": ("* eps Boo", "grammar: Bootes", 72105, "odybench/ephem.py HIP_STARS"),
    "eta_boo": ("* eta Boo", "grammar: Bootes", 67927, "odybench/ephem.py HIP_STARS"),
    "sirius": ("* alf CMa", "grammar: Sirius", 32349, "DESIGN 7.3 [from memory]"),
    "aldebaran": ("* alf Tau", "grammar: Hyades (Aldebaran, the bright star of the V; not a cluster member)", 21421,
                  "DESIGN 7.3 [from memory]"),
    "betelgeuse": ("* alf Ori", "grammar: Orion", 27989, "DESIGN 7.3 [from memory]"),
    "rigel": ("* bet Ori", "grammar: Orion", 24436, "DESIGN 7.3 [from memory]"),
    "dubhe": ("* alf UMa", "grammar: the Bear", 54061, "DESIGN 7.3 [from memory]"),
    # extras: true Hyades members, the rest of Orion's figure, the other Bootes stars of
    # docs/research_visibility_calc.py -- not yet used by the grammar, fetched so that a
    # fork 'which star stands for the constellation' can be run without another fetch.
    "gam_tau": ("* gam Tau", "extra: Hyades member (Prima Hyadum)", None, None),
    "del01_tau": ("* del01 Tau", "extra: Hyades member", None, None),
    "eps_tau": ("* eps Tau", "extra: Hyades member (Ain)", None, None),
    "tet02_tau": ("* tet02 Tau", "extra: Hyades member (brightest)", None, None),
    "bellatrix": ("* gam Ori", "extra: Orion (Bellatrix)", None, None),
    "mintaka": ("* del Ori", "extra: Orion's belt (Mintaka)", None, None),
    "alnilam": ("* eps Ori", "extra: Orion's belt (Alnilam)", None, None),
    "alnitak": ("* zet Ori", "extra: Orion's belt (Alnitak)", None, None),
    "saiph": ("* kap Ori", "extra: Orion (Saiph)", None, None),
    "gam_boo": ("* gam Boo", "extra: Bootes", None, None),
    "bet_boo": ("* bet Boo", "extra: Bootes", None, None),
    "del_boo": ("* del Boo", "extra: Bootes", None, None),
}


def cached_get(tag, url, refetch):
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"{tag}.txt"
    if f.exists() and not refetch:
        return f.read_text(encoding="utf-8").split("\n", 1)[1]
    req = urllib.request.Request(url, headers={"User-Agent": "odybench/1.0 (research bench)"})
    txt = urllib.request.urlopen(req, timeout=180).read().decode("utf-8")
    f.write_text(url + "\n" + txt, encoding="utf-8", newline="\n")
    return txt


def simbad(adql, tag, refetch):
    url = SIMBAD_TAP + "?" + urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json",
                                                      "QUERY": adql})
    d = json.loads(cached_get(tag, url, refetch))
    cols = [c["name"] for c in d["metadata"]]
    return [dict(zip(cols, r)) for r in d["data"]]


def vizier(source, tag, refetch, **constraints):
    params = {"-source": source, "-out.all": "1"}
    params.update(constraints)
    url = VIZIER_ASU + "?" + urllib.parse.urlencode(params)
    txt = cached_get(tag, url, refetch)
    rows = [l for l in txt.splitlines() if l and not l.startswith("#")]
    if len(rows) < 4:
        return [], {}
    hdr = [h.strip() for h in rows[0].split("\t")]
    units = [u.strip() for u in rows[1].split("\t")]
    out = []
    for r in rows[3:]:
        vals = [v.strip() for v in r.split("\t")]
        out.append({h: v for h, v in zip(hdr, vals)})
    out_units = dict(zip(hdr, units))
    return out, out_units


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def sep_arcsec(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(math.radians, (ra1, de1, ra2, de2))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    s = math.hypot(math.cos(d2) * math.sin(r2 - r1),
                   math.cos(d1) * math.sin(d2) - math.sin(d1) * math.cos(d2) * math.cos(r2 - r1))
    return math.degrees(math.atan2(s, c)) * 3600


def propagate(ra, de, pmra_star, pmde, plx, rv, jd_from, jd_to):
    """ERFA eraPmsafe space motion (rigorous, with radial velocity and light-time).
    pmra_star = mu_alpha cos(dec) in mas/yr.  Returns (ra_deg, dec_deg)."""
    mas = math.radians(1 / 3.6e6)
    pmr = pmra_star * mas / math.cos(math.radians(de))       # ERFA wants d(alpha)/dt
    out = erfa.pmsafe(math.radians(ra), math.radians(de), pmr, pmde * mas, plx / 1000.0, rv,
                      jd_from, 0.0, jd_to, 0.0)
    return math.degrees(out[0]) % 360.0, math.degrees(out[1])


def orbit_offset(epoch, P, T0, a, e, w, i, Om, sign=1.0):
    """(east, north) offset in the units of `a` at Julian epoch `epoch` on a Keplerian
    visual orbit (Thiele-Innes constants; x = Dec offset, y = RA* offset)."""
    i, Om, w = map(math.radians, (i, Om, w))
    A_ = a * (math.cos(w) * math.cos(Om) - math.sin(w) * math.sin(Om) * math.cos(i))
    B_ = a * (math.cos(w) * math.sin(Om) + math.sin(w) * math.cos(Om) * math.cos(i))
    F_ = a * (-math.sin(w) * math.cos(Om) - math.cos(w) * math.sin(Om) * math.cos(i))
    G_ = a * (-math.sin(w) * math.sin(Om) + math.cos(w) * math.cos(Om) * math.cos(i))
    M = 2 * math.pi * (epoch - T0) / P
    E = M
    for _ in range(60):
        E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    X = math.cos(E) - e
    Y = math.sqrt(1 - e * e) * math.sin(E)
    return sign * (B_ * X + G_ * Y), sign * (A_ * X + F_ * Y)


# Sirius A about the centre of mass, mas.  BOND: Bond et al. 2017, ApJ 840:70, Table 4 (relative orbit
# of B about A: P 50.1284 yr, T0 1994.5715, e 0.59142, omega 149.161, i 136.336, Omega 45.400) with
# a_A = 2476.1 mas (their Table 5); A moves opposite to B.  DMSA: the orbit the Hipparcos solution
# held FIXED (I/239 hip_dm_o: P 18295.4 d, T JD 2440000-27123.7, a0 2490.40 mas, e 0.5923, w 327.27,
# i 136.53, Omega 44.86; status flags 111110000000 = only the 5 astrometric parameters estimated).
BOND = dict(P=50.1284, T0=1994.5715, a=2476.1, e=0.59142, w=149.161, i=136.336, Om=45.400, sign=-1.0)
DMSA = dict(P=18295.4 / 365.25, T0=2000.0 + (2440000.0 - 27123.7 - 2451545.0) / 365.25, a=2490.40,
            e=0.5923, w=327.27, i=136.53, Om=44.86, sign=1.0)
HIP_MISSION = (1989.85, 1993.21)        # Hipparcos observations, Nov 1989 - Mar 1993 (ESA 1997)


def orbit_velocity(orbit, epoch, h=1e-3):
    e1, n1 = orbit_offset(epoch - h, **orbit)
    e2, n2 = orbit_offset(epoch + h, **orbit)
    return (e2 - e1) / (2 * h), (n2 - n1) / (2 * h)


def mission_slope(orbit_a, orbit_b, n=401):
    """Least-squares slope (mas/yr) of orbit_a - orbit_b over the Hipparcos mission: the
    error a 5-parameter fit with orbit_b held fixed makes in the barycentric proper motion
    when orbit_a is the true orbit."""
    t = np.linspace(*HIP_MISSION, n)
    d = np.array([np.subtract(orbit_offset(x, **orbit_a), orbit_offset(x, **orbit_b)) for x in t])
    A = np.vstack([np.ones_like(t), t - t.mean()]).T
    return tuple(float(np.linalg.lstsq(A, d[:, k], rcond=None)[0][1]) for k in (0, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refetch", action="store_true")
    a = ap.parse_args()
    stars = {}
    problems = []
    for key, (sid, role, hip_stated, stated_where) in STARS.items():
        tag = re.sub(r"[^a-z0-9]+", "_", sid.lower()).strip("_")
        q = ("SELECT b.main_id, b.ra, b.dec, b.coo_bibcode, b.pmra, b.pmdec, b.pm_bibcode, b.plx_value, "
             "b.plx_bibcode, b.rvz_radvel, b.rvz_err, b.rvz_qual, b.rvz_bibcode, b.rvz_type, b.sp_type "
             f"FROM basic AS b WHERE b.oid IN (SELECT oidref FROM ident WHERE id = '{sid}')")
        basic = simbad(q, f"simbad_basic_{tag}", a.refetch)
        idents = [r["id"] for r in simbad(f"SELECT id FROM ident WHERE oidref IN (SELECT oidref FROM ident WHERE id = '{sid}')",
                                          f"simbad_ident_{tag}", a.refetch)]
        flux = simbad(f"SELECT filter, flux, bibcode FROM flux WHERE oidref IN (SELECT oidref FROM ident WHERE id = '{sid}') "
                      "AND filter IN ('B', 'V')", f"simbad_flux_{tag}", a.refetch)
        if len(basic) != 1:
            problems.append(f"{key}: SIMBAD returned {len(basic)} objects for {sid}")
            continue
        b = basic[0]
        hips = sorted({int(m.group(1)) for i in idents for m in [re.fullmatch(r"HIP\s+(\d+)", i)] if m})
        if len(hips) != 1:
            problems.append(f"{key}: SIMBAD lists HIP ids {hips}")
            continue
        hip = hips[0]
        h2, u2 = vizier("I/311/hip2", f"vizier_hip2_{hip}", a.refetch, HIP=str(hip))
        h1, u1 = vizier("I/239/hip_main", f"vizier_hip1_{hip}", a.refetch, HIP=str(hip))
        assert len(h2) == 1 and len(h1) == 1, (key, len(h2), len(h1))
        h2, h1 = h2[0], h1[0]
        V = {f["filter"]: (f["flux"], f["bibcode"]) for f in flux}
        # --- verification
        ra2, de2 = float(h2["RArad"]), float(h2["DErad"])
        pmra2, pmde2, plx2 = float(h2["pmRA"]), float(h2["pmDE"]), float(h2["Plx"])
        jd2000 = 2451545.0
        dr = sep_arcsec(*propagate(ra2, de2, pmra2, pmde2, plx2, 0.0, EPOCH_HIP, jd2000), b["ra"], b["dec"])
        hp = float(h2["Hpmag"])
        vmag = V.get("V", (None, None))[0]
        ok_pos = dr < 1.0
        ok_mag = vmag is not None and abs(hp - vmag) < 0.6
        ok_hip = hip_stated is None or hip_stated == hip
        if not (ok_pos and ok_mag and ok_hip):
            problems.append(f"{key}: position {dr:.3f}\" mag Hp-V {hp - (vmag or 0):+.2f} hip {hip} vs stated {hip_stated}")
        names = [i for i in idents if i.startswith("NAME ")]
        rec = {
            "role": role,
            "simbad_id": sid,
            "simbad_main_id": b["main_id"],
            "hip": hip,
            "hip_check": {
                "stated_before": hip_stated, "stated_where": stated_where,
                "simbad_identifiers_hip": hips,
                "verdict": ("confirmed" if hip_stated == hip else "corrected") if hip_stated else "from SIMBAD",
                "hip2_vs_simbad_J2000_arcsec": round(dr, 4),
                "Hp_minus_V_mag": round(hp - vmag, 3) if vmag is not None else None,
            },
            "names": names,
            "other_ids": [i for i in idents if re.match(r"(HR|HD|FK5|GJ|Gaia DR3)\s", i)],
            "simbad": {
                "ra_icrs_j2000_deg": b["ra"], "dec_icrs_j2000_deg": b["dec"], "coo_bibcode": b["coo_bibcode"],
                "pmra_mas_yr": b["pmra"], "pmdec_mas_yr": b["pmdec"], "pm_bibcode": b["pm_bibcode"],
                "plx_mas": b["plx_value"], "plx_bibcode": b["plx_bibcode"],
                "rv_km_s": b["rvz_radvel"], "rv_err_km_s": b["rvz_err"], "rv_quality": b["rvz_qual"],
                "rv_bibcode": b["rvz_bibcode"], "rv_type": b["rvz_type"], "sp_type": b["sp_type"],
                "V_mag": vmag, "V_bibcode": V.get("V", (None, None))[1],
                "B_mag": V.get("B", (None, None))[0],
            },
            "hip2": {k: (num(v) if num(v) is not None else v) for k, v in h2.items()
                     if k in ("HIP", "Sn", "So", "Nc", "RArad", "e_RArad", "DErad", "e_DErad", "Plx", "e_Plx",
                              "pmRA", "e_pmRA", "pmDE", "e_pmDE", "Ntr", "F2", "F1", "var", "Hpmag", "e_Hpmag",
                              "sHp", "B-V", "e_B-V", "V-I")},
            "hip1": {k: (num(v) if num(v) is not None else v) for k, v in h1.items()
                     if k in ("HIP", "Vmag", "RAICRS", "DEICRS", "AstroRef", "Plx", "pmRA", "pmDE", "e_Plx", "e_pmRA",
                              "e_pmDE", "MultFlag", "Hpmag", "B-V", "SpType", "CCDM", "Nsys", "Ncomp")},
        }
        rv = b["rvz_radvel"]
        rec["adopted"] = {
            "ra_deg": ra2, "dec_deg": de2, "frame": "ICRS", "epoch": "J1991.25", "epoch_jd_tt": EPOCH_HIP,
            "plx_mas": plx2, "pmra_mas_yr": pmra2, "pmde_mas_yr": pmde2,
            "pmra_is": "mu_alpha* = mu_alpha cos(dec)",
            "rv_km_s": rv,
            "astrometry_source": "Hipparcos new reduction, van Leeuwen 2007, VizieR I/311/hip2",
            "rv_source": f"SIMBAD rvz_radvel ({b['rvz_bibcode']}, quality {b['rvz_qual']})",
        }
        stars[key] = rec
        print(f"{key:11s} {sid:12s} HIP {hip:6d} ({rec['hip_check']['verdict']}); hip2 vs SIMBAD {dr:7.4f}\";"
              f" Hp-V {hp - (vmag or 0):+.2f}; AstroRef {h1.get('AstroRef')!r} MultFlag {h1.get('MultFlag')!r}"
              f" Sn {h2['Sn']} So {h2['So']}; RV {rv} ({b['rvz_qual']})")

    # --- Sirius
    s = stars["sirius"]
    fk5, _ = vizier("I/149A/catalog", "vizier_fk5_257", a.refetch, FK5="257")
    dmo, _ = vizier("I/239/hip_dm_o", "vizier_hip_dm_o_32349", a.refetch, HIP="32349")
    fk5, dmo = fk5[0], dmo[0]
    de2000 = s["simbad"]["dec_icrs_j2000_deg"]
    fk5_pmra_star = float(fk5["pmRA"]) * 15.0 * 1000.0 / 100.0 * math.cos(math.radians(de2000))  # s/cy -> mas/yr
    fk5_pmde = float(fk5["pmDE"]) * 1000.0 / 100.0
    ad = s["adopted"]
    rv_sys_obs, rv_sys_true = -7.70, -8.47        # Bond et al. 2017 sect. 5.1
    ad["rv_km_s"] = rv_sys_true
    ad["rv_source"] = ("Bond et al. 2017, ApJ 840:70, sect. 5.1: system (centre-of-mass) velocity -7.70 km/s from"
                       " RVs 1903-1995 and the relative orbit, -8.47 km/s after removing Sirius A's gravitational"
                       " redshift (the true radial component of the space motion)")
    ad["astrometry_source"] = ("Hipparcos (van Leeuwen 2007, I/311/hip2; = ESA 1997 orbital solution): the astrometric"
                               " parameters refer to the CENTRE OF MASS (I/239 hip_main AstroRef '+', MultFlag 'O',"
                               " DMSA part O orbit P 18295.4 d, a0 2490.40 mas); i.e. an orbit-corrected"
                               " barycentric proper motion")
    ad["proper_motion_kind"] = "orbit-corrected barycentric (Hipparcos orbital solution)"

    def at_m1177(pmra, pmde, rv=ad["rv_km_s"]):
        return propagate(ad["ra_deg"], ad["dec_deg"], pmra, pmde, ad["plx_mas"], rv, EPOCH_HIP, JD_M1177)

    base = at_m1177(ad["pmra_mas_yr"], ad["pmde_mas_yr"])
    ep_hip = float(C.julian_epoch(EPOCH_HIP))
    vorb_e, vorb_n = orbit_velocity(BOND, ep_hip)
    vdm_e, vdm_n = orbit_velocity(DMSA, ep_hip)
    sl_e, sl_n = mission_slope(BOND, DMSA)
    comps = {}

    def comp(label, pmra, pmde, rv=ad["rv_km_s"], note=""):
        p = at_m1177(pmra, pmde, rv)
        d = sep_arcsec(*base, *p)
        comps[label] = {"pmra_mas_yr": round(pmra, 3), "pmde_mas_yr": round(pmde, 3), "rv_km_s": rv,
                        "dpm_mas_yr": round(math.hypot(pmra - ad["pmra_mas_yr"], pmde - ad["pmde_mas_yr"]), 3),
                        "position_m1177_ra_deg": round(p[0], 6), "position_m1177_dec_deg": round(p[1], 6),
                        "difference_from_adopted_arcmin": round(d / 60.0, 3), "note": note}

    comp("hipparcos_1997_I239", float(s["hip1"]["pmRA"]), float(s["hip1"]["pmDE"]),
         note="ESA 1997, same centre-of-mass solution")
    comp("fk5_long_baseline_I149A", fk5_pmra_star, fk5_pmde,
         note=(f"FK5 (Fricke et al. 1988) ground-based meridian proper motion, central epochs RA {fk5['EpRA-1900']}"
               f"+1900, Dec {fk5['EpDE-1900']}+1900; {fk5['pmRA']} s/cy, {fk5['pmDE']}\"/cy converted with cos(dec);"
               " FK5 system, not rotated to ICRS (FK5-Hipparcos spin is about 1 mas/yr)"))
    # the fit made photocentre = bary_fit + DMSA orbit; if photocentre = bary_true + Bond orbit, then
    # pm_fit = pm_true + slope(Bond - DMSA), so pm_true = pm_fit - slope
    comp("hipparcos_reduced_with_bond2017_orbit", ad["pmra_mas_yr"] - sl_e, ad["pmde_mas_yr"] - sl_n,
         note=("the Hipparcos centre-of-mass proper motion re-referred from the fixed DMSA/O orbit to Bond et al."
               " 2017's orbit: minus the least-squares slope of (Bond orbit - DMSA orbit) over the mission"
               " 1989.85-1993.21 (computed here; it assumes the 5-parameter fit absorbed that slope)"))
    comp("sirius_A_instantaneous_J1991.25", ad["pmra_mas_yr"] + vorb_e, ad["pmde_mas_yr"] + vorb_n,
         note=("barycentric + orbital velocity of Sirius A at J1991.25 from Bond et al. 2017 Tables 4-5: what a"
               " short-baseline single-star (photocentre) solution would have measured"))
    comp("rv_simbad_sirius_A", ad["pmra_mas_yr"], ad["pmde_mas_yr"], rv=s["simbad"]["rv_km_s"],
         note="same proper motion with SIMBAD's RV for Sirius A (-5.5 km/s, 2006AstL...32..759G) instead of the system's")
    comp("rv_bond_observed", ad["pmra_mas_yr"], ad["pmde_mas_yr"], rv=rv_sys_obs,
         note="system velocity without the gravitational-redshift correction")
    stars["sirius"]["proper_motion_comparison_m1177"] = {
        "epoch": "-1177-04-16 0h TT (JD 1291263.5)",
        "method": "ERFA eraPmsafe space motion from J1991.25 (catalogue coordinates, ICRS)",
        "adopted_position_m1177_ra_deg": round(base[0], 6), "adopted_position_m1177_dec_deg": round(base[1], 6),
        "orbital_velocity_A_J1991.25_mas_yr": {"east": round(vorb_e, 2), "north": round(vorb_n, 2),
                                               "total": round(math.hypot(vorb_e, vorb_n), 2),
                                               "source": "Bond et al. 2017 Tables 4-5"},
        "orbital_velocity_photocentre_J1991.25_DMSA_O_mas_yr": {"east": round(vdm_e, 2), "north": round(vdm_n, 2),
                                                                "total": round(math.hypot(vdm_e, vdm_n), 2),
                                                                "source": "I/239 hip_dm_o (held fixed by Hipparcos)"},
        "bond_minus_dmsa_mission_slope_mas_yr": {"east": round(sl_e, 2), "north": round(sl_n, 2)},
        "fk5_row": {k: fk5[k] for k in ("FK5", "pmRA", "pmDE", "EpRA-1900", "EpDE-1900", "e_pmRA", "e_pmDE", "RV")},
        "hip_dmsa_o_row": dmo,
        "alternatives": comps,
    }
    print("\nSirius at -1177, difference from the adopted (Hipparcos centre-of-mass) proper motion:")
    for k, v in comps.items():
        print(f"  {k:38s} pm ({v['pmra_mas_yr']:9.2f}, {v['pmde_mas_yr']:9.2f}) dpm {v['dpm_mas_yr']:7.2f} mas/yr"
              f" -> {v['difference_from_adopted_arcmin']:7.3f} arcmin")
    fk, bd = comps["fk5_long_baseline_I149A"], comps["hipparcos_reduced_with_bond2017_orbit"]
    d_fb = math.hypot(fk["pmra_mas_yr"] - bd["pmra_mas_yr"], fk["pmde_mas_yr"] - bd["pmde_mas_yr"])
    stars["sirius"]["proper_motion_comparison_m1177"]["fk5_minus_bond_rereferred_mas_yr"] = round(d_fb, 2)
    print(f"  FK5 vs Hipparcos re-referred to the Bond orbit: {d_fb:.2f} mas/yr apart")
    print(f"  orbital velocity of A at J1991.25: Bond 2017 {math.hypot(vorb_e, vorb_n):.1f} mas/yr,"
          f" DMSA/O {math.hypot(vdm_e, vdm_n):.1f} mas/yr; Bond - DMSA slope over the mission ({sl_e:+.2f}, {sl_n:+.2f}) mas/yr")

    # --- consistency with the four stars hard-wired in odybench.ephem
    from odybench.ephem import HIP_STARS
    legacy = {}
    for k, (hip, name, ra, de, plx, pmra, pmde, rv) in HIP_STARS.items():
        ad = stars[k]["adopted"]
        same = (hip == stars[k]["hip"] and ra == ad["ra_deg"] and de == ad["dec_deg"] and plx == ad["plx_mas"]
                and pmra == ad["pmra_mas_yr"] and pmde == ad["pmde_mas_yr"])
        legacy[k] = {"astrometry_identical": same, "ephem_rv": rv, "simbad_rv": ad["rv_km_s"]}
        print(f"ephem.HIP_STARS[{k!r}] astrometry identical to hip2 row: {same}; RV ephem {rv} SIMBAD {ad['rv_km_s']}")
        if not same:
            problems.append(f"{k}: ephem.HIP_STARS differs from the fetched hip2 row")
        # keep the module's value as adopted so that adding stars.json changes no computed value
        ad["rv_km_s"] = rv
    out = {
        "about": ("Star data for odybench, written by tools/fetch_stars.py.  Every star's HIP number is taken from"
                  " SIMBAD's identifier list for its Bayer designation and checked against the Hipparcos row"
                  " (position and magnitude).  'adopted' is what odybench.ephem.star() uses."),
        "fetched": "2026-10-04",
        "conventions": {
            "positions": "ICRS degrees; hip2 at epoch J1991.25 (JD 2448349.0625 TT); SIMBAD at J2000",
            "proper_motion": "mas/yr; pmra is mu_alpha* = mu_alpha cos(dec)",
            "parallax": "mas", "radial_velocity": "km/s, positive receding",
            "propagation": "linear space motion with radial velocity (skyfield Star / ERFA eraPmsafe)",
        },
        "sources": {
            "SIMBAD": "SIMBAD TAP, https://simbad.cds.unistra.fr/simbad/sim-tap (basic, ident, flux tables)",
            "hip2": "van Leeuwen 2007, A&A 474, 653, Hipparcos new reduction, VizieR I/311/hip2",
            "hip1": "ESA 1997, The Hipparcos and Tycho Catalogues, ESA SP-1200, VizieR I/239/hip_main",
            "FK5": "Fricke et al. 1988, VizieR I/149A",
            "Bond2017": "Bond, H.E. et al. 2017, ApJ 840:70 (arXiv:1703.10625), data/refs/stars/bond2017_arxiv1703.10625v1.pdf",
            "raw": "data/refs/stars/*.txt (request URL on line 1)",
        },
        "legacy_ephem_check": legacy,
        "problems": problems,
        "stars": stars,
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"\nwrote {OUT.relative_to(ROOT)} ({len(stars)} stars); sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()}")
    print("problems:", problems or "none")


if __name__ == "__main__":
    main()
