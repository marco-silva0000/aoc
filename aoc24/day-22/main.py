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
    data = """1
10
100
2024"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "37327623"


# def test_123_part2():
#     data = """123"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part2(parsed_data)
#     assert result == "6"


# def test_part2():
#     data = """1
# 2
# 3
# 2024"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part2(parsed_data)
#     assert result == "23"


def test_2_part2():
    data = """2021
5017
19751"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "27"


def test_first_part2():
    data = """5053
10083
11263"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "27"
