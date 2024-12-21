from typing import List, Set, Dict, Tuple, Optional, Union
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from itertools import product, islice, chain
import matplotlib.pyplot as plt
from collections import deque
import networkx as nx
from functools import cache

logger = structlog.get_logger()


def consturct_num_keypad_graph():
    """+---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
        | 0 | A |
        +---+---+"""

    # nodes from 0 to 9 plus A
    num_keypad_graph = nx.DiGraph()
    num_keypad_graph.add_nodes_from([str(i) for i in range(10)])
    num_keypad_graph.add_node("A")
    num_keypad_graph.add_edge("A", "0", direction="<")
    num_keypad_graph.add_edge("A", "3", direction="^")
    num_keypad_graph.add_edge("0", "2", direction="^")
    num_keypad_graph.add_edge("0", "A", direction=">")
    num_keypad_graph.add_edge("1", "4", direction="^")
    num_keypad_graph.add_edge("1", "2", direction=">")
    num_keypad_graph.add_edge("2", "1", direction="<")
    num_keypad_graph.add_edge("2", "5", direction="^")
    num_keypad_graph.add_edge("2", "3", direction=">")
    num_keypad_graph.add_edge("2", "0", direction="v")
    num_keypad_graph.add_edge("3", "2", direction="<")
    num_keypad_graph.add_edge("3", "A", direction="v")
    num_keypad_graph.add_edge("3", "6", direction="^")
    num_keypad_graph.add_edge("4", "7", direction="^")
    num_keypad_graph.add_edge("4", "5", direction=">")
    num_keypad_graph.add_edge("4", "1", direction="v")
    num_keypad_graph.add_edge("5", "4", direction="<")
    num_keypad_graph.add_edge("5", "8", direction="^")
    num_keypad_graph.add_edge("5", "6", direction=">")
    num_keypad_graph.add_edge("5", "2", direction="v")
    num_keypad_graph.add_edge("6", "5", direction="<")
    num_keypad_graph.add_edge("6", "9", direction="^")
    num_keypad_graph.add_edge("6", "3", direction="v")
    num_keypad_graph.add_edge("7", "8", direction=">")
    num_keypad_graph.add_edge("7", "4", direction="v")
    num_keypad_graph.add_edge("8", "7", direction="<")
    num_keypad_graph.add_edge("8", "9", direction=">")
    num_keypad_graph.add_edge("8", "5", direction="v")
    num_keypad_graph.add_edge("9", "8", direction="<")
    num_keypad_graph.add_edge("9", "6", direction="v")
    return num_keypad_graph


def consturct_dir_keypad_graph():
    """+---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """
    dir_keypad_graph = nx.DiGraph()
    dir_keypad_graph.add_nodes_from(["^", "v", ">", "<"])
    dir_keypad_graph.add_node("A")
    dir_keypad_graph.add_edge("^", "v", direction="v")
    dir_keypad_graph.add_edge("^", "A", direction=">")
    dir_keypad_graph.add_edge("A", "^", direction="<")
    dir_keypad_graph.add_edge("A", ">", direction="v")
    dir_keypad_graph.add_edge("v", ">", direction=">")
    dir_keypad_graph.add_edge("v", "<", direction="<")
    dir_keypad_graph.add_edge("v", "^", direction="^")
    dir_keypad_graph.add_edge(">", "v", direction="<")
    dir_keypad_graph.add_edge(">", "A", direction="^")
    dir_keypad_graph.add_edge("<", "v", direction=">")
    return dir_keypad_graph


def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


num_keypad_graph = consturct_num_keypad_graph()
dir_keypad_graph = consturct_dir_keypad_graph()
num_pad_paths = dict(nx.all_pairs_all_shortest_paths(num_keypad_graph))
dir_pad_paths = dict(nx.all_pairs_all_shortest_paths(dir_keypad_graph))


@cache
def convert_path_to_directions(path: Tuple[str], pad="dir") -> List:
    match pad:
        case "num":
            path_dict = num_pad_paths
            graph = num_keypad_graph
        case "dir":
            path_dict = dir_pad_paths
            graph = dir_keypad_graph
        case _:
            raise ValueError(f"pad {pad} not supported")
    path_directions = []
    for this, that in sliding_window(path, 2):
        edge_data = graph.get_edge_data(this, that)
        path_directions.append(edge_data["direction"])
    path_directions.append("A")
    return path_directions


def old_generate_paths_from_of_nodes(nodes: Tuple[str], pad="dir"):
    """
    eg. nodes = ("0", "2", "9", "A")
    yield all paths from 0 to 2, 2 to 9, 9 to A
    [
            ["<", "A", "^", "A", ">", "^", "^", "A", "v", "v", "v", "A"],
            ["<", "A", "^", "A", "^", ">", "^", "A", "v", "v", "v", "A"],
            ["<", "A", "^", "A", "^", "^", ">", "A", "v", "v", "v", "A"],
    ]

    """
    match pad:
        case "num":
            path_dict = num_pad_paths
            graph = num_keypad_graph
        case "dir":
            path_dict = dir_pad_paths
            graph = dir_keypad_graph
        case _:
            raise ValueError(f"pad {pad} not supported")

    all_options = []
    for this, that in sliding_window(nodes, 2):
        paths = path_dict[this][that]
        # logger.debug(f"paths from {this} to {that}: {paths}")
        move_options = []
        for path in paths:
            # logger.debug(f"path: {path}")
            directions = convert_path_to_directions(tuple(path), pad)
            move_options.append(directions)
        all_options.append(move_options)
    # logger.debug(f"all_options: {all_options}")
    for moves in product(*all_options):
        # logger.debug(f"moves: {moves}")
        yield list(chain(*moves))
    #


