from glob import glob
from helpers import timeit
import numpy as np
from sklearn.metrics.pairwise import cosine_distances

import joblib
import spacy

import newspaper
from langdetect import detect

nlp = spacy.load('en_core_web_sm')


@timeit
def orchestrate(article):
    return scrape(article)


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
        return Classify(article.text + ' ' + article.title)


class VectorFit:
    ''' Transform input text to fit the training tf-idf vector '''

    def __init__(self, other):
        self.other = other

        self.vectorized = joblib.load(open('vectorizer.pkl', 'rb'))

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


@timeit
class CosineCalcs:
    ''' input a new vector, recieve all distances back '''
    vectors = {f.replace('./lsa_', '').replace('.pkl', ''): joblib.load(f) for f in glob('./lsa_*.pkl')}

    def __init__(self, vec):
        ''' calculate cosine distance '''
        self.in_vect = vec

    def vec_from_model(self, vname):
        components = CosineCalcs.vectors[vname].components_
        array = components[0]
        for row in components[1:]:
            array += np.square(row)

        return array.reshape(1, -1)

    def distances(self):
        for v in CosineCalcs.vectors:
            yield v, round(1. - float(cosine_distances(self.vec_from_model(v), self.in_vect)), 3)


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
