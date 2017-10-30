import matplotlib.pyplot as plt
from helpers import timeit
import numpy as np
import seaborn as sns


@timeit
def plot(json_results, url, name_clean):
    results_ = {k: v for k, v in json_results[0].items()}
    y, x = list(zip(*sorted(results_.items(), key=lambda kv: kv[1], reverse=True)))

    # x = x / np.sum(x)
    sns.set()

    def label_cleaner():
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

    y = list(label_cleaner())

    y_pos = np.arange(len(y))
    plt.figure(figsize=(8, 8))
    sns.barplot(y=y_pos, x=x, palette='viridis_r', orient='h')
    plt.yticks(y_pos, y)
    plt.ylabel('Usage')
    plt.title(url.replace('https://', '').replace('http://', ''))

    plt.savefig('./static/{}.png'.format(name_clean), format='png', bbox_inches='tight', dpi=200)
