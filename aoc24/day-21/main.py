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


# def test_sm_part1():
#     data = """029A"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part1(parsed_data)
#     assert result == "1972"


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

# def test_sm_0_part2():
#     # <A^A>^^AvvvA
#     data = """029A"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part2(parsed_data, n_robots=0)
#     assert result == "348"

def test_sm_1_part2():
    # v<<A>>^A<A>AvA<^AA>A<vAAA>^A
    data = """029A"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, n_robots=1)
    assert result == "812"

def test_sm_2_part2():
    # <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    data = """029A"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, n_robots=2)
    assert result == "1972"

# def test_sm_3_part2():
#     data = """029A"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part2(parsed_data, n_robots=3)
#     assert result == "1972"


# def test_sm2_part2():
#     data = """586A"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part2(parsed_data)
#     assert result == "39848"


def test_part2():
    data = """029A
980A
179A
456A
379A"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, n_robots=2)
    assert result == "126384"
