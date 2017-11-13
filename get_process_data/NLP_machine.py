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

    def __init__(self, articles_gen, n_top_words=15, n_topics=7, show=False, topic=None):
        self.show_topics = show
        self.n_top_words = n_top_words
        self.n_topics = n_topics
        self.text_ = articles_gen
        self.vectorized = Model()
        self.topic = topic

    @timeit
    def fit(self):

        # self.vectorized.feature_names = vectorizer.feature_names
        vectorizer = TfidfVectorizer(norm='l2', min_df=10, max_df=0.95, max_features=10000)

        self.doc_term_matrix = vectorizer.fit_transform((self.preprocess(doc) for doc in self.text_))
        self.vectorized.vectorizer = vectorizer

    def preprocess(self, doc):

        if self.topic == None:
            self.topic = doc['flag']

        return ' '.join(doc['article'])

    @timeit
    def LSA(self):
        dtm = self.doc_term_matrix
        model = NMF(n_components=self.n_topics).fit(dtm)
        self.vectorized.nmf = model.fit(dtm).components_.mean(axis=0).reshape(1, -1)

        joblib.dump(self.vectorized, 'lsa_{}.pkl'.format(self.topic.replace(' ', '')))

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

    for _ in mongo_driver.get_articles_by_flag():
        yield _


def vectorize_corpus():

    def corpus_gen():
        for i, _ in enumerate(mongo_driver.get_all('articles_cleaned')):

            if _['article']:  #and _['flag'] != 'satire':
                yield _

    corpus_vec = TopicModeler(corpus_gen(), topic='corpus')
    corpus_vec.fit()
    corpus_vec.LSA()


#%%


def run_vectorize():
    for tag in flags_articles_gen():

        category = TopicModeler(tag)

        category.fit()
        category.LSA()


if __name__ == '__main__':

    run_vectorize()
    vectorize_corpus()