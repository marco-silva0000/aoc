from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

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
    log.info("day 19 part1")
    data = iter(values_list)
    flegs = next(data).split(", ")
    _ = next(data)
    patterns = []
    for pattern in data:
        patterns.append(pattern)
    log.debug(patterns)
    log.debug(flegs)

    valid_paths = []
    for pattern in patterns:
        initial_flegs = filter(lambda x: pattern.startswith(x), flegs)
        options = list(initial_flegs)
        log.debug(f"finding {pattern}", options=options)
        while options:
            option = options.pop(0)
            if option == pattern:
                valid_paths.append(pattern)
                break
            still_valid = filter(lambda x: pattern.startswith(option + x), flegs)
            for valid in still_valid:
                log.debug(
                    f"found valid for option {option}+{valid}",
                    pattern=pattern,
                    option=option,
                )
                options.insert(0, option + valid)

    print(len(valid_paths))
    print(len(valid_paths))
    print(len(valid_paths))
    return f"{len(valid_paths)}"
