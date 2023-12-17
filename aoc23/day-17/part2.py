from collections import defaultdict
from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum
from queue import PriorityQueue
logger = structlog.get_logger()


@dataclass()
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __neg__(self):
        return Point(x=-self.x, y=-self.y)

    def dist(self, other):
        # manhattan
        return abs(self.x - other.x) + abs(self.y - other.y)


def print_grid(grid: Dict[Point, int], max_x: int, max_y: int, nodes=[]):
    # print(rays)
    print("*" * 2)

    for y in range(max_y):
        for x in range(max_x):
            # tile = grid.get(Point(x, y))
            point = Point(x, y)
            tile = grid[Point(x, y)]
            try:
                node_index = [n[0] for n in nodes].index(point)
                direction = nodes[node_index][1]
                if direction == Point(1, 0):
                    print(">", end="")
                elif direction == Point(-1, 0):
                    print("<", end="")
                elif direction == Point(0, 1):
                    print("v", end="")
                else:
                    print("^", end="")
            except ValueError:
                if tile is None:
                    print(".", end="")
                else:
                    print(tile, end="")
        print("")
grid: Dict[Point, int] = dict()


def part2(values_list) -> str:
    grid = dict()
    for y, line in enumerate(values_list):
        for x, c in enumerate(line):
            grid[Point(x, y)] = int(c)
    max_x = len(values_list[0])
    max_y = len(values_list)
    type State = tuple[Point, Point, int] 

    def a_star(start_state, goal_pos, min_chain_before_turn, max_chain):
        def reconstruct_path(came_from, current):
            total_path = [current]
            while current in came_from.keys():
                current = came_from.pop(current)
                total_path.insert(0, current)
            return total_path
        def h(state):
            pos, _direction, _chain_length = state
            return pos.dist(goal_pos)

        def get_neighbours(state: State)-> Iterable[State]:
            pos, direction, chain_length = state
            for delta in (Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)):
                if direction is not None:
                    if delta == -direction:
                        continue
                    if delta == direction and chain_length == max_chain:
                        continue
                    if delta !=direction and chain_length < min_chain_before_turn:
                        continue
                new_pos = pos + delta
                if not (0 <= new_pos.x < max_x and 0 <= new_pos.y < max_y):
                    continue
                new_direction = delta
                if new_direction != direction:
                    new_chain_length = 1
                else:
                    new_chain_length = chain_length + 1
                yield new_pos, new_direction, new_chain_length

        q = PriorityQueue()
        heat_loss = {start_state: 0}
        q.put((heat_loss[start_state] + h(start_state), start_state))
        came_from = dict()


        while not q.empty():
            f_dist, current_state = q.get()
            (current_position, current_direction, current_chain) = current_state
            if current_position == goal_pos:
                path = reconstruct_path(came_from, current_state)
                return heat_loss[current_state], path
            if f_dist > heat_loss[current_state] + h(current_state):
                continue
            for neighbor_state in get_neighbours(current_state):
                neighbor_position = neighbor_state[0]
                g_dist = heat_loss[current_state] + grid[neighbor_position]
                came_from[neighbor_state] = current_state
                if neighbor_state in heat_loss and heat_loss[neighbor_state] <= g_dist:
                    continue
                heat_loss[neighbor_state] = g_dist
                q.put((heat_loss[neighbor_state] + h(neighbor_state), neighbor_state))

    start_state = (Point(0, 0), None, 1)
    goal_pos = Point(max_x-1, max_y-1)
    
    result, nodes = a_star(start_state, goal_pos, 4, 10)
    print(result)
    print_grid(grid, max_x, max_y, nodes)
    return f"{result}"

