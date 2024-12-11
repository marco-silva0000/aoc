from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import functools
import numpy as np

import concurrent.futures

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
def rule1_int(stone: int) -> int:
    return 1

@functools.cache
def better_rule2(stone: int, n=int) -> List[int]:
    half = n // 2
    return [stone // 10**half, stone % 10**half]


@functools.cache
def rule2(stone_str: str) -> List[int]:
    half = int(len(stone_str) / 2)
    return [int(stone_str[:half]), int(stone_str[half:])]


@functools.cache
def rule3(stone: int) -> List[int]:
    # return [(stone << 11) - 24]
    return [stone * 2024]


@functools.cache
def transform_stone(stone: int, count: int) -> int:
    if count == 0: # stop counting
        return 1
    elif stone == 0:
        return transform_stone(1, count -1)
    elif (stone_n := len(str(stone))) % 2 == 0:
        half = stone_n // 2
        return transform_stone(stone // 10**half, count-1) + transform_stone(stone % 10**half, count-1)

    return transform_stone(stone * 2024, count - 1)


def transform_old(stones: List[int]):
    """naive aproach, won't work"""
    new_stones = []
    for stone in stones:
        new_stones.extend(transform_stone(stone))
    return new_stones



@functools.cache
def transform(stones: List[int]) -> List[int]:
    """Multithreaded and multiprocess approach"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with concurrent.futures.ProcessPoolExecutor() as process_executor:
            futures = [
                process_executor.submit(transform_stone, stone) for stone in stones
            ]
            new_stones = []
            for future in concurrent.futures.as_completed(futures):
                new_stones.extend(future.result())
    return new_stones

@functools.cache
def process_chunk(chunk: List[int]) -> List[int]:
    new_stones = []
    for stone in chunk:
        new_stones.extend(transform_stone(stone))
    return new_stones

@functools.cache
def transform_new(stones: List[int], chunk_splits: int = 10) -> List[int]:

    chunks = np.array_split(stones, chunk_splits)
    new_stones = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_chunk, chunk) for chunk in chunks]
        for future in concurrent.futures.as_completed(futures):
            new_stones.extend(future.result())

    return new_stones

@functools.cache
def transform_new2(stones: List[int], chunk_splits: int = 10) -> List[int]:
    chunk_size = max(1, len(stones) // chunk_splits)
    chunks = [stones[i:i + chunk_size] for i in range(0, len(stones), chunk_size)]
    new_stones = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_chunk, chunk) for chunk in chunks]
        for future in concurrent.futures.as_completed(futures):
            new_stones.extend(future.result())

    return new_stones

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
    log.info("day 11 part2")
    result = []
    n_blinks = 75
    for index, values in enumerate(values_list):
        stones_og = list(map(int, values.split()))

        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
    result = 0
    for stone in stones_og:
        log.debug(f"stone: {stone}")
        result += transform_stone(stone, n_blinks)
    print(result)
    return f"{result}"


