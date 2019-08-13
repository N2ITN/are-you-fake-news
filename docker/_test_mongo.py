from pymongo import MongoClient

db = MongoClient()['AYFN']


def insert(table_name, payload):
    db[table_name].update(payload, {'$set': payload}, upsert=True)


insert('test', {"whatever": "test"})

print(list(db['test'].find()))