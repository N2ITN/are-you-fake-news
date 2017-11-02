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
                xy[key] -= xy[key] * noise_factor[key]

        return xy

    sns.set(style='whitegrid', font='Tahoma', font_scale=1.7)

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
        'pro-science': 0.061887029732885866,
        'center': 0.06247483418041247,
        'veryhigh': 0.05788358362527255,
        'mixed': 0.06805638525548371,
        'extremeright': 0.06878851037821127,
        'right': 0.06891257276494546,
        'high': 0.06524550847047719,
        'propaganda': 0.06949692231056298,
        'right-center': 0.06302589103490643,
        'left-center': 0.053387499913627456,
        'extremeleft': 0.054999368695196595,
        'hate': 0.06881112428161597,
        'conspiracy': 0.05395269045774935,
        'left': 0.06498058031045123,
        'fakenews': 0.07137089251423262,
        'low': 0.046726606073968835
    }
    s = sum(noise_factor.values())
    noise_factor = {k: v / s for k, v in noise_factor.items()}
    default_cp = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
    policic_colors = ["#9c3229", "#C8493A", "#D6837F", "#DCDDDD", "#98B5C6", "#6398C9", "#3F76BB"]
    veracity_colors = ["#444784", "#2F7589", "#29A181", "#7CCB58"]
    charachter_colors = ["#444784", "#7CCB58", "#3976C5", "#02B97C", "#C8493A"]

    def make_fig(x, y, cat, colors='coolwarm_r'):
        color_p = default_cp
        if cat == "Political":
            color_p = policic_colors
        elif cat == "Accuracy":
            color_p = veracity_colors
        elif cat == "Character":
            color_p = charachter_colors

        y = list(label_cleaner(y))

        plt.figure(figsize=(8, 8))
        y_pos = np.arange(len(y))
        # x = np.square(np.asarray(x))
        x = np.asarray(x)
        print(dict(zip(y, x.round(4).astype(str))))
        g = sns.barplot(y=y_pos, x=x, palette=(sns.color_palette(color_p)), orient='h', saturation=.9)
        plt.yticks(y_pos, y)
        plt.title('{} - {}'.format(url, cat))
        plt.xlabel('Text similarity')
        plt.xlim(0, .4)
        # frame1 = plt.gca()
        # frame1.axes.xaxis.set_ticklabels([])
        plt.savefig(
            './static/{}.png'.format(name_clean + '_' + cat), format='png', bbox_inches='tight', dpi=100)

        plt.clf()

    get_spectrum(
        ['extremeright', 'right', 'right-center', 'center', 'left-center', 'left',
         'extremeleft'], 'Political', 'policic_colors')

    get_spectrum(['veryhigh', 'high', 'mixed', 'low', 'unreliable'], 'Accuracy', 'veracity_colors')
    plt.close('all')

    get_spectrum(['conspiracy', 'fakenews', 'propaganda', 'pro-science', 'hate'], 'Character',
                 'charachter_colors')


if __name__ == '__main__':

    j = {
        "center": 0.3,
        "conspiracy": 0.229,
        "extremeleft": 0.285,
        "extremeright": 0.355,
        "fakenews": 0.379,
        "hate": 0.307,
        "high": 0.315,
        "left": 0.352,
        "left-center": 0.256,
        "low": 0.192,
        "mixed": 0.306,
        "pro-science": 0.242,
        "propaganda": 0.36,
        "right": 0.34,
        "right-center": 0.299,
        "veryhigh": 0.231
    }
    plot(
        ' Test wired',
        'cnncom',)
