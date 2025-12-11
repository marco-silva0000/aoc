from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import networkx as nx
import plotly.graph_objects as go


logger = structlog.get_logger()

data = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""


def view_graph_plotly(G: nx.Graph, title="Graph Visualization"):
    """
    Visualizes a NetworkX graph using Plotly.
    """
    # 1. Generate Layout (Calculate X,Y positions for nodes)
    # spring_layout tries to position nodes so edges are short and nodes are spread out
    pos = nx.spring_layout(G, seed=42)

    # 2. Create Edges Trace (The lines)
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_y.append(y0)
        edge_x.append(x1)
        edge_y.append(y1)
        # Add None to break the line between distinct edges
        edge_x.append(None)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    # 3. Create Nodes Trace (The dots)
    node_x = []
    node_y = []
    node_text = []
    node_adjacencies = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

        # Calculate number of connections for coloring
        node_adjacencies.append(len(G.adj[node]))

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=node_text,
        textposition="top center",
        marker=dict(
            showscale=True,
            colorscale="YlGnBu",
            reversescale=True,
            color=node_adjacencies,  # Color by number of connections
            size=20,
            colorbar=dict(
                thickness=15,
                title="Node Connections",
                xanchor="left",
            ),
            line_width=2,
        ),
    )

    # 4. Create the Figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=title,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    # Optional: Add arrows for Directional Graph (DiGraph)
    # Plotly lines don't natively support arrows easily, so we add annotations
    if isinstance(G, nx.DiGraph):
        for edge in G.edges():
            start = pos[edge[0]]
            end = pos[edge[1]]
            fig.add_annotation(
                x=end[0],
                y=end[1],
                ax=start[0],
                ay=start[1],
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                text="",
                showarrow=True,
                arrowhead=2,
                arrowsize=2,
                arrowwidth=1.5,
                arrowcolor="#555",
                standoff=15,
                opacity=0.7,
            )

    fig.show()


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
    log.info("day 11 part1")
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

    start = "you"
    end = "out"
    paths = nx.all_simple_paths(G, source=start, target=end)
    logger.debug(G)
    # view_graph_plotly(G)
    result = 0
    for path in paths:
        logger.debug(path)
        result += 1

    print(result)
    return f"{result}"
