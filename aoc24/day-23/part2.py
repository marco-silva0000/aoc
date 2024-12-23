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
    for clique in nx.find_cliques(G):
        log.debug("clique", clique=clique)
    log.debug("result", result=result)

    print(result)
    return f"{result}"
