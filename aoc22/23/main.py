from collections import defaultdict
from threading import current_thread

from defaultlist import defaultlist
import itertools
from pickle import NONE
from typing import List, Dict, Tuple
from itertools import chain, groupby, cycle
from sympy import symbols, Eq, solve
from enum import Enum


Point = Tuple[int, int]


class Tile(str, Enum):
    EMPTY = '🌫️'
    FLOOR = "🟦"
    BLOCKED = "🗿"


class Move(str, Enum):
    NORTH = "👆"
    NORTHEAST = "🏹"
    EAST = "👉"
    SOUTHEAST = "🛩"
    SOUTH = "👇"
    SOUTHWEST = "🏄"
    WEST = "👈"
    NORTHWEST = "💘"

DIRECTIONS = [Move.NORTH, Move.SOUTH, Move.WEST, Move.EAST]

Grid = Dict[Point, (Tile | Move)]


class Elf():
    def __init__(self, position: Point) -> None:
        self.position = position
        self.moving_options = cycle(DIRECTIONS)

    def adjacent_positions(self):
        options = [-1, 0, 1]
        result = []
        xx, yy = self.position
        for x in options:
            for y in options:
                if (x, y) == (0, 0):
                    continue
                result.append((x+xx, y+yy))
        return result

    def propose_move(self, grid) -> Point:
        next_move = next(self.moving_options)
        if not any([grid[position] != Tile.EMPTY for position in self.adjacent_positions()]):
            return self.position
        match next_move:
            case Move.NORTH:
                pass
            case Move.SOUTH:
                pass
            case Move.WEST:
                pass
            case Move.EAST:
                pass
        return self.position


    @property
    def value(self):
        return "🧝"
    

def print_grid(grid: Dict[Point, (Elf| Tile)], player=None, min_x=None, max_x=None, min_y=None, max_y=None):
    x_points = list(set([x for x, _ in grid.keys()]))
    x_points.sort()
    y_points = list(set([y for _, y in grid.keys()]))
    y_points.sort()
    if min_x is None:
        min_x = min(x_points, default=0)
    if max_x is None:
        max_x = max(x_points, default=1)
    if min_y is None:
        min_y = min(y_points, default=0)
    if max_y is None:
        max_y = max(y_points, default=1)
    point = None
    if player:
        point = player.position
    for y in range(min_y-2, max_y+2):
        print(f"{y:03}:", end="")
        for x in range(min_x-2, max_x+2):
            try:
                value = grid[(x, y)].value
            except KeyError:
                value = Tile.EMPTY.value
            if (x,y) == (0, 0):
                value = "🌌"
            if player and (x,y) == point:
                value = player.direction.value
            print(value, end="")
        print("")
    print("")

grid: Dict[Point, Elf | Tile] = {}
input_file = "23/test.txt"
elfs = []
f = open(input_file)
for y, l in enumerate(f.readlines()):
    l = l.strip()
    for x, c in enumerate(l):
        if c == ".":
            grid[(x, y)] = Tile.EMPTY
        elif c == "#":
            elf = Elf((x,y))
            grid[(x, y)] = elf
            elfs.append(elf)
f.close()

print_grid(grid)
