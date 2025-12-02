from typing import List, Set, Dict, Tuple, Optional, Union
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from more_itertools import grouper

logger = structlog.get_logger()


def is_invalid(id_to_validate: int) -> bool:
    str_id_to_validate = str(id_to_validate)
    logger.debug(f"validating: {str_id_to_validate}")
    len_str_id_to_validate = len(str_id_to_validate)
    middle = len_str_id_to_validate // 2
    for i in range(1, middle + 1):
        set_to_validate = set(grouper(str_id_to_validate, i, fillvalue="x"))
        logger.debug(f"set_to_validate: {set_to_validate}")
        if len(set_to_validate) == 1:
            return True
    return False


def find_invalids(start: int, end: int) -> list[int]:
    result = []
    for id_to_validate in range(start, end + 1):
        if is_invalid(id_to_validate):
            result.append(id_to_validate)
    return result


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
    log.info("day 2 part2")
    result = []
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        ids = values.split(",")
        for start_end in ids:
            start, end = map(int, start_end.split("-"))
            invalids = find_invalids(start, end)
            log.debug(f"start:{start} end:{end} invalids:{invalids}")
            result.extend(invalids)
    print(sum(result))
    return f"{sum(result)}"
