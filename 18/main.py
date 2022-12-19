from typing import Dict, List, Tuple, Any

from collections import defaultdict, deque
from enum import Enum
from itertools import cycle, islice, chain


class Material(str, Enum):
    EMPTY = '🌫️'
    ROCK = "🗿"
    PIECE = "🔽"
    WALL = "🧱"
    ELE = "🎸"
    ROD = "🤘"
    SQUARE = "💎"
    LINE = "🗿"
    CROSS = "🪨"
    LAVA = "🌋"
    FIRE = "🔥"
    AIR = "🛩️"
    BUBBLE = "🫧"

Point = Tuple[int, int, int]

# def left_shift(shape: List[Point]):
#     new_keys: List[Point] = [(x-1, y) for x, y in shape]
#     if any(x < 0 for x, _ in new_keys):
#         return shape
#     return new_keys


# def right_shift(shape: List[Point], x_size=7):
#     new_keys: List[Point] = [(x+1, y) for x, y in shape]
#     if any(x >= x_size for x, _ in new_keys):
#         return shape
#     return new_keys


# def down_shift(shape: List[Point]):
#     new_keys: List[Point] = [(x, y - 1) for x, y in shape]
#     if any(y < 0 for _, y in new_keys):
#         return shape
#     return new_keys


# def up_shift(shape: List[Point]):
#     new_keys: List[Point] = [(x, y + 1) for x, y in shape]
#     return new_keys


# def is_coliding(this: List[Point], that: List[Point] ):
#     for x, y in this:
#         for xx, yy in that:
#             if x == xx and y == yy:
#                 return True
#     return False

# def get_top_y(grid: Dict[Point, Any], min_x=0, max_x=7):
#     top_y = []
#     for x in range(min_x, max_x):
#         y = max([yy for xx, yy in grid.keys() if x == xx], default=-1)
#         top_y.append((x, y,))
#     return top_y

# def is_coliding_with_grid(this: List[Point], grid: Dict[Point, Any], min_x=0, max_x=7, top_y=None):
#     if not top_y:
#         top_y = get_top_y(grid, min_x=min_x, max_x=max_x)
#     return is_coliding(this, top_y)

# class Piece():
#     _base_shape: List[Point] = []
#     shape: List[Point] = []
#     left_edge = (0,0,)
#     bottom_edge = left_edge
#     material = Material.PIECE
#     settle_material = Material.PIECE
#     settle_time = 0
#     last_shift_value = None
#     shifts = []
#     n_shifts = 0
#     start_i = 0

#     def __init__(self, x_shifts: int, y_shifts: int, x_size=7):
#         self.x_size = x_size
#         self.shape = self._base_shape
#         self.shape = self >> x_shifts
#         self.shape = self + y_shifts

#     def move_left(self, grid: Dict[Point, Material], top_y=None):
#         tentative_shape = self << 1
#         if not is_coliding(tentative_shape, list(grid.keys())):
#             self.shape = tentative_shape

#     def move_right(self, grid: Dict[Point, Material], top_y=None):
#         tentative_shape = self >> 1
#         if not is_coliding(tentative_shape, list(grid.keys())):
#             self.shape = tentative_shape

#     def __eq__(self, other) -> bool:
#         return type(self) == type(other) and self.start_i == other.start_i and self.settle_time == other.settle_time and self.n_shifts == other.n_shifts and self.last_shift_value == other.last_shift_value and self.shifts == other.shifts

#     def __str__(self) -> str:
#         return f"{type(self)}({self.shape})"

#     def __repr__(self) -> str:
#         return str(self)

#     def settle(self):

#         self.material = self.settle_material

#     def __lshift__(self, reference) -> List[Point]: 
#         if type(reference) == int:
#             result = self.shape
#             for _ in range(reference):
#                 result = left_shift(result)
#             return result
#         elif type(reference) == dict:
#             result = left_shift(self.shape)
#             if is_coliding(result, reference.keys()):
#                 return self.shape
#             return result
#         raise TypeError

