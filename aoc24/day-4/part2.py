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
            neighbours = filter(lambda x: x[1] in directions, neighbours)
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

    def neighbour_by_direction(self, direction: "Direction") -> "Point":
        match direction:
            case Direction.NORTH:
                return self.north_neighbour()
            case Direction.SOUTH:
                return self.south_neighbour()
            case Direction.EAST:
                return self.east_neighbour()
            case Direction.WEST:
                return self.west_neighbour()
            case Direction.NORTH_WEST:
                return self.north_west_neighbour()
            case Direction.NORTH_EAST:
                return self.north_east_neighbour()
            case Direction.SOUTH_EAST:
                return self.south_east_neighbour()
            case Direction.SOUTH_WEST:
                return self.south_west_neighbour()


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    NORTH_WEST = "NW"
    NORTH_EAST = "NE"
    SOUTH_EAST = "SE"
    SOUTH_WEST = "SW"

    @property
    def oposite(self):
        match self:
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.NORTH
            case Direction.EAST:
                return Direction.WEST
            case Direction.WEST:
                return Direction.EAST
            case Direction.NORTH_WEST:
                return Direction.SOUTH_EAST
            case Direction.NORTH_EAST:
                return Direction.SOUTH_WEST
            case Direction.SOUTH_EAST:
                return Direction.NORTH_WEST
            case Direction.SOUTH_WEST:
                return Direction.NORTH_EAST


class Tile(StrEnum):
    EMPTY = "."
    X = "X"
    M = "M"
    A = "A"
    S = "S"


grid: Dict[Point, Tile] = dict()


def print_grid(
    grid: Dict[Point, Tile],
    max_x: int,
    max_y: int,
    points: Optional[List[Point]] = None,
):
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
            if points is not None and point not in points:
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

        """finds MAS, not X-MAS"""
        # for n_point, direction in a_neignbours:
        #     n_tile = grid[n_point]
        # if n_tile == Tile.M:
        #     maybe_s_neignbours = a_point.get_neignbours(
        #         directions=[direction.oposite],
        #         max_x=max_x,
        #         max_y=max_y,
        #         min_x=min_x,
        #         min_y=min_y,
        #     )
        #     for s_point, _ in maybe_s_neignbours:
        #         s_tile = grid[s_point]
        #         if s_tile == Tile.S:
        #             valid_mas = (n_point, a_point, s_point)
        #             print("found MAS1 in:")
        #             print_grid(grid, max_x, max_y, points=valid_mas)
        #             result.append(valid_mas)
        # elif n_tile == Tile.S:
        #     maybe_m_neignbours = a_point.get_neignbours(
        #         directions=[direction.oposite],
        #         max_x=max_x,
        #         max_y=max_y,
        #         min_x=min_x,
        #         min_y=min_y,
        #     )
        #     for m_point, _ in maybe_m_neignbours:
        #         m_tile = grid[m_point]
        #         if m_tile == Tile.M:
        #             valid_mas = (m_point, a_point, n_point)
        #             print("found MAS2 in:")
        #             print_grid(grid, max_x, max_y, points=valid_mas)
        #             result.append(valid_mas)


def part2(values_list) -> str:
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
            a_point = Point(x, y)
            a_tile = grid[a_point]
            if a_tile == Tile.A:
                directions = [
                    Direction.NORTH_WEST,
                    Direction.NORTH_EAST,
                    Direction.SOUTH_WEST,
                    Direction.SOUTH_EAST,
                ]
                a_neignbours = list(
                    a_point.get_neignbours(
                        max_x=max_x,
                        max_y=max_y,
                        min_x=min_x,
                        min_y=min_y,
                        directions=directions,
                    )
                )
                # print("found A in:")
                # print(a_neignbours)
                # print_points = []
                # for neighbour in a_neignbours:
                #     print_point, d = neighbour
                #     print_points.append(print_point)
                # print_points.append(a_point)
                # print(print_points)
                # print_grid(
                #     grid,
                #     max_x,
                #     max_y,
                #     points=print_points,
                # )
                mas = []
                for m_point, direction in a_neignbours:
                    m_tile = grid[m_point]
                    if m_tile == Tile.M:
                        potential_s = a_point.neighbour_by_direction(direction.oposite)
                        try:
                            oposite_tile = grid[potential_s]
                        except KeyError:
                            continue
                        if oposite_tile == Tile.S:
                            s_point = potential_s
                            valid_mas = (m_point, a_point, s_point)
                            # print("found MAS in:")
                            # print(mas)
                            # print_grid(grid, max_x, max_y, points=valid_mas)
                            mas.append((valid_mas))

                if len(mas) == 2:
                    result.append(mas)

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    all_points = []
    for r in result:
        for mas in r:
            all_points.extend(list(mas))
    print_grid(grid, max_x, max_y, points=all_points)
    print(len(result))
    print(len(result))
    print(len(result))
    print(len(result))
    return f"{len(result)}"
