import json
from multiprocessing.dummy import Pool
from time import sleep
import unicodedata
import httplib2
import requests
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()

cat_pages = '''left
leftcenter
center
right-center
right
pro-science
conspiracy
fake-news
satire'''.split('\n')


class accumulator:
    cat = None
    json_ = []


def cat_links(cat):
    accumulator.cat = cat
    response = requests.get('https://mediabiasfactcheck.com/' + cat).text
    s = BeautifulSoup(response, 'html.parser').find(class_='entry clearfix')
    links_ = BeautifulSoup(str(s), 'html.parser', parse_only=SoupStrainer('a'))
    return links_


def get_links(link):
    sleep(2)
    if link.has_attr('href') and link['href'].startswith('http'):
        page = link['href']

        def check_page():
            if page.startswith('https://mediabiasfactcheck.com/' + accumulator.cat):
                return
            try:
                tag_ = BeautifulSoup(requests.get(page).text, 'html.parser').find(class_='entry-content')

                return tag_
            except requests.exceptions.ConnectionError:
                return

        def get_facts(tag_):
            p_list = list(filter(lambda _: 'Factual' in _.text, tag_.find_all('p')))
            p_list = unicodedata.normalize('NFKD', p_list[0].text.split('\n')[0])
            return p_list.split('strong')[0].split(': ')[1]

        def get_site_url(tag_):
            try:

                return list(
                    filter(lambda _: 'Source:' in _.text or 'Sources:' in _.text, tag_.find_all('p')))[
                        0].text.split()[1]

            except Exception as e:

                print('Warning: URL not found in {}'.format(page))
                return 'URL not found'

        tag_ = check_page()
        if tag_ is None:
            print('Failed to load page {}'.format(page))
            return {'error': 'Failed to load page {}'.format(page)}
        get_site_url(tag_)
        ''''''
        results = {
            'cat1': accumulator.cat,
            'cat2': get_facts(tag_),
            'url': get_site_url(tag_),
            'reference': page
        }
        print(results)
        ''''''
        accumulator.json_.append(results)


def cat_json():
    category_pages = (cat_links(cat) for cat in cat_pages)
    for page in category_pages:
        pool = Pool(10)

        pool.map(get_links, page)
        # [get_links(p) for p in page]
        print(accumulator.json_)

    json.dump(open('mbfc.json', 'w'), accumulator.json_)


cat_json()
'''
TODO:
    Add threadpool
    Make better variables and less hacky error handling    
'''
