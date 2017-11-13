from pymongo import MongoClient
from pprint import pprint
import json
client = MongoClient()
db = client['newscraper']


def insert(payload):

    db['ip_logs'].update(payload, {'$set': payload}, upsert=True)


def kill():
    db['ip_logs'].drop()


if __name__ == '__main__':
    pprint([_ for _ in db['ip_logs'].find()])