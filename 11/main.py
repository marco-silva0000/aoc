from collections import defaultdict
import itertools
from pickle import NONE
from typing import List, Dict, Tuple
from itertools import chain, groupby
from enum import Enum


class Monkey:
    def __init__(self, id, items, operation_str: str, test_str: str, if_true_id: int, if_false_id: int):
        self.id = id
        self.items = items
        self.operation_str = operation_str
        self.test_str = test_str
        self.if_true_id = if_true_id
        self.if_false_id = if_false_id
        self.inspections = 0

    def operation(self, item: int) -> int:
        prefix = "new = old "
        rest = self.operation_str.lstrip(prefix)
        operand, other = rest.split(" ")
        if other == "old":
            other = item
        else:
            other = int(other)
        # print(f"o: {item} {operand} {other}")
        if operand == "+":
            return item + other
        else:
            return item * other

    def test(self, item: int) -> bool:
        prefix = "divisible by "
        rest = self.test_str.lstrip(prefix)
        other = int(rest)
        # print(f"t: {item} % {other} == 0")
        return item % other == 0

    def inspect(self, item, chill=True):
        result = self.operation(item)
        if chill:
            result = int(result/3)
        else:
            result = result % 9699690 # magic number you get from multiplying all divisors of all monkeys
        self.inspections += 1
        if self.test(result):
            return self.if_true_id, result
        else:
            return self.if_false_id, result

    def play(self, monkeys, chill=True):
        for _ in range(len(self.items)):
            item = self.items.pop(0)
            send_to, item = self.inspect(item, chill=chill)
            monkeys[send_to].items.append(item)
        return monkeys


    def __str__(self) -> str:
        return f"{self.id}: {self.items}, i:{self.inspections}"

    def __repr__(self) -> str:
        return str(self)


def round(monkeys: Dict[int, Monkey], chill=True):
    keys = list(monkeys.keys())
    keys.sort()
    for key in keys:
        # print(f"processing {key}")
        # print(monkeys[key])
        monkeys = monkeys[key].play(monkeys, chill=chill)
    # print(monkeys)


monkeys = {}
f = open("11/input.txt")
id = None
items = None
operation_str = None
test_str = None
if_true_id = None
if_false_id = None
for l in f.readlines():
    l = l.strip()
    print(l)
    if l.startswith("Monkey "):
        id = int(l.lstrip("Monkey ").rstrip(":"))
        print(f"id:{id}")
    elif l.startswith("Starting items: "):
        items = [int(i) for i in l.lstrip("Starting items: ").split(",")]
        print(f"items:{items}")
    elif l.startswith("Operation: "):
        operation_str = l.lstrip("Operation: ")
        print(f"operation_str:{operation_str}")
    elif l.startswith("Test: "):
        test_str = l.lstrip("Test: ")
        print(f"test_str:{test_str}")
    elif l.startswith("If true: "):
        if_true_id = int(l.lstrip("If true: throw to monkey "))
        print(f"if_true_id:{if_true_id}")
    elif l.startswith("If false: "):
        if_false_id = int(l.lstrip("If false: throw to monkey "))
        print(f"if_false_id:{if_false_id}")
    else:
        monkey = Monkey(id, items, operation_str, test_str, if_true_id, if_false_id)
        print(f"monkey:{monkey}")
        monkeys[id] = monkey

f.close()

monkey = Monkey(id, items, operation_str, test_str, if_true_id, if_false_id)
print(f"monkey:{monkey}")
monkeys[id] = monkey

monkeys2 = monkeys.copy()
def part1():
    for i in range(20):
        print(f"round {i+1}")
        round(monkeys)
    print(monkeys)
    inspections = [monkey.inspections for monkey in monkeys.values()]
    inspections.sort(reverse=True)
    print(inspections[0] * inspections[1])

def part2():
    for i in range(10000):
        # print(monkeys2.items())
        print(f"round {i+1}")
        round(monkeys2, False)
    inspections2 = [monkey.inspections for monkey in monkeys2.values()]
    inspections2.sort(reverse=True)
    print(inspections2[0] * inspections2[1])

part2()
