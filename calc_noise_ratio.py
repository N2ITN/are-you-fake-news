r = {
    'propaganda': 0.022126999999999987,
    'conspiracy': 0.017177899999999992,
    'right': 0.021940950000000008,
    'fakenews': 0.022723649999999998,
    'right-center': 0.020066699999999996,
    'pro-science': 0.019704100000000013,
    'left-center': 0.01699795,
    'center': 0.019891250000000003,
    'hate': 0.02190865,
    'extremeright': 0.021901450000000006,
    'left': 0.020689050000000007,
    'mixed': 0.02166835,
    'low': 0.014877200000000004,
    'extremeleft': 0.017511149999999993,
    'high': 0.020773399999999987,
    'veryhigh': 0.018429450000000003,
}

import numpy as np

k, v = zip(*r.items())
# v = 2 * (v - np.max(v)) / -np.ptp(v) - 1
v = 1 * (v - np.max(v)) / -np.ptp(v) - 1
print(dict(zip(k, v)))

s = sum(r.values())
noise_norm = {k: v / s for k, v in r.items()}

# print(noise_norm)
