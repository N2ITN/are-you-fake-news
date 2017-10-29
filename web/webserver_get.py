# from langdetect import detect
import json
import os
from multiprocessing import dummy

import matplotlib.pyplot as plt
import numpy as np
import requests
import seaborn as sns

import newspaper
from newscraper.helpers import timeit

# matplotlib.use('Agg')

api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/prod/newscraper'


class Collection:
    json_results = []


@timeit
def api_endpoint(text_):
    response = json.loads(requests.put(api, data=text_).text)
    Collection.json_results.append(response)
    return response


@timeit
def send_to_lambda(articles):

    @timeit
    def articles_gen():
        yield from dummy.Pool(35).imap_unordered(scrape, articles)

    return api_endpoint(' '.join(list(articles_gen())))


@timeit
def scrape(article):
    payload = article
    article = ' '.join(list(filter(lambda c: c == ' ' or c.isalpha(), payload.split(' '))))

    return article


class GetSite:

    def __init__(self, url, test=True, name_clean=None):
        if test == False:
            self.url = self.https_test(url)
            self.articles = self.get_newspaper()
        else:
            self.url = self.https_test(url)
            self.articles = self.get_articles((newspaper.Article(a) for a in cnn_sample))
        if not name_clean:
            self.name_clean = self.strip()
        else:
            self.name_clean = name_clean
        self.run_lambda()
        self.dump()
        plot(self.url, self.name_clean)

    def strip(self):
        return ''.join([
            c for c in self.url.replace('https://', '').replace('http://', '').replace('www.', '')
            if c.isalpha()
        ])

    def dump(self):

        j_path = 'newscraper/web/static/{}.json'.format(self.name_clean)
        with open(j_path, 'w') as fp:
            json.dump(Collection.json_results, fp, sort_keys=True)
        assert os.path.exists(j_path)

    @timeit
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
            return url

    @timeit
    def run_lambda(self):

        @timeit
        def API():
            for res in send_to_lambda(self.articles):

                yield res

        return list(API())

    @timeit
    def get_newspaper(self):

        try:
            src = newspaper.build(
                self.url, fetch_images=False, request_timeout=3, limit=5, memoize_articles=False)
            src.download()
            src.parse()

        except Exception as e:
            print(e)
            print(self.url)
            return "No articles found!"

        yield from self.get_articles(src.articles)

    def get_articles(self, articles):
        for i, a in enumerate(articles):
            if i > 5:
                break
            try:
                a.download()
                a.parse()
            except newspaper.article.ArticleException:
                pass
            yield a.text + ' ' + a.title


@timeit
def plot(url, name_clean):
    results_ = {k: v for k, v in Collection.json_results[0].items() if v != 0}
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
    plt.title(url.replace('https://', '').replace('http://', ''))

    plt.savefig(
        'newscraper/web/static/{}.png'.format(name_clean), format='png', bbox_inches='tight', dpi=200)

    # plt.show()


cnn_sample = [
    "http://www.theatlantic.com/national/archive/2014/03/here-is-when-each-generation-begins-and-ends-according-to-facts/359589/",
    "http://www.cnn.com/interactive/2014/05/specials/city-of-tomorrow/index.html",
    "http://money.cnn.com/news/world/",
    "https://cnn.com/style/article/la-raza-autry-museum-los-angeles/index.html",
    "https://cnn.com/2017/10/27/sport/judo-abu-dhabi-grand-slam-tal-flicker-israel-national-anthem-flag/index.html",
    "https://cnn.com/travel/article/china-unesco-site-kulangsu/index.html",
    "http://www.cnn.com/travel/article/eqi-glacier-greenland/index.html",
    "http://money.cnn.com/video/news/2017/10/25/mega-millions-lottery-changes-sje-lon-orig.cnnmoney/index.html",
    "https://cnn.com/2017/10/26/health/undocumented-child-federal-custody-surgery-trnd/index.html",
    "https://cnn.com/2017/09/29/politics/tom-price-resigns/index.html",
    "https://cnn.com/2017/10/20/health/caffeine-fix-food-drayer/index.html",
    "https://cnn.com/2016/09/20/politics/white-working-class-americans-have-split-on-muslim-immigrants-trump-clinton/index.html"
]

if __name__ == '__main__':

    @timeit
    def run(url, sample_articles=None):
        GetSite(url, sample_articles)
        plot(url)
        print(Collection.json_results)

    # run('cnn.com')

    run('cnn.com')
