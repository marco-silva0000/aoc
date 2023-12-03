from typing import Dict, List, Tuple, Any, Optional, Set

f = open("3/test.txt")
f = open("3/input.txt")


Point = Tuple[int, int]
PointAttr = Tuple[str, bool, bool, Optional[bool]]

grid: Dict[Point, PointAttr] =  dict()
part_numbers = []
max_x = 0
max_y = 0
for y, l in enumerate(f.readlines()):
    l = l.strip()
    print(l)
    for x, c in enumerate(l):
        is_int = c.isdigit()
        is_symbol = not is_int and c != "."
        is_part = None
        grid[(x, y)] = (c, is_int, is_symbol, is_part,)
        if x > max_x:
            max_x = x
    if y > max_y:
        max_y = y
print(max_x)
print(max_y)
print(grid)

def is_touching(one: Point, other: Point) -> bool:
    x, y  = one
    xx, yy = other
    dx = abs(xx - x)
    dy = abs(yy - y)
        
    return dx + dy == 1 

def get_neighbours(point: Point) -> List[Point]:
    x, y = point
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1),]

def get_x_neighbours(point: Point) -> List[Point]:
    x, y = point
    return [(x+1, y), (x-1, y),]

def any_neighbour_is_symbol(point: Point) -> bool:
    neighbours = get_neighbours(point)
    for n in neighbours:
        if n in grid:
            if grid[n][2]:
                return True

    return False

for point, attrs in grid.items():
    x, y = point
    is_int = attrs[1]
    if is_int and any_neighbour_is_symbol(point):
        pointAttr = grid[point]
        grid[point] = (pointAttr[0], pointAttr[1], pointAttr[2], True,)

prev_is_part = False
for y in range(max_y+1):
    for x in range(max_x+1):
        point = (x, y)
        is_part = grid[point][3]
        is_int = grid[point][1]
        if prev_is_part and is_int:
            is_part = True
            pointAttr = grid[point]
            grid[point] = (pointAttr[0], pointAttr[1], pointAttr[2], True,)
        prev_is_part = is_part

prev_is_part = False
for y in range(max_y+1):
    for x in range(max_x, -1, -1):
        point = (x, y)
        is_part = grid[point][3]
        is_int = grid[point][1]
        if prev_is_part and is_int:
            is_part = True
            pointAttr = grid[point]
            grid[point] = (pointAttr[0], pointAttr[1], pointAttr[2], True,)
        prev_is_part = is_part


current_int = ""
current_parts = [[]]
for y in range(max_y+1):
    if current_int:
        part_numbers.append(int(current_int))
        current_int = ""
        current_parts.append([])
    for x in range(max_x+1):
        point = (x, y)
        is_part = grid[point][3]
        if is_part:
            print("is_part", point)
            current_int += grid[point][0]
            current_parts[-1].append(point)
        else:
            if current_int:
                part_numbers.append(int(current_int))
                current_int = ""
                current_parts.append([])

print(part_numbers)
print(current_parts)
print(sum(part_numbers))
parts_dict = {}
for part in current_parts:
    for p in part:
        parts_dict[p] = part
print(parts_dict)


gear_tuples = []
for y in range(max_y+1):
    for x in range(max_x+1):
        point = (x, y)
        is_gear = grid[point][0] == "*"
        if is_gear:
            gear_set = set()
            gear_neighbours = get_neighbours(point)
            for n in gear_neighbours:
                if n in grid:
                    is_part = grid[n][3]
                    if is_part:
                        parts = tuple(parts_dict[n])
                        print("parts", parts)
                        gear_set.add(parts)

            if len(gear_set) == 2:
                print("gear_set", gear_set)
                gear_tuples.append(gear_set)
print(gear_tuples)
gear_ratios = []
for gear_tuple in gear_tuples:
    first, second = gear_tuple
    print("first", first)
    sorted_first = sorted(first)
    print(sorted_first)
    first_int = ""
    for p in sorted_first:
        first_int += grid[p][0]
    first_int = int(first_int)
    print(first_int)
    sorted_second = sorted(second)
    print(sorted_second)
    second_int = ""
    for p in sorted_second:
        second_int += grid[p][0]
    second_int = int(second_int)
    gear_ratios.append(first_int * second_int)
print(gear_ratios)
print(sum(gear_ratios))








