# coding: utf-8
"""
"""

import logging
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

np.set_printoptions(precision=3)

logger = logging.getLogger(__name__)

class PlotResults:

    def __init__(self, results, path, logger=logger):
        """Plot results of are-you-fake-news query

        Plots scores returned from model in format::

            results = {'scores': {
                 'fake news': 0.026105,
                 'center': 0.017353,
                 'left': 0.069697,
                 'extreme left': 0.001491,
                 'mixed': 0.293917,
                 'low': 0.006344,
                 'right-center': 0.062835,
                 'propaganda': 0.011925,
                 'conspiracy': 0.036079,
                 'hate': 0.002538,
                 'high': 0.29368,
                 'satire': 0.023235,
                 'extreme right': 0.013205,
                 'very high': 0.002354,
                 'pro-science': 0.001237,
                 'left-center': 0.101551,
                 'right': 0.151564
                },
            'url': 'rad.com',
            'name_clean': 'rad.com'
            }


        Args:
            results (dict): dict containing scores, url, and name_clean elements.
            path (str): Path where plots are to be saved to.
            logger: Logger to be used in logging, for example app.logger which
                to hook into flask app logger. Passing None, will instantiate
                its own logger using logging.getLogger.

        """

        # Separate the entities in results for easier access.

        self.scores = results.get("scores")
        self.url = results.get("url")
        self.plot_name_clean = results.get("name_clean")

        self.path = path
        self.logger = logger

        # Define labels and color palettes for the various plot types here so
        # that they can easily be accessed by the barplot function.

        self.params = {
            "default": {
                "palette": ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c",
                            "#34495e", "#2ecc71"]
            },
            "Political": {
                "palette": ['#FF0000', '#D5002B', '#AA0055', '#800080',
                            '#5500AA', '#2B00D5', '#0000FF'],
                "spec": ['extreme right', 'right', 'right-center', 'center',
                         'left-center', 'left', 'extreme left'],
            },
            "Accuracy": {
                "palette": ['#2B80C5', '#35C52B', '#FFC21A', '#EF5337'],
                "spec": ['very high', 'high', 'mixed', 'low', 'unreliable'],
            },
            "Character": {
                "palette":['#009999', '#33A38F', '#66AD85', '#99B87A',
                           '#CCC270', '#FFCC66'],
                "spec": ['conspiracy', 'fake news', 'propaganda', 'pro-science',
                         'satire', 'hate'],
            }
        }

        self.font = {'family': 'sans-serif', 'weight': 'normal', 'size': 16}
        self.max_val = max([value for key, value in self.scores.items() if key != 'n_words']) + 0.01
        self.key = {
            'center': 'Center',
            'conspiracy': 'Conspiracy',
            'extreme left': 'Extreme Left',
            'extreme right': 'Extreme Right',
            'fake news': 'Fake News',
            'hate': 'Hate',
            'high': 'High Accuracy',
            'left': 'Left',
            'left-center': 'Left Of Center',
            'low': 'Pants On Fire!',
            'mixed': 'Mixed Accuracy',
            'pro-science': 'Pro-Science',
            'propaganda': 'Propaganda',
            'right': 'Right',
            'right-center': 'Right Of Center',
            'satire': 'Satire',
            'very high': 'Very High Accuracy',
        }


    def plot(self):

        self.make_fig(name='Political')

        self.make_fig(name='Accuracy')

        self.make_fig(name='Character')

        self.logger.info('Plotting complete')


    def make_fig(self, name):
        """Make a figure

        Args:
            name (str): Which type of plot is being produced. One of `
                ["Accuracy", "Character", "Political"]`

        Returns:
            None
        """

        spec = self.params[name]["spec"]

        x, y = self._prepare_x_y(spec, self.scores)

        # Sanitize label names using the self.key dict

        y = [self.key.get(label, label) for label in y]

        plot_file_name = "%s_%s.png" % (self.plot_name_clean, name)

        plot_file_name = os.path.join(self.path, plot_file_name)

        palette = self.params[name]["palette"]

        y_pos = np.arange(len(y))
        x = np.asarray(x)

        matplotlib.use('Agg')

        plt.figure(figsize=(9, 9))

        matplotlib.rc('font', **self.font)
        plt.barh(y_pos, x, color=palette, rasterized=False)
        plt.xlim(0, self.max_val)
        plt.yticks(y_pos, y)
        plt.title('%s - %s' % (self.url, name))
        plt.xlabel('Neural network estimation')
        plt.savefig(plot_file_name, format='png', bbox_inches='tight', dpi=150)
        plt.clf()

        self.logger.info("%s plot saved to %s" % (name, plot_file_name))


    def _prepare_x_y(self, spec, scores):
        """Prepare x and y data for plotting

        Takes spectrum and scores, and outputs x, and y.

        Args:
            spec (list): List of spectrum (y axis) labels.
            scores (dict): Dict of scores

        Returns:
            Two lists corresponding to x and y, ready for plotting.
        """

        # Create a dict of spec: index

        spec = dict(zip(spec, range(len(spec))))

        out = filter(lambda kv: kv[0] in spec, scores.items())
        out = sorted(out, key=lambda kv: spec[kv[0]])

        y = [i[0] for i in out]
        x = [i[1] for i in out]

        return x, y
