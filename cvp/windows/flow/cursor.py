# -*- coding: utf-8 -*-

from typing import Dict, Optional
from weakref import ReferenceType, ref

from cvp.config.sections.flow import FlowAuiConfig
from cvp.flow.datas.graph import Graph
from cvp.imgui.fonts.mapper import FontMapper
from cvp.logging.logging import flow_logger as logger
from cvp.widgets.canvas.graph import CanvasGraph


class FlowCursor:
    _canvases: Dict[str, CanvasGraph]
    _ref: Optional[ReferenceType[Graph]]

    def __init__(self, fonts: FontMapper, config: FlowAuiConfig):
        self._fonts = fonts
        self._config = config
        self._canvases = dict()
        self._ref = None

    def _create_canvas(self, graph: Graph) -> CanvasGraph:
        canvas = CanvasGraph(graph, self._fonts, self._config)
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
    def graph(self) -> Optional[Graph]:
        if self._ref is None:
            return None
        return self._ref()

    @property
    def opened(self) -> bool:
        if self._ref is None:
            return False
        return self._ref() is not None

    def open(self, graph: Graph) -> None:
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
