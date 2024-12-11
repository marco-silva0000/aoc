from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import functools

logger = structlog.get_logger()

bigint = 9223372036854775807


# rules
# If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
# If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
@functools.cache
def rule1(stone: int):
    return [1]


@functools.cache
def wrong_rule2(stone: int) -> List[int]:
    half = int(len(stone) / 2)
    mask_up = bigint << half
    mask_down = ~bigint
    return [stone & mask_up, stone & mask_down]


@functools.cache
def rule2(stone_str: str) -> List[int]:
    half = int(len(stone_str) / 2)
    return [int(stone_str[:half]), int(stone_str[half:])]


@functools.cache
def rule3(stone: int) -> List[int]:
    # return [stone << 11]
    return [stone * 2024]


@functools.cache
def transform_stone(stone: int) -> List[int]:
    if stone == 0:
        return rule1(stone)
    elif len(stone_str := str(stone)) % 2 == 0:
        return rule2(stone_str)
    return rule3(stone)


def transform(stones: List[int]):
    """naive aproach, won't work"""
    new_stones = []
    for stone in stones:
        new_stones.extend(transform_stone(stone))
    return new_stones


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
    log.info("day 11 part1")
    result = []
    n_blinks = 25
    for index, values in enumerate(values_list):
        stones = map(int, values.split())

        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
    for iteration in range(n_blinks):
        stones = transform(stones)
        if iteration < 5:
            print(list(stones))
    result = stones
    print(len(result))
    return f"{len(result)}"
