from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from time import sleep

logger = structlog.get_logger()



class Point(StrEnum):
    EMPTY = "."
    CUBE = "#"
    ROUNDED = "O"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    GOLD = '\033[0;33;46m'
    UNDERLINE = '\033[4m'

def print_platform(platform, max_x=0, max_y=0, highlight_x=None, highlight_y=None, flush=False):
    output = ""
    for y in range(max_y):
        for x in range(max_x):
            sleep(0.01)
            if (x, y) == (highlight_x, highlight_y):
                print(f"{bcolors.GOLD}{platform[(x, y)]}{bcolors.ENDC}", end="", flush=flush)
            else:
                print(platform[(x, y)], end="", flush=flush)
        print(flush=flush)

def print_platform(platform, max_x=0, max_y=0, highlight_x=None, highlight_y=None, flush=False):
    output = "\r"
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) == (highlight_x, highlight_y):
                output += f"{bcolors.GOLD}{platform[(x, y)]}{bcolors.ENDC}"
                # print(f"{bcolors.GOLD}{platform[(x, y)]}{bcolors.ENDC}", end="", flush=flush)
            else:
                output += platform[(x, y)]
                # print(platform[(x, y)], end="", flush=flush)
        # print(flush=flush)
        output += "\n"
    print(output, end="", flush=flush)
    if flush:
        sleep(0.05)


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
            else: # ROUNDED
                if (free_spot:= free_spots[x]) is not None:
                    # logger.debug("there's a free spot, gonna move", free_spots=free_spots)
                    platform[(x, free_spot)] = Point.ROUNDED
                    platform[(x, y)] = Point.EMPTY
                    free_spots[x] += 1
            # print_platform(platform, max_x=max_x, max_y=max_y, highlight_x=x, highlight_y=y)
    return platform


def count_stones(platform, max_y, print=False):
    result = 0
    for (x, y), value in platform.items():
        # print_platform(platform, max_x=max_y, max_y=max_y, highlight_x=x, highlight_y=y, flush=True)
        if value == Point.ROUNDED:
            result += (max_y - y)
    return result

def rotate_right(platform, max_x=0, max_y=0):
    new_platform = {}
    for y in range(max_y):
        for x in range(max_x):
            new_platform[(max_y - y - 1, x)] = platform[(x, y)]
    return new_platform

def cycle_platform(platform, max_x=0, max_y=0):
    from structlog import get_logger
    logger = get_logger()
    logger = logger.bind(max_x=max_x, max_y=max_y)
    # logger.debug("cycle_platform")
    # logger.debug("gonna tilt north")
    new_platform = tilt_up(platform, max_x=max_y, max_y=max_x)
    # print_platform(new_platform, max_x=max_x, max_y=max_y)
    # logger.debug("gonna rotate right")
    new_platform = rotate_right(new_platform, max_x=max_x, max_y=max_y)
    # print_platform(new_platform, max_x=max_x, max_y=max_y)
    # logger.debug("gonna titl west")
    new_platform = tilt_up(new_platform, max_x=max_y, max_y=max_x)
    # print_platform(new_platform, max_x=max_x, max_y=max_y)
    # logger.debug("gonna rotate right")
    new_platform = rotate_right(new_platform, max_x=max_x, max_y=max_y)
    # print_platform(new_platform, max_x=max_x, max_y=max_y)
    # logger.debug("gonna tilt south")
    new_platform = tilt_up(new_platform, max_x=max_y, max_y=max_x)
    # print_platform(new_platform, max_x=max_x, max_y=max_y)
    # logger.debug("gonna rotate right")
    new_platform = rotate_right(new_platform, max_x=max_x, max_y=max_y)
    # print_platform(new_platform, max_x=max_x, max_y=max_y)
    # logger.debug("gonna tilt east")
    new_platform = tilt_up(new_platform, max_x=max_y, max_y=max_x)
    # print_platform(new_platform, max_x=max_x, max_y=max_y)
    # logger.debug("gonna rotate back to original")
    new_platform = rotate_right(new_platform, max_x=max_x, max_y=max_y)
    # print_platform(new_platform, max_x=max_x, max_y=max_y)
    return new_platform

def generate_map_hashkey(platform, max_x=0, max_y=0):
    result = ()
    for y in range(max_y):
        part = ()
        for x in range(max_x):
            part += ('.#O'.index(platform[(x, y)].value), )
        result += (part, )
    return hash(result)

def part2(values_list, spins=1000000000) -> str:
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
    print_platform(platform, max_x=max_x, max_y=max_y)

    seen_keys = set()
    tail = []
    looped = False
    spin = 0
    while spin < spins:
        platform = cycle_platform(platform, max_x=max_x, max_y=max_y)
        hashkey = generate_map_hashkey(platform, max_x=max_x, max_y=max_y)
        # print(hashkey)
        # print(seen_keys)
        # print(hashkey in seen_keys)
        if hashkey in seen_keys and not looped:
            print("found a loop")
            # print(tail)
            index = tail.index(hashkey)
            size = len(tail) - index
            delta = spins - spin
            n_loops = delta // size
            spin += n_loops * size
            looped = True
            logger.debug("looped", spin=spin, n_loops=n_loops, size=size, delta=delta, index=index, hashkey=hashkey)

        tail.append(hashkey)
        seen_keys.add(hashkey)
        if spin % 1000 == 0:
            print(f"spin: {spin}")
        spin += 1

    print_platform(platform, max_x=max_x, max_y=max_y)
    result = count_stones(platform, max_y, print=True)
    print(result)
    return str(result)
