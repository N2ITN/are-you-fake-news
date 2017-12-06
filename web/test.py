nlp_api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/prod/dnn_nlp'
import requests, json
res = requests.put(nlp_api, data={' '}).json()

for r in sorted(res.items(), key=lambda kv: kv[1], reverse=True):
    print(r)
