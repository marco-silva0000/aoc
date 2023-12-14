from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
from structlog import get_logger
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from cachetools import cached
from cachetools.keys import hashkey

log = get_logger()

"""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
class Spring(StrEnum):
    OPERATIONAL = "."
    DAMAGED = "#"
    UNKNOWN = "?"

global_reult=0

@cached(cache={}, key=lambda permutation, group, group_index=0, current_group=0, i=None, carry_over="": hashkey(permutation, group, group_index, current_group))
def validate_permutation(permutation, group, group_index=0, current_group=0, i=None, carry_over=""):
    # log.debug("validate_permutation", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i, carry_over=carry_over)
    if group_index >= len(group):
        # log.debug("TRUE?: ---no more damaged?", group_index=group_index, len_group=len(group))
        return True
        return permutation.count(Spring.DAMAGED.value) == 0
        return carry_over + permutation.replace(Spring.UNKNOWN.value, Spring.OPERATIONAL.value)
    group_value = group[group_index]
    if current_group > group_value :
        # log.debug("EXIT: ---current_group > group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        return False
    elif current_group == group_value:
        # log.debug("current_group == group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        if permutation.startswith(Spring.OPERATIONAL.value):
            return validate_permutation(permutation[1:], group, group_index=group_index+1, current_group=0, i=i, carry_over=carry_over+Spring.OPERATIONAL.value)
        elif permutation.startswith(Spring.DAMAGED.value):
            # log.debug("EXIT: DMG and current_group = group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return False
        else:
            return validate_permutation(permutation[1:], group, group_index=group_index+1, i=i, carry_over=carry_over+Spring.OPERATIONAL.value)

    if permutation.startswith(Spring.OPERATIONAL.value):
        # log.debug("OPERATIONAL", permutation=permutation, group=group, group_index=group_index, current_group=0, i=i)
        if current_group > 0: 
            if current_group != group_value:
                 # log.debug("EXIT: current_group > 0 and current_group != group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
                 return False
            else:
                return validate_permutation(permutation[1:], group, group_index=group_index+1, current_group=0, i=i, carry_over=carry_over+Spring.OPERATIONAL.value)
        return validate_permutation(permutation[1:], group, group_index=group_index, i=i, carry_over=carry_over+Spring.OPERATIONAL.value)
    elif permutation.startswith(Spring.DAMAGED.value):
        # log.debug("DAMAGED", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        # current_group += 1
        if current_group == group_value:
            # log.debug("EXIT: current_group == group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return False
        elif current_group > group_value:
            # log.debug("EXIT: current_group > group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return False
        else:
            # log.debug("DMG current_group < group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return validate_permutation(permutation[1:], group, group_index=group_index, current_group=current_group+1, i=i, carry_over=carry_over+Spring.DAMAGED.value)

    elif permutation.startswith(Spring.UNKNOWN.value):
        # log.debug("UNKNOWN", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        if current_group > 0: # we have to have only # or ? until end of group
            # log.debug("current_group > 0", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return validate_permutation(permutation[1:], group, group_index=group_index, current_group=current_group+1, i=i, carry_over=carry_over+Spring.DAMAGED.value),
        else:
        #     next_chunk = permutation[1:group_value]
        #     diff = group_value - current_group
        #     counted = next_chunk.count(Spring.DAMAGED.value) + next_chunk.count(Spring.UNKNOWN.value)
        #     if counted == diff and permutation[diff] != Spring.DAMAGED.value:
        #         log.debug("current_group > 0", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i, counted=counted, next_chunk=next_chunk, diff=diff)
        #         return validate_permutation(permutation[diff:], group, group_index=group_index+1, current_group=0, i=i, carry_over=carry_over+permutation[:diff])
        #     else:
        #         log.debug("current_group > 0 but else", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        #         return validate_permutation(permutation[group_value - current_group:], group, group_index=group_index+1, current_group=0, i=i, carry_over=carry_over+permutation[:group_value - current_group])
        # try operational
            return (
                    validate_permutation(permutation[1:], group, group_index=group_index, current_group=current_group+1, i=i, carry_over=carry_over+Spring.DAMAGED.value),
                    validate_permutation(permutation[1:], group, group_index=group_index, current_group=current_group, i=i, carry_over=carry_over+Spring.OPERATIONAL.value), # its'operational
                    )
    # log.debug("end of the line", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i, carry_over=carry_over)
    return False


@cached(cache={}, key=lambda permutation, group, group_index=0, current_group=0, i=None, carry_over="": hashkey(permutation, group, group_index, current_group))
def flatten(container):
    try:
        for i in container:
            if isinstance(i, (list,tuple)):
                for j in flatten(i):
                    yield j
            else:
                yield i
    except TypeError:
        return container


@cached(cache={}, key=lambda permutation, group, group_index=0, current_group=0, i=None, carry_over="": hashkey(permutation, group, group_index, current_group))
def validate_permutation(permutation, group, group_index=0, current_group=0, i=None, carry_over=""):
    # log.debug("validate_permutation", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i, carry_over=carry_over)
    if group_index >= len(group):
        # log.debug("TRUE?: ---no more damaged?", group_index=group_index, len_group=len(group))
        return True
    group_value = group[group_index]
    if current_group > group_value :
        # log.debug("EXIT: ---current_group > group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        return False
    elif current_group == group_value:
        # log.debug("current_group == group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        if permutation.startswith(Spring.OPERATIONAL.value):
            return validate_permutation(permutation[1:], group, group_index=group_index+1, current_group=0, i=i, carry_over=carry_over+Spring.OPERATIONAL.value)
        elif permutation.startswith(Spring.DAMAGED.value):
            # log.debug("EXIT: DMG and current_group = group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return False
        else:
            return validate_permutation(permutation[1:], group, group_index=group_index+1, i=i, carry_over=carry_over+Spring.OPERATIONAL.value)

    if permutation.startswith(Spring.OPERATIONAL.value):
        # log.debug("OPERATIONAL", permutation=permutation, group=group, group_index=group_index, current_group=0, i=i)
        if current_group > 0: 
            if current_group != group_value:
                 # log.debug("EXIT: current_group > 0 and current_group != group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
                 return False
            else:
                return validate_permutation(permutation[1:], group, group_index=group_index+1, current_group=0, i=i, carry_over=carry_over+Spring.OPERATIONAL.value)
        return validate_permutation(permutation[1:], group, group_index=group_index, i=i, carry_over=carry_over+Spring.OPERATIONAL.value)
    elif permutation.startswith(Spring.DAMAGED.value):
        # log.debug("DAMAGED", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        if current_group == group_value:
            # log.debug("EXIT: current_group == group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return False
        elif current_group > group_value:
            # log.debug("EXIT: current_group > group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return False
        else:
            # log.debug("DMG current_group < group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return validate_permutation(permutation[1:], group, group_index=group_index, current_group=current_group+1, i=i, carry_over=carry_over+Spring.DAMAGED.value)

    elif permutation.startswith(Spring.UNKNOWN.value):
        # log.debug("UNKNOWN", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        if current_group > 0: # we have to have only # or ? until end of group
            # log.debug("current_group > 0", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return validate_permutation(permutation[1:], group, group_index=group_index, current_group=current_group+1, i=i, carry_over=carry_over+Spring.DAMAGED.value)
        else:
            return (
                    validate_permutation(permutation[1:], group, group_index=group_index, current_group=current_group+1, i=i, carry_over=carry_over+Spring.DAMAGED.value),
                    validate_permutation(permutation[1:], group, group_index=group_index, current_group=current_group, i=i, carry_over=carry_over+Spring.OPERATIONAL.value), # its'operational
                    )
    # log.debug("end of the line", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i, carry_over=carry_over)
    return False

@cached(cache={})
def validate_permutation(permutation, groups):
    if not groups:
        return int(permutation.count(Spring.DAMAGED.value) == 0)
    if not permutation:
        return False
    current_group = groups[0]
    current_char = permutation[0]
    def is_operational():
        return validate_permutation(permutation[1:], groups)

    def is_damaged():
        slice = permutation[:current_group]
        if slice.count(Spring.DAMAGED.value) + slice.count(Spring.UNKNOWN.value) != current_group:
            return 0
        if len(permutation) == current_group:
            if len(groups) == 1:
                return 1
            else:
                return 0
        if permutation[current_group] in [Spring.OPERATIONAL.value, Spring.UNKNOWN.value]:
            return validate_permutation(permutation[current_group+1:], groups[1:])
        return 0

    def is_unknown():
        return is_damaged() + is_operational()

    match current_char:
        case Spring.DAMAGED.value:
            return is_damaged()
        case Spring.UNKNOWN.value:
            return is_unknown()
        case Spring.OPERATIONAL.value:
            return is_operational()


def validate_permutation_line(permutation, groups, i=None):
    results = validate_permutation(permutation, tuple(groups))
    # log.debug("results", results=results, i=i)
    # log.debug("results")
    # log.debug("flatten")
    # real_result = 0
    # try:
    #     for r in results:
    #         log.debug("r", r=r)
    #         if r is True:
    #             real_result += 1
    # except TypeError:
    #     print("TypeError")
    #     print(results)
    #     real_result = 1
    # log.debug("results", real_result=real_result, i=i)
    # with open('output.txt', 'w') as filetowrite:
        # filetowrite.write(str(results))
    return results


def parse_line(springs, groups, folding=1, i=None):
    log.debug("parse_line", springs=springs, groups=groups, folding=folding, i=i)
    springs = "?".join([springs]*folding)
    groups = folding*groups
    # print(springs)
    # print(groups)
    return validate_permutation_line(springs, groups, i=i)


def part2(values_list, folding=5) -> str:
    result = []
    for i, values in enumerate(values_list):
        springs, groups = values.split()
        groups = list(map(int, groups.split(",")))
        
        result.append(parse_line(springs, groups, folding=folding, i=i))

        # log.debug("result", result=result, i=i)
    # flattened_result = []
    # for r in result:
    #     flat = flatten(r)
    #     # log.debug("flat", flat=flat)
    #     filtered_flat = filter(lambda x: x is not False, flat)
    #     # log.debug("filtered_flat", filtered_flat=filtered_flat)
    #     set_flat = set(filtered_flat)
    #     # log.debug("set_flat", set_flat=set_flat)
    #     flattened_result.append(len(set_flat))

    # print("result", result)
    # print("result", flatten(result[0]).count(True))

    # log.debug("result", result=result)


    return str(sum(result))
    log.debug("real_result", real_result=real_result)
    return str(real_result)
