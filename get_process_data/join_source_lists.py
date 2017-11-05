import json
import mongo_driver
from pprint import pprint
from helpers import addDict


def transform_open_format(x):
    ''' Original format:
        (u'NutritionalAnarchy.com',
        {u'2nd type': u'',
        u'3rd type': u'',
        u'Source Notes (things to know?)': u'',
        u'type': u'unreliable'})
    '''

    urls = mongo_driver.get_url('opensources')
    if x[0] in urls:
        return

    template = {
        'Category': 'conspiracy',
        'Reference': 'http://mediabiasfactcheck.com/zero-hedge/',
        'Truthiness': 'MIXED',
        'url': 'http://www.zerohedge.com/'
    }

    out_dict = dict().fromkeys(template)
    out_dict['url'] = x[0]
    out_dict['Category'] = ', '.join(
        list(set([x[1][_] for _ in x[1].keys() if 'type' in _ and x[1][_]])))
    out_dict['Reference'] = 'http://www.opensources.co'

    mongo_driver.insert('opensources', out_dict)


def load_opensources():
    mongo_driver.kill('opensources')
    opensources = json.load(
        open('./opensources/sources/sources.json'))
    list(map(transform_open_format, opensources.items()))
    assert mongo_driver.check_for_dups('opensources')


def get_clean_urls(table_name):
    raw_data = list(mongo_driver.get_all(table_name))
    urls = list(filter(lambda item: 'url' in item, raw_data))

    def clean_link(data):

        link = data['url'].lower().replace('http://', '').replace('https://', '').replace(
            'www.', '').replace((' '), '')
        if link.endswith('/'):
            return link[:-1], data
        else:
            return link, data

    return dict(list(map(lambda item: clean_link(item), urls)))


def merge(url):
    os_ = addDict(correct(url, 'os'))
    mb_ = addDict(correct(url, 'mb'))
    [os_.pop(_) for _ in ('_id', 'url')]
    [mb_.pop(_) for _ in ('_id', 'url')]

    merged_ = mb_ + os_
    merged_['url'] = url
    mongo_driver.insert('all_sources', merged_)


def correct(url, source):
    if source == 'os':
        data_ = os_data[url]
    elif source == 'mb':
        data_ = mb_data[url]

    def string_clean(s):
        sanitized = list(
            map(lambda _: _.strip(), s.lower().replace('.', ', ').replace('*', ', ').strip().split(
                ', ')))

        replacements = [('hate group', 'hate'), ('fake-news', 'fake'), ('fake news', 'fake'), (
            'high (no pun intended)', 'high'), ('imposter website', 'imposter site'),('imposter site','fake') ,(
                'leftcenter', 'left-center'), ('some fake news', 'fake'), ('satirical', 'satire'),
                        ('unrealiable', 'unreliable'), ('neo-fascist', 'extreme right'),
                        ('some fake', 'fake'), ('conspiracy theory', 'conspiracy'), (
                            'mostly fake', 'fake'), ('islamophobia', 'hate'), ('anti-islam', 'hate'), (
                                'pro-syrian state', 'state'), ('mixed (depends on source)', 'mixed'),
                        ('junksci', 'pseudoscience'), ('pseudoscience', 'conspiracy'), (
                            'fake', 'fake news'), ('anti-lgbt', 'hate'), ('white nationalism', 'hate'), (
                                'sensationalism', 'mixed'), ('nationalism', 'state'),('poor sourcing','low'),('extreme bias','low'),('right libertarian','right')]

        def replacer():
            for item in sanitized:
                for k, v in replacements:
                    item = item.replace(k, v)
                if item:
                    yield item

        return list(replacer())

    if 'Truthiness' in data_ and data_['Truthiness'] is not None:
        data_['Category'] += ', ' + data_['Truthiness']
        data_.pop('Truthiness')
    data_['Category'] = string_clean(data_['Category'])

    data_['url'] = url
    return data_


if __name__ == '__main__':
    mongo_driver.kill('all_sources')

    os_data = get_clean_urls('opensources')
    mb_data = get_clean_urls('media_bias')

    os_urls = set(os_data.keys())
    mb_urls = set(mb_data.keys())

    shared_urls = os_urls & mb_urls

    stats = {
        'individual': [len(os_urls), len(mb_urls)],
        'total': [len(os_urls) + len(mb_urls)],
        'not shared': len(os_urls ^ mb_urls),
        'shared': len(shared_urls),
        'total': len(os_urls | mb_urls),
        'opensource only': len(os_urls - mb_urls),
        'mediabias only': len(mb_urls - os_urls)
    }
    print(stats)

    [mongo_driver.insert('all_sources', correct(url, 'os')) for url in os_urls - mb_urls]
    [mongo_driver.insert('all_sources', correct(url, 'mb')) for url in mb_urls - os_urls]
    list(map(merge, shared_urls))

    x = sorted([_ for _ in mongo_driver.db['all_sources'].find().distinct('Category')])
    pprint(x)
    print(len(x))
