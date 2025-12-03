from typing import List, Set, Dict, Tuple, Optional, Union
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from structlog import get_logger

logger = structlog.get_logger()


def get_joltage(values: str, n: int) -> int:
    log = get_logger()
    if n == 0:
        return ""
    if n == 1:
        max_c = max(values)
    else:
        max_c = max(values[: -n + 1])
    index_c = values.index(max_c)
    log.debug("", values=values, n=n, index_c=index_c, max_c=max_c)
    return max_c + get_joltage(values[index_c + 1 :], n - 1)


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
    log.info("day 3 part2")
    result = []
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        joltage = get_joltage(values, 12)
        log.debug("values", values=values, joltage=joltage)
        result.append(int(joltage))
    print(sum(result))
    return f"{sum(result)}"
