from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from collections import defaultdict
from copy import copy, deepcopy


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

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

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
class Robot:
    id: int
    location: Point
    speed: Point

    def __hash__(self):
        return hash((self.height, self.location))

    def move(self, grid_size_x, grid_size_y):
        initial_location = copy(self.location)
        self.location += self.speed
        if self.location.x >= grid_size_x:
            self.location.x -= grid_size_x
        if self.location.y >= grid_size_y:
            self.location.y -= grid_size_y
        if self.location.x < 0:
            self.location.x += grid_size_x
        if self.location.y < 0:
            self.location.y += grid_size_y
        logger.debug(
            "moved",
            speed=self.speed,
            initial_location=initial_location,
            location=self.location,
        )


def print_image(robots, index, max_x, max_y, blur=True, save_gte=100):
    grid: Dict[Point, List[Robot]] = defaultdict(list)
    for robot in robots:
        grid[robot.location].append(robot)

    from PIL import Image, ImageColor, ImageFilter
    from io import BytesIO

    im = Image.new("1", (max_x, max_y))  # create the Image of size 1 pixel
    for y in range(max_y):
        for x in range(max_x):
            point = Point(x, y)
            n_robots = len(grid[point])
            if n_robots == 0:
                im.putpixel((x, y), ImageColor.getcolor("black", "1"))
            else:
                im.putpixel((x, y), ImageColor.getcolor("green", "1"))
    if blur:
        im = im.filter(ImageFilter.MedianFilter)

    img_file = BytesIO()
    # quality='keep' is a Pillow setting that maintains the quantization of the image.
    # Not having the same quantization can result in different sizes between the in-
    # memory image and the file size on disk.
    im.save(img_file, "png", quality="keep")
    image_file_size = img_file.tell()
    logger.info(image_file_size)
    if image_file_size >= save_gte:
        im.save(f"day-14/renders/{index}.png")  # or any image format


def print_grid(
    grid: Dict[Point, Robot],
    max_x: int,
    max_y: int,
    # antinode_list: Optional[List[Point]] = None,
    robots: Optional[List[Robot]] = [],
    # filter_frequency: Optional[str] = None,
):
    # print(rays)
    print("*" * 2)
    word_posititions = set()
    word_map = dict()
    # for word in words:
    #     for point in ray.path:
    #         ray_map[point] = ray
    #         ray_posititions.add(point)
    # antenna_positions = set()
    # antenna_map = dict()
    # if antennas:
    #     for antenna in antennas:
    #         antenna_positions.add(antenna.point)
    #         antenna_map[antenna.point] = antenna.frequency
    grid: Dict[Point, List[Robot]] = defaultdict(list)
    for robot in robots:
        grid[robot.location].append(robot)

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
            n_robots = len(grid[point])
            if n_robots == 0:
                print(".", end="")
            else:
                print(n_robots, end="")
            # if antinode_list and point in antinode_list:
            #     print("#", end="")
            # elif point in antenna_positions:
            #     print(antenna_map[antenna.point], end="")
            # else:
            #     try:
            #         frequency = grid[point].height
            #         if filter_frequency is not None:
            #             if filter_frequency == frequency:
            #                 print(frequency, end="")
            #             else:
            #                 print(".", end="")
            #         else:
            #             print(frequency, end="")
            # except KeyError:
            #     print(".", end="")
            #     continue

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


def part2(values_list, secconds=10000) -> str:
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
    log.info("day 14 part2")
    result = []
    grid: Dict[Point, List[Robot]] = defaultdict(list)
    robots = []
    grid_size_x = 11
    grid_size_y = 7
    for id, line in enumerate(values_list):
        p, v = line.split(" ")
        p_x, p_y = map(int, p.removeprefix("p=").split(","))
        v_x, v_y = map(int, v.removeprefix("v=").split(","))
        location = Point(p_x, p_y)
        speed = Point(v_x, v_y)
        robot = Robot(id, location, speed)
        grid[location].append(robot)
        robots.append(robot)
        if p_x > 11:
            grid_size_x = 101
            grid_size_y = 103

    max_x = grid_size_x
    max_y = grid_size_y
    min_x = 0
    min_y = 0

    # print_grid(grid, max_x + 1, max_y + 1, robots=robots)

    for i in range(secconds):
        log.info(f"After {i+1} secconds")
        for robot in robots:
            robot.move(grid_size_x, grid_size_y)
        print_image(robots, i, max_x, max_y)
        # print_grid(grid, max_x + 1, max_y + 1, robots=robots)
    # print_grid(grid, max_x + 1, max_y + 1, robots=robots)

    print("done")
    return f""

    def calculate_safety_factor(robots, grid_size_x, grid_size_y):
        half_x = grid_size_x // 2
        half_y = grid_size_y // 2
        # logger.debug("calculating safety", half_x=half_x, half_y=half_y)
        q1_start_x = 0
        q1_end_x = half_x
        q1_start_y = 0
        q1_end_y = half_y
        q2_start_x = half_x + 1
        q2_end_x = grid_size_x
        q2_start_y = 0
        q2_end_y = half_y
        q3_start_x = 0
        q3_end_x = half_x
        q3_start_y = half_y + 1
        q3_end_y = grid_size_y
        q4_start_x = half_x + 1
        q4_end_x = grid_size_x
        q4_start_y = half_y + 1
        q4_end_y = grid_size_y
        q1_start = Point(q1_start_x, q1_start_y)
        q1_end = Point(q1_end_x, q1_end_y)
        q2_start = Point(q2_start_x, q2_start_y)
        q2_end = Point(q2_end_x, q2_end_y)
        q3_start = Point(q3_start_x, q3_start_y)
        q3_end = Point(q3_end_x, q3_end_y)
        q4_start = Point(q4_start_x, q4_start_y)
        q4_end = Point(q4_end_x, q4_end_y)
        q1 = []
        q2 = []
        q3 = []
        q4 = []
        for robot in robots:
            l = robot.location
            # if l > q1_start and l < q1_end:
            #     q1.append(robot)
            # elif l > q2_start and l < q2_end:
            #     q2.append(robot)
            # elif l > q3_start and l < q3_end:
            #     q3.append(robot)
            # elif l > q4_start and l < q4_end:
            #     q4.append(robot)
            if (
                l.x >= q1_start_x
                and l.x < q1_end_x
                and l.y >= q1_start_y
                and l.y < q1_end_y
            ):
                q1.append(robot)
            elif (
                l.x >= q2_start_x
                and l.x < q2_end_x
                and l.y >= q2_start_y
                and l.y < q2_end_y
            ):
                q2.append(robot)
            elif (
                l.x >= q3_start_x
                and l.x < q3_end_x
                and l.y >= q3_start_y
                and l.y < q3_end_y
            ):
                q3.append(robot)
            elif (
                l.x >= q4_start_x
                and l.x < q4_end_x
                and l.y >= q4_start_y
                and l.y < q4_end_y
            ):
                q4.append(robot)
            else:
                logger.debug("robot on border", robot=robot)

        qs = [q1, q2, q3, q4]
        logger.debug(f"{qs}")
        qs_safety = map(len, qs)
        logger.debug(f"{list(qs_safety)}", prod=math.prod(list(qs_safety)))
        logger.debug(len(q1) * len(q2) * len(q3) * len(q4))
        return len(q1) * len(q2) * len(q3) * len(q4)
        return math.prod(qs_safety)

    # result = calculate_safety_factor(robots, grid_size_x, grid_size_y)
    print(result)
    print(result)
    print(result)
    print("done")
    return f"{result}"
