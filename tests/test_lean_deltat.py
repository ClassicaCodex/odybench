"""
Tests of deltat.py (N6; agent L2; LEAN.md, DESIGN 5.6, 2.3, I2(c)).

    cd C:\\Projects\\odybench && py tests/test_lean_deltat.py

1. The port of program.js's getall() against program.js itself, run under
   Node (data/jsex/program.js in a vm context, as tools/jsex_sites.js runs
   it), over Delta-T offsets of -3000..+3000 s, for eclipses of -699..-600
   that exercise every branch (partial, annular, total, sunrise and sunset
   patterns) and for the two N6 eclipses.  Skipped (and reported) if Node is
   absent.
2. The port against NASA's site catalogues (deltat.selftest).
3. The canon-frame totality windows at Vathy against DESIGN 2.3's bisected
   values (28,801.02-29,584.91 s; 27,049.07-28,038.49 s, from the review's
   independent Besselian solver), and P(total) per model and for the mixture
   within I2(c)'s 0.005 of 2.3's table; the DE431 window against 2.3's
   28,761-29,545 s.
4. The probability helpers and the window search on synthetic predicates;
   the frames (+34 s at -1177); the refusal to write results/n6 before the
   second freeze.
These eclipse circumstances are the ones DESIGN 2.3 publishes; no planet is
evaluated.
"""
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np  # noqa: E402
import deltat as D  # noqa: E402
from odybench import ephem as E  # noqa: E402

NODE = shutil.which("node") or r"C:\Program Files\nodejs\node.exe"

JS = r"""
const fs = require('fs'), vm = require('vm'), path = require('path');
const dir = process.argv[2];
const req = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const out = [];
for (const file of Object.keys(req)) {
  const ctx = { Math, console };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(dir, 'program.js'), 'utf8'), ctx);
  let cap = null;
  ctx.calculatefor = function (el) { cap = el; };
  ctx.recalculate = function () {};
  vm.runInContext(fs.readFileSync(path.join(dir, file), 'utf8'), ctx);
  vm.runInContext(path.basename(file, '.js') + '()', ctx);
  for (const r of req[file]) {
    const o = ctx.obsvconst;
    o[0] = r.lat * Math.PI / 180; o[1] = -r.lon * Math.PI / 180; o[2] = 0; o[3] = 0;
    const tmp = Math.atan(0.99664719 * Math.tan(o[0]));
    o[4] = 0.99664719 * Math.sin(tmp); o[5] = Math.cos(tmp); o[6] = r.idx * 28;
    const dt0 = cap[5 + r.idx * 28];
    for (const dt of r.dts) {
      cap[5 + r.idx * 28] = dt;
      ctx.getall(cap);
      const m = ctx.mid;
      out.push({file, idx: r.idx, lat: r.lat, lon: r.lon, dt, mag: m[37], ratio: m[38], type: m[39],
                alt: m[32], h: m[16], t: m[1], vis: m[40]});
    }
    cap[5 + r.idx * 28] = dt0;
  }
}
console.log(JSON.stringify(out));
"""


