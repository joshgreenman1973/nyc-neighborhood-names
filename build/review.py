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
 'Upper West Side': ('1900-01-21', 'IN THE REAL ESTATE FIELD', None, False),
 'Upper East Side': ('1902-10-20', 'POLICE KNEW NOTHING', None, True),
 'Greenwich Village': ('1900-01-02', "CITY'S GREETING TO 1900", None, False),
 'Lower East Side': ('1898-11-05', 'ROOSEVELT TOURS THE CITY', None, True),
 'Brooklyn Heights': ('1854-05-01', 'THE ACCIDENT ON BROOKLYN HEIGHTS', None, True),
 'Bedford-Stuyvesant': ('1927-06-05', 'CROSSTOWN SUBWAY URGED', None, True),
 'Red Hook': ('1851-11-28', 'BROOKLYN CITY', None, True),
 'Gowanus': ('1851-10-18', 'TEMPERANCE MASS MEETING', None, True),
 'Astoria': ('1865-04-04', 'THE VOICE OF THE PEOPLE', None, True),
 'Long Island City': ('1870-02-20', 'The New Long Island City', None, True),
 'Greenpoint': ('1860-01-02', 'DIED', None, False),
 'Crown Heights': ('1912-05-04', "JESUITS' BROOKLYN COLLEGE", None, True),
 'Flatbush': ('1851-09-20', 'BROOKLYN', None, True),
 'Kensington': ('1860-01-23', 'MARINE INTELLIGENCE', None, False),
 'Bay Ridge': ('1859-08-26', 'BROOKLYN INTELLIGENCE', None, True),
 'Dyker Heights': ('1900-03-17', 'EXCITING UP-TOWN FIRE', None, False),
 'Bensonhurst': ('1897-08-13', 'TROLLEY CAR COLLISION', None, True),
 'Brownsville': ('1860-03-28', 'NEWS OF THE DAY', None, False),
 'East New York': ('1852-09-07', 'BROOKLYN CITY', None, False),
 'Canarsie': ('1852-07-23', 'BROOKLYN CITY', None, True),
 'Sheepshead Bay': ('1885-07-02', 'MISS WOODFORD BEATEN', None, True),
 'Brighton Beach': ('1878-07-02', 'ANOTHER CONEY ISLAND RAILROAD', None, True),
 'Coney Island': ('1860-03-29', 'THE MURDERS AT SEA', None, False),
 'Starrett City': ('1972-07-16', 'Housing for 24,000', None, True),
 'Jackson Heights': ('1917-04-04', 'Rifle Club at Jackson Heights', None, True),
 'Sunset Park': ('1957-03-11', 'CHURCH REDEDICATED', 'Sunset Park|19550101|0', True),
 'Forest Hills': ('1910-08-14', 'MORE SAGE HOTELS', None, True),
 'Sunnyside': ('1864-01-26', 'The Prize Ring', None, False),
 'Ridgewood': ('1860-09-26', 'BROOKLYN NEWS', None, False),
 'Flushing': ('1860-10-26', 'Extension of the New-York and Flushing', None, True),
 'Jamaica': ('1860-01-25', 'BROOKLYN INTELLIGENCE', None, False),
 'Rego Park': ('1926-08-08', 'QUEENS TROLLEYS TIED UP', None, True),
 'Far Rockaway': ('1899-08-15', 'APPEAL TO THE GOVERNOR', None, True),
 'Riverdale': ('1901-12-07', 'MARK TWAIN', None, True),
 'Mott Haven': ('1900-05-16', 'MOTT HAVEN CANAL CASE', None, True),
 'Hunts Point': ('1910-09-11', 'HUNTS POINT AUCTION', None, True),
 'Co-op City': ('1965-02-20', 'ARCHITECTS SCORE CO-OP CITY', None, True),
 'City Island': ('1901-04-06', 'City Island Yacht News', None, True),
 'St. George': ('1860-02-13', 'MARINE INTELLIGENCE', None, False),
 'Tottenville': ('1878-03-24', 'FURTHER VIEWS AFOOT', None, True),
 'Great Kills': ('1865-05-12', 'Obituary 1', None, False),
}
PRE1950_ACCEPTED = {"Hell's Kitchen", 'Prospect Heights', 'Park Slope', 'Williamsburg', 'Harlem', 'Bushwick', 'Upper West Side', 'Upper East Side', 'Greenwich Village', 'Lower East Side', 'Brooklyn Heights', 'Bedford-Stuyvesant', 'Red Hook', 'Gowanus', 'Astoria', 'Long Island City', 'Greenpoint', 'Crown Heights', 'Flatbush', 'Kensington', 'Bay Ridge', 'Dyker Heights', 'Bensonhurst', 'Brownsville', 'East New York', 'Canarsie', 'Sheepshead Bay', 'Brighton Beach', 'Coney Island', 'Jackson Heights', 'Forest Hills', 'Sunnyside', 'Ridgewood', 'Flushing', 'Jamaica', 'Rego Park', 'Far Rockaway', 'Riverdale', 'Mott Haven', 'Hunts Point', 'City Island', 'St. George', 'Tottenville', 'Great Kills', 'Manhattan Valley', 'Stuyvesant Heights',
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
 'Upper West Side': 'No early headline or summary shows the name. The date is the earliest search match.',
 'Greenwich Village': 'No early headline or summary shows the name. The date is the earliest search match.',
 'Bedford-Stuyvesant': 'Earlier matches from 1901 on could not be checked. The 1927 summary describes a meeting of a Bedford-Stuyvesant group.',
 'Red Hook': 'Some matches may be Red Hook in Dutchess County; the Brooklyn filter cuts most of them.',
 'Astoria': 'Some matches are likely the Waldorf-Astoria hotel rather than the Queens neighborhood.',
 'Long Island City': 'Long Island City was chartered as its own city in 1870, the year of the first headline. The pre-1950 count hit the API ceiling of 10,000, so the true figure is higher.',
 'Greenpoint': 'No early headline or summary shows the name. The date is the earliest search match.',
 'Kensington': "No early headline or summary shows the name, and many early matches are likely London's Kensington. The date is the earliest search match.",
 'Dyker Heights': 'No early headline or summary shows the name. The date is the earliest search match.',
 'Brownsville': 'No early headline or summary shows the name, and some early matches may be Brownsville, Texas. The date is the earliest search match.',
 'East New York': 'No early headline or summary shows the name. The date is the earliest search match.',
 'Coney Island': 'No early headline or summary among the oldest matches shows the name. The date is the earliest search match. The pre-1950 count hit the API ceiling of 10,000.',
 'Flatbush': 'In 1851 Flatbush was its own town, outside the City of Brooklyn. The pre-1950 count hit the API ceiling of 10,000.',
 'Crown Heights': 'The 1912 headline puts a Jesuit college "on Crown Heights."',
 'Starrett City': 'The 1972 summary describes the start of construction on the housing development that gave the area its name.',
 'Sheepshead Bay': 'The earliest confirmed headlines are about the racetrack at Sheepshead Bay.',
 'Sunset Park': 'Earlier matches include the park itself and other Sunset Parks, such as a Catskills inn. They are not counted. The 1957 headline describes a renovated Sunset Park church in Brooklyn.',
 'Forest Hills': 'Counts from the 1910s to the 1970s likely include many tennis stories; the national championships were played at Forest Hills for decades.',
 'Sunnyside': 'No early headline or summary shows the name, and other Sunnysides (the Irving estate on the Hudson, for one) may match. The date is the earliest search match.',
 'Ridgewood': 'No early headline or summary shows the name, and some matches may be Ridgewood, New Jersey. The date is the earliest search match.',
 'Jamaica': 'No early headline or summary shows the name. Counts include Jamaica Bay and Jamaica Avenue stories, and some about the country. The pre-1950 count hit the API ceiling of 10,000. The date is the earliest search match.',
 'Flushing': 'The pre-1950 count hit the API ceiling of 10,000. Counts likely include Flushing Meadows stories, among them coverage of the 1939 and 1964 World\'s Fairs.',
 'Co-op City': 'The name first appears in 1965 coverage of the plan to build the development on the Freedomland site.',
 'St. George': 'An 1872 headline about a St. George cricket club is excluded. No early headline or summary shows the neighborhood name, so the date is the earliest search match.',
 'Great Kills': 'No early headline or summary shows the name. The date is the earliest search match.',
 'Rego Park': 'The name first appears in 1926, in a story about a trolley jumping its track.',
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
PENDING = set()  # needs a date-bounded search; pre-1950 matches are other Sunset Parks
missing = set(raw) - set(FIRST) - set(DROP) - PENDING
assert not missing, missing
json.dump(out, open(os.path.join(ROOT, 'build', 'review.json'), 'w'), indent=1, ensure_ascii=False)
for n, v in out['names'].items(): print(f"{v['category']:8s} {n:36s} {v['first']['date']} {'' if v['first']['confirmed'] else '(earliest match)'}")
