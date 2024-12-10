from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from collections import defaultdict

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

    def x_dist(self, other):
        return self.x - other.x

    def y_dist(self, other):
        return self.y - other.y

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

    def get_neighbours(
        self,
        directions: Optional[List["Direction"]] = None,
        max_x: Optional[int] = None,
        max_y: Optional[int] = None,
        min_x: Optional[int] = None,
        min_y: Optional[int] = None,
        only_orthogonal: Optional[bool] = None,
    ) -> Tuple["Point", "Direction"]:
        if only_orthogonal:
            neighbours = self.get_orthogonal_neighbours()
        else:
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

    def get_orthogonal_neighbours(self) -> Tuple["Point", "Direction"]:
        return [
            (self.north_neighbour(), Direction.NORTH),
            (self.south_neighbour(), Direction.SOUTH),
            (self.east_neighbour(), Direction.EAST),
            (self.west_neighbour(), Direction.WEST),
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

    def generate_oposite_antinodes(self, other):
        result = []
        p1_x = self.x + self.x_dist(other)
        p1_y = self.y + self.y_dist(other)
        p2_x = other.x + other.x_dist(self)
        p2_y = other.y + other.y_dist(self)
        p1 = Point(p1_x, p1_y)
        p2 = Point(p2_x, p2_y)
        logger.debug("antinodes", this=self, other=other, p1=p1, p2=p2)
        result.append(p1)
        result.append(p2)

        for item in result:
            yield item

    def generate_inline_antinodes(self, other, min_x, min_y, max_x, max_y):
        yield self
        yield other
        i = 1
        while True:
            p1_x = self.x + self.x_dist(other) * i
            p1_y = self.y + self.y_dist(other) * i
            p1 = Point(p1_x, p1_y)
            if in_bounds(p1, min_x, min_y, max_x, max_y):
                i += 1
                yield p1
            else:
                break
        i = 1
        while True:
            p2_x = other.x + other.x_dist(self) * i
            p2_y = other.y + other.y_dist(self) * i
            p2 = Point(p2_x, p2_y)
            if in_bounds(p2, min_x, min_y, max_x, max_y):
                i += 1
                yield p2
            else:
                break


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

    @property
    def clockwise(self):
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.WEST:
                return Direction.NORTH
            case Direction.NORTH_WEST:
                return Direction.NORTH_EAST
            case Direction.NORTH_EAST:
                return Direction.SOUTH_EAST
            case Direction.SOUTH_EAST:
                return Direction.SOUTH_WEST
            case Direction.SOUTH_WEST:
                return Direction.NORTH_WEST


@dataclass()
class LavaTile:
    height: int
    location: Point

    def __hash__(self):
        return hash((self.height, self.location))


def print_grid(
    grid: Dict[Point, LavaTile],
    max_x: int,
    max_y: int,
    antinode_list: Optional[List[Point]] = None,
    antennas: Optional[List[LavaTile]] = None,
    filter_frequency: Optional[str] = None,
):
    # print(rays)
    print("*" * 2)
    word_posititions = set()
    word_map = dict()
    # for word in words:
    #     for point in ray.path:
    #         ray_map[point] = ray
    #         ray_posititions.add(point)
    antenna_positions = set()
    antenna_map = dict()
    if antennas:
        for antenna in antennas:
            antenna_positions.add(antenna.point)
            antenna_map[antenna.point] = antenna.frequency

    for x in range(max_x):
        print(format(x, "04x")[0], end="")
    print("")
    for x in range(max_x):
        print(format(x, "04x")[1], end="")
    print("")
    for x in range(max_x):
        print(format(x, "04x")[2], end="")
    print("")
    for x in range(max_x):
        print(format(x, "04x")[3], end="")
    print("")
    for y in range(max_y):
        for x in range(max_x):
            # tile = grid.get(Point(x, y))
            point = Point(x, y)
            if antinode_list and point in antinode_list:
                print("#", end="")
            elif point in antenna_positions:
                print(antenna_map[antenna.point], end="")
            else:
                try:
                    frequency = grid[point].height
                    if filter_frequency is not None:
                        if filter_frequency == frequency:
                            print(frequency, end="")
                        else:
                            print(".", end="")
                    else:
                        print(frequency, end="")
                except KeyError:
                    print(".", end="")
                    continue

            # if tile.type == TileType.EMPTY and point in ray_posititions:
            #     print(ray_map[point], end="")
            # else:
            #     if tile is None:
            #         print(".", end="")
            #     # elif tile.is_energized:
            #     # print("#", end="")
            # else:
            # print(tile, end="")
        print(format(y, "04x"))


def in_bounds(point: Point, min_x, min_y, max_x, max_y):
    return point.x < max_x and point.x >= min_x and point.y < max_y and point.y >= min_y


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
    log.info("day 10 part1")
    result = []
    grid: Dict[Point, LavaTile] = dict()
    trailheads = []
    for y, line in enumerate(values_list):
        for x, c in enumerate(line):
            if c != ".":
                point = Point(x, y)
                tile = LavaTile(int(c), point)
                grid[point] = tile
                if c == "0":
                    trailheads.append(point)

    max_x = len(values_list[0])
    max_y = len(values_list)
    min_x = 0
    min_y = 0
    print_grid(grid, max_x + 1, max_y + 1)

    def find_trailhead_score(
        grid,
        start,
        goal=9,
        max_x: Optional[int] = None,
        max_y: Optional[int] = None,
        min_x: Optional[int] = None,
        min_y: Optional[int] = None,
    ) -> int:
        result = set()
        current_value = grid[start].height
        log.debug(
            f"finding neighbours of {start}", goal=goal, current_value=current_value
        )
        if current_value == goal:
            result.add(start)
            return result
        for neighbour, _direction in start.get_neighbours(
            max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y, only_orthogonal=True
        ):
            if grid[neighbour].height == current_value + 1:
                result = result.union(
                    find_trailhead_score(
                        grid,
                        neighbour,
                        goal=goal,
                        max_x=max_x,
                        max_y=max_y,
                        min_x=min_x,
                        min_y=min_y,
                    )
                )
        return result

    trailhead_scores = []
    for trailhead in trailheads:
        logger.info(f"finding score for {trailhead}")
        matches = find_trailhead_score(
            grid, trailhead, max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y
        )
        logger.debug(f"found {len(matches)}", matches=matches)
        logger.info(f"found {len(matches)}")
        trailhead_scores.append(matches)

    result = sum([len(score) for score in trailhead_scores])
    print(result)
    print("done")
    return f"{result}"
