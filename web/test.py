# Example 3: asynchronous requests with larger thread pool
import asyncio
import concurrent.futures
import requests
import aiohttp

scrape_api = 'https://x9wg9drtci.execute-api.us-west-2.amazonaws.com/prod/article_get'


async def get_article(url):
    async with aiohttp.ClientSession() as session:
        async with session.put(scrape_api, data=url) as resp:
            data = await resp.text()
            print(data)
        return data


loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(*(get_article(url) for url in ['http://cnn.com', 'http://google.com'])))
