from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
import re
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

logger = structlog.get_logger()


def part2(values_list) -> str:
    from structlog import get_logger

    logger = get_logger()
    logger.debug("part1")
    data = ""
    result = 0
    for values in values_list:
        data += values

    regex_do = r"do\(\)"
    regex_mul = r"(?:mul\()\d+(?:\,)\d+(?:\))"
    regex_mul2 = r"(\d+)\,(\d+)"
    regex_dont = r"don't\(\)"
    regex_all = f"({regex_mul})|({regex_do})|({regex_dont})"
    matches = re.finditer(regex_all, data)
    do = True
    for match in matches:
        print(match)
        match_group = str(match.group(0))
        print(match_group)
        if match_group.startswith("mul"):
            match_type = "mul"
        elif match_group.startswith("don't"):
            match_type = "dont"
        elif match_group.startswith("do"):
            match_type = "do"

        if match_type == "dont":
            do = False
        elif match_type == "do":
            do = True
        elif do and match_type == "mul":
            values = re.search(regex_mul2, match_group)
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
