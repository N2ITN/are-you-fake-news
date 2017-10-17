''' module-wide mongo handler '''
from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client['newscraper']


def insert(table_name, payload):
    db[table_name].insert_one(payload)
    print(payload)


def kill(table_name):
    db[table_name].drop()


# kill('media_bias')
# pprint(db['media_bias'].find_one({'url': 'http://www.zerohedge.com/'}))

pprint([_ for _ in db['articles'].find(limit=1)])
print(db['media_bias'].count())

# pprint([_ for _ in db['media_bias'].find({'cat1': 'fake-news'})])


def rm_by_attr():
    db['media_bias'].remove({'category': 'fake-news'})


def bias_urls():
    return db['media_bias'].find().distinct('Reference')
