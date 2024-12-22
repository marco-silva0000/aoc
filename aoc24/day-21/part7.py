from typing import List, Set, Dict, Tuple, Optional, Union
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from itertools import product, islice, chain
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
        # logger.debug(f"going from {this} to {that}", edge_data=edge_data)
        path_directions += edge_data["direction"]
    if add_a:
        path_directions += "A"
    return path_directions


def count_changes(value):
    counter = 0
    for i in range(1, len(value)):
        if value[i - 1] != value[i]:
            counter += 1
    return counter


for f, edges in num_pad_paths.items():
    # print(edges)
    for t, paths in edges.items():
        best_path = None
        best_path_score = math.inf
        best_paths = []
        # logger.debug(f"from {f} to {t}")
        for path in paths:
            path_as_directions = convert_path_to_directions(
                tuple(path), pad="num", add_a=False
            )
            path_score = (
                len(path_as_directions) * 100
                + count_changes(path_as_directions) * 10
                + len(Counter(path_as_directions).keys())
            )
            if path_score == best_path_score:
                best_paths.append(path_as_directions)
                logger.debug(
                    "found another good path",
                    path_as_directions=path_as_directions,
                    best_paths=best_paths,
                )
            elif path_score < best_path_score:
                best_path_score = path_score
                best_path = path_as_directions
                best_paths = [path_as_directions]

        logger.debug(
            "final best paths",
            best_path_score=best_path_score,
            best_paths=best_paths,
        )
        for best_path in best_paths:
            data = {
                "path": best_path,
                "cost": best_path_score,
                "weight": best_path_score,
            }
            optimized_num_keypad_graph.add_edge(f, t, **data)

for f, edges in dir_pad_paths.items():
    # print(edges)
    for t, paths in edges.items():
        best_path = None
        best_path_score = math.inf
        best_paths = []
        logger.debug(f"from {f} to {t}")
        for path in paths:
            path_as_directions = convert_path_to_directions(
                tuple(path), pad="dir", add_a=False
            )
            path_score = (
                len(path_as_directions) * 100
                + count_changes(path_as_directions) * 10
                + len(Counter(path_as_directions).keys())
            )
            if path_score == best_path_score:
                best_paths.append(path_as_directions)
                logger.debug(
                    "found another good path",
                    path_as_directions=path_as_directions,
                    best_paths=best_paths,
                )
            elif path_score < best_path_score:
                best_path_score = path_score
                best_path = path_as_directions
                best_paths = [path_as_directions]

        for best_path in best_paths:
            data = {
                "path": best_path,
                "cost": best_path_score,
                "weight": best_path_score,
            }
            optimized_dir_keypad_graph.add_edge(f, t, **data)


optimized_num_pad_paths = dict(
    nx.all_pairs_all_shortest_paths(optimized_num_keypad_graph)
)
optimized_dir_pad_paths = dict(
    nx.all_pairs_all_shortest_paths(optimized_dir_keypad_graph)
)
# print(optimized_num_pad_paths)
# print(optimized_dir_pad_paths)


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
    logger.debug(f"input path {path}")

    for this, that in sliding_window(path, 2):
        # logger.debug(f"going from {this} to {that}")
        edge_data = graph.get_edge_data(this, that)
        logger.debug(f"going from {this} to {that}", edge_data=edge_data, pad=pad)
        path_directions += edge_data["direction"]
    if add_a:
        path_directions += "A"
    return path_directions


@cache
def convert_path_to_directions_optimized(path: Tuple[str], pad="dir") -> List:
    match pad:
        case "num":
            path_dict = dir_pad_paths
            graph = dir_keypad_graph
        case "dir":
            path_dict = dir_pad_paths
            graph = dir_keypad_graph
        case _:
            raise ValueError(f"pad {pad} not supported")
    path_directions = ""
    logger.debug(f"input path {path}", pad=pad)
    for this, that in sliding_window(path, 2):
        edge_data = graph.get_edge_data(this, that)
        logger.debug("edge_data", edge_data=edge_data, this=this, that=that)
        path_directions += edge_data["direction"]
    path_directions += "A"
    return path_directions


@cache
def generate_paths_from_of_node_str(nodes: str, pad="dir"):
    """
    eg. nodes = "029A")
    yield all paths from 0 to 2, 2 to 9, 9 to A
    [
        "<A^A>^^AvvvA",
        "<A^A^>^AvvvA",
        "<A^A^^>AvvvA",
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
        logger.debug(f"paths from {this} to {that}: {paths}")
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


@cache
def generate_paths_from_of_node_str_optimized(nodes: str, pad="dir"):
    """
    eg. nodes = "029A")
    yield all paths from 0 to 2, 2 to 9, 9 to A
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
    for this, that in sliding_window(nodes, 2):
        # logger.debug(f"paths from {this} to {that}: [this]{path_dict[this]}")

        paths = path_dict[this][that]
        paths = [v["path"] for v in graph.get_edge_data(this, that).values()]
        # logger.debug(f"paths from this:{this} to that:{that}: {paths}")
        if pad == "num":
            move_options = [path + "A" for path in paths]
        else:
            move_options = [paths[0] + "A"]
        all_options.append(move_options)
    # logger.debug(f"all_options: {all_options}")
    rs = []
    for option in product(*all_options):
        option = "".join(option)
        logger.debug(f"option: {option}")
        rs.append(option)
    return rs

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

    # @cache
    def do_robots2(keypad_option, n_robot=25):
        if n_robot == 0:
            logger.debug("doing robot=0", keypad_option=keypad_option)
            return len(keypad_option)
            # min_str_len = math.inf
            # min_str = ""
            # for option in keypad_option:
            #     logger.debug("doing robot=0", option=option)
            #     if len(option) < min_str_len:
            #         min_str_len = len(option)
            #         min_str = "".join(option)
            # yield min_str
            # return

        logger.info(f"{n_robot}_keypad_options: {keypad_option}")
        if not keypad_option == "A":
            keypad_option = "A" + keypad_option
        paths_gen = generate_paths_from_of_node_str_optimized(keypad_option, "dir")
        rs = []
        for paths in paths_gen:
            logger.debug(f"requesting on robot={n_robot}", paths=paths)
            r = do_robots2(paths, n_robot=n_robot - 1)
            rs.append(r)
        return min(rs)

    n_robots = 25
    results = []
    result_tuples = []
    for code in codes:
        min_str_len = math.inf
        min_str = ""
        if not code.startswith("A"):
            code = f"A{code}"
        # log.debug(f"code: {code}")
        first_keypad_options = generate_paths_from_of_node_str_optimized(code, "num")
        log.debug("first_keypad_options", first_keypad_options=first_keypad_options)
        for option in first_keypad_options:
            log.debug("option", option=option)
            op = "".join(option)
            ans = do_robots2(op, n_robot=n_robots)
            for r in ans:
                if r and len(r) < min_str_len:
                    min_str_len = len(r)
                    min_str = r

        code_digits = int("".join(filter(lambda i: i.isdigit(), code)))
        # log.debug(
        #     f"directions: {min_str}",
        #     code_digits=code_digits,
        #     best_option_len=len(min_str),
        #     min_str=min_str,
        # )
        code_score = code_digits * len(min_str)
        results.append(code_score)
        result_tuples.append((code_digits, len(min_str), min_str))
    log.info(f"results: {results}")
    log.info(f"result_tuples: {result_tuples}")
    print(str(sum(results)))
    return str(sum(results))
    return f"{len(result)}"
