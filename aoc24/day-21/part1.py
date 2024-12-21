from functools import cache
from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import networkx as nx
from itertools import product, islice, chain
import matplotlib.pyplot as plt
from collections import deque

logger = structlog.get_logger()


"""+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+"""


"""    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    NORTH_WEST = "NW"
    NORTH_EAST = "NE"
    SOUTH_EAST = "SE"
    SOUTH_WEST = "SW"

    @property
    def oposite(self):
        match self:
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.NORTH
            case Direction.EAST:
                return Direction.WEST
            case Direction.WEST:
                return Direction.EAST
            case Direction.NORTH_WEST:
                return Direction.SOUTH_EAST
            case Direction.NORTH_EAST:
                return Direction.SOUTH_WEST
            case Direction.SOUTH_EAST:
                return Direction.NORTH_WEST
            case Direction.SOUTH_WEST:
                return Direction.NORTH_EAST

    @property
    def clockwise(self):
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.WEST:
                return Direction.NORTH
            case Direction.NORTH_WEST:
                return Direction.NORTH_EAST
            case Direction.NORTH_EAST:
                return Direction.SOUTH_EAST
            case Direction.SOUTH_EAST:
                return Direction.SOUTH_WEST
            case Direction.SOUTH_WEST:
                return Direction.NORTH_WEST

    @property
    def as_arrow(self):
        match self:
            case Direction.NORTH:
                return "^"
            case Direction.SOUTH:
                return "v"
            case Direction.EAST:
                return ">"
            case Direction.WEST:
                return "<"
            case Direction.NORTH_WEST:
                return "\\"
            case Direction.NORTH_EAST:
                return "/"
            case Direction.SOUTH_EAST:
                return "L"
            case Direction.SOUTH_WEST:
                return "J"

    @classmethod
    def from_arrows(cls, c):
        match c:
            case ">":
                return Direction.EAST
            case "<":
                return Direction.WEST
            case "^":
                return Direction.NORTH
            case "v":
                return Direction.SOUTH
            case _:
                raise ValueError(
                    f"can't create Direction from arrow {c} that's not <>^v"
                )


def consturct_num_keypad_graph_directions():
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
    num_keypad_graph.add_edge("A", "0", direction=Direction.WEST)
    num_keypad_graph.add_edge("A", "3", direction=Direction.NORTH)
    num_keypad_graph.add_edge("0", "2", direction=Direction.NORTH)
    num_keypad_graph.add_edge("0", "A", direction=Direction.EAST)
    num_keypad_graph.add_edge("1", "4", direction=Direction.NORTH)
    num_keypad_graph.add_edge("1", "2", direction=Direction.EAST)
    num_keypad_graph.add_edge("2", "1", direction=Direction.WEST)
    num_keypad_graph.add_edge("2", "5", direction=Direction.NORTH)
    num_keypad_graph.add_edge("2", "3", direction=Direction.EAST)
    num_keypad_graph.add_edge("2", "0", direction=Direction.SOUTH)
    num_keypad_graph.add_edge("3", "2", direction=Direction.WEST)
    num_keypad_graph.add_edge("3", "A", direction=Direction.SOUTH)
    num_keypad_graph.add_edge("3", "6", direction=Direction.NORTH)
    num_keypad_graph.add_edge("4", "7", direction=Direction.NORTH)
    num_keypad_graph.add_edge("4", "5", direction=Direction.EAST)
    num_keypad_graph.add_edge("4", "1", direction=Direction.SOUTH)
    num_keypad_graph.add_edge("5", "4", direction=Direction.WEST)
    num_keypad_graph.add_edge("5", "8", direction=Direction.NORTH)
    num_keypad_graph.add_edge("5", "6", direction=Direction.EAST)
    num_keypad_graph.add_edge("5", "2", direction=Direction.SOUTH)
    num_keypad_graph.add_edge("6", "5", direction=Direction.WEST)
    num_keypad_graph.add_edge("6", "9", direction=Direction.NORTH)
    num_keypad_graph.add_edge("6", "3", direction=Direction.SOUTH)
    num_keypad_graph.add_edge("7", "8", direction=Direction.EAST)
    num_keypad_graph.add_edge("7", "4", direction=Direction.SOUTH)
    num_keypad_graph.add_edge("8", "7", direction=Direction.WEST)
    num_keypad_graph.add_edge("8", "9", direction=Direction.EAST)
    num_keypad_graph.add_edge("8", "5", direction=Direction.SOUTH)
    num_keypad_graph.add_edge("9", "8", direction=Direction.WEST)
    num_keypad_graph.add_edge("9", "6", direction=Direction.SOUTH)
    return num_keypad_graph


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


def consturct_dir_keypad_graph_directions():
    """+---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """
    dir_keypad_graph = nx.DiGraph()
    dir_keypad_graph.add_nodes_from(
        [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
    )
    dir_keypad_graph.add_node("A")
    dir_keypad_graph.add_edge(
        Direction.NORTH, Direction.SOUTH, direction=Direction.SOUTH
    )
    dir_keypad_graph.add_edge(Direction.NORTH, "A", direction=Direction.EAST)
    dir_keypad_graph.add_edge("A", Direction.NORTH, direction=Direction.WEST)
    dir_keypad_graph.add_edge("A", Direction.EAST, direction=Direction.SOUTH)
    dir_keypad_graph.add_edge(Direction.SOUTH, Direction.EAST, direction=Direction.EAST)
    dir_keypad_graph.add_edge(Direction.SOUTH, Direction.WEST, direction=Direction.WEST)
    dir_keypad_graph.add_edge(
        Direction.SOUTH, Direction.NORTH, direction=Direction.NORTH
    )
    dir_keypad_graph.add_edge(Direction.EAST, Direction.SOUTH, direction=Direction.WEST)
    dir_keypad_graph.add_edge(Direction.EAST, "A", direction=Direction.NORTH)
    dir_keypad_graph.add_edge(Direction.WEST, Direction.SOUTH, direction=Direction.EAST)
    return dir_keypad_graph


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
    log.info("day 21 part1")
    codes = []
    for index, values in enumerate(values_list):
        codes.append(values)
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )

    num_keypad_graph = consturct_num_keypad_graph()
    dir_keypad_graph = consturct_dir_keypad_graph()
    num_pad_paths = dict(nx.all_pairs_all_shortest_paths(num_keypad_graph))
    dir_pad_paths = dict(nx.all_pairs_all_shortest_paths(dir_keypad_graph))

    @cache
    def get_path(start, end, pad="dir"):
        match pad:
            case "num":
                path_dict = num_pad_paths
                graph = num_keypad_graph
            case "dir":
                path_dict = dir_pad_paths
                graph = dir_keypad_graph
            case _:
                raise ValueError(f"pad {pad} not supported")
        return path_dict[start][end]

    @cache
    def get_options(
        string,
        pad="dir",
    ):
        match pad:
            case "num":
                path_dict = num_pad_paths
                graph = num_keypad_graph
            case "dir":
                path_dict = dir_pad_paths
                graph = dir_keypad_graph
            case _:
                raise ValueError(f"pad {pad} not supported")
        directions_list = []
        if string.count("A") > 1:
            for s in string.split("A"):
                directions_list.extend(get_options(s + "A", pad))
            return directions_list

        start = string[0]
        # log.debug(f"string: {string}", string_to_be_pressed=string_to_be_pressed)
        for i in range(1, len(string)):
            end = string[i]
            # log.debug(f"start: {start}, end: {end}")
            # log.debug(f"path[start]: {path_dict[start]}", start=start, end=end)
            # log.debug(
            #     f"path[start][end][0]: {path_dict[start][end][0]}", start=start, end=end
            # )
            possilbe_paths = path_dict[start][end]
            possilbe_directions = []
            for possible_path in possilbe_paths:
                directions = []
                f = start
                for edge in possible_path[1:]:
                    # log.debug(
                    #     f"edge: {edge}",
                    #     edge=edge,
                    #     possible_path=possible_path,
                    #     graph_f=graph[f],
                    #     graph_edge=graph[f],
                    #     f=f,
                    # )
                    directions.append(graph[f][edge]["direction"])
                    f = edge
                directions.append("A")
                possilbe_directions.append(directions)
            directions_list.append(possilbe_directions)
            start = end

        # log.debug(f"directions_list: {directions_list}")
        return directions_list

    @cache
    def get_directions(
        string,
        pad="dir",
    ):
        match pad:
            case "num":
                path_dict = num_pad_paths
                graph = num_keypad_graph
            case "dir":
                path_dict = dir_pad_paths
                graph = dir_keypad_graph
            case _:
                raise ValueError(f"pad {pad} not supported")

        string_to_be_pressed = string
        start = string_to_be_pressed[0]
        directions_list = []
        # log.debug(f"string: {string}", string_to_be_pressed=string_to_be_pressed)
        for i in range(1, len(string_to_be_pressed)):
            end = string_to_be_pressed[i]
            # log.debug(f"start: {start}, end: {end}")
            # log.debug(f"path[start]: {path_dict[start]}", start=start, end=end)
            # log.debug(
            #     f"path[start][end][0]: {path_dict[start][end][0]}", start=start, end=end
            # )
            possilbe_paths = path_dict[start][end]
            possilbe_directions = []
            for possible_path in possilbe_paths:
                directions = []
                f = start
                for edge in possible_path[1:]:
                    # log.debug(
                    #     f"edge: {edge}",
                    #     edge=edge,
                    #     possible_path=possible_path,
                    #     graph_f=graph[f],
                    #     graph_edge=graph[f],
                    #     f=f,
                    # )
                    directions.append(graph[f][edge]["direction"])
                    f = edge
                directions.append("A")
                possilbe_directions.append(directions)
            directions_list.append(possilbe_directions)
            start = end

        # log.debug(f"directions_list: {directions_list}")
        return directions_list
        result = []
        for sublist in directions_list:
            result.extend(sublist)
            result.append("A")
        return result

    def get_movements(this, that, pad="dir"):
        match pad:
            case "num":
                path_dict = num_pad_paths
                graph = num_keypad_graph
            case "dir":
                path_dict = dir_pad_paths
                graph = dir_keypad_graph
            case _:
                raise ValueError(f"pad {pad} not supported")
        # log.debug(
        #     f"getting movements from {this} to {that}", path_dict__this=path_dict[this]
        # )
        possilbe_paths = path_dict[this][that]
        return (this, that, possilbe_paths)

    # get all paths untill now and yield them with the new path list as well
    def generate_paths_from_current(current: List, paths: List):
        log.debug("generate_paths_from_current", current=current, paths=paths)
        if not current:
            for path in paths:
                yield path
        for path in paths:
            for c in current:
                yield c + path

    n_robots = 2
    results = []
    for code in codes:
        if not code.startswith("A"):
            code = "A" + code
        current = []
        paths_list = []
        for this, that in sliding_window(code, 2):
            _, _, paths = get_movements(this, that, pad="num")
            path_options = []
            for path in paths:
                path_directions = []
                for this1, that1 in sliding_window(path, 2):
                    log.debug(f"this1: {this1}, that1: {that1}")
                    edge_data = num_keypad_graph.get_edge_data(this1, that1)
                    log.debug(edge_data)
                    path_directions.append(edge_data["direction"])
                path_directions.append("A")
                log.debug(f"path_directions: {path_directions}")
                path_options.append(path_directions)

            paths_list.append(path_options)

        log.debug(f"paths_list", paths_list=paths_list)

        combinations = product(*paths_list)
        new_combinations = []
        for combination in combinations:
            log.debug(f"combination", combination=combination)
            way_to_do_combination = []
            ## if first position of combination is not A, then add A to the start
            if combination[0][0] != "A":
                combination[0].insert(0, "A")
            for move in combination:
                paths_list_to_do_move = []
                log.debug(f"move", move=move)
                for this, that in sliding_window(move, 2):
                    _, _, paths = get_movements(this, that, pad="dir")
                    log.debug(f"got paths from: {this} to that: {that}", paths=paths)
                    path_options = []
                    for path in paths:
                        path_directions = []
                        for this1, that1 in sliding_window(path, 2):
                            log.debug(f"this1: {this1}, that1: {that1}", path=path)
                            edge_data = dir_keypad_graph.get_edge_data(this1, that1)
                            log.debug(edge_data)
                            path_directions.append(edge_data["direction"])
                        path_directions.append("A")
                        log.debug(f"path_directions: {path_directions}")
                        path_options.append(path_directions)
                    paths_list_to_do_move.append(path_options)
                way_to_do_combination.append(paths_list_to_do_move)
            new_combinations.append(way_to_do_combination)

        final_combinations = []
        for combination in new_combinations:
            combinations2 = product(*combination)

            new_combinations2 = []
            for combination in combinations2:
                log.debug(f"combination2", combination=combination)
                way_to_do_combination = []
                ## if first position of combination is not A, then add A to the start
                if combination[0][0] != "A":
                    combination[0].insert(0, "A")
                for move in combination:
                    paths_list_to_do_move = []
                    log.debug(f"move", move=move)
                    for this, that in sliding_window(move, 2):
                        _, _, paths = get_movements(this, that, pad="dir")
                        log.debug(
                            f"got paths from: {this} to that: {that}", paths=paths
                        )
                        path_options = []
                        for path in paths:
                            path_directions = []
                            for this1, that1 in sliding_window(path, 2):
                                log.debug(f"this1: {this1}, that1: {that1}", path=path)
                                edge_data = dir_keypad_graph.get_edge_data(this1, that1)
                                log.debug(edge_data)
                                path_directions.append(edge_data["direction"])
                            path_directions.append("A")
                            log.debug(f"path_directions: {path_directions}")
                            path_options.append(path_directions)
                        paths_list_to_do_move.append(path_options)
                    way_to_do_combination.append(paths_list_to_do_move)
                new_combinations2.append(way_to_do_combination)
            final_combinations.append(new_combinations2)

        min_option = min(final_combinations, key=lambda x: len(x))

        code_digits = int("".join(filter(lambda i: i.isdigit(), code)))
        log.debug(
            f"code: {code}",
            code_digits=code_digits,
            best_option_len=min_option,
        )
        code_score = code_digits * min_option
        results.append(code_score)
    return f"{sum(results)}"

    results = []
    for code in codes:
        # get directions form num_keypad_graph
        # use directions in dir_keypad_graph
        # 3 times
        num_solution_graph = nx.MultiDiGraph()
        if not code.startswith("A"):
            code = "A" + code
        for this, that in sliding_window(code, 2):
            if not num_solution_graph.has_edge(this, that):
                this, that, possible_paths = get_movements(this, that, "num")
                for path in possible_paths:
                    num_solution_graph.add_edge(this, that, path=path, cost=len(path))
                    logger.debug(f"add edge from {this} to {that}")
        log.debug(f"graph", num_solution_graph=num_solution_graph)
        log.debug(f"edges", edges=num_solution_graph.edges(keys=True, data=True))
        log.debug(f"nbunch", nbunch=list(num_solution_graph.nbunch_iter(code)))

        def generate_paths_from_pair(graph, this, that):
            paths = nx.all_shortest_paths(graph, this, that)
            for path in paths:
                yield path

        def arst(this, that, prev=""):
            for path in generate_paths_from_pair(num_solution_graph, this, that):
                for this_p, that_p in sliding_window(path, 2):
                    if prev:
                        yield from arst(
                            that_p,
                            that,
                            prev + num_solution_graph[this_p][that_p]["path"],
                        )
                    else:
                        yield from arst(
                            that_p, that, num_solution_graph[this_p][that_p]["path"]
                        )

        def generate_stings_from_graph(graph, input_string):
            for this, that in sliding_window(input_string, 2):
                result = 0

        # nx.draw(num_solution_graph, with_labels=True)
        # plt.tight_layout()
        # plt.show()
        # plt.savefig("num_solution_graph.png")
        # input()
        # return 1
        robot_graphs = []
        for this, that in sliding_window(code, 2):
            paths = nx.all_shortest_paths(num_solution_graph, this, that)
            path_str = ""
            log.debug(
                f"getting best path from {this} to {that}",
                this=this,
                that=that,
                # paths=list(paths),
                edge_data=num_solution_graph.get_edge_data(this, that),
            )
            for path in paths:
                log.debug(path)
                for this_p, that_p in sliding_window(path, 2):
                    log.debug(num_solution_graph[this_p][that_p])
                    path_str += num_solution_graph[this_p][that_p]["path"]
                    log.debug(
                        "path_to_add",
                        path_str=path_str,
                        this_p=this_p,
                        that_p=that_p,
                        edge=num_solution_graph[this_p][that_p],
                    )

        return 1

        for index in range(n_robots):
            for this, that in sliding_window:
                pass
            num_solution_graph.all_shortert_paths()
            num_solution_graph = nx.MultiDiGraph()
            for jindex, option in enumerate(option_strings):
                if not option.startswith("A"):
                    option = "A" + option
                log.debug(
                    f"getting option{jindex}/{len(option_strings)} in robot{index + 1}",
                    option=option,
                )
                movements = get_options(
                    option,
                    "dir",
                )
                for move_options in movements:
                    path_options = []
                    for move_path in move_options:
                        path = ""
                        for move in move_path:
                            path += move
                        path_options.append(path)
                    options.append(path_options)
            log.debug(f"options", possibility=options)
            combinations = list(product(*options))
            option_strings = ["".join(combination) for combination in combinations]
            log.debug(f"option_strings_len", option_strings=len(option_strings))
            min_option = min(option_strings, key=lambda x: len(x))
            option_strings = list(
                filter(lambda x: len(x) == len(min_option), option_strings)
            )
            log.debug(f"option_strings_len", option_strings=len(option_strings))

        best_option = min(option_strings, key=lambda x: len(x))

        code_digits = int("".join(filter(lambda i: i.isdigit(), code)))
        log.debug(
            f"directions: {best_option}",
            code_digits=code_digits,
            best_option_len=len(best_option),
        )
        code_score = code_digits * len(best_option)
        results.append(code_score)
    log.info("results", results=results)
    print(sum(results))
    return f"{sum(results)}"
