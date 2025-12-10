from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from collections import deque
import networkx as nx

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


class State(list):
    def __hash__(self):
        return hash("".join(self))


@dataclass()
class Machine:
    state: State
    actions: list(tuple)
    joltage: list[int]
    graph: any = None

    def generate_graph(self):
        initial_state = "".join([StateType.OFF] * len(self.state))
        goal_state = "".join(self.state)
        logger.debug(
            "generate_graph",
            goal=self.state,
            actions=self.actions,
            initial_state=initial_state,
        )
        G = nx.DiGraph()
        G.add_node(initial_state)

        queue = deque([initial_state])
        visited = set([initial_state])

        logger.info(f"Starting Search: {initial_state} -> {goal_state}")
        found = False
        while queue:
            current = queue.popleft()
            if current == goal_state:
                found = True
                self.graph = G
                return self.graph

            for action in self.actions:
                next_state = action_func(action, current)

                if next_state is not None and next_state not in visited:
                    visited.add(next_state)
                    queue.append(next_state)
                    G.add_edge(current, next_state, action=action)
        raise "couldnt find path"

    def shortest_path(self):
        initial_state = "".join([StateType.OFF] * len(self.state))
        goal = "".join(self.state)
        path = nx.shortest_path(self.graph, source=initial_state, target=goal)[1:]
        logger.debug("shortest_path", goal=goal, initial_state=initial_state, path=path)
        return path


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
    log.info("day 10 part1")
    machines = []
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        state_goal, *buttons, joltage = values.split()
        state_goal = [StateType(c) for c in state_goal[1:-1]]
        actions = [eval(button.replace(")", ",)")) for button in buttons]
        joltage = joltage[1:-1].split(",")
        machine = Machine(state_goal, actions, joltage)
        logger.info("machine", machine=machine)
        machines.append(machine)

    result = []
    for machine in machines:
        machine.generate_graph()
        result.append(machine.shortest_path())

    result = sum(map(len, result))
    print(result)
    return f"{result}"
