from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from collections import deque

logger = structlog.get_logger()


def part2(values_list) -> str:
    from structlog import get_logger

    log = get_logger()
    log.debug("part2")
    memory = []
    is_free_mem = False
    index = 0
    for values in values_list:
        # print(values)
        for value in values:
            value = int(value)
            if is_free_mem:
                memory.append(deque([], value))
            else:
                memory.append(deque([index] * value, value))
                index += 1
            is_free_mem = not is_free_mem

    def print_memory(memory):
        for mem in memory:
            len_mem = len(mem)
            maxlen = mem.maxlen
            diff = maxlen - len_mem
            for n in mem:
                print(n, end="")
            if len_mem < mem.maxlen:
                print("." * diff, end="")
        print(
            "",
        )

    mem_size = sum([mem.maxlen for mem in memory if len(mem) != 0])
    # print(mem_size)

    def defrag(memory):
        last_mem_index = len(memory)
        for index in range(len(memory)):
            free_mem_index = index * 2 - 1
            # print(sum([mem.maxlen for mem in memory[:free_mem_index]]))
            if sum([len(mem) for mem in memory[:free_mem_index]]) == mem_size:
                break
            free_mem = memory[free_mem_index]
            mem_to_fill = free_mem.maxlen
            while mem_to_fill > 0:
                try:
                    last_bit = memory[last_mem_index].pop()
                    free_mem.append(last_bit)
                    mem_to_fill -= 1
                except IndexError:
                    last_mem_index -= 1  # 2 might be better
            index += 2
            # print_memory(memory)

    def file_defrag(memory):
        from structlog import get_logger

        log = get_logger()
        index = len(memory) - 1
        mem_iter = iter(reversed(memory))
        for mem in mem_iter:
            # log = log.bind(mem=mem)
            log.debug(index)
            if mem != []:
                size = len(mem)
                # log = log.bind(size=size)
                for jindex, maybe_free_mem in enumerate(memory):
                    # log = log.bind(index=index, jindex=jindex)
                    # log.debug("idexes")
                    if jindex > index:
                        break
                    free_bits = maybe_free_mem.maxlen - len(maybe_free_mem)
                    # log = log.bind(free_bits=free_bits)
                    if free_bits > 0 and free_bits >= size:
                        maybe_free_mem.extend(mem)
                        mem.clear()
                        # log.debug("moved")
                        break
            index -= 2
            try:
                next(mem_iter)
            except StopIteration:
                break
            # print_memory(memory)

    # print_memory(memory)
    file_defrag(memory)
    # print_memory(memory)
    result = 0
    index = 0
    for mem in memory:
        for mindex in range(mem.maxlen):
            try:
                val = index * mem[mindex]
            except IndexError:
                val = 0
            result += val
            index += 1
    # flat_list = []
    # for mem in memory:
    #     for mindex in range(mem.maxlen):
    #         flat_list.append(mem[mindex])
    # print(flat_list)
    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    print(result)
    return f"{result}"
