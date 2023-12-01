from collections import defaultdict
import itertools
from pickle import NONE
from typing import List, Dict, Tuple
from itertools import chain, groupby
from sympy import symbols, Eq, solve



def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    return a / b

func_map = {
        add: "+",
        sub: "-",
        mul: "*",
        div: "/",
        }
monkeys = {}
operations = {}
def parse(part2=False):
    monkeys.clear()
    operations.clear()
    f = open("21/input.txt")
    for l in f.readlines():
        l = l.strip()
        print(l)
        monkey_id, rest = l.split(": ")
        if part2 and monkey_id == "humn":
            continue
        if rest.isnumeric():
            monkeys[monkey_id] = int(rest)
        else:
            if "+" in rest:
                this, that = rest.split(" + ")
                operations[monkey_id] = (this, add, that)
            elif "-" in rest:
                this, that = rest.split(" - ")
                operations[monkey_id] = (this, sub, that)
            elif "*" in rest:
                this, that = rest.split(" * ")
                operations[monkey_id] = (this, mul, that)
            else:
                this, that = rest.split(" / ")
                operations[monkey_id] = (this, div, that)
    f.close()



def get_val(monkey_id):
    try:
        return monkeys[monkey_id]
    except KeyError:
        this, op, that = operations[monkey_id]
        this_val = get_val(this)
        that_val = get_val(that)
        monkeys[monkey_id] = op(this_val, that_val)
        return monkeys[monkey_id]

def get_equation(monkey_id):

    if monkey_id == 'humn':
        return 'humn'
    try:
        return str(monkeys[monkey_id])
    except KeyError:
        this, op, that = operations[monkey_id]
        this = get_equation(this)
        that = get_equation(that)
        return f"({this}{func_map[op]}{that})"



# part1
parse()
print(get_val("root"))

# part1
parse(part2=True)
print(solve(get_equation(operations["root"][0]) + "-" + get_equation(operations["root"][2])))

