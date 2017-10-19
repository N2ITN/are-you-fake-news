from fake_useragent import UserAgent
import os
os.environ['TLDEXTRACT_CACHE'] = '~/tldextract.cache'
import newspaper
from time import sleep
from multiprocessing.dummy import Pool
from pprint import pprint


class NewsSource:

    def __init__(self, source, n_articles=5):
        self._data = source
        self.url = 'http://www.' + source['url'].split('/')[0]
        print(self.url)
        self.categories = source['Category']
        self.n_articles = n_articles
        self.get_links()
        self.build_meta()
        self.get_articles_controller()
        if self.source_obj.size()size > 0:
            pprint(self.meta)
            mongo_driver.insert('articles', self.meta)

    def build_meta(self):
        self.meta = {}
        self.meta['Meta'] = {
            'Source': self.url,
            'Size': self.source_obj.size(),
            'Flags': self.categories,
            'Description': self.source_obj.description
        }

        self.meta['Articles'] = []

    def get_links(self):
        ua = UserAgent()
        self.source_obj = newspaper.build(self.url, browser_user_agent=ua.chrome, language='en')

    def get_articles_controller(self):
        articles = self.source_obj.articles
        if not self.source_obj.articles:
            print("No articles")
            return

        def get_articles(article):
            article_data = {}
            article.url = article.url.strip()
            article.download()

            try:
                article.parse()
            except Exception as e:
                print(e)
                return

            if article.title:
                # article.nlp()
                # article_data[article.title] = {'keywords': article.keywords}
                # self.meta['Articles'].append(article_data)
                article_data['title'] = article.title
                article_data['text'] = article.texts
                self.meta['Articles'].append(article_data)

        list(map(get_articles, articles[:self.n_articles]))


if __name__ == '__main__':
    import mongo_driver
    news_sources = mongo_driver.get_all('all_sources')
    feed_list = list(news_sources)

    pool = Pool(50)
    pool.map(NewsSource, feed_list)
