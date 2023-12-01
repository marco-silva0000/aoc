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

Point = Tuple[int, int]

def left_shift(shape: List[Point]):
    new_keys: List[Point] = [(x-1, y) for x, y in shape]
    if any(x < 0 for x, _ in new_keys):
        return shape
    return new_keys


def right_shift(shape: List[Point], x_size=7):
    new_keys: List[Point] = [(x+1, y) for x, y in shape]
    if any(x >= x_size for x, _ in new_keys):
        return shape
    return new_keys


def down_shift(shape: List[Point]):
    new_keys: List[Point] = [(x, y - 1) for x, y in shape]
    if any(y < 0 for _, y in new_keys):
        return shape
    return new_keys


def up_shift(shape: List[Point]):
    new_keys: List[Point] = [(x, y + 1) for x, y in shape]
    return new_keys


def is_coliding(this: List[Point], that: List[Point] ):
    for x, y in this:
        for xx, yy in that:
            if x == xx and y == yy:
                return True
    return False

def get_top_y(grid: Dict[Point, Any], min_x=0, max_x=7):
    top_y = []
    for x in range(min_x, max_x):
        y = max([yy for xx, yy in grid.keys() if x == xx], default=-1)
        top_y.append((x, y,))
    return top_y

def is_coliding_with_grid(this: List[Point], grid: Dict[Point, Any], min_x=0, max_x=7, top_y=None):
    if not top_y:
        top_y = get_top_y(grid, min_x=min_x, max_x=max_x)
    return is_coliding(this, top_y)

class Piece():
    _base_shape: List[Point] = []
    shape: List[Point] = []
    left_edge = (0,0,)
    bottom_edge = left_edge
    material = Material.PIECE
    settle_material = Material.PIECE
    settle_time = 0
    last_shift_value = None
    shifts = []
    n_shifts = 0
    start_i = 0

    def __init__(self, x_shifts: int, y_shifts: int, x_size=7):
        self.x_size = x_size
        self.shape = self._base_shape
        self.shape = self >> x_shifts
        self.shape = self + y_shifts

    def move_left(self, grid: Dict[Point, Material], top_y=None):
        tentative_shape = self << 1
        if not is_coliding(tentative_shape, list(grid.keys())):
            self.shape = tentative_shape

    def move_right(self, grid: Dict[Point, Material], top_y=None):
        tentative_shape = self >> 1
        if not is_coliding(tentative_shape, list(grid.keys())):
            self.shape = tentative_shape

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.settle_time == other.settle_time and self.shifts == other.shifts

    def __str__(self) -> str:
        return f"{type(self)}({self.shape})"

    def __repr__(self) -> str:
        return str(self)

    def settle(self):

        self.material = self.settle_material

    def __lshift__(self, reference) -> List[Point]: 
        if type(reference) == int:
            result = self.shape
            for _ in range(reference):
                result = left_shift(result)
            return result
        elif type(reference) == dict:
            result = left_shift(self.shape)
            if is_coliding(result, reference.keys()):
                return self.shape
            return result
        raise TypeError

    def __irshift__(self, reference) -> List[Point]: 
        self.shape = self >> reference
        return self.shape

    def __ilshift__(self, reference) -> List[Point]: 
        self.shape = self << reference
        return self.shape


    def __rshift__(self, reference) -> List[Point]: 
        if type(reference) == int:
            result = self.shape
            for _ in range(reference):
                result = right_shift(result, self.x_size)
            return result
        elif type(reference) == dict:
            result = right_shift(self.shape, self.x_size)
            if is_coliding(result, reference.keys()):
                return self.shape
            return result
        raise TypeError

    def __sub__(self, other) -> List[Point]:
        if type(other) == int:
            result = self.shape
            for _ in range(other):
                result = down_shift(result)
            return result
        raise TypeError

    def __add__(self, other) -> List[Point]:
        if type(other) == int:
            result = self.shape
            for _ in range(other):
                result = up_shift(result)
            return result
        raise TypeError



