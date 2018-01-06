import json
from pprint import pprint
from time import ctime

import requests
from pymongo import MongoClient

client = MongoClient()
db = client['newscraper']


def log_ip(ip, name):
    try:
        geo_ip = requests.get('http://freegeoip.net/json/' + ip, timeout=1).text

        geo_ip = json.loads(geo_ip)
        geo_ip.update({'time': ctime(), 'request': name})
        insert(geo_ip)
    except Exception as e:
        print('IP geolocate failure', e)


def insert(payload):

    db['ip_logs'].update(payload, {'$set': payload}, upsert=True)


def kill():
    db['ip_logs'].drop()


def get_coords():
    return db['ip_logs'].aggregate([{
        "$group": {
            "_id": {
                "latitude": "$latitude",
                "longitude": "$longitude"
            }
        }
    }])


if __name__ == '__main__':
    import sys
    try:
        ip = sys.argv[1]
        name = sys.argv[2]
        log_ip(ip, name)
    except IndexError:

        pprint([_ for _ in db['ip_logs'].find()])
