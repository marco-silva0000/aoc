from collections import defaultdict
import itertools
from pickle import NONE
from typing import List, Dict, Tuple
from itertools import chain, groupby
from enum import Enum


class Direction(str, Enum):
    LEFT = ("L",)
    RIGHT = ("R",)
    UP = ("U",)
    DOWN = ("D",)
    NONE = ("",)


class Status(str, Enum):
    HEAD = "H"
    TAIL = "T"
    VISITED = "#"
    ORIGIN = "s"
    NONE = "."
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"


"""
head (H) and tail (T) must always be touching (diagonally adjacent and even overlapping both count as touching)
If the head is ever two steps directly up, down, left, or right from the tail, the tail must also move one step in that direction so it remains close enough
Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail always moves one step diagonally to keep up
"""


def move_head(direction: Direction, prev_head: Tuple[int, int]) -> Tuple[int, int]:
    x, y = prev_head
    if direction == Direction.NONE:
        return (x,y,)
    elif direction == Direction.LEFT:
        x -= 1
    elif direction == Direction.RIGHT:
        x += 1
    elif direction == Direction.UP:
        y += 1
    elif direction == Direction.DOWN:
        y -= 1
    return (
        x,
        y,
    )


def is_touching(one: Tuple[int, int], other: Tuple[int, int]) -> bool:
    touching = [other]
    up = (other[0], other[1] + 1)
    upright = (other[0] + 1, other[1] + 1)
    upleft = (other[0] - 1, other[1] + 1)
    right = (other[0] + 1, other[1])
    left = (other[0] - 1, other[1])
    down = (other[0], other[1] - 1)
    downright = (other[0] + 1, other[1] - 1)
    downleft = (other[0] - 1, other[1] - 1)
    touching.extend([up, upright, upleft, right, left, down, downright, downleft])
    return one in touching


def same_row(one: Tuple[int, int], other: Tuple[int, int]) -> bool:
    return one[0] == other[0]


def same_col(one: Tuple[int, int], other: Tuple[int, int]) -> bool:
    return one[1] == other[1]


def aproximate(orig: int, dest: int) -> int:
    if dest > orig:
        return orig + 1
    else:
        return orig - 1


def move_tail(prev_tail: Tuple[int, int], new_head: Tuple[int, int]) -> Tuple[int, int]:
    if is_touching(new_head, prev_tail):
        return prev_tail
    elif (row := same_row(prev_tail, new_head)) or same_col(prev_tail, new_head):
        if row:
            y = aproximate(prev_tail[1], new_head[1])
            return (prev_tail[0], y)
        else:
            x = aproximate(prev_tail[0], new_head[0])
            return (x, prev_tail[1])
    else:
        x = aproximate(prev_tail[0], new_head[0])
        y = aproximate(prev_tail[1], new_head[1])
        return (x, y)


original_key = (
    0,
    0,
)


def next_map(
    direction: Direction,
    prev_head: Tuple[int, int],
    prev_tail: Tuple[int, int],
):
    new_head = move_head(direction, prev_head)
    new_tail = move_tail(prev_tail, new_head)
    # new_map[prev_head] = Status.NONE
    # new_map[prev_tail] = Status.NONE
    # new_map[new_head] = Status.HEAD
    # new_map[new_tail] = Status.TAIL

    return new_head, new_tail


def print_map(map: Dict[Tuple[int, int], Status], head=None):
    keys = list(map.keys())
    keys.sort()
    max_x = max([key[0] for key in keys])
    max_y = max([key[1] for key in keys])
    min_x = min([key[0] for key in keys])
    min_y = min([key[1] for key in keys])
    if max_x == 0:
        max_x = 1
    if max_y == 0:
        max_y = 1
    if min_x == 0:
        min_x = -1
    if min_y == 0:
        min_y = -1
    for y in range(max_y, min_y, -1):
        for x in range(min_x, max_x+1):
            value = map[x, y].value
            if (x, y) == head:
                value = Status.HEAD.value
            elif (x, y) == original_key:
                value = Status.ORIGIN.value
            print(value, 
                end="",
            )
        print("")
    print("--")



f = open("9/input.txt")
map: Dict[Tuple[int, int], Status] = defaultdict(lambda: Status.NONE)
maps = []
prev_head = original_key
prev_tail = original_key
map[original_key] = Status.ORIGIN
map[prev_head] = Status.HEAD
map[prev_tail] = Status.TAIL
tails :List[Tuple[int, int]] = [original_key]*10
maps.append(map)
visited = set()
for l in f.readlines():
    l = l.strip()
    print(l)
    direction, magnitude = l.split(" ")
    magnitude = int(magnitude)
    direction = Direction(direction)
    print(f"{magnitude} , {direction}")
    for _ in range(magnitude):
        tails[0], tails[1] = next_map(direction, tails[0], tails[1])
        map[tails[0]] = Status.HEAD
        map[tails[1]] = Status.ONE
        for i, tail in enumerate(tails[2:]):
            tail_head = tails[i+1]
            _, tails[i+2] = next_map(Direction.NONE, tails[i+1], tail)
            map[tails[i+2]] = Status(str(i+2))
        else:
            visited.add(tails[-1])
    else:
        map: Dict[Tuple[int, int], Status] = defaultdict(lambda: Status.NONE)
        for i, tail in enumerate(tails):
            if i == 0:
                map[tail] = Status.HEAD
            else:
                map[tail] = Status(str(i))
        print_map(map, head=tails[0])
            # maps.append(map)

# result = set((prev_tail,))
# for map in maps:
#     for key, value in map.items():
#         if value == Status.NINE:
#             result.add(key)
# print(maps)
# print_map(maps[-1])
# print(result)
# print(len(result))
print(len(visited))

f.close()
