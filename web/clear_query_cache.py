from pymongo import MongoClient

import os
client = MongoClient()
db = client['newscraper']

print('dropping queries')
db['queries'].drop()

print('removing newspaper cache')
os.system('rm -rf ~/.newspaper_scraper')
