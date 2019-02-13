import newspaper
import json
import requests


def crawl(url: str):

    def test_url(url):
        print(url)
        try:
            if requests.get(url, timeout=4).ok:
                print('connected to url'.format(url))
                return url
            else:
                print('failed to connect to url'.format(url))
                return
        except requests.exceptions.ConnectionError:
            print('connection error')
            return 'ConnectionError'

    def https_test(url):
        if 'http://' or 'https://' not in url:
            return test_url('http://' + url) or test_url('https://' + url)
        else:
            return test_url(url)

    def get_newspaper(url):

        try:
            src = newspaper.build(
                url, fetch_images=False, request_timeout=7, limit=100, memoize_articles=False)

        except Exception as e:
            print(e)
            print(url)
            return "No articles found!"
        if len(src.articles) == 0:
            return "Empty list"

        url_list = [a.url for a in src.articles]
        print(url_list[0])
        return url_list

    url = https_test(url)
    output = get_newspaper(url)

    return output