import numpy as np
import joblib

import cosine_dist


class VectorFit:
    ''' Transform input text to fit the training tf-idf vector '''

    def __init__(self):
        self.vectorized = joblib.load('./vectorizer.pkl')
        print(vars(self.vectorized).keys())
        self.vocab = self.vectorized.vectorizer.vocabulary_
        self.bacov = {v: k for k, v in self.vocab.items()}

    def get_randomize(self):
        value_pool = list(set(self.vocab.values()))
        text = np.random.choice(value_pool, 5000)
        text = (self.bacov[_] for _ in text)
        return ' '.join(list(text))


class ave_dict(dict):

    def __iadd__(self, other):
        for k, v in other.items():
            if k in self:
                if self[k] == 0:
                    self[k] = other[k]
                self[k] += other[k]
                self[k] /= 2
            else:
                self[k] = other[k]
        return self


# a = ave_dict(zip(['a', 'b', 'c'], [1, 2, 3]))
# b = ave_dict(zip(['a', 'b', 'c'], [7, 8, 8]))

# a += b
# print(a)
# exit()


def average_noise():

    means = ave_dict(
        zip([
            'fakenews', 'left', 'high', 'hate', 'mixed', 'low', 'propaganda', 'conspiracy', 'center',
            'unreliable', 'left-center', 'extremeright', 'veryhigh', 'right-center', 'pro-science',
            'bias', 'right'
        ], (0 for _ in range(17))))

    def make_noise(means):
        indices = VectorFit().get_randomize()
        distances = dict(cosine_dist.orchestrate(indices))
        means += distances
        print(means)

        return means

    n_runs = 150
    for i in range(n_runs):
        means = make_noise(means)

    json.dump(means, open('noise_{}.json'.format(str(n_runs)), 'w'), sort_keys=True)
    return means


import json

average_noise()