from glob import glob

import numpy as np
from sklearn.decomposition import NMF
from pprint import pprint
from sklearn.metrics.pairwise import cosine_distances

import joblib
import spacy
from lemmatize_articles import LemmaTokenizer
from NLP_machine import Model

nlp = spacy.load('en_core_web_sm')


def LemmaTokenizer(text_):

    def process():
        tokens = nlp(text_)
        for token in tokens:
            if len(token) > 2 and token.is_alpha and not (
                    token.is_stop):  #and  and token.lemma_ != '-PRON-':
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
    return vectors[name].components_.sum(axis=0).reshape(1, -1)


def get_dist(v1):

    def distances():
        for k in vectors:
            yield k, round(1. - float(cosine_distances(get_v(k), v1)), 3)

    return sorted(list(distances()), key=lambda _: _[1], reverse=True)


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


pickle_jar = glob('./lsa_*.pkl')

vectors = {f.replace('./lsa_', '').replace('.pkl', ''): joblib.load(f) for f in pickle_jar}

if __name__ == '__main__':

    sample = revector(open('sample_text.txt').read())
    test = get_dist(sample.nmf())
    pprint(test)

    print(test[:5])
