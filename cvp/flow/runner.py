# -*- coding: utf-8 -*-

from collections import deque
from concurrent.futures import Executor, Future
from dataclasses import dataclass
from enum import IntEnum, auto, unique
from logging import Logger
from threading import Condition, Lock
from typing import Deque, Dict, Final, NamedTuple, Optional, Union

from cvp.flow.graph import FlowGraph
from cvp.flow.memory import FlowMemory
from cvp.flow.node import FlowNode
from cvp.flow.node_pin import FlowNodePin
from cvp.flow.pin import FlowPin
from cvp.logging.logging import flow_logger
from cvp.memory.copy import copy_flexible
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.nodes.registry.registry import NodeRegistry
from cvp.pins.special import EntrypointPin

INFINITY_COUNTER: Final[int] = -1
STOP_COUNTER: Final[int] = -2


@unique
class FlowRunnerStep(IntEnum):
    done = auto()
    running = auto()
    waiting = auto()


class FlowRunnerState(NamedTuple):
    step: FlowRunnerStep

    def __str__(self):
        return f"<{type(self).__name__} step={self.step}>"


@dataclass
class _FlowRunnerArguments:
    """
    Do not use locks. <- Why ?? - TODO: Comment this section
    """

    nodes: Dict[str, Node]
    graph: FlowGraph
    start_node: FlowNode
    entrypoint: FlowPin
    logger: Logger
    use_copy: bool
    use_deepcopy: bool
    debug: bool
    verbose: int

    @property
    def graph_name(self):
        return self.graph.name

    @property
    def graph_uuid(self):
        return self.graph.uuid

    @property
    def logger_prefix(self) -> str:
        return f"<{FlowRunner.__name__} {self.graph_name}({self.graph_uuid})>"

    @property
    def start_cursor(self) -> Optional[FlowNodePin]:
        """The Optional return value is to automatically infer the type of 'cursor'."""
        return FlowNodePin(self.start_node, self.entrypoint)

    def exception_logging(self, e: BaseException) -> None:
        self.logger.exception(e)

    def error_logging(self, message: str) -> None:
        self.logger.error(f"{self.logger_prefix} {message}")

    def warning_logging(self, message: str) -> None:
        self.logger.warning(f"{self.logger_prefix} {message}")

    def info_logging(self, message: str) -> None:
        self.logger.info(f"{self.logger_prefix} {message}")

    def debug_logging(self, message: str) -> None:
        self.logger.debug(f"{self.logger_prefix} {message}")


