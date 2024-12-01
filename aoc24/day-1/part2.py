from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from collections import Counter

logger = structlog.get_logger()


def part2(values_list) -> str:
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
    counter = Counter(second_list)
    result = 0
    for val in first_list:
        result += int(val) * counter[val]
    return f"{result}"
