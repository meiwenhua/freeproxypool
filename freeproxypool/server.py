from common import *
import asyncio
from aiohttp import web

class Server():
    def __init__(self, hub):
        async def handler(request):
            log.info('{}'.format(self._hub))
            return web.Response(text='{}'.format(self._hub))

        self._hub = hub
        self._server = web.Server(handler)
        self._runner = web.ServerRunner(self._server)

    async def run(self):
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, 'localhost', 8080)
        await self._site.start()
        await asyncio.sleep(100*3600)

