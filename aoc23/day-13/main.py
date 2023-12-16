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


# def run_part1():
#     data = get_data()
#     parsed_data = parse(data)
#     print(part1(parsed_data))


def test_part1():
    data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "405"


# def test_h_square_part1():
#     data = """#..#
# ...#
# ...#
# ...#
# ...#
# #..#"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part1(parsed_data)
#     assert result == "300"

# # def test_v_square_part1():
# #     data = """#....#
# # #....#
# # ......
# # #....#"""
# #     parsed_data = parse(data)
# #     log.debug(parsed_data)
# #     result = part1(parsed_data)
# #     assert result == "3"

# def test_h_odd_square_part1():
#     data = """#..#
# ...#
# ....
# ....
# ....
# ...#
# #..#"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part1(parsed_data)
#     assert result == "300"

# def test_v_odd_square_part1():
#     data = """#.....#
# #.....#
# .......
# #.....#"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part1(parsed_data)
#     assert result == "3"


def test_part2():
    data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "400"
