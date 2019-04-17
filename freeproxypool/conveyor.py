from common import *

class Conveyor():
    def __init__(self, queue, feeders):
        self._queue = queue
        self._feeders = feeders

    async def run(self):
        while True:
            proxies = await self._queue.get()

            log.debug('get some in queue')
            for feeder in self._feeders:
                await feeder.feed(proxies)
