# -*- coding: utf-8 -*-

from cvp.context.mixins._base import BaseContextMixin
from cvp.flow.graph import GraphKey


class FlowMixins(BaseContextMixin):
    @property
    def selected_graph_key(self) -> GraphKey:
        return GraphKey(self._config.flow.selected_uuid)

    @selected_graph_key.setter
    def selected_graph_key(self, value: GraphKey) -> None:
        self._config.flow.selected_uuid = str(value)

    @property
    def selected_graph(self):
        return self._flows.graphs.get(self.selected_graph_key)
