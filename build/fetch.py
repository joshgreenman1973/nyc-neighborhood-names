"""Pull New York Times Article Search counts for each neighborhood name.

For each name: the oldest 20 matching articles (for first-appearance review)
and hit counts by decade. Query = the quoted name AND its borough name.
Cached per request in data/cache/ so reruns cost nothing. Fails loudly on
any non-200 or missing metadata. API limit: 5 requests/min, 500/day.
"""
import json, os, subprocess, sys, time, urllib.parse, urllib.request, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'data', 'cache'); os.makedirs(CACHE, exist_ok=True)
KEY = subprocess.check_output(['security', 'find-generic-password', '-s', 'NYT_API_KEY', '-w']).decode().strip()
BINS = [('pre-1950', '18510101', '19491231')] + [(f'{d}s', f'{d}0101', f'{d+9}1231') for d in range(1950, 2030, 10)]
BINS[-1] = ('2020s', '20200101', '20260922')
last = [0.0]

def call(params):
    h = hashlib.sha1(json.dumps(params, sort_keys=True).encode()).hexdigest()[:16]
    fp = os.path.join(CACHE, h + '.json')
    if os.path.exists(fp):
        return json.load(open(fp))
    for attempt in range(6):
        wait = 13 - (time.time() - last[0])
        if wait > 0: time.sleep(wait)
        last[0] = time.time()
        url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?' + urllib.parse.urlencode({**params, 'api-key': KEY})
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                j = json.load(r)
            if not j.get('response') or 'metadata' not in j['response']:
                raise RuntimeError('no metadata: ' + str(j)[:200])
            json.dump(j, open(fp, 'w'))
            return j
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print('  429, backing off', flush=True); time.sleep(60 * (attempt + 1)); continue
            raise
    raise RuntimeError('gave up after retries: ' + str(params))

def main():
    names = json.load(open(os.path.join(ROOT, 'build', 'names.json')))
    out = []
    for n in names:
        q = f'"{n["name"]}" {n["borough"]}'
        rec = {**n, 'query': q, 'decades': {}, 'oldest': []}
        for page in (0, 1):
            j = call({'q': q, 'sort': 'oldest', 'page': page})
            for d in j['response'].get('docs') or []:
                rec['oldest'].append({'date': d.get('pub_date', '')[:10], 'headline': (d.get('headline') or {}).get('main', ''),
                    'url': d.get('web_url', ''), 'abstract': d.get('abstract', ''), 'snippet': d.get('snippet', ''),
                    'lead': (d.get('lead_paragraph') or '')[:400], 'section': d.get('section_name', '')})
            if j['response']['metadata']['hits'] <= 10: break
        for label, b, e in BINS:
            j = call({'q': q, 'begin_date': b, 'end_date': e})
            rec['decades'][label] = j['response']['metadata']['hits']
        total = sum(rec['decades'].values())
        print(f'{n["name"]:38s} total {total:6d}  ' + ' '.join(f'{k}:{v}' for k, v in rec['decades'].items()), flush=True)
        if total == 0:
            print('  WARNING: zero hits', flush=True)
        out.append(rec)
        json.dump(out, open(os.path.join(ROOT, 'data', 'raw.json'), 'w'), indent=1)
    print('DONE', len(out), flush=True)

if __name__ == '__main__':
    main()
