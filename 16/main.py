from typing import Dict, Tuple, List
import threading
import concurrent.futures
from collections import defaultdict
from enum import Enum
from itertools import chain
import heapq



class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f

    def return_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current.position)
            current = current.parent
        return path[::-1]  # Return reversed path

    def return_path_nodes(self):
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # Return reversed path


def astar(graph, start, end):
    # Create start and end node 
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)


    while len(open_list) > 0:
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return current_node.return_path()

        # Generate c    hildren
        # print(f"current: {current_node.position}")
        children = [Node(current_node, neighbor) for neighbor in graph[current_node.position]]
         
        # Loop through children
        for child in children:
            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = 0
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_list:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)
    raise ValueError("can't find path")


f = open("16/input.txt")
graph : Dict[str, List[str]] = dict()
flow_rates = dict()

for i, l in enumerate(f.readlines()):
    l = l.strip()
    print(l)
    valve_str, tunnels_str = l.split("; ")
    print(valve_str)
    valve_str = valve_str.removeprefix("Valve ")
    valve_id = valve_str.split(" ")[0]
    flow_rate = int(valve_str.split(" ")[-1].removeprefix("rate="))
    tunnels = tunnels_str.split(" ")[4:]
    graph[valve_id] = [tunnel.removesuffix(",") for tunnel in tunnels]
    flow_rates[valve_id] = flow_rate
print(graph)
print(flow_rates)
f.close()

def find_distance(graph, this, that):
    result = len(astar(graph, this, that)) - 1
    print(f"distance from {this} to {that} is {result}")
    return result

def path_to_target(graph, current, target):
    path = astar(graph, current, target)
    return path


distances: Dict[Tuple[str, str], int] = dict()
paths_to_target: Dict[Tuple[str, str], List[str]] = dict()

for this in graph.keys():
    for that in graph.keys():
        path = path_to_target(graph, this, that)
        distances[(this, that)] = len(path) - 1
        paths_to_target[(this, that)] = path


def get_open_neighbors_with_cost(graph, this, closed, cost=1):
    neighbors = graph[this]
    return [(neighbor, cost,) for neighbor in neighbors if neighbor not in closed]

_closable_valves = [key for key in graph.keys() if flow_rates[key] != 0]

def closed_valves(open):
    result = [key for key in _closable_valves if key not in open]
    return result


class Path:
    def __init__(self, parent=None, position=''):
        self.parent = parent
        self.position = position
        self.open_valves = []

        self.move_cost = 0
        self.added_flow_rate = 0
        self.score_til_here = 0
        self.time_spent = 0

    def __eq__(self, other):
        return self.position == other.position and self.score_til_here == other.score_til_here
    
    def __repr__(self):
      return f"{self.position} - move_cost: {self.move_cost} added_flow_rate: {self.added_flow_rate} time_spent: {self.time_spent} score_til_here: {self.score_til_here}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.score_til_here > other.score_til_here
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.score_til_here < other.score_til_here

    def return_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current.position)
            current = current.parent
        return path[::-1]  # Return reversed path

    def return_path_nodes(self):
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # Return reversed path


def astar_path(graph, start, max_length=30):
    # Create start and end node
    start_node = Path(None, start)
    best = start_node

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)
    iters = 0


    while len(open_list) > 0:
        iters += 1
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        closed_valve_list = closed_valves(current_node.open_valves)

        if current_node < best:
            best = current_node

        # Found the goal
        if closed_valves == []:
            return current_node.return_path()


        # Generate children
        # print(f"current: {current_node.position}")
        children = [Path(current_node, valve) for valve in closed_valve_list]
         
        if iters % 1000 == 0:
            print('best', best)
            print('best', best.return_path())
            print('current', current_node.return_path())

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            processes = []
            for child in children:
                processes.append(executor.submit(process_child, child, current_node, closed_list, open_list, max_length))
            for _ in concurrent.futures.as_completed(processes):
                result = _.result()
                if result:
                    heapq.heappush(open_list, result)
        # # Loop through children
        # for child in children:
        #     # Child is on the closed list
        #     if child in closed_list:
        #         continue
        #     # Child is already in the open list
        #     if child in open_list:
        #         continue


        #     child.move_cost = distances[current_node.position, child.position]
        #     # Create the f, g, and h values
        #     child.time_spent = current_node.time_spent + child.move_cost + 1
        #     if child.time_spent > max_length:
        #         continue
        #     child.added_flow_rate = (max_length-child.time_spent)*flow_rates[child.position]
        #     child.score_til_here = current_node.score_til_here +  child.added_flow_rate

        #     child.open_valves = current_node.open_valves.copy()
        #     child.open_valves.append(child.position)
        #     # Add the child to the open list
        #     heapq.heappush(open_list, child)
    return best

