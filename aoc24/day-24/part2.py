from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import networkx as nx
from collections import defaultdict
from matplotlib import pyplot as plt

logger = structlog.get_logger()


def draw_graph(graph, nodelist=[], layered=False, ms_layered=False):
    logger.debug("draw_graph", nodelist=nodelist)
    # pos = nx.spring_layout(graph, seed=3113794652)  # positions for all nodes
    pos = nx.nx_agraph.graphviz_layout(graph, prog="dot", args="")
    # pos = nx.nx_pydot.graphviz_layout(graph, prog="dot")
    # pos = nx.multipartite_layout(graph)
    if ms_layered:
        max_gens = len(list(nx.topological_generations(graph)))
        logger.info("max_gens", max_gens=max_gens)
        for layer, nodes in enumerate(nx.topological_generations(graph)):
            # `multipartite_layout` expects the layer as a node attribute, so add the
            # numeric layer value as a node attribute
            for node in nodes:
                node_layer = None
                if isinstance(node, OperationNode):
                    # if a z node is successor
                    if any(
                        n.startswith("z") and n[1:].isdigit()
                        for n in graph.successors(node)
                    ):
                        node_layer = max_gens - 1
                    # if a x or y node is a ancestor
                    elif any(
                        (n.startswith("x") and n[1:].isdigit())
                        or (n.startswith("y") and n[1:].isdigit())
                        for n in graph.predecessors(node)
                    ):
                        node_layer = 1
                elif node.startswith("z") and node[1:].isdigit():
                    node_layer = max_gens
                elif (
                    node.startswith("x")
                    and node[1:].isdigit()
                    or node.startswith("y")
                    and node[1:].isdigit()
                ):
                    node_layer = 0

                graph.nodes[node]["layer"] = node_layer if node_layer else layer

        pos = nx.multipartite_layout(graph, subset_key="layer")
    if layered:
        max_gens = len(list(nx.topological_generations(graph)))
        logger.info("max_gens", max_gens=max_gens)
        for layer, nodes in enumerate(nx.topological_generations(graph)):
            # `multipartite_layout` expects the layer as a node attribute, so add the
            # numeric layer value as a node attribute
            for node in nodes:
                graph.nodes[node]["layer"] = layer

        pos = nx.multipartite_layout(graph, subset_key="layer")

    not_nodelist = [n for n in pos if n not in nodelist]
    # nodes
    options = {"edgecolors": "tab:gray", "node_size": 400, "alpha": 0.9}
    grey_nodes = [
        n for n, value in graph.nodes.data("value") if isinstance(n, OperationNode)
    ]
    green_nodes = [
        n
        for n, value in graph.nodes.data("value")
        if value == 1 and n not in grey_nodes
    ]
    red_nodes = [
        n
        for n, value in graph.nodes.data("value")
        if value == 0 and n not in grey_nodes
    ]
    locked_nodes = [n for n, value in graph.nodes.data("locked") if value]
    print(green_nodes)
    n1 = nx.draw_networkx_nodes(
        graph, pos, nodelist=green_nodes, node_color="tab:green", **options
    )
    n2 = nx.draw_networkx_nodes(
        graph, pos, nodelist=red_nodes, node_color="tab:red", **options
    )
    n3 = nx.draw_networkx_nodes(
        graph, pos, nodelist=grey_nodes, node_color="tab:grey", **options
    )
    rings = nx.draw_networkx_nodes(
        graph,
        pos,
        node_size=600,
        nodelist=locked_nodes,
        node_color="tab:purple",
    )
    n1.set_zorder(2)
    n2.set_zorder(2)
    n2.set_zorder(2)
    rings.set_zorder(1)

    # edges
    nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=graph.edges(nodelist),
        width=2,
        alpha=0.5,
        edge_color="tab:grey",
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
    plt.savefig("day-24/input.png")
    plt.show()


