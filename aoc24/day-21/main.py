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


# def test_get_directions_part1():
#     parsed_data = """<A^A>^^AvvvA"""
#     log.debug(parsed_data)
#     result = get_directions(parsed_data, "dir")
#     assert result == "1972"


def test_sm_part1():
    data = """029A"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "1972"


def test_part1():
    data = """029A
980A
179A
456A
379A"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "126384"


# def test_sm_part2():
#     data = """029A"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part2(parsed_data)
#     assert result == "1972"


def test_part2():
    data = """029A
980A
179A
456A
379A"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "126384"
