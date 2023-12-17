from typing import List, Set, Dict, Tuple, Optional, Type, Union
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from copy import deepcopy


logger = structlog.get_logger()

# Point = Tuple[int, int]
# Tile = Tuple[str, bool, bool, Optional[bool]]


@dataclass()
class Point:
    x: int
    y: int

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

    def __hash__(self):
        return hash((self.x, self.y))


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class TileType(StrEnum):
    EMPTY = "."
    MIRROR_GRAVE = "\\"
    MIRROR_AGUDO = "/"
    MIRROR_SPLIT_H = "-"
    MIRROR_SPLIT_V = "|"


@dataclass()
class Beam:
    origin: Point
    position: Point
    direction: Direction
    path: List[Point]
    children: List["Beam"]

    def __str__(self):
        match self.direction:
            case Direction.NORTH:
                return f"^"
            case Direction.SOUTH:
                return f"v"
            case Direction.EAST:
                return f">"
            case Direction.WEST:
                return f"<"

    def traverse(self, tile: "Tile", max_x, max_y) -> List["Beam"]:
        path = self.path.copy()
        path.append(self.position)
        match tile.type:
            case TileType.MIRROR_GRAVE:
                match self.direction:
                    case Direction.EAST:
                        new_beam = Beam(
                            origin=self.origin,
                            position=self.position.move(Direction.SOUTH),
                            direction=Direction.SOUTH,
                            path=path,
                            children=[],
                        )
                    case Direction.SOUTH:
                        new_beam = Beam(
                            origin=self.origin,
                            position=self.position.move(Direction.EAST),
                            direction=Direction.EAST,
                            path=path,
                            children=[],
                        )
                    case Direction.WEST:
                        new_beam = Beam(
                            origin=self.origin,
                            position=self.position.move(Direction.NORTH),
                            direction=Direction.NORTH,
                            path=path,
                            children=[],
                        )
                    case Direction.NORTH:
                        new_beam = Beam(
                            origin=self.origin,
                            position=self.position.move(Direction.WEST),
                            direction=Direction.WEST,
                            path=path,
                            children=[],
                        )
            case TileType.MIRROR_AGUDO:
                match self.direction:
                    case Direction.EAST:
                        new_beam = Beam(
                            origin=self.origin,
                            position=self.position.move(Direction.NORTH),
                            direction=Direction.NORTH,
                            path=path,
                            children=[],
                        )
                    case Direction.SOUTH:
                        new_beam = Beam(
                            origin=self.origin,
                            position=self.position.move(Direction.WEST),
                            direction=Direction.WEST,
                            path=path,
                            children=[],
                        )
                    case Direction.WEST:
                        new_beam = Beam(
                            origin=self.origin,
                            position=self.position.move(Direction.SOUTH),
                            direction=Direction.SOUTH,
                            path=path,
                            children=[],
                        )
                    case Direction.NORTH:
                        new_beam = Beam(
                            origin=self.origin,
                            position=self.position.move(Direction.EAST),
                            direction=Direction.EAST,
                            path=path,
                            children=[],
                        )
            case TileType.MIRROR_SPLIT_V:
                match self.direction:
                    case Direction.EAST | Direction.WEST:
                        new_position1 = self.position.move(Direction.NORTH)
                        new_position2 = self.position.move(Direction.SOUTH)
                        new_beam1 = Beam(
                            origin=new_position1,
                            position=new_position1,
                            direction=Direction.NORTH,
                            path=[],
                            children=[],
                        )
                        new_beam2 = Beam(
                            origin=new_position2,
                            position=new_position2,
                            direction=Direction.SOUTH,
                            path=[],
                            children=[],
                        )
                        new_beams = []
                        if (0 <= new_beam1.position.x < max_x) and (
                            0 <= new_beam1.position.y < max_y
                        ):
                            self.children.append(new_beam1)
                            new_beams.append(new_beam1)
                        if (0 <= new_beam2.position.x < max_x) and (
                            0 <= new_beam2.position.y < max_y
                        ):
                            self.children.append(new_beam2)
                            new_beams.append(new_beam2)
                        return new_beams
                    case _:
                        new_beam = Beam(
                            origin=self.origin,
                            position=self.position.move(self.direction),
                            direction=self.direction,
                            path=path,
                            children=[],
                        )
            case TileType.MIRROR_SPLIT_H:
                match self.direction:
                    case Direction.NORTH | Direction.SOUTH:
                        new_position1 = self.position.move(Direction.EAST)
                        new_position2 = self.position.move(Direction.WEST)
                        new_beam1 = Beam(
                            origin=new_position1,
                            position=new_position1,
                            direction=Direction.EAST,
                            path=[],
                            children=[],
                        )
                        new_beam2 = Beam(
                            origin=new_position2,
                            position=new_position2,
                            direction=Direction.WEST,
                            path=[],
                            children=[],
                        )
                        new_beams = []
                        if (0 <= new_beam1.position.x < max_x) and (
                            0 <= new_beam1.position.y < max_y
                        ):
                            self.children.append(new_beam1)
                            new_beams.append(new_beam1)
                        if (0 <= new_beam2.position.x < max_x) and (
                            0 <= new_beam2.position.y < max_y
                        ):
                            self.children.append(new_beam2)
                            new_beams.append(new_beam2)
                        return new_beams
                    case _:
                        new_beam = Beam(
                            origin=self.origin,
                            position=self.position.move(self.direction),
                            direction=self.direction,
                            path=path,
                            children=[],
                        )
            case TileType.EMPTY:
                new_beam = Beam(
                    origin=self.origin,
                    position=self.position.move(self.direction),
                    direction=self.direction,
                    path=path,
                    children=[],
                )
            case _:
                raise Exception("Unknown tile type")
        if 0 <= new_beam.position.x < max_x and 0 <= new_beam.position.y < max_y:
            return [new_beam]
        return []