class Operation(StrEnum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"


def flatten(xss):
    return [x for xs in xss for x in xs]


@dataclass
class Wire:
    wire_a: str
    wire_b: str
    to_wire: str
    operation: Operation


@dataclass
class OperationNode:
    operation: Operation
    id: int

    def calculate(self, this, that):
        match self.operation:
            case Operation.AND:
                return this & that
            case Operation.OR:
                return this | that
            case Operation.XOR:
                return this ^ that

    def __hash__(self) -> int:
        return hash((self.id, self.operation))

    def __str__(self) -> str:
        return f"{self.operation} {self.id}"


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
    log.info("day 24 part2")
    result = []
    on_registers = True
    registers = dict()
    wires = []
    for index, values in enumerate(values_list):
        if not values:
            on_registers = False
            continue
        if on_registers:
            register, value = values.split(": ")
            registers[register] = int(value)
        else:
            f, t = values.split(" -> ")
            wire_a, operation, wire_b = f.split(" ")
            operation = Operation(operation)
            wires.append(Wire(wire_a, wire_b, t, operation))

        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
    og_registers = registers.copy()
    for register, value in registers.items():
        log.debug("register", register=register, value=value)
    for wire in wires:
        log.debug("wire", wire=wire)

    def process_wires():
        processed_wires = False
        while not processed_wires:
            # find wire with all dependencies resolved
            for wire in wires:
                if wire.to_wire in registers:
                    continue
                if wire.wire_a in registers and wire.wire_b in registers:
                    match wire.operation:
                        case Operation.AND:
                            registers[wire.to_wire] = (
                                registers[wire.wire_a] & registers[wire.wire_b]
                            )
                            break
                        case Operation.OR:
                            registers[wire.to_wire] = (
                                registers[wire.wire_a] | registers[wire.wire_b]
                            )
                            break
                        case Operation.XOR:
                            registers[wire.to_wire] = (
                                registers[wire.wire_a] ^ registers[wire.wire_b]
                            )
                            break
            else:
                processed_wires = True

    def print_registers():
        for register, value in sorted(registers.items(), key=lambda x: x[0]):
            log.debug("register", register=register, value=value)

    def get_z_registers():
        return sorted(
            list(
                filter(
                    lambda r: r.startswith("z") and r[1:].isdigit(),
                    [register for register in registers.keys()],
                )
            ),
            reverse=True,
        )

    def clear_all_but_starting_registers(graph):
        for node in list(graph.nodes()):
            if isinstance(node, OperationNode):
                graph.nodes[node]["value"] = None
                log.info("clearing op", node=node)
            else:
                if node.startswith("x") and node[1:].isdigit():
                    continue
                elif node.startswith("y") and node[1:].isdigit():
                    continue
                else:
                    log.info("clearing reg", node=node)
                    graph.nodes[node]["value"] = None

    def propagate_operation_nodes(graph):
        clear_all_but_starting_registers(graph)
        operation_nodes = sorted(
            [node for node in graph.nodes() if isinstance(node, OperationNode)],
            key=lambda x: x.id,
        )
        empty_operation_nodes = list(
            filter(lambda x: graph.nodes[x].get("value") is None, operation_nodes)
        )
        while empty_operation_nodes:
            for operation_node in empty_operation_nodes:
                log.info("operation_node", operation_node=operation_node)
                x, y = list(graph.predecessors(operation_node))
                x_value = graph.nodes[x].get("value")
                y_value = graph.nodes[y].get("value")

                if x_value is not None and y_value is not None:
                    log.info(f"values {x_value} {y_value}")
                    graph.nodes[operation_node]["value"] = operation_node.calculate(
                        x_value, y_value
                    )
                    log.info("value", value=graph.nodes[operation_node]["value"])
                    for successor in graph.successors(operation_node):
                        graph.nodes[successor]["value"] = graph.nodes[operation_node][
                            "value"
                        ]
                        log.info("successor", successor=successor)
            empty_operation_nodes = list(
                filter(lambda x: graph.nodes[x].get("value") is None, operation_nodes)
            )

    def get_z_registers_from_graph(graph):
        return sorted(
            list(
                filter(
                    lambda r: r.startswith("z") and r[1:].isdigit(),
                    [
                        node
                        for node in graph.nodes()
                        if not isinstance(node, OperationNode)
                    ],
                )
            ),
            reverse=True,
        )

    def get_x_registers_from_graph(graph):
        return sorted(
            list(
                filter(
                    lambda r: r.startswith("x") and r[1:].isdigit(),
                    [
                        node
                        for node in graph.nodes()
                        if not isinstance(node, OperationNode)
                    ],
                )
            ),
            reverse=True,
        )

    def get_y_registers_from_graph(graph):
        return sorted(
            list(
                filter(
                    lambda r: r.startswith("y") and r[1:].isdigit(),
                    [
                        node
                        for node in graph.nodes()
                        if not isinstance(node, OperationNode)
                    ],
                )
            ),
            reverse=True,
        )

    def get_and_gates_from_graph(graph):
        return [
            node
            for node in graph.nodes()
            if isinstance(node, OperationNode) and node.operation == Operation.AND
        ]

    def get_or_gates_from_graph(graph):
        return [
            node
            for node in graph.nodes()
            if isinstance(node, OperationNode) and node.operation == Operation.OR
        ]

    # def delete_useless_nodes(graph)
    #     for node in list(graph.nodes()):
    #         if not isinstance(node, OperationNode):
    #             # none only has one predecessor and one successor

    process_wires()

    G = nx.DiGraph()

    for id, wire in enumerate(wires):
        operation_node = OperationNode(wire.operation, id)
        wire_x_data = {"locked": wire.wire_a in og_registers.keys(), "stickiness": 0}
        if wire.wire_a in registers:
            log.debug("wire_a", wire_a=wire.wire_a, value=registers[wire.wire_a])
            wire_x_data["value"] = registers[wire.wire_a]
        wire_y_data = {"locked": wire.wire_b in og_registers.keys(), "stickiness": 0}
        if wire.wire_b in registers:
            log.debug("wire_b", wire_b=wire.wire_b, value=registers[wire.wire_b])
            wire_y_data["value"] = registers[wire.wire_b]

        G.add_node(operation_node, **{"stickiness": 0})
        G.add_node(wire.wire_a, **wire_x_data)
        G.add_node(wire.wire_b, **wire_y_data)
        G.add_edge(wire.wire_a, operation_node)
        G.add_edge(wire.wire_b, operation_node)
        G.add_edge(operation_node, wire.to_wire)

    is_dag = nx.is_directed_acyclic_graph(G)
    log.info("is_dag", is_dag=is_dag)

    for node in G.nodes():
        # add empty value to all nodes without value
        if not G.nodes[node].get("value"):
            G.nodes[node]["value"] = 0

    propagate_operation_nodes(G)

    def print_input_output_result(graph):
        x_registers = get_x_registers_from_graph(graph)
        log.debug("x_registers", x_registers=x_registers)
        x_values_list = [str(graph.nodes[a]["value"]) for a in x_registers]
        x_values_str = "".join(x_values_list)
        x_value = int("".join(x_values_str), 2)
        y_registers = get_y_registers_from_graph(graph)
        y_values_list = [str(graph.nodes[b]["value"]) for b in y_registers]
        y_values_str = "".join(y_values_list)
        y_value = int("".join(y_values_str), 2)
        z_registers = get_z_registers_from_graph(graph)
        for register in z_registers:
            log.info("z_register", register=register)
            log.info("z_register_value", value=graph.nodes[register]["value"])
        z_values_list = [str(graph.nodes[node]["value"]) for node in z_registers]
        z_values_str = "".join(z_values_list)
        z_value = int(z_values_str, 2)
        max_len = max(len(x_values_str), len(y_values_str), len(z_values_str))

        z_goal = x_value + y_value
        z_goal_str = bin(z_goal)[2:]
        z_diff = z_goal ^ z_value
        z_diff_str = bin(z_diff)[2:]

        log.info(f"{x_values_str:0>{max_len}}", x_value=x_value)
        log.info(f"{y_values_str:0>{max_len}}", y_value=y_value)
        log.info(f"{z_values_str:0>{max_len}}", z_value=z_value)
        log.info(f"{z_goal_str:0>{max_len}}", z_goal=z_goal)
        log.info(f"{z_diff_str:0>{max_len}}", z_diff=z_diff)

    print_input_output_result(G)

    g2 = G.copy()
    x_registers = get_x_registers_from_graph(g2)
    y_registers = get_y_registers_from_graph(g2)
    z_registers = get_z_registers_from_graph(g2)
    # for index, z_register in enumerate(reversed(z_registers)):
    #     try:
    #         bit = z_diff_str[index]
    #         if bit == "0":
    #             for ancestor in nx.ancestors(g2, z_register):
    #                 # update stickiness value
    #                 g2.nodes[ancestor]["stickiness"] = (
    #                     g2.nodes[ancestor]["stickiness"] + 1
    #                 )
    #     except IndexError:
    #         continue

    carry_register = z_registers[0]
    for index, z_register in enumerate(reversed(z_registers)):
        # identify sus predecessors. need to be XOR
        predecessors = list(g2.predecessors(z_register))

        if len(predecessors) > 1:
            log.info(
                "is sus, more than 1 predecessor",
                predecessors=predecessors,
                z_register=z_register,
            )
        elif z_register == carry_register:
            if predecessors[0].operation != Operation.AND:
                log.info(
                    "is sus, carry is not AND",
                    predecessors=predecessors,
                    z_register=z_register,
                )
        else:
            if predecessors[0].operation != Operation.XOR:
                log.info(
                    "is sus, not XOR", predecessors=predecessors, z_register=z_register
                )
    # carry and only has one successor, swap sus with carry

    for or_gate in get_or_gates_from_graph(g2):
        # if g2.out_degree(or_gate) != 1:
        #     log.info("is sus, not like other AND", and_gate=and_gate)
        # # else:
        successor = list(g2.successors(or_gate))[0]
        if g2.out_degree(successor) == 1:
            log.info(
                "is sus, OR successor with only one connection, might be carry",
                or_gate=or_gate,
            )
    # didn't find any sus...

    # all x registers need to connect to one xor and one and
    for x_register in x_registers:
        if g2.out_degree(x_register) != 2:
            log.info(
                "is sus, x register, not 2 out degree",
                x_register=x_register,
                out_degree=g2.out_degree(x_register),
            )

        has_xor = False
        has_or = False
        for successor in g2.successors(x_register):
            if successor.operation == Operation.XOR:
                has_xor = True
            if successor.operation == Operation.AND:
                has_or = True
        if not has_xor or not has_or:
            log.info(
                "is sus, x register",
                x_register=x_register,
                has_xor=has_xor,
                has_or=has_or,
            )

    # all y registers need to connect to one xor and one and
    for y_register in y_registers:
        if g2.out_degree(y_register) != 2:
            log.info(
                "is sus, y register, not 2 out degree",
                y_register=y_register,
                out_degree=g2.out_degree(y_register),
            )

        has_xor = False
        has_or = False
        for successor in g2.successors(y_register):
            # log.info("successor", successor=successor)
            if successor.operation == Operation.XOR:
                has_xor = True
            if successor.operation == Operation.AND:
                has_or = True
        if not has_xor or not has_or:
            log.info(
                "is sus, y register",
                y_register=y_register,
                has_xor=has_xor,
                has_or=has_or,
            )
    # all except 0 go to a xor xor chain
    n_bits = 44
    maybe_broken_z_registers = []
    for i in range(1, n_bits):
        x_register = f"x{i:02}"
        y_register = f"y{i:02}"
        z_register = f"z{i:02}"
        x_shortest_path = nx.shortest_path(g2, x_register, z_register)
        y_shortest_path = nx.shortest_path(g2, y_register, z_register)
        x_xor = 0
        for node in x_shortest_path:
            if isinstance(node, OperationNode) and node.operation == Operation.XOR:
                x_xor += 1
        y_xor = 0
        for node in y_shortest_path:
            if isinstance(node, OperationNode) and node.operation == Operation.XOR:
                y_xor += 1
        if x_xor != 2:
            log.info(
                "is sus, x register",
                x_register=x_register,
                x_xor=x_xor,
                x_shortest_path=x_shortest_path,
            )
            maybe_broken_z_registers.append(z_register)
        if y_xor != 2:
            log.info(
                "is sus, y register",
                y_register=y_register,
                y_xor=y_xor,
                y_shortest_path=y_shortest_path,
            )
            maybe_broken_z_registers.append(z_register)
    maybe_broken_z_registers = sorted(list(set(maybe_broken_z_registers)))
    log.info(
        "maybe_broken_z_registers", maybe_broken_z_registers=maybe_broken_z_registers
    )

    first_broken_z_register = maybe_broken_z_registers[0]
    ancestors = nx.ancestors(g2, first_broken_z_register)
    ancestors.add(first_broken_z_register)
    ancestors_sub_graph = g2.subgraph(ancestors)
    # next z register may have a broken path
    z_register_id = int(first_broken_z_register[1:])
    adjacent_z_register = f"z{z_register_id + 1:0>2}"
    source_x_register = f"x{z_register_id:0>2}"
    source_y_register = f"y{z_register_id:0>2}"
    # adjacent_ancestors = nx.ancestors(g2, adjacent_z_register)
    # adjacent_ancestors_sub_graph = g2.subgraph(ancestors)
    # unioned_sub_graph = nx.compose(ancestors_sub_graph, adjacent_ancestors_sub_graph)

    path_from_x = nx.all_simple_paths(g2, source_x_register, first_broken_z_register)
    graph_from_x = nx.subgraph(g2, flatten(path_from_x))
    path_from_y = nx.all_simple_paths(g2, source_y_register, first_broken_z_register)
    graph_from_y = nx.subgraph(g2, flatten(path_from_y))
    path_from_x_to_adjacent = nx.all_simple_paths(
        g2, source_x_register, adjacent_z_register
    )
    graph_from_x_to_adjacent = nx.subgraph(g2, flatten(path_from_x_to_adjacent))
    path_from_y_to_adjacent = nx.all_simple_paths(
        g2, source_y_register, adjacent_z_register
    )
    graph_from_y_to_adjacent = nx.subgraph(g2, flatten(path_from_y_to_adjacent))
    both = nx.compose_all(
        [graph_from_x, graph_from_y, graph_from_x_to_adjacent, graph_from_y_to_adjacent]
    )
    # draw_graph(both, layered=False)
    # y06 AND x06 -> fdv is sus, should be carry, should go to dbp
    # x06 XOR y06 -> dbp is sus, should go to z06, through fdv, test swap
    # make XOR 151 point to fdv and make AND 75 point to dbp
    # cut edges
    # xor151_node = OperationNode(Operation.XOR, 151)
    # and75_node = OperationNode(Operation.AND, 75)
    # log.info("xor151_node", xor151_node=xor151_node)
    # log.info("and75_node", and75_node=and75_node)

    # g2.remove_edge(xor151_node, "dbp")
    # g2.remove_edge(and75_node, "fdv")
    # g2.add_edge(xor151_node, "fdv")
    # g2.add_edge(and75_node, "dbp")

    # x15 AND y15 -> z15 is sus, output can't just be the and, must be the cary bit, outputs to the or(pkt or ckj)
    # ckj comes from xor, can't go to or, qbw XOR fqf -> ckj is sus
    # try swap??
    # success

    # rqt OR rdt -> z23 is sus, needs to come from xor
    # there's a xor xor chain with XOR 146 and XOR 62, should go to Z
    # maybe nsr XOR gsd -> kdf
    # try swap
    # success

    # vbt AND vqr -> z39 is sus, can't come from and, there's a xor xor chain that goes to rpp
    # vqr XOR vbt -> rpp
    # try swap

    propagate_operation_nodes(g2)
    print_input_output_result(g2)

    path_from_x = nx.all_simple_paths(g2, source_x_register, first_broken_z_register)
    graph_from_x = nx.subgraph(g2, flatten(path_from_x))
    path_from_y = nx.all_simple_paths(g2, source_y_register, first_broken_z_register)
    graph_from_y = nx.subgraph(g2, flatten(path_from_y))
    path_from_x_to_adjacent = nx.all_simple_paths(
        g2, source_x_register, adjacent_z_register
    )
    graph_from_x_to_adjacent = nx.subgraph(g2, flatten(path_from_x_to_adjacent))
    path_from_y_to_adjacent = nx.all_simple_paths(
        g2, source_y_register, adjacent_z_register
    )
    graph_from_y_to_adjacent = nx.subgraph(g2, flatten(path_from_y_to_adjacent))
    both = nx.compose_all(
        [graph_from_x, graph_from_y, graph_from_x_to_adjacent, graph_from_y_to_adjacent]
    )
    draw_graph(both, layered=False)

    ancestors = nx.ancestors(g2, adjacent_z_register)
    ancestors.add(adjacent_z_register)
    ancestors_sub_graph = g2.subgraph(ancestors)
    draw_graph(ancestors_sub_graph, layered=False)
    # from xn to zn, goes through 2 xor gates and nothing else.
    # from yn to zn, goes through 2 xor gates and nothing else.
    # xor closest to zn is between cary of n-1 and result of xor between xn and yn
    # to make the cary bit, take output from xn first xor, send to and gate with output from yn first xor

    # for index, z_register in enumerate(reversed(z_registers)):
    #     bit = z_diff_str[index]
    #     if bit == "1":  # found a bit that is wrong
    #         # get the ancestor with the lowest stickiness value
    #         lowest_stickiness = math.inf
    #         lowest_stickiness_ancestor = None
    #         second_lowest_stickiness_ancestor = None
    #         for ancestor in nx.ancestors(g2, z_register):
    #             if g2.nodes[ancestor]["stickiness"] < lowest_stickiness:
    #                 lowest_stickiness = g2.nodes[ancestor]["stickiness"]
    #                 second_lowest_stickiness_ancestor = lowest_stickiness_ancestor
    #                 lowest_stickiness_ancestor = ancestor
    #         log.info(
    #             "ancestor",
    #             ancestor=lowest_stickiness_ancestor,
    #             stickiness=g2.nodes[lowest_stickiness_ancestor]["stickiness"],
    #         )
    #         log.info(
    #             "second_ancestor",
    #             second_ancestor=second_lowest_stickiness_ancestor,
    #             second_stickiness=g2.nodes[second_lowest_stickiness_ancestor][
    #                 "stickiness"
    #             ],
    #         )
    #         break

    result = [str(registers[register]) for register in z_registers]

    result_num = int("".join(result), 2)
    draw_graph(G)
    print(result_num)
    return f"{result_num}"
