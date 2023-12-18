from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import sys
sys.setrecursionlimit(100000)

logger = structlog.get_logger()

class Direction(Enum):
    RIGHT = "R"
    LEFT = "L"
    UP = "U"
    DOWN = "D"

    @property
    def as_point(self) -> 'Point':
        return {
            Direction.RIGHT: Point(x=1, y=0),
            Direction.LEFT: Point(x=-1, y=0),
            Direction.UP: Point(x=0, y=-1),
            Direction.DOWN: Point(x=0, y=1),
        }[self]


@dataclass()
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __add__(self, other) -> 'Point':
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __neg__(self):
        return Point(x=-self.x, y=-self.y)

    def dist(self, other):
        # manhattan
        return abs(self.x - other.x) + abs(self.y - other.y)

    def get_neighbors(self) -> Iterable['Point']:
        return (
            self + Direction.UP.as_point,
            self + Direction.DOWN.as_point,
            self + Direction.LEFT.as_point,
            self + Direction.RIGHT.as_point,
        )


@dataclass()
class Tile:
    point: Point
    color: Optional[int]
    dug: bool = False

    @property
    def is_edge(self):
        return self.color is not None

    def dig(self, grid: 'Grid', color=0):
        self.color = color
        self.dug = True
        grid[self.point] = self


type Grid = Dict[Point, Tile] 


@dataclass()
class Instruction:
    direction: Direction
    color: Optional[int]
    distance: int

    def dig(self, grid: Grid, start: Point) -> Point:
        from structlog import get_logger
        logger = get_logger()
        logger.debug("dig", grid_size=len(grid.keys()))
        current_point = start
        logger = logger.bind(start=start)
        for _ in range(self.distance):
            point = current_point + self.direction.as_point
            logger = logger.bind(point=point)
            tile = Tile(point=current_point, dug=True, color=self.color if self.color is not None else 0)
            grid[point] = tile
            current_point = point
            logger.debug("dug", tile=tile, current_point=current_point, grid=grid[point])
        logger.debug("done", current_point=current_point, grid_size=len(grid.keys()))
        return current_point


def dig_in(grid: Grid, start: Tile, min_x: int, min_y: int, max_x: int, max_y: int):
    # flood fill

    from structlog import get_logger
    logger = get_logger()
    logger.debug("flood_fill", grid_size=len(grid.keys()))
    if not start.dug:
        start.dig(grid)
        grid[start.point] = start
    for neighbor in start.point.get_neighbors():
        logger.debug("neighbor", neighbor=neighbor)
        if neighbor not in grid.keys():
            if (min_x < neighbor.x < max_x) and (min_y < neighbor.y < max_y):
                logger.debug("in if")
                try:
                    neighbor_tile = grid[neighbor]
                    logger.debug("already dug")
                    continue # already dug
                except KeyError:
                    logger.debug("not dug yet")
                    neighbor_tile = Tile(point=neighbor, color=0)
                    logger.debug("neighbor_tile", neighbor_tile=neighbor_tile)
                    dig_in(grid, neighbor_tile, min_x, min_y, max_x, max_y)


def print_grid(grid: Grid, min_x: int, min_y: int, max_x: int, max_y: int):
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            point = Point(x, y)
            tile = grid.get(point, Tile(point=point, color=None))
            if tile.color is None:
                print(" ", end="")
            elif tile.color == 0:
                print("X", end="")
            else:
                print("#", end="")
        print()


def part1(values_list, fillx=1, filly=1) -> str:
    input()
    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    from structlog import get_logger
    logger = get_logger()
    logger.debug("part1")
    grid = dict()
    instructions = []
    for line in values_list:
        direction, distance, color = line.split()
        distance = int(distance)
        color = int(color.removeprefix("(#").removesuffix(")"), 16)
        intruction = Instruction(direction=Direction(direction), distance=distance, color=color)
        logger.debug("instruction", instruction=intruction)
        instructions.append(intruction)

    print(instructions)

    start_point = Point(0, 0)
    current_point = start_point
    for instruction in instructions:
        # grid, current_point = instruction.dig(grid, current_point)
        current_point = instruction.dig(grid, current_point)
    else:
        logger.debug("done all instructions", current_point=current_point, last_tile=grid[current_point],grid_size=len(grid.keys()))


    max_x = max(grid.keys(), key=lambda p: p.x).x
    max_y = max(grid.keys(), key=lambda p: p.y).y
    min_x = min(grid.keys(), key=lambda p: p.x).x
    min_y = min(grid.keys(), key=lambda p: p.y).y

    center_point = Point(math.floor((max_x - min_x) / 2), math.floor((max_y - min_y) / 2))

    logger.debug("max", min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)

    print_grid(grid, min_x, min_y, max_x, max_y)

    start_point = center_point
    while start_point in grid:
        start_point += Point(1, 1)
    start_tile = Tile(point=Point(fillx, filly), color=0)
    input()
    try:
        dig_in(grid, start_tile, min_x, min_y, max_x, max_y)
    except RecursionError:
        print_grid(grid, min_x, min_y, max_x, max_y)
        raise

    print_grid(grid, min_x, min_y, max_x, max_y)

    grid_size = len(grid.keys())
    logger.debug("done digging in", grid_size=grid_size)

    print(grid_size)
    # return ""
    return f"{grid_size}"
