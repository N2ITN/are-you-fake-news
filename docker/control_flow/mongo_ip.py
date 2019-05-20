import json
from pprint import pprint
from time import ctime

import requests
from pymongo import MongoClient
import hashlib
import os
# client = MongoClient()
try:
    client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017, connect=False)
except KeyError:
    print('docker-compose mongo not found, trying local connection')

    client = MongoClient(connect=False)
db = client['newscraper']


def log_ip(ip, name):
    try:
        geo_ip = requests.get('http://freegeoip.net/json/' + ip, timeout=1).text

        geo_ip = json.loads(geo_ip)
        geo_ip.update({'time': ctime(), 'request': name})
        geo_ip['ip'] = hashlib.md5(bytes(geo_ip['ip'].encode('utf-8'))).hexdigest()[7:12]
        insert(geo_ip)
        print()
        print(geo_ip)
        print()
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