#     def __irshift__(self, reference) -> List[Point]: 
#         self.shape = self >> reference
#         return self.shape

#     def __ilshift__(self, reference) -> List[Point]: 
#         self.shape = self << reference
#         return self.shape


#     def __rshift__(self, reference) -> List[Point]: 
#         if type(reference) == int:
#             result = self.shape
#             for _ in range(reference):
#                 result = right_shift(result, self.x_size)
#             return result
#         elif type(reference) == dict:
#             result = right_shift(self.shape, self.x_size)
#             if is_coliding(result, reference.keys()):
#                 return self.shape
#             return result
#         raise TypeError

#     def __sub__(self, other) -> List[Point]:
#         if type(other) == int:
#             result = self.shape
#             for _ in range(other):
#                 result = down_shift(result)
#             return result
#         raise TypeError

#     def __add__(self, other) -> List[Point]:
#         if type(other) == int:
#             result = self.shape
#             for _ in range(other):
#                 result = up_shift(result)
#             return result
#         raise TypeError



# class Line(Piece):
#     settle_material = Material.LINE
#     _base_shape = [(0,0,),(1,0,),(2,0,),(3,0,)]

# class Cross(Piece):
#     settle_material = Material.CROSS
#     left_edge = (0,1,)
#     bottom_edge = (1, 0,)
#     _base_shape = [(1,0,),(0,1,),(1,1,),(2,1,),(1,2,)]

# class Ele(Piece):
#     settle_material = Material.ELE
#     _base_shape = [(0,0,),(1,0,),(2,0,),(2,1,),(2,2,)]

# class Rod(Piece):
#     settle_material = Material.ROD
#     _base_shape = [(0,0,),(0,1,),(0,2,),(0,3,),]

# class Square(Piece):
#     settle_material = Material.SQUARE
#     _base_shape = [(0,0,),(0,1,),(1,0,),(1,1,),]


# def print_grid(grid: Dict[Point, Material], piece=None, pieces=[]):
#     x_points = list(set([x for x, _ in grid.keys()]))
#     x_points.sort()
#     y_points = list(set([y for _, y in grid.keys()]))
#     y_points.sort()
#     min_x = -1
#     max_x = 8
#     min_y = -2
#     max_y = max(y_points, default=0)+2
#     if piece:
#         piece_max_y = max(piece.shape, key= lambda x: x[1])[1]
#         if piece_max_y > max_y:
#             max_y = piece_max_y
#     for y in range(max_y, min_y, -1):
#         print(f"{y:03}:", end="")
#         for x in range(min_x, max_x):
#             try:
#                 value = grid[(x, y)].value
#             except KeyError:
#                 value = Material.EMPTY.value
#             if x<0 or x>=7 or y<0:
#                 value = Material.WALL.value
#             if piece and (x,y) in piece.shape:
#                 value = piece.material.value
#             if (x,y) == (0, 0):
#                 value = "🌌"
#             for piece in pieces:
#                 if (x,y) in piece.shape:
#                     value = Material.PIECE.value
#             print(value, end="")
#         print("")
#     print("")



f = open("18/input.txt")
grid: Dict[Point, int] =  dict()
for line in f.readlines():
    line = line.strip()
    x, y, z = line.split(",")
    x, y, z = (int(x), int(y), int(z))
    grid[x,y,z] = 1
f.close()

def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)

def is_touching(one: Tuple[int, int, int], other: Tuple[int, int, int]) -> bool:
    x, y, z = one
    xx, yy, zz = other
    dx = abs(xx - x)
    dy = abs(yy - y)
    dz = abs(zz - z)


    return dx + dy + dz == 1 


print(grid.keys())
# grid = {}
# grid[1,1,1] = True
# grid[2,1,1] = True
X = 0
Y = 1
Z = 1
def get_neighbor_faces(cube: Tuple[int, int, int]):
    x, y, z = cube
    north = (x, y+1, z)
    south = (x, y-1, z)
    east = (x+1, y, z)
    west = (x-1, y, z)
    top = (x, y, z+1)
    bottom = (x, y, z-1)
    return [north, south, east, west, top, bottom]

