from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
from structlog import get_logger
from dataclasses import dataclass
from itertools import cycle

log = get_logger()

f = open("9/test.txt")
f = open("9/input.txt")

@dataclass()
class Node():
    name: str
    neighbour_list: List[str]
    l: str
    r: str
    finished_in: int = 0

def differ(values: List[int]):
    # log.debug(f"differ", values=values)
    iterable = iter(values)
    last = next(iterable)
    result = []
    for current in iterable:
        result.append(current - last)
        last = current
    # log.debug(f"differ done", result=result)
    if len(result) == 0:
        result = [0]
    return result


def sperad_back(values: List[int]):
    # log.debug(f"sperading", values=values)
    if any([x for x in values if x != 0]):
        next_list = differ(values)
        # log.debug(f"will spread done", values=values)
        next_list = sperad_back(next_list)
        # log.debug(f"sperading done", next_list=next_list)
        to_prepend = values[0] - next_list[0]
        values.insert(0, to_prepend)
        # log.debug(f"sperading done", values=values, next_list=next_list, to_prepend=to_prepend)
    return values


def sperad(values: List[int]):
    # log.debug(f"sperading", values=values)
    if any([x for x in values if x != 0]):
        next_list = differ(values)
        # log.debug(f"will spread done", values=values)
        next_list = sperad(next_list)
        # log.debug(f"sperading done", next_list=next_list)
        to_append = values[-1] + next_list[-1]
        values.append(to_append)
        # log.debug(f"sperading done", values=values, next_list=next_list, to_append=to_append)
    return values
        
    

def part1(values_list):
    result = []
    for values in values_list:
        spreaded_values = sperad(values)[-1]
        result.append(spreaded_values)
        # log.debug(f"new result", values=values, spreaded_values=spreaded_values, result=result)
    print(sum(result))

def part2(values_list):
    result = []
    for values in values_list:
        spreaded_values = sperad_back(values)[0]
        result.append(spreaded_values)
        # log.debug(f"new result", values=values, spreaded_values=spreaded_values, result=result)
    print(sum(result))

lines = f.readlines()
values_list = []
for line in lines:
    values = list(map(int, line.split()))
    values_list.append(values)

part1(values_list)
part2(values_list)
