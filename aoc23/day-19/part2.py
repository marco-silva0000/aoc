from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from copy import deepcopy

logger = structlog.get_logger()

class Result(StrEnum):
    Accepted = "A"
    Rejected = "R"


class Operator(StrEnum):
    LESS_THAN = "<"
    GREATER_THAN = ">"
    # EQUALS = "="
    # NOT_EQUALS = "!="

@dataclass
class Rule:
    result: Result | str
    lhs: Optional[int|str] = None
    rhs: Optional[int|str] = None
    operator: Optional[str] = None

@dataclass
class Workflow:
    name: str
    rules: List[Rule]

    def process_range(self, part_range: "PartRange", workflows: Dict[str, "Workflow"]):
        from structlog import get_logger
        logger = get_logger()
        logger.debug("workflow process", workflow=self.name)
        current_ranges = [part_range]
        logger.debug("start_range", start_range=part_range)
        accepted_ranges = []
        for rule in self.rules:
            logger.debug("rule", rule=rule)
            lhs = rule.lhs
            rhs = rule.rhs
            operator = rule.operator
            for i in range(0, len(current_ranges)):
                logger.debug("all current ranges", current_ranges=current_ranges, i=i)
                current = current_ranges[i]
                logger.debug("current", current=current)
                if not rule.lhs or not rule.rhs or not rule.operator:
                    logger.debug("rule has no lhs, rhs or operator")
                    if rule.result == Result.Accepted:
                        logger.debug("rule result is accepted")
                        accepted_ranges.append(current)
                        current_ranges.pop(i) # remove the current range as it's been dealt with
                    elif rule.result == Result.Rejected:
                        logger.debug("rule result is rejected")
                        current_ranges.pop(i) # remove the current range as it's been dealt with
                    else:
                        workflow = workflows[rule.result]
                        accepted_ranges.extend(workflow.process_range(current, workflows))
                        current_ranges.pop(i) # remove the current range as it's been dealt with
                elif isinstance(lhs, int):
                    # this is porbably unused as it looks like it's always ints on the left hand side
                    raise Exception("lhs is int")

                elif isinstance(rhs, int):
                        split_point = rhs
                        logger.debug('split', split_point=split_point, operator=operator)
                        if operator == Operator.LESS_THAN:
                            logger.debug("operator is less than")
                            first_half = deepcopy(current)
                            first_half.__setattr__(f"{lhs}_end", split_point - 1)
                            second_half = deepcopy(current)
                            second_half.__setattr__(f"{lhs}_start", split_point)
                            logger.debug('after split', first_half=first_half, second_half=second_half)
                            if rule.result == Result.Accepted:
                                logger.debug("rule result is accepted")
                                accepted_ranges.append(first_half)
                                current_ranges.pop(i) # remove the current range as it's been split
                                current_ranges.insert(i, second_half) # replace it with the second half so it doesn't get processed again
                            elif rule.result == Result.Rejected:
                                logger.debug("rule result is rejected, discard first half, keep second half")
                                current_ranges.pop(i) # remove the current range as it's been split
                                current_ranges.insert(i, second_half) # replace it with the second half so it doesn't get processed again
                            else:
                                workflow = workflows[rule.result]
                                logger.debug("rule result is a workflow", workflow=workflow)
                                accepted_ranges.extend(workflow.process_range(first_half, workflows))
                                current_ranges.pop(i) # remove the current range as it's been split
                                current_ranges.insert(i, second_half) # replace it with the second half so it doesn't get processed again

                        elif operator == Operator.GREATER_THAN:
                            logger.debug("operator is greater than")
                            first_half = deepcopy(current)
                            first_half.__setattr__(f"{lhs}_end", split_point)
                            second_half = deepcopy(current)
                            second_half.__setattr__(f"{lhs}_start", split_point + 1)
                            logger.debug('after split', first_half=first_half, second_half=second_half)
                            if rule.result == Result.Accepted:
                                logger.debug("rule result is accepted")
                                accepted_ranges.append(second_half)
                                current_ranges.pop(i) # remove the current range as it's been split
                                current_ranges.insert(i, first_half) # replace it with the first half so it doesn't get processed again
                            elif rule.result == Result.Rejected:
                                logger.debug("rule result is rejected, discard second half, keep first half")
                                current_ranges.pop(i) # remove the current range as it's been split
                                current_ranges.insert(i, first_half) # replace it with the first half so it doesn't get processed again
                            else:
                                workflow = workflows[rule.result]
                                logger.debug("rule result is a workflow", workflow=workflow)
                                accepted_ranges.extend(workflow.process_range(second_half, workflows))
                                current_ranges.pop(i) # remove the current range as it's been split
                                current_ranges.insert(i, first_half) # replace it with the first half so it doesn't get processed again

                else:
                    raise Exception(f"don't know how to parse rule: {rule}")
        return accepted_ranges

