import itertools
import multiprocessing
import os
from multiprocessing.dummy import Pool
from time import sleep
import mongo_driver
import newspaper
from fake_useragent import UserAgent

os.environ['TLDEXTRACT_CACHE'] = '~/tldextract.cache'

config = newspaper.Config()
config.fetch_images = False
config.request_timeout = 3


class NewsSource:

    def __init__(self, source, n_articles=45):
        self._data = source
        self.url = 'http://www.' + source['url'].split('/')[0]
        self.categories = source['Category']
        self.n_articles = n_articles
        self.get_links()
        self.build_meta()
        print(self.url, self.categories)
        self.get_articles_controller()
        if self.source_obj.size() > 0:

            mongo_driver.insert('source_logs', self.meta)

    def build_meta(self):
        self.meta = {}
        self.meta['Meta'] = {
            'Source': self.url,
            'Size': self.source_obj.size(),
            'Flags': self.categories,
            'Description': self.source_obj.description
        }

    def get_links(self):
        ua = UserAgent()
        self.source_obj = newspaper.build(
            self.url, browser_user_agent=ua.chrome, language='en', config=config)

    def get_articles_controller(self):
        articles = self.source_obj.articles
        if not self.source_obj.articles:
            return

        def get_articles(article):
            article_data = {}
            article.url = article.url.strip()

            try:
                article.download()
                sleep(.1)
                article.parse()
            except Exception as e:
                print(e)
                return

            if article.title:
                # try:
                    # article.nlp()
                # except:
                # article_data['keywords'] = article.keywords
                article_data['title'] = article.title
                article_data['text'] = article.text
                article_data['flags'] = self.categories
                article_data['source'] = self.url
                article_data['url'] = article.url
                print(article_data['title'])
                mongo_driver.insert('articles', article_data)

        list(map(get_articles, articles[:self.n_articles]))


def go(source):
    NewsSource(source)


def threadpool():
    pool = Pool(50)
    x = pool.imap_unordered(go, batch)
    while True:
        try:
            x.next(timeout=10)
        except multiprocessing.context.TimeoutError:
            print('timeout!')
        except AttributeError as e:
            print(e)
        except StopIteration:
            print('batch finished.')
            pool.close()
            break
        except EOFError:
            pass


if __name__ == '__main__':
    news_sources = mongo_driver.get_all('all_sources')
    while True:
        try:
            batch = itertools.islice(news_sources, 300)
            threadpool()

        except StopIteration:
            print('finished.')
            break
