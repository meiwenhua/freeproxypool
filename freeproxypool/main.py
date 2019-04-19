#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    File name: main.py
    Author: meiwenhua
    Date created: 4/11/2019
    Python Version: 3.7
'''

from common import *
from fetcher import fetchers
from feeder import feeders
from factory import Factory
from server import Server
from hub import Hub
import asyncio
import logging
import sys

def main():
    hub = Hub()
    if '-v' in sys.argv:
        set_console_log_level(logging.DEBUG)

    log.info('Start')
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    factory = Factory(loop, queue, fetchers, feeders, hub)
    tasks = factory.get_tasks()
    tasks.append(asyncio.ensure_future(Server(hub).run()))
    loop.run_until_complete(asyncio.gather(*tasks, loop=loop))

if __name__ == '__main__':
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
    main()
