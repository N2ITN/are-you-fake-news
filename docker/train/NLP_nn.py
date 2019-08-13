""" 
Vectorizes the corpus from all of the collected articles, saves it to a pickle file
`lsa_corpus.pkl`
"""

import pickle

import mongo_driver
from tensorflow import keras
Tokenizer = keras.preprocessing.text.Tokenizer


class TopicModeler:

    def __init__(self, articles_gen, n_words=20000, topic=None):

        self.text_ = articles_gen
        self.topic = topic
        self.n_words = n_words

    def fit(self):

        tokenizer = Tokenizer(num_words=self.n_words)

        tokenizer.fit_on_texts([self.preprocess(doc) for doc in self.text_])

        pickle.dump(tokenizer, open('lsa_{}.pkl'.format(self.topic.replace(' ', '')), 'wb'))

    def preprocess(self, doc):
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