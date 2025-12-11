import contextvars
import logging
import math
import structlog
import networkx as nx
from functools import cache
from .vis import visualize_critical_paths, view_graph_plotly

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
    log.info("day 11 part2")
    result = []
    G = nx.DiGraph()
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        logger.debug(values)
        source, destinations = values.split(":")
        destinations = map(
            lambda x: x.strip(), filter(lambda x: x, destinations.split(" "))
        )
        source = source.strip()
        for destination in destinations:
            logger.debug("add connection", source=source, destination=destination)
            G.add_edge(source, destination)

    logger.debug(G)
    visualize_critical_paths(G, title="Graph Traffic Heatmap")
    # view_graph_plotly(G)

    def count_paths_dag(start_node, end_node):
        @cache
        def _dfs(current):
            if current == end_node:
                return 1

            count = 0
            for neighbor in G.successors(current):
                count += _dfs(neighbor)
            return count

        return _dfs(start_node)

    start = "svr"
    end = "out"
    stop_1 = "dac"
    stop_2 = "fft"

    n_svr_dac = count_paths_dag(start, stop_1)
    n_dac_fft = count_paths_dag(stop_1, stop_2)
    n_fft_out = count_paths_dag(stop_2, end)

    n_svr_fft = count_paths_dag(start, stop_2)
    n_fft_dac = count_paths_dag(stop_2, stop_1)
    n_dac_out = count_paths_dag(stop_1, end)

    path_a_total = n_svr_dac * n_dac_fft * n_fft_out
    path_b_total = n_svr_fft * n_fft_dac * n_dac_out
    result = path_a_total + path_b_total

    print(result)
    return f"{result}"