result = 0
keys = list(grid.keys())
for cube in keys:
    touching = 0
    neighbors = get_neighbor_faces(cube)
    for other in neighbors:
        if other in keys:
            touching += 1
    result += 6 - touching


print(result)

def print_face(points, min_x=None, max_x=None, min_y=None, max_y=None):
    x_points = list(set([x for x, _ in points]))
    x_points.sort()
    y_points = list(set([y for _, y in points]))
    y_points.sort()
    if min_x is None:
        min_x = min(x_points, default=0)
    if max_x is None:
        max_x = max(x_points, default=1)
    if min_y is None:
        min_y = min(y_points, default=1)
    if max_y is None:
        max_y = max(y_points, default=0)
    for y in range(max_y, min_y, -1):
        print(f"{y:03}:", end="")
        for x in range(min_x, max_x):
            if (x, y) in points:
                value = Material.LAVA.value
            else:
                value = Material.EMPTY.value
            print(value, end="")
        print("")
    print("")

def print_face(points, out_cubes, air_cubes, out_air_cubes, min_x=0, max_x=10, min_y=0, max_y=10):
    for y in range(max_y, min_y - 1, -1):
        print(f"{y:03}:", end="")
        for x in range(min_x, max_x):
            value = Material.EMPTY.value
            if (x, y) in air_cubes:
                value = Material.AIR.value
            if (x, y) in out_air_cubes:
                value = Material.BUBBLE.value
            if (x, y) in points:
                value = Material.LAVA.value
            if (x, y) in out_cubes:
                value = Material.FIRE.value
            print(value, end="")
        print("")
    print("")


