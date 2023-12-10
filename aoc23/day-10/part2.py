from typing import List, Set, Dict, Tuple, Optional, Union, Self
import logging
import math
from structlog import get_logger
from dataclasses import dataclass
from itertools import cycle

log = get_logger()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    GOLD = '\033[0;33;46m'
    RED = '\033[0;36;44m'
    BLU = '\033[0;36;47m'
    UNDERLINE = '\033[4m'

## Direction str enum
from enum import StrEnum, Enum
class Direction(StrEnum):
    NORTH = "U"
    NORTHSOUTH = "|"
    SOUTH = "D"
    EAST = "E"
    WEST = "W"
    EASTWEST = "-"
    NORTHEAST = "L"
    NORTHWEST = "J"
    SOUTHWEST = "7"
    SOUTHEAST = "F"
    GROUND = "."
    START = "S"

    def __str__(self):
        if self == Direction.NORTHSOUTH:
            return "│"
        elif self == Direction.EASTWEST:
            return "─"
        elif self == Direction.NORTHEAST:
            return "└"
        elif self == Direction.NORTHWEST:
            return "┘"
        elif self == Direction.SOUTHWEST:
            return "┐"
        elif self == Direction.SOUTHEAST:
            return "┌"
        elif self == Direction.GROUND:
            return "·"
        elif self == Direction.GROUND:
            return "·"
        elif self == Direction.START:
            return "x"
        return self.value

    # @classmethod
    # def from_string(cls, s):
    #     for finger in cls:
    #         if finger.value[1] == s:
    #             return finger
    #     raise ValueError(cls.__name__ + ' has no value matching "' + s + '"')



Point = Tuple[int, int]

@dataclass
class PointAttr:
    x: int
    y: int
    c: str
    direction: Direction
    is_pipe: Optional[bool] = None
    is_loop: bool = False
    dist_from_start: Optional[int] = None
    touched_by_light: Optional[bool] = None

    def neighbours(self):
        if self.direction == Direction.NORTHSOUTH:
            return [
                (self.x, self.y - 1),
                (self.x, self.y + 1),
            ]
        elif self.direction == Direction.EASTWEST:
            return [
                (self.x - 1, self.y),
                (self.x + 1, self.y),
            ]
        elif self.direction == Direction.NORTHEAST:
            return [
                (self.x, self.y - 1),
                (self.x + 1, self.y),
            ]
        elif self.direction == Direction.NORTHWEST:
            return [
                (self.x, self.y - 1),
                (self.x - 1, self.y),
            ]
        elif self.direction == Direction.SOUTHWEST:
            return [
                (self.x, self.y + 1),
                (self.x - 1, self.y),
            ]
        elif self.direction == Direction.SOUTHEAST:
            return [
                (self.x, self.y + 1),
                (self.x + 1, self.y),
            ]
        return [
            (self.x, self.y - 1),
            (self.x + 1, self.y),
            (self.x, self.y + 1),
            (self.x - 1, self.y),
        ]

    def pipe_neighbours(self, grid: Dict[Point, Self]):
        if self.direction == Direction.START: # hardcoded hack insead of identifying start
            self.direction = Direction.NORTHSOUTH
        return list(filter(lambda p: p.is_pipe and p.dist_from_start is None, map(lambda p: grid[p], [n for n in self.neighbours() if n in grid.keys()])))

Grid = Dict[Point, PointAttr]


def print_map(grid: Grid, dists=False, points_enclosed=[]):
    max_x = max(map(lambda p: p[0], grid.keys()))
    max_y = max(map(lambda p: p[1], grid.keys()))
    log.debug("points_enclosed", points_enclosed=points_enclosed)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            p = (x, y)
            if p in grid:
                if grid[p].dist_from_start is not None:
                    if dists:
                        print(grid[p].dist_from_start % 9, end="")
                    else:
                        print(f"{bcolors.GOLD}{grid[p].direction}{bcolors.ENDC}", end="")
                else:
                    if p in points_enclosed:
                        print(f"{bcolors.BLU}{grid[p].direction}{bcolors.ENDC}", end="")
                    else:
                        if grid[p].touched_by_light:
                            print(f"{bcolors.BLU}{grid[p].direction}{bcolors.ENDC}", end="")
                        else:
                            print(f"{grid[p].direction}", end="")
            else:
                print(" ", end="")
        print()



