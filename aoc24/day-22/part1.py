from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

logger = structlog.get_logger()


def calc_secret_number(n):
    n2 = n ^ (n << 6) % 16777216
    n3 = (n2 >> 5) ^ n2 % 16777216
    return n3 ^ (n3 << 11) % 16777216


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
    log.info("day 22 part1")
    numbers = []
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        numbers.append(int(values))
    results = []
    for n in numbers:
        r = n
        for _ in range(2000):
            r = calc_secret_number(r)
        results.append(r)

    print(results)
    print(sum(results))
    return f"{sum(results)}"
