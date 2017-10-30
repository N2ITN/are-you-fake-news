''' Does NLP stuff '''
import json
import os
from itertools import islice

import joblib
import numpy as np
from sklearn.decomposition import NMF, TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

from langdetect import detect
import mongo_driver
from models import Model

from helpers import timeit


class TopicModeler:

    def __init__(self, tags_arcticles, n_top_words=15, n_topics=20, refit=True, show=False):
        self.show_topics = show
        self.refit = refit
        self.n_top_words = n_top_words
        self.n_topics = n_topics
        self.text_ = tags_arcticles

        self.vectorized = Model()

    @timeit
    def fit(self):

        if self.refit:
            try:
                os.remove('vectorizer.pkl')
            except FileNotFoundError:
                pass
        try:
            self.vectorized = joblib.load('vectorizer.pkl')
        except Exception as e:

            params = {'smooth_idf': True, 'min_df': 10, 'max_df': 0.95, 'max_features': 10000}
            # self.vectorized.feature_names = vectorizer.feature_names
            corpus = [self.preprocess(doc) for doc in self.text_]
            vectorizer = TfidfVectorizer(params)
            self.vectorized.vectorizer = vectorizer.fit(corpus)

            self.doc_term_matrix = TfidfVectorizer(params).fit_transform(corpus)

            print(dir(self.vectorized.vectorizer))
            # print(vars(vectorizer))

            # open('keywords.txt', 'w').write(str(vectorizer.feature_names))
            joblib.dump(self.vectorized, 'vectorizer.pkl')

    def preprocess(self, doc):
        flag, val = doc
        self.vectorized.flag_index.append(flag)

        return ' '.join(val)

    def LSA(self):
        for topic in set(self.vectorized.flag_index):

            self.topic_gen(topic)

    @timeit
    def topic_gen(self, topic, model='nmf'):
        if self.refit:
            try:
                os.remove('lsa_{}.pkl'.format(topic.replace(' ', '')))
            except FileNotFoundError:
                pass
        try:
            self.lsa_model = joblib.load('lsa_{}.pkl'.format(topic.replace(' ', '')))
            print('loaded lsa')

        except Exception as e:
            dtm = self.doc_term_matrix[np.array(self.vectorized.flag_index) == topic]

            if model == 'tsvd':
                model = TruncatedSVD(n_components=7)

            if model == 'nmf':
                model = NMF(n_components=self.n_topics).fit(dtm)
            elif model == 'lda':
                model = LatentDirichletAllocation(
                    n_components=self.n_topics,
                    max_iter=10,
                    learning_method='batch',
                    learning_offset=50.)
            self.lsa_model = model.fit_transform(dtm)
            joblib.dump(self.lsa_model, 'lsa_{}.pkl'.format(topic.replace(' ', '')))

        if self.show_topics:
            self.show(topic)

    def sentiment(self):
        print(TextBlob(' '.join(self.arcticles_tagged[tag])).sentiment, '\n')

    def show(self, topic):
        print(topic)
        for topic_idx, topic in enumerate(self.lsa_model.components_):
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
