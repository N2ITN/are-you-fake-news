from mongo_query_results import db, del_TLD

tld = x.find()
sorted(d.items(),key=lambda kv: kv[1])
d={}
for t in tld:
   if 'articles' in t:
    d.update({t['TLD']: len(t['articles'])})



for domain, count in d.items():
    if count > 1000:
        del_TLD(domain)

        