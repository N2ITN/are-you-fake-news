''' Uses a generator pipeline to get one article at a time '''

import mongo_driver


class curr_flag:
    val = None


def unique_flags():
    flags = mongo_driver.db['articles'].aggregate([{
        '$unwind': "$flags"
    }, {
        '$group': {
            '_id': {
                '$toLower': '$flags'
            }
        }
    }])
    yield from (list(_.values())[0] for _ in flags)


def articles_by_flag(flags):
    for flag in flags:
        curr_flag.val = flag

        yield mongo_driver.db['articles'].find({'flags': {'$exists': True, '$in': [flag]}})


def article_feeder():
    flag_corpus = articles_by_flag(unique_flags())

    def feed():
        for flag in flag_corpus:
            yield from flag

    yield from feed()


def main():
    for i, article in enumerate(article_feeder()):

        mongo_driver.insert(
            'articles_by_flag',
            {
                'article': article['text'].replace('\n', ' '),
                # {'article': article['keywords'],
                'flag': curr_flag.val
            })


if __name__ == '__main__':
    mongo_driver.kill('articles_by_flag')
    main()

    # mongo_driver.print_n('articles_by_flag', 10)
