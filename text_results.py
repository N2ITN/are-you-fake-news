import sys
import requests
from pprint import pprint
import json
nlp_api = 'https://lbs45qdjea.execute-api.us-west-2.amazonaws.com/prod/newscraper-dev'

try:
    print(sys.argv)
    text_ = sys.argv[1]
    r = json.loads(requests.put(nlp_api, data=text_).text)
    for kv in sorted(r.items(), key=lambda kv: kv[0], reverse=True):
        print(kv)
except Exception as e:
    print(e)
`