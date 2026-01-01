# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .read_csv_node import ReadCsvNode
from .read_json_node import ReadJsonNode
from .to_csv_node import ToCsvNode


def get_io_nodes() -> List[Node]:
    """Get all I/O pandas nodes."""
    return [
        ReadCsvNode(),
        ReadJsonNode(),
        ToCsvNode(),
    ]
