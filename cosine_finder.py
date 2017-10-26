import matplotlib
matplotlib.use('Agg')
#%%
from glob import glob
from pprint import pprint
import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_distances

import joblib
import newspaper
import spacy
from helpers import addDict, new_print, timeit
from NLP_machine import Model

import pickle
from langdetect import detect
nlp = spacy.load('en_core_web_sm')

#%%

# print = new_print

#%%


class revector:

    def __init__(self, other):
        self.other = other
        self.vectorized = joblib.load('vectorizer.pkl')

    def LemmaTokenizer(self, text_):

        def process():
            tokens = nlp(text_)
            for token in tokens:
                if len(token) > 2 and token.is_alpha and not (token.is_stop):
                    yield token.lemma_ or token

        return list(process())

    def transform(self):

        text_ = self.LemmaTokenizer(self.other)
        return self.vectorized.vectorizer.transform([text_])


#%%
def get_v(name):
    components = vectors[name].components_
    array = components[0]
    for row in components[1:]:
        array += np.square(row)
        # array += row

    return array.reshape(1, -1)


#%%
def get_dist(v1):

    def distances():
        for k in vectors:
            yield k, round(1. - float(cosine_distances(get_v(k), v1)), 3)

    return dict(distances())


def cosine():
    done = set()
    for k in vectors:
        done.add(k)
        for k1 in vectors:
            if not k1 in done:
                done.add(k1)
            else:
                continue

            yield ' : '.join(sorted((k, k1))), round(1. - float(cosine_distances(get_v(k), get_v(k1))),
                                                     3)

    cosine_dist_dict = {k: v for k, v in cosine()}
    sorted(cosine_dist_dict.items(), key=lambda kv: kv[1], reverse=True)


class articles_text:
    txt = []
    titles = []


# @timeit
def get_newspaper(source_):
    br = newspaper.build(source_, memoize_articles=False)

    br.download()
    br.parse()

    scrape_list = []
    for i, article in enumerate(br.articles):
        scrape_list.append(article)
        if i == 30:
            break

    def scrape(article):
        article.url = article.url.strip()#.split('/#')[0].replace(' https://www.infowars.com/ ', '') # infowars is weird
        try:
            article.download()
            article.parse()
        except newspaper.article.ArticleException:
            return

        if article.text and detect(article.title) == 'en':
            print(article.title)
            print()
            articles_text.txt.append(article.text + ' ' + article.title)
            articles_text.titles.append(article.title)
        time.sleep(.2)

    from multiprocessing import dummy

    pool = dummy.Pool(5)
    list(pool.map(scrape, scrape_list))
    return articles_text.txt


# @timeit
def classify(text_input):
    pol = [
        'extremeright',
        'right-center',
        'right',
        'center',
        'left-center',
        'left',
        'extremeleft',
    ]
    cred = [
        'fakenews',
        'low',
        'unreliable',
        'mixed',
        'high',
        'veryhigh',
    ]

    def argmax(dict_):
        cred_max = dict_.argmax(cred, n=1)
        pol_max = dict_.argmax(pol, n=1)
        for k in pol + cred:
            dict_[k] = 0.

        dict_[pol_max[0][0]] = pol_max[0][1]
        dict_[cred_max[0][0]] = cred_max[0][1]
        return dict_

    def classifier(input_str):

        sample = revector(input_str)
        try:
            test = get_dist(sample.transform())
        except ValueError as e:
            print(e)
            return {}
        return test

    if isinstance(text_input, str):
        return classifier(text_input(str))
    elif isinstance(text_input, list):

        accumulate = addDict()

        def weight(goal, d):
            weights = []
            scores = []
            for i, k in enumerate(goal, start=1):
                if k in d:
                    weights.append(i * d[k])
                    scores.append(d[k])
            ave = np.mean(weights)
            best = goal[int(round(ave / np.mean(scores)))]
            # print(best)
            # print(weights)
            # print(ave)
            # print()
            for k in goal:
                if k != best:
                    d[k] = 0.0001

            return d

        for input_str in text_input:
            res = addDict(classifier(input_str))
            # res = weight(pol, res)
            # res = weight(cred, res)
            accumulate = accumulate + res
        # pprint(accumulate)
        # accumulate = weight(pol, accumulate)
        # accumulate = weight(cred, accumulate)

        # pprint(accumulate)

        accumulate = argmax(accumulate)
        # pprint(accumulate)
        return accumulate


vectors = {f.replace('./lsa_', '').replace('.pkl', ''): joblib.load(f) for f in glob('./lsa_*.pkl')}


#@timeit
def main(source_):
    articles_text = get_newspaper(source_)

    return classify(articles_text)


#%%
from functools import reduce
#%%
from helpers import addDict as addDict

#%%


#@timeit
def plot(results, target):
    results_ = {k: v for k, v in results.items() if v != 0}
    y, x = list(zip(*sorted(results_.items(), key=lambda kv: kv[1], reverse=True)))

    # x = x[:5]
    # y = y[:5]
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
    plt.title(target)

    name = ''.join([
        c for c in target.replace('https://', '').replace('http://', '').replace('www.', '')
        if c.isalpha()
    ])
    plt.savefig('static/{}.png'.format(name), format='png', bbox_inches='tight', dpi=300)
    plt.show()


#%%

from sys import argv

if len(argv) > 1:
    url = argv[1]

    results = main(url)

    plot(results, url)


def get(url):
    if 'http://' or 'https://' not in url:
        url = 'https://' + url
    results = main(url)

    plot(results, url)
    return articles_text.titles

    # print(len(), 'articles')


#%%