def test_port_against_program_js():
    if not Path(NODE).exists():
        print("    SKIPPED: Node not found")
        return
    sites = [(38.37, 20.72), (39.62, 19.92), (37.78, 20.90)]
    files = {}
    els = {}
    for f, idxs in (("SEm0699.js", (27, 34, 59, 105, 131, 152, 206, 10, 100, 200)),):
        els[f] = list(D.load_jsex(D.JSEX_DIR / f).values())
        files[f] = [dict(idx=i, lat=la, lon=lo,
                         dts=[els[f][i][5] + d for d in range(-3000, 3001, 250)]) for i in idxs for la, lo in sites]
    keys78 = list(D.load_jsex(D.JSEX_DIR / "SEm1199.js"))
    els["SEm1199.js"] = list(D.load_jsex(D.JSEX_DIR / "SEm1199.js").values())
    files["SEm1199.js"] = [dict(idx=keys78.index(k), lat=la, lon=lo,
                                dts=list(np.arange(26000.0, 32001.0, 137.0)))
                           for k in ((-1177, 4, 16), (-1130, 9, 30)) for la, lo in sites + [D.VATHY]]
    with tempfile.TemporaryDirectory() as td:
        js, rq = Path(td) / "drive.js", Path(td) / "req.json"
        js.write_text(JS, encoding="utf-8")
        rq.write_text(json.dumps(files), encoding="utf-8")
        p = subprocess.run([NODE, str(js), str(D.JSEX_DIR), str(rq)], capture_output=True, text=True, timeout=300)
    assert p.returncode == 0, p.stderr
    rows = json.loads(p.stdout)
    worst = dict(mag=0.0, alt=0.0, h=0.0, t=0.0)
    types = set()
    for r in rows:
        el = els[r["file"]][r["idx"]]
        m = D.jsex_local(el, r["lat"], r["lon"], r["dt"])
        assert m["type"] == r["type"], (r, m)
        types.add((r["type"], r["vis"]))
        assert m["vis"] == r["vis"], (r, m)
        worst["mag"] = max(worst["mag"], abs(m["smag"] - r["mag"]))
        worst["alt"] = max(worst["alt"], abs(m["alt_deg"] - r["alt"] * 180 / math.pi))
        last = (12 + r["h"] * 180 / math.pi / 15) % 24
        worst["h"] = max(worst["h"], min(abs(m["lat_hours"] - last), 24 - abs(m["lat_hours"] - last)))
        worst["t"] = max(worst["t"], abs(m["tt_hours"] - (r["t"] + el[1])))
    print(f"    {len(rows)} program.js evaluations; (type, vis) seen {sorted(types)}; worst |diff|: "
          f"smag {worst['mag']:.1e}, alt {worst['alt']:.1e} deg, LAT {worst['h']:.1e} h, t {worst['t']:.1e} h")
    assert worst["mag"] < 1e-12 and worst["alt"] < 1e-9 and worst["h"] < 1e-9 and worst["t"] < 1e-9, worst
    assert {0, 1, 2, 3} <= {t for t, _ in types}
    assert {2, 3} & {v for _, v in types}                  # a sunrise or sunset pattern was exercised


def test_port_against_site_catalogues():
    assert D.selftest()


def test_windows_and_p_against_design_23():
    el78 = D.elements_for((-1177, 4, 16))
    el31 = D.elements_for((-1130, 9, 30))
    lat, lon = D.VATHY
    w = {}
    for k, el, (a, b) in (("78", el78, (28700.0, 29700.0)), ("31", el31, (26900.0, 28200.0))):
        ws = D.windows(D.nasa_pred(el, lat, lon), a, b, 10.0, keys=("total",))["total"]
        assert len(ws) == 1 and not ws[0][2] and not ws[0][3], ws
        w[k] = ws[0][:2]
    ref78, ref31 = D.REF_23["window_1178_canon"], D.REF_23["window_1131_canon"]
    assert max(abs(w["78"][0] - ref78[0]), abs(w["78"][1] - ref78[1])) < 0.1, w["78"]
    assert max(abs(w["31"][0] - ref31[0]), abs(w["31"][1] - ref31[1])) < 0.1, w["31"]
    y78 = float(E.julian_epoch(el78[0]))
    y31 = float(E.julian_epoch(el31[0]))
    c78, c31 = D.model_values(y78, "canon"), D.model_values(y31, "canon")
    p78 = {m: D.p_intervals(*c78[m], [w["78"]]) for m in D.MODELS}
    p31 = {m: D.p_intervals(*c31[m], [w["31"]]) for m in D.MODELS}
    p78["mixture"] = sum(p78[m] for m in D.MODELS) / 4
    p31["mixture"] = sum(p31[m] for m in D.MODELS) / 4
    for m, ref in D.REF_23["P78"].items():
        assert abs(p78[m] - ref) <= D.I2C_TOL, (m, p78[m], ref)
    for m, ref in D.REF_23["P31"].items():
        assert abs(p31[m] - ref) <= D.I2C_TOL, (m, p31[m], ref)
    assert abs(p78["mixture"] - 0.3076) < 0.001                  # 2.3's unrounded continuous value
    j = {m: D.joint_common_offset(c78[m][0], c78[m][1], [w["78"]], c31[m][0], [w["31"]]) for m in D.MODELS}
    for m in D.MODELS:
        assert abs(j[m] - D.REF_23["joint"][m]) <= D.I2C_TOL, (m, j[m])
    print(f"    Vathy windows {w['78'][0]:.2f}-{w['78'][1]:.2f} and {w['31'][0]:.2f}-{w['31'][1]:.2f} s; "
          f"P(total) mixture {p78['mixture']:.4f} / {p31['mixture']:.4f}")


