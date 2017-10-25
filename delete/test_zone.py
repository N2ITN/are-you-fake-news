def t():
    for i, x in enumerate(range(12, 22)):
        yield i, x


def y(a, b):
    print(a, b)


i_t = t()


def x(args):
    for i in args:
        print(i)


x(zip(*i_t))