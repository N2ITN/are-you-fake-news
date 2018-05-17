import json
from pprint import pprint
from time import ctime

import requests
from pymongo import MongoClient
import hashlib

CLIENT = MongoClient()
DB = CLIENT['newscraper']


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
        print('IP geolocate failure {!r}'.format(e))


def insert(payload):

    DB['ip_logs'].update(payload, {'$set': payload}, upsert=True)


def kill():
    DB['ip_logs'].drop()


def get_coords():
    # pylint: disable=C4001
    # keep mongo queries copy/pastable to mongo
    return DB['ip_logs'].aggregate([{
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
        IP = sys.argv[1]
        NAME = sys.argv[2]
        log_ip(IP, NAME)
    except IndexError:

        pprint([_ for _ in DB['ip_logs'].find()])
