from collections import defaultdict
from threading import current_thread

from defaultlist import defaultlist
import itertools
from pickle import NONE
from typing import List, Dict, Tuple
from itertools import chain, groupby
from sympy import symbols, Eq, solve
from enum import Enum


Point = Tuple[int, int]


class Tile(str, Enum):
    EMPTY = '🌫️'
    FLOOR = "🟦"
    BLOCKED = "🗿"


class Move(str, Enum):
    EAST = "👉"
    WEST = "👈"
    SOUTH = "👇"
    NORTH = "👆"

DIRECTIONS = [Move.EAST, Move.SOUTH, Move.WEST, Move.NORTH]

Grid = Dict[Point, (Tile | Move)]


def warp(grid: Grid, start: Point, direction: Move) -> Point:
    x, y = start
    print(f"warping from {start} {direction.value}")
    match direction:
        case Move.EAST:
            x = min([xx for xx, yy in grid.keys() if y == yy])
        case Move.WEST:
            x = max([xx for xx, yy in grid.keys() if y == yy])
        case Move.NORTH:
            y = max([yy for xx, yy in grid.keys() if x == xx])
        case Move.SOUTH:
            y = min([yy for xx, yy in grid.keys() if x == xx])
    print(f"x:{x} y:{y}")
    print(f"x:{x} y:{y}")
    if grid[(x,y)] == Tile.BLOCKED:
        print(f"is blocked")
        return start
    return (x, y)

def warp_cube(grid: Grid, faces, faces_map, start: Point, direction: Move) -> Point:
    current_face = faces_map[start]
    next_face, next_face_entry_direction, n_spins = faces[(current_face, direction)]
    face_keys = [key for key, value in faces_map.items() if value == next_face]
    min_x = min(face_keys, key= lambda p: p[0])[0]
    min_y = min(face_keys, key= lambda p: p[1])[1]
    max_x = max(face_keys, key= lambda p: p[0])[0]
    max_y = max(face_keys, key= lambda p: p[1])[1]
    zero_plane_x = start[0] % 4
    zero_plane_y = start[1] % 4

    

    x = zero_plane_x + min_x
    y = zero_plane_y + min_y
    match next_face_entry_direction:
        case Move.EAST:
            x = max_x
        case Move.WEST:
            x = min_x
        case Move.NORTH:
            y = min_y
        case Move.SOUTH:
            y = max_y
            if n_spins in [1, 3]:
                pass
            else:
                x = 4 - x
    if grid[(x,y)] == Tile.BLOCKED:
        return start
    return (x, y)


def move_to(grid, origin, desination, direction, is_cube=False, faces=None, faces_map=None):
    try:
        match grid[desination]:
            case Tile.FLOOR:
                return desination
            case Tile.BLOCKED:
                return origin
            case Tile.EMPTY:
                if is_cube:
                    return warp_cube(grid, faces, faces_map, origin, direction)
                else:
                    return warp(grid, origin, direction)
            case _:  # It's Move, therefore Floor 
                return desination
    except KeyError:
        if is_cube:
            return warp_cube(grid, faces, faces_map, origin, direction)
        else:
            return warp(grid, origin, direction)


def move_point(grid: Grid, start: Point, direction: Move, is_cube=False, faces=None, faces_map=None) -> Point:
    x, y = start
    match direction:
        case Move.EAST:
            temp = (x + 1, y)
        case Move.WEST:
            temp = (x - 1, y)
        case Move.NORTH:
            temp = (x, y - 1)
        case Move.SOUTH:
            temp = (x, y + 1)
    return move_to(grid, start, temp, direction, is_cube=is_cube, faces=faces, faces_map=faces_map)
            

