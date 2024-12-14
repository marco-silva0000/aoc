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


# def test_se_part1():
#     data = """p=2,4 v=2,3"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part1(parsed_data, secconds=5)
#     assert result == "1"


def test_sm_part1():
    data = """p=2,4 v=2,-3"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data, secconds=5)
    assert result == "0"


def test_all_2_part1():
    data = """p=0,0 v=0,0
p=0,1 v=0,0
p=0,2 v=0,0
p=0,3 v=0,0
p=0,4 v=0,0
p=0,5 v=0,0
p=0,6 v=0,0
p=1,0 v=0,0
p=1,1 v=0,0
p=1,2 v=0,0
p=1,3 v=0,0
p=1,4 v=0,0
p=1,5 v=0,0
p=1,6 v=0,0
p=2,0 v=0,0
p=2,1 v=0,0
p=2,2 v=0,0
p=2,3 v=0,0
p=2,4 v=0,0
p=2,5 v=0,0
p=2,6 v=0,0
p=3,0 v=0,0
p=3,1 v=0,0
p=3,2 v=0,0
p=3,3 v=0,0
p=3,4 v=0,0
p=3,5 v=0,0
p=3,6 v=0,0
p=4,0 v=0,0
p=4,1 v=0,0
p=4,2 v=0,0
p=4,3 v=0,0
p=4,4 v=0,0
p=4,5 v=0,0
p=4,6 v=0,0
p=5,0 v=0,0
p=5,1 v=0,0
p=5,2 v=0,0
p=5,3 v=0,0
p=5,4 v=0,0
p=5,5 v=0,0
p=5,6 v=0,0
p=6,0 v=0,0
p=6,1 v=0,0
p=6,2 v=0,0
p=6,3 v=0,0
p=6,4 v=0,0
p=6,5 v=0,0
p=6,6 v=0,0
p=7,0 v=0,0
p=7,1 v=0,0
p=7,2 v=0,0
p=7,3 v=0,0
p=7,4 v=0,0
p=7,5 v=0,0
p=7,6 v=0,0
p=8,0 v=0,0
p=8,1 v=0,0
p=8,2 v=0,0
p=8,3 v=0,0
p=8,4 v=0,0
p=8,5 v=0,0
p=8,6 v=0,0
p=9,0 v=0,0
p=9,1 v=0,0
p=9,2 v=0,0
p=9,3 v=0,0
p=9,4 v=0,0
p=9,5 v=0,0
p=9,6 v=0,0
p=10,0 v=0,0
p=10,1 v=0,0
p=10,2 v=0,0
p=10,3 v=0,0
p=10,4 v=0,0
p=10,5 v=0,0
p=10,6 v=0,0"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data, secconds=1)
    assert result == "50625"


