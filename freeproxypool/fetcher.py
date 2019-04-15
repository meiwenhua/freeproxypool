import asyncio
import aiohttp
import random
import re

IPPortPatternGlobal = re.compile(
    r'(?P<ip>(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))'  # noqa
    r'(?=.*?(?:(?:(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))|(?P<port>\d{2,5})))',  # noqa
    flags=re.DOTALL,
)

class FetcherSchedule():
    def __init__(self, queue, fetchers):
        self.fetchers = fetchers
        self.queue = queue

    async def run(self):
        while True:
            for fetcher in self.fetchers:
                await fetcher.fetch(self.queue)

            await asyncio.sleep(10)

class Fetcher():
    def __init__(self, domain, urls):
        self.domain = domain
        self.urls = urls
        self._session = aiohttp.ClientSession()
        self._headers = {'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    async def fetch(self, queue):
        '''
        await asyncio.sleep(5)
        random_proxy = '{}.{}.{}.{}:{}'.format(
            random.randint(10,254),
            random.randint(10,254),
            random.randint(10,254),
            random.randint(10,254),
            random.randint(1,65535)
        )
        print(random_proxy)
        await queue.put(random_proxy)
        '''
        for url in self.urls:
            async with self._session.request('GET', url, headers=self._headers) as resp:
                page = await resp.text()
                proxies = IPPortPatternGlobal.findall(page)
                print('fetch put queue: {}'.format(proxies))
                await queue.put(proxies)
                print('queue size {}'.format(queue.qsize()))

fetcher1 = Fetcher('data5u.com', ['http://www.data5u.com/free/gngn/index.shtml'])
fetchers = [fetcher1]

