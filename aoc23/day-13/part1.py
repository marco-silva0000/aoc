from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
import numpy as np
logger = structlog.get_logger()

# def get_candidates(counts):
#     from structlog import get_logger
#     logger = get_logger()
#     logger = logger.bind(counts=counts)
#     is_odd = not len(counts) % 2 == 0
#     for i, _ in enumerate(counts):
#         lhs = counts[:i+1]
#         rhs = counts[i+1:]
#         logger = logger.bind(lhs=lhs, rhs=rhs, i=i)
#         if not lhs or not rhs:
#             return 0
#         if len(lhs) < len(rhs):
#             test = lhs.copy()
#             test.reverse()
#             test2 = rhs[:len(test)]
#             logger.debug("is reflection?", test=test)
#             if test == test2:
#                 logger.debug("got_horizontal_reflection candidate", lhs=lhs, rhs=rhs, test=test)
#                 return i
#         if len(lhs) >= len(rhs):
#             # test = rhs.copy()
#             # test.reverse()
#             # test2 = lhs[-len(test):]
#             # logger.debug("is reflection?", test=test, test2=test2)
#             test = lhs.copy()
#             logger.debug("copy", test=test)
#             test.reverse()
#             logger.debug("reverse", test=test)
#             if is_odd:
#                 test = test[1:]
#                 logger.debug("cut because odd", test=test)
#             test = test[:len(rhs)]
#             logger.debug("cut", test=test)
#             if test == rhs:
#                 logger.debug("got_horizontal_reflection candidate", lhs=lhs, rhs=rhs, test=test)
#                 return i


# def get_candidates(counts):
#     from structlog import get_logger
#     logger = get_logger()
#     logger = logger.bind(counts=counts)
#     for i, _ in enumerate(counts):
#         lhs = counts[:i+1]
#         rhs = counts[i+1:]
#         logger = logger.bind(lhs=lhs, rhs=rhs, i=i)
#         if not lhs or not rhs:
#             return 0
#         test = lhs.copy()
#         test.reverse()
#         test2 = rhs.copy()
#         test3 = test2[1:].copy()
#         if len(test) > len(test2):
#             test = test[:len(test2)]
#         elif len(test) < len(test2):
#             test2 = test2[:len(test)]
#             test3 = test3[:len(test)]
#         logger.debug("is reflection?", test=test, test2=test2, test3=test3)
#         if test == test2 or test == test3:
#             logger.debug("got_horizontal_reflection candidate", lhs=lhs, rhs=rhs, test=test)
#             return i


# def get_horizontal_reflection(pattern):
#     from structlog import get_logger
#     logger = get_logger()
#     counts = [l.count('#') for l in pattern]
#     logger = logger.bind(counts=counts)

#     candidate = get_candidates(counts)
#     logger.debug("got horizontal reflection candidate===", counts=counts, candidate=candidate)
#     for y, line in enumerate(pattern):
#         for x, c in enumerate(line):
#             print(c, end='')
#         print()
#     if candidate:
#         lhs = pattern[:candidate+1]
#         rhs = pattern[candidate+1:]
#         lhs.reverse()
#         lhs_iter = iter(lhs)
#         rhs_iter = iter(rhs)
#         prev_r = next(rhs_iter)
#         while True:
#             try:
#                 l = next(lhs_iter)
#                 r = next(rhs_iter)
#                 logger.debug("reflection check", l=l, r=r, prev_r=prev_r)
#             except StopIteration:
#                 logger.debug("reflection :)")
#                 return candidate + 1

#             if l != r and l != prev_r:
#                 logger.debug("not reflection :(", l=l, r=r, prev_r=prev_r)
#                 return 0
#             prev_r = r
#     return candidate
#     
# def get_vertical_reflection(pattern):
#     from structlog import get_logger
#     logger = get_logger()
#     counts = [0] * len(pattern[0])
#     for y, line in enumerate(pattern):
#         for x, c in enumerate(line):
#             if c == '#':
#                 counts[x] += 1

#     logger.debug("counts", counts=counts)
#     candidate = get_candidates(counts)
#     logger.debug("got vertical reflection candidate|||", counts=counts, candidate=candidate)
#     for y, line in enumerate(pattern):
#         for x, c in enumerate(line):
#             print(c, end='')
#         print()
#     if candidate:
#         a = np.array([[c for c in l] for l in pattern])
#         logger.debug("a", a=a)
#         lhs, rhs = np.array_split(a, 2, axis=1)
#         # if len(pattern) % 2 == 1:
#         #     lhs = lhs[:-1]

#         lhs = np.flip(lhs, axis=1)
#         lhs_iter = iter(lhs.T)
#         rhs_iter = iter(rhs.T)
#         prev_r = next(rhs_iter)
#         while True:
#             try:
#                 l = next(lhs_iter)
#                 r = next(rhs_iter)
#                 logger.debug("reflection check", l=l, r=r, prev_r=prev_r)
#             except StopIteration:
#                 logger.debug("reflection :)")
#                 return candidate + 1

#             if not np.array_equal(l, r) and not np.array_equal(l, prev_r):
#                 logger.debug("not reflection :(", l=l, r=r, prev_r=prev_r)
#                 return 0
#             prev_r = r
#     return candidate

def get_reflection(pattern, rotate=False):
    from structlog import get_logger
    logger = get_logger()
    pattern = np.array(pattern)
    if rotate:
        pattern = pattern.T
    logger.debug("get_reflection", pattern=pattern)
    for i in range(1, len(pattern)):
        lhs, rhs = np.array_split(pattern, [i], axis=0)
        print("pre flip lhs")
        for y, line in enumerate(lhs):
            for x, c in enumerate(line):
                print(c, end='')
            print()
        lhs = np.flipud(lhs)
        # logger.debug(lhs=lhs, rhs=rhs)
        print("post flip lhs")
        for y, line in enumerate(lhs):
            for x, c in enumerate(line):
                print(c, end='')
            print()
        print("rhs")
        for y, line in enumerate(rhs):
            for x, c in enumerate(line):
                print(c, end='')
            print()
        zippy = zip(lhs, rhs)
        for l, r in zippy:
            logger.debug("in zippy", l=l, r=r)
            if not np.array_equal(l, r):
                # logger.debug("not reflection :(", l=l, r=r)
                break
        else:
            logger.debug("reflection :)")
            return i
    return 0


def get_reflections(pattern):
    from structlog import get_logger
    logger = get_logger()
    logger.debug("get_reflections", pattern=pattern)
    horizontal = get_reflection(pattern)
    vertical = get_reflection(pattern, rotate=True)
    return horizontal, vertical

def part1(values_list) -> str:
    maps = []
    current_map = []
    for values in values_list:
        values = [int(c == '#') for c in values]
        # log.debug("values", values=values)
        if not values:
            maps.append(current_map)
            current_map = []
        else:
            current_map.append(values)
    maps.append(current_map)

    reflections = []
    logger.debug("maps", maps=maps)
    for i, m in enumerate(maps):
        structlog.contextvars.bind_contextvars(
            iteration=i,
        )
        log = logger.bind()
        log.debug("map", map=m)
        reflections.append(get_reflections(m))

    result = 0
    for h, v in reflections:
        result += h*100 + v
        
    logger.debug("result", result=result)

    return str(result)
