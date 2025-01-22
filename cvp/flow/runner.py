# -*- coding: utf-8 -*-

from collections import deque
from concurrent.futures import Executor
from copy import deepcopy
from enum import IntEnum, auto, unique
from logging import Logger
from threading import Lock
from typing import Deque, NamedTuple, Optional, Union

from cvp.flow.graph import FlowGraph
from cvp.flow.node import FlowNode
from cvp.flow.node_pin import FlowNodePin
from cvp.flow.pin import FlowPin
from cvp.flow.store import VariableStore
from cvp.logging.logging import flow_logger
from cvp.nodes.node import Node
from cvp.nodes.record import NodeExecutionRecord
from cvp.pins.special import EntrypointPin
from cvp.variables import FLOW_PATH_SEPARATOR


@unique
class FlowRunnerStep(IntEnum):
    done = auto()
    running = auto()


class FlowRunnerState(NamedTuple):
    step: FlowRunnerStep

    def __str__(self):
        return f"step={self.step}"


class FlowRunner:
    _exception: Optional[BaseException]
    _records: Deque[NodeExecutionRecord]

    def __init__(
        self,
        executor: Executor,
        graph: FlowGraph,
        start_node: Union[FlowNode, str],
        memory: Optional[VariableStore] = None,
        *,
        logger: Optional[Logger] = None,
        use_copy=False,
        use_deepcopy=False,
        use_graph_lock=False,
    ):
        if use_copy and use_deepcopy:
            raise ValueError("use_copy and use_deepcopy cannot coexist.")

        for node in graph.nodes:
            if node.template is None:
                raise ValueError(f"invalid node template: '{node.name}'")

            for pin in node.pins:
                if pin.template is None:
                    pin_path = node.name + FLOW_PATH_SEPARATOR + pin.name
                    raise ValueError(f"Invalid pin template: '{pin_path}'")

        if isinstance(start_node, FlowNode):
            if start_node != graph.find_begin_node(start_node.uuid):
                raise KeyError(f"The graph has no starting node: '{start_node.uuid}'")
        elif isinstance(start_node, str):
            temp_start_node = graph.find_begin_node(start_node)
            if temp_start_node is None:
                raise KeyError(f"Not found begin node: '{start_node}'")
            start_node = temp_start_node
        else:
            raise TypeError(f"Invalid node type: '{type(start_node).__name__}'")

        assert isinstance(start_node, FlowNode)
        self._start_node = start_node
        self._entrypoint = FlowPin.from_template(EntrypointPin())
        self._graph = graph
        self._logger = logger if logger else flow_logger
        self._use_copy = use_copy
        self._use_deepcopy = use_deepcopy
        self._use_graph_lock = use_graph_lock

        self._step = FlowRunnerStep.done
        self._records = deque()
        self._exception = None
        self._memory = VariableStore.from_other(
            other=memory,
            use_copy=use_copy,
            use_deepcopy=use_deepcopy,
        )

        self._lock = Lock()
        self._future = executor.submit(self._runner)

    @property
    def future(self):
        return self._future

    @property
    def state(self):
        with self._lock:
            return FlowRunnerState(FlowRunnerStep(self._step))

    def create_record(self, node_template: Node, node_uuid: str) -> NodeExecutionRecord:
        with self._lock:
            return self._memory.create_node_execution_record(
                node_template,
                node_uuid,
                use_copy=self._use_copy,
                use_deepcopy=self._use_deepcopy,
            )

    def append_record(self, record: NodeExecutionRecord) -> None:
        with self._lock:
            self._records.append(record)

    def get_start_cursor(self) -> Optional[FlowNodePin]:
        with self._lock:
            return FlowNodePin(self._start_node, self._entrypoint)

    @property
    def exception(self) -> Optional[BaseException]:
        with self._lock:
            return deepcopy(self._exception)

    def _runner(self):
        self._logger.info(f"{type(self).__name__} start")
        with self._lock:
            self._step = FlowRunnerStep.running
            graph_lock = self._use_graph_lock
            prev_lock = self._graph.lock
            if graph_lock:
                self._graph.lock = True

        cursor = self.get_start_cursor()
        try:
            while cursor is not None:
                cursor = self._execute_node(cursor)
        except BaseException as e:
            self._logger.error(e)
            with self._lock:
                self._exception = e
        finally:
            self._logger.info(f"{type(self).__name__} done")
            with self._lock:
                self._step = FlowRunnerStep.done
                if graph_lock:
                    self._graph.lock = prev_lock
                return self._records.copy()

    def _execute_node(self, np: FlowNodePin) -> Optional[FlowNodePin]:
        node_template = np.node.template
        pin_template = np.pin.template
        assert node_template is not None
        assert pin_template is not None

        record = self.create_record(node_template, np.node.uuid)
        try:
            next_pin_template = node_template.run(pin_template, record)
        finally:
            self.append_record(record)

        if next_pin_template is None:
            return None  # There is no next flow.

        next_pin = np.node.find_pin(next_pin_template.name)
        if next_pin is None:
            raise IndexError(f"Not found next pin: '{next_pin_template.name}'")

        if not next_pin.arcs:
            return None  # The arc is not connected.

        if 2 <= len(next_pin.arcs):
            raise ValueError("Only one output arc is allowed")

        arc_uuid = next_pin.arcs[0]
        arc = self._graph.find_arc(arc_uuid)
        if arc is None:
            raise IndexError(f"Not found arc: '{arc_uuid}'")

        assert arc.output is not None
        assert next_pin.name == arc.output.pin.name

        input_node_uuid = arc.input.node.uuid
        input_node = self._graph.find_node(input_node_uuid)
        if input_node is None:
            raise IndexError(f"Not found input node: '{input_node_uuid}'")

        input_pin = input_node.find_pin(arc.input.pin.name)
        if input_pin is None:
            raise IndexError("Not found input pin")

        assert input_node is not None
        assert input_pin is not None
        return FlowNodePin(input_node, input_pin)
