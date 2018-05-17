import json
from time import ctime, time
import hashlib

import requests
import pandas as pd
import tldextract
from pymongo import MongoClient

from helpers import timeit

CLIENT = MongoClient(connect=False)
DB = CLIENT['newscraper']


def get_TLD(url):
    return ''.join(tldextract.extract(url))

    # return ''.join([char for char in '.'.join(tldextract.extract(url)[-2:]) if char.isalnum()])


@timeit
def filter_news_results(domain: str, article_urls: list):

    prev_hashes = DB['queries'].find().distinct('url')
    return [k for k in article_urls if hashlib.md5(k.encode('utf-8')).hexdigest() not in prev_hashes]


def dud(url):
    DB['queries'].update_one({'url': url}, {'$set': {'url': url}}, upsert=True)


def check_age(url):
    """
    check if website has been spidered within last day

    returns True to spider + scrape
    returns False to not

    """
    '''
    THIS IS WRONG
    It only checks if someone has *tried* to look at the site, and in doing so, updates
    timestamp, effectively locking out popular sites.
    '''
    spider = True
    try:
        # Is url in table
        res = next(DB['cache'].find({'url': url}))
    except StopIteration:
        # If no url exists, add one
        print('ERROR no age cache')
        DB['cache'].insert({'url': url, 'last_access': time()})
        res = None

    if res:
        # Has the site been spidered in the time window? If so spider = False
        access = res['last_access']
        delta = time() - access
        spider = delta > 3600 * 5

        print('delta', delta)
        print('last access', access)
        print('now', time())
        print(spider)

        if spider:
            # If the site is to be rescraped
            DB['cache'].remove({'url': url})
            DB['cache'].insert({'url': url, 'last_access': time()})

    return spider


def del_TLD(TLD):
    DB['queries'].remove({'TLD': TLD})


def delete_cached_duds():
    url_only = [x for x in DB['queries'].find().distinct('url') if not x.startswith('http')]
    [DB['queries'].remove({'url': x}) for x in url_only]


def insert(entries: list, url: str):

    TLD = get_TLD(url)
    # prev_urls = db['queries'].find({'TLD': url}).distinct('url')
    try:
        prev_urls = set([x['url'] for x in list(DB['queries'].find({'TLD': url}))[0]['articles']])
    except (IndexError, KeyError):
        prev_urls = []

    try:
        for entry in entries:

            if entry['url'] not in prev_urls:
                new = {'articles': entry}
                DB['queries'].update_one({'TLD': TLD}, {'$push': new}, upsert=True)
                DB['queries'].update_one(
                    {
                        'url': entry['url']
                    }, {'$set': {
                        'url': entry['url']
                    }}, upsert=True)
    except Exception as e:
        print(entries)
        raise e
    print('inserted {} entries'.format(len(entries)))


def get_TLD_entries(url):
    return DB['queries'].find({'TLD': get_TLD(url)})


def get_scores(url):
    print('SCORES')
    print(url)
    try:
        scores = [_['score'] for _ in list(get_TLD_entries(url))[0]['articles'] if 'score' in _]
    except IndexError:
        print('No articles in DB!')
        return 'ConnectionError', 0
    print(len(scores))
    for score in scores:
        if score == pd.DataFrame(scores).median().to_dict():
            raise Exception
    return pd.DataFrame(scores).median().to_dict(), len(scores)


# if __name__ == '__main__':
#     cnn = [
#         "http://cnn.com/2015/07/07/us/illinois-athletics-allegations/index.html",
#         "http://cnn.com/2015/05/19/us/scam-charity-investigation/index.html",
#         "http://cnn.com/2015/04/13/us/airport-luggage-theft/index.html",
#         "http://cnn.com/2015/09/10/us/virgin-islands-pesticide-investigation/index.html",
#         "http://cnn.com/2015/03/13/us/va-investigation-los-angeles/index.html",
#         "http://cnn.com/2015/03/13/us/irs-scam/index.html",
#         "http://cnn.com/2014/11/17/us/south-dakota-indian-school-fundraising-investigation/index.html",
#         "http://cnn.com/2014/10/29/politics/politicians-play-lobbyists-pay/index.html",
#         "http://cnn.com/2016/09/22/us/immigration-attitudes-cnn-kff-poll/index.html",
#         "http://cnn.com/2016/09/25/politics/white-working-class-overview-kff-poll/index.html",
#         "http://cnn.com/2016/09/20/politics/2016-election-white-working-class-voters/index.html",
#         "http://cnn.com/2016/09/24/politics/white-working-class-evangelicals/index.html",
#         "http://cnn.com/2016/09/23/opinions/shell-shocked-white-working-class-opinion-coontz/index.html",
#         "http://cnn.com/2016/09/20/politics/election-2016-white-working-class-donald-trump-kaiser-family-foundation/index.html",
#         "http://cnn.com/2016/09/20/politics/white-working-class-americans-have-split-on-muslim-immigrants-trump-clinton/index.html",
#         "http://money.cnn.com/2016/09/21/news/economy/white-working-class-government/index.html?iid=hp-toplead-dom",
#         "http://www.cnn.com/2016/09/19/politics/trump-supporters-working-class-white-kaiser-family-foundation-infographic/index.html",
#         "http://money.cnn.com/2016/09/23/news/economy/white-working-class-economy/index.html",
#         "http://cnn.com/2017/08/15/world/iyw-aid-sierra-leone-mudslide-victims/index.html",
#         "http://cnn.com/2017/03/16/world/iyw-how-to-help-east-africa/index.html",
#         "http://cnn.com/2016/10/19/middleeast/iyw-mosul-iraq-how-to-help/index.html",
#         "http://cnn.com/2016/05/10/health/iyw-prescription-drug-abuse-how-to-help-health/index.html",
#         "http://cnn.com/2017/08/07/world/iyw-impact-of-youssif/index.html",
#         "http://cnn.com/2016/10/28/us/iyw-girl-friendship-trnd/index.html",
#         "http://cnn.com/2016/09/28/world/iyw-girl-up-michelle-obama-girls-education-how-to-help/index.html",
#         "http://cnn.com/2015/01/06/world/iyw-syria-resource-list/index.html",
#         "http://cnn.com/2017/06/28/world/elle-snow-trafficking/index.html",
#         "http://cnn.com/2017/05/30/world/ciw-fair-food-program-freedom-project/index.html",
#         "http://cnn.com/2017/06/02/world/tonys-chocolonely-slavery-free-chocolate/index.html",
#         "http://cnn.com/2017/04/26/americas/brazil-amazon-slavery-freedom-project/index.html",
#         "http://cnn.com/2017/07/26/asia/cambodia-brick-kiln/index.html",
#         "http://cnn.com/2017/07/24/asia/return-to-cambodia-sex-trafficking/index.html",
#         "http://www.cnn.com/interactive/2014/05/specials/city-of-tomorrow/index.html",
#         "http://www.cnn.com/interactive/2014/09/health/cnn10-healthiest-cities/"
#     ]
#     ...