def print_faces(points, out_cubes, air_cubes, out_air_cubes, min_x=None, max_x=None, min_y=None, max_y=None):
    x_points = list(set([x for x, _, _ in points]))
    x_points.sort()
    y_points = list(set([y for _, y, _ in points]))
    y_points.sort()
    z_points = list(set([z for _, _, z in points]))
    z_points.sort()
    if min_x is None:
        min_x = min(x_points, default=0)
    if max_x is None:
        max_x = max(x_points, default=1)
    if min_y is None:
        min_y = min(y_points, default=0)
    if max_y is None:
        max_y = max(y_points, default=1)
    min_z = min(z_points, default=0)
    max_z = max(z_points, default=1)

    print("(x,y)=z")
    temp_points = []
    temp_out = []
    temp_air = []
    temp_out_air = []
    for z in range(max_z+1, min_z-2, -1):
        for x in range(min_x-2, max_x+2):
            for y in range(min_y-2, max_y+2):
                if (x, y, z) in points and (x, y) not in temp_points: # first time this x,y appears
                    temp_points.append((x,y))
                if (x, y, z) in out_cubes and (x, y) not in temp_out: # first time this x,y appears
                    temp_out.append((x,y))
                if (x, y, z) in air_cubes and (x, y) not in temp_air: # first time this x,y appears
                    temp_air.append((x,y))
                if (x, y, z) in out_air_cubes and (x, y) not in temp_out_air: # first time this x,y appears
                    temp_out_air.append((x,y))
    for z in range(min_z-2, max_z+2):
        for x in range(min_x-2, max_x+2):
            for y in range(min_y-2, max_y+2):
                if (x, y, z) in points and (x, y) not in temp_points: # first time this x,y appears
                    temp_points.append((x,y))
                if (x, y, z) in out_cubes and (x, y) not in temp_out: # first time this x,y appears
                    temp_out.append((x,y))
                if (x, y, z) in air_cubes and (x, y) not in temp_air: # first time this x,y appears
                    temp_air.append((x,y))
                if (x, y, z) in out_air_cubes and (x, y) not in temp_out_air: # first time this x,y appears
                    temp_out_air.append((x,y))
    print_face(temp_points, temp_out, temp_air, temp_out_air, min_x=min_x-2, max_x=max_x+3, min_y=min_y-2, max_y=max_y+2)

    print("(z,y)=x")
    temp_points = []
    temp_out = []
    temp_air = []
    temp_out_air = []
    for x in range(max_x+5, min_x-2, -1):
        for z in range(min_z-2, max_z+2):
            for y in range(min_y-2, max_y+2):
                if (x, y, z) in points and (y, z) not in temp_points: # first time this x,y appears
                    temp_points.append((y,z))
                if (x, y, z) in out_cubes and (y, z) not in temp_out: # first time this x,y appears
                    temp_out.append((y,z))
                if (x, y, z) in air_cubes and (y, z) not in temp_air: # first time this x,y appears
                    temp_air.append((y,z))
                if (x, y, z) in out_air_cubes and (y, z) not in temp_out_air: # first time this x,y appears
                    temp_out_air.append((y,z))
    for x in range(min_x-2, max_x+2):
        for z in range(min_z-2, max_z+2):
            for y in range(min_y-2, max_y+2):
                if (x, y, z) in points and (y, z) not in temp_points: # first time this x,y appears
                    temp_points.append((y,z))
                if (x, y, z) in out_cubes and (y, z) not in temp_out: # first time this x,y appears
                    temp_out.append((y,z))
                if (x, y, z) in air_cubes and (y, z) not in temp_air: # first time this x,y appears
                    temp_air.append((y,z))
                if (x, y, z) in out_air_cubes and (y, z) not in temp_out_air: # first time this x,y appears
                    temp_out_air.append((y,z))
    print_face(temp_points, temp_out, temp_air, temp_out_air, min_x=min_y-2, max_x=max_y+3, min_y=min_z-2, max_y=max_z+2)


    print("(x,z)=y")
    temp_points = []
    temp_out = []
    temp_air = []
    temp_out_air = []
    for y in range(max_y+5, min_y-2, -1):
        for x in range(min_x-2, max_x+2):
            for z in range(min_z-2, max_z+2):
                if (x, y, z) in points and (x, z) not in temp_points: # first time this x,y appears
                    temp_points.append((x,z))
                if (x, y, z) in out_cubes and (x, z) not in temp_out: # first time this x,y appears
                    temp_out.append((x,z))
                if (x, y, z) in air_cubes and (x, z) not in temp_air: # first time this x,y appears
                    temp_air.append((x,z))
                if (x, y, z) in out_air_cubes and (x, z) not in temp_out_air: # first time this x,y appears
                    temp_out_air.append((x,z))
    for y in range(min_y-2, max_y+2):
        for x in range(min_x-2, max_x+2):
            for z in range(min_z-2, max_z+2):
                if (x, y, z) in points and (x, z) not in temp_points: # first time this x,y appears
                    temp_points.append((x,z))
                if (x, y, z) in out_cubes and (x, z) not in temp_out: # first time this x,y appears
                    temp_out.append((x,z))
                if (x, y, z) in air_cubes and (x, z) not in temp_air: # first time this x,y appears
                    temp_air.append((x,z))
                if (x, y, z) in out_air_cubes and (x, z) not in temp_out_air: # first time this x,y appears
                    temp_out_air.append((x,z))
    print_face(temp_points, temp_out, temp_air, temp_out_air, min_x=min_x-2, max_x=max_x+3, min_y=min_z-2, max_y=max_z+2)