class Path2:
    def __init__(self, parent=None, position_me='', position_ele=''):
        self.parent = parent
        self.position_me = position_me
        self.position_ele = position_ele

        self.open_valves = []
        self.move_cost = 0
        self.move_cost_ele = 0
        self.added_flow_rate = 0
        self.added_flow_rate_ele = 0
        self.score_til_here = 0
        self.time_spent = 0
        self.time_spent_ele = 0

    def __eq__(self, other):
        return self.position_me == other.position_me and self.position_ele == other.position_ele and self.score_til_here == other.score_til_here
    
    def __repr__(self):
        return f"{self.position_me} ele:{self.position_ele} path: {self.return_path_me()} - path_ele: {self.return_path_ele()} - added_flow_rate: {self.added_flow_rate} added_flow_rate_ele: {self.added_flow_rate_ele} time_spent: {self.time_spent} time_spent_ele: {self.time_spent_ele} score_til_here: {self.score_til_here}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.score_til_here > other.score_til_here
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.score_til_here < other.score_til_here

    def return_path_me(self):
        path = []
        current = self
        while current is not None:
            path.append(current.position_me)
            current = current.parent
        return path[::-1]  # Return reversed path

    def return_path_ele(self):
        path = []
        current = self
        while current is not None:
            path.append(current.position_ele)
            current = current.parent
        return path[::-1]  # Return reversed path

    def return_path_nodes(self):
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # Return reversed path


def astar_path2(graph, start, max_length=30):
    # Create start and end node
    start_node = Path2(None, start, start)
    best = start_node

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)
    iters = 0


    while len(open_list) > 0:
        iters += 1
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        closed_valve_list = closed_valves(current_node.open_valves)

        if current_node < best:
            print(closed_valve_list)
            print("found best")
            print('bestme', best.return_path_me())
            print('bestele', best.return_path_ele())
            print('current', current_node.return_path_me(), current_node.return_path_ele())
            best = current_node

        # Found the goal
        if closed_valves == []:
            return current_node.return_path_nodes()


        # Generate children
        # print(f"current: {current_node.position}")
        children = []
        for my_valve in closed_valve_list:
            for ele_valve in closed_valve_list:
                if my_valve != ele_valve:
                    if current_node.position_me == '':
                        my_valve = ''
                    if current_node.position_ele == '':
                        ele_valve = ''
                    children.append(Path2(current_node, my_valve, ele_valve))
         
        if iters % 1000 == 0:
            print('current best', best)
            print('current', current_node.return_path_me(), current_node.return_path_ele())

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            processes = []
            for child in children:
                processes.append(executor.submit(process_child2, child, current_node, closed_list, open_list, max_length))
            for _ in concurrent.futures.as_completed(processes):
                result = _.result()
                if result:
                    heapq.heappush(open_list, result)
        # # Loop through children
        # for child in children:
        #     # Child is on the closed list
        #     if child in closed_list:
        #         continue
        #     # Child is already in the open list
        #     if child in open_list:
        #         continue


        #     child.move_cost = distances[current_node.position, child.position]
        #     # Create the f, g, and h values
        #     child.time_spent = current_node.time_spent + child.move_cost + 1
        #     if child.time_spent > max_length:
        #         continue
        #     child.added_flow_rate = (max_length-child.time_spent)*flow_rates[child.position]
        #     child.score_til_here = current_node.score_til_here +  child.added_flow_rate

        #     child.open_valves = current_node.open_valves.copy()
        #     child.open_valves.append(child.position)
        #     # Add the child to the open list
        #     heapq.heappush(open_list, child)
    return best

