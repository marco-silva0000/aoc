import itertools
from typing import List, Dict
from itertools import chain, groupby
from enum import Enum


class Direction(str, Enum):
    NORTH = ("N",)
    SOUTH = ("S",)
    EAST = ("E",)
    WEST = ("W",)


class Tree:
    def __init__(self, x, y, height, forest_size=0) -> None:
        self.is_visible = False
        self.x = x
        self.y = y
        self.height = height
        self.north = 0
        self.south = 0
        self.east = 0
        self.west = 0
        self.scenic_score = 0
        self.forest_size = forest_size

    def check_and_calc(self, forest):
        self.check_views(forest)
        self.calc_scenic_score()
        return self.scenic_score

    def calc_scenic_score(self):
        self.scenic_score = self.north * self.south * self.east * self.west

    def check_view(self, trees: List) -> int:
        result = 0
        print(f"calculating for tree ({self.x},{self.y})h:{self.height}")
        for tree in trees:
            print(f"t:({tree.x},{tree.y})h:{tree.height}")
            if tree.height < self.height:
                result += 1
                # print(f"added: ch:{current_height} t:({tree.x},{tree.y})h{tree.height}")
            else:
                print(f"stop")
                return result + 1
        return result

    def check_views(self, forest: Dict):
        north_keys = self.gen_keys(Direction.NORTH)
        self.north = self.check_view([forest[key] for key in north_keys])
        south_keys = self.gen_keys(Direction.SOUTH)
        self.south = self.check_view([forest[key] for key in south_keys])
        east_keys = self.gen_keys(Direction.EAST)
        self.east = self.check_view([forest[key] for key in east_keys])
        west_keys = self.gen_keys(Direction.WEST)
        self.west = self.check_view([forest[key] for key in west_keys])
        print(f"N{north_keys}, S{south_keys}, W{west_keys}, E{east_keys}, ")

    def gen_keys(self, direction: Direction):
        print(direction)
        result = []
        if direction == Direction.NORTH:
            for y in range(self.y - 1, -1, -1):
                key = f"{self.x},{y}"
                result.append(key)
        elif direction == Direction.SOUTH:
            for y in range(self.y + 1, self.forest_size, 1):
                key = f"{self.x},{y}"
                result.append(key)
        elif direction == Direction.WEST:
            for x in range(self.x - 1, -1, -1):
                key = f"{x},{self.y}"
                result.append(key)
        elif direction == Direction.EAST:
            for x in range(self.x + 1, self.forest_size, 1):
                key = f"{x},{self.y}"
                result.append(key)
        return result

    def __str__(self) -> str:
        return f"Tree({self.x}, {self.y}, {self.height}, {self.is_visible})"

    def __repr__(self) -> str:
        return str(self)


f = open("8/input.txt")


def count_trees(line: List[Tree]) -> List[Tree]:
    print(line)
    current_height = -1
    result = []
    for t in line:
        if t.height > current_height:
            t.is_visible = True
            result.append(t)
            current_height = t.height
    return result


forest = []
forest_d = {}
for x, l in enumerate(f.readlines()):
    forest.append([Tree(x, y, int(c)) for y, c in enumerate(l.strip())])
    for y, c in enumerate(l.strip()):
        key = f"{y},{x}"
        forest_d[key] = Tree(y, x, int(c), forest_size=len(l.strip()))

print(forest)
rotated = list(zip(*forest))[::-1]
print(rotated)
west = list(chain.from_iterable([count_trees(l) for l in forest]))
north = list(chain.from_iterable([count_trees(l) for l in rotated]))

print("west")
print(west)
print(north)
for i in range(len(forest)):
    forest[i].reverse()
    rotated[i] = list(rotated[i])
    rotated[i].reverse()
print(forest)
print(rotated)
east = list(chain.from_iterable([count_trees(l) for l in forest]))
south = list(chain.from_iterable([count_trees(l) for l in rotated]))
print(east)
print(south)
all_visible = west + north + east + south
result = {}
for tree in all_visible:
    key = f"{tree.x},{tree.y}"
    result[key] = tree
print(result)
print(len(result.items()))

winner = None
result = 0
print(forest_d)
for tree in forest_d.values():
    score = tree.check_and_calc(forest_d)
    print(f"tree({tree.x}, {tree.y}) score:{score}, N:{tree.north},S:{tree.south},E:{tree.east},W:{tree.west}")
    if score > result:
        result = score
        winner = tree
 
keys = list(forest_d.keys())
keys.sort()
for i, key in enumerate(keys):
    print(forest_d[key].scenic_score, end="")
    if (i+1) % 5 == 0:
        print("")
print(winner)
print(result)

# print(sum([west, north, east, south]))

f.close()
