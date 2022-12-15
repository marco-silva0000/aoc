from typing import Dict, Tuple

from collections import defaultdict
from enum import Enum

class Material(str, Enum):
    EMPTY = '🌫️'
    ROCK = "🗿"
    SAND_SOURCE = "⏳"
    SAND = "🔽"

class Grid(dict):
    floor = None
    def __getitem__(self, __key):
        try:
            return super().__getitem__(__key)
        except KeyError:
            if self.floor and __key[1] == self.floor:
                return Item(*__key, material=Material.ROCK)

            return Item(*__key, material=Material.EMPTY)

Point = Tuple[int, int]

class Item():
    def __init__(self, x: int, y: int, material=Material.EMPTY) -> None:
        self.x = x
        self.y = y
        self.material = material

    def __str__(self) -> str:
        return f"({self.x},{self.y}) {self.material.value}"

    def __repr__(self) -> str:
        return str(self)

    @property
    def one_bellow(self) -> Point:
        return (self.x, self.y + 1,)

    @property
    def one_bellow_left(self) -> Point:
        return (self.x - 1, self.y + 1,)

    @property
    def one_bellow_right(self) -> Point:
        return (self.x + 1, self.y + 1,)

    @property
    def is_empty(self) -> bool:
        return self.material  == Material.EMPTY

    @property
    def is_blocked(self) -> bool:
        return self.material in [Material.ROCK, Material.SAND]
    @property
    def point(self):
        return (self.x, self.y,)

    def get_bellow(self, grid: Dict[Point, "Item"]):
        return grid[self.one_bellow]


def print_grid(grid: Dict[Point, Item]):
    x_points = list(set([x for x, _ in grid.keys()]))
    x_points.sort()
    y_points = list(set([y for _, y in grid.keys()]))
    y_points.sort()
    for y in range(min(y_points)-1, max(y_points)+2):
        print(f"{y:03}:", end="")
        for x in range(min(x_points)-1, max(x_points)+2):
            try:
                value = grid[(x, y)].material.value
            except KeyError:
                value = Material.EMPTY.value
            print(value, end="")
        print("")
    print("")


def has_solid_bellow(point: Point, grid: Dict[Point, Item]):
    if grid.floor:
        return True
    return len([key for key in grid.keys() if key[0] == point[0] and key[1] > point[1]]) > 0


def make_sand(sand_source: Item, grid: Dict[Point, Item], stop=None):
    candidate = sand_source.get_bellow(grid)
    if candidate.is_empty:
        return make_sand(candidate, grid)
    elif candidate.is_blocked:
        left_candidate = grid[sand_source.one_bellow_left]
        if not left_candidate.is_blocked:
            if has_solid_bellow(left_candidate.point, grid):
                return make_sand(left_candidate, grid)
            return None
        else:
            right_candidate = grid[sand_source.one_bellow_right]
            if not right_candidate.is_blocked:
                if has_solid_bellow(right_candidate.point, grid):
                    return make_sand(right_candidate, grid)
                return None
            else:
                sand_source.material = Material.SAND
                grid[sand_source.point] = sand_source
                return sand_source
    print("not solid")
    return None


f = open("14/input.txt")
pairs = []
pair = [None, None]
pair_index = 0
grid: Dict[Point, Item] = Grid()
grid2: Dict[Point, Item] = Grid()
for i, l in enumerate(f.readlines()):
    l = l.strip()
    print(l)
    rock_lines = l.split(" -> ")
    prev = rock_lines[0]
    for current in rock_lines[1:]:
        prev_x, prev_y = [int(n) for n in prev.split(",")]
        current_x, current_y = [int(n) for n in current.split(",")]
        if prev_x == current_x:
            x = prev_x
            if prev_y > current_y:
                temp = current_y
                current_y = prev_y
                prev_y = temp
            for y in range(prev_y, current_y + 1):
                grid[(x,y)] = Item(x,y, Material.ROCK)
                grid2[(x,y)] = Item(x,y, Material.ROCK)
        else:
            y = prev_y
            if prev_x > current_x:
                temp = current_x
                current_x = prev_x
                prev_x = temp
            for x in range(prev_x, current_x + 1):
                grid[(x,y)] = Item(x,y, Material.ROCK)
                grid2[(x,y)] = Item(x,y, Material.ROCK)
        prev = current
        # print_grid(grid)
sand_source = Item(500, 0, Material.SAND_SOURCE)
grid[500, 0] = sand_source 
floor = max(list(set([pos[1] for pos in grid2.keys()]))) + 2
print(floor)
grid2.floor=floor
print_grid(grid)
i=0
while True: 
    i += 1
    # print_grid(grid)
    settle_point = make_sand(sand_source, grid)
    if (settle_point and settle_point.point == sand_source.point) or settle_point is None:
        break

print_grid(grid)
print(len([item for item in grid.values() if item.material == Material.SAND]))

while True: 
    i += 1
    # print_grid(grid2)
    settle_point = make_sand(sand_source, grid2)
    print(settle_point)
    if (settle_point and settle_point.point == sand_source.point) or settle_point is None:
        break
print_grid(grid2)
print(len([item for item in grid2.values() if item.material == Material.SAND]))

f.close()

