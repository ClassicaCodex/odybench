// Runs NASA's original JavaScript Solar Eclipse Explorer (program.js) headless
// with a stub DOM, for one site and one century file, and prints its table.
// Used only to check the Python port in eclipse_local.py against the original.
// usage: node jsex_harness.js <lat N> <lon E> <century-file.js>
const fs = require('fs');
const path = require('path');
const NASA = path.join(__dirname, '..', '..', 'data', 'refs', 'nasa');
const [lat, lonE, cent] = process.argv.slice(2);

function el(tag) {
  return { tag, children: [], attrs: {}, setAttribute(k, v) { this.attrs[k] = v; },
           appendChild(c) { this.children.push(c); return c; }, removeChild() {} };
}
function nodeText(n) {
  if (n.text !== undefined) return n.text;
  return n.children.map(nodeText).join("");
}
function sel(v) { return { selectedIndex: 0, options: [{ value: String(v), text: String(v) }] }; }
const aLat = Math.abs(+lat), aLon = Math.abs(+lonE);
const form = {
  latd: { value: String(aLat) }, latm: { value: '0' }, lats: { value: '0' },
  lond: { value: String(aLon) }, lonm: { value: '0' }, lons: { value: '0' },
  alt: { value: '0' },
  latx: sel(+lat >= 0 ? 1 : -1),
  lonx: sel(+lonE >= 0 ? -1 : 1),          // program uses WEST longitude positive
  tzh: sel(0), tzm: sel(0), tzx: sel(1),
  loc_name: { value: 'test' },
};
const RESULTS = el("div");
global.document = {
  eclipseform: form,
  getElementById(id) { return id === "el_results" ? RESULTS : null; },
  createElement: el,
  createTextNode(t) { return { text: String(t) }; },
};
eval(fs.readFileSync(path.join(NASA, 'JSEX-program.js'), 'utf8'));
const fn = path.basename(cent).replace(/^JSEX-/, '').replace(/\.js$/, '');
currenttimeperiod = fn;   // the century file ends by calling recalculate()
eval(fs.readFileSync(path.join(NASA, cent), 'utf8'));
const table = RESULTS.children[RESULTS.children.length - 1];
for (const row of table.children[0].children.slice(1)) {
  console.log(row.children.map(nodeText).join(' | '));
}
