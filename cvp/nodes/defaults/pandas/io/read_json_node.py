# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName


class ReadJsonNode(Node):
    """Read a JSON file into a DataFrame."""

    def __init__(self):
        self._path_pin = DataInputPin(
            name=PinName("path_or_buf"),
            dtype=Dtype.any(),
            docs="File path or buffer to read from",
        )
        self._orient_pin = DataInputPin(
            name=PinName("orient"),
            dtype=Dtype.any(),
            docs="Expected JSON string format (optional)",
            required=False,
        )
        self._output = DataOutputPin(
            name=PinName("dataframe"),
            dtype=Dtype.any(),
            docs="DataFrame read from JSON",
        )
        super().__init__(self._path_pin, self._orient_pin, self._output)

    def run(self, record: NodeRecord) -> Pin:
        path = record.get(self._path_pin)

        kwargs: Dict[str, Any] = {"path_or_buf": path}

        try:
            orient = record.get(self._orient_pin)
            if orient is not None:
                kwargs["orient"] = orient
        except KeyError:
            pass

        df = pd.read_json(**kwargs)
        record.set(self._output, df)
        return self.nonext()
