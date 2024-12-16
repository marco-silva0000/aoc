from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
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

    @property
    def as_arrow(self):
        match self:
            case Direction.NORTH:
                return "^"
            case Direction.SOUTH:
                return "v"
            case Direction.EAST:
                return ">"
            case Direction.WEST:
                return "<"
            case Direction.NORTH_WEST:
                return "\\"
            case Direction.NORTH_EAST:
                return "/"
            case Direction.SOUTH_EAST:
                return "L"
            case Direction.SOUTH_WEST:
                return "J"

    @classmethod
    def from_arrows(cls, c):
        match c:
            case ">":
                return Direction.EAST
            case "<":
                return Direction.WEST
            case "^":
                return Direction.NORTH
            case "v":
                return Direction.SOUTH
            case _:
                raise ValueError(
                    f"can't create Direction from arrow {c} that's not <>^v"
                )


class TileType(StrEnum):
    ROBOT = "@"
    BOX = "O"
    EMPTY = "."
    WALL = "#"


@dataclass()
class Tile:
    tile_type: TileType
    location: Point


def print_grid(
    grid: Dict[Point, Tile],
    max_x: int,
    max_y: int,
    point_list: Optional[List[Point]] = None,
    objs: Optional[List[Tile]] = None,
    filter_frequency: Optional[str] = None,
    origin: Optional[Tile] = None,
):
    # print(rays)
    print("*" * 2)
    word_posititions = set()
    word_map = dict()
    # for word in words:
    #     for point in ray.path:
    #         ray_map[point] = ray
    #         ray_posititions.add(point)
    positions = set()
    _map = dict()
    if objs:
        for obj in objs:
            positions.add(obj.point)
            _map[obj.point] = obj.value
    #
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
            if point_list and point in point_list:
                print("#", end="")
            elif point in positions:
                print(_map[point.point], end="")
            else:
                try:
                    frequency = grid[point].tile_type
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
    log.info("day 15 part1")
    grid: Dict[Point, Tile] = dict()
    in_directions = False
    directions = []
    for y, line in enumerate(values_list):
        if line == "":
            in_directions = True
            max_y = y
        for x, c in enumerate(line):
            if not in_directions:
                logger.debug(c)
                tile_type = TileType(c)
                point = Point(x, y)
                tile = Tile(tile_type, point)
                grid[point] = tile
                if c == "@":
                    start = point
            if in_directions:
                direction = Direction.from_arrows(c)
                directions.append(direction)

    max_x = len(values_list[0])
    min_x = 0
    min_y = 0
    print_grid(grid, max_x, max_y)

    def can_move(point, direction):
        neighbour = point.neighbour_by_direction(direction)
        logger.debug("can move?", point=point, direction=direction, neighbour=neighbour)
        match (neighbour_tile := grid[neighbour]).tile_type:
            case TileType.EMPTY:
                logger.debug(
                    "can, is empty",
                    point=point,
                    direction=direction,
                    neighbour=neighbour,
                )
                return True
            case TileType.WALL:
                logger.debug(
                    "can't, is wall",
                    point=point,
                    direction=direction,
                    neighbour=neighbour,
                )
                return False
            case TileType.BOX:
                logger.debug(
                    "maybe can, is box",
                    point=point,
                    direction=direction,
                    neighbour=neighbour,
                )
                return can_move(neighbour_tile.location, direction)

    def find_moves(point, direction):
        neighbour = point.neighbour_by_direction(direction)
        match (neighbour_tile := grid[neighbour]).tile_type:
            case TileType.EMPTY:
                return [(point, neighbour)]
            case TileType.WALL:
                raise ValueError("can't move box")
            case TileType.BOX:
                return find_moves(neighbour_tile.location, direction) + [
                    (point, neighbour)
                ]
            case _:
                logger.debug(
                    "something else",
                    neighbour_tile=neighbour_tile,
                    point=point,
                    direction=direction,
                )
                raise ValueError("something's broken")

    current = start
    size = len(directions)
    for index, direction in enumerate(directions):
        logger.info(f"{index}/{size}{direction.as_arrow}")
        if can_move(current, direction):
            moves = find_moves(current, direction)
            logger.debug("moves", moves=moves)
            for move in moves:
                logger.debug("will move", move=move)
                origin, destination = move
                origin_tile_type = grid[origin].tile_type
                grid[origin].tile_type = TileType.EMPTY
                grid[destination].tile_type = origin_tile_type
                if origin_tile_type == TileType.ROBOT:
                    current = destination
        print_grid(grid, max_x, max_y)

    result = 0
    for y in range(max_y):
        for x in range(max_x):
            point = Point(x, y)
            if (tile := grid[point]).tile_type == TileType.BOX:
                gps_value = tile.location.x + 100 * tile.location.y
                logger.debug(
                    "value",
                    gps_value=gps_value,
                    point=point,
                    x=tile.location.x,
                    y=tile.location.y * 100,
                )
                result += gps_value
    print(result)
    print(result)
    return f"{result}"
