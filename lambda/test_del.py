from helpers import addDict

x = (addDict() + addDict({'a': 1, 'b': 7, 'c': 6}) + addDict({'a': 1, 'b': 7, 'c': 6}))

x += addDict({'a': 1, 'b': 7, 'c': 6})
print(x)


class foo:

    def __new__(self, other):
        return foo.add(3, other)

    def add(mything, other):
        return mything + other


print(foo(3))