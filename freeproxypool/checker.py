from common import *
import copy
import asyncio
from functools import partial
import aiohttp

class CheckerManager():
    def __init__(self, hub, max_checker):
        self._hub = hub
        self._checkers = [Checker(i) for i in range(max_checker)]

    async def run(self):
        def checker_task_done(checker, proxy, f):
            if f.result():
                self._hub[proxy] = 'OK'
            else:
                self._hub[proxy] = 'FAIL'

        while True:
            async with self._hub._lock:
                ok_count = 0
                for proxy in self._hub:
                    if self._hub[proxy] == 'OK':
                        ok_count += 1
                log.info('total {} proxies in hub, {} OK'.format(len(self._hub), ok_count))
                local_hub = self._hub.copy() #TODO: add lock

            await asyncio.sleep(3)
            for proxy in local_hub:
                checker = await self.idle_checker()
                checker._status = 'working'
                task = asyncio.ensure_future(checker.check(proxy))
                task.add_done_callback(partial(checker_task_done, checker, proxy))

            await asyncio.sleep(30)

    async def idle_checker(self):
        while True:
            for checker in self._checkers:
                if checker._status == 'idle':
                    return checker
            await asyncio.sleep(1)


class Checker():
    def __init__(self, index):
        self._index = index
        self._status = 'idle'
        self._url = 'http://httpbin.org/get?show_env'
        log.debug('checker {} ready'.format(self._index))

    async def check(self, proxy):
        ret = False
        log.debug('checker {} working for {}'.format(self._index, proxy))
        proxy_str = '{}:{}'.format(proxy[0], proxy[1])
        #proxy = '39.137.77.66:8080'
        log.debug('use proxy {}'.format(proxy_str))
        #await asyncio.sleep(1)
        timeout = aiohttp.ClientTimeout(total=6)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=self._url, timeout=timeout, proxy="http://{}".format(proxy_str)) as resp:
                    page = await resp.text()
                    log.debug(page)
                    if proxy[0] in page:
                        ret = True
                        log.info('proxy {} OK'.format(proxy_str))
        except (
            asyncio.TimeoutError,
            aiohttp.ClientOSError,
            aiohttp.ClientResponseError,
            aiohttp.ServerDisconnectedError,
        ) as e:
            log.debug('%s is failed. Error: %r;' % (self, e))
        finally:
            self._status = 'idle'
            log.debug('checker {} done for {}: {}'.format(self._index, proxy, ret))

        return ret
