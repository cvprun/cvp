# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Generic, Optional, TypeVar

from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.renderer.context import RendererContext
from cvp.renderer.widget.interface import WidgetInterface
from cvp.types.override import override

ItemT = TypeVar("ItemT")


class TabItem(Generic[ItemT], WidgetInterface):
    _item: Optional[ItemT]

    def __init__(
        self,
        context: Context,
        label: Optional[str] = None,
        opened: Optional[bool] = None,
        flags=0,
    ):
        self._context = context
        self._label = label if label else type(self).__name__
        self._opened = opened
        self._flags = flags
        self._item = None

    @property
    def context(self):
        assert isinstance(self._context, RendererContext)
        return self._context

    @property
    def label(self):
        return self._label

    @property
    def item(self):
        return self._item

    def begin(self):
        return imgui.begin_tab_item(self._label, self._opened, self._flags)

    def end(self) -> None:
        assert self
        imgui.end_tab_item()

    def do_process(self, item: Optional[ItemT] = None) -> None:
        if not self.begin().selected:
            return

        self._item = item
        try:
            self.on_process()
        finally:
            self._item = None
            self.end()

    @override
    def on_process(self) -> None:
        if self._item is not None:
            self.on_item(self._item)
        else:
            self.on_none()

    def on_item(self, item: ItemT) -> None:
        pass

    def on_none(self) -> None:
        pass


class TabBar(Generic[ItemT], WidgetInterface):
    _items: OrderedDict[str, TabItem]
    _item: Optional[ItemT]

    def __init__(
        self,
        context: Context,
        identifier: Optional[str] = None,
        flags=0,
    ):
        self._context = context
        self._identifier = identifier if identifier else type(self).__name__
        self._flags = flags
        self._items = OrderedDict()
        self._item = None

    @property
    def context(self):
        return self._context

    @property
    def identifier(self):
        return self._identifier

    @property
    def item(self):
        return self._item

    def register(self, item: TabItem) -> None:
        self._items[item.label] = item

    def begin(self):
        return imgui.begin_tab_bar(self._identifier, self._flags)

    def end(self) -> None:
        assert self
        imgui.end_tab_bar()

    def do_process(self, item: Optional[ItemT] = None) -> None:
        if not self.begin().opened:
            return

        self._item = item
        try:
            self.on_process()
        finally:
            self._item = None
            self.end()

    @override
    def on_process(self) -> None:
        for item in self._items.values():
            item.do_process(self._item)
