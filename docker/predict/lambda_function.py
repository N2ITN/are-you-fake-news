from cnn_predict import orchestrate
import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=['POST'])
def lambda_handler():
    data = request.data.decode('utf-8')

    result = orchestrate(json.loads(data))
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=5000)
