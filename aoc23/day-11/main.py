import os
from structlog import get_logger
import pytest

log = get_logger()

from part1 import part1
from part2 import part2


def parse(data: str):
    # current_dir = os.path.dirname(os.path.abspath(__file__))
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
    print(part2(parsed_data, expansion=1000000))


def run_part1():
    data = get_data()
    parsed_data = parse(data)
    print(part1(parsed_data))


def test_part1():
    data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    print(result)
    assert result == "374"


def test_sm_part1():
    data = """#.#
#.#
#.#"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    print(result)
    assert result == "43"


def test_gaps_part1():
    data = """#..#
#..#
....
....
#..#"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    print(result)
    assert result == "93"


def test_edge_part1():
    data = """#...
....
....
....
...#"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    print(result)
    assert result == "12"


def test_square_part1():
    data = """........
..#..#..
........
..#..#..
........"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    print(result)
    assert result == "32"


def test_join_square_part1():
    data = """........
...##...
...##...
........
........"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    print(result)
    assert result == "8"


def test_part2():
    data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    print(result)
    assert result == "374"


def test_sm_part2():
    data = """#.#
#.#
#.#"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    print(result)
    assert result == "43"


def test_gaps_part2():
    data = """#..#
#..#
....
....
#..#"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    print(result)
    assert result == "93"


def test_edge_part2():
    data = """#...
....
....
....
...#"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    print(result)
    assert result == "12"


def test_square_part2():
    data = """........
..#..#..
........
..#..#..
........"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    print(result)
    assert result == "32"


def test_join_square_part2():
    data = """........
...##...
...##...
........
........"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    print(result)
    assert result == "8"


def test_times10_part2():
    data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, expansion=10)
    print(result)
    assert result == "1030"


def test_times100_part2():
    data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, expansion=100)
    print(result)
    assert result == "8410"
