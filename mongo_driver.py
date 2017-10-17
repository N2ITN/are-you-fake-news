''' module-wide mongo handler '''
from pymongo import MongoClient
from pprint import pprint
import json
client = MongoClient()
db = client['newscraper']


def insert(table_name, payload):
    db[table_name].insert_one(payload)
    print(payload)


def get_url(table_name):
    return db[table_name].find().distinct('url')


def check_for_dups(table_name):
    unique = len(db[table_name].find().distinct('url'))
    ct = count(table_name)
    return unique == ct


def kill(table_name):
    db[table_name].drop()
    print('deleted table:', table_name)


def rm_by_attr():
    db['media_bias'].remove({'category': 'fake-news'})


def bias_urls():
    return db['media_bias'].find().distinct('Reference')


def count(table_name):
    return db[table_name].count()


def get_all(table_name):
    return (_ for _ in db[table_name].find())


def get_one(table_name):
    pprint([_ for _ in db[table_name].find(limit=1)])


if __name__ == '__main__':

    # kill('media_bias')

    # pprint(db['media_bias'].update_one({
    #     'url': 'http://www.zerohedge.com/'
    # }, {"$set": {
    #     "Category": list()
    # }}))
    # pprint(db['media_bias'].find_one({'url': 'http://www.zerohedge.com/'}))

    # pprint([_ for _ in db['articles'].find(limit=1)])
    # print(db['media_bias'].count())
    print(check_for_dups('opensources'))
    get_one('opensources')
    # count('opensources')
    # pprint((_ for _ in db['media_bias'].find()))