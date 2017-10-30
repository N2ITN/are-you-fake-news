

web.helpers import LemmaTokenizer
import mongo_driver


def lemma_wrapper(dict_):

    dict_['article'] = LemmaTokenizer(dict_['article'])
    return dict_


def flags_articles_gen():
    for i, _ in enumerate(mongo_driver.get_all('articles_by_flag')):

        yield _


if __name__ == '__main__':
    mongo_driver.kill('articles_cleaned')
    mongo_driver.drop_articles()
    list(
        map(lambda _: mongo_driver.insert('articles_cleaned', _), (LemmaTokenizer(doc)
                                                                   for doc in flags_articles_gen())))
