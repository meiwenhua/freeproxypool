import asyncio

from fetcher import FetcherManager
from conveyor import Conveyor

class Factory():
    def __init__(
        self,
        loop,
        queue,
        fetchers,
        feeders
    ):
        self._loop = loop
        self._queue = queue
        self._tasks = []
        self._fetchers = fetchers
        self._feeders = feeders

    def run(self):
        self._tasks = [
            asyncio.ensure_future(FetcherManager(self._queue, self._fetchers).run()),
            asyncio.ensure_future(Conveyor(self._queue, self._feeders).run())
        ]
        self._loop.run_until_complete(asyncio.gather(*self._tasks, loop=self._loop))
