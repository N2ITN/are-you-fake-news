"""
This module contains some auxilliary functions

The most important include: 
    * lemmaTokenizer: performs NLP preprocessing
    * AddDict: allows the values of two dictionaries to be added by matching keys
    * timeit: prints function exectution time to stdout



TODO: This module is duplicated in 3 different forms: 
        A version exists in ./web, an identical version in ./get_process_data
        This was to avoid local imports, but is dangerous
        A third version exists as helpers_nlp and is stripped down for AWS Lambda
    Ideally there should only be one version.
"""
import json
import time
import unicodedata
from functools import wraps
from pprint import pprint
import imp
import sys

import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.stop_words import \
    ENGLISH_STOP_WORDS as stopwords


def j_writer(f, silent=False):

    def wrapper(*args, **kwargs):

        res = f(*args)
        if not res: return
        _j, name = res

        j = json.dumps(_j, indent=4, sort_keys=True, ensure_ascii=False, *kwargs)
        if not name.endswith('.json'):
            name += '.json'
        with open(name, 'w') as obj:
            obj.write(j)
        return 'JSON writer: saved {} to file'.format(name)

    return wrapper


class addDict(dict):
    ''' provides an 'add' method to dictionaries '''

    def __iadd__(self, b):
        return self + b

    def __add__(self, b):
        ''' magic method override'''
        # Only works if b is a dictionary
        if isinstance(b, dict):
            a_key = set(self.keys())
            b_key = set(b.keys())
            res = {}
            # Operate on matching keys:
            for k in a_key & b_key:
                # If values not the same type, return in tuple
                if type(self[k]) != type(b[k]):
                    res[k] = (self[k], b[k])
                # If None, move on
                elif not self[k]:
                    continue
                # If int, add itns
                elif isinstance(self[k], (int, float)):
                    res[k] = self[k] + b[k]
                # If tuple or list, a
                elif isinstance(self[k], (tuple, list)):
                    res[k] = list(set(self[k] + b[k]))
                # If anything else ( strings, dicts, objects) just concat in lists
                else:
                    res[k] = [self[k] + b[k]]

            # Otherwise, keep distinct items
            for k in a_key - b_key:
                res[k] = self[k]
            for k in b_key - a_key:
                res[k] = b[k]
            return addDict(res)

    def argmax(self, filt=None, n=1):
        if filt:
            self = {k: v for k, v in self.items() if k in filt}
        max_ = sorted(self.items(), key=lambda kv: kv[1], reverse=True)[:n]

        return max_

    def reverse(self):
        return {v: k for k, v in self.items()}


def test_addDict():
    a = addDict({'a': 1, 'b': 2, 'c': 4})
    print(a.argmax(n=2))
    a = addDict({'a': 9, 'b': 2, 'c': 4})
    print(a.argmax(n=2, filt=('b', 'c')))
    a = addDict({'a': 1, 'b': 2, 'c': 3})
    print(a.argmax(['b', 'c']))
    a = addDict({'a': .3434})

    a += addDict({'a': .6563})
    a += addDict({'a': .6563})
    print(a)
    print(a.reverse())
    print(dict(a))


def timeit(func):
    """ Returns time of delta for function in seconds """

    @wraps(func)
    def timed(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()
        delta = round((te - ts), 1)
        if delta > 1:
            t = ' '.join([str(delta), 's'])
        else:
            t = ' '.join([str(round((te - ts) * 1000, 1)), 'ms'])

        print('Function', func.__name__, 'time:', t)
        return result

    return timed


class new_print:

    def __new__(self, args=None):
        if not args:
            print()
        elif isinstance(args, (list, tuple, set, dict)):

            pprint(args)

        else:
            print(args)


stopwords_ = set(stopwords)
[stopwords_.add(_) for _ in ['the', 'this', 'use', 'just', 'of', 'there', 'these', 'like']]


def fix_unicode(u):
    u = unicodedata.normalize('NFKD', u).encode('ascii', 'ignore')
    return str(u, 'utf-8')


def LemmaTokenizer(text_):
    stemmer = PorterStemmer().stem

    # text_ = nlp_wrapper(text_)

    def process():
        tokens = fix_unicode(text_).split(' ')
        for token in tokens:
            token = token.lower()
            if len(token) > 2 and all([c.isalpha() for c in token]) and not token in stopwords_:
                yield stemmer(token.lower())

    return list(process())


# from newspaper import nlp

# def nlp_wrapper(text):
#     """Keyword extraction wrapper
#     """
#     nlp.load_stopwords('en')
#     return ' '.join(list(nlp.keywords(text).keys()))