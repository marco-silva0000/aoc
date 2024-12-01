from collections import defaultdict
from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

from copy import deepcopy
import networkx as nx
from queue import PriorityQueue

logger = structlog.get_logger()
from collections import deque

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

class TileType(StrEnum):
    GARDEN = "."
    ROCK = "#"

@dataclass()
class Tile:
    point: Point
    kind: TileType
    is_walked: bool = False

    def __hash__(self):
        return hash((self.point, self.kind))

    def get_neighbors(self, grid: 'Grid') -> Iterable[Point]:
        from structlog import get_logger
        logger = get_logger()
        logger.debug("get_neighbors for tile", tile=self)
        for direction in Direction:
            other = direction.as_point
            new_point =  self.point + other
            logger.debug("new_point", new_point=new_point)
            in_grid = new_point in grid
            not_rock = not grid[new_point].kind == TileType.ROCK if in_grid else False
            logger.debug("yielding new_point?", not_rock=not_rock, in_grid=in_grid)
            if in_grid and not_rock:
                logger.debug("yielding new_point.", not_rock=not_rock, in_grid=in_grid)
                yield new_point


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

type Grid = Dict[Point, Tile]


def print_grid(grid: Grid, max_x: int, max_y: int, min_x: int, min_y: int, nodes: List[Point] = []):
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            point = Point(x, y)
            if point in grid:
                if point in nodes:
                    print("O", end="")
                else:
                    tile = grid[point]
                    if tile.kind == TileType.GARDEN:
                        if tile.is_walked:
                            print("X", end="")
                        else:
                            print(".", end="")
                    elif tile.kind == TileType.ROCK:
                        print("#", end="")
            else:
                print(" ", end="")
        print()

