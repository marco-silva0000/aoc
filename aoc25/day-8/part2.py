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
import plotly.graph_objects as go


logger = structlog.get_logger()


# ai genned visualize_mst_plotly
def visualize_mst_plotly(df, G_full):
    mst_edges = list(nx.minimum_spanning_edges(G_full, algorithm="kruskal", data=False))

    # 1. Create Nodes Trace
    node_x, node_y, node_z = [], [], []
    text_labels = []

    for idx, row in df.iterrows():
        p = row.geometry
        node_x.append(p.x)
        node_y.append(p.y)
        node_z.append(p.z)
        text_labels.append(f"ID: {row.ID}")

    node_trace = go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode="markers",
        marker=dict(size=4, color="blue"),
        text=text_labels,
        name="Junction Boxes",
    )

    # 2. Create Edges Trace
    # Plotly draws lines by connecting points in a sequence.
    # To draw separate lines, we insert 'None' between pairs.
    edge_x, edge_y, edge_z = [], [], []

    for u, v in mst_edges:
        p1 = df.loc[df.ID == u, "geometry"].iloc[0]
        p2 = df.loc[df.ID == v, "geometry"].iloc[0]

        edge_x.extend([p1.x, p2.x, None])
        edge_y.extend([p1.y, p2.y, None])
        edge_z.extend([p1.z, p2.z, None])

    edge_trace = go.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode="lines",
        line=dict(color="red", width=2),
        opacity=0.5,
        name="Connections",
    )

    # 3. Render
    fig = go.Figure(data=[node_trace, edge_trace])
    fig.update_layout(
        title="3D Network Connections",
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
        margin=dict(l=0, r=0, b=0, t=40),
    )
    fig.show()


def part2(values_list, n=999) -> str:
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
    log.info("day 8 part2")
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
    logger.debug(f"Calculated {len(edges_df)} pairs.")
    G = nx.Graph()
    G.add_nodes_from(df["ID"])

    edges_list = list(
        edges_df[["ID_A", "ID_B", "distance"]].itertuples(index=False, name=None)
    )
    G.add_weighted_edges_from(edges_list)

    mst_edges = list(nx.minimum_spanning_edges(G, algorithm="kruskal", data=False))

    last_u, last_v = mst_edges[-1]

    geom_u = df.loc[df.ID == last_u, "geometry"].iloc[0]
    geom_v = df.loc[df.ID == last_v, "geometry"].iloc[0]

    print(f"Final connection between ID {last_u} and {last_v}")
    print(f"Coords: {geom_u} <-> {geom_v}")

    result = int(geom_u.x * geom_v.x)
    visualize_mst_plotly(df, G)
    print(result)
    return f"{result}"
