import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'results/controls-almagest')
import records as RC, greek
T = RC.rows()
for r in RC.R:
    pairs = [(k, r.get(k), r['ref']) for k in ("date_words", "date_words_nab", "phen_words", "side_words", "extra_words", "observer_words",
              "ref_star_words", "time_words", "before_words", "after_words", "mean_sun_words")]
    pairs += [("star", s['words'], r['ref']) for s in r.get('stars', [])]
    if r.get('moon'): pairs.append(("moon", r['moon']['words'], r['ref']))
    if r.get('moonsun'): pairs.append(("moonsun", r['moonsun']['words'], r['ref']))
    if r.get('ge_claim_words'): pairs.append(("ge_claim", r['ge_claim_words'], r['ge_claim_ref']))
    if r.get('phen_ref'): pairs.append(("phen_ref", r['phen_words'], r['phen_ref']))
    for k, w, ref in pairs:
        if not w or w in T[ref]:
            continue
        e = greek.exact(T[ref], w)
        print(r['id'], k, 'FOUND' if e else 'NOTFOUND', '|', w, '|', e)
