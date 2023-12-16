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
    print(part2(parsed_data, folding=5))


def test_part1():
    data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "21"


def run_part1():
    data = get_data()
    parsed_data = parse(data)
    print(part1(parsed_data))


def test_line1_part1():
    data = """???.### 1,1,3"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "1"


def test_line2_part1():
    data = """.??..??...?##. 1,1,3"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "4"


def test_line3_part1():
    data = """?#?#?#?#?#?#?#? 1,3,1,6"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "1"


def test_line4_part1():
    data = """????.#...#... 4,1,1"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "1"


def test_line5_part1():
    data = """????.######..#####. 1,6,5"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "4"


def test_line6_part1():
    data = """?###???????? 3,2,1"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "10"


def test_antepen_part1():
    data = """#.?#?.#.????.???# 1,3,1,2,4"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    print(result)
    assert result == "3"


def test_line1_folding1_part2():
    data = """???.### 1,1,3"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=1)
    assert result == "1"


def test_line2_folding1_part2():
    data = """.??..??...?##. 1,1,3"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=1)
    assert result == "4"


def test_line3_folding1_part2():
    data = """?#?#?#?#?#?#?#? 1,3,1,6"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=1)
    assert result == "1"


def test_line4_folding1_part2():
    data = """????.#...#... 4,1,1"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=1)
    assert result == "1"


def test_line5_folding1_part2():
    data = """????.######..#####. 1,6,5"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=1)
    assert result == "4"


def test_line6_folding1_part2():
    data = """?###???????? 3,2,1"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=1)
    assert result == "10"


def test_antepen_folding1_part2():
    data = """#.?#?.#.????.???# 1,3,1,2,4"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=1)
    print(result)
    assert result == "3"


def test_folding1_part2():
    data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=1)
    assert result == "21"


def test_line0_part2():
    data = """.# 1"""
    parsed_data = parse(data)
    # log.debug(parsed_data)
    result = part2(parsed_data, folding=5)
    assert result == "1"


def test_line1_part2():
    data = """???.### 1,1,3"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=5)
    assert result == "1"


def test_line2_part2():
    data = """.??..??...?##. 1,1,3"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=5)
    assert result == "16384"


def test_line3_part2():
    data = """?#?#?#?#?#?#?#? 1,3,1,6"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=5)
    assert result == "1"


def test_line4_part2():
    data = """????.#...#... 4,1,1"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=5)
    assert result == "16"


def test_line5_part2():
    data = """????.######..#####. 1,6,5"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=5)
    assert result == "2500"


def test_line6_part2():
    data = """?###???????? 3,2,1"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=5)
    assert result == "506250"


def test_part2():
    data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data, folding=5)
    assert result == "525152"
