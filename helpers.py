import json


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

    # def __iter__(self):
    #     for k, v in self.items():
    #         yield k, v

    def reverse(self):
        return {v: k for k, v in self.items()}


def test_addDict():

    a = addDict({'a': .3434})

    a += addDict({'a': .6563})
    a += addDict({'a': .6563})
    print(a)
    print(a.reverse())
    print(dict(a))


test_addDict()

import time
from functools import wraps


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


from pprint import pprint


class new_print:

    def __new__(self, args):
        if isinstance(args, (list, tuple, set, dict)):

            pprint(args)

        else:
            print(args)
