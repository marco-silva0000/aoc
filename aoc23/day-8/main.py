from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
from structlog import get_logger
from dataclasses import dataclass
from itertools import cycle

log = get_logger()

f = open("8/test.txt")
f = open("8/input.txt")
skip_part_1 = False

@dataclass()
class Node():
    name: str
    neighbour_list: List[str]
    l: str
    r: str
    finished_in: int = 0

lines = f.readlines()
lines = iter(lines)

node_map = dict()

instructions = next(lines)
instructions = instructions.strip()

next(lines)
for line in lines:
    line = line.strip()
    name, neigbours = line.split(" = ")
    neigbours = neigbours.removeprefix("(")
    neigbours = neigbours.removesuffix(")")
    # print(neigbours)
    neigbour_list = neigbours.split(", ")
    neighbour_l = neigbour_list[0]
    neighbour_r = neigbour_list[1]
    node_map[name] = Node(name, neigbour_list, neighbour_l, neighbour_r)

if not skip_part_1:
    # print(node_map)
    current_node = node_map["AAA"]
    goal_node = node_map["ZZZ"]
    steps = 0
    for instruction in cycle(instructions):
        if current_node == goal_node or current_node.name == "ZZZ":
            print("part1:", steps)
            break
        next_node_name = current_node.l if instruction.lower() == "l" else current_node.r
        current_node = node_map[next_node_name]
        steps += 1


# part 2
current_nodes = [node_map[node] for node in node_map.keys() if node.endswith("A")]
# print(current_nodes)
# exit()
steps = 0
finished_nodes = [0 for _ in range(len(current_nodes))]
for instruction in cycle(instructions):
    try:
        next(n for n in current_nodes if not n.name.endswith("Z"))
        next(n for n in finished_nodes if n == 0)
    except StopIteration:
        print("part2:", math.lcm(*finished_nodes))
        break
    next_nodes = []
    steps += 1
    if steps % 100000 == 0:
        pass
        # print(steps)
    for i, current_node in enumerate(current_nodes):
        next_node_name = current_node.l if instruction.lower() == "l" else current_node.r
        next_node = node_map[next_node_name]
        if next_node.name.endswith("Z") and next_node.finished_in == 0:
            finished_nodes[i] = steps

        next_nodes.append(next_node)
    current_nodes = next_nodes



