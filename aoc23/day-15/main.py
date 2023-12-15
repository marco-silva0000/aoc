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


def run_part1():
    data = get_data()
    parsed_data = parse(data)
    print(part1(parsed_data))
"""
rn=1 becomes 30.
cm- becomes 253.
qp=3 becomes 97.
cm=2 becomes 47.
qp- becomes 14.
pc=4 becomes 180.
ot=9 becomes 9.
ab=5 becomes 197.
pc- becomes 48.
pc=6 becomes 214.
ot=7 becomes 231
"""

def test_part1():
    data = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "1320"


def test_part2():
    data = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "145"
