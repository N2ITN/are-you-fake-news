from multiprocessing import dummy

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
import seaborn as sns

import newspaper

from helpers import addDict, timeit
from langdetect import detect
import json
# matplotlib.use('Agg')

api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/prod/newscraper'


@timeit
def api_endpoint(text_):
    response = json.loads(requests.put(api, data=text_).text)
    print(response)
    return response


@timeit
def send_to_lambda(articles):

    def articles_gen():
        yield from dummy.Pool(30).imap(scrape, articles)

    for article in articles_gen():

        yield article


@timeit
def scrape(article):

    # article = newspaper.Article(article.strip())
    # try:
    #     article.download()
    #     article.parse()
    # except newspaper.article.ArticleException:
    #     return

    # if article.text and detect(article.title) == 'en':
    #     print(article.title)
    #     print()
    # if article.text:
    # payload = article.text + ' ' + article.title
    payload = article
    article = ' '.join(list(filter(lambda c: c == ' ' or c.isalpha(), payload.split(' '))))
    return api_endpoint(article)


class GetSite:

    def __init__(self, url):
        self.url = self.https_test(url)
        self.articles = self.get_newspaper()
        # print(self.articles)
        self.run_lambda()
        # self.results = self.collect.softmax()
        # self.plot()

    @timeit
    def test_url(self, url_):
        try:
            if requests.get(url_).ok:
                return url_
            else:
                return False
        except requests.exceptions.ConnectionError:
            return False

    @timeit
    def https_test(self, url):
        if 'http://' or 'https://' not in url:
            url = self.test_url('https://' + url) or self.test_url('http://' + url)
            print(url)
            if not url:
                print('No website here!')
                return
            return (url)

    @timeit
    def run_lambda(self):

        @timeit
        def API():
            for res in send_to_lambda(self.get_newspaper()):

                # print(res)
                # self.collect + res
                yield res

        return list(API())

    @timeit
    def get_newspaper(self):

        # try:
        #     src = newspaper.build(
        #         self.url, fetch_images=False, request_timeout=3, limit=30, memoize_articles=False)
        #     from itertools import islice
        #     print(list(islice((a.url for a in src.articles), 10)))
        #     exit()
        #     # src.download()
        #     # src.parse()
        # except Exception as e:
        #     print(e)
        #     print(self.url)
        #     return "No articles found!"

        articles = [
            'https://cnn.com/2017/10/27/health/processed-food-eat-less-drayer/index.html',
            'http://www.cnn.com/interactive/2017/10/entertainment/neal-preston-cnnphotos/index.html',
            'https://cnn.com/2017/10/16/sport/gallery/what-a-shot-sports-1017/index.html',
            'https://cnn.com/2017/07/28/politics/john-mccain-maverick-health-care/index.html',
            'https://cnn.com/2017/10/26/entertainment/anna-wintour-james-corden/index.html',
            'https://cnn.com/2017/10/26/asia/indonesia-fireworks-factor-explosion/index.html',
            'https://cnn.com/2016/01/08/living/okcupid-polyamorous-open-relationships-feat/index.html',
            'https://cnn.com/2016/09/25/politics/white-working-class-overview-kff-poll/index.html',
            'https://cnn.com/2017/01/20/opinions/gallery/2017-opinion-cartoon-galley/index.html',
            'http://nymag.com/news/features/my-generation-2011-10/'
        ]
        for a in articles:
            _ = newspaper.Article(a)
            _.download()
            _.parse()
            yield _.text

    def plot(self):
        print(self.results)


if __name__ == '__main__':
    GetSite('cnn.com')
