class AddDict(dict):
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
                # If int, add ints
                elif isinstance(self[k], (int, float)):
                    res[k] = self[k] + b[k]
                # If tuple or list, make a set
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
            return AddDict(res)


if __name__ == '__main__':
    d1 = AddDict({'one': [1], 'two': [2]})
    d2 = AddDict({'three': [3], 'two': [2]})
    print(d1 + d2)
