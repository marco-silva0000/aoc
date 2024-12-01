from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

logger = structlog.get_logger()


@dataclass()
class FlipFlop:
    id: str
    outputs: List[str]
    state = False
    inputs: List[str]
    input_values: List[bool]

    def __str__(self):
        outputs = ", ".join(self.outputs)
        return f"%{self.id} -> {outputs}"

@dataclass()
class Conjunction:
    id: str
    outputs: List[str]
    inputs: List[str]
    input_values: List[bool]

    def __str__(self):
        outputs = ", ".join(self.outputs)
        return f"&{self.id} -> {outputs}"

@dataclass()
class Broadcast:
    id = "broadcaster"
    outputs: List[str]

    def __str__(self):
        outputs = ", ".join(self.outputs)
        return f"{self.id} -> {outputs}"

@dataclass()
class Output:
    id: str

    def __str__(self):
        return f"{self.id} -> Fizzle"


type Component = Union[FlipFlop, Conjunction, Broadcast]


@dataclass()
class Pulse:
    source: Component
    target: Component
    value: bool

    def __str__(self):
        value_str = "-low->"
        if self.value:
            value_str = "-high->"

        return f"{self.source.id} {value_str} {self.target.id}"


type Network = Dict[str, Component]


def hit_the_button(network: Network):
    # input()
    from structlog import get_logger
    logger = get_logger()
    logger.debug("hit_the_button")
    low = 1
    high = 0
    start = network["broadcaster"]
    pulse_groups = []
    pulses = []
    for component_id in start.outputs:
        p = Pulse(start, network[component_id], False)
        logger.debug(p)
        pulses.append(p)
        low += 1
    pulse_groups.append(pulses)

    while pulse_groups:
        pulse_group = pulse_groups.pop(0)
        logger.debug("processing pulse group", pulse_groups=pulse_groups)
        for pulse in pulse_group:
            logger.debug("processing pulse", pulse=pulse)
            if isinstance(pulse.target, FlipFlop):
                if not pulse.value:
                    pulse.target.state = not pulse.target.state
                    next_conjunction_pulses = []
                    next_flip_flop_pulses = []
                    for component_id in pulse.target.outputs:
                        source = pulse.target
                        target = network[component_id]
                        value = pulse.target.state
                        p = Pulse(source, target, value)
                        if isinstance(target, Conjunction):
                            logger.debug("target is Conjunction", target=target)
                            next_conjunction_pulses.append(p)
                        else:
                            logger.debug("target is FlipFlop", target=target)
                            next_flip_flop_pulses.append(p)
                        logger.debug(p)
                        if value:
                            high += 1
                        else:
                            low += 1
                    else:
                        logger.debug("next_conjunction_pulses", next_conjunction_pulses=next_conjunction_pulses)
                        logger.debug("next_flip_flop_pulses", next_flip_flop_pulses=next_flip_flop_pulses)
                        if next_conjunction_pulses:
                            pulse_groups.insert(0, next_conjunction_pulses)
                        if next_flip_flop_pulses:
                            pulse_groups.append(next_flip_flop_pulses)
            elif isinstance(pulse.target, Conjunction):
                pulse.target.input_values[pulse.target.inputs.index(pulse.source.id)] = pulse.value
                logger.debug(pulse.target.input_values)
                next_conjunction_pulses = []
                next_flip_flop_pulses = []
                if all([iv for iv in pulse.target.input_values]):
                    for component_id in pulse.target.outputs:
                        source = pulse.target
                        target = network[component_id]
                        p = Pulse(source, target, False)
                        if isinstance(target, Conjunction):
                            logger.debug("target is Conjunction", target=target)
                            next_conjunction_pulses.append(p)
                        else:
                            logger.debug("target is FlipFlop", target=target)
                            next_flip_flop_pulses.append(p)
                        logger.debug(p)
                        low += 1
                    else:
                        logger.debug("next_conjunction_pulses", next_conjunction_pulses=next_conjunction_pulses)
                        logger.debug("next_flip_flop_pulses", next_flip_flop_pulses=next_flip_flop_pulses)
                        if next_conjunction_pulses:
                            pulse_groups.insert(0, next_conjunction_pulses)
                        if next_flip_flop_pulses:
                            pulse_groups.append(next_flip_flop_pulses)
                else:
                    for component_id in pulse.target.outputs:
                        source = pulse.target
                        target = network[component_id]
                        p = Pulse(source, target, True)
                        if isinstance(target, Conjunction):
                            logger.debug("target is Conjunction", target=target)
                            next_conjunction_pulses.append(p)
                        else:
                            logger.debug("target is FlipFlop", target=target)
                            next_flip_flop_pulses.append(p)
                        logger.debug(p)
                        high += 1
                    else:
                        logger.debug("next_conjunction_pulses", next_conjunction_pulses=next_conjunction_pulses)
                        logger.debug("next_flip_flop_pulses", next_flip_flop_pulses=next_flip_flop_pulses)
                        if next_conjunction_pulses:
                            pulse_groups.insert(0, next_conjunction_pulses)
                        if next_flip_flop_pulses:
                            pulse_groups.append(next_flip_flop_pulses)
            elif isinstance(pulse.target, Output):
                pass
            else:
                raise ValueError(f"Unknown component type {type(pulse.target)}")

    logger.debug("hit_the_button result", low=low, high=high)
    return low, high


def part1(values_list, times_to_hit_the_button=1000) -> str:
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )
    from structlog import get_logger
    logger = get_logger()

    network = {}
    for values in values_list:
        logger.debug(values)
        source, targets = values.split(" -> ")
        targets = targets.split(", ")
        logger.debug(targets)
        compinent_type = source[0]
        component_id = source[1:]
        match compinent_type:
            case "&":
                component = Conjunction(component_id, targets, [], [])
            case "%":
                component = FlipFlop(component_id, targets, [], [])
            case "b":
                component_id = source
                component = Broadcast(targets)
            case _:
                raise ValueError(f"Unknown component type {compinent_type}")
        print(component)
        network[component_id] = component
    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    logger.debug("network", network=network)
    for id, component in network.items():
        print(f"{id}: {component}")

    ouptuts_to_add = []
    for component in network.values():
        for component_id in component.outputs:
            try:
                target = network[component_id]
            except KeyError:
                target = Output(component_id)
                ouptuts_to_add.append(component_id)
                # target = network[component_id]
            if isinstance(target, Conjunction) or isinstance(target, FlipFlop):
                target.inputs.append(component.id)
                target.input_values.append(False)
    for id in ouptuts_to_add:
        network[id] = Output(id)


    # times_to_hit_the_button = 1
    low_total = 0
    high_total = 0
    for _ in range(times_to_hit_the_button):
        low, high = hit_the_button(network)
        low_total += low
        high_total += high
    print(low_total, high_total)
    result = low_total * high_total
    print(f"Part 1: {result}")
    return f"{result}"
