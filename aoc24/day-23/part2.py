from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle, combinations, tee
from enum import Enum, StrEnum
from collections import deque, defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

logger = structlog.get_logger()


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
    log.info("day 23 part2")
    G = nx.Graph()
    for index, values in enumerate(values_list):
        G.add_edge(*values.split("-"))
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
    result = ",".join(
        sorted(sorted(nx.find_cliques(G), key=lambda x: len(x), reverse=True)[0])
    )
    log.debug("result", result=result)

    print(result)

    nodes_in_clique = result.split(",")

    def draw_graph(graph, nodelist=[]):
        log.debug("draw_graph", nodelist=nodelist)
        pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

        not_nodelist = [n for n in pos if n not in nodelist]
        # nodes
        options = {"edgecolors": "tab:gray", "node_size": 400, "alpha": 0.9}
        nx.draw_networkx_nodes(
            graph, pos, nodelist=nodelist, node_color="tab:red", **options
        )
        nx.draw_networkx_nodes(
            graph, pos, nodelist=not_nodelist, node_color="tab:blue", **options
        )

        # edges
        nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.5)
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=graph.edges(nodelist),
            width=2,
            alpha=0.5,
            edge_color="tab:red",
        )
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=graph.edges(not_nodelist),
            width=2,
            alpha=0.5,
            edge_color="tab:blue",
        )
        nx.draw_networkx_labels(graph, pos, font_size=12, font_family="sans-serif")
        plt.tight_layout()
        plt.axis("off")
        plt.savefig("day-23/input.png")
        plt.show()

    draw_graph(G, nodelist=nodes_in_clique)

    return f"{result}"
