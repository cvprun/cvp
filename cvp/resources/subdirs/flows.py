# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.resources.formats.yaml import YamlFormatPath
from cvp.variables import FLOW_GRAPHS_DIRNAME


class FlowsPath(YamlFormatPath):
    def __init__(
        self,
        *path: Union[str, PathLike[str]],
        graphs_dirname=FLOW_GRAPHS_DIRNAME,
    ):
        super().__init__(*path)
        self._graphs_dirname = graphs_dirname

    def get_graph_filepath(self, key: str):
        return self.make_object_path(self._graphs_dirname, key)
