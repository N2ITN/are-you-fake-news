"""
Generator to stream articles from mongo during neural net training

"""
import pickle

from helpers_nlp import LemmaTokenizer

from pymongo import MongoClient

client = MongoClient(connect=False)
db = client['newscraper']

corpus_vector = pickle.load(open('./lsa_corpus.pkl', 'rb'))
n_articles = int(open('n_articles.json').read())


def transform(text):
    text_ = LemmaTokenizer(text)
    return corpus_vector.texts_to_matrix(text_, mode='tfidf')


def vectorize_article():

    def corpus_gen():
        for i, _ in enumerate(
                db['articles_cleaned'].aggregate([{
                    "$sample": {
                        'size': n_articles
                    }
                }], allowDiskUse=True)):
            if _['article']:
                yield _['flags'], _['article']

    for flag, article in corpus_gen():
        try:
            yield flag, transform(' '.join(article))
        except Exception as e:
            raise e


if __name__ == '__main__':

    print(next(vectorize_article()))
