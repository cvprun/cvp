# -*- coding: utf-8 -*-

from typing import Any, Dict

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName


class ReadCsvNode(Node):
    """Read a CSV file into a DataFrame."""

    def __init__(self):
        self._filepath_pin = DataInputPin(
            name=PinName("filepath_or_buffer"),
            dtype=Dtype.any(),
            docs="File path or buffer to read from",
        )
        self._sep_pin = DataInputPin(
            name=PinName("sep"),
            dtype=Dtype.any(),
            docs="Delimiter to use (default: ',')",
            required=False,
        )
        self._header_pin = DataInputPin(
            name=PinName("header"),
            dtype=Dtype.any(),
            docs="Row number(s) to use as column names (default: 'infer')",
            required=False,
        )
        self._index_col_pin = DataInputPin(
            name=PinName("index_col"),
            dtype=Dtype.any(),
            docs="Column(s) to set as index (optional)",
            required=False,
        )
        self._output = DataOutputPin(
            name=PinName("dataframe"),
            dtype=Dtype.any(),
            docs="DataFrame read from CSV",
        )
        super().__init__(
            self._filepath_pin,
            self._sep_pin,
            self._header_pin,
            self._index_col_pin,
            self._output,
        )

    def run(self, record: NodeRecord) -> Pin:
        filepath = record.get(self._filepath_pin)

        kwargs: Dict[str, Any] = {"filepath_or_buffer": filepath}

        try:
            sep = record.get(self._sep_pin)
            if sep is not None:
                kwargs["sep"] = sep
        except KeyError:
            pass

        try:
            header = record.get(self._header_pin)
            if header is not None:
                kwargs["header"] = header
        except KeyError:
            pass

        try:
            index_col = record.get(self._index_col_pin)
            if index_col is not None:
                kwargs["index_col"] = index_col
        except KeyError:
            pass

        df = pd.read_csv(**kwargs)
        record.set(self._output, df)
        return self.nonext()
