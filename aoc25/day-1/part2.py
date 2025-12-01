from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from collections import deque

logger = structlog.get_logger()
class Dial(deque):
    def __init__(self, start, *args, **kwargs):
        self.part1 = 0
        self.part2 = 0
        super().__init__(*args, **kwargs)
        self.rotate(start)

    def rotate_left(self, n: int):
        self.rotate(n)

    def rotate_right(self, n: int):
        self.rotate(n*-1)

    def rotate_n_left(self, n: int):
        for _ in range(n):
            self.rotate_left(1)
            if self[0] == 0:
                self.part2 += 1

    def rotate_n_right(self, n: int):
        for _ in range(n):
            self.rotate_right(1)
            if self[0] == 0:
                self.part2 += 1

    def spin(self, direction, number):
        match direction:
            case "R":
                self.rotate_n_right(number)
            case "L":
                self.rotate_n_left(number)
            case _:
                raise ValueError("Unsuported move")
        if self[0] == 0:
            self.part1 += 1


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
    log.info("day 25 part2")

    dial = Dial(50, range(0,100))

    for index, line in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        letter = line[0]
        number = int(line[1:])
        dial.spin(letter, number)


    print(dial.part2)
    return f"{dial.part2}"
