"""
Download article text given list of article urls
"""

import asyncio

import newspaper
from async_timeout import timeout


def scrape(url):
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()
    except newspaper.article.ArticleException:
        return ''
    output = article.text + ' ' + article.title

    return output


def meta_async(url_list):

    res = {}

    async def get_article(url: str):
        with timeout(2):
            text = scrape(url)

            return res.update({url: text})

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*(get_article(url) for url in url_list)))
    return res


if __name__ == '__main__':

    urls = [
        "http://cnn.com/2015/07/07/us/illinois-athletics-allegations/index.html",
        "http://cnn.com/2015/05/19/us/scam-charity-investigation/index.html",
        "http://cnn.com/2015/04/13/us/airport-luggage-theft/index.html",
        "http://cnn.com/2015/09/10/us/virgin-islands-pesticide-investigation/index.html",
        "http://cnn.com/2015/03/13/us/va-investigation-los-angeles/index.html",
        "http://cnn.com/2015/03/13/us/irs-scam/index.html"
    ]

    print(len(urls))
    response = meta_async(urls)
    print(len(response))
    first_item = list(response.keys())[0]
    print(first_item, response[first_item])
