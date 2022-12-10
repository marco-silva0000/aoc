from collections import defaultdict
import itertools
from pickle import NONE
from typing import List, Dict, Tuple
from itertools import chain, groupby
from enum import Enum


class Command(str, Enum):
    ADDX = "addx"
    NOOP = "noop"


opps = []
vals = []

class Processor():
    reg = 1
    i = 1
    power = 0
    operations = ""
    horiz = 0

    def process(self):
        current = opps.pop(0)
        prev = self.reg
        # print(f"start of cycle {self.i} the {current.value} instruction begins. the value of x is {self.reg}")
        if current == Command.ADDX:
            val = vals.pop(0)
            self.reg += val
        # print(f"start of cycle {self.i} the {current.value} instruction begins. the value of x is {self.reg}")
        if self.horiz == prev or self.horiz == prev + 1 or self.horiz == prev - 1 :
            print("#", end="")
        else:
            print(".", end="")

        if (self.i) % 40 == 0:
            # print(f"During the {self.i}th cycle, register X has the value {prev}, so the signal strength is {self.i} * {prev} = {(self.i) * prev}")
            # self.power += (self.i) * prev
            self.horiz = -1
            print("")
        self.i += 1
        self.horiz += 1


f = open("10/input.txt")
x = 1
processor = Processor()
for l in f.readlines():
    l = l.strip()
    # print(l)
    if l.startswith(Command.NOOP.value):
        opps.append(Command.NOOP)
    else:
        command, val = l.split(" ")
        command = Command(command)
        val = int(val)
        opps.append(Command.NOOP)
        opps.append(command)
        vals.append(val)
    processor.process()

while len(opps) > 0:
    processor.process()
   
print(processor.power)

f.close()