def process_child(child: Path, current_node:Path, closed_list, open_list, max_length):
        # Child is on the closed list
        # if child in closed_list:
            # return None
        # Child is already in the open list
        # if child in open_list:
            # return None

        child.move_cost = distances[current_node.position, child.position]
        # Create the f, g, and h values
        child.time_spent = current_node.time_spent + child.move_cost + 1
        if child.time_spent > max_length:
            return None
        child.added_flow_rate = (max_length-child.time_spent)*flow_rates[child.position]
        child.score_til_here = current_node.score_til_here +  child.added_flow_rate

        child.open_valves = current_node.open_valves.copy()
        child.open_valves.append(child.position)
        return child

def process_child2(child: Path2, current_node:Path2, closed_list, open_list, max_length):

        if current_node.position_me != '':
            child.move_cost = distances[current_node.position_me, child.position_me]
            child.time_spent = current_node.time_spent + child.move_cost + 1

        if current_node.position_ele != '':
            child.move_cost_ele = distances[current_node.position_ele, child.position_ele]
            # Create the f, g, and h values
            child.time_spent_ele = current_node.time_spent_ele + child.move_cost_ele + 1

        if child.time_spent > max_length:
            child.position_me = ''
        if child.time_spent_ele > max_length:
            child.position_ele = ''

        child.score_til_here = current_node.score_til_here
        open_valves = current_node.open_valves.copy()
        if child.position_me != '':
            child.added_flow_rate = (max_length-child.time_spent)*flow_rates[child.position_me]
            child.score_til_here += child.added_flow_rate
            open_valves.append(child.position_me)

        if child.position_ele != '':
            child.added_flow_rate_ele = (max_length-child.time_spent_ele)*flow_rates[child.position_ele]
            child.score_til_here += child.added_flow_rate_ele
            child.open_valves = current_node.open_valves.copy()
            open_valves.append(child.position_ele)

        if child.position_me == '' and child.position_ele == '':
            return None
        child.open_valves = open_valves
        return child

def find_best(current, open, time_left):
    closed_list = closed_valves(open)
    cost = [((time_left - distances[(current, target)]-1)*flow_rates[target], target ,) for target in closed_list]
    cost.sort(key=lambda x: x[0], reverse=True)
    print("cost", cost)
    return cost[0][1]


def estimate_best(graph, flow_rates, current, open, minutes_left, real=False):

    closed_flow_rates = [(value,  key) for key, value in flow_rates.items() if key not in open and value != 0]
    closed_flow_rates.sort(key=lambda x: x[0], reverse=True)
    weighted = [(value*(minutes_left - distances[(current, key)]), key) for value, key in closed_flow_rates]
    weighted.sort(key=lambda x: x[0], reverse=True)


    # Simulate for first 5
    results = []
    candidates = [key for _, key in weighted[:5]]
    if real:
        print("will sim next", candidates)
        print("will sim next weighted", weighted)
    paths = set()
    for candidate in candidates:
        path = paths_to_target[(current, candidate,)]
        if len(path) > 1:
            paths.add(path[1])
        else:
            paths.add(path[0])

            
    if real:
        print("will sim next set", paths)
        print("current", current)

    for candidate in paths:
        candidate_open = open.copy()
        result = 0
        if candidate == current:
            candidate_open.append(candidate)
            result = flow_rates[candidate]*(minutes_left-1)

        result += try_from(minutes_left - 1, graph, candidate_open, candidate)

        results.append((result, candidate),)
    results.sort(key=lambda x: x[0], reverse=True)
    if real:
        print(results)
    if results:
        return results[0][1]
    else:
        if len(weighted):
            return weighted[0][1]
        else:
            return current


def try_from(total_time, graph, open, current, real=False):
    minute = 0
    released_pressure = 0
    added_pressure = 0
    while minute < total_time and len(open) != len(graph.keys()):
        minute += 1
        minutes_left = total_time - minute
        if real:
            print(f"\n== Minute {minute} ==")
        if added_pressure:
            if real:
                print(f"Valve {open[-1]} was opened releasing a total of {added_pressure}")
            released_pressure += added_pressure
            added_pressure = 0
        best = estimate_best(graph, flow_rates, current, open, minutes_left, real=real)
        target = best
        if real:
            print(f"Best is to move to {target}")
        current_flow_rate = flow_rates[current]
        if current == target:
            if real:
                print(f"You open valve {current}")
            open.append(current)
            added_pressure = current_flow_rate * (minutes_left)
            continue
        path = paths_to_target[(current, target)]
        if real:
            print(f"moving from {current} to {target} because of path {path}")
        current = path[1]
        if real:
            print(f"You move to valve {current}")
    return released_pressure

