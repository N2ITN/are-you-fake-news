import json
import sys
from multiprocessing import dummy
from time import sleep

import pandas as pd
import requests
from pymongo import MongoClient
from unidecode import unidecode

client = MongoClient(connect=False)
db = client['facescraper']


def get_links(page):
    for entry in db['facescraper'].find({'status_type': 'link', 'page': page}):
        yield entry['status_link']


def get_article_text(api, links):
    res = {}
    pool = dummy.Pool(30)

    def request(url):
        try:
            data = requests.put(api, data=url, timeout=2).json()
            # print(True,)
            res.update({url: data})
        except Exception as e:
            ...
            # print(False,)
        sleep(.5)

    list(pool.imap(request, links))
    return res


# def get_article_text(api: str, links: list):

#     res = {}

#     async def get_article(url: str):
#         async with aiohttp.ClientSession() as session:
#             try:
#                 async with session.put(api, data=url, timeout=15) as resp:
#                     data = await resp.json()
#                     res.update({url: data})
#             except concurrent.futures._base.TimeoutError:
#                 ...

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.gather(*(get_article(url) for url in links)))
#     return res


def insert(payload, table_name='nlp'):
    db[table_name].update_one(payload, {'$set': payload}, upsert=True)


def get_results(page):
    scrape_api = 'https://x9wg9drtci.execute-api.us-west-2.amazonaws.com/prod/article_get'
    nlp_api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/dev_dnn_nlp'

    links = list(get_links(page))
    print(len(links))
    text_dict = (get_article_text(scrape_api, links[:180]))
    print(len(text_dict))

    text_dict = {k: unidecode(v) for k, v in text_dict.items() if len(v) > 1}
    print(len(text_dict))
    nlp = json.loads(requests.put(nlp_api, json=text_dict).text)
    scores = [_['score'] for _ in nlp]
    median = pd.DataFrame(scores)

    # median = median.drop(['very high', 'high', 'mixed'], axis=1).median().to_dict()
    median = median.median().to_dict()
    zero = {
        'center': 0.079685,
        'conspiracy': 0.070119,
        'extreme left': 0.015009,
        'extreme right': 0.075946,
        'fake news': 0.23967,
        'hate': 0.039379,
        'high': 0.489697,
        'left': 0.077148,
        'left-center': 0.228174,
        'low': 0.030978,
        'mixed': 0.06897,
        'pro-science': 0.142508,
        'propaganda': 0.05581,
        'right': 0.052456,
        'right-center': 0.054424,
        'satire': 0.037862,
        'very high': 0.090974
    }
    # median = {k: v - zero[k] for k, v in median.items()}
    median = {k: v for k, v in median.items()}

    insert({'page': page, 'scores': median, 'posts': len(text_dict)})

    return median
    # median = sorted(median.items(), key=lambda kv: kv[1], reverse=True)
    # print(median[:3])
    # if 'left' in median and 'right' in median:
    #     print('moderate')


def check_db(page_id):
    return db['facescraper'].find({'page': page_id}).count() > 100


def check_scores(page_id):
    # return db['nlp'].find({'page': page_id}).count() > 150
    return next(db['nlp'].find({'page': page_id}))


if __name__ == '__main__':
    # print(check_db('foxnews'))

    if len(sys.argv) > 1:

        page_id = sys.argv[1]
        print(f'results for {page_id}')
    else:
        page_id = 'theatlantic'

    print(get_results(page_id))
