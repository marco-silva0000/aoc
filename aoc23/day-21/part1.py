from collections import defaultdict
from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

import networkx as nx
from queue import PriorityQueue

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

def part1(values_list, max_steps=16) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    grid: Grid = dict()
    start = None
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
    bfs = nx.bfs_layers(graph, start)
    layers = dict(enumerate(bfs))
    result_set = set()
    for k, v in layers.items():
        # print_grid(grid, max_x, max_y, min_x, min_y, nodes=v)
        # print(k, v)
        # print(len(v))
        if k % 2 == 0:
            result_set.update(v)
        if k == max_steps:
            break
        # input()

    print_grid(grid, max_x, max_y, min_x, min_y, nodes=list(result_set))
    input()
    result = len(result_set)
    print(result)
    return f"{result}"

    # bfs = nx.bfs_tree(graph, start, depth_limit=max_steps)

    # print(dict(enumerate(bfs)))
    # print(bfs.edges)
    # print(bfs.nodes)
    # print(len(bfs.edges))
    # print(len(bfs.nodes))
    # descendants = nx.descendants_at_distance(graph, start, max_steps - 1)
    # print(descendants)
    # input()
    # descendants = nx.descendants_at_distance(graph, start, max_steps)
    # print(descendants)
    # input()
    # descendants = nx.descendants_at_distance(graph, start, max_steps + 1)
    # print(descendants)
    # input()

    # q = PriorityQueue()
    # q.put((start_state, grid[start]))
    # final_positions = set()
    # iterations = 0
    # visited = set()
    # while not q.empty():
    #     iterations += 1
    #     logger.debug("queue", q=q.queue)
    #     # input()
    #     # print_grid(grid, max_x, max_y, min_x, min_y)
    #     state = q.get()
    #     (_, steps, point), tile = q.get()
    #     visited.add(point)
    #     if iterations % 1000 == 0:
    #         logger.info("iteration", iterations=iterations, steps=steps, final_positions=len(final_positions), q_len=len(q.queue))
    #     if steps == max_steps:
    #         final_positions.add(point)
    #         continue
    #     for neighbor in tile.get_neighbors(grid):
    #         if neighbor not in visited:
    #             continue
    #         new_tile = grid[neighbor]
    #         new_tile.is_walked = True
    #         new_steps = steps + 1
    #         score = new_steps
    #         new_state = (score, new_steps, neighbor)
    #         # if new_steps < max_steps:
    #         q.put((new_state, new_tile))


    print_grid(grid, max_x, max_y, min_x, min_y)
    walked_tiles = list(filter(lambda x: x.is_walked, grid.values()))
    print(walked_tiles)
    print(final_positions)
    result = len(final_positions)
    print(result)
    return f"{result}"
