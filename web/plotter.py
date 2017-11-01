import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from helpers import timeit
import numpy as np
import seaborn as sns
import json
import numpy as np
np.set_printoptions(precision=3)


@timeit
def plot(url, name_clean):
    j_name = './static/{}.json'.format(name_clean)
    json_results = json.load(open(j_name))
    results_ = {k: v for k, v in json_results[0].items()}

    def get_spectrum(spec, name, colors):
        spec = dict(zip(spec, range(len(spec))))
        y, x = list(
            zip(*sorted(filter(lambda kv: kv[0] in spec, results_.items()), key=lambda kv: spec[kv[0]])))
        y, x = list(zip(*sorted(denoise(x, y).items(), key=lambda kv: spec[kv[0]])))
        make_fig(x, y, name, colors)

    def denoise(x, y):

        xy = dict(zip(y, x))

        for key in xy:
            if key in noise_factor:
                xy[key] -= noise_factor[key]

        # y, x = zip(*xy.items())
        return xy

        return

    sns.set(style='whitegrid', font_scale=1.7)

    def label_cleaner(y):
        key = {
            'fakenews': 'fake news',
            'extremeright': 'extreme right',
            'extremeleft': 'extreme left',
            'veryhigh': 'very high veracity',
            'low': 'low veracity',
            'pro-science': 'pro science',
            'mixed': 'mixed veracity',
            'high': 'high veracity'
        }
        for label in y:
            for k, v in key.items():
                if label == k:
                    label = v.title()

            yield label.title()

    noise_factor = {
        "bias": 0.13019499999999995,
        "center": 0.113665,
        "conspiracy": 0.10497000000000004,
        "extremeright": 0.10439,
        "fakenews": 0.11656000000000005,
        "hate": 0.13590500000000005,
        "high": 0.14559,
        "left": 0.13008999999999993,
        "left-center": 0.13813,
        "low": 0.11782000000000005,
        "mixed": 0.11934499999999997,
        "pro-science": 0.11907000000000006,
        "propaganda": 0.1091749999999999,
        "right": 0.11631499999999999,
        "right-center": 0.11712500000000002,
        "unreliable": 0.097765,
        "veryhigh": 0.13111
    }

    def make_fig(x, y, cat, colors='coolwarm_r'):

        y = list(label_cleaner(y))

        plt.figure(figsize=(8, 8))
        y_pos = np.arange(len(y))
        # x = np.square(np.asarray(x))
        x = np.asarray(x)
        print(dict(zip(y, x.round(4).astype(str))))
        g = sns.barplot(y=y_pos, x=x, palette=colors, orient='h', saturation=.9)
        plt.yticks(y_pos, y)
        plt.title('{} - {}'.format(url, cat))
        plt.xlabel('Text similarity')
        plt.xlim(0, .5)
        # frame1 = plt.gca()
        # frame1.axes.xaxis.set_ticklabels([])
        plt.savefig(
            './static/{}.png'.format(name_clean + '_' + cat), format='png', bbox_inches='tight', dpi=100)

        plt.clf()

    get_spectrum(
        ['extremeright', 'right', 'right-center', 'center', 'left-center', 'left',
         'extremeleft'], 'Political', 'coolwarm_r')

    get_spectrum(['veryhigh', 'high', 'mixed', 'low', 'unreliable'], 'Accuracy', 'viridis')
    plt.close('all')

    get_spectrum(['conspiracy', 'fakenews', 'propaganda', 'pro-science', 'hate'], 'Character', 'husl')


if __name__ == '__main__':
    plot('bbr', 'naturalnewscom')
