from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

logger = structlog.get_logger()


@dataclass()
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __neg__(self):
        return Point(x=-self.x, y=-self.y)

    def dist(self, other):
        # manhattan
        return abs(self.x - other.x) + abs(self.y - other.y)

    def move(self, direction: "Direction") -> "Point":
        match direction:
            case Direction.NORTH:
                return Point(x=self.x, y=self.y - 1)
            case Direction.SOUTH:
                return Point(x=self.x, y=self.y + 1)
            case Direction.EAST:
                return Point(x=self.x + 1, y=self.y)
            case Direction.WEST:
                return Point(x=self.x - 1, y=self.y)

    def get_neignbours(
        self,
        directions: Optional[List["Direction"]] = None,
        max_x: Optional[int] = None,
        max_y: Optional[int] = None,
        min_x: Optional[int] = None,
        min_y: Optional[int] = None,
    ) -> Tuple["Point", "Direction"]:
        neighbours = self.get_all_neighbours()
        if directions is not None:
            for direction in directions:
                neighbours = filter(lambda x: x[1] == direction, neighbours)
        if max_x is not None:
            neighbours = filter(lambda n: n[0].x < max_x, neighbours)
        if max_y is not None:
            neighbours = filter(lambda n: n[0].y < max_y, neighbours)
        if min_x is not None:
            neighbours = filter(lambda n: n[0].x >= min_x, neighbours)
        if min_y is not None:
            neighbours = filter(lambda n: n[0].y >= min_y, neighbours)
        return neighbours

    def get_all_neighbours(self) -> Tuple["Point", "Direction"]:
        return [
            (self.north_neighbour(), Direction.NORTH),
            (self.south_neighbour(), Direction.SOUTH),
            (self.east_neighbour(), Direction.EAST),
            (self.west_neighbour(), Direction.WEST),
            (self.north_west_neighbour(), Direction.NORTH_WEST),
            (self.north_east_neighbour(), Direction.NORTH_EAST),
            (self.south_west_neighbour(), Direction.SOUTH_WEST),
            (self.south_east_neighbour(), Direction.SOUTH_EAST),
        ]

    def north_neighbour(self):
        return Point(x=self.x, y=self.y - 1)

    def south_neighbour(self):
        return Point(x=self.x, y=self.y + 1)

    def east_neighbour(self):
        return Point(x=self.x + 1, y=self.y)

    def west_neighbour(self):
        return Point(x=self.x - 1, y=self.y)

    def north_west_neighbour(self):
        return Point(x=self.x - 1, y=self.y - 1)

    def north_east_neighbour(self):
        return Point(x=self.x + 1, y=self.y - 1)

    def south_west_neighbour(self):
        return Point(x=self.x - 1, y=self.y + 1)

    def south_east_neighbour(self):
        return Point(x=self.x + 1, y=self.y + 1)


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    NORTH_WEST = "NW"
    NORTH_EAST = "NE"
    SOUTH_EAST = "SE"
    SOUTH_WEST = "SW"


class Tile(StrEnum):
    EMPTY = "."
    X = "X"
    M = "M"
    A = "A"
    S = "S"


grid: Dict[Point, Tile] = dict()


def print_grid(grid: Dict[Point, Tile], max_x: int, max_y: int, points=[]):
    # print(rays)
    print("*" * 2)
    word_posititions = set()
    word_map = dict()
    # for word in words:
    #     for point in ray.path:
    #         ray_map[point] = ray
    #         ray_posititions.add(point)

    for y in range(max_y):
        for x in range(max_x):
            # tile = grid.get(Point(x, y))
            point = Point(x, y)
            try:
                tile = grid[point]
            except KeyError:
                print("@", end="")
                continue
            if point not in points:
                print(".", end="")
            else:
                print(tile, end="")
            # if tile.type == TileType.EMPTY and point in ray_posititions:
            #     print(ray_map[point], end="")
            # else:
            #     if tile is None:
            #         print(".", end="")
            #     # elif tile.is_energized:
            #     # print("#", end="")
            # else:
            # print(tile, end="")
        print("")


def part1(values_list) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    result = []
    grid = dict()
    for y, line in enumerate(values_list):
        for x, c in enumerate(line):
            tile = Tile(c)
            grid[Point(x, y)] = tile
    max_x = len(values_list[0])
    max_y = len(values_list)
    min_x = 0
    min_y = 0
    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    print_grid(grid, max_x + 1, max_y + 1)
    for y in range(max_y):
        for x in range(max_x):
            x_point = Point(x, y)
            x_tile = grid[x_point]
            if x_tile == Tile.X:
                x_neignbours = x_point.get_neignbours(
                    max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y
                )
                for m_point, direction in x_neignbours:
                    m_tile = grid[m_point]
                    if m_tile == Tile.M:
                        m_neignbours = m_point.get_neignbours(
                            directions=[direction],
                            max_x=max_x,
                            max_y=max_y,
                            min_x=min_x,
                            min_y=min_y,
                        )
                        for a_point, _ in m_neignbours:
                            a_tile = grid[a_point]
                            if a_tile == Tile.A:
                                a_neignbours = a_point.get_neignbours(
                                    directions=[direction],
                                    max_x=max_x,
                                    max_y=max_y,
                                    min_x=min_x,
                                    min_y=min_y,
                                )
                                for s_point, _ in a_neignbours:
                                    s_tile = grid[s_point]
                                    if s_tile == Tile.S:
                                        result.append(
                                            (x_point, m_point, a_point, s_point)
                                        )

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    all_points = []
    for r in result:
        all_points.extend(list(r))
    print_grid(grid, max_x, max_y, points=all_points)
    print(len(result))
    print(len(result))
    print(len(result))
    print(len(result))
    return f"{len(result)}"
