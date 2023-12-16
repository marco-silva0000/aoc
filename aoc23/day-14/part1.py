from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

logger = structlog.get_logger()


class Point(StrEnum):
    EMPTY = "."
    CUBE = "#"
    ROUNDED = "O"


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    GOLD = "\033[0;33;46m"
    UNDERLINE = "\033[4m"


def print_platform(platform, max_x=0, max_y=0, highlight_x=None, highlight_y=None):
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) == (highlight_x, highlight_y):
                print(f"{bcolors.GOLD}{platform[(x, y)]}{bcolors.ENDC}", end="")
            else:
                print(platform[(x, y)], end="")
        print()


def tilt_up(platform, max_x=0, max_y=0):
    from structlog import get_logger

    logger = get_logger()
    # logger = logger.bind(platform=platform)
    free_spots = [None] * max_x
    # print_platform(platform, max_x=max_x, max_y=max_y)
    for y in range(max_y):
        for x in range(max_x):
            # logger = logger.bind(x=x, y=y)
            if platform[(x, y)] == Point.EMPTY:
                # logger.debug("found free spot", free_spots=free_spots)
                if free_spots[x] is None:
                    free_spots[x] = y
            elif platform[(x, y)] == Point.CUBE:
                if free_spots[x] is not None:
                    # logger.debug("found cube", free_spots=free_spots)
                    free_spots[x] = None
            else:  # ROUNDED
                if (free_spot := free_spots[x]) is not None:
                    # logger.debug("there's a free spot, gonna move", free_spots=free_spots)
                    platform[(x, free_spot)] = Point.ROUNDED
                    platform[(x, y)] = Point.EMPTY
                    free_spots[x] += 1
            # print_platform(platform, max_x=max_x, max_y=max_y, highlight_x=x, highlight_y=y)
    return platform


def part1(values_list) -> str:
    result = []
    platform = {}
    max_y = 0
    max_x = 0
    for y, values in enumerate(values_list):
        for x, value in enumerate(values):
            platform[(x, y)] = Point(value)
        max_y = y
        max_x = len(values)
    max_y += 1

    # print_platform(platform, max_x=max_x, max_y=max_y)
    # print('will tilt up')
    new_platform = tilt_up(platform, max_y=max_y, max_x=max_x)
    # print_platform(new_platform, max_x=max_x, max_y=max_y)
    result = 0
    for (_, y), value in new_platform.items():
        if value == Point.ROUNDED:
            result += max_y - y
    print(result)
    return str(result)
