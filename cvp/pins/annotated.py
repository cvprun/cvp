# -*- coding: utf-8 -*-

from typing import Any, List, Optional, Sequence

from cvp.inspect.parameter import NoDefault
from cvp.pins.action import Action
from cvp.pins.stream import Stream


class PinAnnotated:
    pass


class PinName(PinAnnotated):
    def __init__(self, name: str):
        self.name = name


class PinDocs(PinAnnotated):
    def __init__(self, docs: str):
        self.docs = docs


class PinAction(PinAnnotated):
    def __init__(self, action: Action):
        self.action = action


class PinData(PinAction):
    def __init__(self):
        super().__init__(Action.data)


class PinFlow(PinAction):
    def __init__(self):
        super().__init__(Action.flow)


class PinStream(PinAnnotated):
    def __init__(self, stream: Stream):
        self.stream = stream


class PinInput(PinStream):
    def __init__(self):
        super().__init__(Stream.input)


class PinOutput(PinStream):
    def __init__(self):
        super().__init__(Stream.output)


class PinRequired(PinAnnotated):
    def __init__(self, required=True):
        self.required = required


class PinOptional(PinRequired):
    def __init__(self, optional=True):
        super().__init__(not optional)


class PinArcs(PinAnnotated):
    def __init__(self, arcs: Sequence[str]):
        self.arcs = list(arcs)


class PinArc(PinAnnotated):
    def __init__(self, arc: str):
        self.arc = arc


class PinDefault(PinAnnotated):
    def __init__(self, default: Any):
        self.default = default


class PinNoDefault(PinDefault):
    def __init__(self):
        super().__init__(NoDefault)


def get_name(*args, default: Optional[str] = None) -> str:
    for arg in args:
        if isinstance(arg, PinName):
            return arg.name
    return default if default else str()


def get_docs(*args, default: Optional[str] = None) -> str:
    for arg in args:
        if isinstance(arg, PinDocs):
            return arg.docs
    return default if default else str()


def get_action(*args, default: Action) -> Action:
    for arg in args:
        if isinstance(arg, PinAction):
            return arg.action
        elif isinstance(arg, Action):
            return arg
    return default


def get_stream(*args, default: Stream) -> Stream:
    for arg in args:
        if isinstance(arg, PinStream):
            return arg.stream
        elif isinstance(arg, Stream):
            return arg
    return default


def get_required(*args, default: Optional[bool] = None) -> bool:
    for arg in args:
        if isinstance(arg, PinRequired):
            return arg.required
    return bool(default)


def get_arcs(*args) -> List[str]:
    result = list()
    for arg in args:
        if isinstance(arg, PinArcs):
            result.extend(arg.arcs)
        elif isinstance(arg, PinArc):
            result.append(arg.arc)
    return result


def get_default(*args, default: Any = NoDefault) -> Any:
    for arg in args:
        if isinstance(arg, PinDefault):
            return arg.default
    return default
