import json
from pprint import pprint
from proto import NewsSource
from helpers import j_writer
import requests
from multiprocessing.dummy import Pool

import os


@j_writer
def collect_sources_articles(kv):
    k, v = kv
    out_name = 'scraped/' + k.replace('.', '-').replace('/', '_')
    # if os.path.exists(out_name):
    #     return
    try:
        if not requests.get('http://' + k).ok:
            return
    except Exception as e:
        if requests.exceptions.ConnectionError == e:
            return
        else:
            print(e)
    src = NewsSource(k, v, n_articles=50)
    if not src.meta['Articles']:
        return
    else:
        print(src.meta['Meta'])
        return (src.meta, out_name)


bad_sources = json.load(open('./opensources/sources/sources.json'))
good_soures = json.load(open('./opensources/sources/not_fake.json'))

sources = list(good_soures.items())
pool = Pool(5)
list(pool.map(collect_sources_articles, sources))
