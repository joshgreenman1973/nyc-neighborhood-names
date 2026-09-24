"""Hand review -> build/review.json.

FIRST: the first article whose headline or summary shows the name used for
the neighborhood (confirmed=True). Where no such article turned up, the
earliest search match is used and marked confirmed=False.
PRE1950_ACCEPTED: names whose pre-1950 matches are taken as this place.
Category rule (applied in code below, stated on the methodology page):
  - pre-1950 use accepted: 'revived' if the quietest decade of the 1950s-70s
    had no more than 20 articles and no more than 5% of the name's busiest
    decade since 1950, else 'old'.
  - otherwise: 'flop' if no decade since 1950 reached 50 articles, else 'coined'.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = {r['name']: r for r in json.load(open(os.path.join(ROOT, 'data', 'raw.json')))}
fu = json.load(open(os.path.join(ROOT, 'data', 'followups.json')))
DROP = {'NoMad': 'the ordinary word "nomad" swamps the search in every decade',
        'Two Bridges': 'the phrase "two bridges" turns up in bridge and transit stories in every decade'}
FIRST = {  # name: (date, headline fragment, source list or None for raw oldest, confirmed)
 'SoHo': ('1970-05-11', 'SoHo Is Artists', 'SoHo|19690101|0', True),
 'Tribeca': ('1976-06-12', 'LOFTS IN TRIBECA', None, True),
 'NoHo': ('1975-10-29', 'About Real Estate', None, True),
 'Nolita': ('1996-11-14', 'Jewel Boxes', None, True),
 'Alphabet City': ('1987-05-17', 'LOISAIDA OR ALPHABET', None, True),
 'Loisaida': ('1981-05-27', 'The Real Loisaida', None, True),
 'East Village': ('1963-07-28', 'CITY TOWN HOUSES', None, True),
 'Hudson Square': ('1989-09-17', 'Hudson Square', None, True),
 'Meatpacking District': ('1981-05-01', 'FLOURISHING AERIE', None, False),
 'Flatiron District': ('1985-07-25', 'EMERGING FLATIRON', None, True),
 'Hudson Yards': ('2003-03-11', "Midtown's Final Frontier", None, True),
 'SoHa': ('1996-11-03', 'SoHa Loses Blight', None, True),
 'Manhattan Valley': ('1895-03-20', 'GREAT WEST SIDE WINS', None, True),
 "Hell's Kitchen": ('1905-07-16', 'Seeing Manhattan', None, True),
 'Dumbo': ('1997-10-27', 'A Private Eye', 'Meatpacking District', True),
 'Boerum Hill': ('1966-03-20', 'Brooklyn Renewal', None, True),
 'Cobble Hill': ('1960-02-28', 'Restoration of Cobble Hill', None, True),
 'Carroll Gardens': ('1966-12-12', 'Bedford-Stuyvesant Blocks', None, True),
 'BoCoCa': ('2004-03-14', 'BROWNSTONE BROOKLYN', None, True),
 'Vinegar Hill': ('1998-02-01', '2d Battle of Vinegar Hill', None, True),
 'Prospect Heights': ('1890-06-01', 'PROSPECT HEIGHTS POPULAR', None, True),
 'Prospect Lefferts Gardens': ('1973-04-29', 'Other Byways', None, True),
 'ProCro': ('2011-04-19', 'NoJoke', None, True),
 'East Williamsburg': ('1984-03-25', 'LURE INDUSTRIES', 'East Williamsburg|19600101|0', True),
 'Columbia Street Waterfront District': ('2010-10-22', 'Growing in a Family Way', None, True),
 'Ditmas Park': ('1903-05-03', 'ATTRACTIONS FOR THE HOMESEEKER', None, False),
 'South Slope': ('1988-05-08', 'South Slope Pioneering', None, True),
 'Greenwood Heights': ('1999-06-13', 'GREENWOOD HEIGHTS', None, True),
 'Stuyvesant Heights': ('1911-04-16', 'REALTY CONDITIONS IN BROOKLYN', None, True),
 'Hunters Point': ('1863-09-03', 'Conclusion of the Draft', None, False),
 'Dutch Kills': ('1901-02-11', 'NEWS OF THE RAILROADS', None, False),
 'SoBro': ('1994-04-10', 'Antiquing of the South Bronx', None, True),
 'Piano District': ('2015-03-25', 'Mott Haven, the Bronx', None, False),
 'Port Morris': ('1900-03-30', 'MANY BILLS PASSED', None, False),
 'Park Slope': ('1897-11-26', 'BIG BILL FOR BROOKLYN', None, True),
 'Williamsburg': ('1851-12-03', 'WILLIAMSBURG JUBILEE', None, True),
 'Harlem': ('1860-08-23', 'HARLEM OF HARLEM', None, True),
 'Bushwick': ('1853-10-06', 'CONSOLIDATION', None, True),
}
PRE1950_ACCEPTED = {"Hell's Kitchen", 'Prospect Heights', 'Park Slope', 'Williamsburg', 'Harlem', 'Bushwick', 'Manhattan Valley', 'Stuyvesant Heights',
                    'Hunters Point', 'Port Morris', 'Dutch Kills', 'Ditmas Park'}
NOTES = {
 'SoHo': "All 36 matches before 1970 are London's Soho or other uses, judging by their headlines and summaries.",
 'Tribeca': "An October 1975 article on SoHo already matches the search, but its summary doesn't show the name.",
 'NoHo': 'Arts listings from May 1975 match the search, but their summaries do not show the name.',
 'Nolita': 'The 1996 summary spells it NoLiTa, for North of Little Italy. A 1977 match is a death notice, not the place.',
 'Alphabet City': "A 1984 review of the film \"Alphabet City\" comes first. A 1941 match is about something else.",
 'East Village': 'The 1963 headline lists "the East Village" among six affordable Manhattan sections. A few earlier matches could not be checked.',
 'Hudson Square': 'Twelve matches before 1950 could not be checked, so they are not counted as this neighborhood.',
 'Meatpacking District': 'No early headline or summary shows the name. The date is the earliest search match.',
 'Hudson Yards': 'The first matches, from 2001 and 2002, concern the Olympic bid for the same West Side rail yards.',
 'SoHa': 'The Times placed SoHa in three different stretches: 104th to 107th Streets (1996), south of Columbia (1999) and 96th to 113th Streets (2002).',
 'Manhattan Valley': 'The 1890s headlines concern a Riverside Drive viaduct over a valley near 125th Street, not the blocks that carry the name today.',
 'Dumbo': 'Earlier matches are mostly the Disney elephant. The 1997 summary calls the waterfront between the bridges "dubbed Dumbo."',
 'Cobble Hill': 'Matches before 1950 are mostly a Cobble Hill in the Adirondacks, so they are not counted.',
 'Vinegar Hill': 'Earlier matches from 1970 on exist, but their summaries do not show the name.',
 'ProCro': 'The first article covers an assemblyman\'s bill to penalize brokers who invent neighborhood names.',
 'East Williamsburg': 'Sixty-two matches before 1950, mostly obituaries, could not be checked, so they are not counted as this neighborhood.',
 'Columbia Street Waterfront District': 'A 2005 profile describes the Columbia Street neighborhood without the full name in its summary.',
 'Ditmas Park': 'No early headline or summary shows the full name. The date is the earliest search match.',
 'Greenwood Heights': 'A 1920 headline mentions a Greenwood Heights church, and a 1987 real estate column is titled "Capitalizing On a Name." Neither summary places them.',
 'Park Slope': 'The 1897 headline calls it "the Park Slope," with the article.',
 'Williamsburg': 'In 1851 Williamsburg was its own city. An 1853 headline covers plans to consolidate Brooklyn, Williamsburg and Bushwick. Counts also pick up articles about East Williamsburg and the Williamsburg Bridge.',
 'Harlem': 'The 1860 headline is a baseball game against the Harlem club "of Harlem." The Times archive starts in 1851, and the pre-1950 count hit the API ceiling of 10,000, so the true figure is higher.',
 'Bushwick': 'In 1853 Bushwick was a separate town; the headline covers plans to consolidate it with Brooklyn and Williamsburg.',
 'Hunters Point': 'No early headline or summary shows the name. The date is the earliest search match.',
 'Dutch Kills': 'No early headline or summary shows the name. The date is the earliest search match.',
 'Port Morris': 'No early headline or summary shows the name. The date is the earliest search match.',
 'Piano District': 'A 1990 match about a school piano is excluded. No 2015 summary shows the name, so the date is the earliest match after that.',
}
DECS = ['pre-1950','1950s','1960s','1970s','1980s','1990s','2000s','2010s','2020s']
def find(name, date, frag, src):
    pool = fu[src] if src and '|' in src else raw[src or name]['oldest']
    for d in pool:
        if d['date'] == date and frag.lower() in d['headline'].lower():
            return d
    raise SystemExit(f'NOT FOUND: {name} {date} {frag}')
FINDINGS = [
 "<b>Brooklyn's brownstone names came first.</b> Cobble Hill (1960), Boerum Hill (1966) and Carroll Gardens (1966) show up in Times headlines and summaries in the 1960s. Manhattan's loft-district names followed in the 1970s: SoHo in 1970, NoHo in 1975 and Tribeca in 1976.",
 "<b>SoHo went from nothing to everywhere.</b> All 10 matching articles from the 1960s are about London. The count rose to 649 in the 1970s and 4,921 in the 2000s.",
 "<b>Most portmanteau names flopped.</b> BoCoCa, ProCro, SoBro, SoHa and the Piano District never reached 50 articles in any decade. ProCro first appeared in April 2011, in a story about an assemblyman's bill to penalize brokers who invent neighborhood names.",
 "<b>SoHa kept moving.</b> The Times put it at 104th to 107th Streets in 1996, south of Columbia in 1999 and 96th to 113th Streets in 2002.",
 "<b>Some old names faded, then came back.</b> Hell's Kitchen matched 113 articles before 1950 and nine in the 1950s, then 562 in the 2000s. Ditmas Park drew one article in each of the 1950s and 1960s, then 159 in the 1990s.",
 "<b>Hudson Yards started from zero.</b> No article matches before 2001. With more than three years still to go, the 2020s already equal the 2010s, at 410 articles each.",
]
out = {'drop': DROP, 'findings': FINDINGS, 'names': {}}
for name, (date, frag, src, conf) in FIRST.items():
    d = find(name, date, frag, src)
    dec = raw[name]['decades']; post = [dec[k] for k in DECS[1:]]; peak = max(post)
    if name in PRE1950_ACCEPTED:
        quiet = min(dec['1950s'], dec['1960s'], dec['1970s'])
        cat = 'revived' if quiet <= 20 and quiet <= 0.05 * peak else 'old'
    else:
        cat = 'flop' if peak < 50 else 'coined'
    out['names'][name] = {'category': cat, 'note': NOTES.get(name, ''),
        'first': {'date': d['date'], 'headline': d['headline'].split(';')[0].strip(), 'url': d['url'],
                  'section': d.get('section', ''), 'confirmed': conf}}
missing = set(raw) - set(FIRST) - set(DROP)
assert not missing, missing
json.dump(out, open(os.path.join(ROOT, 'build', 'review.json'), 'w'), indent=1, ensure_ascii=False)
for n, v in out['names'].items(): print(f"{v['category']:8s} {n:36s} {v['first']['date']} {'' if v['first']['confirmed'] else '(earliest match)'}")
