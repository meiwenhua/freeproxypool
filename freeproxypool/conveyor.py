from common import *

class Conveyor():
    def __init__(self, queue, hub):
        self._queue = queue
        self._hub = hub

    async def run(self):
        while True:
            fetcher_domain, proxies = await self._queue.get()

            log.debug('get some in queue')
            new_proxies = []
            for proxy in proxies:
                if not proxy in self._hub:
                    new_proxies.append(proxy)
                    self._hub[proxy] = 'new'

            log.info('from {}:get {} proxies, {} new proxies'.format(fetcher_domain, len(proxies), len(new_proxies)))

