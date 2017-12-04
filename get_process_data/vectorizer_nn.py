import pickle
from mongo_driver import db
from helpers_nlp import LemmaTokenizer

corpus_vector = pickle.load(open('./lsa_corpus.pkl', 'rb'))


def transform(text):

    text_ = LemmaTokenizer(text)

    return corpus_vector.texts_to_matrix(text_, mode='tfidf')


def vectorize_article(size=43000):
    
    def corpus_gen():

        for i, _ in enumerate(
                db['articles_cleaned'].aggregate([{
                    "$sample": {
                        'size': size
                    }
                }], allowDiskUse=True)):
            if _['article']:
                yield _['flag'], _['article']

    for flag, article in corpus_gen():

        try:
            yield flag, transform(' '.join(article))
        except Exception as e:
            raise e
