from webserver_get import GetSite
import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=['POST'])
def lambda_handler():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    result = GetSite(url=data['name']).run()
    
    print(type(result))

    return json.dumps(result)

'''
TODO

what this api should return: 
    scores, n_articles, name_clean

'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=5000)
