import os
import structlog
import pytest

log = structlog.get_logger()

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
    data = """3   4
4   3
2   5
1   3
3   9
3   3"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "11"


def test_part2():
    data = """3   4
4   3
2   5
1   3
3   9
3   3"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "31"
