import json

import numpy as np

from sklearn.preprocessing import MinMaxScaler

sc = MinMaxScaler(feature_range=(-1, 1))


def noise_norm():
    r = json.load(open('./noise_200.json'))
    k, v = zip(*r.items())
    v = sc.fit_transform(np.asarray(v).reshape(-1, 1))
    v = [_.tolist()[0] for _ in v]
    return dict(zip(k, v))
    # s = sum(r.values())
    # return {k: v / s for k, v in r.items()}


print(noise_norm())
