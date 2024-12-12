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


def test_sm_part3():
    data = """AAAA
BBCD
BBCC
EEEC"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "140"


def test_md_part3():
    data = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    print(result)
    print(result)
    log.debug(result)
    log.debug(result)
    log.debug(result)
    log.debug(result)
    assert result == "772"


def test_part3():
    data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "1930"


def test_sm_part3():
    data = """AAAA
BBCD
BBCC
EEEC"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "80"


def test_md_part3():
    data = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    print(result)
    print(result)
    log.debug(result)
    log.debug(result)
    log.debug(result)
    log.debug(result)
    assert result == "436"


def test_part3():
    data = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "236"


def test_part3():
    data = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "368"


def test_part3():
    data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "1206"
