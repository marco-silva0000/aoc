import os
from structlog import get_logger
import pytest

log = get_logger()

from .part1 import part1
from .part1 import is_invalid as is_invalid_p1
from .part2 import is_invalid as is_invalid_p2
from .part1 import find_invalids as find_invalids_p1
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
    data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    assert is_invalid_p1(11)
    assert not is_invalid_p1(12)
    assert is_invalid_p1(22)
    assert is_invalid_p1(1010)
    assert is_invalid_p1(1188511885)
    assert is_invalid_p1(222222)
    assert is_invalid_p1(446446)
    assert is_invalid_p1(38593859)
    result = part1(parsed_data)
    assert result == "1227775554"


def test_part2():
    """
        11-22 still has two invalid IDs, 11 and 22.
    95-115 now has two invalid IDs, 99 and 111.
    998-1012 now has two invalid IDs, 999 and 1010.
    1188511880-1188511890 still has one invalid ID, 1188511885.
    222220-222224 still has one invalid ID, 222222.
    1698522-1698528 still contains no invalid IDs.
    446443-446449 still has one invalid ID, 446446.
    38593856-38593862 still has one invalid ID, 38593859.
    565653-565659 now has one invalid ID, 565656.
    824824821-824824827 now has one invalid ID, 824824824.
    2121212118-2121212124 now has one invalid ID, 2121212121.

    Adding up all the invalid IDs in this example produces 4174379265.

    """
    assert is_invalid_p2(11)
    assert not is_invalid_p2(12)
    assert is_invalid_p2(22)
    assert is_invalid_p2(999)
    assert is_invalid_p2(1010)
    assert is_invalid_p2(1188511885)
    assert is_invalid_p2(222222)
    assert is_invalid_p2(446446)
    assert is_invalid_p2(38593859)
    assert is_invalid_p2(565656)
    assert is_invalid_p2(824824824)
    assert is_invalid_p2(2121212121)
    data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "4174379265"