class FlowRunner:
    _records: Deque[NodeRecord]
    _future: Future[Deque[NodeRecord]]

    def __init__(
        self,
        executor: Executor,
        node_registry: NodeRegistry,
        graph: FlowGraph,
        start_node: Union[FlowNode, str],
        *,
        logger: Optional[Logger] = None,
        use_copy=False,
        use_deepcopy=False,
        debug=False,
        verbose=0,
    ):
        if use_copy and use_deepcopy:
            raise ValueError("use_copy and use_deepcopy cannot coexist")

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

        registered_nodes = dict()
        for node in graph.nodes:
            if node.path in registered_nodes:
                continue
            registered_nodes[node.path] = copy_flexible(
                node_registry.get(node.path),
                use_copy=use_copy,
                use_deepcopy=use_deepcopy,
            )

        self._lock = Lock()
        self._counter = INFINITY_COUNTER
        self._condition = Condition(self._lock)
        self._step = FlowRunnerStep.done
        self._records = deque()
        self._memory = FlowMemory.from_graph(graph)

        arguments = _FlowRunnerArguments(
            nodes=registered_nodes,
            start_node=start_node,
            entrypoint=FlowPin.from_template(EntrypointPin()),
            graph=graph,
            logger=logger if logger else flow_logger,
            use_copy=use_copy,
            use_deepcopy=use_deepcopy,
            debug=debug,
            verbose=verbose,
        )

        # [IMPORTANT]
        # After initializing the variables, you must do 'submit' at the end.
        self._future = executor.submit(self._runner, arguments)

    @property
    def future(self):
        return self._future

    @property
    def state(self):
        with self._lock:
            return FlowRunnerState(FlowRunnerStep(self._step))

    def create_record(
        self,
        index: int,
        node: FlowNode,
        pin: FlowPin,
        *,
        use_copy=False,
        use_deepcopy=False,
    ):
        with self._lock:
            return self._memory.create_node_execution_record(
                index=index,
                node_uuid=node.uuid,
                pin_name=pin.name,
                data_pins=node.data_pins,
                use_copy=use_copy,
                use_deepcopy=use_deepcopy,
            )

    def update_result_record(self, record: NodeRecord) -> None:
        with self._lock:
            self._memory.update_with_node_execution_record(record)
            self._records.append(record)

    def stop(self) -> None:
        with self._condition:
            self._counter = STOP_COUNTER
            self._condition.notify_all()

    def pause(self) -> None:
        with self._condition:
            self._counter = 0

    def resume(self) -> None:
        with self._condition:
            self._counter = INFINITY_COUNTER
            self._condition.notify_all()

    def step(self, count=1) -> None:
        with self._condition:
            if self._counter <= INFINITY_COUNTER:
                self._counter = count
            elif 0 <= self._counter:
                self._counter += count
            self._condition.notify_all()

    def _pause_if_running(self) -> None:
        with self._condition:
            if self._counter == INFINITY_COUNTER:
                self._counter = 0

    def _wait_for_next_step(self) -> None:
        with self._condition:
            if 1 <= self._counter:
                self._counter -= 1
            elif self._counter == INFINITY_COUNTER:
                pass
            elif self._counter == STOP_COUNTER:
                raise InterruptedError("The STOP counter has been detected")

            if self._counter == 0:
                self._step = FlowRunnerStep.waiting
                try:
                    while self._counter == 0:
                        self._condition.wait()
                finally:
                    self._step = FlowRunnerStep.running

    def _runner(self, args: _FlowRunnerArguments):
        args.info_logging("Running ...")
        with self._lock:
            self._step = FlowRunnerStep.running

        index = 0
        prev_cursor = args.start_cursor
        next_cursor = prev_cursor

        try:
            while next_cursor is not None:
                prev_cursor = next_cursor
                args.info_logging(f"[{str(prev_cursor)}] Begin")

                if prev_cursor.node.breakpoint:
                    self._pause_if_running()

                self._wait_for_next_step()

                next_cursor = self._execute_flow_node(
                    index=index,
                    graph=args.graph,
                    np=prev_cursor,
                    node=args.nodes[prev_cursor.node.path],
                    use_copy=args.use_copy,
                    use_deepcopy=args.use_deepcopy,
                )

                index += 1
                args.info_logging(f"[{str(prev_cursor)}] End")
        except BaseException as e:
            if args.debug and 1 <= args.verbose:
                args.exception_logging(e)
            else:
                args.error_logging(f"An exception occurred in {str(prev_cursor)}: {e}")
            raise
        finally:
            args.info_logging("Done!")
            with self._lock:
                self._step = FlowRunnerStep.done
                return self._records.copy()

    # def _execute_data_node(
    #     self,
    #     index: int,
    #     graph: FlowGraph,
    #     np: FlowNodePin,
    #     node: Node,
    #     *,
    #     use_copy=False,
    #     use_deepcopy=False,
    # ) -> Optional[FlowNodePin]:
    #     assert np.node.any_flow
    #     assert np.pin.is_flow_inputs
    #
    #     for data_input in np.node.data_inputs:
    #         for arc_uuid in data_input.arcs:
    #             if arc := graph.find_arc(arc_uuid):
    #                 assert arc.output is not None
    #                 assert arc.output.node.uuid == np.node.uuid
    #                 assert arc.output.pin.name == data_input.name
    #
    #                 assert arc.input is not None
    #                 input_node = arc.input.node
    #                 input_pin = arc.input.pin

    def _execute_flow_node(
        self,
        index: int,
        graph: FlowGraph,
        np: FlowNodePin,
        node: Node,
        *,
        use_copy=False,
        use_deepcopy=False,
    ) -> Optional[FlowNodePin]:
        assert np.node.any_flow
        assert np.pin.is_flow_inputs

        record = self.create_record(
            index=index,
            node=np.node,
            pin=np.pin,
            use_copy=use_copy,
            use_deepcopy=use_deepcopy,
        )

        try:
            next_pin_name = node.run(record)
        finally:
            self.update_result_record(record)
            if record.has_exception:
                raise record.exc_val.with_traceback(record.exc_tb)

        if next_pin_name is None:
            return None  # There is no next flow.

        next_pin = np.node.find_pin(next_pin_name)
        if next_pin is None:
            raise IndexError(f"Not found next pin: '{next_pin_name}'")

        if not next_pin.arcs:
            return None  # The arc is not connected.

        if 2 <= len(next_pin.arcs):
            raise ValueError("Only one output arc is allowed")

        arc_uuid = next_pin.arcs[0]
        arc = graph.find_arc(arc_uuid)
        if arc is None:
            raise IndexError(f"Not found arc: '{arc_uuid}'")

        assert arc.output is not None
        assert next_pin.name == arc.output.pin.name

        input_node_uuid = arc.input.node.uuid
        input_node = graph.find_node(input_node_uuid)
        if input_node is None:
            raise IndexError(f"Not found input node: '{input_node_uuid}'")

        input_pin = input_node.find_pin(arc.input.pin.name)
        if input_pin is None:
            raise IndexError("Not found input pin")

        assert input_node is not None
        assert input_pin is not None
        return FlowNodePin(input_node, input_pin)
