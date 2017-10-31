''' Does NLP stuff '''
import json
import os
from itertools import islice

import joblib
import numpy as np
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

from langdetect import detect
import mongo_driver
from models import Model

from helpers import timeit


class TopicModeler:

    def __init__(self, tags_arcticles, n_top_words=15, n_topics=20, refit=True, show=True):

        self.refit = refit
        self.n_top_words = n_top_words
        self.n_topics = n_topics
        self.text_ = tags_arcticles

        self.vectorized = Model()
        # if show:
        #     self.show()

    @timeit
    def fit(self):

        if self.refit:
            try:
                os.remove('reconstructed_NMF.pkl')
            except FileNotFoundError:
                pass
        try:
            self.inverse_transformer = joblib.load('reconstructed_NMF.pkl')
            self.vectorized = joblib.load('vectorizer.pkl')
            print('loaded pickles')
        except Exception as e:

            vectorizer = TfidfVectorizer(
                smooth_idf=True,
                min_df=10,
                max_df=0.95,
                max_features=10000,)

            self.doc_term_matrix = vectorizer.fit_transform((self.preprocess(doc) for doc in self.text_))
            self.vectorized.vectorizer = vectorizer
            self.vectorized.feature_names = vectorizer.get_feature_names()
            joblib.dump(self.vectorized, 'vectorizer.pkl')
            self.nmf = NMF(n_components=self.n_topics).fit(self.doc_term_matrix)
            self.transformer = self.nmf.transform(self.doc_term_matrix)
            self.inverse_transformer = self.nmf.inverse_transform(self.transformer)
            print('NMF topic model', self.nmf.components_.shape)
            print('transformed NMF', self.transformer.shape)
            print('inverse_transform', self.inverse_transformer.shape)
            joblib.dump(self.inverse_transformer, 'reconstructed_NMF.pkl')

    def preprocess(self, doc):
        flag, val = doc
        self.vectorized.flag_index.append(flag)

        return ' '.join(val)

    def LSA(self):
        for topic in set(self.vectorized.flag_index):

            self.topic_gen(topic)

    @timeit
    def topic_gen(self, topic):

        dtm = self.inverse_transformer[np.array(self.vectorized.flag_index) == topic]

        print(dtm.shape)
        dtm = dtm.sum(axis=0)

        joblib.dump(dtm, 'lsa_{}.pkl'.format(topic.replace(' ', '')))

    def show(self):

        for topic_idx, topic in enumerate(self.nmf.components_):
            print(" ".join(
                [self.vectorized.feature_names[i] for i in topic.argsort()[:-self.n_top_words - 1:-1]]))
        print()


''' Getting docs by arcticles_tagged'''


def flags_articles_gen():

    for i, _ in enumerate(mongo_driver.get_all('articles_cleaned')):

        if _['article'] and _['flag'] != 'satire':
            yield _['flag'], _['article']


#%%


def run_vectorize():
    test = TopicModeler(flags_articles_gen())
    test.fit()

    return test


if __name__ == '__main__':
    mod = run_vectorize()

    mod.LSA()
