from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from collections import deque
import numpy as np
import networkx as nx
import concurrent.futures
import ilpy

logger = structlog.get_logger()


class StateType(StrEnum):
    OFF = "."
    ON = "#"


def action_func(action: tuple, state: str) -> str:
    next_state = [c for c in state]
    for operation_index in action:
        match next_state[operation_index]:
            case StateType.ON:
                next_state[operation_index] = StateType.OFF
            case StateType.OFF:
                next_state[operation_index] = StateType.ON
    logger.debug(
        "action_func", action=action, state=state, next_state="".join(next_state)
    )
    return "".join(next_state)


@dataclass()
class Machine:
    state: list
    actions: list[tuple]
    action_matrix: list[list[int]]
    joltage: tuple[int]
    graph: any = None

    def ilp_solve(self):
        num_buttons = len(self.actions)
        solver = ilpy.LinearSolver(num_buttons, ilpy.VariableType.Integer)
        objective = ilpy.LinearObjective()
        for i in range(num_buttons):
            objective.set_coefficient(i, 1.0)
        solver.set_objective(objective)
        for index_joltage, target_joltage in enumerate(self.joltage):
            constraint = ilpy.LinearConstraint()
            for action_index, action in enumerate(self.actions):
                if index_joltage in action:
                    constraint.set_coefficient(action_index, 1.0)

            constraint.set_relation(ilpy.Relation.Equal)
            constraint.set_value(target_joltage)
            solver.add_constraint(constraint)

        # non negative button presses
        for i in range(num_buttons):
            nn_constraint = ilpy.LinearConstraint()
            nn_constraint.set_coefficient(i, 1.0)
            nn_constraint.set_relation(ilpy.Relation.GreaterEqual)
            nn_constraint.set_value(0)
            solver.add_constraint(nn_constraint)
        solution = solver.solve()
        value = int(solution.objective_value)
        logger.info("found solution", solution=solution, value=value)
        return int(round(value))


def process_machine(machine):
    shortest_joltage_path = machine.ilp_solve()
    logger.info(
        f"found shortest_joltage_path for {machine.joltage} with length {shortest_joltage_path}"
    )
    return shortest_joltage_path


def make_action_matrix(actions, joltage):
    result = []
    for action in actions:
        action_arr = [0] * len(joltage)
        for action_index in action:
            action_arr[action_index] += 1
        result.append(action_arr)
    return result


def part2(values_list) -> str:
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
    log.info("day 10 part2")
    machines = []
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        state_goal, *buttons, joltage = values.split()
        state_goal = [StateType(c) for c in state_goal[1:-1]]
        actions = [eval(button.replace(")", ",)")) for button in buttons]
        actions.sort(key=len, reverse=True)
        joltage = tuple(map(int, joltage[1:-1].split(",")))
        action_matrix = make_action_matrix(actions, joltage)
        machine = Machine(state_goal, actions, action_matrix, joltage)
        logger.info("machine", machine=machine)
        machines.append(machine)

    result = []

    # result = list(map(process_machine, machines))
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = list(executor.map(process_machine, machines))

    print(result)
    result = sum(result)
    print(result)
    return f"{result}"
