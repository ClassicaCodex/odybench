"""Scratch (A0): writes six prereg files of DESIGN 10.1's A0 row, each entry with
its source:

  data/prereg/sites.json          (DESIGN 0, 4.1; a span and a column set per site)
  data/prereg/windows.json        (4.1, 4.6, 5.1, 6.3.2, 7.2)
  data/prereg/seeds.json          (every random draw the design names; seeds derived by rule)
  data/prereg/deltat_models.json  (0, 2.3, 6.3.3, 10.2 deltat_mix)
  data/prereg/slots.json          (4.2)
  data/prereg/verdict_rule.json   (9.1, 9.2; every threshold)

Nothing here reads a truth file or evaluates the sky.  Run from C:\\Projects\\odybench:
    py results/build-A0/make_prereg.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from odybench import calendar as C  # noqa: E402
from odybench import model as M  # noqa: E402

P = ROOT / "data" / "prereg"
WRITTEN = "2026-10-04 by A0 (lead), from DESIGN.md revision 8"


def dump(name, obj):
    (P / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", name)


# ------------------------------------------------------------------ sites

ALL_ARRAYS = ["jdn", "jd0_ut", "rise_ut", "set_ut", "rise_az", "set_az", "sun_alt_at_rise", "sun_alt_at_set",
              "mag_at_rise", "mag_at_set", "elong", "lat_ecl", "lon_ecl", "twl_eve_ut", "twl_morn_ut",
              "star_alt_eve12", "star_alt_morn12", "star_rise_ut", "star_set_ut", "sun_alt_at_star_rise",
              "sun_alt_at_star_set", "moon_frac_midnight", "moon_up_frac_dark", "night_len_h"]
BASE = ["jdn", "jd0_ut", "twl_eve_ut", "twl_morn_ut", "night_len_h"]
HORIZON = ["rise_ut", "set_ut", "sun_alt_at_rise", "sun_alt_at_set", "mag_at_rise", "mag_at_set"]
AZ = ["rise_az", "set_az"]
GEOM = ["elong", "lat_ecl", "lon_ecl"]
STAR = ["star_alt_eve12", "star_alt_morn12", "star_rise_ut", "star_set_ut", "sun_alt_at_star_rise",
        "sun_alt_at_star_set"]
MOON = ["moon_frac_midnight", "moon_up_frac_dark"]
ALL_STARS = list(json.loads((ROOT / "data" / "stars.json").read_text(encoding="utf-8"))["stars"].keys())


def columns(bodies, stars, az=False):
    cols = BASE + HORIZON + GEOM + (AZ if az else []) + (STAR if stars else []) + (MOON if "moon" in bodies else [])
    return [c for c in ALL_ARRAYS if c in cols]


# each negative set's needs, read off its clue rows' option texts (negatives.json); a set's rows may
# be evaluated at any of its observer places, so every place of the set gets the set's whole need
NEG_NEEDS = {
    "AEN-TROY": (["sun", "moon", "venus", "mars", "jupiter"], ["sirius"], True,
                 "02 Moon up / conjunction; 04 Moon up; 05 conjunction; 07 Venus lead, AV 7, herald "
                 "(Venus, Jupiter, Sirius, Mars), Venus rise azimuth (ida rider)"),
    "AEN-CRETE": (["sun", "moon"], ["sirius"], False, "01 Sirius heliacal rising; 02 opposition, Moon up"),
    "AEN-ITALY": (["sun"], ["arcturus", "aldebaran", "betelgeuse", "rigel", "dubhe"], False,
                  "02 Arcturus, Aldebaran, Betelgeuse, Rigel above 5 or 2 deg (the Triones circumpolar)"),
    "AEN-ETNA": (["sun", "moon", "venus", "mars", "jupiter"], ["sirius"], False,
                 "02 Moon up; 03 Venus lead, AV 7, herald; 04 waxing Moon, opposition"),
    "AEN-CARTHAGE": (["sun", "mercury"], [], True,
                     "01, 05 Mercury rise-azimuth maximum, GWE, station, first visibility (AV 10); 03 season"),
    "ARG-CIUS": (["sun", "moon", "venus", "mars", "jupiter"], ["sirius", "alcyone"], False,
                 "02 opposition, Moon up; 03 Venus lead, AV 7, herald; 05 Moon below the horizon; "
                 "07 solstice, Pleiades' morning setting"),
    "ARG-COLCHIS": (["sun", "moon"], ["arcturus", "betelgeuse", "rigel", "dubhe"], False,
                    "01 Arcturus' four phases; 04 Betelgeuse, Rigel at nautical dusk; 05 Dubhe past "
                    "culmination; 06 moonrise in the dark hours"),
    "ARG-RETURN": (["sun", "moon", "venus", "mars", "jupiter"], ["sirius"], False,
                   "01 Venus set lag, AV 7, evening herald; 04 Moon below the horizon, conjunction, lunar "
                   "and solar eclipse"),
    "QS-SACK": (["sun", "moon"], ["alcyone"], False,
                "02 lunar eclipse, Moon up and full, conjunction; 03 Alcyone above the horizon; 06 solar "
                "eclipse"),
    "VF-LEMNOS": (["sun", "moon"], ["betelgeuse", "rigel", "alcyone"], False,
                  "02 Moon in evening twilight; 03 Betelgeuse, Rigel, Mirfak, Orion's morning setting; "
                  "04 Pleiades' phases, Alcyone at nautical dawn; 05 Pleiades' morning setting, equinox; "
                  "06 Moon's age at sunset. Mirfak (alpha Per) is not in data/stars.json"),
    "VF-CYZICUS": (["sun", "moon"], [], False, "02 Moon up in Night 0"),
    "VF-COLCHIS": (["sun", "venus", "mars", "jupiter"], ["sirius"], False,
                   "01 Venus set lag, AV 7, evening herald; 02 Venus lead, AV 7, herald"),
    "IL-PATROCLUS": (["sun", "moon", "mercury", "venus", "mars", "jupiter"],
                     ["alcyone", "aldebaran", "betelgeuse", "rigel", "sirius"], True,
                     "02, 04, 05 conjunction, solar eclipse, Moon up; 06 stars above 2 deg, Pleiades' "
                     "morning setting, opposition; 08 Venus lead, AV 7, herald; 10 Mercury events, "
                     "first visibility, dawn visibility"),
}
NEG_KEYS = {(39.9575, 26.2389): "troy", (39.8219, 26.0289): "tenedos", (35.21, 24.91): "crete_pergamea",
            (40.1986, 19.5917): "ceraunia", (37.5636, 15.1614): "etna_coast", (36.8528, 10.3233): "carthage",
            (40.4325, 29.1564): "cius", (40.3878, 27.8706): "cyzicus", (42.15, 41.6667): "colchis_phasis",
            (40.9289, 38.4361): "ares_island", (35.3128, 26.3076): "cape_salmonis",
            (36.3719, 25.7953): "anaphe", (32.8225, 21.8625): "libyan_coast",
            (38.1167, 24.5667): "cape_caphereus", (40.0, 24.7): "athos_lemnos_sea",
            (39.8833, 25.0667): "lemnos"}
CTRL_POINTS = {(32.54, 44.42): "babylon", (31.2, 29.92): "alexandria", (37.97, 23.72): "athens",
               (37.07, 15.29): "syracuse", (38.5, 22.85): "boeotia_entry", (39.5, 22.6): "thessaly",
               (36.19, 44.01): "arbela", (36.5, 43.0): "tigris_camp", (40.37, 22.6): "pydna",
               (40.85, 14.05): "cumae", (41.89, 12.49): "rome", (41.5, 15.56): "arpi"}
BACKGROUND_MARGINS = [-2060, 241]
CONTROL_ENVELOPE = [-1999, 300]


def sites():
    out = {}

    def add(key, lat, lon, source, span, cols, role, bodies, stars, extra=None):
        assert key not in out, key
        row = {"lat": lat, "lon": lon, "elev_m": 0.0, "source": source, "span": span,
               "columns": cols, "role": role, "build": {"bodies": bodies, "stars": stars}}
        if extra:
            row.update(extra)
        out[key] = row

    full = list(ALL_ARRAYS)
    add("ithaki", 38.37, 20.72, "Ithaki (Vathy): the coordinates that reproduce the NASA site catalogue "
        "[acq 2.2]; Vathy 38.367, 20.717 differs by 0.3 km (DESIGN 0)", BACKGROUND_MARGINS, full,
        "primary Odyssey site: every column over the whole span (4.1)", list(M.BODIES), ALL_STARS,
        {"span_source": "the data margins -2060..+241 (4.1, 10.2 sky.py): the background -1999..+200 with the "
                        "40-day clue offsets and the +/-60-day Mercury searches"})
    add("bm", 38.4, 20.7, "B&M's fitted site, the S2 clock fit [bm 3.2] (DESIGN 0)", [-1250, -1113],
        columns(["sun", "mercury", "venus"], ["arcturus", "alcyone"], az=True),
        "T0b only (3.2): B&M's clock, a constant Delta-T", ["sun", "mercury", "venus"], ["arcturus", "alcyone"],
        {"span_source": "the reproduction window -1249..-1114 (4.6) with one year on each side for the "
                        "-34-day offsets and the +/-60-day Mercury searches",
         "build_extra": {"dt_model": 27602.7, "dt_source": "B&M's clock, 27,602.7 s (DESIGN 0, 2.3; T0b only)"}})
    ionian = {"kefalonia": (38.18, 20.49, "Argostoli [acq 2.2] (DESIGN 0)"),
              "lefkada": (38.83, 20.70, "Lefkada town [acq 2.2]; research-ephemeris used 20.71 [eph "
                                        "conventions]; 20.70 is adopted so that the site catalogue reproduces "
                                        "(DESIGN 0)"),
              "corfu": (39.62, 19.92, "Corfu town [acq 2.2] (DESIGN 0)"),
              "zakynthos": (37.78, 20.90, "Zakynthos town [acq 2.2] (DESIGN 0)")}
    for k, (la, lo, src) in ionian.items():
        add(k, la, lo, src, BACKGROUND_MARGINS, columns(["sun", "moon"], []),
            "sensitivity (DESIGN 0): the Ionian sites of the eclipse sensitivities (5.6, 6.2 pool ii); "
            "the eclipse circumstances come from eclipses.py, the table serves daylight and twilight",
            ["sun", "moon"], [])
    neg = json.loads((P / "negatives.json").read_text(encoding="utf-8"))
    place_sets: dict[tuple, list] = {}
    place_src: dict[tuple, str] = {}
    for s in neg["sets"]:
        for i, p in enumerate(s.get("observer_places") or []):
            ll = (p["lat"], p["lon"])
            place_sets.setdefault(ll, []).append(s["set"])
            place_src.setdefault(ll, f"negatives.json {s['set']} observer_places[{i}]: {p['place']} "
                                     f"({p.get('coord_source', '')})")
    for ll, sets_ in place_sets.items():
        key = NEG_KEYS[ll]
        bodies, stars, az, why = set(), set(), False, []
        for sid in dict.fromkeys(sets_):
            b, st, a, w = NEG_NEEDS[sid]
            bodies |= set(b)
            stars |= set(st)
            az = az or a
            why.append(f"{sid}: {w}")
        bodies = [b for b in M.BODIES if b in bodies]
        stars = [x for x in ALL_STARS if x in stars]
        add(key, ll[0], ll[1], place_src[ll], BACKGROUND_MARGINS, columns(bodies, stars, az),
            "negative control (6.5): the background with margins, only the columns its sets use (4.1)",
            bodies, stars, {"sets": list(dict.fromkeys(sets_)), "needs": why})
    real = json.loads((P / "controls_real.json").read_text(encoding="utf-8"))
    ctrl_src: dict[tuple, list] = {}
    for s in real["sets"]:
        for p in s["observer_place"]:
            c = p.get("search_coordinates")
            if c and isinstance(c.get("lat"), (int, float)):
                ctrl_src.setdefault((c["lat"], c["lon"]), []).append(
                    f"controls_real.json {s['set_id']} observer_place {p['place']}")
        for cl in s["clues"]:
            for o in cl.get("fork_options") or []:
                st = (o.get("operational") or {}).get("site")
                if isinstance(st, dict) and isinstance(st.get("lat"), (int, float)):
                    ctrl_src.setdefault((st["lat"], st["lon"]), []).append(
                        f"controls_real.json {s['set_id']} {cl['clue_id']} option {o['option']}")
    alm = json.loads((P / "controls_almagest.json").read_text(encoding="utf-8"))
    for s in alm["sets"]:
        c = s["observer_place"].get("search_coordinates")
        if c:
            ctrl_src.setdefault((c["lat"], c["lon"]), []).append(
                f"controls_almagest.json {s['set']} observer_place")
    planets = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"]
    for ll, srcs in ctrl_src.items():
        key = CTRL_POINTS[ll]
        alm_site = key in ("alexandria", "babylon")
        bodies = planets if alm_site else ["sun", "moon"]
        role = ("control (6.3, 6.4): the default site of the Almagest control (6.4)" if key == "alexandria" else
                "control (6.3, 6.4): Babylonian lunar eclipses (R-PTOL-BAB) and the Babylon sensitivity of ALM-K"
                if key == "babylon" else "control (6.3): a point option or observer place of controls_real.json")
        add(key, ll[0], ll[1], "; ".join(dict.fromkeys(srcs)) + " (modern approximate placement written by the "
            "drafter; the text gives only the name)", CONTROL_ENVELOPE, columns(bodies, [], az=alm_site),
            role, bodies, [],
            {"span_rule": "windows only (4.1): tables are built for the union of the set's window positions as "
                          "the harness places them (seeds.json; truth-side), each widened by the set's longest "
                          "link, and for I16(a)'s null windows; 'span' is the public envelope of every control "
                          "window (4.1) and reads no truth",
             "on_demand": "eclipse and lunar-eclipse circumstances, LAT and seasonal hours of a contact come "
                          "from eclipses.py and lunar.py at the instant, not from these tables"})
    doc = {
        "schema": "odybench sites v1 (DESIGN 0, 4.1, 10.2)",
        "written": WRITTEN,
        "fields": {"lat, lon": "degrees, east positive", "elev_m": "metres (sea level throughout)",
                   "span": "Julian years [y0, y1], inclusive (model.Site)",
                   "columns": "the SkyTable arrays the site needs (10.2 sky.py)",
                   "build.bodies, build.stars": "the bodies (model.BODIES) and stars (data/stars.json keys) "
                                                "sky.build fills; the arrays with a body or star axis hold "
                                                "only these",
                   "role, span_source, span_rule, sets, needs, build_extra, on_demand": "provenance and use; "
                   "model.Site takes key, lat, lon, elev_m, source, span and columns"},
        "spans": {"background": [-1999, 200], "data_margins": BACKGROUND_MARGINS,
                  "control_envelope": CONTROL_ENVELOPE,
                  "source": "4.1: background -1999..+200; data margins -2060..+241; every control window lies "
                            "inside -1999..+300"},
        "not_sites": "site boxes and discs of controls_real.json (the Greek box, Sicily, the Italian box, "
                     "Sardinia, Diodorus' disc and route box) are site rules evaluated on a grid by the searcher "
                     "(6.3.1), not table sites; AEN-TROY's Mount Ida is a landmark, the bearing target of its "
                     "'ida' rider, not an observer place (6.5)",
        "data_gaps": ["VF-LEMNOS-03:a names Mirfak (alpha Per), which data/stars.json does not hold; the star "
                      "must be fetched (tools/fetch_stars.py) or the option recorded as unevaluable before the "
                      "freeze (A3/A9)",
                      "the Almagest reference stars of the held-out rows are not in data/stars.json yet (11.1)"],
        "sites": out,
    }
    dump("sites.json", doc)
    return doc


# ---------------------------------------------------------------- windows

def ut2_bounds(y0, y1):
    """[start, end) JD (UT) of the UT+2 civil years y0..y1 inclusive."""
    a, b = C.span_bounds((y0, 1, 1), (y1, 12, 31), offset_hours=2.0)
    return [a, b]


def windows():
    named = {
        "reproduction": (-1249, -1114, "1250-1115 BC, 136 years: B&M's search window [B&M; win 9] (4.6)"),
        "primary": (-1349, -1099, "1350-1100 BC, 251 years [win 9] (4.6)"),
        "troy_viia": (-1239, -1149, "1240-1150 BC, 91 years: Troy VIIa [win 4, 9] (4.6)"),
        "eratosthenes_strict": (-1175, -1171, "1176-1172 BC: the strict Eratosthenes return [win 5-6] (4.6, 5.5)"),
    }
    out = {}
    for k, (y0, y1, src) in named.items():
        a, b = ut2_bounds(y0, y1)
        out[k] = {"years": [y0, y1], "n_years": y1 - y0 + 1, "jd_ut": [a, b], "n_days": b - a,
                  "clock": "UT+2", "source": src}
    spans = {
        "background": {"years": [-1999, 200], "jd_ut": ut2_bounds(-1999, 200), "clock": "UT+2",
                       "source": "4.1: -1999-01-01 to +200-12-31 (2,200 Julian years), from the first year of "
                                 "NASA's elements"},
        "core": {"years": [-1748, -51], "jd_ut": ut2_bounds(-1748, -51), "clock": "UT+2",
                 "source": "4.1: targets lie at least 251 years inside B, so every window of every width lies "
                           "inside it"},
        "data_margins": {"years": [-2060, 241], "source": "4.1: the 40-day clue offsets and the +/-60-day "
                                                          "Mercury searches"},
        "control_envelope": {"years": [-1999, 300], "source": "4.1: every control window lies inside -1999..+300"},
        "null_window_range": {"years": [-1000, 300],
                              "source": "6.3.2 [r3v7 R3-7]: I16(a)'s 21 null windows per counted set lie within "
                                        "-1000..+300, each so that every event the set's rows can link to, at "
                                        "the set's longest link or day offset in either direction, lies inside "
                                        "-1999..+300"},
        "epoch_band": {"years": [-1877, -477], "source": "4.2, 7.2: P_BM,E and P_MWRA,E, Day 0 (UT+2) within "
                                                         "+/-700 years of the target's year"},
        "epoch_band_halves": {"early": [-1877, -1178], "late": [-1177, -477],
                              "source": "7.2: Q_exch's drift tests inside the band"},
        "background_halves": {"early": [-1999, -900], "late": [-899, 200], "source": "7.3, R21"},
        "p8_ends": {"first": [-1999, -1300], "last": [-499, 200],
                    "source": "8.2 P8: the first and last 700 years of the background (7.2 notes the "
                              "difference from the epoch band)"},
    }
    doc = {
        "schema": "odybench windows v1 (DESIGN 4.6, 4.1)",
        "written": WRITTEN,
        "rule": "A window of width W years is the half-open JD interval [a, a + 365.25 W) (4.6). A named window "
                "below runs from 0 h UT+2 of 1 Jan of its first year to 0 h UT+2 of 1 Jan after its last year, "
                "half-open; a candidate is inside if its UT+2 Day 0 (day0_jdn_ut2) is.",
        "named": out,
        "spans": spans,
        "widths": {"rule": 136, "doc": [91, 136, 251], "n1_sliding": [50, 91, 100, 136, 200, 251, 500, 900],
                   "controls": 136, "negatives": [136, 251],
                   "source": "5.3 F7 (136 BM; 91, 251 DOC); 5.1 item 5; 6.3.1 and 6.4 (136); 6.5 (the Odyssey's "
                             "two windows)"},
        "negatives": {"windows": ["reproduction", "primary"], "sensitivity_positions_per_width": 20,
                      "source": "6.5: each clean negative is searched in the Odyssey's own two windows at its own "
                                "site; twenty further random positions per width are a sensitivity (seeds.json)"},
        "controls": {"width_years": 136, "positions": "the harness places the anchor's accepted date at a uniformly "
                                                      "random position (seeds.json, per set), plus twenty further "
                                                      "positions as a sensitivity; I16(a)'s 21 null windows per "
                                                      "counted set lie in null_window_range",
                     "source": "6.3.1, 6.3.2, 6.4, 4.6"},
    }
    dump("windows.json", doc)
    return doc


# ------------------------------------------------------------------ seeds

def seed_of(purpose, key):
    h = hashlib.sha256(f"odybench|{purpose}|{key}".encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big")


def seeds():
    real = json.loads((P / "controls_real.json").read_text(encoding="utf-8"))
    alm = json.loads((P / "controls_almagest.json").read_text(encoding="utf-8"))
    neg = json.loads((P / "negatives.json").read_text(encoding="utf-8"))
    pcr_sets = [s["set_id"] for s in real["sets"]]
    livy = ["H-LIVY:L1", "H-LIVY:L2", "H-LIVY:L3", "H-LIVY:L4"]
    alm_sets = [s["set"] for s in alm["sets"]]
    pcr_counted = ["R-PTOL-BAB", "R-PTOL-ALEX", "R-THUC", "R-XEN", "R-ARBELA", "R-PYDNA", "R-DIOD"]
    alm_counted = [s for s in alm_sets if s != "ALM-C"]
    neg_sets = [s["set"] for s in neg["sets"]]
    purposes = {
        "control_window": ([s for s in pcr_sets if s != "H-LIVY"] + livy + alm_sets,
                           "6.3.1, 6.4: the harness places each set's 136-year window so that its anchor's "
                           "accepted date falls at a uniformly random position (u = rng.random(); a = t_anchor - "
                           "u * 365.25 * 136); H-LIVY's notices are searched alone (6.3.5)"),
        "control_window_sensitivity": ([s for s in pcr_sets if s != "H-LIVY"] + livy + alm_sets,
                                       "6.3.2, 6.4: twenty further window positions per set, drawn as above"),
        "null_windows_I16a": (pcr_counted + alm_counted,
                              "6.3.2, I16(a): 21 null windows per counted set, placed at random around no truth "
                              "within windows.json spans.null_window_range, redrawn until every event the set's "
                              "rows can link to lies inside -1999..+300"),
        "negative_window_sensitivity": ([f"{s}:{w}" for s in neg_sets for w in (136, 251)],
                                        "6.5: twenty further random positions per width per set, inside the "
                                        "background with the core's margins"),
        "epics": (["A", "B"], "5.4: epics drawn per variant from a seeded stream, until 200 enter the stratum or "
                              "10^6 draws"),
        "epic_windows": (["A", "B"], "5.4: each stratum epic's 136-year window at a random position (p_N4)"),
        "pcs_truths": (["pool_i", "instrument_200"], "6.2: pool (i), 2,000 daylight conjunctions drawn from T; the "
                                                     "instrument mode's 200 truths drawn from pool (i)"),
        "pcs_noise": (["science"], "6.2: offset jitter and displacement draws of the noise study"),
        "I2c_monte_carlo": (["mixture"], "6.1 I2(c): a 10^6-draw Monte Carlo of the four-model mixture"),
        "I4_pages": (["convention_check"], "6.1 I4: three LEcat5 century pages for the convention check"),
        "I5_events": (["horizons_1000", "check_mwra_2000"], "6.1 I5: 1,000 random events (Sun, Moon, Venus, "
                                                             "Mercury, Jupiter; Ithaki, Alexandria, Troy; "
                                                             "-1999..+300) and 2,000 events for (b)"),
        "I6b_events": (["horizons_200"], "6.1 I6(b): 200 random stations, greatest elongations and oppositions"),
        "I7_years": (["background_300"], "6.1 I7: 300 random background years"),
        "I9_synthetic": (["reach_10000", "cores_2000"], "6.1 I9: (a) 10,000 random synthetic survivor sets; "
                                                         "(b) 2,000 synthetic cores of 243-year blocks"),
        "G_bootstrap": (["block_136", "block_243"], "5.3: moving-block bootstrap of G, 10,000 resamples "
                                                    "(136-year blocks; 243-year blocks reported)"),
        "bessel_vec_check": (["pairs_1000"], "10.2 bessel_vec.check: 1,000 random site-eclipse pairs"),
        "reading_sample": ([s for s in pcr_sets if s != "H-LIVY"] + alm_sets,
                           "6.3.2: the fraction of readings that make the truth the unique strict survivor, "
                           "sampled to 10,000 fork combinations where there are more"),
        "n1_permutation": (["venus_mercury"], "5.1 item 7: 10,000 permutations of the Venus outcome"),
        "I12_lunations": (["yallop_500"], "6.1 I12: 500 lunations"),
        "heldout_simulation": (["test_heldout"], "10.5 test_heldout.py: exactness under exchangeability by "
                                                 "simulation"),
    }
    out = {}
    for purpose, (keys, src) in purposes.items():
        out[purpose] = {"source": src, "seeds": {k: seed_of(purpose, k) for k in keys}}
    doc = {
        "schema": "odybench seeds v1 (DESIGN 4.6, 5.4, 6.1-6.5)",
        "written": WRITTEN,
        "rule": "seed(purpose, key) = the first 8 bytes, big-endian, of SHA-256('odybench|<purpose>|<key>') as an "
                "unsigned integer; no seed is chosen by hand. Draws use numpy.random.default_rng(seed) (PCG64), "
                "one generator per (purpose, key), consumed in the order the owning module documents.",
        "generator": "numpy.random.default_rng",
        "purposes": out,
    }
    dump("seeds.json", doc)
    return doc


# ------------------------------------------------------------- delta-T models

def deltat_models():
    doc = {
        "schema": "odybench deltat_models v1 (DESIGN 0, 2.3, 6.3.3, 10.2)",
        "written": WRITTEN,
        "argument": "the Julian epoch of the TT instant, calendar.julian_epoch(JD_TT) = 2000 + (JD_TT - 2451545)/365.25 "
                    "(DESIGN 0; identical to ephem.julian_epoch)",
        "models": [
            {"key": "smh2020", "ephem_model": "smh2020",
             "definition": "Addendum 2020 spline (Table S15 v2020) for -720..2019; before -720 the HMNAO lod integral "
                           "lod = +1.72 t - 3.5 sin(2 pi (t + 0.75)/14) ms, t = (y - 1825)/100, continuous at -720",
             "sigma": "HMNAO's error estimate epsilon, interpolated (ephem.sigma_smh2020); before -2000 an "
                      "extrapolation, 0.74e-4 (y - 1825)^2, not a published value",
             "ndot_frame": -25.82, "pairs_with": "DE431 (the DE430 lunar model)",
             "value_at_-1176.68": [28543, 720],
             "source": "DESIGN 0, 2.3; eph 2.1-2.3 [ADD20; HMNAO]"},
            {"key": "smh2020_parabola", "ephem_model": "smh2020_parabola",
             "definition": "Addendum 2020 eq. 5.1: -10 + 31.4 tau^2, tau = (y - 1825)/100",
             "sigma": "0.6 tau^2 (ephem.sigma_parabola)", "ndot_frame": -25.82, "pairs_with": "DE431",
             "value_at_-1176.68": [28282, 541], "source": "DESIGN 0, 2.3; eph 2.1 [ADD20]"},
            {"key": "smh2016_parabola", "ephem_model": "smh2016_parabola",
             "definition": "SMH2016 eq. 4.1: -320.0 + 32.5 tau^2, tau = (y - 1825)/100",
             "sigma": "0.6 tau^2 (ephem.sigma_parabola)", "ndot_frame": -25.82, "pairs_with": "DE431",
             "value_at_-1176.68": [28963, 541], "source": "DESIGN 0, 2.3; eph 2.1 [SMH16]"},
            {"key": "em_canon", "ephem_model": "em2006_canon",
             "definition": "Espenak-Meeus polynomials (Morrison-Stephenson 2004 parabola -20 + 32 u^2, "
                           "u = (y - 1820)/100, before -500) plus c = -0.000012932 (y - 1955)^2 for the canon's "
                           "n-dot -25.858",
             "sigma": "Huber 2000 before -500 (ephem.sigma_huber, calibration year -500, M = 2500, Q = 0.058); "
                      "Morrison-Stephenson 2004's 0.8 u^2 from -500 on (ephem.sigma_ms2004), as on NASA's page; "
                      "the envelope is discontinuous at -500. ephem.delta_t_sigma('em2006_canon') returns Huber "
                      "only (0 from -500 to 2005), so deltat_mix must apply this rule itself",
             "ndot_frame": -25.858, "pairs_with": "NASA's Besselian elements (the canon frame)",
             "value_at_-1176.68": [28589, 1008],
             "source": "DESIGN 0, 2.3; eph 2.1 [EM06]; acq 2.2; tools/jsex_sites.js"},
        ],
        "mixture": {
            "weights": [0.25, 0.25, 0.25, 0.25],
            "form": "each model a Gaussian with its stated sigma (an assumption, stated every time it is used, "
                    "DESIGN 0)",
            "p_exact": {"span_sigma": 6.0, "scan_s": 10.0, "tol_s": 0.1,
                        "rule": "over [min(mu - 6 sigma), max(mu + 6 sigma)], the mean over the four models of the "
                                "sum over passing intervals of Phi((b - mu)/(s sigma)) - Phi((a - mu)/(s sigma)); "
                                "intervals by a 10-s scan and bisection to 0.1 s (10.2, 6.3.3)"},
            "pass_threshold": 0.5,
            "reported_thresholds": [0.05, 0.95],
            "noncirc_sigma_scale": 3.0,
            "grid_diagnostic": {"n": 41, "note": "never a rule input (10.2)"},
            "source": "DESIGN 0, 6.3.3, 10.2 deltat_mix"},
        "frames": {
            "canon": {"ndot": -25.858, "used_by": "solar rows, h_tot, h_09, h_06 (NASA's elements)"},
            "de431": {"ndot": -25.82, "used_by": "lunar rows and lunar-timed quantities (DE431)"},
            "conversion": "dT(to) = dT(from) + ephem.ndot_correction(y, ndot_to, ndot_from), "
                          "ndot_correction = -0.91072 (ndot_to - ndot_from) T^2, T = (y - 1955)/100; "
                          "SMH -> canon is +34 s at -1177 (DESIGN 0, 2.3; eph 2.3)",
            "source": "DESIGN 0 ('Delta-T travels with its lunar ephemeris'); eph 2.3, 5.3"},
        "fixed_values": {
            "bm_clock_s": {"value": 27602.7, "use": "T0b's clock only (DESIGN 0, 3.2); uninterpretable, never "
                                                    "converted into another frame (2.3, 5.6)"},
            "sky_tables": {"value": "smh2020", "use": "the default dt_model of sky.build (10.2)"}},
    }
    dump("deltat_models.json", doc)
    return doc


# ------------------------------------------------------------------- slots

def slots():
    venus_v0 = {"rule": "rises_before_sun_visible", "sun_alt_max_at_venus_rise_deg": -7.0,
                "text": "Venus rises before the Sun, with the Sun at or below -7 deg at Venus' rising (a visible "
                        "morning star, AV 7 deg)"}
    venus_v4 = {"rule": "rise_lead_min", "lead_min": 60.0, "text": "Venus rises at least 60 min before the Sun"}
    events = ["rise_azimuth_max_vertex", "greatest_western_elongation", "morning_station"]
    vis = {"sun_alt_max_at_mercury_rise_deg": -10.0, "text": "visible: Sun at or below -10 deg at Mercury's rising"}

    def merc(k, mode):
        return {"events": events, "k_days": k, "continuous": True, "combine": mode,
                "visibility": vis if mode != "event" else None}

    doc = {
        "schema": "odybench slots v1 (DESIGN 4.2)",
        "written": WRITTEN,
        "purpose": "A slot defines the categorical reading formed with the target in view (5.3). Nothing in the "
                   "record fixes its width, so the bench freezes a family and uses it against the claim (4.2) "
                   "[r2 R2-2].",
        "day_counts": {"sequential": {"C": [-29, -12], "venus": -5, "mercury": -34},
                       "parallel": {"C": [-28, -11], "venus": -4, "mercury": -33},
                       "pairing": "C, the Venus slot and the Mercury slot hold on one count; a target is in T_A(v) "
                                  "if either count passes as a whole (revision 3's mixing is withdrawn) [r2 R2-2]",
                       "day0": "the UT+2 conjunction date, the Day 0 and count of P_spring (4.2)"},
        "combine_modes": {"event_and_visible": "the event within k days, and Mercury visible on the slot day",
                          "event_or_visible": "the event within k days, or Mercury visible",
                          "event": "the event within k days"},
        "variants": {
            "v0": {"venus": venus_v0, "mercury": merc(6.0, "event_and_visible"), "n_A_design": 82,
                   "label": "documented",
                   "source": "V: MacDonald identifies the herald as Venus, the morning star of that spring "
                             "[unread 2.1, 2.5], with de Jong's AV [vis 1.2]. M: B&M name the three events and "
                             "require Mercury visible [B&M References]; 6 d is the slack of Ptolemy's Mercury "
                             "records, all 14 within 5.5 d [alm 4]"},
            "v1": {"venus": venus_v0, "mercury": merc(6.0, "event_or_visible"), "n_A_design": 131,
                   "label": "revision 3", "source": "[v3 4.2]"},
            "v2": {"venus": venus_v0, "mercury": merc(6.0, "event"), "n_A_design": 87, "label": "",
                   "source": "DESIGN 4.2"},
            "v3": {"venus": venus_v0, "mercury": merc(4.0, "event"), "n_A_design": 66, "label": "",
                   "source": "4.0 d: 12 of the 14 Almagest records [alm 4]"},
            "v4": {"venus": venus_v4, "mercury": merc(6.0, "event_or_visible"), "n_A_design": 101, "label": "",
                   "source": "the FULL-tier herald threshold [vis 1.3]"},
            "v5": {"venus": venus_v4, "mercury": merc(4.0, "event"), "n_A_design": 56, "label": "",
                   "source": "DESIGN 4.2"},
        },
        "rule_family": ["v0", "v1", "v2", "v3", "v4", "v5"],
        "reported": {
            "v6": {"venus": {"rule": "western_elongation_near_apparition_max", "within_deg": 2.0,
                             "text": "Venus' western elongation within 2 deg of the apparition's maximum"},
                   "mercury": merc(6.0, "event_and_visible"),
                   "in_rule": False,
                   "source": "DESIGN 4.2: reported, not in the family, because its width is set by the target's "
                             "own value. Its Mercury slot is not stated; v0's is used [A0]"}},
        "use": {"label_2_G_leg_and_Q_tol": "the variant most favourable to B&M, the smallest G_BM,lo (4.2, 9.2)",
                "Q_slot": "printed when a decision differs between variants (4.2, 9.2)",
                "held_out": "the held-out test does not use T_A, so outcome 1 does not depend on the slots (4.2, 7.2)",
                "identity": "every reading of G_BM* implies the slots of v1-v5, so G(G_BM*, T) = (n_A(v)/n_T) "
                            "G(G_BM*, T_A(v)) exactly for v1-v5 (4.2; checked by I9(c))"},
        "n_A_source": "design-stage counts of 2.9 (the recheck's rough rows); recomputed by attain.py at the "
                      "null-side stage",
    }
    dump("slots.json", doc)
    return doc


# ------------------------------------------------------------ verdict rule

def verdict_rule():
    text = (ROOT / "DESIGN.md").read_text(encoding="utf-8")
    i = text.index("### 9.2 The rule")
    j = text.index("```", i)
    k = text.index("```", j + 3)
    rule_text = text[j + 3:k].strip("\n")
    doc = {
        "schema": "odybench verdict_rule v1 (DESIGN 9.1, 9.2)",
        "written": WRITTEN,
        "rule_text": rule_text,
        "rule_text_source": "DESIGN 9.2, verbatim; odybench/verdict_rule.py implements exactly this",
        "thresholds": {
            "gate_3a": {"legs": ["AL_bf", "AL_st", "WO_bf", "WO_st"], "n_counted": 7, "fires_if_min_below": 4,
                        "q_score3a_if_max_at_least": 4,
                        "counted_sets": ["R-PTOL-BAB", "R-PTOL-ALEX", "R-THUC", "R-XEN", "R-ARBELA", "R-PYDNA",
                                         "R-DIOD"],
                        "variants": ["main", "redraft", "sibling", "noncirc"],
                        "source": "6.3.2, 9.2: fewer than half of 7, rounded up"},
            "gate_3b": {"legs": [["bf", "fine"], ["bf", "mid"], ["bf", "coarse"], ["st", "fine"], ["st", "mid"],
                                 ["st", "coarse"]],
                        "n_counted": 11, "fires_if_min_below": 6, "q_score3b_if_max_at_least": 6,
                        "counted_sets": ["ALM-A", "ALM-B", "ALM-D", "ALM-E", "ALM-F", "ALM-G", "ALM-H", "ALM-I",
                                         "ALM-J", "ALM-K", "ALM-L"],
                        "reported_only": ["ALM-C"],
                        "meanings": {"frozen": "same_apparition", "other": "same_apparition_side (no label; "
                                                                           "Q_score3b)"},
                        "reported_lines": [0.04, 0.06],
                        "source": "6.4, 9.2: fewer than half of 11, rounded up"},
            "seen": {"narrowing_fraction": 0.05,
                     "rule": "seen (strict): truth in S0 and |S0| <= 0.05 N_cand; seen (best fit): truth in B and "
                             "|B| <= 0.05 N_cand",
                     "cluster_days": 3, "source": "6.3.2"},
            "narrowable": {"min_windows": 11, "of_windows": 21, "fraction": 0.05,
                           "q_attain3a_if_N_narrow_below": 4, "q_attain3b_if_N_narrow_below": 6,
                           "printed_only_beside_a_firing_gate": True, "source": "6.3.2, 6.4, 9.2 [r3v7 R3-8]"},
            "q_bm": {"rec_ALM_BM_below": 6, "source": "6.4, 9.2"},
            "q_h": {"held_ALM_below": 6, "p_max": 0.05, "steps": ["fine", "mid", "coarse"],
                    "held_ALM_max_by_construction": 8, "source": "6.4, 9.2"},
            "q_exposure": {"rule": "fire3a(redraft) != fire3a(main) or fire3a(sibling) != fire3a(main)",
                           "source": "6.3.4, 9.2"},
            "q_dt": {"rule": "fire3a(noncirc) != fire3a(main)", "sigma_scale": 3.0, "source": "6.3.3, 9.2"},
            "q_attain": {"p_H_min_above": 0.05, "source": "7.2, 9.2"},
            "q_exch": {"fisher_two_sided_p_max": 0.05, "n_tests": 6, "source": "7.2, 9.1 [r2v6 N9]"},
            "label_2": {"g2_G_BM_lo_at_least": 0.20, "pct_N4_lo_at_least": 0.50, "no_match_if_r_Ody": 0.0,
                        "source": "5.3, 5.4, 9.2"},
            "q_tol": {"G_BM_lo_above": 0.05, "all_variants": True, "source": "5.3, 9.2"},
            "q_slot": {"rule": "g2 or tol differs between slot variants", "variants": ["v0", "v1", "v2", "v3",
                                                                                      "v4", "v5"],
                       "source": "4.2, 9.2"},
            "label_1": {"requires_T0_pass": True, "p_H_max": 0.05,
                        "pools": ["P_BM", "P_MWRA", "P_BM_E", "P_MWRA_E"], "p_H": "the largest of the four p_P; "
                        "p_P = 1 if the target is not a member", "source": "7.2, 9.2"},
            "label_4": {"rule": "some clean negative j has hit_j and G_j_hi <= G_BM_u_lo", "source": "6.5, 9.2"},
            "q_attain4": {"m_hat": 0.304, "rule": "no clean negative has 0 < G_j, G_j_hi <= G_BM_u_lo and "
                                                  "hit_j(m_hat); never printed beside a label 4",
                          "source": "4.4, 6.5, 9.2 [r3v7 R3-2]"},
            "u0": {"rule": "U0(n) = 3.69 / n", "coefficient": 3.69, "source": "5.3, 9.2"},
            "pass_rule_dt": {"p_mix_at_least": 0.5, "source": "6.3.3, 10.3"},
        },
        "clean_negatives": ["AEN-TROY", "AEN-CRETE", "AEN-ITALY", "AEN-ETNA", "AEN-CARTHAGE", "ARG-CIUS",
                            "ARG-COLCHIS", "ARG-RETURN", "QS-SACK", "VF-LEMNOS", "VF-CYZICUS", "VF-COLCHIS"],
        "comparison_only": ["IL-PATROCLUS"],
        "labels": ["1", "2 (no match)", "2 (ordinary)", "3a", "3b", "4", "inconclusive", "BLOCKED"],
        "qualifiers": ["Q_contra", "Q_exch", "Q_score3a", "Q_score3b", "Q_attain3a", "Q_attain3b", "Q_BM", "Q_H",
                       "Q_exposure", "Q_dT", "Q_attain", "Q_record", "Q_tol", "Q_slot", "Q_attain4"],
        "headline_order": ["Q_contra", "label 1 (with Q_exch beside it)", "3a and 3b", "label 2", "label 4",
                           "Q_attain, Q_record, Q_attain4, Q_attain3a, Q_attain3b"],
        "headline_source": "9.3",
        "instr": {"checks": ["I1", "I2", "I2b", "I4", "I5", "I6", "I7", "I8", "I9", "I11", "I13", "I14", "I15",
                             "I16"],
                  "reported_beside": ["I3", "I10", "I10b", "I12"],
                  "rule": "verdict.py refuses to run unless INSTR holds; the verdict is BLOCKED",
                  "source": "6.1, 9.1, 9.2"},
    }
    dump("verdict_rule.json", doc)
    return doc


if __name__ == "__main__":
    sites()
    windows()
    seeds()
    deltat_models()
    slots()
    verdict_rule()