class Line(Piece):
    settle_material = Material.LINE
    _base_shape = [(0,0,),(1,0,),(2,0,),(3,0,)]

class Cross(Piece):
    settle_material = Material.CROSS
    left_edge = (0,1,)
    bottom_edge = (1, 0,)
    _base_shape = [(1,0,),(0,1,),(1,1,),(2,1,),(1,2,)]

class Ele(Piece):
    settle_material = Material.ELE
    _base_shape = [(0,0,),(1,0,),(2,0,),(2,1,),(2,2,)]

class Rod(Piece):
    settle_material = Material.ROD
    _base_shape = [(0,0,),(0,1,),(0,2,),(0,3,),]

class Square(Piece):
    settle_material = Material.SQUARE
    _base_shape = [(0,0,),(0,1,),(1,0,),(1,1,),]


def print_grid(grid: Dict[Point, Material], piece=None, pieces=[]):
    x_points = list(set([x for x, _ in grid.keys()]))
    x_points.sort()
    y_points = list(set([y for _, y in grid.keys()]))
    y_points.sort()
    min_x = -1
    max_x = 8
    min_y = -2
    max_y = max(y_points, default=0)+2
    if piece:
        piece_max_y = max(piece.shape, key= lambda x: x[1])[1]
        if piece_max_y > max_y:
            max_y = piece_max_y
    for y in range(max_y, min_y, -1):
        print(f"{y:03}:", end="")
        for x in range(min_x, max_x):
            try:
                value = grid[(x, y)].value
            except KeyError:
                value = Material.EMPTY.value
            if x<0 or x>=7 or y<0:
                value = Material.WALL.value
            if piece and (x,y) in piece.shape:
                value = piece.material.value
            if (x,y) == (0, 0):
                value = "🌌"
            for piece in pieces:
                if (x,y) in piece.shape:
                    value = Material.PIECE.value
            print(value, end="")
        print("")
    print("")



f = open("17/input.txt")
pieces = cycle([Line, Cross, Ele, Rod, Square])
grid: Dict[Point, Material] =  dict()
moves_str = f.read().strip()
f.close()
print("moves_str", moves_str)
moves = cycle(moves_str)

def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)



def find_pattern(grid, last_pieces, min_size=6):
    print("finding_pattern")
    pattern_height = 0
    pattern_offset = 0
    slice_size = min_size
    result_slice = []
    result_index = 0
    while not result_slice and slice_size < len(last_pieces):
        for i in range(len(last_pieces)-slice_size):
            candidate = last_pieces[i:i+slice_size]
            # print("candidate", candidate)
            for j, window in enumerate(sliding_window(last_pieces[i+slice_size:], slice_size)):
                # print("window", window)
                for k in range(len(candidate)):
                    if candidate[k] != window[k]:
                        break
                else:
                    next_loop_first = last_pieces[i+slice_size+1]
                    if  next_loop_first == last_pieces[i]:
                        print("found pattern")
                        result_slice = last_pieces[i:i+j+slice_size]
                        result_index = i
                        print(result_slice)
                        print("result_index", result_index)
                        print("len result slice", len(result_slice))
                        break
            if result_slice:
                break
        slice_size += 1

        print("slice_size", slice_size)

    min_y = min([min(piece.shape, key= lambda p: p[1])[1] for piece in result_slice])
    max_y = max([max(piece.shape, key= lambda p: p[1])[1] for piece in result_slice])
    pattern_height = max_y - min_y + 1 - 15
    pattern_offset = result_index
    print(result_slice[0])
    print(result_slice[-1])
    return pattern_height, pattern_offset, result_slice

def clear_above(grid, y):
    keys = [key for key in grid.keys() if key[1] >= y]
    for key in keys:
        del grid[key]


def clear_slice(grid, slice):
    keys = [piece.shape for piece in slice]
    for key in chain.from_iterable(keys):
        del grid[key]

    
    