class Player():
    is_cube = False
    def __init__(self, position: Point, direction: Move, faces=None, faces_map=None) -> None:
        self.position = position
        self.direction = direction
        self.current_direction = direction
        self.faces = faces
        self.faces_map = faces_map
        if self.faces and self.faces_map:
            self.is_cube = True

    def spin(self, direction: str):
        current_direction = self.current_direction
        if direction == "R":
            match current_direction:
                case Move.EAST:
                    current_direction = Move.SOUTH
                case Move.WEST:
                    current_direction = Move.NORTH
                case Move.NORTH:
                    current_direction = Move.EAST
                case Move.SOUTH:
                    current_direction = Move.WEST
        else:
            match current_direction:
                case Move.EAST:
                    current_direction = Move.NORTH
                case Move.WEST:
                    current_direction = Move.SOUTH
                case Move.NORTH:
                    current_direction = Move.WEST
                case Move.SOUTH:
                    current_direction = Move.EAST
        self.current_direction = current_direction

    
    def move(self, grid: Dict[Point, (Tile | Move)]) -> Dict[Point, (Tile | Move)]:
        new_grid = grid.copy()
        old_position = self.position
        self.position = move_point(grid, self.position, self.current_direction, is_cube=self.is_cube, faces=self.faces, faces_map=self.faces_map)
        if self.is_cube:
            if faces_map[old_position] != faces_map[self.position]:
                # changed face
                for _ in range(self.faces[(faces_map[old_position], self.current_direction)][2]):
                    self.spin("R")
 
        new_grid[self.position] = self.current_direction
        return new_grid


def print_grid(grid: Dict[Point, (Tile| Move)], player=None, min_x=None, max_x=None, min_y=None, max_y=None):
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

grid: Dict[Point, (Tile | Move)] = {}
input_file = "22/test.txt" 
f = open(input_file)
moves_str = f.read().splitlines()[-1]
moves_str = moves_str.strip()
f.close()

f = open(input_file)
puzzle = f.read()[:-2]
for y, l in enumerate(puzzle.splitlines()):
    # print(l)
    for x, c in enumerate(l):
        if c == " ":
            continue
        elif c == ".":
            grid[(x, y)] = Tile.FLOOR
        elif c == "#":
            grid[(x, y)] = Tile.BLOCKED
        else:
            continue
f.close()

moves_list = defaultlist(lambda: "")
last_is_digit = True
for move in moves_str:
    if move.isdigit() and last_is_digit:
        try:
            moves_list[-1] += move
            last_is_digit = True
        except IndexError:
            moves_list[0] = move
    else:
        moves_list.append(move)
        last_is_digit = False
    if move.isdigit():
        last_is_digit = True


moves = []
for move in moves_list:
    if move.isdigit():
        moves.append(int(move))
    else:
        moves.append(move)

x_points = list(set([x for x, _ in grid.keys()]))
y_points = list(set([y for _, y in grid.keys()]))
min_x = min(x_points, default=0)
min_y = min(y_points, default=0)
keys = list(grid.keys())
point = min([(x,y) for x,y in keys if y == 0], key=lambda x: x[0])
print(min_x)
print(min_y)
grid2 = grid.copy()
player = Player(point, Move.EAST)
print_grid(grid, player=player)
print(moves)
for move in moves:
    print(move)
    if type(move) == int:
        for i in range(move):
            print(f"{i}/{move}")
            grid = player.move(grid)
            print_grid(grid)
    else:
        player.spin(move)
    print_grid(grid)
print_grid(grid)
final_position = player.position
print(player.position)
print("part1 password", (final_position[1] + 1) * 1000 + (final_position[0] + 1) * 4 + DIRECTIONS.index(player.current_direction))

FaceMap = Tuple[int, Move]
FaceMapSwap = Tuple[int, Move, int, bool]
faces: Dict[FaceMap, FaceMapSwap] = dict()
faces_map = dict()


