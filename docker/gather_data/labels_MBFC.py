"""
Scrapes the website bias labels from mediabiasfactcheck.com
and puts the results into a mongodb table
"""
import os
from logging import getLogger, config

import string
import unicodedata
from multiprocessing.dummy import Pool
from time import sleep
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, SoupStrainer

import mongo_driver

config.fileConfig('logging.ini')
logger = getLogger(__file__)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

HOST = 'mediabiasfactcheck.com'
SITE_URL = f'https://{HOST}/'

cat_pages =["left", "leftcenter", "center", "right-center", "right", "pro-science", "conspiracy", "fake-news", "satire"]


class accumulator:
    cat = None
    errors = []


def cat_links(cat):
    url = SITE_URL + cat
    logger.info("Fetching %s" % url)
    accumulator.cat = cat
    response = requests.get(url).text
    s = BeautifulSoup(response, 'html.parser').find(class_='entry clearfix')
    links_ = BeautifulSoup(str(s), 'html.parser', parse_only=SoupStrainer('a'))
    return links_


class UrlProcessor:

    def __init__(self, link):

        sleep(1)
        logger.info("Processing url %s" % link)
        self.orchestrate(link)

    def orchestrate(self, link):
        self.page = self.get_page(link)
        if self.page is None:
            return
        self.tag = self.get_tag()
        if self.tag is None:
            return
        self.get_targets()
        self.export_results()

    def get_page(self, link):
        if link.has_attr('href') and link['href'].startswith('http'):
            page = link['href']
            logger.debug("Getting page %s" % page)
            if page in mongo_driver.bias_urls() or '?share=' in page or '#print' in page or urlparse(page).hostname != HOST:
                logger.info('Skipping page %s' % page)
                return
            return page

    def get_tag(self):
        logger.info("Fetching page %s" % self.page)
        try:
            tag_ = BeautifulSoup(requests.get(self.page).text, 'html.parser').find_all(
                class_='entry-content')
            logger.debug("Parsed %s" % tag_)
            return tag_
        except requests.exceptions.ConnectionError:
            accumulator.errors.append({self.page: 'ConnectionError'})

    def get_targets(self):
        results = {}
        codex = {
            'Bias:': 'Truthiness',
            'Factual Reporting:': 'Truthiness',
            'Source:': 'url',
            'Sources:': 'url',
            'Notes: http://': 'url'
        }

        def clean(text_, key):
            cleaned = unicodedata.normalize('NFKD', text_).split(key + ' ')[1]
            if codex[key] == 'Bias':
                return cleaned.split(', ')
            elif codex[key] == 'Truthiness':
                [c for c in text_ if c in string.ascii_uppercase + ' ']
                return cleaned.split('\n')[0]
            else:
                return cleaned

        for t in self.tag:
            for key in codex:
                if key in t.text:
                    for p in t.find_all('p'):
                        if key in p.text:
                            results[codex[key]] = clean(p.text, key)

        self.results = results
        logger.debug("Got results")
        logger.debug(results)

    def export_results(self):
        logger.debug("Exporting results")

        self.results.update({'Reference': self.page, 'Category': accumulator.cat})
        logger.debug(self.results)

        logger.debug("Saving results to mongo")
        mongo_driver.insert('media_bias', self.results)


def cat_json():
    category_pages = (cat_links(cat) for cat in cat_pages)
    for page in category_pages:

        pool = Pool(10)
        pool.map(UrlProcessor, page)


if __name__ == '__main__':

    cat_json()

    logger.info(accumulator.errors)
    '''
    TODO:
        Make better variables and less hacky error handling
    '''