def part2(values_list, max_steps=26501365) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )
    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    grid: Grid = dict()
    start = None
    grid_array = open('day-21/input.txt').read().splitlines()

    for y, values in enumerate(values_list):
        for x, value in enumerate(values):
            logger.debug("value", value=value)
            match value:
                case TileType.GARDEN.value:
                    point = Point(x, y)
                    tile = Tile(point=point, kind=TileType.GARDEN)
                case TileType.ROCK.value:
                    point = Point(x, y)
                    tile = Tile(point=point, kind=TileType.ROCK)
                case 'S':
                    start = Point(x, y)
                    point = Point(x, y)
                    tile = Tile(point=start, kind=TileType.GARDEN)
                case _:
                    raise Exception(f"Unknown tile type: {value}")
                
            grid[point] = tile
    assert start is not None
    max_x = max([point.x for point in grid.keys()])
    max_y = max([point.y for point in grid.keys()])
    min_x = min([point.x for point in grid.keys()])
    min_y = min([point.y for point in grid.keys()])

    
    score = 0
    start_state = (score, 0, start)

    graph = nx.Graph()
    graph.add_nodes_from(filter(lambda key: grid[key].kind == TileType.GARDEN, grid.keys()))
    edges_dict_set = defaultdict(set)
    for point, tile in grid.items():
        if tile.kind == TileType.GARDEN:
            for neighbor in tile.get_neighbors(grid):
                edges_dict_set[point].add(neighbor)


    for key, values in edges_dict_set.items():
        graph.add_edges_from([(key, node) for node in values])
    print(graph.edges)
    print("start_edger", graph.edges(start))
    north_graph = deepcopy(graph)
    bfs = nx.bfs_layers(graph, start)
    layers = dict(enumerate(bfs))
    result_set = set()
    # On real output reaches end of grid in 65 steps

    def fill(start: Point, steps: int, print_end=False, wait=False):
        bfs = nx.bfs_layers(graph, start)
        layers = dict(enumerate(bfs))
        result_set = set()
        for k, v in layers.items():
            # print_grid(grid, max_x, max_y, min_x, min_y, nodes=v)
            # print(k, v)
            # print(len(v))
            if k % 2 == 0:
                result_set.update(v)
            if k == steps:
                break
        if print_end:
            print_grid(grid, max_x, max_y, min_x, min_y, nodes=list(result_set))
            if wait:
                input()
        return len(result_set)

    def fill(point: Point, ss):
        grid = grid_array
        sc = point.x
        sr = point.y
        ans = set()
        seen = {(sr, sc)}
        q = deque([(sr, sc, ss)])

        while q:
            r, c, s = q.popleft()

            if s % 2 == 0:
                ans.add((r, c))
            if s == 0:
                continue

            for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]) or grid[nr][nc] == "#" or (nr, nc) in seen:
                    continue
                seen.add((nr, nc))
                q.append((nr, nc, s - 1))
        
        return len(ans)

    assert fill(start, 64) == 3751 # 3751 from prat1

    assert max_x == max_y
    steps = max_steps
    assert len(values_list) == len(values_list[0])
    size = len(values_list)
    print("size", size)
    print("steps % size", steps % size)
    print("size // 2", size // 2)
    print("steps // size", steps // size)
    assert steps % size == size // 2
    total_grids_width = steps // size - 1 # to remove center grid
    odd_grids_width = (total_grids_width // 2 * 2 + 1) ** 2
    even_grids_width = ((total_grids_width + 1) // 2 * 2) ** 2
    print("odd_grids_width", odd_grids_width)
    print("even_grids_width", even_grids_width)

    odd_points = fill(start, size * 2 + 1)
    even_points = fill(start, size * 2)
    print("odd_points", odd_points)
    print("even_points", even_points)
    corner_north_point = Point(start.x, size - 1)
    corner_north_points = fill(corner_north_point, size - 1)
    corner_east_point = Point(0, start.y)
    corner_east_points = fill(corner_east_point, size - 1)
    corner_south_point = Point(start.x, 0)
    corner_south_points = fill(corner_south_point, size - 1)
    corner_west_point = Point(size - 1, start.y)
    corner_west_points = fill(corner_west_point, size - 1)
    print("corner_north_points", corner_north_points)

    small_top_right = Point(0, size - 1)
    small_top_right_points = fill(small_top_right, size // 2 - 1)
    small_top_left = Point(size - 1, size - 1)
    small_top_left_points = fill(small_top_left, size // 2 - 1)
    small_bottom_right = Point(0, 0)
    small_bottom_right_points = fill(small_bottom_right, size // 2 - 1)
    small_bottom_left = Point(size - 1, 0)
    small_bottom_left_points = fill(small_bottom_left, size // 2 - 1)
    
    n_small_grids = total_grids_width + 1

    large_top_right = Point(0, size - 1)
    large_top_right_points = fill(large_top_right, size * 3 // 2 - 1)
    large_top_left = Point(size - 1, size - 1)
    large_top_left_points = fill(large_top_left, size * 3 // 2 - 1)
    large_bottom_right = Point(0, 0)
    large_bottom_right_points = fill(large_bottom_right, size * 3 // 2 - 1)
    large_bottom_left = Point(size - 1, 0)
    large_bottom_left_points = fill(large_bottom_left, size * 3 // 2 - 1)

    n_large_grids = total_grids_width

    result = (
            odd_grids_width * odd_points +
            even_grids_width * even_points +
            corner_north_points + corner_east_points + corner_south_points + corner_west_points +
            n_small_grids * (small_top_right_points + small_top_left_points + small_bottom_right_points + small_bottom_left_points) +
            n_large_grids * (large_top_right_points + large_top_left_points + large_bottom_right_points + large_bottom_left_points)
            )
    # 619284550296772 too low 619366424141158 too low 619407349431158 too low 619407349431167
    print("result", result)
     
    return f"{result}"
  
    

    north_start_point = Point(65, 130)
    north_start_point = Point(65, 130)
    north_bfs = nx.bfs_layers(north_graph, north_start_point)
    north_layers = dict(enumerate(north_bfs))
    result_set = set()
    for k, v in north_layers.items():
        print_grid(grid, max_x, max_y, min_x, min_y, nodes=v)
        input()
        # print(k, v)
        # print(len(v))
        if k % 2 == 0:
            result_set.update(v)
        if len([point for point in v if point.y == 0]) > 0:
            print("found it at step", k)
            break
        # input()
    print_grid(grid, max_x, max_y, min_x, min_y, nodes=list(result_set))
    input()
    result = len(result_set)
    print(result)
    return f"{result}"
    # return f"{result}"

