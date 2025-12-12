import os
from structlog import get_logger
import pytest

log = get_logger()

from .part1 import part1
from .part2 import part2


def parse(data: str):
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    lines = data.splitlines()
    values_list = []
    for line in lines:
        values_list.append(line)
    return values_list


def get_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    f = open(f"{current_dir}/input1.txt")
    data = f.read()
    f.close()
    return data


if __name__ == "__main__":
    data = get_data()
    parsed_data = parse(data)
    print(part1(parsed_data))
    print(part2(parsed_data))


def run_part1(parsed_data):
    print(part1(parsed_data))


def run_part2(parsed_data):
    print(part2(parsed_data))


def test_part1():
    data = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data, test=True)
    assert result == "2"


def test_part2():
    data = """"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == ""
