# -*- coding: utf-8 -*-

import collections
import contextlib
import dataclasses
import decimal
import fractions
import functools
import numbers
import os
import queue
import re
import shelve
import types
import weakref
from functools import lru_cache
from typing import Sequence, Type

from cvp.dtypes.dtype import Dtype


@lru_cache
def get_standard_types() -> Sequence[Type]:
    return (
        collections.ChainMap,
        collections.Counter,
        collections.OrderedDict,
        collections.defaultdict,
        collections.deque,
        contextlib.AbstractAsyncContextManager,
        contextlib.AbstractContextManager,
        dataclasses.Field,
        decimal.Decimal,
        fractions.Fraction,
        functools.cached_property,
        functools.partialmethod,
        numbers.Complex,
        numbers.Integral,
        numbers.Number,
        numbers.Rational,
        numbers.Real,
        os.PathLike,
        queue.LifoQueue,
        queue.PriorityQueue,
        queue.Queue,
        queue.SimpleQueue,
        re.Match,
        re.Pattern,
        shelve.BsdDbShelf,
        shelve.DbfilenameShelf,
        shelve.Shelf,
        types.MappingProxyType,
        types.ModuleType,
        weakref.WeakKeyDictionary,
        weakref.WeakMethod,
        weakref.WeakSet,
        weakref.WeakValueDictionary,
    )


@lru_cache
def get_standard_dtypes() -> Sequence[Dtype]:
    return tuple(Dtype(cls, hidden=True) for cls in get_standard_types())
