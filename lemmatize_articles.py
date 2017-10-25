import mongo_driver
import spacy
nlp = spacy.load('en_core_web_sm')


def LemmaTokenizer(dict_):

    def process():
        tokens = nlp(dict_['article'])
        for token in tokens:
            if len(token) > 2 and token.is_alpha and not (
                    token.is_stop):  #and  and token.lemma_ != '-PRON-':
                yield token.lemma_ or token

    dict_['article'] = list(process())
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
