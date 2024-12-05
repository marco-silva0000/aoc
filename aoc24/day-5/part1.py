from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from collections import defaultdict

logger = structlog.get_logger()


def part1(values_list) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    result = []
    first_bit = True
    page_rules = defaultdict(set)
    print_lists = []
    for values in values_list:
        print(values)
        if not values:
            first_bit = False
            continue
        if first_bit:
            first_page, second_page = values.split("|")
            page_rules[first_page].add(second_page)
        else:
            print_lists.append(values.split(","))
    print(page_rules)

    def is_list_ordered(pages, rules):
        print("pages_being_tested:")
        print(pages)
        seen_pages = set()
        for page in pages:
            print("seen_pages", seen_pages)
            cant_be_in_seen = rules[page]
            print("cant_be_in_seen", cant_be_in_seen)
            print("intersection", cant_be_in_seen.intersection(seen_pages))
            print("intersection_bool", bool(cant_be_in_seen.intersection(seen_pages)))
            if cant_be_in_seen.intersection(seen_pages):
                return False
            seen_pages.add(page)
        return True

    ordered_lists = []
    for l in print_lists:
        if is_list_ordered(l, page_rules):
            ordered_lists.append(l)

    result = 0
    print(print_lists)
    for l in ordered_lists:
        result += int(l[len(l) // 2])

    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    print(result)
    print(result)
    print(result)
    return f"{result}"
