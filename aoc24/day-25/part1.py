from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from itertools import product
import numpy as np

logger = structlog.get_logger()


def part1(values_list) -> str:
    from structlog import get_logger

    ctx = contextvars.copy_context()
    logging_ctx_value = None
    for var, value in ctx.items():
        if var.name == "logging":
            logging_ctx_value = value
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging_ctx_value),
    )

    log = get_logger()
    log.info("day 25 part1")
    result = []
    maps = [[]]

    for index, values in enumerate(values_list):
        if values == "":
            maps.append([])
            continue
        maps[-1].append([1 if value == "#" else 0 for value in values])

        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
    # keys have first row all ones
    keys = []
    locks = []

    for map in maps:
        log.debug(map)
        log.debug(map[0])
        log.debug(map[-1])
        log.debug(map[0] == 1)
        if all([m == 1 for m in map[0]]):
            log.debug("all are one, is key")
            keys.append(np.array(map))
        elif all([m == 1 for m in map[-1]]):
            log.debug("all are one, is lock")
            locks.append(np.array(map))

    result = 0
    for key, lock in product(keys, locks):
        # log.debug("trying", key=key, lock=lock)
        log.debug(key + lock)
        skip = False
        for row in key + lock:
            for cell in row:
                log.debug(cell)
                if cell >= 2:
                    skip = True
                    break
        if not skip:
            log.debug("found", key=key, lock=lock)
            result += 1

    print(result)
    return f"{result}"
