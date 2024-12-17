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
    f = open(f"{current_dir}/input.txt")
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
    data = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "4,6,3,5,6,3,5,2,1,0"


def test_a_2024_part1():
    """If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0"""
    data = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "4,2,5,6,7,7,7,7,3,1,0"


def test_a_part1():
    """If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2."""
    data = """Register A: 10
Register B: 0
Register C: 0

Program: 5,0,5,1,5,4"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "0,1,2"


def test_part2():
    data = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "0"
