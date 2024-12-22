from typing import List, Set, Dict, Tuple, Optional, Union
import contextvars
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle, islice
from collections import defaultdict, deque, Counter

logger = structlog.get_logger()


def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def calc_secret_number(n):
    n2 = n ^ (n << 6) % 16777216
    n3 = (n2 >> 5) ^ n2 % 16777216
    return n3 ^ (n3 << 11) % 16777216


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
    log.info("day 22 part2")
    numbers = []
    for index, values in enumerate(values_list):
        structlog.contextvars.bind_contextvars(
            iteration=index,
        )
        numbers.append(int(values))
    results = []
    prices = defaultdict(list)
    changes = defaultdict(list)

    for index, n in enumerate(numbers):
        prev_price = 0
        r = n
        for jindex in range(2000):
            r = calc_secret_number(r)
            price = r % 10
            change = price - prev_price
            prices[index].append(price)
            changes[index].append(change)
            prev_price = price
            if jindex < 10:
                log.debug(f"{r:10d}: {price} ({change})")

        results.append(r)

    # for index in prices.keys():
    #     prices[index].pop(0)

    sequences = defaultdict(dict)
    sequences_counter = defaultdict(lambda: 0)
    sequences_counter_best = defaultdict(lambda: defaultdict(list))
    for index in prices.keys():
        for jindex in range(3, 2000):
            sequence_id = f"{changes[index][jindex-3]},{changes[index][jindex-2]},{changes[index][jindex-1]},{changes[index][jindex]},"
            price = prices[index][jindex]
            sequences[index][sequence_id] = price
            sequences_counter_best[index][sequence_id].append(price)
    for key, value in sequences.items():
        log.debug(f"sequences for index {key}")
        log.debug(value)

    first_sequence_count = defaultdict(dict)
    for index in prices.keys():
        sequence_keys = sequences_counter_best[index].keys()
        for sequence_key in sequence_keys:
            first_sequence_count[index][sequence_key] = sequences_counter_best[index][
                sequence_key
            ][0]

    for index, values in first_sequence_count.items():
        log.debug(f"index {index}")
        log.debug(f"index {values}")
        for key, value in values.items():
            sequences_counter[key] += value

    for key, value in sequences_counter.items():
        logger.debug(f"{key}: {value}")

    most_bannanas = max(sequences_counter.values())
    result = most_bannanas
    print(result)
    return f"{result}"

    # for index, values in prices.items():
    #     for a, b, c, d in sliding_window(values, 4):
    #         sequences[index][f"{a},{b},{c},{d}"] = d
    # print(sequences)

    print(results)
    print(sum(results))
    return f"{sum(results)}"