def test_1_2_big_part1():
    data = """p=0,0 v=0,0
p=0,1 v=0,0
p=0,2 v=0,0
p=0,3 v=0,0
p=0,4 v=0,0
p=0,5 v=0,0
p=0,6 v=0,0
p=1,0 v=0,0
p=1,1 v=0,0
p=1,2 v=0,0
p=1,3 v=0,0
p=1,4 v=0,0
p=1,5 v=0,0
p=1,6 v=0,0
p=2,0 v=0,0
p=2,1 v=0,0
p=2,2 v=0,0
p=2,3 v=0,0
p=2,4 v=0,0
p=2,5 v=0,0
p=2,6 v=0,0
p=3,0 v=0,0
p=3,1 v=0,0
p=3,2 v=0,0
p=3,3 v=0,0
p=3,4 v=0,0
p=3,5 v=0,0
p=3,6 v=0,0
p=4,0 v=0,0
p=4,1 v=0,0
p=4,2 v=0,0
p=4,3 v=0,0
p=4,4 v=0,0
p=4,5 v=0,0
p=4,6 v=0,0
p=5,0 v=0,0
p=5,1 v=0,0
p=5,2 v=0,0
p=5,3 v=0,0
p=5,4 v=0,0
p=5,5 v=0,0
p=5,6 v=0,0
p=6,0 v=0,0
p=6,1 v=0,0
p=6,2 v=0,0
p=6,3 v=0,0
p=6,4 v=0,0
p=6,5 v=0,0
p=6,6 v=0,0
p=7,0 v=0,0
p=7,1 v=0,0
p=7,2 v=0,0
p=7,3 v=0,0
p=7,4 v=0,0
p=7,5 v=0,0
p=7,6 v=0,0
p=8,0 v=0,0
p=8,1 v=0,0
p=8,2 v=0,0
p=8,3 v=0,0
p=8,4 v=0,0
p=8,5 v=0,0
p=8,6 v=0,0
p=9,0 v=0,0
p=9,1 v=0,0
p=9,2 v=0,0
p=9,3 v=0,0
p=9,4 v=0,0
p=9,5 v=0,0
p=9,6 v=0,0
p=10,0 v=0,0
p=10,1 v=0,0
p=10,2 v=0,0
p=10,3 v=0,0
p=10,4 v=0,0
p=10,5 v=0,0
p=10,6 v=0,0
p=80,0 v=0,0
p=80,1 v=0,0
p=80,2 v=0,0
p=80,3 v=0,0
p=80,4 v=0,0
p=80,5 v=0,0
p=80,6 v=0,0
p=81,0 v=0,0
p=81,1 v=0,0
p=81,2 v=0,0
p=81,3 v=0,0
p=81,4 v=0,0
p=81,5 v=0,0
p=81,6 v=0,0
p=82,0 v=0,0
p=82,1 v=0,0
p=82,2 v=0,0
p=82,3 v=0,0
p=82,4 v=0,0
p=82,5 v=0,0
p=82,6 v=0,0
p=83,0 v=0,0
p=83,1 v=0,0
p=83,2 v=0,0
p=83,3 v=0,0
p=83,4 v=0,0
p=83,5 v=0,0
p=83,6 v=0,0
p=84,0 v=0,0
p=84,1 v=0,0
p=84,2 v=0,0
p=84,3 v=0,0
p=84,4 v=0,0
p=84,5 v=0,0
p=84,6 v=0,0
p=85,0 v=0,0
p=85,1 v=0,0
p=85,2 v=0,0
p=85,3 v=0,0
p=85,4 v=0,0
p=85,5 v=0,0
p=85,6 v=0,0
p=86,0 v=0,0
p=86,1 v=0,0
p=86,2 v=0,0
p=86,3 v=0,0
p=86,4 v=0,0
p=86,5 v=0,0
p=86,6 v=0,0
p=87,0 v=0,0
p=87,1 v=0,0
p=87,2 v=0,0
p=87,3 v=0,0
p=87,4 v=0,0
p=87,5 v=0,0
p=87,6 v=0,0
p=88,0 v=0,0
p=88,1 v=0,0
p=88,2 v=0,0
p=88,3 v=0,0
p=88,4 v=0,0
p=88,5 v=0,0
p=88,6 v=0,0
p=89,0 v=0,0
p=89,1 v=0,0
p=89,2 v=0,0
p=89,3 v=0,0
p=89,4 v=0,0
p=89,5 v=0,0
p=89,6 v=0,0
p=90,0 v=0,0
p=90,1 v=0,0
p=90,2 v=0,0
p=90,3 v=0,0
p=90,4 v=0,0
p=90,5 v=0,0
p=90,6 v=0,0"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data, secconds=1)
    assert result == "0"


def test_all_big_part1():
    data = """p=0,0 v=0,0