def print_slices(points, out_cubes, air_cubes, out_air_cubes, min_x=None, max_x=None, min_y=None, max_y=None):
    x_points = list(set([x for x, _, _ in points]))
    x_points.sort()
    y_points = list(set([y for _, y, _ in points]))
    y_points.sort()
    z_points = list(set([z for _, _, z in points]))
    z_points.sort()
    if min_x is None:
        min_x = min(x_points, default=0)
    if max_x is None:
        max_x = max(x_points, default=1)
    if min_y is None:
        min_y = min(y_points, default=0)
    if max_y is None:
        max_y = max(y_points, default=1)
    min_z = min(z_points, default=0)
    max_z = max(z_points, default=1)

    for z in range(max_z+1, min_z-2, -1):
        temp_points = []
        temp_out = []
        temp_air = []
        temp_out_air = []
        print(f"(x,y)=z({z})")
        for x in range(min_x-2, max_x+2):
            for y in range(min_y-2, max_y+2):
                if (x, y, z) in points and (x, y) not in temp_points: # first time this x,y appears
                    temp_points.append((x,y))
                if (x, y, z) in out_cubes and (x, y) not in temp_out: # first time this x,y appears
                    temp_out.append((x,y))
                if (x, y, z) in air_cubes and (x, y) not in temp_air: # first time this x,y appears
                    temp_air.append((x,y))
                if (x, y, z) in out_air_cubes and (x, y) not in temp_out_air: # first time this x,y appears
                    temp_out_air.append((x,y))
        print_face(temp_points, temp_out, temp_air, temp_out_air, min_x=min_x-2, max_x=max_x+3, min_y=min_y-2, max_y=max_y+2)

    for x in range(min_x-2, max_x+2):
        print(f"(z,y)=x({x})")
        temp_points = []
        temp_out = []
        temp_air = []
        temp_out_air = []
        for z in range(min_z-2, max_z+2):
            for y in range(min_y-2, max_y+2):
                if (x, y, z) in points and (y, z) not in temp_points: # first time this x,y appears
                    temp_points.append((y,z))
                if (x, y, z) in out_cubes and (y, z) not in temp_out: # first time this x,y appears
                    temp_out.append((y,z))
                if (x, y, z) in air_cubes and (y, z) not in temp_air: # first time this x,y appears
                    temp_air.append((y,z))
                if (x, y, z) in out_air_cubes and (y, z) not in temp_out_air: # first time this x,y appears
                    temp_out_air.append((y,z))
        print_face(temp_points, temp_out, temp_air, temp_out_air, min_x=min_y-2, max_x=max_y+3, min_y=min_z-2, max_y=max_z+2)


    for y in range(min_y-2, max_y+2):
        print(f"(x,z)=y({y})")
        temp_points = []
        temp_out = []
        temp_air = []
        temp_out_air = []
        for x in range(min_x-2, max_x+2):
            for z in range(min_z-2, max_z+2):
                if (x, y, z) in points and (x, z) not in temp_points: # first time this x,y appears
                    temp_points.append((x,z))
                if (x, y, z) in out_cubes and (x, z) not in temp_out: # first time this x,y appears
                    temp_out.append((x,z))
                if (x, y, z) in air_cubes and (x, z) not in temp_air: # first time this x,y appears
                    temp_air.append((x,z))
                if (x, y, z) in out_air_cubes and (x, z) not in temp_out_air: # first time this x,y appears
                    temp_out_air.append((x,z))
        print_face(temp_points, temp_out, temp_air, temp_out_air, min_x=min_x-2, max_x=max_x+3, min_y=min_z-2, max_y=max_z+2)




x_keys = [key[0] for key in keys]
y_keys = [key[1] for key in keys]
z_keys = [key[2] for key in keys]
min_x = min(x_keys)-1
min_y = min(y_keys)-1
min_z = min(z_keys)-1
max_x = max(x_keys)+1
max_y = max(y_keys)+1
max_z = max(z_keys)+1
print(min_x)
print(max_y)
print(min_z)
print(max_x)
print(max_y)
print(max_z)

