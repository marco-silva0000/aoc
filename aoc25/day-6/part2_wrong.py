from typing import List, Set, Dict, Tuple, Optional, Union
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from collections import defaultdict

logger = structlog.get_logger()


def celopod_calc(values, operator):
    maxy = max(map(len, map(str, values)))
    logger.debug(maxy)

    paded_values = list(map(lambda x: f"{x:0<{maxy}}", values))
    logger.debug(paded_values)
    shifted_values = defaultdict(list)
    for _, value in enumerate(paded_values):
        logger.debug("value", value=value)
        for index, v in enumerate(value):
            logger.debug("v", value=v)
            shifted_values[index].append(v)
    logger.debug(shifted_values)
    inted_values = map(int, ["".join(values) for values in shifted_values.values()])
    problem = operator.join(map(str, inted_values))
    solution = eval(problem)
    logger.debug(f"{problem}={solution}")

    return solution


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
    log.info("day 6 part2")
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
        result += celopod_calc(worksheet[index], operation)

    print(result)
    return f"{result}"