def part2(values_list) -> str:
    grid: Grid = dict()
    for y, l in enumerate(values_list):
        for x, c in enumerate(l):
            is_pipe = c != "." or c == "S"
            direction = Direction(c)
            grid[(x, y)] = PointAttr(
                    x,
                    y,
                c,
                direction,
                is_pipe,
            )
    print_map(grid)
    start_point = list(filter(lambda p: grid[p].direction == Direction.START, grid.keys()))[0]
    start = grid[start_point]
    log.debug(start, start_point=start_point)
    start.dist_from_start = 0
    next_neighbours = list([(n, start.dist_from_start) for n in start.pipe_neighbours(grid)])
    queue = []
    queue.extend(next_neighbours)
    while len(queue) > 0:
        # print_map(grid, dists=True)
        # log.debug("queue", queue=queue)
        current, prev_dist = queue.pop(0)
        # log.debug(current)
        current.dist_from_start = prev_dist + 1
        next_neighbours = list([(n, current.dist_from_start) for n in current.pipe_neighbours(grid)])
        queue.extend(next_neighbours)

    print_map(grid, dists=True)
    print_map(grid, dists=False)
    mapped_values = list(filter(lambda p: p.dist_from_start is not None, grid.values()))
    min_x_mapped = min(map(lambda p: p.x, mapped_values))
    max_x_mapped = max(map(lambda p: p.x, mapped_values))
    min_y_mapped = min(map(lambda p: p.y, mapped_values))
    max_y_mapped = max(map(lambda p: p.y, mapped_values))
    log.debug("will scan in boundry", min_x_mapped=min_x_mapped, max_x_mapped=max_x_mapped, min_y_mapped=min_y_mapped, max_y_mapped=max_y_mapped)
    points_enclosed = []
    for y in range(min_y_mapped -1 , max_y_mapped + 1):
        for x in range(min_x_mapped-1 , max_x_mapped + 1):
            p = (x, y)
            if p in grid:
                if grid[p].dist_from_start is None:  # is not part of loop
                    grid[p].touched_by_light = True
                else:
                    break
        for x in range(max_x_mapped + 1, min_x_mapped-1 , -1):
            p = (x, y)
            if p in grid:
                if grid[p].dist_from_start is None:  # is not part of loop
                    grid[p].touched_by_light = True
                else:
                    break
                    
    for x in range(min_x_mapped -1 , max_x_mapped + 1):
        for y in range(min_y_mapped -1 , max_y_mapped + 1):
            p = (x, y)
            if p in grid:
                if grid[p].dist_from_start is None:
                    grid[p].touched_by_light = True
                else:
                    break
        for y in range(max_y_mapped + 1, min_y_mapped -1 , -1):
            p = (x, y)
            if p in grid:
                if grid[p].dist_from_start is None:
                    grid[p].touched_by_light = True
                else:
                    break

    maybe_enclosed = list(filter(lambda p: p.dist_from_start is None and not p.touched_by_light, grid.values()))
    for p in maybe_enclosed:
        # log.debug("maybe_enclosed", p=p)
        count = 0
        for test_x in range(0, p.x):
            test_p = (test_x, p.y)
            # log.debug("test_p", test_p=test_p, dist_from_start=grid[test_p].dist_from_start, direction=str(grid[test_p].direction))
            if test_p in grid and grid[test_p].dist_from_start is not None and grid[test_p].direction in [Direction.NORTHSOUTH, Direction.NORTHEAST, Direction.NORTHWEST]:
                count += 1
                # log.debug("found barrier", p=p, test_p=test_p, count=count)

        if count > 0 and count % 2 == 1:
            # log.debug("enclosed", p=p, count=count)
            points_enclosed.append((p.x, p.y))

    print_map(grid, points_enclosed=points_enclosed)
    result = len(points_enclosed)
    # log.debug("result", result=result, points_enclosed=points_enclosed)


    return str(result)
