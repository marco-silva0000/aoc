from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import sys
from shapely.geometry import Polygon
from shapely import Point

logger = structlog.get_logger()

class Direction(Enum):
    RIGHT = "R"
    LEFT = "L"
    UP = "U"
    DOWN = "D"

    @property
    def as_point(self) -> 'Point':
        return {
            Direction.RIGHT: Point(1, 0),
            Direction.LEFT: Point(-1, 0),
            Direction.UP: Point(0, -1),
            Direction.DOWN: Point(0, 1),
        }[self]


@dataclass()
class Instruction:
    direction: Direction
    color: Optional[int]
    distance: int

    def walk(self, start_point: Point) -> Point:
        logger.debug("walking", start_point=start_point, instruction=self)
        direction_point = self.direction.as_point

        return Point(direction_point.x * self.distance + start_point.x, direction_point.y * self.distance + start_point.y)


def part2(values_list) -> str:
    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    from structlog import get_logger
    logger = get_logger()
    logger.debug("part2")
    instructions = []
    d = []
    for line in values_list:
        color, _, distance_hex = line.split()
        distance_hex = distance_hex.removeprefix("(#").removesuffix(")")
        distance = int(distance_hex[:-1], 16)
        d.append(distance)
        direction = distance_hex[-1]
        match direction:
            case "0":
                direction = Direction.RIGHT
            case "1":
                direction = Direction.DOWN
            case "2":
                direction = Direction.LEFT
            case "3":
                direction = Direction.UP

        intruction = Instruction(direction=direction, distance=distance, color=color)
        logger.debug("instruction", instruction=intruction)
        instructions.append(intruction)

    start_point = Point(0, 0)
    current_point = start_point
    points = [start_point]
    for instruction in instructions:
        current_point = instruction.walk(current_point)
        points.append(current_point)
    else:
        logger.debug("done all instructions", current_point=current_point, points=points)

    geometry = Polygon(points)
    area = geometry.area
    perimeter = geometry.length
    result = int(perimeter/2 + area + 1)
    print(result)
    return f"{result}"
