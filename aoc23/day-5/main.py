from typing import List, Set, Dict, Tuple, Optional, Union
import threading
from copy import deepcopy

f = open("5/test.txt")
f = open("5/input.txt")

Range = Tuple[int, int, int]

class Mapy:
    def __init__(self, from_map: str, to_map: str, ranges: List[Range]):
        self.from_map = from_map
        self.to_map = to_map
        self.ranges = ranges

    def __repr__(self):
        return f"Mapy({self.from_map}, {self.to_map}, {self.ranges})"

    def __str__(self):
        return f"Mapy({self.from_map}, {self.to_map}, {self.ranges})"

    def add_range(self, range: Range):
        self.ranges.append(range)

    def find_range_subset(self, start: int, end:int) -> List[Tuple[int, int]]:
        result = []
        for (this_start, next_start, length) in self.ranges:
            if start >= this_start and start < this_start + length: 
                new_start_diff = start - this_start
                if end <= this_start + length:
                    # print(1)
                    end_diff = end - start
                    # print(f"next_start: {next_start}, new_start_diff: {new_start_diff}, end_diff: {end_diff}")
                    result.append((next_start + new_start_diff, next_start + new_start_diff + end_diff,))
                    # print(f"result: {result}")
                    return result
                else:
                    # print(2)
                    next_start_diff = next_start - this_start
                    result.append((start + next_start_diff, this_start + length + next_start_diff))
                    start = this_start + length
        else:
            # print(3)
            result.append((start, end))
            return result

    def propagate_ranges(self, min_max: List[int], target: str) -> List[Tuple[int, int]]:
        # print(f"propagating {min_max} from {self.from_map} to {self.to_map}")
        finish = False
        if self.to_map == target:
            finish = True
        start, end = min_max
        ranges = self.find_range_subset(start, end)
        # print(f"ranges: {ranges}")

        if not finish:
            target_mapy = deepcopy(globals()[self.to_map+"_map"])
            # print(f"target_mapy: {target_mapy}")
            result = []
            for r in ranges:
                result += target_mapy.propagate_ranges(r, target)
            return result
        else:
            return ranges


    def fix_ranges(self):
        self.ranges.sort(key=lambda x: x[0])
        first_start = self.ranges[0][0]
        if first_start != 0:
            self.ranges.insert(0, (0, 0, first_start))
        self.ranges.sort(key=lambda x: x[0])
        ranges = iter(self.ranges)
        prev = next(ranges)
        ranges_copy = deepcopy(self.ranges)

        for r in ranges:
            this_start, _, _ = r
            prev_start, _, prev_length = prev
            if this_start != prev_start + prev_length:
                ranges_copy.insert(0, (prev_start + prev_length, this_start, this_start - (prev_start + prev_length)))
            prev = r
        self.ranges = ranges_copy
        self.ranges.sort(key=lambda x: x[0])



    def __getitem__(self, key: int) -> int:
        for r in self.ranges:
            this_start, that_start, length = r
            if key >= this_start and key < this_start + length:
                diff = (key - this_start)
                # print(f"key: {key}, this_start: {this_start}, that_start: {that_start}, diff: {diff}")
                return that_start + diff
        return key
        raise KeyError(f"key {key} not found in {self.ranges}")

my_iter = iter(f.readlines())
l = next(my_iter)
l = l.strip()
print(l)
_, *seeds = l.split()
print(seeds)
seeds = list(map(int, seeds))
next(my_iter)  # empty line

for l in my_iter:
    l = l.strip()
    print(l)
    from_map, to_map = l.split("-to-")
    to_map = to_map.removesuffix(" map:")
    # print(from_map)
    # print(to_map)
    mapy = Mapy(from_map, to_map, [])
    globals()[from_map+"_map"] = mapy
    while (l:=next(my_iter).strip()) != "":
        first, second, len = tuple(map(int, l.split()))
        mapy.add_range((second, first, len,))
    mapy.fix_ranges()

def walk_mapy(mapy: Mapy, id: int, destination_map: str) -> int:
    # print(f"walking {mapy.from_map} from {id} to {destination_map}")
    # print(f"mapy: {mapy}")

    if mapy.to_map == destination_map:
        return mapy[id]
    target_mapy = globals()[mapy.to_map+"_map"]
    # print(f"target_mapy: {target_mapy}")
    target = mapy[id]
    # print(f"target: {target}")
    return walk_mapy(target_mapy, target, destination_map)

seed_locations = []
for seed in seeds:
    mapy = globals()["seed_map"]
    seed_locations.append(walk_mapy(mapy, seed, "location"))

part2_seeds = []
seed_iter = iter(seeds)
for seed in seed_iter:
    length = next(seed_iter)
    part2_seeds.append((seed, seed + length))

print(seed_locations)
current_min = min(seed_locations)
print(current_min)

print(part2_seeds)
current_min = 2**64

def calc_range(seed_start, seed_end):
    mapy = globals()["seed_map"]
    c_min = 2**32
    for i in range(seed_start, seed_end):
        result = walk_mapy(mapy, i, "location")
        if result < c_min:
            c_min = result
    return c_min

# for seed_start, seed_end in part2_seeds:
#     result = calc_range(seed_start, seed_end)
#     if result < current_min:
#         current_min = result
# got result in almost 3 hours

seedy_mapy = deepcopy(globals()["seed_map"])
part2 = []
for start, end in part2_seeds:
    part2.extend(seedy_mapy.propagate_ranges([start, end], "location"))
print(part2)
print(min(part2, key=lambda x: x[0]))

print("part2 should be 46 then 26714516")


