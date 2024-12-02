from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
import numpy as np

logger = structlog.get_logger()


def part2(values_list) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    result = 0
    for values in values_list:
        structlog.contextvars.bind_contextvars(
            iteration=values,
        )
        # line = np.array(values.split(), dtype=np.int32)
        # logger.debug(f"line: {line}")
        #
        # diff = np.diff(line)
        # logger.debug(f"diff: {diff}")
        # total = len(line) - 1
        # n_greater_than_3 = sum(np.abs(diff) > 3)
        # errors = n_greater_than_3
        # n_positive = sum(diff > 0)
        # n_negative = sum(diff < 0)
        # if n_positive >= total - 1:
        #     errors += total - n_positive
        # elif n_negative >= total - 1:
        #     errors += total - n_negative
        # else:
        #     errors += 500
        #
        # n_constant = sum(diff == 0)
        # if n_constant <= 1:
        #     errors += n_constant
        # else:
        #     errors += 1000
        # logger.debug(
        #     f"n_greater_than_3: {n_greater_than_3}, n_positive: {n_positive}, n_negative: {n_negative}, n_constant:{n_constant} errors: {errors}"
        # )
        # if errors <= 1:
        #     result.append(True)
        # line = np.array(values.split(), dtype=np.int32)

        # def analyze(line):
        #     logger.debug(f"line: {line}")
        #     diff = np.diff(line)
        #     total = len(diff)
        #     logger.debug(f"diff: {diff}")
        #     no_greater_than_3 = np.abs(diff) <= 3
        #     if sum(no_greater_than_3) != total:
        #         logger.debug(f"some greater than 3 {sum(no_greater_than_3)} != {total}")
        #         logger.debug(f"no_greater_than_3: {no_greater_than_3}")
        #         return np.where(no_greater_than_3 == False)[0][0]
        #     all_positive = diff > 0
        #     all_negative = diff < 0
        #     is_monotonic = sum(all_positive) == total or sum(all_negative) == total
        #     if not is_monotonic:
        #         logger.debug("not monotonic")
        #         if sum(all_negative) > sum(all_positive):  # should have been negative
        #             logger.debug(
        #                 f"should be negative: {np.where(all_negative == False)}"
        #             )
        #             return int(np.where(all_negative == False)[0][0]) + 1
        #         else:
        #             logger.debug(
        #                 f"should be positive: {np.where(all_positive == False)}"
        #             )
        #             return int(np.where(all_positive == False)[0][0])
        #     any_constant = np.any(diff == 0)
        #     if any_constant:
        #         logger.debug("some constant")
        #         return np.where(diff == 0)[0][0] + 1
        #
        #     logger.debug(
        #         f"no_greater_than_3: {no_greater_than_3}, is_monotonic: {is_monotonic}, not any_constant: {not any_constant}"
        #     )
        #     if sum(no_greater_than_3) == total and is_monotonic and not any_constant:
        #         logger.debug("SUCCESSSS")
        #         return True
        #
        # current = analyze(line)
        # if type(current) is not type(True):
        #     logger.debug(f"gonna pop {current}")
        #     logger.debug(f"{line}")
        #     logger.debug(" " * 3 * int(current) + "^")
        #     line = np.delete(line, current)
        #     current = analyze(line)
        # logger.debug(f"current: {current}")
        # if current is True:
        #     result.append(True)
        # else:
        #     logger.debug("FAIL")
        line = np.array(values.split(), dtype=np.int32)

        def analyse(line):
            logger.debug(f"line: {line}")
            diff = np.diff(line)
            logger.debug(f"diff: {diff}")
            no_greater_than_3 = np.all(np.abs(diff) <= 3)
            all_positive = np.all(diff > 0)
            all_negative = np.all(diff < 0)
            any_constant = np.any(diff == 0)
            is_monotonic = all_positive | all_negative
            logger.debug(
                f"no_greater_than_3: {no_greater_than_3}, is_monotonic: {is_monotonic}, not any_constant: {not any_constant}"
            )
            if no_greater_than_3 and is_monotonic and not any_constant:
                return True

        if analyse(line):
            result += 1
        else:
            for i in range(len(line)):
                new_line = np.delete(line, i)
                if analyse(new_line):
                    result += 1
                    break

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    logger.debug(f"result: {result}")
    return str(result)
