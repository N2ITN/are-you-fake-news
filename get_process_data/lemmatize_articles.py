from helpers import LemmaTokenizer
import mongo_driver
import json


def lemma_wrapper(dict_):

    dict_['article'] = LemmaTokenizer(dict_['text'])
    dict_.pop('text')
    return dict_


def flags_articles_gen():
    for i, _ in enumerate(mongo_driver.get_all('articles')):
        yield _


if __name__ == '__main__':
    mongo_driver.kill('articles_cleaned')
    mongo_driver.drop_articles()

    cleaner_gen = (lemma_wrapper(doc) for doc in flags_articles_gen())
    for i, cleaned_article in enumerate(cleaner_gen):
        mongo_driver.insert('articles_cleaned', cleaned_article)
        if not i % 50:
            print(i)
    json.dump(db['articles_cleaned'].count(), open('n_articles.json', 'w'))