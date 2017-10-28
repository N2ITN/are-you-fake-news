from cosine_dist import *


def lambda_handler(url, context=None):
    result = orchestrate(url)

    return result


print(lambda_handler(open('../lambdatest.txt').read()))
