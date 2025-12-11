import math
import networkx as nx
from functools import cache
import plotly.graph_objects as go


def get_node_traffic(G, start_node, end_node):
    """
    Calculates how many paths pass through each node using DP (Fast).
    Returns a dict: {node: number_of_paths_through_here}
    """

    # 1. Calculate paths FROM start TO every node
    @cache
    def count_paths_from_start(current):
        if current == start_node:
            return 1
        return sum(count_paths_from_start(pred) for pred in G.predecessors(current))

    # 2. Calculate paths FROM every node TO end
    @cache
    def count_paths_to_end(current):
        if current == end_node:
            return 1
        return sum(count_paths_to_end(succ) for succ in G.successors(current))

    # 3. Combine them: Traffic(Node) = (Start->Node) * (Node->End)
    traffic = {}
    max_traffic = 0

    # We only care about nodes that can actually reach the end
    relevant_nodes = set()

    try:
        # Quick check to ensure nodes exist
        if start_node not in G or end_node not in G:
            return {}, 0

        for node in G.nodes():
            try:
                # Use standard networkx for reachability check to prune dead branches
                if nx.has_path(G, start_node, node) and nx.has_path(G, node, end_node):
                    relevant_nodes.add(node)
            except:
                continue

        for node in relevant_nodes:
            from_start = count_paths_from_start(node)
            to_end = count_paths_to_end(node)
            total = from_start * to_end
            traffic[node] = total
            if total > max_traffic:
                max_traffic = total

    except RecursionError:
        print("Graph too deep for recursion, visualization might be partial.")

    return traffic, max_traffic


def visualize_critical_paths(G, title="Path Heatmap"):
    start, end = "svr", "out"
    targets = ["dac", "fft"]  # The nodes you must visit

    # Calculate traffic statistics (O(N) speed)
    traffic_map, max_traffic = get_node_traffic(G, start, end)

    # --- Plotly Setup ---
    # Use Multipartite layout if possible for "flow" charts, otherwise Spring
    # Creating a custom 'layer' attribute for multipartite if you wanted to try it,
    # but standard spring is safer for generic inputs.
    pos = nx.spring_layout(G, seed=42, k=0.5, iterations=50)

    edge_x, edge_y = [], []
    for edge in G.edges():
        if edge[0] in traffic_map and edge[1] in traffic_map:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#ccc"),
        hoverinfo="none",
        mode="lines",
    )

    node_x, node_y = [], []
    node_text = []
    node_colors = []
    node_sizes = []
    node_borders = []

    for node in G.nodes():
        if node not in traffic_map:
            continue  # Skip dead nodes

        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        path_count = traffic_map.get(node, 0)

        # Color Logic: Logarithmic scale for heat because paths grow exponentially
        if node in [start, end]:
            color_val = 1.0  # Max heat color
            size_val = 30
            border_color = "black"
        elif node in targets:
            color_val = 0.9
            size_val = 30
            border_color = "red"  # Highlight targets
        else:
            # Normalize log scale for gradient
            if max_traffic > 1:
                color_val = math.log(path_count + 1) / math.log(max_traffic + 1)
            else:
                color_val = 0
            size_val = 10 + (color_val * 15)  # Bigger nodes = more traffic
            border_color = "white"

        node_text.append(f"{node}<br>Paths: {path_count:,}")
        node_colors.append(color_val)
        node_sizes.append(size_val)
        node_borders.append(border_color)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=[
            n if n in [start, end] + targets else "" for n in traffic_map
        ],  # Only label key nodes on map
        textposition="top center",
        hovertext=node_text,
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="Plasma",  # Dark blue to bright yellow
            color=node_colors,
            size=node_sizes,
            line=dict(width=2, color=node_borders),
            colorbar=dict(title="Path Traffic (Log Scale)"),
        ),
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=title,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=0, l=0, r=0, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    fig.show()


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
