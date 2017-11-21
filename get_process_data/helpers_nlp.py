""" Does NLP preprocessing only """
import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
import nltk
import unicodedata

import joblib

from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.stop_words import \
    ENGLISH_STOP_WORDS as stopwords

stopwords_ = set(stopwords)
[stopwords_.add(_) for _ in ['the', 'this', 'use', 'just', 'of', 'there', 'these', 'like']]


def fix_unicode(u):
    u = unicodedata.normalize('NFKD', u).encode('ascii', 'ignore')
    return str(u, 'utf-8')


def LemmaTokenizer(text_):
    stemmer = PorterStemmer().stem

    def process():
        tokens = fix_unicode(text_).split(' ')
        for token in tokens:
            token = token.lower()
            if len(token) > 2 and all([c.isalpha() for c in token]) and not token in stopwords_:
                yield stemmer(token.lower())

    return list(process())


corpus_vector = joblib.load('./lsa_corpus.pkl').vectorizer

import pickle


def transform(text):
    text_ = LemmaTokenizer(text)
    sparse_matrix = corpus_vector.transform(text_)
    return pickle.dumps(sparse_matrix)
