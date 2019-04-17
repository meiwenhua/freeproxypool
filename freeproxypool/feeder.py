from common import *

class Feeder():
    def __init__(self):
        pass

    async def feed(self, proxies):
        log.debug('feed {}'.format(proxies))

feeders = [Feeder()]
