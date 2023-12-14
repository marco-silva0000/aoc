from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
from structlog import get_logger
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

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

def validate_permutation(permutation, group, group_index=0, current_group=0, i=None, carry_over=""):
    log.debug("validate_permutation", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i, carry_over=carry_over)
    if group_index >= len(group):
        log.debug("---no more damaged?", group_index=group_index, len_group=len(group))
        return permutation.count(Spring.DAMAGED.value) == 0
    group_value = group[group_index]
    if permutation.startswith(Spring.OPERATIONAL.value):
        # if current_group > 0: 
        #     log.debug("current_group > 0 and current_group != group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        #     return False
        log.debug("OPERATIONAL", permutation=permutation, group=group, group_index=group_index, current_group=0, i=i)
        return validate_permutation(permutation[1:], group, group_index=group_index, i=i, carry_over=carry_over+Spring.OPERATIONAL.value)
    elif permutation.startswith(Spring.DAMAGED.value):
        log.debug("DAMAGED", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        current_group += 1
        if current_group == group_value:
            return validate_permutation(permutation[1:], group, group_index=group_index+1, current_group=0, i=i, carry_over=carry_over+Spring.OPERATIONAL.DAMAGED)
        elif current_group > group_value:
            log.debug("current_group > group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return False
        else:
            log.debug("---current_group < group_value", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
            return validate_permutation(permutation[1:], group, group_index=group_index, current_group=current_group, i=i, carry_over=carry_over+Spring.DAMAGED.value)

    elif permutation.startswith(Spring.UNKNOWN.value):
        if current_group > 0: # we have to have only # or ? until end of group
            next_chunk = permutation[1:group_value]
            diff = group_value - current_group
            counted = next_chunk.count(Spring.DAMAGED.value) + next_chunk.count(Spring.UNKNOWN.value)
            if counted == diff and permutation[diff] != Spring.DAMAGED.value:
                log.debug("current_group > 0", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i, counted=counted, next_chunk=next_chunk, diff=diff)
                return validate_permutation(permutation[diff:], group, group_index=group_index+1, current_group=0, i=i, carry_over=carry_over+permutation[:diff])
            else:
                log.debug("current_group > 0 but else", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
                return validate_permutation(permutation[group_value - current_group:], group, group_index=group_index+1, current_group=0, i=i, carry_over=carry_over+permutation[:group_value - current_group])
        log.debug("UNKNOWN", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
        # try operational
        return (
                validate_permutation(permutation[1:], group, group_index=group_index, current_group=current_group, i=i, carry_over=carry_over+Spring.OPERATIONAL.value), # its'operational
                validate_permutation(permutation[1:], group, group_index=group_index, current_group=1, i=i, carry_over=carry_over+Spring.DAMAGED.value)
                )
    log.debug("end of the line", permutation=permutation, group=group, group_index=group_index, current_group=current_group, i=i)
    return True


def validate_permutations(permutations, groups, i=None):
    valid_permutation_list = []
    for permutation in permutations:
        results = validate_permutation(permutation, groups, i=i)
        log.debug("results", results=results, i=i)
        return results
        valid_permutation_list.extend(results)

    # validate_permutations = list(filter(lambda x: x, valid_permutations))
    if len(valid_permutation_list) == 0:
        # log.debug("no valid permutations", permutations=permutations, groups=groups, i=i)
        raise Exception("no valid permutations")
    return valid_permutation_list


def parse_line(springs, groups, folding=1, i=None):
    log.debug("parse_line", springs=springs, groups=groups, folding=folding, i=i)
    springs = "?".join([springs]*folding)
    groups = folding*groups
    print(springs)
    print(groups)
    return validate_permutations([springs], groups, i=i)


def part2(values_list, folding=1) -> str:
    result = []
    for i, values in enumerate(values_list):
        springs, groups = values.split()
        groups = list(map(int, groups.split(",")))
        result.append(parse_line(springs, groups, folding=folding, i=i))
        log.debug("result", result=result, i=i)

    return str(sum(result))
