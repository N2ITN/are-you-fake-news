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
        ''' remove denoiseing until new baseline is calculated '''
        y, x = list(zip(*sorted(denoise(x, y).items(), key=lambda kv: spec[kv[0]])))
        make_fig(x, y, name, colors)

    def denoise(x, y):
        xy = dict(zip(y, x))

        for key in xy:
            if key in noise_factor:
                # xy[key] = xy[key] * (noise_factor[key])
                # xy[key] -= (xy[key] * noise_factor[key])

                pass

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
        'left-center': -0.29927100284366454,
        'left': -0.19109156434406593,
        'veryhigh': 0.0329219882637215,
        'conspiracy': -0.14033811660667034,
        'extremeright': 0.015654535890989973,
        'propaganda': -0.06100522708220374,
        'hate': 0.5,
        'satire': 0.2472231125795149,
        'corpus': -0.5,
        'pro-science': 0.06033232243536002,
        'low': 0.12490137580748684,
        'mixed': -0.25225911040978355,
        'right': -0.08607118201094716,
        'center': -0.27269589230238067,
        'fakenews': -0.06030150237519838,
        'right-center': -0.03685154593421647,
        'high': -0.3867568256159899,
        'extremeleft': 0.4101831533441821
    }
    print(noise_factor)

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
        # plt.xlim(0, .5)
        plt.savefig(
            './static/{}.png'.format(name_clean + '_' + cat), format='png', bbox_inches='tight', dpi=100)

        plt.clf()

    get_spectrum(
        ['extremeright', 'right', 'right-center', 'center', 'left-center', 'left',
         'extremeleft'], 'Political', 'policic_colors')

    get_spectrum(['veryhigh', 'high', 'mixed', 'low', 'unreliable'], 'Accuracy', 'veracity_colors')
    plt.close('all')

    get_spectrum(['conspiracy', 'fakenews', 'propaganda', 'pro-science', 'hate', 'satire', 'corpus'],
                 'Character', 'charachter_colors')


if __name__ == '__main__':

    plot(' _test_', 'breitbartcom')
    plot(' _test_', 'msnbccom')
