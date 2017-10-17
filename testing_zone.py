def test_soup():
    import requests
    from bs4 import BeautifulSoup

    r = requests.get('https://mediabiasfactcheck.com/10news-one/')
    soup = BeautifulSoup(r.text, 'html.parser')
    tag = soup.find_all(class_='entry-content')

    # print([t.find('p') for t in tag if 'Bias' in t.text])

    for t in tag:
        for key in ['Bias:', 'Source:', 'Sources:']:
            if key in t.text:
                for p in t.find_all('p'):
                    if key in p.text:
                        print(key, p)


class wtf:

    def __init__(self, thing):
        print(thing)


list(map(wtf, range(5)))
