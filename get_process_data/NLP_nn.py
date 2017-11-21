''' Vectorize corpus, train neural network with article labels'''
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
        from keras.preprocessing.text import Tokenizer
        tokenizer = Tokenizer()
        #%%
        texts = ['this test', 'here is another', 'how about that', 'one more', 'here is a test']
        tokenizer.fit_on_texts((self.preprocess(doc) for doc in self.text_)).texts_to_matrix()

        # self.vectorized.feature_names = vectorizer.feature_names
        # vectorizer = TfidfVectorizer(norm='l2', max_df=0.99, max_features=10000)

        # self.doc_term_matrix = vectorizer.fit_transform((self.preprocess(doc) for doc in self.text_))
        # self.vectorized.vectorizer = vectorizer
        joblib.dump(tokenizer, 'lsa_{}.pkl'.format(self.topic.replace(' ', '')))

    def preprocess(self, doc):

        if self.topic == None:
            self.topic = doc['flag']

        return ' '.join(doc['article'])


def vectorize_corpus():

    def corpus_gen():
        for i, _ in enumerate(mongo_driver.get_all('articles_cleaned')):

            if _['article']:
                yield _

    corpus_vec = TopicModeler(corpus_gen(), topic='corpus')
    corpus_vec.fit()


if __name__ == '__main__':

    vectorize_corpus()