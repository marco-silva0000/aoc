from typing import Dict, List, Tuple, Any

from collections import defaultdict, deque
from enum import Enum
from itertools import cycle


class Value(int):
    moved = False
    mixed_at = 0

data = []
f = open("20/input.txt")
for line in f.readlines():
    line = line.strip()
    data.append(Value(int(line)))
f.close()
size = len(data)
# print(data)
# print(data2)
def mix(data):
    data2 = data.copy()
    i = 0
    mixed_at = 1
    while i < size:
        # print("i", i)
        # print('before data', data2)
        if data2[i].moved:
            i += 1
            continue
        val = data2.pop(i)
        index = val + i
        if index >= size:
            offset = 0
            while index >= size:
                index = index - (size - 1)
            index += offset
        elif index < 0:
            if abs(index) > size:
                index = abs(index)
                offset = 0
                while index >= size:
                    index = index - (size - 1)
                index += offset
                index *= -1
        if index == 0:
            index = size-1
        val.moved = True
        val.mixed_at = mixed_at
        mixed_at += 1
        data2.insert(index, val)
        # try:
        #     print(f"{val} moves between {data2[index-1]} and {data2[index+1]}")
        # except Exception:
        #     print(index)
        #     index = index % size
        #     print(f"{val} moves between {data2[index-1]} and {data2[index]}")
        # print('after data', data2)
    return data2

def mix_review(data):
    data2 = data.copy()
    i = 0
    mixed_at = 1
    while i < size:
        # print("i", i)
        # print('before data', data2)
        if data2[i].moved:
            i += 1
            continue
        val = data2.pop(i)
        index = val + i
        if index >= size:
            index = index % (size-1)
        elif index < 0:
            if abs(index) > size:
                index = abs(index)
                index = index % (size-1)
                index *= -1
        if index == 0:
            index = size-1
        val.moved = True
        val.mixed_at = mixed_at
        mixed_at += 1
        data2.insert(index, val)
        # try:
        #     print(f"{val} moves between {data2[index-1]} and {data2[index+1]}")
        # except Exception:
        #     print(index)
        #     index = index % size
        #     print(f"{val} moves between {data2[index-1]} and {data2[index]}")
        # print('after data', data2)
    return data2

def mix2(data2, key=0, n_scrambles=10):
    data2 = [Value(key*item) for item in data2]
    mixed = mix_review(data2)
    size = len(data2)
    for scramble in range(n_scrambles -1):
        mixed_at = 0
        print('scramble', scramble)
        while mixed_at < size:
            # print('before data', data2)
            mixed_at += 1

            val_index = [i for i in range(size) if mixed[i].mixed_at == mixed_at][0]
            val = mixed.pop(val_index)
            index = val + val_index
            if index >= size:
                index = index % (size-1)
            elif index < 0:
                if abs(index) > size:
                    index = abs(index)
                    index = index % (size-1)
                    index *= -1
            if index == 0:
                index = size-1
            mixed.insert(index, val)
            # try:
            #     print(f"{val} moves between {data2[index-1]} and {data2[index+1]}")
            # except Exception:
            #     print(index)
            #     index = index % size
            #     print(f"{val} moves between {data2[index-1]} and {data2[index]}")
            # print('after data', data2)
    return mixed


def calc_coords(data, start=0):
    data2 = data.copy()
    index = data2.index(start)
    data3 = data2[index:] + data2[:index]
    result = 0
    # print("data", data)
    # print("data2", data2)
    # print("data3", data3)
    for i, val in enumerate(cycle(data3)):
        if i == 1000:
            print("1000", val)
        if i == 2000:
            print("2000", val)
        if i == 3000:
            print("3000", val)
        if i == 1000:
            result += val
        if i == 2000:
            result += val
        if i == 3000:
            result += val
            break
    return result

print(calc_coords(mix_review(data)))

print(calc_coords(mix2(data, key=811589153)))



