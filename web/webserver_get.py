"""
This module gets called by the web app each time a site is requested.

It orchestrates much of the user facing data processing including:
    * Checking for a valid web address
    * Spidering target site for article urls
    * Sending each article URL to a article scraping lambda to get text
    * Sending the accumulated text to the NLP lambda
    * Activating the plotting function to plot the NLP results

"""

import json
import os
import hashlib
from itertools import islice
from multiprocessing import dummy
from time import sleep, time
from unidecode import unidecode

import boto3
import newspaper
import requests
import tldextract

from helpers import addDict, timeit
import mongo_query_results

NLP_API = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/dev_dnn_nlp'
SCRAPE_ARTICLES_API = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/scraper'
META_SCRAPER = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/meta_scraper'
PLOT_API = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/plotter'
TEST = False


class LambdaWhisperer:
    json_results = []

    def __init__(self):
        pass

    @timeit
    def scrape_api_endpoint(self, url_: str):
        req = requests.put(SCRAPE_ARTICLES_API, data=url_)
        req.raise_for_status()
        response = req.json()
        if 'message' in response:
            raise Exception('Lambda Error')  # TODO: custom exception class

        return {url_: response}

    @timeit
    def nlp_api_endpoint(self, url_text: dict, url: str, name_clean: str):
        url_text = {k: v for k, v in url_text.items() if type(v) == str}

        req = requests.put(NLP_API, json=url_text)
        req.raise_for_status()
        response = req.json()
        if 'message' in response:
            raise Exception('Lambda Error')  # TODO: custom exception class

        mongo_query_results.insert(response, name_clean)

        LambdaWhisperer.json_results, n_articles = mongo_query_results.get_scores(name_clean)
        return n_articles


class Titles:
    collect = []


class GetSite:

    def __init__(self, url, name_clean=None):
        self.API = LambdaWhisperer()
        self.bucket = boto3.resource('s3').Bucket('fakenewsimg')
        self.url = url
        if not name_clean:
            self.name_clean = self.strip()
        else:
            self.name_clean = self.strip()

    def run(self):
        if not self.url or self.url == 'ConnectionError':
            return self.url
        # Get list of newspaper.Article objs
        self.articles = []

        if mongo_query_results.check_age(self.name_clean):

            self.article_objs = self.get_newspaper()

        else:
            self.article_objs = 'Recent cache'  # TODO: enum.Enum

        if self.article_objs in ['No articles found!', 'Empty list', 'Recent cache']:
            print(self.article_objs)
            try:
                LambdaWhisperer.json_results, self.num_articles = mongo_query_results.get_scores(
                    self.url)

            except IndexError:
                return 'ConnectionError'  # TODO: enum.Enum
        else:
            # Threadpool for getting articles

            self.articles = self.download_articles()

            if self.articles == 'ConnectionError':
                return 'ConnectionError'  # TODO: enum.Enum
            elif len(self.articles) == 0:
                try:
                    LambdaWhisperer.json_results, self.num_articles = \
                        mongo_query_results.get_scores(self.name_clean)
                except IndexError:
                    return 'ConnectionError'  # TODO: enum.Enum
            else:
                self.num_articles = self.API.nlp_api_endpoint(
                    self.articles, self.url, self.name_clean
                )

        if self.articles:
            self.save_plot()

        print(self.url)
        print('NAME', self.name_clean)
        return self.num_articles, self.name_clean

    @timeit
    def save_plot(self):

        def clear_bucket_item():
            print('clearing plots from bucket')
            objects = [
                self.name_clean + fname
                for fname in ['_Political.png', '_Accuracy.png', '_Character.png']
            ]

            [
                print(self.bucket.delete_objects(Delete={
                    'Objects': [{
                        'Key': obj
                    },],
                    'Quiet': False
                })) for obj in objects
            ]

        print('Plotting article:')
        payload = [LambdaWhisperer.json_results, self.url, self.name_clean]
        req = requests.post(PLOT_API, json=payload)
        req.raise_for_status()
        print(req.text)
        print('results')
        print(payload)
        print('\n' * 3)

    @timeit
    def download_articles(self):
        try:
            urls = eval(self.article_objs)[:150]
        except TypeError:
            return 'ConnectionError'  # TODO: enum.Enum
        if len(urls) == 18 or urls == 'Empty list':
            print(urls)
            return 'ConnectionError'  # TODO: enum.Enum

        print('urls', len(urls))

        urls_filtered = mongo_query_results.filter_news_results(self.name_clean, urls)
        print('urls to download', len(urls_filtered))

        req = requests.put(META_SCRAPER, json=urls_filtered)
        req.raise_for_status()
        res = req.json()
        print('articles downloaded', len(res))
        # self.dud_articles(set(urls) ^ set(res.keys()))

        return res

    @timeit
    def dud_articles(self, duds):
        print('dud articles', len(duds))
        for dud in duds:
            hashed = hashlib.md5(dud.encode('utf-8')).hexdigest()

            mongo_query_results.dud(hashed)

    def strip(self):
        return ''.join(tldextract.extract(self.url))

        # return ''.join([char for char in '.'.join(tldextract.extract(self.url)[-2:]) if char.isalnum()])

    @timeit
    def get_newspaper(self):
        """ Get list of articles from site """
        return requests.put(SCRAPE_ARTICLES_API, self.url).text



if __name__ == '__main__':  # TODO: move to /tests for pytest
    test = False

    @timeit
    def run(url, sample_articles=None):
        GetSite(url, sample_articles).run()

    run('cnn.com')
