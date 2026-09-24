import json,re,sys
names=sys.argv[1:]
for r in json.load(open('data/raw.json')):
  if r['name'] in names:
    pat=re.compile(re.escape(r['name']).replace('\\-','[ -]').replace('\\.','\\.?'),re.I)
    print('=====',r['name'],r['decades'])
    shown=0
    for i,d in enumerate(r['oldest'][:20]):
      t=d['headline']+' '+d['abstract']
      if pat.search(t) or i<2:
        print(' ',i,d['date'],'*' if pat.search(t) else ' ','|',d['headline'][:88],'|',d['abstract'][:60]); shown+=1
      if shown>=5: break
