from typing import List, Set, Dict, Tuple, Optional, Union
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from itertools import product, islice, chain, tee
import matplotlib.pyplot as plt
from collections import deque, Counter
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


optimized_num_keypad_graph = nx.MultiDiGraph()
optimized_dir_keypad_graph = nx.MultiDiGraph()

num_keypad_graph = consturct_num_keypad_graph()
dir_keypad_graph = consturct_dir_keypad_graph()
num_pad_paths = dict(nx.all_pairs_all_shortest_paths(num_keypad_graph))
dir_pad_paths = dict(nx.all_pairs_all_shortest_paths(dir_keypad_graph))


@cache
def convert_path_to_directions(path: Tuple[str], pad="dir", add_a=True) -> List:
    match pad:
        case "num":
            path_dict = num_pad_paths
            graph = num_keypad_graph
        case "dir":
            path_dict = dir_pad_paths
            graph = dir_keypad_graph
        case _:
            raise ValueError(f"pad {pad} not supported")
    path_directions = ""
    for this, that in sliding_window(path, 2):
        # logger.debug(f"going from {this} to {that}")
        edge_data = graph.get_edge_data(this, that)
        logger.debug(f"going from {this} to {that}", edge_data=edge_data)
        path_directions += edge_data["direction"]
    if add_a:
        path_directions += "A"
    return path_directions


def save_paths_on_keypads():
    for f, edges in num_pad_paths.items():
        # print(edges)
        for t, paths in edges.items():
            # logger.debug(f"from {f} to {t}")
            for path in paths:
                path_as_directions = convert_path_to_directions(
                    tuple(path), pad="num", add_a=False
                )
                data = {
                    "path": path_as_directions,
                }
                optimized_num_keypad_graph.add_edge(f, t, **data)
    for f, edges in dir_pad_paths.items():
        # print(edges)
        for t, paths in edges.items():
            # logger.debug(f"from {f} to {t}")
            for path in paths:
                path_as_directions = convert_path_to_directions(
                    tuple(path), pad="dir", add_a=False
                )
                data = {
                    "path": path_as_directions,
                }
                optimized_dir_keypad_graph.add_edge(f, t, **data)


save_paths_on_keypads()

optimized_num_pad_paths = dict(
    nx.all_pairs_all_shortest_paths(optimized_num_keypad_graph)
)
optimized_dir_pad_paths = dict(
    nx.all_pairs_all_shortest_paths(optimized_dir_keypad_graph)
)


@cache
def get_paths_from_str(nodes: str, pad="dir") -> List[str]:
    """
    eg. nodes = "029A")
    return all paths from 0 to 2, 2 to 9, 9 to A
    [
        "<A^A>^^AvvvA",
        "<A^A^>^AvvvA",
        "<A^A^^>AvvvA",
    ]

    """
    match pad:
        case "num":
            path_dict = optimized_num_pad_paths
            graph = optimized_num_keypad_graph
        case "dir":
            path_dict = optimized_dir_pad_paths
            graph = optimized_dir_keypad_graph
        case _:
            raise ValueError(f"pad {pad} not supported")

    all_options = []
    if not nodes.startswith("A"):
        nodes = "A" + nodes
    # nodes = "A" + nodes
    for this, that in sliding_window(nodes, 2):
        if this == that:
            all_options.append("A")
        else:
            paths = path_dict[this][that]
            paths = [v["path"] for v in graph.get_edge_data(this, that).values()]
            logger.debug(f"paths from {this} to {that}: {paths}")
            move_options = []
            for path in paths:
                move_options.append(path)
            all_options.append(move_options)
    result = list(product(*all_options))
    logger.debug(f"all_options_product: {result}")
    return result


@cache
def do_robots(keypad_option: str, n_robot=25, pad="dir") -> int:
    if n_robot == 0:
        logger.debug("finished robot=0", keypad_option=keypad_option)
        return len(keypad_option)

    logger.debug(f"{n_robot}_keypad_options: {keypad_option}")
    # if not keypad_option.startswith("A"):
    #     keypad_option = "A" + keypad_option
    expansions = get_paths_from_str(keypad_option, pad=pad)
    logger.debug(
        f"got expansions on robot={n_robot}",
        expansions=expansions,
        keypad_option=keypad_option,
    )
    robot_results = []
    for expansion in expansions:
        expansion_score = 0
        logger.debug(f"requesting on robot={n_robot}", expansion=expansion)
        for jindex, exp in enumerate(expansion):
            # if not exp.startswith("A"):
            #     exp = "A" + exp
            expansion_score += do_robots(exp, n_robot=n_robot - 1, pad="dir")
        robot_results.append(expansion_score)
    logger.debug(f"robot results on robot={n_robot}", robot_results=robot_results)
    return min(robot_results)


def part2(values_list, n_robots=25) -> str:
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

    results = []
    result_tuples = []
    for code in codes:
        # if not code.startswith("A"):
        #     code = f"A{code}"
        # log.debug(f"code: {code}")
        ans = do_robots(code, n_robot=n_robots, pad="num")

        code_digits = int("".join(filter(lambda i: i.isdigit(), code)))
        # log.debug(
        #     f"directions: {min_str}",
        #     code_digits=code_digits,
        #     best_option_len=len(min_str),
        #     min_str=min_str,
        # )
        code_score = code_digits * ans
        results.append(code_score)
        result_tuples.append((code_digits, ans, code_score))
    log.info(f"results: {results}")
    log.info(f"result_tuples: {result_tuples}")
    print(str(sum(results)))
    return str(sum(results))
    return f"{len(result)}"
