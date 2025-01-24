# -*- coding: utf-8 -*-

from typing import Dict, Optional
from weakref import ReferenceType, ref

from cvp.flow.graph import FlowGraph
from cvp.logging.logging import flow_logger as logger
from cvp.renderer.context import RendererContext
from cvp.widgets.canvas.graph import CanvasGraph


class Canvases:
    _canvases: Dict[str, CanvasGraph]
    _ref: Optional[ReferenceType[FlowGraph]]

    def __init__(self, context: RendererContext):
        self._context = context
        self._canvases = dict()
        self._ref = None

    def _create_canvas(self, graph: FlowGraph) -> CanvasGraph:
        canvas = CanvasGraph(graph, self._context.fonts, self._context.config.flow_aui)
        self._canvases[graph.uuid] = canvas
        return canvas

    def clear(self) -> None:
        self._canvases.clear()

    @property
    def canvas(self) -> Optional[CanvasGraph]:
        if self._ref is None:
            return None

        graph = self._ref()
        if graph is None:
            return None

        if canvas := self._canvases.get(graph.uuid):
            return canvas

        return self._create_canvas(graph)

    @property
    def graph(self) -> Optional[FlowGraph]:
        if self._ref is None:
            return None
        return self._ref()

    @property
    def opened(self) -> bool:
        if self._ref is None:
            return False
        return self._ref() is not None

    def open(self, graph: FlowGraph) -> None:
        if self._ref is not None:
            prev_graph = self._ref()
            if prev_graph is not None:
                if prev_graph.uuid in self._canvases:
                    self._canvases.pop(prev_graph.uuid)

        self._ref = ref(graph)
        if graph.uuid in self._canvases:
            self._canvases.pop(graph.uuid)
        self._create_canvas(graph)
        logger.info("The graph has been opened")

    def close(self) -> None:
        if self._ref is None:
            return
        graph = self._ref()
        if graph is not None:
            if graph.uuid in self._canvases:
                self._canvases.pop(graph.uuid)
        self._ref = None
        logger.info("The graph has been closed")
