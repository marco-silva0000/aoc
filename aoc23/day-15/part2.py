from typing import List, Set, Dict, Tuple, Optional, Union
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum

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


@dataclass()
class Lens:
    focal_val: int
    label: str

    def __str__(self):
        return f"{self.label} {self.focal_val}"

    def __repr__(self) -> str:
        return f"{self.label} {self.focal_val}"


@dataclass()
class Box:
    lenses: List[Lens]
    label: int

    def find_lens_index(self, label: str) -> int:
        # return map(lambda lens: lens.label == label, self.lenses).index(True)
        for i, lens in enumerate(self.lenses):
            if lens.label == label:
                return i

    def __str__(self):
        return f"Box {self.label}: {self.lenses}"

    @property
    def power(self):
        box_power = self.label + 1
        lens_power = 0
        for i, lens in enumerate(self.lenses):
            lens_power += (i + 1) * lens.focal_val
        return box_power * lens_power


class Operation(Enum):
    REMOVE = "-"
    FOCUS = "="


def part2(values_list) -> str:
    from structlog import get_logger

    logger = get_logger()
    logger.debug("part")
    values_list = values_list[0]
    mappy = {}
    for step in values_list.strip().split(","):
        logger = logger.bind(step=step)
        if "-" in step:
            operation = Operation.REMOVE
            label = step[:-1]
        else:
            operation = Operation.FOCUS
            label, focus_val = step.split("=")
            logger = logger.bind(focus_val=focus_val)
        logger = logger.bind(operation=operation, label=label)

        box_id = hash(Hashy(label))
        logger.debug(box_id)
        try:
            box = mappy[box_id]
        except KeyError:
            box = Box([], box_id)
        logger.debug(box)
        lens_index = box.find_lens_index(label)
        logger = logger.bind(lens_index=lens_index)
        match operation:
            case Operation.REMOVE:
                logger.debug("remove")
                if lens_index is not None:
                    box.lenses.pop(lens_index)
                    mappy[box_id] = box
            case Operation.FOCUS:
                logger.debug("focus")
                v = int(focus_val)
                lens = Lens(v, label)
                if lens_index is not None:
                    box.lenses[lens_index] = lens
                else:
                    box.lenses.append(lens)
                mappy[box_id] = box

        print(f"After '{step}':")
        for box in mappy.values():
            print(box)
        # print(mappy.values())

    for box in mappy.values():
        print(box)
        print(box.power)
        print()
    result = sum([box.power for box in mappy.values()])

    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
    print(result)
    return str(result)
