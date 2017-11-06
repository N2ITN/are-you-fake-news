import numpy as np
import joblib
from helpers import addDict

import cosine_dist


class VectorFit:
    ''' Transform input text to fit the training tf-idf vector '''

    def __init__(self):
        self.vectorized = joblib.load('./lsa_corpus.pkl')
        print(vars(self.vectorized).keys())
        self.vocab = self.vectorized.vectorizer.vocabulary_
        self.bacov = {v: k for k, v in self.vocab.items()}

    def get_randomize(self):
        text_len = np.random.randint(50000)
        value_pool = list(set(self.vocab.values()))
        text = np.random.choice(value_pool, text_len)
        text = (self.bacov[_] for _ in text)
        return ' '.join(list(text))


# a = ave_dict(zip(['a', 'b', 'c'], [1, 2, 3]))
# b = ave_dict(zip(['a', 'b', 'c'], [7, 8, 8]))

# a += b
# print(a)
# exit()


def average_noise():

    means = addDict(
        zip([
            'fakenews', 'left', 'high', 'hate', 'mixed', 'low', 'propaganda', 'conspiracy', 'center',
            'unreliable', 'left-center', 'extremeright', 'veryhigh', 'right-center', 'pro-science',
            'bias', 'right', 'corpus'
        ], (0. for _ in range(17))))

    def make_noise(means):
        indices = VectorFit().get_randomize()
        distances = dict(cosine_dist.orchestrate(indices))
        means += distances
        print(means)

        return means

    n_runs = 200
    for i in range(n_runs):
        print('\n', i, '\n')
        means = make_noise(means)
    means = means / (n_runs)

    json.dump(means, open('noise_{}.json'.format(str(n_runs)), 'w'), sort_keys=True)
    return means


import json

print(average_noise())