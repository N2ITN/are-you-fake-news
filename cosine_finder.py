import matplotlib
matplotlib.use('Agg')
#%%
from glob import glob
from pprint import pprint
import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
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

print = new_print


#%%
def LemmaTokenizer(text_):

    def process():
        tokens = nlp(text_)
        for token in tokens:
            if len(token) > 2 and token.is_alpha and not (token.is_stop):
                yield token.lemma_ or token

    return list(process())


class revector:

    def __init__(self, other):
        self.other = other
        self.vectorized = joblib.load('vectorizer.pkl')

    def transform(self):

        text_ = LemmaTokenizer(self.other)
        return self.vectorized.vectorizer.transform([text_])

    def nmf(self):

        # dtm = self.transform()

        # return NMF(n_components=1).fit(dtm).components_.sum(axis=0).reshape(1, -1)
        return self.transform()


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


@timeit
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
        except newspaper.article.ArticleException:
            return

        article.parse()

        if article.text and detect(article.title) == 'en':
            articles_text.txt.append(article.text + ' ' + article.title)
        time.sleep(.2)

    from multiprocessing import dummy

    pool = dummy.Pool(20)
    list(pool.map(scrape, scrape_list))
    return articles_text.txt


@timeit
def classify(text_input):

    def classifier(input_str):

        sample = revector(input_str)
        try:
            test = get_dist(sample.nmf())
        except ValueError as e:
            print(e)
            return {}
        return test

    if isinstance(text_input, str):
        return classifier(text_input(str))
    elif isinstance(text_input, list):

        accumulate = addDict()
        pol = ['extremeright', 'right-center', 'right', 'center', 'left-center', 'left', 'extremeleft']
        cred = ['low', 'mixed', 'high', 'veryhigh']

        for input_str in text_input:

            res = addDict(classifier(input_str))
            if argmax_pol_cred:
                cred_max = res.argmax(cred)
                pol_max = res.argmax(pol)
                for k in pol + cred:
                    res[k] = 0.
                res[pol_max[0]] = pol_max[1]
                res[cred_max[0]] = cred_max[1]

            accumulate = accumulate + res
        print(accumulate)
        return accumulate


vectors = {f.replace('./lsa_', '').replace('.pkl', ''): joblib.load(f) for f in glob('./lsa_*.pkl')}


class classifier_results:
    results = []


@timeit
def main(source_):
    articles_text = get_newspaper(source_)

    return classify(articles_text)


#%%
from functools import reduce
#%%
from helpers import addDict as addDict

#%%


@timeit
def plot():
    y, x = list(zip(*sorted(results.items(), key=lambda kv: kv[1], reverse=True)))

    x = x[:4]
    y = y[:4]
    x = x / np.sum(x)
    sns.set()

    def label_cleaner():
        key = {
            'fakenews': 'fake news',
            'extremeright': 'extreme right',
            'extremeleft': 'extreme left',
            'veryhigh': 'very high credibility',
            'low': 'low credibility',
            'pro-science': 'pro science',
            'mixed': 'mixed credibility',
            'high': 'high credibility'
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
    plt.title(argv[1])

    plt.savefig('temp.png', format='png', bbox_inches='tight', dpi=300)
    plt.show()


#%%

from sys import argv
argmax_pol_cred = False
if len(argv) > 1:
    results = main(argv[1])
    if len(argv) > 2:
        argmax_pol_cred = argv[3]

    plot()
#%%
