from typing import Dict, Tuple, List
import threading
import concurrent.futures
from collections import defaultdict
from enum import Enum
from itertools import chain


class Material(str, Enum):
    BEACON = "📡"
    SENSOR = "📟"
    EMPTY = '🌫️'
    NO_BEACON = '❌'
    TARGET = '🚩'
    EDGE = '🚨'
    D1 = '🏹'
    D2 = '🤾'
    D3 = '🏄'
    D4 = '📣'

class Grid(dict):
    floor = None
    def __getitem__(self, __key):
        try:
            return super().__getitem__(__key)
        except KeyError:
            return Item(*__key, material=Material.EMPTY)

Point = Tuple[int, int]


def manh(this:Point, that: Point):
    return abs(this[0] - that[0]) + abs(this[1] - that[1])

def get_diagonal(this:Point, that: Point):
    result = []
    new_x = this[0]
    new_y = this[1]
    result.append((new_x, new_y))
    size = int(manh(this, that)/2)
    if this[0] < that[0]:
        if this[1] < that[1]:
            for _ in range(size):
                new_x += 1
                new_y += 1
                result.append((new_x, new_y))
        else:
            for _ in range(size):
                new_x += 1
                new_y -= 1
                result.append((new_x, new_y))

    else:
        if this[1] < that[1]:
            for _ in range(size):
                new_x -= 1
                new_y += 1
                result.append((new_x, new_y))
        else:
            for _ in range(size):
                new_x -= 1
                new_y -= 1
                result.append((new_x, new_y))
    return result

class Item():
    def __init__(self, x: int, y: int, material=Material.EMPTY, beacon_distance=0) -> None:
        self.x = x
        self.y = y
        self.material = material
        self.beacon_distance = beacon_distance

    def __str__(self) -> str:
        return f"({self.x},{self.y}) {self.material.value}"

    def __repr__(self) -> str:
        return str(self)

    def get_manh_edges(self):
        left = self.get_mahn_left() 
        right = self.get_mahn_right() 
        up = self.get_mahn_up() 
        down = self.get_mahn_down() 
        return [left, up, right, down]

    def get_diagonals(self):
        edges = self.get_manh_edges()
        d1 = get_diagonal(edges[0], edges[1])
        d2 = get_diagonal(edges[1], edges[2])
        d3 = get_diagonal(edges[2], edges[3])
        d4 = get_diagonal(edges[3], edges[0])
        return [d1, d2, d3, d4]

    def get_mahn_left(self):
        left = (self.x-self.beacon_distance-1, self.y) 
        return left

    def get_mahn_right(self):
        right = (self.x+self.beacon_distance+1, self.y) 
        return right

    def get_mahn_up(self):
        up = (self.x, self.y-self.beacon_distance-1) 
        return up

    def get_mahn_down(self):
        down = (self.x, self.y+self.beacon_distance+1) 
        return down


    @property
    def is_empty(self) -> bool:
        return self.material  == Material.EMPTY

    @property
    def point(self):
        return (self.x, self.y,)


def print_grid(grid: Dict[Point, Item], empties=False, sensors=False, sensor_i=False, min_x=None, max_x=None, min_y=None, max_y=None):
    x_points = list(set([x for x, _ in grid.keys()]))
    x_points.sort()
    y_points = list(set([y for _, y in grid.keys()]))
    y_points.sort()
    all_sensors: List[Item] = [point for point in grid.values() if point.material == Material.SENSOR]

    if not min_x:
        min_x =min(x_points)-1
    if not max_x:
        max_x =max(x_points)+2

    if not min_y:
        min_y =min(y_points)-1
    if not max_y:
        max_y =max(y_points)+2


    for y in range(min_y, max_y):
        print(f"{y:03}:", end="")
        for x in range(min_x, max_x):
            point = (x, y)
            value = grid[point].material.value
            if (empties or sensor_i) and value == Material.EMPTY.value:
                if sensor_i:
                    all_sensors = [sensor_i]
                for sensor in all_sensors:
                    dist = manh(point, sensor.point)
                    edges = sensor.get_manh_edges()
                    d1 = get_diagonal(edges[0], edges[1])
                    d2 = get_diagonal(edges[1], edges[2])
                    d3 = get_diagonal(edges[2], edges[3])
                    d4 = get_diagonal(edges[3], edges[0])
                    if point in edges:
                        value = Material.EDGE.value
                        break
                    if point in d1:
                        value = Material.D1.value
                        break
                    if point in d2:
                        value = Material.D2.value
                        break
                    if point in d3:
                        value = Material.D3.value
                        break
                    if point in d4:
                        value = Material.D4.value
                        break
                    if dist <= sensor.beacon_distance:
                        value = Material.NO_BEACON.value
                        break
            elif sensors and value == Material.SENSOR.value:
                value = str(grid[point].beacon_distance)
            print(value, end="")
        print("")
    print("")


