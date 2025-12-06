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
    shifted_values = defaultdict(list)
    for _, value in enumerate(values):
        logger.debug("value", value=value)
        for index, v in enumerate(value):
            logger.debug("v", value=v)
            shifted_values[index].append(v)
    logger.debug(shifted_values)
    inted_values = map(
        int, ["".join(values).replace("•", "") for values in shifted_values.values()]
    )
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
    logger.debug(values_list[-1])
    for iteration, values in enumerate(values_list):
        logger.debug(values)
    cut_indexes = []
    operations = iter(values_list[-1])
    next(operations)
    new_values_list = []
    for index, c in enumerate(operations):
        if c != " ":
            cut_indexes.append(index)
    logger.debug("cut", cut_indexes=cut_indexes)
    for iteration, values in enumerate(values_list[:-1]):
        paded_values = values.replace(" ", "•")
        logger.debug("paded_values", paded_values=paded_values)
        paded_values_copy = ""
        for index, c in enumerate(paded_values):
            if index not in cut_indexes:
                paded_values_copy += c
            else:
                paded_values_copy += " "

        logger.debug("paded_values_copy", paded_values_copy=paded_values_copy)
        new_values_list.append(paded_values_copy)

    for iteration, values in enumerate(new_values_list):
        logger.debug(values)
        for index, value in enumerate(values.split()):
            worksheet[index].append(value)
    logger.debug(worksheet)
    for index, operation in enumerate(values_list[-1].split()):
        logger.debug(worksheet[index])
        result += celopod_calc(worksheet[index], operation)

    print(result)
    return f"{result}"
