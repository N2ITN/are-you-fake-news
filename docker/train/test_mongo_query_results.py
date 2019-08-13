import json
from pprint import pprint
from time import ctime
import tldextract
import requests
from pymongo import MongoClient
import hashlib
from add_dict import AddDict
client = MongoClient()
db = client['newscraper']


def get_TLD(url):
    return ''.join([char for char in '.'.join(tldextract.extract(url)[-2:]) if char.isalnum()])


def insert(url: str, entries: list):
    TLD = get_TLD(url)
    prev_urls = db['queries'].find().distinct('url')
    print(prev_urls)
    for entry in entries:
        if entry['url'] not in prev_urls:
            new = {'articles': entry}
            db['queries'].update_one({'TLD': TLD}, {'$push': new}, upsert=True)

            db['queries'].update_one({'url': entry['url']}, {'$set': {'url': entry['url']}}, upsert=True)


def get_TLD_entries(url):
    return db['queries'].find({'TLD': get_TLD(url)})


if __name__ == '__main__':
    # db['queries'].drop()

    entries = [{
        'score': {
            'hate': 0.000117,
            'low': 0.036948,
            'mixed': 0.004485,
            'satire': 0.000486,
            'center': 0.000184,
            'pro-science': 0.000139,
            'extreme right': 0.000158,
            'conspiracy': 0.349955,
            'fake news': 0.000376,
            'right': 9.7e-05,
            'extreme left': 0.0,
            'right-center': 0.004446,
            'left': 0.005477,
            'very high': 1.4e-05,
            'high': 0.018363,
            'left-center': 0.00029,
            'propaganda': 0.000116
        },
        'url': '1e571fd2a6b730ed87aa2f8fe7c00b27',
        'timestamp': '02/12/18'
    }, {
        'score': {
            'hate': 0.010018,
            'low': 0.74259,
            'mixed': 0.002012,
            'satire': 0.0,
            'center': 0.003828,
            'pro-science': 0.001176,
            'extreme right': 0.159544,
            'conspiracy': 0.993555,
            'fake news': 0.05063,
            'right': 0.001056,
            'extreme left': 2e-06,
            'right-center': 0.001567,
            'left': 1.1e-05,
            'very high': 0.001493,
            'high': 0.010507,
            'left-center': 0.01214,
            'propaganda': 0.031203
        },
        'url': '593560e0bbcaef78d1f241a923f27147',
        'timestamp': '02/12/18'
    }, {
        'score': {
            'hate': 0.0,
            'low': 1.0,
            'mixed': 0.000108,
            'satire': 0.0,
            'center': 0.0,
            'pro-science': 0.0,
            'extreme right': 3e-06,
            'conspiracy': 1.0,
            'fake news': 1e-06,
            'right': 0.0,
            'extreme left': 0.0,
            'right-center': 1e-06,
            'left': 0.0,
            'very high': 0.0,
            'high': 5e-06,
            'left-center': 0.001661,
            'propaganda': 4e-06
        },
        'url': 'a24239402274bf268c1c3e68ae6b6afd',
        'timestamp': '02/12/18'
    }]

    url = 'http://www.naturalnews.com/something'
    insert(url, entries)

    from pprint import pprint
    # pprint(list(db['queries'].find()))

    # pprint(list(get_TLD_entries(url)))
    print(len(list(get_TLD_entries(url))[0]['articles']))
