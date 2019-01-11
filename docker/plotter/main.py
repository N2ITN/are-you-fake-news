import json
import logging
import os

import boto3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, jsonify, request
from waitress import serve

matplotlib.use('Agg')
np.set_printoptions(precision=3)

ENV = os.getenv("ENV")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")

if isinstance(LOGGING_LEVEL, str):
    numeric_level = getattr(logging, LOGGING_LEVEL.upper(), 10)
else:
    numeric_level = 10

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=numeric_level,
)

app = Flask(__name__)


def plot(json_results, url, name_clean):

    results_ = {k: v for k, v in json_results.items()}
    app.logger.debug(results_)

    def get_spectrum(spec, name, colors):
        spec = dict(zip(spec, range(len(spec))))
        y, x = list(
            zip(*sorted(filter(lambda kv: kv[0] in spec, results_.items()), key=lambda kv: spec[kv[0]])))
        ''' remove denoiseing until new baseline is calculated '''
        make_fig(x, y, name, colors)

    def label_cleaner(y):
        key = {
            'fakenews': 'fake news',
            'pro-science': 'pro-science',
            'extremeright': 'extreme right',
            'extremeleft': 'extreme left',
            'right-center': 'right of center',
            'left-center': 'left of center',
            'very high': 'very high accuracy',
            'high': 'high accuracy',
            'mixed': 'mixed accuracy',
            'low': 'pants on fire!',
        }

        for label in y:
            for k, v in key.items():
                if label == k:
                    label = v.title()

            yield label.title()

    default_cp = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
    pol_colors = ['#FF0000', '#D5002B', '#AA0055', '#800080', '#5500AA', '#2B00D5', '#0000FF']
    acc_colors = ['#2B80C5', '#35C52B', '#FFC21A', '#EF5337']

    char_colors = ['#009999', '#33A38F', '#66AD85', '#99B87A', '#CCC270', '#FFCC66']

    max_val = max([v for k, v in results_.items() if k != 'n_words']) + 0.01

    app.logger.debug(max_val)

    def make_fig(x, y, cat, colors='coolwarm_r'):

        color_p = default_cp

        if cat == "Political":
            color_p = pol_colors
        elif cat == "Accuracy":
            color_p = acc_colors
        elif cat == "Character":
            color_p = char_colors

        y = list(label_cleaner(y))

        plt.figure(figsize=(9, 9))
        y_pos = np.arange(len(y))
        x = np.asarray(x)

        font = {'family': 'sans-serif', 'weight': 'normal', 'size': 16}

        matplotlib.rc('font', **font)
        plt.barh(y_pos, x, color=color_p, rasterized=False)
        plt.xlim(0, max_val)
        plt.yticks(y_pos, y)
        plt.title('{} - {}'.format(url, cat))
        plt.xlabel('Neural network estimation')
        fname = '{}.png'.format(name_clean + '_' + cat)
        from io import BytesIO
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        plt.clf()

        img_buffer.seek(0)  # rewind to beginning of file
        to_s3(img_buffer, fname)

    def to_s3(png, fname):

        s3 = boto3.resource('s3')

        bucket = s3.Bucket('fakenewsimg')
        bucket.upload_fileobj(png, fname)

    get_spectrum(
        ['extreme right', 'right', 'right-center', 'center', 'left-center', 'left', 'extreme left'],
        'Political', 'policic_colors')

    get_spectrum(['very high', 'high', 'mixed', 'low', 'unreliable'], 'Accuracy', 'veracity_colors')
    plt.close('all')

    get_spectrum(['conspiracy', 'fake news', 'propaganda', 'pro-science', 'satire', 'hate'], 'Character',
                 'charachter_colors')

    app.logger.info('Plotting finished')

@app.route("/", methods=["POST"])
def index():
    """Expecting a payload in format:

     payload = json.dumps({
         'body': [{
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
         }, 'rad.com', 'rad.com']
     })
    """

    payload = request.get_json()

    try:

        scores = payload["scores"]

        app.logger.debug(scores)

        #plot(scores)

        return jsonify({"success": "Plot saved to s3"}), 200

    except KeyError:

        return jsonify({"error": "ERROR: No scores attribute in POST payload"}), 400

    except:

        return jsonify({"error": "Unhandled exception"}), 500


    return jsonify({"error": """ERROR: No text value in payload"""}), 400


if __name__ == "__main__":
    serve(app, listen="*:5000")
