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


def validate_permutations(permutations, groups, i=None):
    valid_permutations = []
    for permutation in permutations:
        log.debug("permutation", permutation=permutation, i=i)
        current_damage = 0
        group_iter = iter(groups)
        group = next(group_iter)
        no_more = False
        for spring in permutation:
            if spring == Spring.DAMAGED:
                # log.debug("    DAMAGED", spring=spring, current_damage=current_damage, group=group, no_more=no_more)
                if no_more:
                    break
                current_damage += 1
                if current_damage > group:
                    # log.debug("too many, breaking", spring=spring, current_damage=current_damage, group=group, no_more=no_more)
                    break
            else:
                # log.debug("not  DAMAGED", spring=spring, current_damage=current_damage, group=group, no_more=no_more)
                if current_damage > 0:
                    if not current_damage == group:
                        # log.debug("not enough, breaking", spring=spring, current_damage=current_damage, group=group, no_more=no_more)
                        break
                    try:
                        group = next(group_iter)
                        current_damage = 0
                    except StopIteration:
                        group = 0
                        current_damage = 0
                        no_more = True

        else:
            # log.debug("else", current_damage=current_damage, group=group, no_more=no_more)
            if current_damage == group:
                try:
                    group = next(group_iter)
                    # log.debug("still have groups to parse, breaking", group=group)
                    continue
                except StopIteration:
                    # log.debug("all groups parsed, adding permutation", group=group)
                    valid_permutations.append(permutation)
            else:
                # log.debug("current_damage != group, not adding", current_damage=current_damage, group=group)
                pass

    if len(valid_permutations) == 0:
        log.debug(
            "no valid permutations", permutations=permutations, groups=groups, i=i
        )
        raise Exception("no valid permutations")
    return valid_permutations


def parse_line(springs, groups, i=None):
    log.debug("parse_line", springs=springs, groups=groups, i=i)

    spring_iter = iter(springs)
    current_spring = next(spring_iter)
    count = 0
    permutations = {}
    if current_spring == Spring.UNKNOWN:
        permutations[count] = Spring.OPERATIONAL.value
        count += 1
        permutations[count] = Spring.DAMAGED.value
        count += 1
    else:
        permutations[count] = current_spring
        count += 1
    for spring in spring_iter:
        permutations_to_add = []
        for id, permutation in permutations.items():
            if spring != Spring.UNKNOWN:
                permutation += spring
                permutations[id] = permutation
            else:
                # log.debug("new_permutation", permutation=permutation, value_to_append=Spring.OPERATIONAL.value)
                new_permutation = permutation + Spring.DAMAGED.value
                permutation = permutation + Spring.OPERATIONAL.value
                permutations[id] = permutation
                permutations_to_add.append(new_permutation)

        for permutation in permutations_to_add:
            permutations[count] = permutation
            count += 1

    # log.debug("permutations", permutations=permutations)

    valid_permutations = validate_permutations(permutations.values(), groups, i=i)
    log.debug("valid_permutations", valid_permutations=valid_permutations, i=i)
    return len(valid_permutations)

    result = 0
    group_iter = iter(groups)
    group_num = next(group_iter)
    current_springs = []
    spring_groups = []
    filter_out_unknowns = lambda x: [spring for spring in x if spring != Spring.UNKNOWN]
    any_known = lambda x: any(filter_out_unknowns(x))
    any_damaged = lambda x: any(spring == Spring.DAMAGED for spring in x)
    for spring in springs:
        spring = Spring(spring)
        log.debug(
            "spring",
            spring=spring,
            current_springs=current_springs,
            spring_groups=spring_groups,
        )
        if any_damaged and len(current_springs) == group_num:
            try:
                group_num = next(group_iter)
            except StopIteration:
                pass
            current_springs = []
        else:
            if len(current_springs) == 0:
                current_springs.append(spring)
            else:
                if spring == Spring.UNKNOWN:
                    if any_known(current_springs):
                        spring_type = filter_out_unknowns(current_springs)[0]
                        spring_groups.append(spring_type)
                    else:
                        spring_groups.append(spring)
                else:
                    if any_known(current_springs):
                        spring_type = filter_out_unknowns(current_springs)[0]
                        if spring_type != spring:
                            spring_groups.append(spring_type)
                            current_springs = [spring]
                        else:
                            current_springs.append(spring)

    log.debug(spring_groups)

    return result


def part1(values_list) -> str:
    result = []
    for i, values in enumerate(values_list):
        springs, groups = values.split()
        groups = list(map(int, groups.split(",")))
        result.append(parse_line(springs, groups, i=i))
        log.debug("result", result=result, i=i)

    return str(sum(result))
