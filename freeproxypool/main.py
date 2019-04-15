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

'''
async def main():
    #loop = asyncio.get_event_loop()
    #print('loop is running {}'.format(loop.is_running()))
    #loop.run_forever()
    #loop.set_debug(True)
    q_fetch = asyncio.Queue()
    fetcher_schedule = FetcherSchedule(q_fetch, fetchers)
    #print(fetchers)
    #tasks = [loop.create_task(fetcher.fetch(q_fetch)) for fetcher in fetchers]
    #print(tasks)
    #loop.run_until_complete(fetcher_schedule.run())
    await fetcher_schedule.run()

if __name__ == '__main__':
    asyncio.run(main())
'''
async def main():
    #loop = asyncio.get_event_loop()
    #loop.set_debug(True)
    q_fetch = asyncio.Queue()
    fetcher_schedule = FetcherSchedule(q_fetch, fetchers)
    feeder_schedule = FeederSchedule(q_fetch)
    #print(fetchers)
    #tasks = [loop.create_task(fetcher.fetch(q_fetch)) for fetcher in fetchers]
    #print(tasks)
    task1 = asyncio.create_task(fetcher_schedule.run())
    task2 = asyncio.create_task(feeder_schedule.run())
    await task1
    await task2

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
