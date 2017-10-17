import json
import mongo_driver
from pprint import pprint


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
        print(x[0].lower())
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
        open('/home/z/Documents/myRepos/newscraper/opensources/sources/sources.json'))
    list(map(transform_open_format, opensources.items()))
    assert mongo_driver.check_for_dups('opensources')


def merge():
    mbfc_data = list(mongo_driver.get_all('media_bias'))
    opensources_data = list(mongo_driver.get_all('opensources'))
    # print(next(opensources_data))
    print(mbfc_data[1])
    shared_urls = set(map(lambda item: tuple(item.keys()), mbfc_data))
    pprint(shared_urls)


def get_clean_urls(table_name):
    raw_data = list(mongo_driver.get_all(table_name))
    urls = list(filter(lambda item: 'url' in item, raw_data))

    def clean_link(link):
        link = link.replace('http://', '').replace('https://', '').replace('www.', '').replace(
            (' '), '').lower()

        if link.endswith('/'):
            return link[:-1]
        else:
            return link

    return list(map(lambda item: clean_link(item['url']), urls))


if __name__ == '__main__':
    # load_opensources()
    os_urls = set(get_clean_urls('opensources'))
    mb_urls = set(get_clean_urls('media_bias'))
    shared_urls = os_urls & mb_urls
    pprint(shared_urls)
    print('individual', len(os_urls), len(mb_urls))
    print('shared', len(shared_urls))
    print('total', len(os_urls | mb_urls))
    # merge()
    # media_bias = (_ for _ in db['media_bias'].find())