f = open("15/input.txt")
pairs = []
pair = [None, None]
pair_index = 0
grid: Dict[Point, Item] = Grid()
grid2: Dict[Point, Item] = Grid()
for i, l in enumerate(f.readlines()):
    l = l.strip()
    print(l)
    sensor_str, beacon_str = l.split(": ")
    sensor_str = sensor_str.removeprefix("Sensor at ")
    sensor_x_str, sensor_y_str = sensor_str.split(", ")
    sensor_x = int(sensor_x_str.removeprefix("x="))
    sensor_y = int(sensor_y_str.removeprefix("y="))
    beacon_str = beacon_str.removeprefix("closest beacon is at ")
    beacon_x_str, beacon_y_str = beacon_str.split(", ")
    beacon_x = int(beacon_x_str.removeprefix("x="))
    beacon_y = int(beacon_y_str.removeprefix("y="))
    sensor_item = Item(sensor_x, sensor_y, Material.SENSOR)
    beacon_item = Item(beacon_x, beacon_y, Material.BEACON)
    sensor_item.beacon_distance = manh(sensor_item.point, beacon_item.point)
    grid[sensor_item.point] = sensor_item
    grid[beacon_item.point] = beacon_item
    grid2[sensor_item.point] = sensor_item
    grid2[beacon_item.point] = beacon_item

f.close()
        # print_grid(grid)
# print_grid(grid)
all_sensors = [point for point in grid.values() if point.material == Material.SENSOR]
x_points = [[sensor.point[0] - sensor.beacon_distance, sensor.point[0] + sensor.beacon_distance, ] for sensor in all_sensors]
x_points = list(chain(*x_points))
print(x_points)
min_x = min(x_points)
max_x = max(x_points)
print(min_x)
print(max_x)
y_points = [[sensor.point[1] - sensor.beacon_distance, sensor.point[1] + sensor.beacon_distance, ] for sensor in all_sensors]
y_points = list(chain(*y_points))
min_y = min(y_points)
max_y = max(y_points)
target_y = 10 # 10 for twest.txt, 2000000 for input.txt
target_y = 2000000 # 10 for test.txt, 2000000 for input.txt

def part1(target_y):
    result = 0
    for i, x in enumerate(range(min_x, max_x)):
        if i % 1000 == 0:
            print(i)
        point = (x, target_y)
        for sensor in all_sensors:
            dist = manh(point, sensor.point)
            if grid[point].material == Material.EMPTY and dist <= sensor.beacon_distance:
                result += 1
                grid[point] = Item(point[0], point[1], Material.TARGET)
                break
    return result

if target_y == 10:
    for sensor in all_sensors:
        print_grid(grid, sensor_i=sensor, min_x=min_x, max_x=max_x , min_y=min_y, max_y=max_y)
    print_grid(grid, empties=True, min_x=min_x, max_x=max_x , min_y=min_y, max_y=max_y)
# print(part1())
target2 = 20
target2 = 4000000
if max_x > target2:
    max_x = target2
if max_y > target2:
    max_y = target2
min_x = 0
min_y = 0

def part2(start, end):
    candidates = []
    for i, sensor in enumerate(all_sensors):
        print(f"{i}/{len(all_sensors)}")
        diagonals = sensor.get_diagonals()
        diagonals = list(chain(*diagonals))
        for candidate in diagonals:
            if start < candidate[0] < end and start < candidate[1] < end:
                candidates.append(candidate)



    # diagonals = list(chain(*list(chain(*[sensor.get_diagonals() for sensor in all_sensors]))))
    # candidates = [(candidate[0], candidate[1]) for candidate in diagonals if start < candidate[0] < end and start < candidate[1] < end]
    len_candidates = len(candidates)
    print(len_candidates)
    for i, point in enumerate(candidates):
        if i % 1000 == 0:
            print(f"{i}/{len_candidates}")
        for sensor in all_sensors:
            dist = manh(point, sensor.point)
            if dist <= sensor.beacon_distance:
                break
        else:
            grid[point] = Item(point[0], point[1], Material.TARGET)
            return point

print(part2(0, target2))
print_grid(grid, empties=True, min_x=min_x, max_x=max_x , min_y=min_y, max_y=max_y)
exit(1)
final_result = None
batch_size = 1000
for batch in range(min_x, max_x, batch_size):
    if final_result:
        break
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        processes = []
        current = batch_size * batch
        print(f"will gen for batch {batch}")
        for i, x in enumerate(range(current, current+batch_size)):
            processes.append(executor.submit(part2, x))
        print("generated")
        for _ in concurrent.futures.as_completed(processes):
            result = _.result()
            if result:
                print('Result: ', _.result())
                if len(result) == 2:
                    final_result=result
                    print('finished, will cancel')
                    for process in processes:
                        process.cancel()


print('Result: ', final_result)





        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            processes = []
            for child in children:
                processes.append(executor.submit(process_child, child))
            for _ in concurrent.futures.as_completed(processes):
                result = _.result()
                if result:
                    heapq.heappush(open_list, result)
