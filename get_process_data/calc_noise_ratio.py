import json

import numpy as np


def noise_norm():
    r = json.load(open('./noise_200.json'))
    k, v = zip(*r.items())
    v = 1 * (v - np.max(v)) / -np.ptp(v) - 1
    print(dict(zip(k, v)))

    s = sum(r.values())
    return {k: v / s for k, v in r.items()}


print(noise_norm())
