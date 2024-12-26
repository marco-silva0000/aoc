from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import networkx as nx
from collections import defaultdict

logger = structlog.get_logger()


class Operation(StrEnum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"


@dataclass
class Wire:
    wire_a: str
    wire_b: str
    to_wire: str
    operation: Operation


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
    log.info("day 24 part1")
    result = []
    on_registers = True
    registers = dict()
    wires = []
    for index, values in enumerate(values_list):
        if not values:
            on_registers = False
            continue
        if on_registers:
            register, value = values.split(": ")
            registers[register] = int(value)
        else:
            f, t = values.split(" -> ")
            wire_a, operation, wire_b = f.split(" ")
            operation = Operation(operation)
            wires.append(Wire(wire_a, wire_b, t, operation))

        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
    for register, value in registers.items():
        log.debug("register", register=register, value=value)
    for wire in wires:
        log.debug("wire", wire=wire)

    processed_wires = False
    while not processed_wires:
        # find wire with all dependencies resolved
        for wire in wires:
            if wire.to_wire in registers:
                continue
            if wire.wire_a in registers and wire.wire_b in registers:
                match wire.operation:
                    case Operation.AND:
                        registers[wire.to_wire] = (
                            registers[wire.wire_a] & registers[wire.wire_b]
                        )
                        break
                    case Operation.OR:
                        registers[wire.to_wire] = (
                            registers[wire.wire_a] | registers[wire.wire_b]
                        )
                        break
                    case Operation.XOR:
                        registers[wire.to_wire] = (
                            registers[wire.wire_a] ^ registers[wire.wire_b]
                        )
                        break
        else:
            processed_wires = True

    for register, value in sorted(registers.items(), key=lambda x: x[0]):
        log.debug("register", register=register, value=value)

    z_registers = sorted(
        list(
            filter(
                lambda r: r.startswith("z") and r[1:].isdigit(),
                [register for register in registers.keys()],
            )
        ),
        reverse=True,
    )
    log.debug("z_registers", z_registers=z_registers)

    result = [str(registers[register]) for register in z_registers]

    result_num = int("".join(result), 2)
    print(result_num)
    return f"{result_num}"
