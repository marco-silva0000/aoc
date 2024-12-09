from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle, permutations, islice, product
from enum import Enum, StrEnum

logger = structlog.get_logger()


def roundrobin(*iterables):
    "Visit input iterables in a cycle until each is exhausted."
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = cycle(islice(iterators, num_active))
        yield from map(next, iterators)


def ltr(values):
    # print(values)
    if len(values) == 1:
        return int(values[0])
    first = values.pop(0)
    op = values.pop(0)
    second = values.pop(0)
    r = f"{first}{op}{second}"
    # print(r)
    values.insert(0, eval(r))
    return ltr(values)


def part1(values_list) -> str:
    from structlog import get_logger

    logger = get_logger()
    logger.debug("part")
    result = 0
    for values in values_list:
        logger = logger.bind(l=values)
        goal, rest = values.split(": ")
        numbers = rest.split()

        operations = product("+*", repeat=len(numbers) - 1)
        operations = set(operations)
        # print(list(operations))
        for operation_set in operations:
            logger = logger.bind(operation_set=operation_set)
            equation = list(roundrobin(numbers, operation_set))
            if int(goal) == ltr(equation):
                result += int(goal)
                logger.debug("fount match")
                break

    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    print(result)
    return f"{result}"
