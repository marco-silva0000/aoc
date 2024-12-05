from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from collections import defaultdict

logger = structlog.get_logger()


def part2(values_list) -> str:
    from structlog import get_logger

    log = get_logger()
    log.debug("part2")
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
        seen_pages = set()
        for page in pages:
            cant_be_in_seen = rules[page]
            if intersection := cant_be_in_seen.intersection(seen_pages):
                return page, intersection
            seen_pages.add(page)
        return True

    ordered_lists = []
    unordered_lists = []
    for l in print_lists:
        if is_list_ordered(l, page_rules) is True:
            ordered_lists.append(l)
        else:
            unordered_lists.append(l)

    print(unordered_lists)
    reordered = []
    for l in unordered_lists:
        log = log.bind(og_l=l)
        unordered = l
        while (page_intersection := is_list_ordered(unordered, page_rules)) is not True:
            log.debug("wasn't ordered")
            wrong_page, intersection = page_intersection
            log = log.bind(wrong_page=wrong_page, intersection=intersection)
            new_page_order = unordered
            index_of_wrong_page = new_page_order.index(wrong_page)
            min_index = min([new_page_order.index(p) for p in intersection])
            log = log.bind(wrong_index=index_of_wrong_page, min_index=min_index)
            new_page_order.pop(index_of_wrong_page)
            new_page_order.insert(min_index, wrong_page)
            unordered = new_page_order
            log.debug(f"new unordered: {unordered}")
        log.debug(f"now ordered: {unordered}")
        reordered.append(unordered)

    result = 0
    print(reordered)
    for l in reordered:
        result += int(l[len(l) // 2])

    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    return f"{result}"
