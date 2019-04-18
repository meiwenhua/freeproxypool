from common import *
import asyncio

class Hub(dict):
    def __init__(self):
        self._lock = asyncio.Lock()
