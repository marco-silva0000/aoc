from typing import List, Set, Dict, Tuple, Optional, Union, Self
import logging
import math
from structlog import get_logger
from dataclasses import dataclass
from itertools import cycle

log = get_logger()


def print_world(
    world,
    min_x,
    max_x,
    min_y,
    max_y,
    marked_x_for_expansion=None,
    marked_y_for_expansion=None,
):
    print(f"  ", end="")
    for x in range(min_x, max_x + 1):
        print(x % 10, end="")
    print()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if x == min_x:
                print(f"{y % 10}:", end="")
            if (marked_x_for_expansion and x in marked_x_for_expansion) or (
                marked_y_for_expansion and y in marked_y_for_expansion
            ):
                print("⚫", end="")
            elif (x, y) in world.keys():
                print("🌌", end="")
            else:
                print("⬛", end="")
        print()


def part2(values_list, expansion=1) -> str:
    if expansion > 1:
        expansion -= 1
    galaxies = {}
    length = len(values_list[0])
    height = len(values_list)
    count = 1
    for y, line in enumerate(values_list):
        for x, value in enumerate(line):
            if value == "#":
                galaxies[(x, y)] = count
                count += 1
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
    print_world(
        galaxies, 0, length, 0, height, marked_x_for_expansion, marked_y_for_expansion
    )

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
                abs(g1[0] - (g2[0]))
                + x_between * expansion
                + abs(g1[1] - (g2[1]))
                + y_between * expansion
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
