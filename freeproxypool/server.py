from common import *
import asyncio
from aiohttp import web

class Server():
    def __init__(self, hub):
        async def handler(request):
            proxies = []
            for proxy in self._hub:
                if self._hub[proxy] == 'OK':
                    proxies.append('{}:{}'.format(proxy[0], proxy[1]))
            return web.json_response(proxies)

        self._hub = hub
        self._server = web.Server(handler)
        self._runner = web.ServerRunner(self._server)

    async def run(self):
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, '0.0.0.0', 8080)
        await self._site.start()
        await asyncio.sleep(100*3600)

