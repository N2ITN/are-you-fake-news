''' module-wide mongo handler '''
from pymongo import MongoClient
from pprint import pprint
import json
client = MongoClient()
db = client['newscraper']


def tables():
    print(db.collection_names())


tables()


def insert(table_name, payload):
    db[table_name].update(payload, {'$set': payload}, upsert=True)


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


def update(table_name, old_, new_):
    return db[table_name].update_one(old_, {'$set': new_})


def print_n(table_name, limit=1):
    pprint([_ for _ in db[table_name].find(limit=limit)])


if __name__ == '__main__':
    pass
    print(count('articles'))
    # kill('articles')
    # print_n('all_sources', 150)
    # print(count('all_sources'))
    # get_one('opensources')
    # pprint(db['media_bias'].update_one({
    #     'url': 'http://www.zerohedge.com/'
    # }, {"$set": {
    #     "Category": list()
    # }}))
    # pprint(db['media_bias'].find_one({'url': 'http://www.zerohedge.com/'}))
    # kill('cool_data')
    # insert('cool_data', {'z': 'rad', 'data_science': 'fun', 'warp_drive': 'optimal'})
    # insert('cool_data', {'z': 'sweet', 'data_science': 'great', 'warp_drive': 'optimal'})
    # update('cool_data', {'z': 'rad'}, {'z': 'radical'})
    # pprint(list(get_all('cool_data')))
    # pprint([_ for _ in db['articles'].find(limit=1)])
    # print(db['media_bias'].count())
    # print(check_for_dups('opensources'))
    # get_one('opensources')
    # count('opensources')
    # pprint((_ for _ in db['media_bias'].find()))

    # x = [_ for _ in db['media_bias'].find().distinct('Truthiness')]
    # x = sorted([_ for _ in db['all_sources'].find().distinct('Category')])

    # x = [_ for _ in db['media_bias'].find()]
    # pprint(list(x))
    # print(len(x))