"""
Download article text given list of article urls
"""

import requests
from collections import deque
import json

import time


def lambda_handler(data, context=None):
    print(type(data))
    url_list = json.loads(data['body'])
    print(type(url_list))

    scrape_api = 'https://x9wg9drtci.execute-api.us-west-2.amazonaws.com/prod/article_get'
    '''
    def scrape_api_endpoint(url_):
        response = json.loads(requests.put(scrape_api, data=url_).text)
        if 'message' in response:
            return None
        return {url_: response}

    res = {}
    chunk_size = 20
    while len(url_list) > 0:
        if len(url_list) >= chunk_size:
            url_chunk = [url_list.pop() for _ in range(chunk_size)]
        else:
            url_chunk = [url_list.pop() for _ in range(len(url_list))]
        # print(url_chunk[0])
        for article_text in dummy.Pool(chunk_size).imap_unordered(scrape_api_endpoint, url_chunk):

            if not article_text:

                break
            else:
                res.update(article_text)
        time.sleep(.1)
    '''
    res = {}
    import asyncio
    import concurrent.futures
    import requests
    import aiohttp

    scrape_api = 'https://x9wg9drtci.execute-api.us-west-2.amazonaws.com/prod/article_get'

    async def get_article(url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.put(scrape_api, data=url, timeout=2) as resp:
                    data = await resp.json()

                    res.update({url: data})
            except concurrent.futures._base.TimeoutError:
                ...

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.gather(*(get_article(url) for url in url_list)))

    return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(res)}


if __name__ == '__main__':

    url_list = [
        "http://cnn.com/2015/07/07/us/illinois-athletics-allegations/index.html",
        "http://cnn.com/2015/05/19/us/scam-charity-investigation/index.html",
        "http://cnn.com/2015/04/13/us/airport-luggage-theft/index.html",
        "http://cnn.com/2015/09/10/us/virgin-islands-pesticide-investigation/index.html",
        "http://cnn.com/2015/03/13/us/va-investigation-los-angeles/index.html",
        "http://cnn.com/2015/03/13/us/irs-scam/index.html",
        "http://cnn.com/2014/11/17/us/south-dakota-indian-school-fundraising-investigation/index.html",
        "http://cnn.com/2014/10/29/politics/politicians-play-lobbyists-pay/index.html",
        "http://cnn.com/2016/09/22/us/immigration-attitudes-cnn-kff-poll/index.html",
        "http://cnn.com/2016/09/25/politics/white-working-class-overview-kff-poll/index.html",
        "http://cnn.com/2016/09/20/politics/2016-election-white-working-class-voters/index.html",
        "http://cnn.com/2016/09/24/politics/white-working-class-evangelicals/index.html",
        "http://cnn.com/2016/09/23/opinions/shell-shocked-white-working-class-opinion-coontz/index.html",
        "http://cnn.com/2016/09/20/politics/election-2016-white-working-class-donald-trump-kaiser-family-foundation/index.html",
        "http://cnn.com/2016/09/20/politics/white-working-class-americans-have-split-on-muslim-immigrants-trump-clinton/index.html",
        "http://money.cnn.com/2016/09/21/news/economy/white-working-class-government/index.html?iid=hp-toplead-dom",
        "http://www.cnn.com/2016/09/19/politics/trump-supporters-working-class-white-kaiser-family-foundation-infographic/index.html",
        "http://money.cnn.com/2016/09/23/news/economy/white-working-class-economy/index.html",
        "http://cnn.com/2017/08/15/world/iyw-aid-sierra-leone-mudslide-victims/index.html",
        "http://cnn.com/2017/03/16/world/iyw-how-to-help-east-africa/index.html",
        "http://cnn.com/2016/10/19/middleeast/iyw-mosul-iraq-how-to-help/index.html",
        "http://cnn.com/2016/05/10/health/iyw-prescription-drug-abuse-how-to-help-health/index.html",
        "http://cnn.com/2017/08/07/world/iyw-impact-of-youssif/index.html",
        "http://cnn.com/2016/10/28/us/iyw-girl-friendship-trnd/index.html",
        "http://cnn.com/2016/09/28/world/iyw-girl-up-michelle-obama-girls-education-how-to-help/index.html",
        "http://cnn.com/2015/01/06/world/iyw-syria-resource-list/index.html",
        "http://cnn.com/2017/06/28/world/elle-snow-trafficking/index.html",
        "http://cnn.com/2017/05/30/world/ciw-fair-food-program-freedom-project/index.html",
        "http://cnn.com/2017/06/02/world/tonys-chocolonely-slavery-free-chocolate/index.html",
        "http://cnn.com/2017/04/26/americas/brazil-amazon-slavery-freedom-project/index.html",
        "http://cnn.com/2017/07/26/asia/cambodia-brick-kiln/index.html",
        "http://cnn.com/2017/07/24/asia/return-to-cambodia-sex-trafficking/index.html",
        "http://www.cnn.com/interactive/2014/05/specials/city-of-tomorrow/index.html",
        "http://www.cnn.com/interactive/2014/09/health/cnn10-healthiest-cities/"
    ]

    print(len(url_list))
    response = json.loads(lambda_handler({'body': json.dumps(url_list)})['body'])
    print(len(response))
    # first_item = list(response.keys())[0]
    # print(first_item, response[first_item])
