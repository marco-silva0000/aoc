from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

logger = structlog.get_logger()


@dataclass()
class Point:
    x: int
    y: int


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
    log.info("day 5 part1")
    is_in_list = False
    fresh_index = []
    result = 0
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        if not values:
            is_in_list = True
            continue
        if not is_in_list:
            start, end = values.split("-")
            fresh_index.append(Point(int(start), int(end)))
        else:
            item = int(values)
            for fresh_range in fresh_index:
                if item >= fresh_range.x and item <= fresh_range.y:
                    result += 1
                    log.debug(
                        f"Ingredient ID {item} is fresh because it falls into range {fresh_range.x}-{fresh_range.y}"
                    )
                    break

    print(result)
    return f"{result}"
