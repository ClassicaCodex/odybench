"""
Tests of odybench/model.py against the contract of DESIGN 10.2 (A0).

    cd C:\\Projects\\odybench && py tests/test_model.py

(no pytest on this machine; also collectable by pytest).  The contract's
constants, dtypes and the field names, order and defaults of every dataclass
are compared with 10.2 as transcribed here, and with the DESIGN.md text itself
(the code block under "odybench/model.py (the contract)").
"""
import dataclasses
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from odybench import model as M  # noqa: E402

CONTRACT_FIELDS = {
    "Site": ["key", "lat", "lon", "elev_m", "source", "span", "columns"],
    "Predicate": ["type", "params", "day", "quant", "site", "dt_rule"],
    "Option": ["name", "primary", "predicate", "grid"],
    "ClueRow": ["clue_id", "event_id", "day_offset", "options"],
    "ClueSet": ["set_id", "role", "anchor_kind", "events", "links", "rows", "site_rule",
                "window_widths", "counted"],
    "Reading": ["choice"],
    "SearchResult": ["pool", "fails", "strict", "best", "n_cand", "clusters"],
    "GStat": ["value", "lo", "hi", "n", "k", "garden", "pool", "slot", "widths", "lo_gamma",
              "hi_gamma", "lo_boot", "hi_boot", "masked"],
}


def _contract_block():
    text = (ROOT / "DESIGN.md").read_text(encoding="utf-8")
    i = text.index("**`odybench/model.py`** (the contract)")
    j = text.index("```", i)
    k = text.index("```", j + 3)
    return text[j + 3:k]


def test_constants():
    assert M.BODIES == ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn")
    assert M.GRAMMAR_STARS == ("alcyone", "arcturus", "sirius", "aldebaran", "betelgeuse", "rigel", "dubhe")
    assert M.DT_MODELS == ("smh2020", "smh2020_parabola", "smh2016_parabola", "em_canon")
    assert M.POOL_DTYPE == [("jd_ut", "f8"), ("jd_tt", "f8"), ("day0_jdn_ut2", "i8"),
                            ("day0_jdn_lmt", "i8"), ("kind", "U12"), ("cat_idx", "i8"), ("daylight", "?")]


def test_constants_match_design_text():
    blk = _contract_block()
    for name in ("BODIES", "GRAMMAR_STARS", "DT_MODELS"):
        mt = re.search(rf"{name} = \((.*?)\)", blk, re.S)
        assert mt, name
        want = tuple(re.findall(r'"([^"]+)"', mt.group(1)))
        assert getattr(M, name) == want, (name, want)
    mt = re.search(r"POOL_DTYPE = \[(.*?)\]\n", blk, re.S)
    pairs = re.findall(r'\("(\w+)","([^"]+)"\)', mt.group(1).replace(" ", ""))
    assert [tuple(p) for p in pairs] == M.POOL_DTYPE


def test_dataclass_fields_match_contract():
    blk = _contract_block()
    for cls, want in CONTRACT_FIELDS.items():
        got = [f.name for f in dataclasses.fields(getattr(M, cls))]
        assert got == want, (cls, got)
        mt = re.search(rf"@dataclass {cls}\((.*?)\)\s*(?:#.*)?\n(?!\s)", blk, re.S)
        assert mt, cls
        names = [re.split(r"[:=]", a.strip())[0].strip() for a in
                 re.split(r",(?![^\[]*\])", mt.group(1).replace("\n", " ")) if a.strip()]
        names = [n for n in names if re.fullmatch(r"\w+", n)]
        assert names == want, (cls, names)


def test_defaults():
    p = M.Predicate("anchor", {"rule": "conj_ut2"}, 0)
    assert (p.quant, p.site, p.dt_rule) == ("any", None, "mixture_p50")
    for cls in ("Site", "Option", "ClueRow", "ClueSet", "Reading", "SearchResult", "GStat"):
        for f in dataclasses.fields(getattr(M, cls)):
            assert f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING, (cls, f.name)


def test_pool_dtype_builds_and_round_trips():
    dt = np.dtype(M.POOL_DTYPE)
    a = np.zeros(3, dtype=dt)
    a["jd_ut"] = [1.5, 2.5, 3.5]
    a["day0_jdn_ut2"] = [10, 11, 12]
    a["kind"] = ["conj", "full_moon", "crescent"]
    a["daylight"] = [True, False, True]
    assert a.dtype.names == tuple(n for n, _ in M.POOL_DTYPE)
    assert a["kind"][2] == "crescent" and a["daylight"].dtype == np.bool_
    assert dt["day0_jdn_lmt"] == np.dtype("i8") and dt["kind"].itemsize == 12 * 4
    # "kind" holds at most 12 characters: numpy truncates longer names silently,
    # so pools must store short kind codes (first_crescent has 14)
    a["kind"][0] = "first_crescent"
    assert a["kind"][0] == "first_cresce"


def test_normalisations():
    s = M.Site("ithaki", 38.37, 20.72, 0.0, "acq 2.2", [-1999, 200], ["rise_ut", "set_ut"])
    assert s.span == (-1999, 200) and s.columns == ("rise_ut", "set_ut")
    p = M.Predicate("star_covis", {}, [-29, -12], quant="all")
    assert p.day == (-29, -12) and p.quant == "all"
    g = M.GStat(0.1, 0.05, 0.2, 100, 3, "BM", "T_A", "v0", [136], 0.05, 0.2, 0.06, 0.19, True)
    assert g.widths == (136,)
    o = M.Option("none", False, None, {})
    r = M.ClueRow("X.1", "E1", 0, [o])
    cs = M.ClueSet("X", "counted", "lunar_eclipse", ["E1"], [], [r], {"rule": "none"}, (136,), True)
    assert cs.rows[0].options[0].predicate is None
    rd = M.Reading({"X.1": ("none", {})})
    assert rd.choice["X.1"][0] == "none"
    sr = M.SearchResult(np.arange(3), np.array([0, 1, 0], dtype=np.int16), np.array([0, 2]),
                        np.array([0, 2]), 3, 2)
    assert sr.fails.dtype == np.int16 and sr.n_cand == 3


def test_grammar_stars_exist_in_star_file():
    stars = json.loads((ROOT / "data" / "stars.json").read_text(encoding="utf-8"))["stars"]
    for s in M.GRAMMAR_STARS:
        assert s in stars, s


def test_dt_models_named_in_deltat_models_json():
    p = ROOT / "data" / "prereg" / "deltat_models.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    assert tuple(m["key"] for m in d["models"]) == M.DT_MODELS


def test_sites_json_rows_build_sites():
    d = json.loads((ROOT / "data" / "prereg" / "sites.json").read_text(encoding="utf-8"))
    names = [f.name for f in dataclasses.fields(M.Site)]
    for key, row in d["sites"].items():
        s = M.Site(**{n: (key if n == "key" else row[n]) for n in names})
        assert s.key == key and len(s.span) == 2 and s.span[0] <= s.span[1]


if __name__ == "__main__":
    import time
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            t0 = time.time()
            try:
                fn()
                print(f"PASS {name} ({time.time() - t0:.2f} s)")
            except Exception as exc:          # noqa: BLE001
                fails += 1
                print(f"FAIL {name}: {exc!r}")
    print("all passed" if not fails else f"{fails} failed")
    sys.exit(1 if fails else 0)