def get_out_cubes(cubes: List[Point]):
    x_keys = [key[0] for key in cubes]
    y_keys = [key[1] for key in cubes]
    z_keys = [key[2] for key in cubes]
    min_x = min(x_keys)-2
    min_y = min(y_keys)-2
    min_z = min(z_keys)-2
    max_x = max(x_keys)+2
    max_y = max(y_keys)+2
    max_z = max(z_keys)+2
    out_cubes = set()
    cubes.sort(key=lambda x: x[1])
    cubes.sort(key=lambda x: x[0])
    cubes.sort(key=lambda x: x[2])
    out_faces = 0
    z_go_up = []
    for z in range(min_z, max_z):
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                # print(f"({x}, {y}, {z})")
                if (x, y, z) in cubes and (x, y) not in z_go_up: # first time this x,y appears
                    # print(f"appending ({x}, {y}, {z})")
                    z_go_up.append((x,y))
                    out_faces += 1
                    out_cubes.add((x, y, z))
    # print(cubes)
    # print("z_go_up", z_go_up)
    # print_face(z_go_up, min_x=0, max_x=max_x, min_y=0, max_y=max_y)
    z_go_down = [] 
    for z in range(max_z, min_z-1, -1):
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                # print(f"({x}, {y}, {z})")
                if (x, y, z) in cubes and (x, y) not in z_go_down: # first time this x,y appears
                    # print(f"appending ({x}, {y}, {z})")
                    z_go_down.append((x,y))
                    out_faces += 1
                    out_cubes.add((x, y, z))
    # print(cubes)
    # print("z_go_down", z_go_down)

    cubes.sort(key=lambda x: x[2])
    cubes.sort(key=lambda x: x[1])
    cubes.sort(key=lambda x: x[0])
    x_go_east = []
    for x in range(min_x, max_x):
        for z in range(min_z, max_z):
            for y in range(min_y, max_y):
                # print(f"({x}, {y}, {z})")
                if (x, y, z) in cubes and (y, z) not in x_go_east: # first time this x,y appears
                    # print(f"appending ({x}, {y}, {z})")
                    x_go_east.append((y,z))
                    out_faces += 1
                    out_cubes.add((x, y, z))
    # print(cubes)
    # print("x_go_east", x_go_east)

    x_go_west = []
    for x in range(max_x, min_x - 1, -1):
        for z in range(min_z, max_z):
            for y in range(min_y, max_y):
                # print(f"({x}, {y}, {z})")
                if (x, y, z) in cubes and (y, z) not in x_go_west: # first time this x,y appears
                    # print(f"appending ({x}, {y}, {z})")
                    x_go_west.append((y,z))
                    out_faces += 1
                    out_cubes.add((x, y, z))

    # print(cubes)
    # print("x_go_west", x_go_west)
    cubes.sort(key=lambda x: x[2])
    cubes.sort(key=lambda x: x[0])
    cubes.sort(key=lambda x: x[1])

    y_go_east = []
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            for z in range(min_z, max_z):
                # print(f"({x}, {y}, {z})")
                if (x, y, z) in cubes and (x, z) not in y_go_east: # first time this x,y appears
                    # print(f"appending ({x}, {y}, {z})")
                    y_go_east.append((x, z))
                    out_faces += 1
                    out_cubes.add((x, y, z))

    # print(cubes)
    # print("y_go_east", y_go_east)
    y_go_west = []
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x):
            for z in range(min_z, max_z):
                # print(f"({x}, {y}, {z})")
                if (x, y, z) in cubes and (x, z) not in y_go_west: # first time this x,y appears
                    # print(f"appending ({x}, {y}, {z})")
                    y_go_west.append((x, z))
                    out_faces += 1
                    out_cubes.add((x, y, z))
    # print(cubes)
    # print("y_go_west", y_go_west)
    return out_cubes

new_out_faces = 0
out_cubes = get_out_cubes(keys)

center_x = (max_x - min_x)//2
center_y = (max_y - min_y)//2
center_z = (max_z - min_z)//2
print(center_x, center_y, center_z)
adjancent_air = set()
for cube in out_cubes:
    for neighbor in get_neighbor_faces(cube):
        if neighbor not in keys:
            adjancent_air.add(neighbor)
air_cubes = list(adjancent_air)

out_air_cubes = get_out_cubes(air_cubes)

for cube in out_cubes:
    touching = 0
    neighbors = get_neighbor_faces(cube)
    for other in neighbors:
        if other in out_air_cubes:
            touching += 1
            grid[other] = touching
    new_out_faces += touching
print_faces(grid, out_cubes, air_cubes, out_air_cubes)
print_slices(grid, out_cubes, air_cubes, out_air_cubes)
print(new_out_faces)
