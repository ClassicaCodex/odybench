// Local circumstances of every solar eclipse in NASA's Five Millennium Canon
// century files, at one site, using NASA's own JavaScript Solar Eclipse
// Explorer code (program.js, C. O'Byrne & F. Espenak, GPL) on the Canon's
// Besselian elements (Espenak & Meeus 2006, NASA/TP-2006-214141).
//
// This is results/window/jsex/local.js (research-window task, 2026-10-03)
// with two changes, made 2026-10-04 for the data-acquisition task:
//   1. the element directory is an argument (it was the script's own folder);
//   2. sigma(Delta-T) for years >= -500, where local.js returned 0, is the
//      Morrison & Stephenson (2004) parabola 0.8 u^2 s, u = (y-1820)/100, which
//      NASA's "Uncertainty in Delta T" page gives for 1000 BCE-1200 CE
//      (eclipse.gsfc.nasa.gov/SEcat5/uncertainty.html; copy in
//      data/refs/nasa/SEcat5_uncertainty.html).  Before -500 it is Huber
//      (2000) exactly as in local.js, so rows before -500 are unchanged.
//      A field "sigmaSrc" ("huber2000" | "ms2004") records which was used.
// Everything else (row format, the +/-2 sigma envelope in 0.1-sigma steps,
// the -0.3 deg visibility threshold) is local.js unchanged.
//
// Usage: node tools/jsex_sites.js <elementDir> <lat> <lonEast> <files...>  -> JSON lines
// (times: "utH" UT hours of maximum, "last" local apparent solar time; "date"
// the UT calendar date of maximum, proleptic Julian before 1582, astronomical
// years; "jdTD" the Canon's T0 on TD = TT.)
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const dir = path.resolve(process.argv[2]);

function loadElements(file) {
  const ctx = { Math, console };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(dir, 'program.js'), 'utf8'), ctx);
  let captured = null;
  ctx.calculatefor = function (el) { captured = el; };
  ctx.recalculate = function () {};
  const src = fs.readFileSync(path.join(dir, file), "utf8");
  vm.runInContext(src, ctx);
  const fname = path.basename(file, '.js');
  vm.runInContext(fname + '()', ctx);
  return { ctx, el: captured };
}

// Huber (2000) before -500 (as local.js); Morrison & Stephenson (2004) from -500 on.
function sigmaDT(year) {
  if (year >= -500) {
    const u = (year - 1820) / 100;
    return { s: 0.8 * u * u, src: 'ms2004' };
  }
  const cal = -500;
  const N = Math.abs(year - cal);
  return { s: 365.25 * N * Math.sqrt((N * 0.058 / 3) * (1 + N / 2500)) / 1000, src: 'huber2000' };
}

function setObserver(ctx, latDeg, lonEastDeg) {
  const o = ctx.obsvconst;
  o[0] = latDeg * Math.PI / 180;
  o[1] = -lonEastDeg * Math.PI / 180; // west longitude positive
  o[2] = 0;
  o[3] = 0; // UT
  const tmp = Math.atan(0.99664719 * Math.tan(o[0]));
  o[4] = 0.99664719 * Math.sin(tmp);
  o[5] = Math.cos(tmp);
}

function evalOne(ctx, el, i) {
  ctx.obsvconst[6] = i;
  ctx.getall(el);
  const mid = ctx.mid;
  const type = mid[39]; // 0 none 1 partial 2 annular 3 total
  const utH = mid[1] + el[1 + i] - (el[4 + i] - 0.5) / 3600.0;
  // hour angle of the Sun at the observer (radians) -> local apparent solar time
  let h = mid[16];
  let last = 12 + (h * 180 / Math.PI) / 15;
  last = ((last % 24) + 24) % 24;
  return {
    type, mag: mid[37], alt: mid[32] * 180 / Math.PI, vis: mid[40],
    date: ctx.getdate(el, mid), utH: ((utH % 24) + 24) % 24, last,
  };
}

const lat = parseFloat(process.argv[3]);
const lonE = parseFloat(process.argv[4]);
const files = process.argv.slice(5);
for (const f of files) {
  const { ctx, el } = loadElements(f);
  setObserver(ctx, lat, lonE);
  for (let i = 0; i < el.length; i += 28) {
    const nominal = evalOne(ctx, el, i);
    const year = parseInt(nominal.date.split('-').length > 3 ? '-' + nominal.date.split('-')[1] : nominal.date.split('-')[0], 10);
    const dtNom = el[5 + i];
    const sg = sigmaDT(year);
    const s = sg.s;
    // envelope over DeltaT within +/-2 sigma (shift only the hour-angle DeltaT, el[5])
    let maxMag1 = -1, maxMag2 = -1, anyTotal1 = false, anyTotal2 = false, anyCentral2 = false;
    for (let k = -20; k <= 20; k++) {
      const d = (k / 10) * s;
      el[5 + i] = dtNom + d;
      const r = evalOne(ctx, el, i);
      const visible = r.alt > -0.3;
      if (!visible || r.type === 0) continue;
      if (Math.abs(k) <= 10) { maxMag1 = Math.max(maxMag1, r.mag); if (r.type === 3) anyTotal1 = true; }
      maxMag2 = Math.max(maxMag2, r.mag);
      if (r.type === 3) anyTotal2 = true;
      if (r.type >= 2) anyCentral2 = true;
    }
    el[5 + i] = dtNom;
    const r0 = evalOne(ctx, el, i);
    console.log(JSON.stringify({
      file: f, idx: i / 28, jdTD: el[i], dT: el[4 + i], sigmaDT: Math.round(s),
      date: r0.date, type: r0.type, mag: +r0.mag.toFixed(4), alt: +r0.alt.toFixed(2), vis: r0.vis,
      utH: +r0.utH.toFixed(3), last: +r0.last.toFixed(3),
      maxMag1s: +maxMag1.toFixed(4), anyTotal1s: anyTotal1, maxMag2s: +maxMag2.toFixed(4), anyTotal2s: anyTotal2, anyCentral2s: anyCentral2,
      sigmaSrc: sg.src,
    }));
  }
}
