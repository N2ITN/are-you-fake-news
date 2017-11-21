import joblib
from mongo_driver import db
from helpers_nlp import LemmaTokenizer

from models import Model

corpus_vector = joblib.load('./lsa_corpus.pkl').vectorizer


def transform(text):

    text_ = LemmaTokenizer(text)
    return corpus_vector.transform(text_)


def vectorize_article():

    def corpus_gen():

        for i, _ in enumerate(db['articles_cleaned'].find().sort('articles', -1)):
            # for i, _ in enumerate(db['articles_cleaned'].find()):

            if _['article']:
                yield _['flag'], _['article']

    for flag, article in corpus_gen():

        try:
            yield flag, transform(' '.join(article))
        except Exception as e:
            raise e
