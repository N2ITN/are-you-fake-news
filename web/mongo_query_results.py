import hashlib
import json
from pprint import pprint
from time import ctime

import pandas as pd
import requests
import tldextract
from pymongo import MongoClient

client = MongoClient()
db = client['newscraper']


def get_TLD(url):
    return ''.join([char for char in '.'.join(tldextract.extract(url)[-2:]) if char.isalnum()])


def insert(entries: list, url: str):
    print(entries)

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


def get_scores(url):
    print("SCORES")

    scores = [_['score'] for _ in list(get_TLD_entries(url))[0]['articles']]

    return pd.DataFrame(scores).median().to_dict(), len(scores)


if __name__ == '__main__':
    # db['queries'].drop
    # print(get_scores('naturalnews.com'))
    ...
