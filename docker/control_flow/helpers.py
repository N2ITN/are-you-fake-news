"""
This module contains some auxilliary functions

The most important include: 
    * lemmaTokenizer: performs NLP preprocessing
    * AddDict: allows the values of two dictionaries to be added by matching keys
    * timeit: prints function exectution time to stdout
"""
import json
import time
import unicodedata
from functools import wraps


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
