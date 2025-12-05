from typing import List, Set, Dict, Tuple, Optional, Union
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle

logger = structlog.get_logger()


@dataclass()
class Point:
    x: int
    y: int

    def __lt__(self, other):
        return self.x < other.x

    def __hash__(self):
        return hash((self.x, self.y))

    def wraps(self, other):
        return self.x <= other.x and self.y >= other.y

    def fuse(self, other):
        """
        if they touch, join self and return True, otherwise return false
        """
        logger.debug("fuse?", x0=self.x, y0=self.y, x1=other.x, y1=other.y)
        if self.wraps(other):
            return True
        if self.y >= other.x and self.y <= other.y:
            self.y = other.y
            return True
        return False


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
    log.info("day 5 part2")
    is_in_list = False
    fresh_index = []
    result = 0
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        if not values:
            is_in_list = True
            continue
        if not is_in_list:
            start, end = values.split("-")
            fresh_index.append(Point(int(start), int(end)))
        else:
            break

    old_list = fresh_index
    old_list.sort()
    log.debug("old_list", old_list=old_list)
    new_list = set()
    iterator = iter(old_list)
    current = next(iterator)
    for next_item in iterator:
        log.debug("start", current=current, next_item=next_item)
        log = log.bind(start_x=current.x, start_y=current.y)
        fuse_result = current.fuse(next_item)
        if fuse_result:
            log.debug("fused", current=current, next_item=next_item)
            continue
        else:
            new_list.add(current)
            current = next_item
    new_list.add(current)

    result = 0
    new_list = list(new_list)
    new_list.sort()
    for item in new_list:
        log.info("counting", item=item)
        result += item.y - item.x + 1

    print(result)
    return f"{result}"
