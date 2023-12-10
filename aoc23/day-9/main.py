import os
from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
from structlog import get_logger
from dataclasses import dataclass
from itertools import cycle
import pytest

log = get_logger()


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
        
    

def part1(values_list) -> str:
    result = []
    for values in values_list:
        spreaded_values = sperad(values)[-1]
        result.append(spreaded_values)
        # log.debug(f"new result", values=values, spreaded_values=spreaded_values, result=result)
    return str(sum(result))

def part2(values_list) -> str:
    result = []
    for values in values_list:
        spreaded_values = sperad_back(values)[0]
        result.append(spreaded_values)
        # log.debug(f"new result", values=values, spreaded_values=spreaded_values, result=result)
    return str(sum(result))

def get_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    f = open(f"{current_dir}/input.txt")
    data = f.read()
    f.close()
    return data

def parse(data: str):
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    lines = data.splitlines()
    values_list = []
    for line in lines:
        values = list(map(int, line.split()))
        values_list.append(values)
    return values_list

if __name__ == "__main__":
    data = get_data()
    parsed_data = parse(data)
    print(part1(parsed_data))
    print(part2(parsed_data))

def test_part1():
    data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "114"



def test_part2():
    data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "2"
