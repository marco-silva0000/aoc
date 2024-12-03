from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
import re
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

logger = structlog.get_logger()


def part1(values_list) -> str:
    from structlog import get_logger

    logger = get_logger()
    logger.debug("part1")
    result = 0
    for values in values_list:
        data = values
        regex1 = r"(?:mul\()\d+(?:\,)\d+(?:\))"
        regex2 = r"(\d+)\,(\d+)"

        groups = re.findall(regex1, data)
        print(groups)
        for group in groups:
            values = re.search(regex2, group)
            val1 = int(values.group(1))
            val2 = int(values.group(2))
            result += val1 * val2

    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )

    print(result)
    return f"{result}"
