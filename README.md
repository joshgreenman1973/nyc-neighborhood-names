# When a neighborhood got its name

Seventy-nine New York City neighborhood names and when each one showed up in The New York Times: a decade-by-decade map, an articles-per-decade chart and the first headline or summary to use each name.

- `index.html`: the page (d3 from jsDelivr, house.css from the experiments site)
- `methodology.html`: sources, rules and every search
- `data/names.json`: the published data (counts, first use, group)
- `data/*.geojson`: base map layers (NYC Open Data boroughs, 2020 NTAs and parks, clipped to shore; Census New Jersey land minus water)
- `build/`: `fetch.py` (Times API pull, cached and rate-limited), `followup.py` (date-bounded searches), `review.py` (every hand decision and the group rules), `assemble.py` (writes `data/names.json`), `names.json` (the search list), `coords.json` (hand-placed label anchors)

Rebuild: `python3 build/review.py && python3 build/assemble.py`. A fresh pull needs a Times API key in the macOS Keychain under `NYT_API_KEY` and runs about 400 requests at 5 per minute (the daily limit is 500). Raw API responses (`data/cache`, `data/raw.json`, `data/followups.json`) are gitignored.

Data provided by The New York Times.