@dataclass()
class Tile:
    type: TileType
    is_energized: Optional[bool]
    position: Point
    has_been_north: bool = False
    has_been_south: bool = False
    has_been_east: bool = False
    has_been_west: bool = False

    def __str__(self):
        match self.type:
            case TileType.EMPTY:
                return f"."
            case TileType.MIRROR_GRAVE:
                return f"\\"
            case TileType.MIRROR_AGUDO:
                return f"/"
            case TileType.MIRROR_SPLIT_H:
                return f"-"
            case TileType.MIRROR_SPLIT_V:
                return f"|"
            case _:
                raise Exception("Unknown tile type")


grid: Dict[Point, Tile] = dict()

# def get_all_rays(grid: Dict[Point, Tile], max_x: int, max_y: int, rays:List[Beam]) -> List[Beam]:
#     ray_map = dict()
#     for ray in rays:
#         ray_map[ray.position] = ray
#         for point in ray.path:
#             for yaray in get_all_rays(grid, max_x, max_y, ray.children):
#                 ray_map[yaray.position] = yaray


def print_grid(grid: Dict[Point, Tile], max_x: int, max_y: int, rays=[]):
    # print(rays)
    print("*" * 2)
    ray_posititions = set()
    ray_map = dict()
    for ray in rays:
        for point in ray.path:
            ray_map[point] = ray
            ray_posititions.add(point)

    for y in range(max_y):
        for x in range(max_x):
            # tile = grid.get(Point(x, y))
            point = Point(x, y)
            tile = grid[Point(x, y)]
            if tile.type == TileType.EMPTY and point in ray_posititions:
                print(ray_map[point], end="")
            else:
                if tile is None:
                    print(".", end="")
                # elif tile.is_energized:
                # print("#", end="")
                else:
                    print(tile, end="")
        print("")


def part2(values_list) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    result = []
    grid = dict()
    for y, line in enumerate(values_list):
        for x, c in enumerate(line):
            tile = Tile(
                type=TileType(c),
                is_energized=None,
                position=Point(x, y),
            )
            grid[Point(x, y)] = tile
    max_x = len(values_list[0])
    max_y = len(values_list)

    start_beams = []
    for y in range(max_y):
        start_beams.append(
            Beam(
                origin=Point(0, y),
                position=Point(0, y),
                direction=Direction.EAST,
                path=[],
                children=[],
            )
        )
        start_beams.append(
            Beam(
                origin=Point(max_x - 1, y),
                position=Point(max_x - 1, y),
                direction=Direction.WEST,
                path=[],
                children=[],
            )
        )
    for x in range(max_x):
        start_beams.append(
            Beam(
                origin=Point(x, 0),
                position=Point(x, 0),
                direction=Direction.SOUTH,
                path=[],
                children=[],
            )
        )
        start_beams.append(
            Beam(
                origin=Point(x, max_y - 1),
                position=Point(x, max_y - 1),
                direction=Direction.NORTH,
                path=[],
                children=[],
            )
        )
    result = []
    for iter, start_beam in enumerate(start_beams):
        print(f"iter: {iter}/{len(start_beams)}")
        unprocessed_beam_list = [start_beam]
        iter_grid = deepcopy(grid)
        while len(unprocessed_beam_list) > 0:
            # print_grid(grid, max_x, max_y, rays=unprocessed_beam_list)
            beam = unprocessed_beam_list.pop()
            iter_grid[beam.position].is_energized = True
            match beam.direction:
                case Direction.NORTH:
                    if iter_grid[beam.position].has_been_north:
                        continue
                    iter_grid[beam.position].has_been_north = True
                case Direction.SOUTH:
                    if iter_grid[beam.position].has_been_south:
                        continue
                    iter_grid[beam.position].has_been_south = True
                case Direction.EAST:
                    if iter_grid[beam.position].has_been_east:
                        continue
                    iter_grid[beam.position].has_been_east = True
                case Direction.WEST:
                    if iter_grid[beam.position].has_been_west:
                        continue
                    iter_grid[beam.position].has_been_west = True
            # logger.debug(beam)
            tile = iter_grid[beam.position]
            # logger.debug(beam, direction=beam.direction, position=beam.position, path=beam.path, tile=tile)
            new_beams = beam.traverse(tile, max_x, max_y)
            # logger.debug(new_beams)
            unprocessed_beam_list.extend(new_beams)
            # print(len(unprocessed_beam_list))
        result.append([tile.is_energized for tile in iter_grid.values()].count(True))

    # print_grid(grid, max_x, max_y, rays=[start_beam])

    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    print(result)
    print(max(result))
    return f"{max(result)}"
