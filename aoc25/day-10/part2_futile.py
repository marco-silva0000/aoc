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


def action_func_joltage(action: tuple[int], state: tuple[int]) -> tuple[int]:
    next_state = list(state)
    # logger.debug("action_func start", action=action, state=state, next_state=next_state)
    for operation_index in action:
        next_state[operation_index] += 1
    next_state = tuple(next_state)
    # logger.debug("action_func", action=action, state=state, next_state=next_state)
    return next_state


def action_func_joltage_from_matrix(
    action_matrix: list[int], state: tuple[int]
) -> tuple[int]:
    next_state = list(state)
    next_state = np.add(next_state, action_matrix)
    next_state = tuple(next_state)
    # logger.debug("action_func", action=action, state=state, next_state=next_state)
    return next_state


def is_valid_joltage_state(next_state: tuple[int], joltage: tuple[int]) -> tuple[int]:
    # logger.debug("is_valid_joltage_state", next_state=next_state, joltage=joltage)
    diff = np.subtract(joltage, next_state)
    return (diff >= 0).all()


class State(list):
    def __hash__(self):
        return hash("".join(self))


@dataclass()
class Machine:
    state: State
    actions: list[tuple]
    action_matrix: list[list[int]]
    joltage: tuple[int]
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

    def generate_joltage_graph(self):
        initial_state = tuple([0] * len(self.joltage))
        goal_state = self.joltage
        logger.debug(
            "generate_joltage_graph",
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

            for action in self.action_matrix:
                next_state = action_func_joltage_from_matrix(action, current)

                if (
                    next_state is not None
                    and next_state not in visited
                    and is_valid_joltage_state(next_state, self.joltage)
                ):
                    visited.add(next_state)
                    queue.append(next_state)
                    G.add_edge(current, next_state, action=action)
        raise "couldnt find path"

    def generate_joltage_graph_path(self):
        initial_state = tuple([0] * len(self.joltage))
        goal_state = self.joltage
        logger.debug(
            "generate_joltage_graph",
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
                break

            for action in self.actions:
                next_state = action_func_joltage(action, current)

                if (
                    next_state is not None
                    and next_state not in visited
                    and is_valid_joltage_state(next_state, self.joltage)
                ):
                    visited.add(next_state)
                    queue.append(next_state)
                    G.add_edge(current, next_state, action=action)

    def generate_joltage_non_graph_path(self):
        initial_state = tuple([0] * len(self.joltage))
        goal_state = self.joltage
        logger.debug(
            "generate_joltage_graph",
            goal=self.state,
            actions=self.actions,
            initial_state=initial_state,
        )

        queue = deque([initial_state])
        came_from = {initial_state: None}

        logger.info(f"Starting Search: {initial_state} -> {goal_state}")
        while queue:
            current = queue.popleft()
            if current == goal_state:
                found = True
                break

            for action in self.action_matrix:
                next_state = action_func_joltage_from_matrix(action, current)

                if (
                    next_state is not None
                    and next_state not in came_from
                    and is_valid_joltage_state(next_state, self.joltage)
                ):
                    came_from[next_state] = current
                    queue.append(next_state)
        return reconstruct_path(came_from, current)

    def generate_joltage_non_graph_non_path(self):
        initial_state = tuple([0] * len(self.joltage))
        goal_state = self.joltage
        logger.debug(
            "generate_joltage_graph",
            goal=self.state,
            actions=self.actions,
            initial_state=initial_state,
        )

        queue = deque([(initial_state, 0)])
        visited = {initial_state}

        logger.info(f"Starting Search: {initial_state} -> {goal_state}")
        while queue:
            current, dist = queue.popleft()
            if current == goal_state:
                found = True
                return dist

            for action in self.action_matrix:
                next_state = action_func_joltage_from_matrix(action, current)

                if (
                    next_state is not None
                    and next_state not in visited
                    and is_valid_joltage_state(next_state, self.joltage)
                ):
                    visited.add(current)
                    queue.append((next_state, dist + 1))
        raise "error, cant find path"

    def shortest_path(self):
        initial_state = "".join([StateType.OFF] * len(self.state))
        goal = "".join(self.state)
        path = nx.shortest_path(self.graph, source=initial_state, target=goal)[1:]
        logger.debug("shortest_path", goal=goal, initial_state=initial_state, path=path)
        return path

    def shortest_joltage_path(self):
        initial_state = tuple([0] * len(self.joltage))
        goal = self.joltage
        path = nx.shortest_path(self.graph, source=initial_state, target=goal)[1:]
        logger.debug("shortest_path", goal=goal, initial_state=initial_state, path=path)
        return path


def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1][1:]


def shortest_joltage_path(graph, joltage):
    initial_state = tuple([0] * len(joltage))
    goal = joltage
    path = nx.shortest_path(graph, source=initial_state, target=goal)[1:]
    logger.debug("shortest_path", goal=goal, initial_state=initial_state, path=path)
    return path


def process_machine(machine):
    shortest_joltage_path = machine.generate_joltage_non_graph_non_path()
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

    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        result = list(executor.map(process_machine, machines))

    print(result)
    result = sum(result)
    print(result)
    return f"{result}"
