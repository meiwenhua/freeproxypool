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
from factory import Factory
from server import Server
from hub import Hub
import asyncio
import logging
import sys
import pickle
import argparse
import sys

def main():
    #handle argument
    parser = argparse.ArgumentParser(description='fetch and check free proxies')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-l', '--load', action='store_true', help='load hub.plk file')
    args = parser.parse_args(sys.argv[1:])

    if args.verbose:
        set_console_log_level(logging.DEBUG)

    if args.load:
        with (open("hub.pkl", "rb")) as f:
            _hub = pickle.load(f)
            hub = Hub(_hub)
    else:
        hub = Hub()

    log.info('Start')
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    factory = Factory(loop, queue, fetchers, hub)
    tasks = factory.get_tasks()
    tasks.append(asyncio.ensure_future(Server(hub).run()))
    tasks = asyncio.gather(*tasks, loop=loop)
    try:
        loop.run_until_complete(tasks)
    except KeyboardInterrupt:
        with open('hub.pkl', 'wb') as f:
            pickle.dump(hub.copy(), f, pickle.HIGHEST_PROTOCOL)
    finally:
        loop.close()

if __name__ == '__main__':
    main()
