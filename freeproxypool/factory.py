import asyncio

from fetcher import FetcherManager
from checker import CheckerManager
from hub import Hub

class Factory():
    def __init__(
        self,
        loop,
        queue,
        fetchers,
        hub
    ):
        self._loop = loop
        self._queue = queue
        self._tasks = []
        self._fetchers = fetchers
        self._hub = hub

    def get_tasks(self):
        self._tasks = [
            asyncio.ensure_future(FetcherManager(self._hub, self._fetchers).run()),
            asyncio.ensure_future(CheckerManager(self._hub).run())
        ]
        return self._tasks
        #self._loop.run_until_complete(asyncio.gather(*self._tasks, loop=self._loop))
