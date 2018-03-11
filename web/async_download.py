import asyncio
import concurrent.futures
import json
import time
from collections import deque

import aiohttp
import requests


def get_data(url_list: list, context=None):

    res = {}

    async def get_article(url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=2) as resp:
                    data = await resp.text()
                    print(data)

                    res.update({url: data})
            except concurrent.futures._base.TimeoutError:
                ...

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.gather(*(get_article(url) for url in url_list)))

    return json.dumps(res)


data = get_data(['http://google.com', 'http://amazon.com', 'http://facebook.com'])

print(data)