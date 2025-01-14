# -*- coding: utf-8 -*-

from cvp.flow.components.graph import Graph


class FlowRunner:
    def __init__(self, graph: Graph):
        self._graph = graph
        self._nodes = {node.uuid: node for node in graph.nodes}
        self._arcs = {arc.uuid: arc for arc in graph.arcs}

    def run(self):
        pass

    def stop(self):
        pass

    def resume(self):
        pass

    def pause(self):
        pass

    def step_over(self):
        pass

    def step_into(self):
        pass

    def step_out(self):
        pass
