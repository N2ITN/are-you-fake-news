from glob import glob
from helpers import timeit
import numpy as np
from sklearn.metrics.pairwise import cosine_distances

import joblib

from helpers import LemmaTokenizer

from models import Model


@timeit
def orchestrate(article):
    return Classify(article)


class VectorFit:
    ''' Transform input text to fit the training tf-idf vector '''

    def __init__(self, other):
        self.other = other

        self.vectorized = joblib.load('./vectorizer.pkl')

    def transform(self):

        text_ = LemmaTokenizer(self.other)
        print(text_)
        return self.vectorized.vectorizer.transform(text_)


@timeit
class CosineCalcs:
    ''' input a new vector, recieve all distances back '''
    vectors = {f.replace('./lsa_', '').replace('.pkl', ''): joblib.load(f) for f in glob('./lsa_*.pkl')}

    def __init__(self, vec):
        ''' calculate cosine distance '''
        self.in_vect = vec.mean(axis=0)
        print(dir(vec))
        print(vec.get_shape())

    def vec_from_model(self, vname):
        components = CosineCalcs.vectors[vname]

        return np.squeeze(components).reshape(1, -1)

    def distances(self):
        for v in CosineCalcs.vectors:
            yield v, float(cosine_distances(self.vec_from_model(v), self.in_vect).T[0])


class Model:

    def __init__(self):
        self.doc_term_matrix = None
        self.feature_names = None
        self.flag_index = []
        self.vectorizer = None


class Classify:

    def __new__(self, text_input):

        return Classify.classify_text(text_input)

    @timeit
    def classify_text(input_str):

        sample = VectorFit(input_str)

        try:
            return list(CosineCalcs(sample.transform()).distances())
        except ValueError as e:
            print(e)
            return {}
