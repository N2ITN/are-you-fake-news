import json
import logging
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, jsonify, request
from waitress import serve

from plotter import PlotResults

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

        results = payload["data"]

        app.logger.debug(results)

        plots = PlotResults(results)

        plots.plot()

        return jsonify({"success": "Plots produced"}), 200

    except KeyError:

        return jsonify({"error": "ERROR: No scores attribute in POST payload"}), 400

    except:

        app.logger.exception("Unhandled exception")

        return jsonify({"error": "Unhandled exception"}), 500


    return jsonify({"error": """ERROR: No text value in payload"""}), 400


if __name__ == "__main__":
    serve(app, listen="*:5000")
