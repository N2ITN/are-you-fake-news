''' Does NLP stuff '''
#%%
import json
from helpers import timeit
from sklearn.decomposition import NMF, LatentDirichletAllocation
import joblib
import mongo_driver

from itertools import islice
import numpy as np

#%%


class Model:

    def __init__(self):
        self.doc_term_matrix = None
        self.feature_names = None
        self.flag_index = []
        self.vectorizer = None


class TopicModeler:

    def __init__(self, tags_arcticles, n_top_words=10, n_topics=15, refit=False):
        self.refit = refit
        self.n_top_words = n_top_words
        self.n_topics = n_topics
        self.text_ = tags_arcticles

        self.vectorized = Model()

    @timeit
    def fit(self):
        import os
        if self.refit:
            try:
                os.remove('./vectorizer.pkl')
            except FileNotFoundError:
                pass
        try:
            self.vectorized = joblib.load('vectorizer.pkl')
        except Exception as e:

            import textacy

            vectorizer = textacy.Vectorizer(
                weighting='tfidf',
                normalize=True,
                smooth_idf=True,
                min_df=2,
                max_df=0.95,
                max_n_terms=5000)

            self.vectorized.doc_term_matrix = vectorizer.fit_transform((self.preprocess(doc)
                                                                        for doc in self.text_))

            self.vectorized.feature_names = vectorizer.feature_names
            self.vectorized.vectorizer = vectorizer

            joblib.dump(self.vectorized, 'vectorizer.pkl')

    def preprocess(self, doc):
        flag, val = doc
        self.vectorized.flag_index.append(flag)

        return val

    def LSA(self):
        for topic in set(self.vectorized.flag_index):

            self.topic_gen(topic)

    @timeit
    def topic_gen(self, topic, model='lda'):
        if self.refit:
            try:
                os.remove('./lsa_lda{}.pkl'.format(topic))
            except FileNotFoundError:
                pass
        try:
            self.vectorized = joblib.load('./lsa_lda{}.pkl'.format(topic))
            print('loaded lsa')
        except Exception as e:
            dtm = self.vectorized.doc_term_matrix[np.array(self.vectorized.flag_index) == topic]

            if model == 'nmf':
                model = NMF(n_components=self.n_topics).fit(dtm)
            elif model == 'lda':
                model = LatentDirichletAllocation(
                    n_components=self.n_topics,
                    max_iter=10,
                    learning_method='batch',
                    learning_offset=50.)

            self.lsa_model = model.fit(dtm)

            joblib.dump(self.lsa_model, './lsa_lda{}.pkl'.format(topic))

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

        yield _['flag'], _['article']


#%%


def run_vectorize():
    test = TopicModeler(flags_articles_gen())
    test.fit()
    test.show()
    return test


mod = run_vectorize()

mod.LSA()