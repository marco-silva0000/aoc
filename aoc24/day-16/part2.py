from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import heapq

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
    RAINDEER = "S"
    EMPTY = "."
    WALL = "#"
    GOAL = "E"


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
    path: Optional[List[Tuple[Point, Direction]]] = None,
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
    path_points = []
    path_directions = dict()
    if path:
        for p, direction in path:
            path_points.append(p)
            path_directions[p] = direction

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
            elif point in path_points:
                print(path_directions[point].as_arrow, end="")
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


@dataclass
class Node:
    tile: Tile
    direction: Direction
    parent: "Node"  # 0  # Parent cell's row index
    # f: float  # = float("inf")  # Total cost of the cell (g + h)
    g: float  # = float("inf")  # Cost from start to this cell
    h: float  # = 0  # Heuristic cost from this cell to destination
    n_steps: int
    n_turns: int

    @property
    def cost(self):
        return self.n_steps + self.n_turns * 1000
        return self.g + self.h

    @property
    def n_ticks(self):
        return self.n_steps + self.n_turns

    def __lt__(self, other):
        cost_diff = self.cost < other.cost
        if cost_diff == 0:
            if self.parent is None:
                return -1
            if other.parent is None:
                return 1
            return self.parent < other.parent
        return cost_diff


def astar(grid, start, end, min_x, min_y, max_x, max_y):
    start_node = Node(
        parent=None,
        tile=grid[start],
        direction=Direction.EAST,
        g=0,
        # h=start.dist(end),
        h=1,
        n_steps=0,
        n_turns=0,
    )

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, (start_node.cost, start_node))
    while len(open_list) > 0:
        n_cost, n = heapq.heappop(open_list)
        logger.debug("got n", n=n, n_cost=n_cost)
        closed_list.append(n.tile.location)
        # If the successor is valid, unblocked, and not visited
        for neighbour, direction in n.tile.location.get_orthogonal_neighbours():
            if (
                in_bounds(
                    neighbour,
                    min_x,
                    min_y,
                    max_x,
                    max_y,
                )
                and grid[neighbour].tile_type != TileType.WALL
                and neighbour not in closed_list
            ):
                if n.direction == direction:
                    g = n.cost + 1
                    n_turns = n.n_turns
                elif n.direction == direction.oposite:
                    g = n.cost + 2000 + 1
                    n_turns = n.n_turns + 2
                else:
                    g = n.cost + 1000 + 1
                    n_turns = n.n_turns + 1
                new_node = Node(
                    parent=n,
                    tile=grid[neighbour],
                    direction=direction,
                    g=g,
                    h=1,
                    n_steps=n.n_steps + 1,
                    n_turns=n_turns,
                )
                if neighbour == end:
                    logger.debug("found end", neighbour=neighbour, n=n, node=new_node)
                    return g, new_node
                logger.debug("pushing_node", new_node=new_node)
                heapq.heappush(open_list, (new_node.cost, new_node))
    raise ValueError("could not find path")


def astar_all(grid, start, end, min_x, min_y, max_x, max_y):
    start_node = Node(
        parent=None,
        tile=grid[start],
        direction=Direction.EAST,
        g=0,
        # h=start.dist(end),
        h=1,
        n_steps=0,
        n_turns=0,
    )

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, (start_node.cost, start_node))
    best_path_score = None
    best_path_list = []
    while len(open_list) > 0:
        n_cost, n = heapq.heappop(open_list)
        logger.info("got n", n_tile=n.tile, n_cost=n_cost, len_open=len(open_list))
        closed_list.append((n.tile.location, n.direction))
        # If the successor is valid, unblocked, and not visited
        for neighbour, direction in n.tile.location.get_orthogonal_neighbours():
            if (
                in_bounds(
                    neighbour,
                    min_x,
                    min_y,
                    max_x,
                    max_y,
                )
                and grid[neighbour].tile_type != TileType.WALL
                and (neighbour, direction) not in closed_list
            ):
                if n.direction == direction:
                    g = n.cost + 1
                    n_turns = n.n_turns
                elif n.direction == direction.oposite:
                    g = n.cost + 2000 + 1
                    n_turns = n.n_turns + 2
                else:
                    g = n.cost + 1000 + 1
                    n_turns = n.n_turns + 1
                new_node = Node(
                    parent=n,
                    tile=grid[neighbour],
                    direction=direction,
                    g=g,
                    h=1,
                    n_steps=n.n_steps + 1,
                    n_turns=n_turns,
                )
                if best_path_score is not None:
                    if new_node.cost > best_path_score:
                        continue
                if neighbour == end:
                    logger.info("found end", neighbour=neighbour, n=n)
                    if best_path_score is None:
                        best_path_score = new_node.cost
                    if new_node.cost == best_path_score:
                        best_path_list.append(new_node)
                        logger.debug("pushing_node", new_node=new_node)
                        logger.debug("open_list", open_list=len(open_list))

                else:
                    heapq.heappush(open_list, (new_node.cost, new_node))
    return best_path_list


def get_path(end_node):
    path = []
    current = end_node
    while current is not None:
        path.append((current.tile.location, current.direction))
        current = current.parent
    return path


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
    log.info("day 16 part2")
    grid: Dict[Point, Tile] = dict()
    for y, line in enumerate(values_list):
        for x, c in enumerate(line):
            logger.debug(c)
            tile_type = TileType(c)
            point = Point(x, y)
            tile = Tile(tile_type, point)
            grid[point] = tile
            if c == "S":
                start = point
            if c == "E":
                end = point

    max_x = len(values_list[0])
    max_y = len(values_list)
    print_grid(grid, max_x, max_y)

    min_x = 0
    min_y = 0

    best_path_list = astar_all(grid, start, end, min_x, min_y, max_x, max_y)
    result_nodes = set()
    for node in best_path_list:
        path = get_path(node)
        points = [point for point, _direction in path]
        result_nodes = result_nodes.union(set(points))
        print_grid(grid, max_x, max_y, path=path)
    result = len(result_nodes)
    print(result)
    print(result)
    print(result)
    print(result)
    print(result)
    print(result)
    print(result)
    print(result)
    print(result)
    print(result)
    print(result)
    print(result)
    print(result)
    return f"{result}"