if "test" in input_file:
    faces[0, Move.NORTH] = 1, Move.NORTH, 2, False
    faces[0, Move.EAST] = 5, Move.EAST, 2, False
    faces[0, Move.SOUTH] = 3, Move.NORTH, 0, False
    faces[0, Move.WEST] = 2, Move.NORTH , 3, False
    faces[1, Move.NORTH] =  0, Move.NORTH, 2, False
    faces[1, Move.EAST] = 2, Move.WEST, 0, False
    faces[1, Move.SOUTH] = 4, Move.SOUTH, 2, False
    faces[1, Move.WEST] = 5, Move.SOUTH, 3, False
    faces[2, Move.NORTH] = 0, Move.WEST, 1, False
    faces[2, Move.EAST] = 3, Move.WEST, 0, False
    faces[2, Move.SOUTH] = 4, Move.WEST, 3, False
    faces[2, Move.WEST] = 1, Move.EAST, 0, False
    faces[3, Move.NORTH] = 0, Move.SOUTH, 0, False
    faces[3, Move.EAST] = 5, Move.NORTH, 1, False
    faces[3, Move.SOUTH] = 4, Move.NORTH, 0, False
    faces[3, Move.WEST] = 2, Move.EAST, 0, False
    faces[4, Move.NORTH] = 3, Move.SOUTH, 0, False
    faces[4, Move.EAST] = 5, Move.WEST, 0, False
    faces[4, Move.SOUTH] = 1, Move.SOUTH, 2, False
    faces[4, Move.WEST] = 2, Move.SOUTH, 1, False
    faces[5, Move.NORTH] = 3, Move.EAST, 3, False
    faces[5, Move.EAST] = 0, Move.EAST, 2, False
    faces[5, Move.SOUTH] = 1, Move.WEST, 3, False
    faces[5, Move.WEST] = 4, Move.EAST, 0, False
    for x in range(8, 12):
        for y in range(0, 4):
            faces_map[(x,y)] = 0
    for x in range(0, 4):
        for y in range(4, 8):
            faces_map[(x,y)] = 1
    for x in range(4, 8):
        for y in range(4, 8):
            faces_map[(x,y)] = 2
    for x in range(8, 12):
        for y in range(4, 8):
            faces_map[(x,y)] = 3
    for x in range(8, 12):
        for y in range(8, 12):
            faces_map[(x,y)] = 4
    for x in range(12, 16):
        for y in range(8, 12):
            faces_map[(x,y)] = 5
else:
    faces[0, Move.NORTH] = 5, Move.WEST, False
    faces[0, Move.EAST] = 1, Move.WEST, False
    faces[0, Move.SOUTH] = 2, Move.NORTH, False
    faces[0, Move.WEST] = 3, Move.WEST, False
    faces[1, Move.NORTH] =  5, Move.SOUTH, False
    faces[1, Move.EAST] = 4, Move.EAST, False
    faces[1, Move.SOUTH] = 2, Move.NORTH, False
    faces[1, Move.WEST] = 0, Move.EAST, False
    faces[2, Move.NORTH] = 0, Move.SOUTH, False
    faces[2, Move.EAST] = 1, Move.SOUTH, False
    faces[2, Move.SOUTH] = 4, Move.NORTH, False
    faces[2, Move.WEST] = 3, Move.NORTH, False
    faces[3, Move.NORTH] = 2, Move.WEST, False
    faces[3, Move.EAST] = 4, Move.WEST, False
    faces[3, Move.SOUTH] = 5, Move.NORTH, False
    faces[3, Move.WEST] = 0, Move.NORTH, False
    faces[4, Move.NORTH] = 2, Move.SOUTH, False
    faces[4, Move.EAST] = 2, Move.EAST, False
    faces[4, Move.SOUTH] = 5, Move.EAST, False
    faces[4, Move.WEST] = 4, Move.EAST, False
    faces[5, Move.NORTH] = 3, Move.SOUTH, False
    faces[5, Move.EAST] = 4, Move.SOUTH, False
    faces[5, Move.SOUTH] = 1, Move.EAST, False
    faces[5, Move.WEST] = 0, Move.NORTH, False
    for x in range(50, 100):
        for y in range(0, 50):
            faces_map[(x,y)] = 0
    for x in range(100, 150):
        for y in range(0, 50):
            faces_map[(x,y)] = 1
    for x in range(50, 100):
        for y in range(50, 100):
            faces_map[(x,y)] = 2
    for x in range(0, 50):
        for y in range(100, 150):
            faces_map[(x,y)] = 3
    for x in range(50, 100):
        for y in range(100, 150):
            faces_map[(x,y)] = 4
    for x in range(0, 50):
        for y in range(150, 200):
            faces_map[(x,y)] = 5

player = Player(point, Move.EAST, faces=faces, faces_map=faces_map)
for move in moves:
    print(move)
    if type(move) == int:
        for i in range(move):
            print(f"{i}/{move}")
            grid2 = player.move(grid2)
            print_grid(grid2)
    else:
        player.spin(move)
    print_grid(grid2)
print_grid(grid2)
final_position = player.position
print(player.position)
print("part2 password", (final_position[1] + 1) * 1000 + (final_position[0] + 1) * 4 + DIRECTIONS.index(player.current_direction))