# print_grid(grid)
i = 0
x_size = 7
moving_piece = None
n_pieces = 0
total_rocks = 1000000000000
# total_rocks = 10
# total_rocks = 3
top_y = None
last_moves_cycle_size = 40
last_pieces = []
pattern_found = False
calculated_height = 0
skip_move = False
print_for_x = 0
while n_pieces < total_rocks: 
    if n_pieces % 20 == 0:
        print(f"{n_pieces}/total_rocks={n_pieces/total_rocks*100}%")
    if not pattern_found and n_pieces / 3500 == 1.0:
        pattern_height, pattern_offset, result_slice = find_pattern(grid, last_pieces)
        next_piece = last_pieces[pattern_offset]
        prev_piece = last_pieces[pattern_offset-1]
        slice_size = len(result_slice)

        print('pattern_height', pattern_height)
        print("pattern_offset", pattern_offset)
        print("result_slice", result_slice)
        next_piece.material = Material.PIECE
        print_grid(grid, moving_piece, pieces=[result_slice[0], result_slice[-1]])
        next_piece.material = Material.PIECE

        clear_slice(grid, last_pieces[pattern_offset:])
        print_grid(grid, next_piece)
        moves = cycle(moves_str)
        for _ in range(next_piece.start_i):
            next(moves)

        cycle_piece = next(pieces)
        while type(prev_piece) != type(cycle_piece(0,0)):
            cycle_piece = next(pieces)
        moving_piece = None

        n_loops = (total_rocks - pattern_offset) // slice_size
        n_loops -= 1
        calculated_height = (n_loops) * pattern_height
        n_pieces = pattern_offset + (n_loops) * slice_size

        print('pattern_height', pattern_height)
        print("pattern_offset", pattern_offset)
        print("result_slice", result_slice)
        print("n_loops", n_loops)
        print("calculated_height", calculated_height)
        print("n_pieces", n_pieces)
        print("left", total_rocks-n_pieces)
        pattern_found = True
        print_for_x = 15


    keys = list(grid.keys())
    min_x = min(keys, default=(0,0,), key= lambda x: x[0])[0]
    max_y = max(keys, default=(0,-1,), key= lambda x: x[1])[1]

    if not moving_piece:
        moving_piece = next(pieces)(2, max_y+4, x_size=x_size)
        moving_piece.start_i = i
        # print("i", i)
        # print("moving_piece.start_i", moving_piece.start_i)
        # print("len moves str", len(moves_str))
        if print_for_x > 0:
            print_grid(grid, moving_piece)
    move = next(moves)
    # print("move", move)
    if move == '<':
        moving_piece.move_left(grid, top_y=top_y)
    else:
        moving_piece.move_right(grid, top_y=top_y)

    moving_piece.shifts.append(move)
    moving_piece.n_shifts += 1
    if print_for_x > 0:
        print_grid(grid, moving_piece)

    tentative_drop_shape = moving_piece - 1
    if not is_coliding(tentative_drop_shape, list(grid.keys())) and tentative_drop_shape != moving_piece.shape:
        moving_piece.shape = tentative_drop_shape
        moving_piece.settle_time += 1
        moving_piece.last_shift_value = move
    else:
        moving_piece.settle()
        n_pieces += 1
        for point in moving_piece.shape:
            grid[point] = moving_piece.material
        # top_y = get_top_y(grid)
        last_pieces.append(moving_piece)
        moving_piece = None

    if print_for_x > 0:
        print_grid(grid, moving_piece)
    i += 1
    if print_for_x > 0:
        print_for_x -= 1

print_grid(grid, moving_piece, pieces=[result_slice[0], result_slice[-1], last_pieces[pattern_offset + len(result_slice)]])

keys = list(grid.keys())
max_y = max(keys, default=(0,-1,), key= lambda x: x[1])[1]
print('pattern_height', pattern_height)
print("pattern_offset", pattern_offset)
print("result_slice", result_slice)
print("n_loops", n_loops)
print("calculated_height", calculated_height)
print("n_pieces", n_pieces)
print("left", total_rocks-n_pieces)
print("max_y", max_y)
print(max_y+1+calculated_height)

