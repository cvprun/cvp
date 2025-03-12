# -*- coding: utf-8 -*-

from collections import deque
from concurrent.futures import Executor, Future
from dataclasses import dataclass
from enum import IntEnum, auto, unique
from logging import Logger
from sys import exc_info
from threading import Condition, Lock
from typing import Deque, Dict, Final, NamedTuple, Optional, Union

from cvp.flow.graph import FlowGraph
from cvp.flow.memory import FlowMemory
from cvp.flow.node import FlowNode
from cvp.flow.node_pin import FlowNodePin
from cvp.flow.pin import FlowPin
from cvp.logging.logging import flow_logger
from cvp.memory.copy import copy_flexible
from cvp.nodes.record import NodeRecord
from cvp.nodes.registry.registry import NodeRegistry
from cvp.nodes.template import NodeTemplate
from cvp.pins.special import EntrypointPinTemplate
from cvp.pins.template import PinTemplate

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
    nodes: Dict[str, NodeTemplate]
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
        return self.graph.key

    @property
    def start_cursor(self) -> Optional[FlowNodePin]:
        """The Optional return value is to automatically infer the type of 'cursor'."""
        return FlowNodePin(self.start_node, self.entrypoint)


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
            entrypoint=FlowPin.from_template(EntrypointPinTemplate()),
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

    def __repr__(self):
        return self._future.__repr__()

    def cancel(self):
        return self._future.cancel()

    def cancelled(self):
        return self._future.cancelled()

    def running(self):
        return self._future.running()

    def done(self):
        return self._future.done()

    def add_done_callback(self, fn):
        return self._future.add_done_callback(fn)

    def result(self, timeout=None):
        return self._future.result(timeout)

    def exception(self, timeout=None):
        return self._future.exception(timeout)

    def set_running_or_notify_cancel(self) -> None:
        self._future.set_running_or_notify_cancel()

    def set_result(self, result: Deque[NodeRecord]) -> None:
        self._future.set_result(result)

    def set_exception(self, exception: BaseException) -> None:
        self._future.set_exception(exception)

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
        args.logger.info("Running ...")

        with self._lock:
            self._step = FlowRunnerStep.running

        try:
            index = 0
            next_np = args.start_cursor
            while next_np is not None:
                data_nps = args.graph.retrieve_data_node_execution_order(next_np.node)
                for data_np in data_nps:
                    self._execute_node(
                        index=index,
                        graph=args.graph,
                        np=data_np,
                        node=args.nodes[data_np.node.path],
                        use_copy=args.use_copy,
                        use_deepcopy=args.use_deepcopy,
                        logger=args.logger,
                    )
                    index += 1

                next_np = self._execute_node(
                    index=index,
                    graph=args.graph,
                    np=next_np,
                    node=args.nodes[next_np.node.path],
                    use_copy=args.use_copy,
                    use_deepcopy=args.use_deepcopy,
                    logger=args.logger,
                )
                index += 1
        except BaseException as e:
            if args.debug and 1 <= args.verbose:
                args.logger.exception(e)
            else:
                args.logger.error(e)
            raise
        finally:
            args.logger.info("Done!")
            with self._lock:
                self._step = FlowRunnerStep.done
                return self._records.copy()

    def _execute_node(
        self,
        index: int,
        graph: FlowGraph,
        np: FlowNodePin,
        node: NodeTemplate,
        *,
        use_copy=False,
        use_deepcopy=False,
        logger: Optional[Logger] = None,
    ) -> Optional[FlowNodePin]:
        prefix = f"{index}. [{str(np)}]" if logger is not None else str()

        if np.node.breakpoint:
            if logger is not None:
                logger.debug(f"{prefix} Pause if running ...")
            self._pause_if_running()
            if logger is not None:
                logger.debug(f"{prefix} Pause if running done")

        if logger is not None:
            logger.debug(f"{prefix} Wait for next step ...")
        self._wait_for_next_step()
        if logger is not None:
            logger.debug(f"{prefix} Wait for next step done")

        try:
            if logger is not None:
                logger.debug(f"{prefix} Start")
            return self.__execute_node_main(
                index=index,
                graph=graph,
                np=np,
                node=node,
                use_copy=use_copy,
                use_deepcopy=use_deepcopy,
            )
        finally:
            if logger is not None:
                logger.debug(f"{prefix} End")

    def __execute_node_main(
        self,
        index: int,
        graph: FlowGraph,
        np: FlowNodePin,
        node: NodeTemplate,
        *,
        use_copy=False,
        use_deepcopy=False,
    ) -> Optional[FlowNodePin]:
        record = self.create_record(
            index=index,
            node=np.node,
            pin=np.pin,
            use_copy=use_copy,
            use_deepcopy=use_deepcopy,
        )

        result_pin: Union[None, PinTemplate, str] = None

        try:
            result_pin = node.run(record)
        except:  # noqa
            record.exception = exc_info()
        finally:
            self.update_result_record(record)
            if record.has_exception:
                raise record.exc_val.with_traceback(record.exc_tb)

        if result_pin is None:
            return None  # There is no next flow.

        if isinstance(result_pin, PinTemplate):
            next_pin_name = str(result_pin.name)
        elif isinstance(result_pin, str):
            next_pin_name = result_pin
        else:
            raise TypeError(f"Unsupported pin type: {type(result_pin).__name__}")

        next_pin = np.node.find_pin(next_pin_name)
        if next_pin is None:
            raise IndexError(f"Not found next pin: '{next_pin_name}'")

        if not next_pin.wires:
            return None  # The wire is not connected.

        if 2 <= len(next_pin.wires):
            raise ValueError("Only one output wire is allowed")

        wire_uuid = next_pin.wires[0]
        wire = graph.wires.get(wire_uuid)
        if wire is None:
            raise IndexError(f"Not found wire: '{wire_uuid}'")

        assert wire.output is not None
        assert next_pin.name == wire.output.pin.name

        input_node_uuid = wire.input.node.uuid
        input_node = graph.find_node(input_node_uuid)
        if input_node is None:
            raise IndexError(f"Not found input node: '{input_node_uuid}'")

        input_pin = input_node.find_pin(wire.input.pin.name)
        if input_pin is None:
            raise IndexError("Not found input pin")

        assert input_node is not None
        assert input_pin is not None
        return FlowNodePin(input_node, input_pin)
