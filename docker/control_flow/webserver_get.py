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

import requests


import newspaper
import tldextract
from helpers import addDict, timeit
from langdetect import detect
from unidecode import unidecode
from logging import getLogger, config
config.fileConfig('logging.ini')
logger = getLogger(__file__)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
nlp_api = 'http://nlp:5000'
scrape_articles_api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/scraper'
meta_scraper = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/dev/meta_scraper'


class LambdaWhisperer:
    json_results = []

    def __init__(self):
        pass

    @timeit
    def nlp_api_endpoint(self, url_text: dict, url: str, name_clean: str):
        url_text = {k: v for k, v in url_text.items() if type(v) == str}
        import mongo_query_results
        response = json.loads(requests.post(nlp_api, json=url_text).text)
        url_text = json.dumps(url_text)
        #     response = json.loads(requests.put(nlp_api, json=url_text).text)
        if 'message' in response:
            raise Exception('Lambda Error')
        mongo_query_results.insert(response, name_clean)
        LambdaWhisperer.json_results, n_articles = mongo_query_results.get_scores(name_clean)
        return n_articles


class Titles:
    collect = []


class GetSite:

    def __init__(self, url, name_clean=None):
        self.API = LambdaWhisperer()
        self.url = url

        if name_clean is None:
            name_clean = ''.join(tldextract.extract(url))
        self.name_clean = name_clean

    def run(self):
        import mongo_query_results

        if not self.url or self.url == 'ConnectionError':
            return self.url
        # Get list of newspaper.Article objs
        self.articles = []

        if mongo_query_results.check_age(self.name_clean):

            self.article_objs = self.get_newspaper()

        else:
            self.article_objs = "Recent cache"

        if self.article_objs in ["No articles found!", "Empty list", "Recent cache"]:
            logger.info(self.article_objs)
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
            elif self.articles == 'LanguageError':
                return 'LanguageError'
            elif len(self.articles) == 0:
                try:

                    LambdaWhisperer.json_results, self.num_articles = mongo_query_results.get_scores(
                        self.name_clean)
                except IndexError:
                    return 'ConnectionError'
            else:
                self.num_articles = self.API.nlp_api_endpoint(self.articles, self.url, self.name_clean)

        # if self.articles:
        #     self.save_plot()

        logger.info(self.url)
        logger.info(f"NAME {self.name_clean}")
        payload = {
            'scores': LambdaWhisperer.json_results,
            'url': self.url,
            'name_clean': self.name_clean,
            'n_articles': self.num_articles
        }
        return payload

    @timeit
    def download_articles(self):

        import mongo_query_results
        try:
            urls = eval(self.article_objs)[:100]
        except TypeError:
            return "ConnectionError"
        if len(urls) == 18 or urls == "Empty list":
            logger.info(urls)
            return "ConnectionError"

        logger.info('urls', len(urls))

        urls_filtered = mongo_query_results.filter_news_results(self.name_clean, urls)
        logger.info(f'urls to download  {len(urls_filtered)}')
        logger.info(urls_filtered)
        res = json.loads(requests.put(meta_scraper, json=urls_filtered).text)

        logger.info(f'articles downloaded {len(res)}')

        try:
            test_article = ' '.join([_ for _ in list(res.values()) if isinstance(_, str)])
            logger.info(f"{test_article} {type(test_article)}")
            if not test_article:
                return "ConnectionError"
            if not detect(test_article) == 'en':
                return "LanguageError"
        except TypeError:

            return "ConnectionError"
        return res

    @timeit
    def dud_articles(self, duds):
        logger.info(f'dud articles {len(duds)}')
        import mongo_query_results
        import hashlib
        for dud in duds:
            hashed = hashlib.md5(dud.encode('utf-8')).hexdigest()

            mongo_query_results.dud(hashed)

    def strip(self):
        return ''.join(tldextract.extract(self.url))

    @timeit
    def get_newspaper(self):
        """ Get list of articles from site """
        return requests.put(scrape_articles_api, self.url).text
