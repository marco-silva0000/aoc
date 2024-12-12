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
class Plant:
    value: str
    location: Point

    def __hash__(self):
        return hash((self.value, self.location))


def print_grid(
    grid: Dict[Point, Plant],
    max_x: int,
    max_y: int,
    point_list: Optional[List[Point]] = None,
    objs: Optional[List[Plant]] = None,
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
                    frequency = grid[point].value
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


def spread(grid, plant, min_x=None, min_y=None, max_x=None, max_y=None, visited=set()):
    logger.debug("spreading", plant=plant, visited=visited)

    def plant_filter(p):
        logger.debug(
            f"filtering {p}, {grid[p[0]].value} == {plant.value}",
            plant=plant,
            visited=visited,
            p_0=p[0],
            not_in_visited=p[0] not in visited,
        )
        return grid[p[0]].value == plant.value and p[0] not in visited

    result = set()
    result.add(plant.location)
    visited.add(plant.location)
    new_neighbours = []
    for neighbour, _ in filter(
        plant_filter,
        plant.location.get_neighbours(
            min_x=min_x,
            min_y=min_y,
            max_x=max_x,
            max_y=max_y,
            only_orthogonal=True,
        ),
    ):
        logger.debug("found neighbour", neighbour=neighbour, location=plant.location)
        result.add(neighbour)
        new_neighbours.append(neighbour)

    for neighbour in new_neighbours:
        neighbour_plant = grid[neighbour]
        result = result.union(
            spread(
                grid,
                neighbour_plant,
                min_x=min_x,
                min_y=min_y,
                max_x=max_x,
                max_y=max_y,
                visited=visited,
            )
        )
    return result


def identify_regions(grid, min_x, min_y, max_x, max_y):
    added_to_region = set()
    regions = []
    for y in range(max_y):
        for x in range(max_x):
            point = Point(x, y)
            plant = grid.get(point)
            if plant.location not in added_to_region:
                logger.debug(
                    "location not in visited",
                    plant=plant,
                    added_to_region=added_to_region,
                )
                current_region = plant.value
                region = spread(
                    grid,
                    plant,
                    min_x=min_x,
                    min_y=min_y,
                    max_x=max_x,
                    max_y=max_y,
                )
                regions.append(
                    (
                        current_region,
                        region,
                    )
                )
                logger.debug("found region", region=region)
                added_to_region = added_to_region.union(region)
                # raise Exception
    logger.debug(f"identified {len(regions)}")
    return regions


def calc_area(region):
    return len(region)


def calc_perimeter(
    region,
    grid,
    min_x=None,
    min_y=None,
    max_x=None,
    max_y=None,
):
    def filter_valid_perim(p):
        pos = p[0]
        try:
            return grid[p[0]].value != grid[position].value
        except KeyError:
            return True

    result = 0
    for position in region:
        result += len(
            list(
                filter(
                    filter_valid_perim,
                    position.get_neighbours(
                        only_orthogonal=True,
                    ),
                )
            )
        )
    return result


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
    log.info("day 12 part1")
    result = []
    grid: Dict[Point, Plant] = dict()
    for y, line in enumerate(values_list):
        for x, c in enumerate(line):
            if c != ".":
                point = Point(x, y)
                tile = Plant(c, point)
                grid[point] = tile

    max_x = len(values_list[0])
    max_y = len(values_list)
    min_x = 0
    min_y = 0
    regions = identify_regions(grid, min_x, min_y, max_x, max_y)
    print_grid(grid, max_x + 1, max_y + 1)
    result = 0
    for region in regions:
        print_grid(grid, max_x + 1, max_y + 1, point_list=region[1])
        perimeter = calc_perimeter(region[1], grid, min_x, min_y, max_x, max_y)
        area = calc_area(region[1])
        log.debug(
            f"calculating for region {region[0]}, perimeter: {perimeter} * {area} :area = {perimeter*area}"
        )
        result += perimeter * area
    print(result)
    print(result)
    print(result)
    print(result)
    return f"{result}"