def print_simplify(path: List[str]):
    prev = path[0]
    print(f"{prev}", end="")
    for p in path[1:]:
        if prev == p:
            print(f"->", end="")
            print(f"{p}", end="")
        prev = p
    print(f"")

def walk_all(total_time, garph, open, current):
    connections = []

    pass

def print_costs():
    keys = list(graph.keys())
    keys.sort()
    for this in keys:
        print(f"{this}:")
        for that in keys:
            print("\t" + f"{that} {distances[(this, that)]} {paths_to_target[(this, that)]}")

def solution(start, total_time):
    open = []
    closed = closed_valves(open)
    time_left = total_time
    current = start
    result = 0
    while len(closed) > 1 or time_left:
        print(f'in {current}')
        target = find_best(current, open, time_left)
        if current == target:
            print(f'opening {current}')
            result += (time_left-1)*flow_rates[current]
            open.append(current)
        else:
            current = paths_to_target[(current, target)]
            print(f'moving to {current}')
            time_left -= 1

        print("")
    return result

def find_all_options(current_path: List[str], open, max_length=30) -> List[List[str]]:
    result: List[List[str]] = []
    closed_list = closed_valves(open)
    current = current_path[-1]

    for candidate in closed_list:
        path = current_path + paths_to_target[(current, candidate)][1:] 
        len_path = len(path)
        if max_length - len_path < 8:
            print_simplify(current_path)
            result.extend([path])

        if len_path + 1 == max_length:
            path.append(candidate)
            result.extend([path])
        elif len_path + 1 > max_length:
            continue
        else:
            new_open = open.copy()
            new_open.append(candidate)
            path.append(candidate)
            result.extend(find_all_options(path, new_open, max_length))
    return result


def calculate_option(path: List[str], minutes_left, real=None):
    result = 0
    if path != []:
        current = path.pop(0)
        next = path[0]
        if current == next:
            if real and "FA" == current:
                print(f"calculate_option {real}", path)
                print_simplify(path)
            # open valve 
            current = path.pop(0)
            result += (minutes_left - 1) * flow_rates[current]
            if len(path) > 1:
                result += calculate_option(path, minutes_left - 2)
            else:
                return result
        else:
            result += calculate_option(path, minutes_left - 1)
            # move
    return result


test = 1651
test1 = 2640
def part1(graph: Dict, flow_rates: Dict):
    start = "AA"
    current = start
    minute = 0
    total_time = 30
    open = []
    released_pressure = 0
    added_pressure = 0
    # print_costs()
    all_options = find_all_options([start], open, max_length=total_time)
    result = []
    for i, option in enumerate(all_options):
        opt_copy = option.copy()
        # print(option)
        result.append((calculate_option(option, total_time, real=f"{i}/{len(all_options)}"), opt_copy))
    print(len(all_options))

    result.sort(key= lambda x: x[0], reverse=True)
    print_simplify(result[0][1])
    return result[0]


def part1(graph: Dict, flow_rates: Dict):
    start = "AA"
    current = start
    minute = 0
    total_time = 30
    open = []
    released_pressure = 0
    added_pressure = 0
    # print_costs()
    result = astar_path(graph, start, total_time)
    print(result)
    print(result.return_path())
    print(result.score_til_here)
    print_simplify(result.return_path())
    return result.return_path()


    # return solution(start, total_time)
def part2(graph: Dict, flow_rates: Dict):
    start = "AA"
    total_time = 26

    result = astar_path2(graph, start, total_time)
    print(result)
    print(result.return_path_nodes())
    print(result.score_til_here)
    print_simplify(result.return_path_me())
    print_simplify(result.return_path_ele())
    return result.score_til_here


    # return solution(start, total_time)



print(part2(graph, flow_rates))

