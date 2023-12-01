import heapq
from itertools import cycle
import threading
import concurrent.futures


def print_map(map, result):
    letters = "ABCDEFGHIJKLMNOPQRSTUVXYZ" * 200
    letters = "🔴🟠🟡🟢🔵🟣🟤⚫⚪🟥🟧🟨🟩🟦🟪🟫⬛" * 300

    for y, line in enumerate(map):
        for x, v in enumerate(line):
            if (x,y) in result:
                # print("🪢", end="")
                letter = letters[result.index((x, y))]
                print(f"{letter}", end="")
            else:
                value = chr(ord('a') + v - 1)
                value = "⬜"
                print(f"{value}", end="")
        print("")


class Node:
    """
    A node class for A* Pathfinding
    """

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

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, allow_diagonal_movement = False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """
    print(start)

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    # print(end)
    # print(maze)
    end_value = maze[end[1]][end[0]]

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze) // 2)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1
        # print(outer_iterations)

        if outer_iterations > max_iterations:
          # if we hit this point return the path such as it is
          # it will not contain the destination
          # return return_path(current_node)       
          pass
          # print('max iters')
        
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)
        if outer_iterations % 100 == 0:
            pass
            # print_map(map, current_node.return_path())

        # Found the goal
        if current_node == end_node:
            # print('found the goal')
            return return_path(current_node)

        current_value = maze[current_node.position[1]][current_node.position[0]] 
        # Generate children
        children = []
        # print(f"current: {current_node.position}")
        
        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[1] > (len(maze) - 1) or node_position[1] < 0 or node_position[0] > (len(maze[len(maze)-1]) -1) or node_position[0] < 0:
                continue

            node_value = maze[node_position[1]][node_position[0]] 

            # Make sure walkable terrain
            if node_value - current_value > 1:
                continue
            else:
                # print(f"neighbour {node_position} valid with {node_value} reachable form {current_value}")
                pass


            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            child_value = maze[child.position[1]][child.position[0]] 
            # if child in current_node.return_path_nodes():
            if child in closed_list:
                # print("already visited")
                continue

            # Create the f, g, and h values
            dist = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            current_dist = ((current_node.position[0] - end_node.position[0]) ** 2) + ((current_node.position[1] - end_node.position[1]) ** 2)
            dist_diff = dist - current_dist 
            # print("current_value")
            # print(current_value)
            # print("dist")
            # print(dist)
            diff = child_value - current_value
            manhattan_dist = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])

            # print("diff")
            # print(f"d:{dist}")
            # print(f"m:{manhattan_dist}")
            child.g = current_node.g + 1
            # child.h = diff if diff < 0 else dist
            # child.h = diff if diff < 0 else manhattan_dist
            # child.h = manhattan_dist
            child.h = 0
            child.f = child.g + child.h

            # Child is already in the open list

            if child in open_list:
            # if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                # print("already open")
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)
    
    return None


f = open("12/input.txt")
map = []
start = (0, 0)
end = (0, 0)
part2 = []
for i, l in enumerate(f.readlines()):
    l = l.strip()
    print(l)
    if (s := l.find("S")) != -1:
        l = l.replace("S", "a")
        start = (s, i)
    if (e := l.find("E")) != -1:
        l = l.replace("E", "z")
        end = (e, i)
    int_line = [ord(c) - ord("a") + 1 for c in l]
    for x, val in enumerate(int_line):
        if val == 2: # get all B instead of all A because there are 40 Bs and hundreds of As
            part2.append((x, i,))
    print(int_line)
    map.append(int_line)

f.close()

print(map)
result = astar(map, start, end)
print(start)
print(end)
print(result)
print_map(map, result)
print(len(result) - 1)
part2_results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    processes = []
    for p2 in part2:
        processes.append(executor.submit(astar, map, p2, end))
    for _ in concurrent.futures.as_completed(processes):
        result = _.result()
        part2_results.append(result)
        print('Result: ', _.result())
part2_result_lens = [len(result) - 1 for result in part2_results if result is not None]
part2_result_lens.sort()
print(part2_result_lens[0] + 1)
