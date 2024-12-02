from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import numpy as np

logger = structlog.get_logger()


def part1(values_list) -> str:
    from structlog import get_logger

    logger = get_logger()
    logger.debug("part 1")
    result = []
    for values in values_list:
        structlog.contextvars.bind_contextvars(
            iteration=values,
        )
        line = np.array(values.split(), dtype=np.int32)
        logger.debug(f"line: {line}")
        diff = np.diff(line)
        logger.debug(f"diff: {diff}")
        no_greater_than_3 = np.all(np.abs(diff) <= 3)
        all_positive = np.all(diff > 0)
        all_negative = np.all(diff < 0)
        any_constant = np.any(diff == 0)
        is_monotonic = all_positive | all_negative
        logger.debug(
            f"no_greater_than_3: {no_greater_than_3}, is_monotonic: {is_monotonic}, not any_constant: {not any_constant}"
        )
        if no_greater_than_3 and is_monotonic and not any_constant:
            result.append(True)

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    logger.debug(f"result: {len(result)}")
    return str(len(result))
