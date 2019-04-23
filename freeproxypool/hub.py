from common import *
import asyncio

class Hub(dict):
    def __init__(self, _dict={}):
        self._lock = asyncio.Lock()
        super(Hub, self).__init__(_dict)
