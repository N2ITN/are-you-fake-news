import httplib2
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

import requests


def cat_links(cat):
    response = requests.get('https://mediabiasfactcheck.com/' + cat).text

    s = BeautifulSoup(response, 'html.parser').find(class_='entry clearfix')

    for link in BeautifulSoup(str(s), 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href') and link['href'].startswith('http'):
            page = link['href']
            if page.startswith('https://mediabiasfactcheck.com/' + cat):
                continue

            x = BeautifulSoup(requests.get(page).text, 'html.parser').find(class_='entry-content')

            z = list(filter(lambda _: 'Factual' in _.text, x.find_all('p')))

            fact_line = z[0].text.split('strong')[0].split('\xa0')
            try:
                fact_line = fact_line[1]
            except IndexError:
                fact_line = fact_line[0].split(':')[1]
                factual_reporting = fact_line
            else:
                factual_reporting = fact_line

            yield {'site': page, 'cat1': cat, 'cat2': factual_reporting}


import json


def cat_json():
    gen_list = list(linker())
    json_ = []
    for cat_gen in gen_list:
        json_ += list(cat_gen)

    json.dump(open('mbfc.json', 'w'), json_)


def linker():
    for cat in cat_pages:
        yield cat_links(cat)


cat_json()
'''
TODO:
    Add threadpool
    Make better variables and less hacky error handling
    
'''