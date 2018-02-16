import json
from pprint import pprint
from time import ctime
import hashlib
import pandas as pd
import requests
import tldextract
from helpers import timeit
from pymongo import MongoClient

client = MongoClient(connect=False)
db = client['newscraper']


def get_TLD(url):
    return ''.join([char for char in '.'.join(tldextract.extract(url)[-2:]) if char.isalnum()])


@timeit
def filter_news_results(domain: str, article_urls: list):

    try:
        new_hashes = {url: hashlib.md5(url.encode('utf-8')).hexdigest() for url in article_urls}
        prev_queries = list(db['queries'].find({'TLD': domain}))[0]
        prev_hashes = set(a['url'] for a in prev_queries['articles'])
        unseen_urls = set(new_hashes.values()) ^ prev_hashes

        results = [k for k in new_hashes.keys() if new_hashes[k] in unseen_urls]

        print("{} existing urls, {} found, {} new".format(
            len(prev_hashes), len(article_urls), len(results)))
        print("returning {} results".format(len(results[:30])))

        return results[:100]
    except Exception as e:
        print("Error filtering out previous queries: {}".format(e))
        return article_urls


def insert(entries: list, url: str):

    TLD = get_TLD(url)
    prev_urls = db['queries'].find().distinct('url')

    print(type(entries), type(url))

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
    cnn = [
        "http://cnn.com/2015/07/07/us/illinois-athletics-allegations/index.html",
        "http://cnn.com/2015/05/19/us/scam-charity-investigation/index.html",
        "http://cnn.com/2015/04/13/us/airport-luggage-theft/index.html",
        "http://cnn.com/2015/09/10/us/virgin-islands-pesticide-investigation/index.html",
        "http://cnn.com/2015/03/13/us/va-investigation-los-angeles/index.html",
        "http://cnn.com/2015/03/13/us/irs-scam/index.html",
        "http://cnn.com/2014/11/17/us/south-dakota-indian-school-fundraising-investigation/index.html",
        "http://cnn.com/2014/10/29/politics/politicians-play-lobbyists-pay/index.html",
        "http://cnn.com/2016/09/22/us/immigration-attitudes-cnn-kff-poll/index.html",
        "http://cnn.com/2016/09/25/politics/white-working-class-overview-kff-poll/index.html",
        "http://cnn.com/2016/09/20/politics/2016-election-white-working-class-voters/index.html",
        "http://cnn.com/2016/09/24/politics/white-working-class-evangelicals/index.html",
        "http://cnn.com/2016/09/23/opinions/shell-shocked-white-working-class-opinion-coontz/index.html",
        "http://cnn.com/2016/09/20/politics/election-2016-white-working-class-donald-trump-kaiser-family-foundation/index.html",
        "http://cnn.com/2016/09/20/politics/white-working-class-americans-have-split-on-muslim-immigrants-trump-clinton/index.html",
        "http://money.cnn.com/2016/09/21/news/economy/white-working-class-government/index.html?iid=hp-toplead-dom",
        "http://www.cnn.com/2016/09/19/politics/trump-supporters-working-class-white-kaiser-family-foundation-infographic/index.html",
        "http://money.cnn.com/2016/09/23/news/economy/white-working-class-economy/index.html",
        "http://cnn.com/2017/08/15/world/iyw-aid-sierra-leone-mudslide-victims/index.html",
        "http://cnn.com/2017/03/16/world/iyw-how-to-help-east-africa/index.html",
        "http://cnn.com/2016/10/19/middleeast/iyw-mosul-iraq-how-to-help/index.html",
        "http://cnn.com/2016/05/10/health/iyw-prescription-drug-abuse-how-to-help-health/index.html",
        "http://cnn.com/2017/08/07/world/iyw-impact-of-youssif/index.html",
        "http://cnn.com/2016/10/28/us/iyw-girl-friendship-trnd/index.html",
        "http://cnn.com/2016/09/28/world/iyw-girl-up-michelle-obama-girls-education-how-to-help/index.html",
        "http://cnn.com/2015/01/06/world/iyw-syria-resource-list/index.html",
        "http://cnn.com/2017/06/28/world/elle-snow-trafficking/index.html",
        "http://cnn.com/2017/05/30/world/ciw-fair-food-program-freedom-project/index.html",
        "http://cnn.com/2017/06/02/world/tonys-chocolonely-slavery-free-chocolate/index.html",
        "http://cnn.com/2017/04/26/americas/brazil-amazon-slavery-freedom-project/index.html",
        "http://cnn.com/2017/07/26/asia/cambodia-brick-kiln/index.html",
        "http://cnn.com/2017/07/24/asia/return-to-cambodia-sex-trafficking/index.html",
        "http://www.cnn.com/interactive/2014/05/specials/city-of-tomorrow/index.html",
        "http://www.cnn.com/interactive/2014/09/health/cnn10-healthiest-cities/"
    ]
    print(filter_news_results('cnncom', cnn))
    ...
