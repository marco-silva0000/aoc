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



class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"

    def __lt__(self, other):
        return self.value < other.value


@dataclass()
class Node:
    position: Point
    cost: int
    path: Optional[List[Point]]
    direction: Direction = Direction.EAST


    def __str__(self):
        match self.direction:
            case Direction.NORTH:
                return "^"
            case Direction.SOUTH:
                return "v"
            case Direction.EAST:
                return ">"
            case Direction.WEST:
                return "<"

    def __repr__(self):
        return f"Node({self.position}, {self.cost}, {self.direction})"

    def neighbors(self, grid: Dict[Point, int], max_x: int, max_y: int, target: Point, average_cost) -> Iterable["Node"]:
        """Return all neighbors of this node that can be reached without crossing a wall.
        can only move in the same direction 3 times before having to turn 90 degrees"""
        from structlog import get_logger
        average_cost = 1
        logger = get_logger()
        
        east_point = Point(self.position.x + 1, self.position.y)
        west_point = Point(self.position.x - 1, self.position.y)
        south_point = Point(self.position.x, self.position.y + 1)
        north_point = Point(self.position.x, self.position.y - 1)
        east_cost = grid.get(east_point, 90)
        west_cost = grid.get(west_point, 90)
        south_cost = grid.get(south_point, 90)
        north_cost = grid.get(north_point, 90)

        east_node = Node(east_point, east_cost, [], Direction.EAST)
        west_node = Node(west_point,  west_cost, [], Direction.WEST)
        south_node = Node(south_point, south_cost, [], Direction.SOUTH)
        north_node = Node(north_point, north_cost, [], Direction.NORTH)
        neighbors = [
            east_node,
            west_node,
            south_node,
            north_node,
            ]
        logger.debug('neighbors pre filtering', neighbors=neighbors)
        n = east_node
        logger.debug('east conditions', one=(0 <= n.position.x < max_x), two=(0 <= n.position.y < max_y))

        if self.direction == Direction.EAST:
            opposite_direction = Direction.WEST
        elif self.direction == Direction.WEST:
            opposite_direction = Direction.EAST
        elif self.direction == Direction.NORTH:
            opposite_direction = Direction.SOUTH
        elif self.direction == Direction.SOUTH:
            opposite_direction = Direction.NORTH
        else:
            opposite_direction = None

        neighbors = filter(lambda n: n.direction != opposite_direction, neighbors)
        neighbors = filter(lambda n: (0 <= n.position.x < max_x) and (0 <= n.position.y < max_y), neighbors)
        logger.debug("neighbors", neighbors=neighbors)
        return neighbors

    def __lt__(self, other):
        return self.cost < other.cost


def print_grid(grid: Dict[Point, int], max_x: int, max_y: int, nodes=[]):
    # print(rays)
    print("*" * 2)

    for y in range(max_y):
        for x in range(max_x):
            # tile = grid.get(Point(x, y))
            point = Point(x, y)
            tile = grid[Point(x, y)]
            try:
                node_index = [n for n in nodes].index(point)
                print('#', end="")
            except ValueError:
                if tile is None:
                    print(".", end="")
                else:
                    print(tile, end="")
        print("")
grid: Dict[Point, int] = dict()

