from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
import numpy as np

logger = structlog.get_logger()


@dataclass()
class Point:
    x: int
    y: int


@dataclass
class Machine:
    button_a: Point
    button_b: Point
    prize: Point


def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (gcd, x, y)


def calculate_k_range(general_solution, dx_factor, dy_factor):
    x0, y0 = general_solution

    k_min_x = -x0 // dx_factor if dx_factor != 0 else -100
    k_max_x = (100 - x0) // dx_factor if dx_factor != 0 else 100
    k_min_y = -y0 // dy_factor if dy_factor != 0 else -100
    k_max_y = (100 - y0) // dy_factor if dy_factor != 0 else 100

    k_min = int(max(k_min_x, k_min_y))
    k_max = int(min(k_max_x, k_max_y))

    return k_min, k_max


def find_min_cost_solution(machine, cost_a, cost_b):
    dx1, dy1 = machine.button_a.x, machine.button_a.y
    dx2, dy2 = machine.button_b.x, machine.button_b.y
    targetX, targetY = machine.prize.x, machine.prize.y

    gcd_dx, x0_dx, y0_dx = extended_gcd(dx1, dx2)
    gcd_dy, x0_dy, y0_dy = extended_gcd(dy1, dy2)

    if targetX % gcd_dx != 0 or targetY % gcd_dy != 0:
        return 0, 0, 0  # No solution exists

    x0_dx *= targetX // gcd_dx
    y0_dx *= targetX // gcd_dx
    x0_dy *= targetY // gcd_dy
    y0_dy *= targetY // gcd_dy

    dx_factor = dx2 // gcd_dx
    dy_factor = dy2 // gcd_dy

    k_min, k_max = calculate_k_range((x0_dx, y0_dy), dx_factor, dy_factor)

    min_cost = float("inf")
    best_press_A = None
    best_press_B = None

    for k in range(k_min, k_max + 1):
        a = x0_dx + k * dy_factor
        b = y0_dy - k * dx_factor

        if 0 <= a <= 100 and 0 <= b <= 100:
            current_cost = a * cost_a + b * cost_b
            if current_cost < min_cost:
                min_cost = current_cost
                best_press_A = a
                best_press_B = b

    if best_press_A is None or best_press_B is None:
        return 0, 0, 0  # No non-negative solution found

    return best_press_A, best_press_B, min_cost


def find_min_cost(machine, a_cost, b_cost):
    A_x = machine.button_a.x
    A_y = machine.button_a.y
    B_x = machine.button_b.x
    B_y = machine.button_b.y
    P_x = machine.prize.x
    P_y = machine.prize.y
    min_cost = float("inf")
    optimal_a = optimal_b = 0

    # Trying different possible values for a and solving for b
    for a in range(P_x // A_x + 1):
        rem_x = P_x - a * A_x
        rem_y = P_y - a * A_y

        if rem_x % B_x == 0 and rem_y % B_y == 0:
            b_x = rem_x // B_x
            b_y = rem_y // B_y

            if b_x >= 0 and b_y >= 0 and b_x == b_y:
                cost = 3 * a + b_x

                if cost < min_cost:
                    min_cost = cost
                    optimal_a = a
                    optimal_b = b_x

    if min_cost == float("inf"):
        return 0, 0, 0  # No solution found

    return optimal_a, optimal_b, min_cost


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
    log.info("day 13 part1")

    a_button_cost = 3
    b_button_cost = 1
    machines = []
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        log.debug(values)
        if "A" in values:
            x, y = map(
                int,
                [part[2:] for part in values.removeprefix("Button A: ").split(", ")],
            )
            button_a = Point(x, y)
        elif "B" in values:
            x, y = map(
                int,
                [part[2:] for part in values.removeprefix("Button B: ").split(", ")],
            )
            button_b = Point(x, y)
        elif "Prize" in values:
            log.debug(values)
            x, y = map(
                int,
                [part[2:] for part in values.removeprefix("Prize: ").split(", ")],
            )
            prize = Point(x, y)
        elif not values:
            machine = Machine(button_a, button_b, prize)
            machines.append(machine)
    print(machines)
    result = []
    for machine in machines:
        result.append(find_min_cost(machine, a_button_cost, b_button_cost))
    print(result)
    result_val = sum([r[2] for r in result])

    print(result_val)
    return f"{result_val}"
