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


def blacklist():
    """ Delete my own IP from records to not bias maps """
    my_ips = ['73.239.218.218', '71.212.99.244', '75.172.58.4', '97.113.121.210', '73.239.218.218']
    for ip in my_ips:
        db['ip_logs'].delete_many({'ip': ip})


if __name__ == '__main__':
    import sys
    try:
        ip = sys.argv[1]
        name = sys.argv[2]
        log_ip(ip, name)
    except IndexError:

        pprint([_ for _ in db['ip_logs'].find()])
