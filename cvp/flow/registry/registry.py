# -*- coding: utf-8 -*-

from inspect import Parameter, signature
from typing import Any, Callable, Dict, List, Optional, Union

from cvp.flow.catalog.dtype.builtins import get_builtin_types
from cvp.flow.catalog.node.builtins import get_builtin_functions
from cvp.flow.components.action import Action
from cvp.flow.components.stream import Stream
from cvp.flow.icons.dtype import DTYPE_ICON_MAPPING
from cvp.flow.icons.node import NODE_ICON_MAPPING
from cvp.flow.templates.dtype import Dtype
from cvp.flow.templates.node import NodeTemplate
from cvp.flow.templates.pin import PinTemplate
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.variables import (
    FLOW_PATH_SEPARATOR,
    FLOW_PIN_NEXT_DOCS_DEFAULT,
    FLOW_PIN_NEXT_NAME_DEFAULT,
    FLOW_PIN_PREV_DOCS_DEFAULT,
    FLOW_PIN_PREV_NAME_DEFAULT,
    FLOW_PIN_RETURN_DOCS_DEFAULT,
    FLOW_PIN_RETURN_NAME_DEFAULT,
)


class FlowRegistry:
    _dtypes: Dict[str, Dtype]
    _type2dtypes: Dict[type, Dtype]
    _nodes: Dict[str, NodeTemplate]

    def __init__(self, *, no_builtins=False):
        self._dtypes = dict()
        self._type2dtypes = dict()
        self._nodes = dict()

        if not no_builtins:
            self.register_builtin_dtypes()
            self.register_builtin_nodes()

    def register_builtin_dtypes(self) -> None:
        for cls in get_builtin_types():
            self.add_new_type(cls)

    def register_builtin_nodes(self) -> None:
        for func in get_builtin_functions():
            self.add_new_callable(func)

    @property
    def dtypes(self):
        return self._dtypes

    @property
    def type2dtypes(self):
        return self._type2dtypes

    @property
    def nodes(self):
        return self._nodes

    def update(self, other: "FlowRegistry") -> None:
        self._dtypes.update(other.dtypes)
        self._type2dtypes.update(other.type2dtypes)
        self._nodes.update(other.nodes)

    def get_dtype(self, path: str) -> Dtype:
        return self._dtypes[path]

    def get_dtype_with_type(self, base: type) -> Dtype:
        return self._type2dtypes[base]

    def get_node(self, path: str) -> NodeTemplate:
        return self._nodes[path]

    def add_dtype(self, dtype: Dtype) -> None:
        if dtype.path in self._dtypes:
            raise KeyError(f"Duplicate dtype path: {dtype.path}")
        self._dtypes[dtype.path] = dtype
        self._type2dtypes[dtype.base] = dtype

    def add_node(self, node: NodeTemplate) -> None:
        if node.path in self._nodes:
            raise KeyError(f"Duplicate node path: {node.path}")
        self._nodes[node.path] = node

    def add(self, item: Union[Dtype, NodeTemplate]):
        if isinstance(item, Dtype):
            self.add_dtype(item)
        elif isinstance(item, NodeTemplate):
            self.add_node(item)
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    @staticmethod
    def create_dtype(
        base: type,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
    ) -> Dtype:
        if not isinstance(base, type):
            raise TypeError(f"Only types can be registered: {base}")

        base_name = name if name else base.__name__
        base_path = path if path else base.__module__ + FLOW_PATH_SEPARATOR + base_name
        base_docs = docs if docs else base.__doc__
        base_icon = icon if icon else DTYPE_ICON_MAPPING[base_name[0]]
        base_color = color if color else WHITE_RGBA

        if not base_name:
            raise ValueError("The 'name' attribute is required")
        if not base_path:
            raise ValueError("The 'path' attribute is required")

        return Dtype(
            name=base_name,
            path=base_path,
            base=base,
            docs=base_docs,
            icon=base_icon,
            color=base_color,
        )

    @staticmethod
    def create_prev_pin():
        return PinTemplate(
            name=FLOW_PIN_PREV_NAME_DEFAULT,
            dtype=None,
            docs=FLOW_PIN_PREV_DOCS_DEFAULT,
            action=Action.flow,
            stream=Stream.input,
            required=False,
        )

    @staticmethod
    def create_next_pin():
        return PinTemplate(
            name=FLOW_PIN_NEXT_NAME_DEFAULT,
            dtype=None,
            docs=FLOW_PIN_NEXT_DOCS_DEFAULT,
            action=Action.flow,
            stream=Stream.output,
            required=False,
        )

    def dtype_path(self, return_annotation) -> str:
        if return_annotation == Parameter.empty:
            if Any in self._type2dtypes:
                return self._type2dtypes[Any].path  # type: ignore[index]
            else:
                dtype = self.create_dtype(Any)  # type: ignore[arg-type]
                self.add_dtype(dtype)
                return dtype.path

        if return_annotation in self._type2dtypes:
            return self._type2dtypes[return_annotation].path

        dtype = self.create_dtype(return_annotation)
        self.add_dtype(dtype)
        return dtype.path

    def create_parameter_pin(self, parameter: Parameter) -> PinTemplate:
        dtype_path = self.dtype_path(parameter.annotation)

        match parameter.kind:
            case Parameter.POSITIONAL_ONLY:
                required = parameter.default == Parameter.empty
            case Parameter.POSITIONAL_OR_KEYWORD:
                required = parameter.default == Parameter.empty
            case Parameter.VAR_POSITIONAL:
                required = False
            case Parameter.KEYWORD_ONLY:
                required = parameter.default == Parameter.empty
            case Parameter.VAR_KEYWORD:
                required = False
            case _:
                raise ValueError(f"Unexpected parameter kind: {parameter.kind}")

        return PinTemplate(
            name=parameter.name,
            dtype=dtype_path,
            docs=str(),
            action=Action.data,
            stream=Stream.input,
            required=required,
        )

    def create_parameter_pins(self, parameters: List[Parameter]) -> List[PinTemplate]:
        return list(self.create_parameter_pin(param) for param in parameters)

    def create_return_annotation_pin(self, return_annotation):
        return PinTemplate(
            name=FLOW_PIN_RETURN_NAME_DEFAULT,
            dtype=self.dtype_path(return_annotation),
            docs=FLOW_PIN_RETURN_DOCS_DEFAULT,
            action=Action.data,
            stream=Stream.output,
            required=False,
        )

    def create_node(
        self,
        func: Callable,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
        flow_inputs: Optional[List[PinTemplate]] = None,
        flow_outputs: Optional[List[PinTemplate]] = None,
        data_inputs: Optional[List[PinTemplate]] = None,
        data_outputs: Optional[List[PinTemplate]] = None,
        tags: Optional[List[str]] = None,
    ) -> NodeTemplate:
        if not callable(func):
            raise TypeError(f"Only callables can be registered: {func}")

        base_name = name if name else func.__name__
        base_docs = docs if docs else func.__doc__
        base_icon = icon if icon else NODE_ICON_MAPPING[base_name[0]]
        base_color = color if color else WHITE_RGBA
        base_tags = list(tags if tags else list())

        if path:
            base_path = path
        elif hasattr(func, "__module__"):
            base_path = func.__module__ + FLOW_PATH_SEPARATOR + base_name
        else:
            raise ValueError("Could not find attribute '__module__' in callable")

        if not base_name:
            raise ValueError("The 'name' attribute is required")
        if not base_path:
            raise ValueError("The 'path' attribute is required")

        base_pins = list()

        if flow_inputs:
            for pin in flow_inputs:
                if not pin.is_flow_inputs:
                    raise ValueError("Pin must be flow inputs")
                base_pins.append(pin)
        else:
            base_pins.append(self.create_prev_pin())

        if flow_outputs:
            for pin in flow_outputs:
                if not pin.is_flow_outputs:
                    raise ValueError("Pin must be flow outputs")
                base_pins.append(pin)
        else:
            base_pins.append(self.create_next_pin())

        sig = signature(func)

        if data_inputs:
            for pin in data_inputs:
                if not pin.is_data_inputs:
                    raise ValueError("Pin must be data inputs")
                base_pins.append(pin)
        else:
            base_pins.extend(self.create_parameter_pins(list(sig.parameters.values())))

        if data_outputs:
            for pin in data_outputs:
                if not pin.is_data_outputs:
                    raise ValueError("Pin must be data outputs")
                base_pins.append(pin)
        else:
            base_pins.append(self.create_return_annotation_pin(sig.return_annotation))

        return NodeTemplate(
            name=base_name,
            path=base_path,
            func=func,
            docs=base_docs,
            icon=base_icon,
            color=base_color,
            pins=base_pins,
            tags=base_tags,
        )

    def add_new_type(
        self,
        base: type,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
    ):
        dtype = self.create_dtype(
            base=base,
            name=name,
            path=path,
            docs=docs,
            icon=icon,
            color=color,
        )
        self.add_dtype(dtype)

    def add_new_callable(
        self,
        func: Callable,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
        flow_inputs: Optional[List[PinTemplate]] = None,
        flow_outputs: Optional[List[PinTemplate]] = None,
        data_inputs: Optional[List[PinTemplate]] = None,
        data_outputs: Optional[List[PinTemplate]] = None,
        tags: Optional[List[str]] = None,
    ):
        node = self.create_node(
            func=func,
            name=name,
            path=path,
            docs=docs,
            icon=icon,
            color=color,
            flow_inputs=flow_inputs,
            flow_outputs=flow_outputs,
            data_inputs=data_inputs,
            data_outputs=data_outputs,
            tags=tags,
        )
        self.add_node(node)

    def register_dtype(
        self,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
    ):
        def _decorator(base: type):
            self.add_new_type(
                base=base,
                name=name,
                path=path,
                docs=docs,
                icon=icon,
                color=color,
            )
            return base

        return _decorator

    def register_node(
        self,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
        flow_inputs: Optional[List[PinTemplate]] = None,
        flow_outputs: Optional[List[PinTemplate]] = None,
        data_inputs: Optional[List[PinTemplate]] = None,
        data_outputs: Optional[List[PinTemplate]] = None,
        tags: Optional[List[str]] = None,
    ):
        def _decorator(func: Callable):
            self.add_new_callable(
                func=func,
                name=name,
                path=path,
                docs=docs,
                icon=icon,
                color=color,
                flow_inputs=flow_inputs,
                flow_outputs=flow_outputs,
                data_inputs=data_inputs,
                data_outputs=data_outputs,
                tags=tags,
            )
            return func

        return _decorator
