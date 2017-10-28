from multiprocessing import dummy

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
import seaborn as sns

import newspaper

from helpers import addDict, timeit
from lambda_build import cosine_dist
from langdetect import detect

matplotlib.use('Agg')


@timeit
def send_to_lambda(articles):

    yield dummy.Pool(2).map_async(cosine_dist.orchestrate, map(scrape, articles))


@timeit
def scrape(article):

    article = newspaper.Article(article.strip())
    try:
        article.download()
        article.parse()
    except newspaper.article.ArticleException:
        return

    if article.text and detect(article.title) == 'en':
        print(article.title)
        print()
        payload = article.text + ' ' + article.title

        return ' '.join(list(filter(lambda c: c == ' ' or c.isalpha(), payload.split(' '))))


class GetSite:

    def __init__(self, url):
        self.url = self.https_test(url)
        self.articles = self.get_newspaper()
        self.collect = CombineResults()
        self.run_lambda()
        self.results = self.collect.softmax()
        self.plot()

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
                r = res.get()
                self.collect + r
                yield r

        return list(API())

    @timeit
    def get_newspaper(self):
        try:
            src = newspaper.build(self.url, memoize_articles=False)
            src.download()
            src.parse()
        except Exception as e:
            print(e)
            print(self.url)
            return "No articles found!"
        for i, article in enumerate(src.articles):
            yield article.url
            if i == 2:
                break

    @timeit
    def plot(self):

        results_ = {k: v for k, v in self.results.items() if v != 0}
        y, x = list(zip(*sorted(results_.items(), key=lambda kv: kv[1], reverse=True)))

        x = x / np.sum(x)
        sns.set()

        def label_cleaner():
            key = {
                'fakenews': 'fake news',
                'extremeright': 'extreme right',
                'extremeleft': 'extreme left',
                'veryhigh': 'very high veracity',
                'low': 'low veracity',
                'pro-science': 'pro science',
                'mixed': 'mixed veracity',
                'high': 'high veracity'
            }
            for label in y:
                for k, v in key.items():
                    if label == k:
                        label = v.title()

                yield label.title()

        y = list(label_cleaner())

        y_pos = np.arange(len(y))
        plt.figure(figsize=(8, 8))
        sns.barplot(y=y_pos, x=x, palette='viridis_r', orient='h')
        plt.yticks(y_pos, y)
        plt.ylabel('Usage')
        plt.title(self.url.replace('https://', '').replace('http://', ''))

        name = ''.join([
            c for c in self.url.replace('https://', '').replace('http://', '').replace('www.', '')
            if c.isalpha()
        ])
        plt.savefig('static/{}.png'.format(name), format='png', bbox_inches='tight', dpi=300)
        plt.show()


class CombineResults:

    def __init__(self):
        self.pol = [
            'extremeright', 'right-center', 'right', 'center', 'left-center', 'left', 'extremeleft'
        ]
        self.cred = ['fakenews', 'low', 'unreliable', 'mixed', 'high', 'veryhigh']
        self.results = addDict({})

    def __add__(self, new_article):

        print(self.results)
        self.results = self.results + addDict(new_article[0])

    def __iadd__(self, new_article):
        return self.results + addDict(new_article[0])

    def softmax(self):
        # self.results = self.lickert_scale()
        self.results = self.argmax()
        return self.results

    def argmax(self):
        pol = self.pol
        cred = self.cred
        cred_max = self.results.argmax(cred, n=1)
        pol_max = self.results.argmax(pol, n=1)
        for k in pol + cred:
            self.results[k] = 0.

        self.results[pol_max[0][0]] = pol_max[0][1]
        self.results[cred_max[0][0]] = cred_max[0][1]
        return self.results

    def lickert_scale(goal):
        weights = []
        scores = []
        for i, k in enumerate(goal, start=1):
            if k in self.results:
                weights.append(i * self.results[k])
                scores.append(self.results[k])
        ave = np.mean(weights)
        best = goal[int(round(ave / np.sum(scores)))]

        for k in goal:
            if k != best:
                self.results[k] = 0.0001

        return self.results


class Model:

    def __init__(self):
        self.doc_term_matrix = None
        self.feature_names = None
        self.flag_index = []
        self.vectorizer = None


if __name__ == '__main__':
    GetSite('cnn.com')
