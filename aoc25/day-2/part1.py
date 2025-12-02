from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

logger = structlog.get_logger()


def is_invalid(id_to_validate: int) -> bool:
    str_id_to_validate = str(id_to_validate)
    len_str_id_to_validate = len(str_id_to_validate)
    if len_str_id_to_validate % 2 != 0:
        return False
    middle_end = len_str_id_to_validate // 2
    middle_out = middle_end + len_str_id_to_validate % 2
    first = str_id_to_validate[0:middle_end]
    second = str_id_to_validate[middle_out:]
    return first == second


def find_invalids(start: int, end: int) -> list[int]:
    result = []
    for id_to_validate in range(start, end + 1):
        if is_invalid(id_to_validate):
            result.append(id_to_validate)
    return result


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
    log.info("day 2 part1")
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
