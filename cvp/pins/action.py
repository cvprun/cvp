# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class Action(StrEnum):
    flow = auto()
    """
    Execution pins are used to connect nodes together to create a flow of execution.
    """

    data = auto()
    """
    Data pins are used for taking data into a node or outputting data from a node.
    """
