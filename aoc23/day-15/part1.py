from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle

logger = structlog.get_logger()


class Hashy(str):
    def __hash__(self):
        """
        Determine the ASCII code for the current character of the string.
        Increase the current value by the ASCII code you just determined.
        Set the current value to itself multiplied by 17.
        Set the current value to the remainder of dividing itself by 256.

        """
        from structlog import get_logger

        logger = get_logger()
        logger.bind(str=self)
        current_value = 0
        for c in self:
            char_value = ord(c)
            current_value += char_value
            current_value *= 17
            current_value %= 256
        return current_value


def part1(values_list) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    values_list = values_list[0]
    result = sum([hash(Hashy(s)) for s in values_list.strip().split(",")])

    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    print(result)
    return str(result)