@dataclass
class PartRange:
    x_start: int
    x_end: int
    m_start: int
    m_end: int
    a_start: int
    a_end: int
    s_start: int
    s_end: int

    @property
    def value(self):
        x_range = self.x_end - self.x_start + 1
        m_range = self.m_end - self.m_start + 1
        a_range = self.a_end - self.a_start + 1
        s_range = self.s_end - self.s_start + 1
        # assert x_range > 0
        # assert m_range > 0
        # assert a_range > 0
        # assert s_range > 0

        # return math.perm(x_range, math.perm(m_range, math.perm(a_range, s_range)))
        # return math.perm(x_range) * math.perm(m_range) * math.perm(a_range) * math.perm(s_range)
        return x_range * m_range * a_range * s_range


def part2(values_list) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    # structlog.configure(
    #     wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    # )
    accepted_parts = []
    workflows = dict()
    values_iter = iter(values_list)
    for i, values in enumerate(values_iter):
        # structlog.contextvars.bind_contextvars(
        #     workflow_iteration=i,
        # )
        if values == "":
            break
        workflow_name, rules = values.split("{")
        rules_list = []
        rules = rules.removesuffix("}")
        rules = rules.split(",")
        for rule in rules:
            logger.debug("rule", rule=rule)
            if rule == Result.Accepted:
                rules_list.append(Rule(result=Result.Accepted))
            elif rule == Result.Rejected:
                rules_list.append(Rule(result=Result.Rejected))
            elif not ":" in rule:
                rules_list.append(Rule(result=rule))
            else:
                operation, result = rule.split(":")
                if result in ["A", "R"]:
                    result = Result(result)
                if Operator.LESS_THAN in operation:
                    lhs, rhs = operation.split(Operator.LESS_THAN)
                    operator = Operator.LESS_THAN
                elif Operator.GREATER_THAN in operation:
                    lhs, rhs = operation.split(Operator.GREATER_THAN)
                    operator = Operator.GREATER_THAN
                else:
                    raise Exception(f"Unknown operator: {operation}")

                if lhs.isdigit():
                    lhs = int(lhs)
                if rhs.isdigit():
                    rhs = int(rhs)
                rules_list.append(Rule(lhs=lhs, rhs=rhs, operator=operator, result=result))
        workflows[workflow_name] = Workflow(name=workflow_name, rules=rules_list)

    max_value = 4000
    min_value = 1
    part_range = PartRange(x_start=min_value, x_end=max_value, m_start=min_value, m_end=max_value, a_start=min_value, a_end=max_value, s_start=min_value, s_end=max_value)
    first_workflow = workflows["in"]
    accepted_parts = first_workflow.process_range(part_range, workflows)

    print("accepted_parts", accepted_parts)
    print("len(accepted_parts)", len(accepted_parts))
    for part in accepted_parts:
        print(f"{part} {part.value}")

    result = sum([p.value for p in accepted_parts])
    print("result", result)
    return f"{result}"