@cache
def generate_paths_from_of_nodes(nodes: Tuple[str], pad="dir"):
    """
    eg. nodes = ("0", "2", "9", "A")
    yield all paths from 0 to 2, 2 to 9, 9 to A
    [
            ["<", "A", "^", "A", ">", "^", "^", "A", "v", "v", "v", "A"],
            ["<", "A", "^", "A", "^", ">", "^", "A", "v", "v", "v", "A"],
            ["<", "A", "^", "A", "^", "^", ">", "A", "v", "v", "v", "A"],
    ]

    """
    match pad:
        case "num":
            path_dict = num_pad_paths
            graph = num_keypad_graph
        case "dir":
            path_dict = dir_pad_paths
            graph = dir_keypad_graph
        case _:
            raise ValueError(f"pad {pad} not supported")

    all_options = []
    for this, that in sliding_window(nodes, 2):
        paths = path_dict[this][that]
        # logger.debug(f"paths from {this} to {that}: {paths}")
        move_options = []
        for path in paths:
            # logger.debug(f"path: {path}")
            directions = convert_path_to_directions(tuple(path), pad)
            move_options.append(directions)
        all_options.append(move_options)
    # logger.debug(f"all_options: {all_options}")
    yield from product(*all_options)
    # for moves in product(*all_options):
    # logger.debug(f"moves: {moves}")
    # yield list(chain(*moves))
    # yield from chain(*moves)
    # yield list(chain(*moves))


def flatten(xss):
    return [x for xs in xss for x in xs]


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
    log.info("day 21 part2")
    result = []
    codes = []
    for index, values in enumerate(values_list):
        codes.append(values)
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )

    def do_robots(keypad_options, n_robot=2):
        logger.debug("doing robot", n_robot=n_robot)
        if n_robot == 0:
            min_str_len = math.inf
            min_str = ""
            logger.debug("doing robot = 0", keypad_options=keypad_options)
            for third_robot_option in keypad_options:
                if len(third_robot_option) < min_str_len:
                    min_str_len = len(third_robot_option)
                    min_str = "".join(third_robot_option)
            yield min_str
            return

        logger.debug(f"{n_robot}_keypad_options: {keypad_options}")
        for first_keypad_option in keypad_options:
            logger.debug(f"{n_robot}_keypad_option: {first_keypad_option}")
            if not first_keypad_option[0] == "A":
                first_keypad_option.insert(0, "A")
            nodes = tuple(first_keypad_option)
            paths_gen = generate_paths_from_of_nodes(nodes, "dir")
            for path in paths_gen:
                logger.debug(f"{n_robot}_generated_path: {path}")
                yield from do_robots(path, n_robot=n_robot - 1)

            # for option in generate_paths_from_of_nodes(nodes, "dir"):
            #     logger.debug(f"{n_robot}_generated_option: {option}")
            #     yield from do_robots(option, n_robot=n_robot - 1)

    def do_robots(keypad_options, n_robot=2):
        if n_robot == 0:
            min_str_len = math.inf
            min_str = ""
            for option in keypad_options:
                logger.debug("doing robot=0", option=option)
                if len(option) < min_str_len:
                    min_str_len = len(option)
                    min_str = "".join(option)
            yield min_str
            return

        logger.debug(f"{n_robot}_keypad_options: {keypad_options}")
        for first_keypad_option in keypad_options:
            first_keypad_option = flatten(first_keypad_option)
            logger.debug(f"{n_robot}_keypad_option: {first_keypad_option}")
            if not first_keypad_option[0] == "A":
                first_keypad_option.insert(0, "A")
            nodes = tuple(first_keypad_option)
            paths_gen = generate_paths_from_of_nodes(nodes, "dir")
            yield from do_robots(paths_gen, n_robot=n_robot - 1)

            # for path in paths_gen:
            #     path = flatten(path)
            #     logger.debug(f"{n_robot}_generated_path: {path}")
            #     yield from do_robots(path, n_robot=n_robot - 1)

    n_robots = 3
    results = []
    result_tuples = []
    for code in codes:
        min_str_len = math.inf
        min_str = ""
        if not code.startswith("A"):
            code = f"A{code}"
        # log.debug(f"code: {code}")
        nodes = tuple(code)
        first_keypad_options = generate_paths_from_of_nodes(nodes, "num")
        # log.debug("first_keypad_options", first_keypad_options=first_keypad_options)
        for option in do_robots(first_keypad_options, n_robot=2):
            # log.debug("got option", option=option)
            if option and len(option) < min_str_len:
                min_str_len = len(option)
                min_str = option

        code_digits = int("".join(filter(lambda i: i.isdigit(), code)))
        log.debug(
            f"directions: {min_str}",
            code_digits=code_digits,
            best_option_len=len(min_str),
            min_str=min_str,
        )
        code_score = code_digits * len(min_str)
        results.append(code_score)
        result_tuples.append((code_digits, len(min_str), min_str))
    log.debug(f"results: {results}")
    log.debug(f"result_tuples: {result_tuples}")
    print(str(sum(results)))
    return str(sum(results))
    return f"{len(result)}"
