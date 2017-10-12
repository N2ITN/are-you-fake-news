from pymongo import MongoClient
from pprint import pprint
client = MongoClient()
db = client['newscraper']

import json
article = json.load(open('./scraped/nytimes-com.json'))
db['articles'].insert_one(article)
# pprint(db['articles'].find_one())
pprint(db['articles'].find_one({'Meta': 'Flags'}))