p=0,1 v=0,0
p=0,2 v=0,0
p=0,3 v=0,0
p=0,4 v=0,0
p=0,5 v=0,0
p=0,6 v=0,0
p=1,0 v=0,0
p=1,1 v=0,0
p=1,2 v=0,0
p=1,3 v=0,0
p=1,4 v=0,0
p=1,5 v=0,0
p=1,6 v=0,0
p=2,0 v=0,0
p=2,1 v=0,0
p=2,2 v=0,0
p=2,3 v=0,0
p=2,4 v=0,0
p=2,5 v=0,0
p=2,6 v=0,0
p=3,0 v=0,0
p=3,1 v=0,0
p=3,2 v=0,0
p=3,3 v=0,0
p=3,4 v=0,0
p=3,5 v=0,0
p=3,6 v=0,0
p=4,0 v=0,0
p=4,1 v=0,0
p=4,2 v=0,0
p=4,3 v=0,0
p=4,4 v=0,0
p=4,5 v=0,0
p=4,6 v=0,0
p=5,0 v=0,0
p=5,1 v=0,0
p=5,2 v=0,0
p=5,3 v=0,0
p=5,4 v=0,0
p=5,5 v=0,0
p=5,6 v=0,0
p=6,0 v=0,0
p=6,1 v=0,0
p=6,2 v=0,0
p=6,3 v=0,0
p=6,4 v=0,0
p=6,5 v=0,0
p=6,6 v=0,0
p=7,0 v=0,0
p=7,1 v=0,0
p=7,2 v=0,0
p=7,3 v=0,0
p=7,4 v=0,0
p=7,5 v=0,0
p=7,6 v=0,0
p=8,0 v=0,0
p=8,1 v=0,0
p=8,2 v=0,0
p=8,3 v=0,0
p=8,4 v=0,0
p=8,5 v=0,0
p=8,6 v=0,0
p=9,0 v=0,0
p=9,1 v=0,0
p=9,2 v=0,0
p=9,3 v=0,0
p=9,4 v=0,0
p=9,5 v=0,0
p=9,6 v=0,0
p=10,0 v=0,0
p=10,1 v=0,0
p=10,2 v=0,0
p=10,3 v=0,0
p=10,4 v=0,0
p=10,5 v=0,0
p=10,6 v=0,0
p=80,0 v=0,0
p=80,1 v=0,0
p=80,2 v=0,0
p=80,3 v=0,0
p=80,4 v=0,0
p=80,5 v=0,0
p=80,6 v=0,0
p=81,0 v=0,0
p=81,1 v=0,0
p=81,2 v=0,0
p=81,3 v=0,0
p=81,4 v=0,0
p=81,5 v=0,0
p=81,6 v=0,0
p=82,0 v=0,0
p=82,1 v=0,0
p=82,2 v=0,0
p=82,3 v=0,0
p=82,4 v=0,0
p=82,5 v=0,0
p=82,6 v=0,0
p=83,0 v=0,0
p=83,1 v=0,0
p=83,2 v=0,0
p=83,3 v=0,0
p=83,4 v=0,0
p=83,5 v=0,0
p=83,6 v=0,0
p=84,0 v=0,0
p=84,1 v=0,0
p=84,2 v=0,0
p=84,3 v=0,0
p=84,4 v=0,0
p=84,5 v=0,0
p=84,6 v=0,0
p=85,0 v=0,0
p=85,1 v=0,0
p=85,2 v=0,0
p=85,3 v=0,0
p=85,4 v=0,0
p=85,5 v=0,0
p=85,6 v=0,0
p=86,0 v=0,0
p=86,1 v=0,0
p=86,2 v=0,0
p=86,3 v=0,0
p=86,4 v=0,0
p=86,5 v=0,0
p=86,6 v=0,0
p=87,0 v=0,0
p=87,1 v=0,0
p=87,2 v=0,0
p=87,3 v=0,0
p=87,4 v=0,0
p=87,5 v=0,0
p=87,6 v=0,0
p=88,0 v=0,0
p=88,1 v=0,0
p=88,2 v=0,0
p=88,3 v=0,0
p=88,4 v=0,0
p=88,5 v=0,0
p=88,6 v=0,0
p=89,0 v=0,0
p=89,1 v=0,0
p=89,2 v=0,0
p=89,3 v=0,0
p=89,4 v=0,0
p=89,5 v=0,0
p=89,6 v=0,0
p=90,0 v=0,0
p=90,1 v=0,0
p=90,2 v=0,0
p=90,3 v=0,0
p=90,4 v=0,0
p=90,5 v=0,0
p=90,6 v=0,0
p=0,70 v=0,0
p=0,71 v=0,0
p=0,72 v=0,0
p=0,73 v=0,0
p=0,74 v=0,0
p=0,75 v=0,0
p=0,76 v=0,0
p=1,70 v=0,0
p=1,71 v=0,0
p=1,72 v=0,0
p=1,73 v=0,0
p=1,74 v=0,0
p=1,75 v=0,0
p=1,76 v=0,0
p=2,70 v=0,0
p=2,71 v=0,0
p=2,72 v=0,0
p=2,73 v=0,0
p=2,74 v=0,0
p=2,75 v=0,0
p=2,76 v=0,0
p=3,70 v=0,0
p=3,71 v=0,0
p=3,72 v=0,0
p=3,73 v=0,0
p=3,74 v=0,0
p=3,75 v=0,0
p=3,76 v=0,0
p=4,70 v=0,0
p=4,71 v=0,0
p=4,72 v=0,0
p=4,73 v=0,0
p=4,74 v=0,0
p=4,75 v=0,0
p=4,76 v=0,0
p=5,70 v=0,0
p=5,71 v=0,0
p=5,72 v=0,0
p=5,73 v=0,0
p=5,74 v=0,0
p=5,75 v=0,0
p=5,76 v=0,0
p=6,70 v=0,0
p=6,71 v=0,0
p=6,72 v=0,0
p=6,73 v=0,0
p=6,74 v=0,0
p=6,75 v=0,0
p=6,76 v=0,0
p=7,70 v=0,0
p=7,71 v=0,0
p=7,72 v=0,0
p=7,73 v=0,0
p=7,74 v=0,0
p=7,75 v=0,0
p=7,76 v=0,0
p=8,70 v=0,0
p=8,71 v=0,0
p=8,72 v=0,0
p=8,73 v=0,0
p=8,74 v=0,0
p=8,75 v=0,0
p=8,76 v=0,0
p=9,70 v=0,0
p=9,71 v=0,0
p=9,72 v=0,0
p=9,73 v=0,0
p=9,74 v=0,0
p=9,75 v=0,0
p=9,76 v=0,0
p=10,70 v=0,0
p=10,71 v=0,0
p=10,72 v=0,0
p=10,73 v=0,0
p=10,74 v=0,0
p=10,75 v=0,0
p=10,76 v=0,0
p=80,70 v=0,0
p=80,71 v=0,0
p=80,72 v=0,0
p=80,73 v=0,0
p=80,74 v=0,0
p=80,75 v=0,0
p=80,76 v=0,0
p=81,70 v=0,0
p=81,71 v=0,0
p=81,72 v=0,0
p=81,73 v=0,0
p=81,74 v=0,0
p=81,75 v=0,0
p=81,76 v=0,0
p=82,70 v=0,0
p=82,71 v=0,0
p=82,72 v=0,0
p=82,73 v=0,0
p=82,74 v=0,0
p=82,75 v=0,0
p=82,76 v=0,0
p=83,70 v=0,0
p=83,71 v=0,0
p=83,72 v=0,0
p=83,73 v=0,0
p=83,74 v=0,0
p=83,75 v=0,0
p=83,76 v=0,0
p=84,70 v=0,0
p=84,71 v=0,0
p=84,72 v=0,0
p=84,73 v=0,0
p=84,74 v=0,0
p=84,75 v=0,0
p=84,76 v=0,0
p=85,70 v=0,0
p=85,71 v=0,0
p=85,72 v=0,0
p=85,73 v=0,0
p=85,74 v=0,0
p=85,75 v=0,0
p=85,76 v=0,0
p=86,70 v=0,0
p=86,71 v=0,0
p=86,72 v=0,0
p=86,73 v=0,0
p=86,74 v=0,0
p=86,75 v=0,0
p=86,76 v=0,0
p=87,70 v=0,0
p=87,71 v=0,0
p=87,72 v=0,0
p=87,73 v=0,0
p=87,74 v=0,0
p=87,75 v=0,0
p=87,76 v=0,0
p=88,70 v=0,0
p=88,71 v=0,0
p=88,72 v=0,0
p=88,73 v=0,0
p=88,74 v=0,0
p=88,75 v=0,0
p=88,76 v=0,0
p=89,70 v=0,0
p=89,71 v=0,0
p=89,72 v=0,0
p=89,73 v=0,0
p=89,74 v=0,0
p=89,75 v=0,0
p=89,76 v=0,0
p=90,70 v=0,0
p=90,71 v=0,0
p=90,72 v=0,0
p=90,73 v=0,0
p=90,74 v=0,0
p=90,75 v=0,0
p=90,76 v=0,0"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data, secconds=1)
    assert result == "35153041"


def test_quads_part1():
    data = """p=0,0 v=0,0
p=3,3 v=0,0
p=6,3 v=0,0
p=5,1 v=0,0
p=5,6 v=0,0
p=10,0 v=0,0
p=0,6 v=0,0
p=10,6 v=0,0"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data, secconds=1)
    assert result == "1"


def test_part1():
    data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "12"


# def test_part2():
#     data = """p=0,4 v=3,-3
# p=6,3 v=-1,-3
# p=10,3 v=-1,2
# p=2,0 v=2,-1
# p=0,0 v=1,3
# p=3,0 v=-2,-2
# p=7,6 v=-1,-3
# p=3,0 v=-1,-2
# p=9,3 v=2,3
# p=7,3 v=-1,2
# p=2,4 v=2,-3
# p=9,5 v=-3,-3"""
#     parsed_data = parse(data)
#     log.debug(parsed_data)
#     result = part2(parsed_data)
#     assert result == "12"
