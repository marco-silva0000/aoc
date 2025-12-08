from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle, combinations, islice
from enum import Enum, StrEnum
from shapely import Point
from shapely.ops import nearest_points
import geopandas as gpd
import networkx as nx
from scipy.spatial import cKDTree
from scipy.spatial.distance import pdist
import numpy as np
import pandas as pd


logger = structlog.get_logger()


def part1(values_list, n=999) -> str:
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
    log.info("day 8 part1")
    result = []
    points = []
    dataframe = []
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        point = Point(*values.split(","))
        points.append(point)
        dataframe.append([index, point])

    df = gpd.GeoDataFrame(dataframe, columns=["ID", "geometry"])
    coords = np.array(list(df.geometry.apply(lambda p: (p.x, p.y, p.z))))
    dist_array = pdist(coords, metric="euclidean")
    logger.debug(dist_array)
    pair_indices = list(combinations(df["ID"], 2))
    logger.debug(pair_indices)

    edges_df = pd.DataFrame(pair_indices, columns=["ID_A", "ID_B"])
    edges_df["distance"] = dist_array
    edges_df = edges_df.sort_values(by="distance").reset_index(drop=True)
    logger.debug(f"Calculated {len(edges_df)} pairs.")
    logger.debug(edges_df.head(n))

    G_final = nx.Graph()
    G_final.add_nodes_from(df["ID"])

    processed_count = 0

    for row in edges_df.itertuples():
        if processed_count >= n:
            break
        u, v = row.ID_A, row.ID_B
        if not nx.has_path(G_final, u, v):
            G_final.add_edge(u, v, weight=row.distance)
        processed_count += 1

    circuits = list(nx.connected_components(G_final))
    circuit_sizes = [len(c) for c in circuits]
    circuit_sizes.sort(reverse=True)

    log.info(f"Processed {processed_count} pairs.")
    log.info(f"Total Circuits: {len(circuits)}")
    log.info(f"Top 5 Circuit Sizes: {circuit_sizes[:5]}")

    result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]

    print(result)
    return f"{result}"
