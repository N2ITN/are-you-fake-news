#%%
from glob import glob
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import cm
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_distances

import joblib
import newspaper
import spacy
from helpers import addDict, new_print
from NLP_machine import Model

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

        dtm = self.transform()

        return NMF(n_components=1).fit(dtm).components_.sum(axis=0).reshape(1, -1)


def get_v(name):
    components = vectors[name].components_
    array = components[0]
    for row in components[1:]:
        array += np.square(row)

    return array.reshape(1, -1)


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


def get_newspaper(source_):
    br = newspaper.build(source_, memoize_articles=False)

    br.download()
    br.parse()
    articles_text = []
    for i, article in enumerate(br.articles):
        article.download()
        article.parse()

        print(article.title)
        if len(article.text) > 100:
            articles_text.append(article.text)
        if i == 15:
            break
    return articles_text


def classify(text_input):

    def classifier(input_str):

        sample = revector(input_str)
        test = get_dist(sample.nmf())
        pprint(test)

        return test

    if isinstance(text_input, str):
        return classifier(text_input(str))
    elif isinstance(text_input, list):

        accumulate = addDict()

        for input_str in text_input:

            accumulate = accumulate + addDict(classifier(input_str))
        return accumulate


vectors = {f.replace('./lsa_', '').replace('.pkl', ''): joblib.load(f) for f in glob('./lsa_*.pkl')}


def main(source_):
    articles_text = get_newspaper(source_)

    return classify(articles_text)


#%%
from functools import reduce
#%%
from helpers import addDict as addDict


#%%
def average_spectrums():
    dict = addDict

    crediblity_spectrum = dict(zip(['low', 'mixed', 'high', 'veryhigh'], range(1, 5)))
    political_spectrum = dict(
        zip(['extremeright', 'right-center', 'right', 'center', 'left-center', 'left', 'extremeleft'],
            range(1, 8)))
    crediblity_scores = {}
    political_scores = {}
    for r in results:
        if r in crediblity_spectrum:
            crediblity_scores[crediblity_spectrum[r]] = results[r]
        if r in political_spectrum:
            political_scores[political_spectrum[r]] = results[r]
    pol_ = list(map(lambda kv: kv[0] * kv[1], political_scores.items()))

    cred_ = list(map(lambda kv: kv[0] * kv[1], crediblity_scores.items()))

    cred_n = crediblity_spectrum.reverse()[int(np.mean(cred_))]
    pol_n = political_spectrum.reverse()[int(np.mean(pol_))]
    new_results = results.copy()
    for k in political_spectrum.keys():
        if k in new_results:
            new_results.pop(k)
    for k in crediblity_spectrum.keys():
        if k in new_results:
            new_results.pop(k)
    new_results[cred_n] = np.mean(cred_) / len(cred_)
    new_results[pol_n] = np.mean(pol_) / len(pol_)
    return new_results


#%%


def plot():
    new_results = average_spectrums()
    y, x = list(zip(*sorted(new_results.items(), key=lambda kv: kv[1], reverse=True)))

    x = x[:7]
    y = y[:7]
    x = x / np.sum(x)
    sns.set()

    def label_cleaner():
        key = {
            'fakenews': 'fake news',
            'extremeright': 'extreme right',
            'veryhigh': 'very high credibility',
            'low': 'low credibility',
            'pro-science': 'pro science',
            'mixed': 'mixed credibility'
        }
        for label in y:
            for k, v in key.items():
                label = label.replace(k, v)
            yield label.replace('high', 'high credibility').title()

    y = list(label_cleaner())
    y_pos = np.arange(len(y))
    plt.figure(figsize=(8, 8))
    sns.barplot(y=y_pos, x=x, palette='viridis_r', orient='h')

    plt.yticks(y_pos, y)
    plt.ylabel('Usage')
    plt.title('Rating')
    print()
    plt.savefig('temp.png', format='png', bbox_inches='tight', dpi=300)
    plt.show()


#%%
results = main('http://www.foxnews.com')
plot()
