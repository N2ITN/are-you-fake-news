import aiohttp
import asyncio
import async_timeout
import os
import uvloop

scrape_api = 'https://x9wg9drtci.execute-api.us-west-2.amazonaws.com/prod/article_get'

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class res:
    data = {}

    def update(kv: dict):
        res.data.update(kv)


async def download_coroutine(session, url):

    with async_timeout.timeout(7):

        async with session.put(scrape_api, data=url, timeout=7) as response:
            try:
                article_text = await response.text()
                res.update({url: article_text})
            except asyncio.TimeoutError:
                pass


async def main(loop, urls):

    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [download_coroutine(session, url) for url in urls]
        await asyncio.gather(*tasks, return_exceptions=True)


def caller(urls):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(main(loop, urls))
    return res.data


if __name__ == '__main__':
    urls = ['http://google.com', 'http://amazon.com', 'http://rt.com', 'http://fadfdsfce.com']

    print(caller(urls))
