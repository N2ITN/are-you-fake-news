import user_agent
import os
os.environ['TLDEXTRACT_CACHE'] = '~/tldextract.cache'
import newspaper
from time import sleep
from multiprocessing.dummy import Pool


class NewsSource:

    def __init__(self, source, vals=None, n_articles=50):
        self.source = 'http://www.' + source
        if vals:
            self.types = list(
                filter(lambda x: x, sorted(set([vals['type'], vals['2nd type'], vals['3rd type']]))))
        else:
            self.types = None
        self.source_obj = None
        self.size = None
        self.n_articles = n_articles
        self.get_links()
        self.build_meta()
        self.get_articles_controller()

    def build_meta(self):
        self.meta = {}
        self.meta['Meta'] = {
            'Source': self.source,
            'Size': self.source_obj.size(),
            'Flags': [_.lower() for _ in self.types],
            'Description': self.source_obj.description
        }
        self.meta['Articles'] = []

    def get_links(self):
        self.source_obj = newspaper.build(
            self.source, browser_user_agent=user_agent.generate_user_agent(), language='en')

    def get_articles_controller(self):
        # TODO: Add threading
        articles = self.source_obj.articles
        if not self.source_obj.articles:
            return

        def get_articles(article):
            article_data = {}
            article.url = article.url.strip()
            article.download()
            # sleep(2)
            try:
                article.parse()
            except Exception as e:
                print(e)

                return

            if article.title:
                article.nlp()
                article_data[article.title] = {'keywords': article.keywords}  #, 'text': article.text}
                self.meta['Articles'].append(article_data)
                print(article.title)

        list(map(get_articles, articles[:self.n_articles]))