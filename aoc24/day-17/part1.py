from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum, IntEnum

logger = structlog.get_logger()

"""
Combo operands 0 through 3 represent literal values 0 through 3.
Combo operand 4 represents the value of register A.
Combo operand 5 represents the value of register B.
Combo operand 6 represents the value of register C.

The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.

The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)
"""


class Op(IntEnum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7


def part1(values_list) -> str:
    from structlog import get_logger

    ctx = contextvars.copy_context()
    logging_ctx_value = None
    for var, value in ctx.items():
        if var.name == "logging":
            logging_ctx_value = value
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging_ctx_value),
    )

    log = get_logger()
    log.info("day 17 part1")
    result = []
    stuff = iter(values_list)
    out_buff = ""
    a = int(next(stuff).removeprefix("Register A: "))
    b = int(next(stuff).removeprefix("Register B: "))
    c = int(next(stuff).removeprefix("Register C: "))
    _ = next(stuff)
    ops = [Op(int(op)) for op in next(stuff).removeprefix("Program: ").split(",")]

    pointer = 0
    try:
        while True:
            op = ops[pointer]
            pointer += 1
            match op:
                case Op.adv:
                    numerator = a
                    operand = ops[pointer]
                    pointer += 1
                    match operand:
                        case 4:
                            denominator = 2**a
                        case 5:
                            denominator = 2**b
                        case 6:
                            denominator = 2**c
                        case _:
                            denominator = 2**operand
                    a = int(numerator / denominator)
                case Op.bdv:
                    numerator = a
                    operand = ops[pointer]
                    pointer += 1
                    match operand:
                        case 4:
                            denominator = 2**a
                        case 5:
                            denominator = 2**b
                        case 6:
                            denominator = 2**c
                        case _:
                            denominator = 2**operand
                    b = int(numerator / denominator)
                case Op.cdv:
                    numerator = a
                    operand = ops[pointer]
                    pointer += 1
                    match operand:
                        case 4:
                            denominator = 2**a
                        case 5:
                            denominator = 2**b
                        case 6:
                            denominator = 2**c
                        case _:
                            denominator = 2**operand
                    c = int(numerator / denominator)

                case Op.bxl:
                    operand = ops[pointer]
                    pointer += 1
                    b = b ^ operand
                case Op.bst:
                    combo_operand = ops[pointer]
                    pointer += 1
                    match combo_operand:
                        case 4:
                            operand = a
                        case 5:
                            operand = b
                        case 6:
                            operand = c
                        case _:
                            operand = combo_operand
                    b = combo_operand % 8
                case Op.jnz:
                    if a != 0:
                        operand = ops[pointer]
                        pointer = operand
                    else:
                        pointer += 1
                case Op.bxc:
                    _operand = ops[pointer]
                    pointer += 1
                    b = b ^ c
                case Op.out:
                    combo_operand = ops[pointer]
                    pointer += 1
                    match combo_operand:
                        case 4:
                            operand = a
                        case 5:
                            operand = b
                        case 6:
                            operand = c
                        case _:
                            operand = combo_operand

                    out_buff += str(operand % 8) + ","
    except IndexError:
        pass

    result = out_buff[:-1]
    print(result)
    print(result)
    print(result)
    print(result)
    return f"{result}"
