from typing import List, Set, Dict, Tuple, Optional, Union
from math import sqrt, prod

f = open("6/test.txt")
f = open("6/input.txt")


my_iter = iter(f.readlines())
time = next(my_iter)
distance = next(my_iter)
time = list(map(int, time.removeprefix("Time:").strip().split()))
distance = list(map(int, distance.removeprefix("Distance:").strip().split()))
print(time)
print(distance)
time_iter = iter(time)
distance_iter = iter(distance)

part1 = []
for d in distance_iter:
    acceleration = 0
    for t in time_iter:
        wins = 0
        acceleration = 0
        for tick in range(t):
            estimate = acceleration/2 * tick**2
            time_left = t - tick
            estimate = acceleration * time_left
            print(f"acceleration: {acceleration}, tick: {tick} time_left: {time_left} estimate: {estimate} d: {d}")
            if estimate > d:
                print(tick)
                wins += 1
            acceleration += 1
        part1.append(wins)
        try:
            d = next(distance_iter)
        except StopIteration:
            break

print(part1)
print(prod(part1))
time = int("".join(map(str, time)))
distance = int("".join(map(str, distance)))

print("time:", time)
print("distance:", distance)
first = 0
for acceleration in range(time):
    time_left = time - acceleration
    estimate = acceleration * time_left
    if estimate > distance:
        first = acceleration
        print(acceleration)
        break

second = 0
for acceleration in range(first, time):
    time_left = time - acceleration
    estimate = acceleration * time_left
    if estimate < distance:
        second = acceleration
        print(acceleration)
        break
print(second - first)
