from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

logger = structlog.get_logger()

part1_test_pieces = {
    0: """###
##.
##.
""",
    1: """###
##.
.##""",
    2: """.##
###
##.""",
    3: """##.
###
##.""",
    4: """###
#..
###""",
    5: """###
.#.
###""",
}

part1_pieces = {
    0: """#.#
###
##.""",
    1: """#.#
###
#.#""",
    2: """###
..#
###""",
    3: """.##
##.
#..""",
    4: """##.
##.
###""",
    5: """..#
.##
###""",
}


class TileType(StrEnum):
    EMPTY = "."
    GIFT = "#"


@dataclass()
class Region:
    width: int
    length: int
    n_gifts: list[int]


def calc_area(piece):
    return piece.count("#")


def will_it_fit(region: Region, pieces: dict) -> bool:
    total_area = region.width * region.length
    pieces_area = 0
    for index, quantity in enumerate(region.n_gifts):
        piece_area = quantity * calc_area(pieces[index])
        logger.debug("calculating", piece=index, piece_area=piece_area)
        pieces_area += piece_area
    logger.debug("will_it_fit", pieces_area=pieces_area, total_area=total_area)
    return pieces_area * 1.2 <= total_area


def part1(values_list, test=False) -> str:
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
    log.info("day 12 part1")
    if test:
        pieces = part1_test_pieces
    else:
        pieces = part1_pieces
    result = []
    iterator = enumerate(values_list)
    regions = []
    for _ in range(30):
        next(iterator)
    for index, values in iterator:
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        region_hw, region_indexes = values.split(":")
        width, length = map(int, region_hw.split("x"))
        n_gifts = list(map(int, region_indexes.strip().split(" ")))
        region = Region(width, length, n_gifts)
        regions.append(region)
        logger.debug(Region(width, length, n_gifts))

    result = 0
    for region in regions:
        if will_it_fit(region, pieces):
            result += 1

    print(result)
    return f"{result}"
