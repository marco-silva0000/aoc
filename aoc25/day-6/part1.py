from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from collections import defaultdict

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
    log.info("day 6 part1")
    result = 0
    worksheet = defaultdict(list)
    for iteration, values in enumerate(values_list[:-1]):
        structlog.contextvars.bind_contextvars(
            iteration=iteration,
        )
        logger.debug(values)
        for index, value in enumerate(values.split()):
            worksheet[index].append(int(value))
    logger.debug(worksheet)
    logger.debug(values_list[-1])
    for index, operation in enumerate(values_list[-1].split()):
        logger.debug(operation)
        logger.debug(worksheet[index])

        problem = operation.join(map(str, worksheet[index]))
        solution = eval(problem)
        logger.debug(f"{problem}={solution}")
        result += solution

    print(result)
    return f"{result}"
