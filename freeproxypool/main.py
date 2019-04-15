#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    File name: main.py
    Author: meiwenhua
    Date created: 4/11/2019
    Python Version: 3.7
'''

from fetcher import fetchers, FetcherSchedule
from feeder import FeederSchedule
import asyncio
from common import *
import logging
import sys

async def main():
    if '-v' in sys.argv:
        set_console_log_level(logging.DEBUG)

    log.info('Start')
    q_fetch = asyncio.Queue()
    fetcher_schedule = FetcherSchedule(q_fetch, fetchers)
    feeder_schedule = FeederSchedule(q_fetch)

    task1 = asyncio.create_task(fetcher_schedule.run())
    task2 = asyncio.create_task(feeder_schedule.run())
    await task1
    await task2

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
