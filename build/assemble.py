"""Merge raw Times counts, label coordinates and the hand review into data/names.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = json.load(open(os.path.join(ROOT, 'data', 'raw.json')))
coords = json.load(open(os.path.join(ROOT, 'build', 'coords.json')))
rv_path = os.path.join(ROOT, 'build', 'review.json')
review = json.load(open(rv_path)) if os.path.exists(rv_path) else {'names': {}, 'findings': []}
DECS = ['pre-1950','1950s','1960s','1970s','1980s','1990s','2000s','2010s','2020s']
out = []
for r in raw:
    if r['name'] in review.get('drop', {}):
        continue
    rv = review['names'].get(r['name'], {})
    lat, lon = coords[r['name']]
    first = rv.get('first')
    out.append({'name': r['name'], 'borough': r['borough'], 'lat': lat, 'lon': lon,
        'query': r['query'], 'decades': {d: r['decades'][d] for d in DECS},
        'total': sum(r['decades'].values()), 'first': first,
        'category': rv['category'], 'note': rv.get('note', ''),
        'capped': [d for d in DECS if r['decades'][d] >= 10000]})
json.dump({'asof': '2026-09-22', 'names': out, 'findings': review['findings'], 'dropped': review['drop']},
          open(os.path.join(ROOT, 'data', 'names.json'), 'w'), indent=1, ensure_ascii=False)
print('wrote', len(out), 'names')
