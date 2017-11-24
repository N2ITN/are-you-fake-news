''' Vectorize corpus, train neural network with article labels'''

import pickle

import mongo_driver


class TopicModeler:

    def __init__(self, articles_gen, n_words=50000, topic=None):

        self.text_ = articles_gen

        self.topic = topic
        self.n_words = n_words

    def fit(self):
        from keras.preprocessing.text import Tokenizer
        tokenizer = Tokenizer(num_words=self.n_words)
        #%% mode='tfidf')

        tokenizer.fit_on_texts([self.preprocess(doc) for doc in self.text_])
        # tokenizer.texts_to_matrix(self.text_, mode='tfidf')
        # print(sorted(tokenizer.word_counts.items(), key=lambda x: x[1]))

        pickle.dump(tokenizer, open('lsa_{}.pkl'.format(self.topic.replace(' ', '')), 'wb'))

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