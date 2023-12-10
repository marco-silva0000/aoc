import os
from structlog import get_logger
import pytest

log = get_logger()

from .part1 import part1, Direction, Grid, print_map
from .part2 import part2


def parse(data: str):
    lines = data.splitlines()
    values_list = []
    for line in lines:
        values = list(line)
        values_list.append(values)
    return values_list


def get_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    f = open(f"{current_dir}/input.txt")
    data = f.read()
    f.close()
    return data


if __name__ == "__main__":
    data = get_data()
    parsed_data = parse(data)
    print(part1(parsed_data))
    print(part2(parsed_data))


def test_part1():
    data = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
    parsed_data = parse(data)
    # log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "15"


def test_part2():
    data = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
    parsed_data = parse(data)
    # log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "10"
