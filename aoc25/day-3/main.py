import os
from structlog import get_logger
import pytest

log = get_logger()

from .part1 import part1
from .part2 import part2
from .part2 import get_joltage as get_joltage_p2


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
    data = """987654321111111
811111111111119
234234234234278
818181911112111"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "357"


def test_part2():
    print(get_joltage_p2("987654321111111", 12))
    assert get_joltage_p2("987654321111111", 12) == "987654321111"
    print(get_joltage_p2("811111111111119", 12))
    assert get_joltage_p2("811111111111119", 12) == "811111111119"
    print(get_joltage_p2("234234234234278", 12))
    assert get_joltage_p2("234234234234278", 12) == "434234234278"
    print(get_joltage_p2("818181911112111", 12))
    assert get_joltage_p2("818181911112111", 12) == "888911112111"

    data = """987654321111111
811111111111119
234234234234278
818181911112111"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "3121910778619"
