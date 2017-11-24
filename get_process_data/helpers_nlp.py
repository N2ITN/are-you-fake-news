""" Does NLP preprocessing only """
import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
import nltk
import unicodedata

from nltk.stem.porter import PorterStemmer
import pickle

stopwords = pickle.load(open('stopwords.pkl', 'rb'))

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


if __name__ == '__main__':
    print(LemmaTokenizer('is this working? I hope so!!!'))
