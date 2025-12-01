from typing import List, Set, Dict, Tuple, Optional, Union
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle

logger = structlog.get_logger()


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
    log.info("day {{day}} part2")
    result = []
    for index, values in enumerate(values_list):
        pass
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
    print(len(result))
    return f"{len(result)}"
