from newspaper import news_pool
from langdetect import detect
import requests
from fake_useragent import UserAgent
import newspaper
import mongo_driver
from time import sleep
from multiprocessing.dummy import Pool
import os
import multiprocessing
import itertools
from logging import getLogger, config
from helpers import addDict
import json
"""
Websites with bias labels are scraped for articles. Each article gets stored with its
bias tags in a MongoDB table.

TODO: Address the class imbalance in the data. Some important categories (hate, for example)
    are underrepresented in the scraped article counts. In the past I have manually rescraped
    underrepresented tags, but it would be nice to have a sort of 'load balancer' to balance
    classes during the scraping.

"""


os.environ['TLDEXTRACT_CACHE'] = '~/tldextract.cache'

config.fileConfig('logging.ini')
logger = getLogger(__file__)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

newspaper_config = newspaper.Config()
newspaper_config.fetch_images = False
newspaper_config.request_timeout = 2
newspaper_config.memoize_articles = False


class NewsSource:

    def __init__(self, newspaper_obj, metadata, n_articles=1000):
        self.n_articles = n_articles
        self.newspaper_obj = newspaper_obj
        self.metadata = metadata
        self.url = metadata['url']

    def build(self):

        self.categories = self.metadata['Category']
        self.build_metadata()
        logger.info(f"found {self.newspaper_obj.size()} articles for {self.url}")

        self.get_articles_controller()
        mongo_driver.insert('source_logs', self.meta)

    def build_metadata(self):
        self.meta = {}
        self.meta['Meta'] = {
            'Source': self.url,
            'Size': self.newspaper_obj.size(),
            'Flags': self.categories,
            'Description': self.newspaper_obj.description
        }

    def get_articles_controller(self):
        articles = self.newspaper_obj.articles

        def get_articles(article):
            article_data = {}
            article.url = article.url.strip()

            if article.title:

                if len(article.text) > 200:
                    article_data['text'] = article.text
                    article_data['title'] = article.title
                    article_data['text'] = article.text
                    article_data['flags'] = self.categories
                    article_data['source'] = self.url
                    article_data['url'] = article.url
                    logger.info(f"{self.categories}    {article_data['source']} {article_data['title']}")
                    mongo_driver.insert('articles', article_data)

        for x in articles:
            get_articles(x)


def test_https(url):

    def test_url(url_):
        try:

            return requests.get(url_, timeout=1).ok

        except requests.exceptions.ReadTimeout:
            return False
        except requests.exceptions.ConnectionError:
            return False
        except requests.exceptions.TooManyRedirects:
            return False

    if 'http://' or 'https://' not in url:
        _url = 'https://' + url

        if test_url(_url) == False:
            _url = 'http://' + url
            if test_url(_url) == False:
                return False
        url = _url
    return url


def threadpool(batch):

    logger.info(f" processing {[source['url'] for source in batch]}")

    papers = []
    sources = []
    for source in batch:
        source['url'] = test_https(source['url'])
        if source['url'] == False:

            continue

        paper = newspaper.build(source['url'], config=newspaper_config)
        papers.append(paper)
        sources.append(source)

    news_pool.set(papers, threads_per_source=10)
    news_pool.join()

    for i, metadata in enumerate(sources):

        if papers[i].articles:
            logger.info(f'analyzing {metadata["url"]},{len(papers[i].articles)} found')

            NewsSource(newspaper_obj=papers[i], metadata=metadata).build()
        else:
            logger.info(f'skipping {metadata["url"]}, no articles')


if __name__ == '__main__':
    # Take random samples from sources to mitigate impact of interruptions
    news_sources = mongo_driver.db['all_sources'].aggregate(
        [{
            "$sample": {
                'size': mongo_driver.db['all_sources'].count()
            }
        }], allowDiskUse=True)

    # filter for certain categories
    # news_sources = mongo_driver.db['all_sources'].find({
    #     'Category': {
    #         "$in": ['extreme left', 'satire', 'hate', 'pro-science', 'very high', 'low', 'right']
    #     }
    # })

    batch_size = 15

    def run_scraper():
        batch = [next(news_sources) for _ in range(batch_size)]

        threadpool(batch)

    for i in range(mongo_driver.db['all_sources'].count() // batch_size):
        run_scraper()
