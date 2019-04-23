from common import *
import copy
import asyncio
from functools import partial
import aiohttp
import datetime

class CheckerManager():
    def __init__(self, hub):
        self._hub = hub
        self._checkers = [Checker(i) for i in range(config.checker_number)]

    async def run(self):
        def checker_task_done(checker, proxy, f):
            if f.result():
                self._hub[proxy].check_record.append(('ok','{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
                self._hub[proxy].status = 'ok'
                self._hub[proxy].continuous_fail_count = 0
                self._hub[proxy].total_ok_count += 1
            else:
                self._hub[proxy].check_record.append(('fail','{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
                self._hub[proxy].status = 'fail'
                self._hub[proxy].continuous_fail_count += 1
                self._hub[proxy].total_fail_count += 1

        while True:
            async with self._hub._lock:
                local_hub = self._hub.copy() #TODO: add lock??
                ok_count = 0
                for proxy in local_hub:
                    if local_hub[proxy].status == 'ok':
                        ok_count += 1
                log.info('total {} proxies in hub, {} OK'.format(len(local_hub), ok_count))

            await asyncio.sleep(3)
            for proxy in [ x for x in local_hub if local_hub[x].continuous_fail_count < config.checker_max_continuous_fail_count ]:
                checker = await self.idle_checker()
                checker._status = 'working'
                task = asyncio.ensure_future(checker.check(proxy))
                task.add_done_callback(partial(checker_task_done, checker, proxy))

            await asyncio.sleep(config.checker_period)

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
        log.debug('use proxy {}'.format(proxy_str))
        timeout = aiohttp.ClientTimeout(total=config.checker_judge_timeout)
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
