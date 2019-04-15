from common import *

class FeederSchedule():
    def __init__(self, f_queue):
        self.feeders = [Feeder()]
        self.f_queue = f_queue

    async def run(self):
        while True:
            proxies = await self.f_queue.get()

            log.debug('get some in queue')
            for feeder in self.feeders:
                await feeder.feed(proxies)


class Feeder():
    def __init__(self):
        pass

    async def feed(self, proxies):
        log.debug('feed {}'.format(proxies))