def test_de431_window_against_design_23():
    el = D.elements_for((-1177, 4, 16))
    lat, lon = D.site_table()["ithaki"]
    pred = D.de_pred(lat, lon, el[0], E.EPHEM_DIR / "de431")
    lo = D.windows(pred, 28700.0, 28820.0, 40.0, tol=0.05, keys=("total",))["total"]
    hi = D.windows(pred, 29500.0, 29600.0, 50.0, tol=0.05, keys=("total",))["total"]
    a, b = lo[0][0], hi[0][1]
    ref = D.REF_23["window_1178_de431_smh"]
    assert abs(a - ref[0]) < 1.0 and abs(b - ref[1]) < 1.0, (a, b)
    print(f"    DE431 + SMH frame window at Ithaki {a:.2f}-{b:.2f} s (2.3: {ref[0]:,.0f}-{ref[1]:,.0f})")


def test_frames_and_sigmas():
    y = -1176.68
    c, o = D.model_values(y, "canon"), D.model_values(y, "own")
    for m in ("smh2020", "smh2020_parabola", "smh2016_parabola"):
        assert abs((c[m][0] - o[m][0]) - 33.9) < 0.2
    assert c["em_canon"] == o["em_canon"]
    ref = {"smh2020": (28543, 720), "smh2020_parabola": (28282, 541), "smh2016_parabola": (28963, 541),
           "em_canon": (28589, 1008)}                             # DESIGN 2.3, own frames
    for m, (mu, s) in ref.items():
        assert abs(o[m][0] - mu) < 1.0 and abs(o[m][1] - s) < 1.0, (m, o[m])
    assert abs(D.sigma_of("em_canon", -400.0) - float(E.sigma_ms2004(-400.0))) < 1e-9   # from -500: MS2004
    assert abs(D.sigma_of("em_canon", -600.0) - float(E.sigma_huber(-600.0))) < 1e-9


def test_helpers():
    assert abs(D.p_intervals(0.0, 1.0, [(-1.0, 1.0)]) - 0.682689492) < 1e-8
    assert abs(D.p_intervals(0.0, 1.0, [(-1.0, 0.0), (0.0, 1.0)]) - 0.682689492) < 1e-8
    # joint: windows [0, 10] and [5, 20] relative to mu 0 -> overlap [5, 10]
    j = D.joint_common_offset(0.0, 10.0, [(0.0, 10.0)], 0.0, [(5.0, 20.0)])
    assert abs(j - (D.phi(1.0) - D.phi(0.5))) < 1e-12
    assert D.joint_common_offset(0.0, 10.0, [(0.0, 1.0)], 0.0, [(2.0, 3.0)]) == 0.0
    pred = lambda x: {"total": 1000.0 < x < 1234.5, "mag09": x > 900.0}
    w = D.windows(pred, 0.0, 2000.0, 10.0, tol=0.01)
    assert len(w["total"]) == 1 and abs(w["total"][0][0] - 1000) < 0.01 and abs(w["total"][0][1] - 1234.5) < 0.01
    assert w["mag09"][0][3] is True                              # clipped at the scan's end
    pred2 = lambda x: {"total": (100 < x < 200) or (500 < x < 650), "mag09": False}
    w = D.windows(pred2, 0.0, 1000.0, 10.0)
    assert [round(a) for a, b, *_ in w["total"]] == [100, 500] and w["mag09"] == []
    assert D.jsex_file_for(-1177).name == "SEm1199.js" and D.jsex_file_for(-1100).name == "SEm1199.js"
    assert D.jsex_file_for(-1099).name == "SEm1099.js" and D.jsex_file_for(0).name == "SEm0099.js"
    assert D.jsex_file_for(1).name == "SE0001.js" and D.jsex_file_for(101).name == "SE0101.js"


def test_refuses_results_n6_before_freeze():
    if D.FROZEN.exists():
        print("    SKIPPED: results/attain/FROZEN exists")
        return
    assert D.main([]) == 2
    assert not (D.DEFAULT_OUT / "n6.json").exists()


if __name__ == "__main__":
    import time
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            t0 = time.time()
            try:
                fn()
                print(f"PASS {name} ({time.time() - t0:.1f} s)")
            except Exception as exc:          # noqa: BLE001
                fails += 1
                import traceback
                traceback.print_exc()
                print(f"FAIL {name}: {exc!r}")
    print("all passed" if not fails else f"{fails} failed")
    sys.exit(1 if fails else 0)
