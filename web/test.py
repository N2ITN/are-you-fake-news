# from pymongo import MongoClient

# client = MongoClient(connect=False)
# db = client['newscraper']

# from time import time

# def check_age(url):
#     """ check if website has been spidered within last day """
#     res = list(db['cache'].find({'url': url}))

#     if res:
#         access = next(db['cache'].find())['last_access']
#         day_old = time() - access > 3600 * 24
#     else:
#         day_old = True

#     db['cache'].delete_one({'url': url})
#     db['cache'].insert({'url': url, 'last_access': time()})

#     return day_old

# if __name__ == '__main__':
#     print(check_age('sdf'))
#     print(db['cache'].drop())

from dataclasses import dataclass
