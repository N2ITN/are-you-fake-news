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
from itertools import islice
from multiprocessing import dummy
from time import sleep, time

import newspaper
import requests

from unidecode import unidecode

from helpers import addDict, timeit
import boto3
nlp_api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/dev_dnn_nlp'
scrape_articles_api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/scraper'
meta_scraper = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/meta_scraper'
plot_api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/plotter'
test = False


class LambdaWhisperer:
    json_results = []

    def __init__(self):
        pass

    @timeit
    def scrape_api_endpoint(self, url_: str):

        response = json.loads(requests.put(scrape_api, data=url_).text)

        if 'message' in response:
            raise Exception('Lambda Error')

        return {url_: response}

    @timeit
    def nlp_api_endpoint(self, url_text: dict, url: str):
        url_text = {k: v for k, v in url_text.items() if type(v) == str}

        import mongo_query_results

        response = json.loads(requests.put(nlp_api, json=url_text).text)

        url_text = json.dumps(url_text)
        #     response = json.loads(requests.put(nlp_api, json=url_text).text)
        if 'message' in response:
            raise Exception('Lambda Error')

        mongo_query_results.insert(response, url)
        LambdaWhisperer.json_results, n_articles = mongo_query_results.get_scores(url)
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
            self.name_clean = name_clean

    def run(self):
        import mongo_query_results
        if not self.url:
            return False
        if self.url == 'ConnectionError':
            return self.url
        # Get list of newspaper.Article objs
        self.article_objs = self.get_newspaper()

        if self.article_objs in ["No articles found!", "Empty list"]:
            try:
                LambdaWhisperer.json_results, self.num_articles = mongo_query_results.get_scores(
                    self.url)
            except IndexError:
                return 'ConnectionError'
        else:
            # Threadpool for getting articles

            self.articles = self.download_articles()
            if self.articles == 'ConnectionError':
                return 'ConnectionError'
            self.num_articles = self.API.nlp_api_endpoint(self.articles, self.url)

        if self.articles:
            self.save_plot()

        print(self.url)

        return self.num_articles, self.name_clean

    @timeit
    def save_plot(self):

        def clear_bucket_item():
            print("clearing plots from bucket")
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

        # try:
        #     clear_bucket_item()
        # except Exception as e:
        #     print(e)
        print("Plotting article:")
        payload = [LambdaWhisperer.json_results, self.url, self.name_clean]
        print(requests.post(plot_api, json=payload).text)
        print("results")
        print(payload)
        print('\n' * 3)

    @timeit
    def download_articles(self):
        import mongo_query_results
        urls = eval(self.article_objs)[:100]
        if len(urls) == 18:
            print(urls)
            return "ConnectionError"
        print('urls', len(urls))
        urls_filtered = mongo_query_results.filter_news_results(self.name_clean, urls)
        print('urls to download', len(urls_filtered))
        res = json.loads(requests.put(meta_scraper, json=urls_filtered).text)
        print('articles downloaded', len(res))
        self.dud_articles(set(urls) ^ set(res.keys()))
        return res

    @timeit
    def dud_articles(self, duds):
        print('dud articles', len(duds))
        import mongo_query_results
        import hashlib
        for dud in duds:
            hashed = hashlib.md5(dud.encode('utf-8')).hexdigest()

            mongo_query_results.dud(hashed)

    def strip(self):

        return ''.join([char for char in '.'.join(tldextract.extract(self.url)[-2:]) if char.isalnum()])

    @timeit
    def get_newspaper(self):
        """ Get list of articles from site """
        return requests.put(scrape_articles_api, self.url).text


import tldextract
if __name__ == '__main__':
    test = False

    @timeit
    def run(url, sample_articles=None):
        GetSite(url, sample_articles).run()

    run('cnn.com')
