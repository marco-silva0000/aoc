from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

logger = structlog.get_logger()


def part1(values_list) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    first_list = []
    second_list = []
    for values in values_list:
        v1, v2 = values.split()
        first_list.append(int(v1))
        second_list.append(int(v2))
    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    first_list = sorted(first_list)
    second_list = sorted(second_list)
    result = 0
    for i in range(len(first_list)):
        first = first_list.pop(0)
        second = second_list.pop(0)
        print(
            f"diffing {first} with {second} in abs {first - second} adding it to {result}"
        )
        result += abs(first - second)
    return f"{result}"
