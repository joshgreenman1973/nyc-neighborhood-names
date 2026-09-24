"""Oldest matches for one name from a given start date, for names whose
earliest matches are other uses (London's Soho, the word "nomad", etc.).
Usage: python3 build/followup.py "SoHo" 19500101 [page]
Writes/merges data/followups.json. Uses the same cache and pacing as fetch.py."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch import call, ROOT
name, begin = sys.argv[1], sys.argv[2]
page = int(sys.argv[3]) if len(sys.argv) > 3 else 0
names = {n['name']: n for n in json.load(open(os.path.join(ROOT, 'build', 'names.json')))}
q = f'"{name}" {names[name]["borough"]}'
j = call({'q': q, 'sort': 'oldest', 'begin_date': begin, 'page': page})
docs = [{'date': d.get('pub_date', '')[:10], 'headline': (d.get('headline') or {}).get('main', ''), 'url': d.get('web_url', ''),
         'abstract': d.get('abstract', ''), 'snippet': d.get('snippet', ''), 'lead': (d.get('lead_paragraph') or '')[:400],
         'section': d.get('section_name', '')} for d in j['response'].get('docs') or []]
fp = os.path.join(ROOT, 'data', 'followups.json')
allf = json.load(open(fp)) if os.path.exists(fp) else {}
allf[f'{name}|{begin}|{page}'] = docs
json.dump(allf, open(fp, 'w'), indent=1)
for i, d in enumerate(docs):
    print(i, d['date'], '|', d['headline'][:70], '|', (d['abstract'] or d['snippet'] or d['lead'])[:170].replace('\n', ' '))
