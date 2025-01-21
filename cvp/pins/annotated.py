# -*- coding: utf-8 -*-

from typing import List, Optional, Sequence


class PinAnnotated:
    pass


class PinName(PinAnnotated):
    def __init__(self, name: str):
        self.name = name


class PinDocs(PinAnnotated):
    def __init__(self, docs: str):
        self.docs = docs


class PinRequired(PinAnnotated):
    def __init__(self, required: bool):
        self.required = required


class PinArcs(PinAnnotated):
    def __init__(self, arcs: Sequence[str]):
        self.arcs = list(arcs)


class PinArc(PinAnnotated):
    def __init__(self, arc: str):
        self.arc = arc


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
        if isinstance(arg, PinArc):
            result.append(arg.arc)
    return result
