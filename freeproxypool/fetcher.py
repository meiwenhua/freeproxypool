import asyncio
import aiohttp
import random
import re
from common import *

IPPortPatternGlobal = re.compile(
    r'(?P<ip>(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))'  # noqa
    r'(?=.*?(?:(?:(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))|(?P<port>\d{2,5})))',  # noqa
    flags=re.DOTALL,
)

class FetcherManager():
    def __init__(self, hub, fetchers):
        self._hub = hub
        self._fetchers = fetchers

    async def run(self):
        while True:
            for fetcher in self._fetchers:
                await fetcher.fetch(self._hub)

            await asyncio.sleep(100)

class Fetcher():
    def __init__(self, domain, urls):
        self._domain = domain
        self._urls = urls
        self._session = aiohttp.ClientSession()
        self._headers = {'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    async def fetch(self, hub):
        for url in self._urls:
            async with self._session.request('GET', url, headers=self._headers) as resp:
                page = await resp.text()
                proxies = IPPortPatternGlobal.findall(page)
                new_proxies = []
                for proxy in proxies:
                    if not proxy in hub:
                        async with hub._lock:
                            hub[proxy] = 'new'
                        new_proxies.append(proxy)
                log.info('from {}:get {} proxies, {} new proxies, {} total in hub'.format(self._domain, len(proxies), len(new_proxies), len(hub)))

fetcher1 = Fetcher('66ip', ['http://www.66ip.cn/mo.php?sxb=&tqsl=30&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='])
fetchers = [fetcher1]

