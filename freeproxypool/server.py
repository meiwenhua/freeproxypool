from common import *
import asyncio
from aiohttp import web
from functools import partial
import json

class Server():
    def __init__(self, hub):
        async def handler(request):
            if (request.method == 'GET'):
                proxies = []
                if (request.path == '/'):
                    for proxy in self._hub:
                        if self._hub[proxy].status == 'ok':
                            proxies.append('{}:{}'.format(proxy[0], proxy[1]))
                if (request.path == '/debug'):
                    for proxy in self._hub:
                        proxies.append('({}:{}, {})'.format(proxy[0], proxy[1], self._hub[proxy].check_record))
                return web.json_response(proxies, dumps=partial(json.dumps, indent=2))

        self._hub = hub
        self._server = web.Server(handler)
        self._runner = web.ServerRunner(self._server)

    async def run(self):
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, config.web_server_ip, config.web_server_port)
        await self._site.start()
        await asyncio.sleep(100*365*24*3600)

