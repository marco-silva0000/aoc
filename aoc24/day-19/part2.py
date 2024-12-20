from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import functools

logger = structlog.get_logger()


def part2(values_list) -> str:
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
    log.info("day 19 part2")
    data = iter(values_list)
    flegs = next(data).split(", ")
    _ = next(data)
    patterns = []
    for pattern in data:
        patterns.append(pattern)
    log.debug(patterns)
    log.debug(flegs)

    @functools.cache
    def count_valids(right_part: str):
        log.debug(f"counting for {right_part}")
        if right_part == "":
            return 1
        result = 0
        valids = filter(lambda x: right_part.startswith(x), flegs)
        for valid in valids:
            next_right_part = right_part.removeprefix(valid)
            log.debug(f"{valid} is valid", next_right_part=next_right_part)
            result += count_valids(next_right_part)
        return result

    n_paths = 0
    for index, pattern in enumerate(patterns):
        n_paths += count_valids(pattern)

    print(n_paths)
    return f"{n_paths}"
