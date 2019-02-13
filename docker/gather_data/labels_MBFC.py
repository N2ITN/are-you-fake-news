"""
Scrapes the website bias labels from mediabiasfactcheck.com
and puts the results into a mongodb table
"""
import os
from logging import getLogger, config

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

cat_pages =["left", "leftcenter", "center", "right-center", "right", "pro-science", "conspiracy", "fake-news", "satire", "re-evaluated-sources"]


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
        self.link = link
        logger.debug("Processing url %s" % link)
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
            text = requests.get(self.page).text
            logger.debug("Extracting tag from page %s" % self.page)
            # It seems some pages skip the 'entry-content' class, eg https://mediabiasfactcheck.com/al-jazeera/
            # while others have our targets outside the entry-content class, eg. https://mediabiasfactcheck.com/council-on-american-islamic-relations-cair/
            # but inside the 'entry' tag, so use that instead of the 'entry-content' class.
            tag_ = BeautifulSoup(text, 'html.parser').find_all(class_='entry')
            logger.debug("Parsed %s from %s" % (tag_, self.page))
            return tag_
        except requests.exceptions.ConnectionError:
            accumulator.errors.append({self.page: 'ConnectionError'})

    def get_targets(self):
        results = {}
        codex = { # Maps mbfcc labels (eg Reasoning) to our inner labels (eg Truthiness)
            'Bias:': 'Truthiness',
            'Factual Reporting:': 'Truthiness', # Eg. Mixed
            'Reasoning:': 'Truthiness', # Eg. Extreme Right, Propaganda, Conspiracy, Failed Fact Checks
            'Source:': 'url',
            'Sources:': 'url',
            'Notes: http://': 'url'
        }

        def clean(text_, key):
            cleaned = unicodedata.normalize('NFKD', text_).split(key + ' ')[1]
            if codex[key] == 'Truthiness':
                # Eg. cleaned equals 'MIXED\nCountry: USA\nWorld Press Freedom Rank: USA 45/180'
                return cleaned.split('\n')[0]
            else:
                return cleaned

        for t in self.tag:
            for key in codex:
                if key in t.text:
                    for p in t.find_all('p'):
                        if key in p.text:
                            results[codex[key]] = clean(p.text, key)
                            logger.debug("Page %s has a %s value of %s" % (self.link, codex[key], results[codex[key]]))
        if not results:
            logger.warning("Unable to extract any key from %s - tag %s" % (self.link, self.tag))
        self.results = results
        logger.info("Got results from %s - %s" % (self.link, results))

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
