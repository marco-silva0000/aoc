from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

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

    def process(self, part: "Part"):
        from structlog import get_logger
        logger = get_logger()
        logger.debug("workflow process", workflow=self.name)
        for rule in self.rules:
            logger = logger.bind(rule=rule)
            if not rule.lhs or not rule.rhs or not rule.operator:
                return rule.result
            lhs = rule.lhs
            rhs = rule.rhs
            operator = rule.operator
            logger.debug("rule", lhs=lhs, rhs=rhs, operator=operator)
            if isinstance(lhs, int):
                logger.debug("lhs is int")
                rhs = getattr(part, rhs)
            if isinstance(rhs, int):
                logger.debug("rhs is int")
                lhs = getattr(part, lhs)
            if operator == Operator.LESS_THAN:
                if lhs < rhs:
                    return rule.result
            elif rule.operator == Operator.GREATER_THAN:
                if lhs > rhs:
                    return rule.result
            else:
                raise Exception(f"Unknown operator: {rule.operator}")
        raise Exception("No rule matched")


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def value(self):
        return self.x + self.m + self.a + self.s

    def process(self, workflows: Dict[str, Workflow]):
        from structlog import get_logger
        logger = get_logger()
        start = workflows["in"]
        current = start
        while True:
            logger.debug("part process", workflow=current.name)
            next = current.process(self)
            match next:
                case Result.Accepted:
                    logger.debug("accepted", workflow=current.name)
                    return Result.Accepted
                case Result.Rejected:
                    logger.debug("rejected", workflow=current.name)
                    return Result.Rejected
                case _:
                    logger.debug("next", next=next)
                    current = workflows[next]
            




def part1(values_list) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    # structlog.configure(
    #     wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    # )
    accepted_parts = []
    rejected_parts = []
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


    parts_list = []
    for i, part_str in enumerate(values_iter):
        # structlog.contextvars.bind_contextvars(
        #     part_iteration=i,
        # )
        part_str = part_str.removeprefix("{").removesuffix("}")
        part_values = part_str.split(",")
        x, m, a, s = [int(value.split("=")[1]) for value in part_values]
        logger.debug("part", x=x, m=m, a=a, s=s)
        part = Part(x=x, m=m, a=a, s=s)
        parts_list.append(part)

    for i, part in enumerate(parts_list):
        structlog.contextvars.bind_contextvars(
            part_iteration=i,
            part=part,
        )
        match part.process(workflows):
            case Result.Accepted:
                accepted_parts.append(part)
            case Result.Rejected:
                rejected_parts.append(part)
            case _:
                raise Exception("Unknown result")

    print("accepted_parts", len(accepted_parts))
    print("rejected_parts", len(rejected_parts))

    result = sum([p.value for p in accepted_parts])
    print("result", result)
    return f"{result}"
