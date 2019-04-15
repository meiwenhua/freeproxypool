import os
import logging
from colorlog import ColoredFormatter
import datetime
from logging.handlers import RotatingFileHandler

DEFAULT_LOG_LEVEL = logging.DEBUG
CONSOLE_LOG_LEVEL = logging.INFO
FILE_LOG_LEVEL = logging.DEBUG
PROJECT_NAME = 'freeproxypool'

s_handler = None

def get_logger():
    global s_handler
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "%(log_color)s[%(levelname).1s][%(asctime)s][%(filename)s:%(lineno)d]:%(message)s",
        datefmt='%Y%m%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )

    logger = logging.getLogger(PROJECT_NAME)

    #add handler at first time call
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        s_handler = logging.StreamHandler()
        s_handler.setFormatter(formatter)
        s_handler.setLevel(CONSOLE_LOG_LEVEL)
        logger.addHandler(s_handler)

        f_handler = RotatingFileHandler(os.path.join('log', 'log'), maxBytes=10000000, backupCount=5)
        f_handler.setFormatter(formatter)
        f_handler.setLevel(FILE_LOG_LEVEL)
        logger.addHandler(f_handler)

        keep_fds = [f_handler.stream.fileno()]

    return logger, keep_fds

def set_console_log_level(level):
    if s_handler:
        s_handler.setLevel(level)

log, keep_fds = get_logger()
