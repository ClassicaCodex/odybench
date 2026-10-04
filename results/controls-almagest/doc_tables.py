"""Markdown tables for docs/controls-almagest.md from records.py and slack.json.
    py results/controls-almagest/doc_tables.py > results/controls-almagest/doc_tables.md"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1]))
import records as RC                 # noqa: E402
from odybench import ephem as E      # noqa: E402
sys.stdout.reconfigure(encoding="utf-8")
RC.resolve()
SL = {}
for o in json.loads((HERE / "slack.json").read_text(encoding="utf-8")):
    SL.setdefault(o["id"], {})[o["reading"]] = o
MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
PH = {"GE": "at greatest elongation", "nearGE": "about greatest elongation", "GEold": "star relation (Ptolemy: near GE)",
      "beforeGE": "before greatest elongation", "afterGE": "after greatest elongation", "occ": "conjunction / occultation",
      "pos": "position (star / Moon)", "opp": "opposition to mean Sun", "ecl": "lunar eclipse", "equinox": "spring equinox",
      "moonsun": "Sun-Moon distance"}
SIDE = {"E": "evening", "W": "morning"}


def civ(r, month=None, day=None):
    jd = RC.nab_jd_noon(r["nab"], month or r["month"], day or r["day"]) + RC.civil_day_offset(r["part"])
    y, m, d, _ = E.julian_from_jd(jd)
    return f"{d} {MON[m-1]} {('AD ' + str(y)) if y > 0 else (str(1 - y) + ' BC')} ({y})"


def tw(r):
    p, h = r["part"], r.get("hours")
    return {"evening": "evening", "morning": "dawn", "noon": "noon"}.get(p) or \
        {"h_before_midnight": f"{h:g} h before midnight", "h_after_midnight": f"{h:g} h after midnight",
         "h_after_noon": f"{h:g} h after noon", "h_before_noon": f"{h:g} h before noon"}[p]


def f(x, n=1):
    return "–" if x is None else f"{x:+.{n}f}"


print("### Table 1. Inventory\n")
print("| id | ref | date as stated (era; Egyptian day; time) | observer | body | stated phenomenon | civil date (Julian, astr. year) | Ptolemy mean Sun: stated / his tables |")
print("|---|---|---|---|---|---|---|---|")
n_ms = n_ok = 0
for r in RC.R:
    ph = PH.get(r["phen"], r["phen"])
    if r.get("side"):
        ph = f"{SIDE[r['side']]}; {ph}"
    dbl = "εἰς τὴν" in (r["date_words"] + (r.get("date_words_nab") or "")) or r["id"] in ("IX.10.6b",)
    nxt = f"{r['day']+1}" if r["day"] < 30 else f"{RC.MONTHS[r['month']]} 1"
    eg = f"Nab {r['nab']} {RC.MONTHS[r['month']-1]} {r['day']}" + (f"/{nxt}" if dbl else "")
    ms, _ = RC.ptolemy_mean_sun(r)
    st = r.get("ptol_mean_sun")
    if st is not None:
        n_ms += 1
        d = ((st - ms + 180) % 360) - 180
        ok = abs(d) <= 0.12
        n_ok += ok
        msc = f"{st:.2f} / {ms:.2f}" + ("" if ok else " **x**")
    else:
        msc = "–"
    date = civ(r)
    if r.get("emend"):
        date += f"; emended {civ(r, r['emend']['month'], r['emend']['day'])}"
    print(f"| {r['id']} | {r['ref']} | {r['era']}; {eg}; {tw(r)} | {r['observer'].split(' (')[0]} | {r['body']} | {ph} | {date} | {msc} |")
print(f"\nMean-Sun statements reproduced to <= 0.12 deg: {n_ok} of {n_ms}.\n")
print("### Table 1b. What each record measures, and the words for the phenomenon\n")
print("| id | what is measured / stated | phenomenon words |")
print("|---|---|---|")
for r in RC.R:
    print(f"| {r['id']} | {r['measured']} | {r['phen_words']} |")
print()

print("### Table 2. Mercury and Venus: offset of the record from the DE441 event (days, record minus event)\n")
print("| id | reading | stated | elong. at record (deg) | true GE (deg) | rec − true GE | rec − mean-Sun GE | short of max (deg) | days within 0.5 / 1 deg of max | rise lead / set lag (min) | Mercury horizon-azimuth: rec − nearest max / min |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for r in RC.R:
    for tag, o in SL[r["id"]].items():
        if "ge_true_val" not in o:
            continue
        rs = "–" if o["rs_min"] is None else f"{o['rs_kind']} {o['rs_min']:.0f}"
        az = f"{f(o.get('az_max_off_d'))} / {f(o.get('az_min_off_d'))}" if "az_kind" in o else "–"
        print(f"| {r['id']} | {tag.split(':')[0]} | {SIDE[r['side']]}, {PH[r['phen']]} | {o['elong_true']:+.2f} | {o['ge_true_val']:+.2f} | "
              f"**{f(o['off_ge_true_d'])}** | {f(o['off_ge_mean_d'])} | {o['deficit_deg']:.2f} | {o['plateau_0p5']} / {o['plateau_1p0']} | {rs} | {az} |")

print("\n### Table 3. Oppositions (days, record minus DE441 opposition)\n")
print("| id | body | record instant (UT) | to true Sun | to mean Sun |")
print("|---|---|---|---|---|")
for r in RC.R:
    o = SL[r["id"]]["printed"]
    if "off_opp_true_d" in o:
        print(f"| {r['id']} | {r['body']} | {o['date'].split(' (')[0]} | {f(o['off_opp_true_d'], 2)} | {f(o['off_opp_mean_d'], 2)} |")

print("\n### Table 4. Planet-star relations at the record instant (deg; ecliptic of date, geocentric)\n")
print("| id | reading | relation in the words | computed | implied day offset |")
print("|---|---|---|---|---|")
for r in RC.R:
    for tag, o in SL[r["id"]].items():
        for s in o.get("stars", []):
            k = s["kind"]
            if k == "offset":
                comp = f"{s['star']}: sep {s['sep']:.2f}; dlon {s['dlon_c']:+.2f}, dlat {s['dlat_c']:+.2f}"
                imp = f(s.get("implied_day_offset"))
            elif k == "line_east":
                comp = f"{s['dist_c']:+.2f} from the {s['star']}-{s['star2']} line (stated {s['dist_s']:+.2f})"
                imp = f(s["implied_day_offset"])
            elif k == "heads_line":
                comp = f"{s['perp_c']:+.2f} off the Castor-Pollux line; {s['beyond_pollux_c']:.2f} beyond Pollux (stated {s['beyond_pollux_s']:.2f})"
                imp = f(s["implied_day_offset"])
            elif k == "conj":
                comp = f"{s['star']}: sep {s['sep']:.2f} at record; closest {s['closest_sep']:.2f} at rec {s['off_closest_d']:+.2f} d"
                imp = f"{s['off_closest_d']:+.1f} (closest)"
            elif k == "nearest":
                comp = f"nearest candidate {s['star']} at {s['seps'][s['star']]:.2f}; dlon {s['dlon_c']:+.2f}"
                imp = f(s["implied_day_offset"])
            else:
                continue
            print(f"| {r['id']} | {tag.split(':')[0]} | {s['reading']} | {comp} | {imp} |")

print("\n### Table 5. Lunar records (topocentric at Alexandria)\n")
print("| id | relation in the words | computed | implied time error | Moon elongation, illuminated fraction | days since / to conjunction |")
print("|---|---|---|---|---|---|")
for r in RC.R:
    o = SL[r["id"]]["printed"]
    m = o.get("moon")
    if not m:
        continue
    if "dlon_c" in m:
        rel = r["moon"]["reading"]
        comp = f"body − Moon dlon {m['dlon_c']:+.2f}, dlat {m['dlat_c']:+.2f}"
        imp = "–" if m.get("implied_hours") is None else f"{m['implied_hours']:+.1f} h"
    else:
        ms = o["moonsun"]
        rel = r["moonsun"]["reading"].split(":")[0]
        comp = f"Moon − Sun {ms['computed']:+.2f} (stated {ms['stated']:+.2f})"
        imp = f"{ms['implied_hours']:+.1f} h"
    print(f"| {r['id']} | {rel} | {comp} | {imp} | {m['elong_signed']:+.1f}, {m['illum']:.2f} | {m['age_d']:.2f} / {m['to_next_d']:.2f} |")

print("\n### Table 6. Eclipse and equinox\n")
for r in RC.R:
    o = SL[r["id"]]["printed"]
    if "eclipse" in o:
        e = o["eclipse"]
        print(f"- {r['id']}: DE441 greatest eclipse {e['date'].split(' (')[0]}, local apparent time {e['lat_hours']:.2f} h at Alexandria "
              f"(Ptolemy: 23 h); umbral magnitude {e['umbral_mag']:.2f} (Ptolemy 5/6 = 0.83); Moon {e['moon_minus_axis_lat']:+.2f} deg "
              f"from the shadow axis in latitude (negative = south, so the north limb is eclipsed: 'from the north'); "
              f"record − DE441 {e['off_h']:+.2f} h.")
    if "equinox" in o:
        q = o["equinox"]
        print(f"- {r['id']}: DE441 spring equinox {q['date'].split(' (')[0]}; Ptolemy's stated instant minus DE441 = {q['off_d']:+.2f} d.")

# summary of GE slack
print("\n### Summary: |record − true greatest elongation| for records the text puts at or about greatest elongation\n")
for body in ("mercury", "venus"):
    vals = []
    for r in RC.R:
        if r["body"] != body or r["phen"] not in ("GE", "nearGE", "GEold"):
            continue
        tags = list(SL[r["id"]])
        tag = [t for t in tags if t.startswith("emended")][0] if r["id"] == "IX.7.11" else "printed"
        vals.append((r["id"], abs(SL[r["id"]][tag]["off_ge_true_d"]), abs(SL[r["id"]][tag]["off_ge_mean_d"])))
    vals.sort(key=lambda x: x[1])
    ks = [1, 2, 3, 4, 6, 10, 17, 21]
    line = ", ".join(f"<= {k} d: {sum(v[1] <= k for v in vals)}/{len(vals)}" for k in ks)
    linem = ", ".join(f"<= {k} d: {sum(v[2] <= k for v in vals)}/{len(vals)}" for k in ks)
    print(f"- {body} (n = {len(vals)}; IX.7.11 at its emended date, IX.9.4 as printed): true Sun {line}")
    print(f"  - mean Sun: {linem}")
    print(f"  - sorted: " + ", ".join(f"{a} {b:.1f}" for a, b, _ in vals))