def part1(values_list) -> str:
    from structlog import get_logger
    logger = get_logger()
    # logger.debug("part")
    grid = dict()
    all_values = []
    for y, line in enumerate(values_list):
        for x, c in enumerate(line):
            all_values.append(int(c))
            grid[Point(x, y)] = int(c)
    max_x = len(values_list[0])
    max_y = len(values_list)
    average_cost = sum(all_values) / len(all_values)

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )

    structlog.contextvars.bind_contextvars(
        # iteration=i,
    )
    type State = tuple[Point, Direction, int] 
    start = Point(0, 0)
    end = Point(max_x - 1, max_y - 1)
    start_cost = grid[start]
    start_node = Node(start, start_cost, [], Direction.EAST)
    priority_queue = PriorityQueue()
    result = []
    i = 0
    came_from = dict()
    g_map = defaultdict(lambda: math.inf)
    f_map = defaultdict(lambda: math.inf)
    direction_map = defaultdict(lambda: {
        Direction.NORTH: math.inf,
        Direction.SOUTH: math.inf,
        Direction.EAST: math.inf,
        Direction.WEST: math.inf,
        })
    g_map[start_node.position] = 0
    direction_map[start_node.position][start_node.direction] = 0

    f_map[start_node.position] = 0 + max_x + max_y - 2
    start_state = (start_node.position, None, 1)
    priority_queue.put((f_map[start_node.position], start_state))
    def reconstruct_path(current: State) -> List[State]:
        total_path = [current]
        while current in came_from.keys():
            current = came_from.pop(current)
            total_path.insert(0, current)
        return total_path

    def get_neighbours(state: State)-> Iterable[State]:
        position, direction, chain = state
        east_point = Point(position.x + 1, position.y)
        west_point = Point(position.x - 1, position.y)
        south_point = Point(position.x, position.y + 1)
        north_point = Point(position.x, position.y - 1)
        east_state = (east_point, Direction.EAST, 0)
        west_state = (west_point, Direction.WEST, 0)
        south_state = (south_point, Direction.SOUTH, 0)
        north_state = (north_point, Direction.NORTH, 0)
        if direction == Direction.EAST:
            opposite_direction = Direction.WEST
        elif direction == Direction.WEST:
            opposite_direction = Direction.EAST
        elif direction == Direction.NORTH:
            opposite_direction = Direction.SOUTH
        elif direction == Direction.SOUTH:
            opposite_direction = Direction.NORTH

        match direction:
            case Direction.NORTH:
                north_state = (north_point, Direction.NORTH, chain+1)
            case Direction.SOUTH:
                south_state = (south_point, Direction.SOUTH, chain+1)
            case Direction.EAST:
                east_state = (east_point, Direction.EAST, chain+1)
            case Direction.WEST:
                west_state = (west_point, Direction.WEST, chain+1)
        neighbors = [east_state, west_state, south_state, north_state]
        neighbors = filter(lambda n: n[1] != opposite_direction, neighbors)
        neighbors = filter(lambda n: (0 <= n[0].x < max_x) and (0 <= n[0].y < max_y), neighbors)
        return neighbors

    max_chain = 3
    min_chain_before_turn = 0
    def get_neighbours(state):
        pos, direction, chain_length = state
        match direction:
            case Direction.NORTH:
                direction = Point(0, -1)
            case Direction.SOUTH:
                direction = Point(0, 1)
            case Direction.EAST:
                direction = Point(1, 0)
            case Direction.WEST:
                direction = Point(-1, 0)
        for delta in (Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)):
            if direction is not None:
                if delta == -direction:
                    continue
                if delta == direction and chain_length == max_chain:
                    continue
                if delta not in (-direction, direction) and chain_length < min_chain_before_turn:
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
    while priority_queue.qsize() > 0:
        i += 1
        # current = nodes.pop(0)
        _, (current_position, current_direction, current_chain) = priority_queue.get()
        if current_position == end:
            result = g_map[current_position]
            print(result)
            print(result)
            print(result)
            print(result)
            print(result)
            result = reconstruct_path(current_position)
            break

        # print_grid(grid, max_x, max_y, current)
        logger = logger.bind(i=i, current_position=current_position, current_direction=current_direction, current_chain=current_chain)

        for (neighbor_position, neighbor_direction, neighbor_chain) in get_neighbours((current_position, current_direction, current_chain)):
            tentaive_g_score = g_map[current_position] + grid[neighbor_position]
            if tentaive_g_score < g_map[neighbor_position]:
                if neighbor_direction == current_direction:
                    if neighbor_chain >= 3:
                        continue
                    else:
                        current_chain = neighbor_chain + 1
                came_from[neighbor_position] = current_position
                g_map[neighbor_position] = tentaive_g_score
                f_map[neighbor_position] = tentaive_g_score + (abs(neighbor_position.x - end.x) + abs(neighbor_position.y - end.y))
                queue_states = [item[1] for item in priority_queue.queue]
                logger.debug("queue states", queue_states=queue_states)
                # input()
                if (neighbor_position, neighbor_direction, neighbor_chain) not in queue_states:
                    logger.debug("adding to queue", neighbor_position=neighbor_position, neighbor_direction=neighbor_direction, neighbor_chain=neighbor_chain, f_map=f_map[neighbor_position])
                    priority_queue.put((f_map[neighbor_position], (neighbor_position, neighbor_direction, neighbor_chain)))
                else:
                    logger.debug("already in queue", neighbor_position=neighbor_position, neighbor_direction=neighbor_direction, neighbor_chain=neighbor_chain, f_map=f_map[neighbor_position])
                    # input()

    print_grid(grid, max_x, max_y, result)
    result2 = sum([grid[node] for node in result]) - start_cost

    print(result)
    print(result2)
    return f"{result2}"

def part1(values_list) -> str:
    grid = dict()
    for y, line in enumerate(values_list):
        for x, c in enumerate(line):
            grid[Point(x, y)] = int(c)
    max_x = len(values_list[0])
    max_y = len(values_list)
    type State = tuple[Point, Point, int] 

    def a_star(start_state, goal_pos, min_chain_before_turn, max_chain):
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
                    if delta not in (-direction, direction) and chain_length < min_chain_before_turn:
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

        while not q.empty():
            f_dist, current_state = q.get()
            (current_position, current_direction, current_chain) = current_state
            if current_position == goal_pos:
                return heat_loss[current_state]
            if f_dist > heat_loss[current_state] + h(current_state):
                continue
            for neighbor_state in get_neighbours(current_state):
                neighbor_position = neighbor_state[0]
                g_dist = heat_loss[current_state] + grid[neighbor_position]
                if neighbor_state in heat_loss and heat_loss[neighbor_state] <= g_dist:
                    continue
                heat_loss[neighbor_state] = g_dist
                q.put((heat_loss[neighbor_state] + h(neighbor_state), neighbor_state))

    start_state = (Point(0, 0), None, 1)
    goal_pos = Point(max_x-1, max_y-1)
    
    result = a_star(start_state, goal_pos, 0, 3)
    return f"{result}"

