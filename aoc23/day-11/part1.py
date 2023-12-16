from typing import List, Set, Dict, Tuple, Optional, Union, Self
import logging
import math
from structlog import get_logger
from dataclasses import dataclass
from itertools import cycle

log = get_logger()


@dataclass
class Point:
    x: int
    y: int
    id: int
    value: str
    distances: Optional[List[int]] = None

    def __str__(self):
        return f"{self.value}"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.y < other.y:
            return True
        elif self.y == other.y:
            return self.x < other.x
        return False


def print_values(values_list):
    for line in values_list:
        print(line)


def print_world(world, min_x, max_x, min_y, max_y, lengths=False):
    print(f"  ", end="")
    for x in range(min_x, max_x + 1):
        print(x % 10, end="")
    print()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if x == min_x:
                print(f"{y % 10}:", end="")
            if (x, y) in world.keys():
                if lengths:
                    print(world[(x, y)], end="")
                else:
                    print(world[(x, y)], end="")
            else:
                print(".", end="")
        print()


def part1(values_list) -> str:
    galaxies = {}
    length = len(values_list[0])
    height = len(values_list)
    count = 1
    for y, line in enumerate(values_list):
        for x, value in enumerate(line):
            if value == "#":
                galaxies[(x, y)] = count
                count += 1
    print_world(galaxies, 0, length, 0, height)
    y_keys = set([p[1] for p in galaxies.keys()])
    x_keys = set([p[0] for p in galaxies.keys()])

    marked_x_for_expansion = set()
    marked_y_for_expansion = set()
    for x in range(0, length):
        if x not in x_keys:
            marked_x_for_expansion.add(x)
    for y in range(0, height):
        if y not in y_keys:
            marked_y_for_expansion.add(y)

    distances_map = {}
    for g1 in galaxies.keys():
        for g2 in galaxies.keys():
            if g1 == g2:
                continue
            x_between = len(
                [
                    x
                    for x in marked_x_for_expansion
                    if (x > g1[0] and x < g2[0]) or (x > g2[0] and x < g1[0])
                ]
            )
            y_between = len(
                [
                    y
                    for y in marked_y_for_expansion
                    if (y > g1[1] and y < g2[1]) or (y > g2[1] and y < g1[1])
                ]
            )
            distance = (
                abs(g1[0] - (g2[0])) + x_between + abs(g1[1] - (g2[1])) + y_between
            )
            if (g1, g2) not in distances_map.keys() and (
                g2,
                g1,
            ) not in distances_map.keys():
                # log.debug("distance", g1=g1, g2=g2, distance=distance, x_between=x_between, y_between=y_between, id1=galaxies[g1], id2=galaxies[g2])
                distances_map[(g1, g2)] = distance

    # for key, value in distances_map.items():
    #     print(key, value)
    result = str(sum(distances_map.values()))
    print(len(distances_map.keys()))
    print(result)
    return str(sum(distances_map.values()))

    new_height = height + len(marked_y_for_expansion)
    new_length = length + len(marked_x_for_expansion)
    for i, x in enumerate(marked_x_for_expansion):
        log.debug("inserting", x=x)
        for y in range(0, height):
            values_list[y].insert(x + 1, "x")
        print_values(values_list)

    for i, y in enumerate(marked_y_for_expansion):
        log.debug("inserting", y=y)
        values_list.insert(y + i, ["x"] * (new_length))
        print_values(values_list)

    world = {}
    galaxies = {}
    length = new_length
    height = new_height
    for y, line in enumerate(values_list):
        for x, value in enumerate(line):
            point = Point(x, y, ".")
            if value == "#":
                point.value = "#"
                galaxies[(x, y)] = point
            world[(x, y)] = point
    print_world(world, 0, length, 0, height)

    distances_map = {}
    for p1 in galaxies.keys():
        distances = []
        for p2 in galaxies.keys():
            if p1 == p2:
                continue
            distance = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
            distances.append(distance)
            if (p1, p2) not in distances_map.keys() and (
                p2,
                p1,
            ) not in distances_map.keys():
                distances_map[(p1, p2)] = distance

        world[p1].distances = distances
    print_world(world, 0, length, 0, height, lengths=True)
    all_distances = list(distances_map.values())
    for key, value in distances_map.items():
        print(key, value)
    print_world(world, 0, length, 0, height, lengths=True)
    print(len(all_distances))
    return str(sum(all_distances))
