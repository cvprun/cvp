# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/stdtypes.html

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
import typing
import weakref


def get_builtin_types() -> typing.List[type]:
    return [
        type(None),
        int,
        float,
        complex,
        bool,
        list,
        tuple,
        range,
        bytes,
        bytearray,
        set,
        frozenset,
        dict,
        str,
        memoryview,
        object,
        type(Ellipsis),
        type(NotImplemented),
        collections.ChainMap,
        collections.Counter,
        collections.OrderedDict,
        collections.abc.AsyncGenerator,
        collections.abc.AsyncIterable,
        collections.abc.AsyncIterator,
        collections.abc.Awaitable,
        collections.abc.ByteString,  # type: ignore[list-item]
        collections.abc.Callable,  # type: ignore[list-item]
        collections.abc.Collection,
        collections.abc.Container,
        collections.abc.Coroutine,
        collections.abc.Generator,
        collections.abc.ItemsView,
        collections.abc.Iterable,
        collections.abc.Iterator,
        collections.abc.KeysView,
        collections.abc.Mapping,
        collections.abc.MappingView,
        collections.abc.MutableMapping,
        collections.abc.MutableSequence,
        collections.abc.MutableSet,
        collections.abc.Reversible,
        collections.abc.Sequence,
        collections.abc.Set,
        collections.abc.ValuesView,
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
        typing.Any,  # type: ignore[list-item]
    ]
