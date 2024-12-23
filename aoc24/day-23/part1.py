from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle, combinations
from enum import Enum, StrEnum
from collections import deque, defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

logger = structlog.get_logger()


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
    log.info("day 23 part1")
    G = nx.Graph()
    for index, values in enumerate(values_list):
        G.add_edge(*values.split("-"))
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )

    # nodes = deque(nx.connected_components(G))[0]
    nodes = G.nodes()
    # log.debug("triangles", triangles=deque(nx.triangles(G)))
    log.debug("nodes", nodes=nodes)
    t_nodes = list(filter(lambda n: n.startswith("t"), nodes))
    result_set = set()
    for t_node in t_nodes:
        neighbors = deque(G.neighbors(t_node))
        log.debug("neighbors", neighbors=neighbors, t_node=t_node)
        for combination in combinations(neighbors, 2):
            logger.debug("combination", combination=combination)
            combi_1, combi_2 = combination
            if G.has_edge(combi_1, combi_2):
                combination_set = set()
                combination_set.add(t_node)
                combination_set.add(combi_1)
                combination_set.add(combi_2)
                result_set.add(frozenset(combination_set))
    result = len(result_set)
    print(result)
    return f"{result}"
    # try to remove duplicates?
    log.debug("result_set", result_set=result_set)
    list_of_keys = []
    for group in result_set:
        key = ",".join(sorted(list(group)))
        list_of_keys.append(key)
    log.debug(
        "list_of_keys",
        list_of_keys=sorted(list_of_keys),
        list_of_keys__len=len(list_of_keys),
    )
    filtered_list_of_keys = sorted(list(filter(lambda x: "t" in x, list_of_keys)))

    result = len(set(filtered_list_of_keys))
    for key in filtered_list_of_keys:
        print(key)

    # nx.draw(G, with_labels=True)
    # color = plt.rainbow(np.linspace(0, 1, n))
    # plt.show()
    # plt.savefig("day-23/input.png")
    # input()
    # result = len(result_set)
    print(result)
    return f"{result}"
    for s in result_set:
        log.debug(s)

    log.debug("t_nodes", t_nodes=t_nodes)
    for n in nodes:
        log.debug(G.degree(n))
    two_nodes = list(filter(lambda n: G.degree(n) == 2, nodes))
    log.debug("two_nodes", two_nodes=two_nodes)
    t_in_neighbor_nodes = list(
        filter(
            lambda n: any(["t" in neigbhor for neigbhor in G.neighbors(n)]),
            nodes,
        )
    )
    log.debug("t_in_neighbor_nodes", t_in_neighbor_nodes=t_in_neighbor_nodes)
    result = len(
        list(
            filter(
                lambda n: G.degree(n) >= 2,
                filter(lambda n: "t" in n, deque(nx.connected_components(G))[0]),
            )
        )
    )
    # result = len(
    #     list(
    #         filter(
    #             lambda n: G.degree(n) >= 3,
    #             filter(lambda n: "t" in n, nx.connected_components(G)),
    #         )
    #     )
    # )

    print(result)
    return f"{result}"
